"""LangGraph v2 — planner + dynamic fan-out + sub-question grading + critic.

This module is independent from knowledge_graph.py (v1). The API can select it
with graph_version="v2"; v1 remains the fallback.

Flow:
  parse_intent -> clarify (interrupt) | plan (LLM)
  plan -> Send(retrieve_subquestion × N) -> join_sub_results
  join -> grade_subquestions
  grade -> reformulate_subquestions (missing only, max 2 rounds) | synthesize
  synthesize -> validate -> critique (LLM) -> repair (once) | human_review | format
"""
import copy
import json
import operator
import re
import sqlite3
import sys
import uuid
from pathlib import Path
from typing import Annotated, Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Send, interrupt

from agents.base_agent import BaseAgent
from agents.knowledge_agent import KnowledgeAgent

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from tools.data_tools import (  # noqa: E402
    get_competitor_products,
    get_currency_rate,
    get_hot_search_categories,
    get_logistics_cost,
    get_market_summary,
    get_platform_fees,
)

VERDICT_ENUM = {"推荐", "谨慎", "不建议", "信息不足"}
REQUIRED_FIELDS = ("verdict", "summary", "evidence", "compliance_checklist", "unknowns")
VAGUE_MARKERS = ("这个", "这款", "该产品", "我的产品", "this product", "produk ini")
CHECKPOINT_DIR = BACKEND_ROOT / "checkpoints"
CHECKPOINT_DB = CHECKPOINT_DIR / "knowledge_v2.sqlite"

PLAN_SYSTEM_PROMPT = """你是跨境电商合规助手的任务规划器。
把用户问题拆成最多 4 个可独立检索的子问题。
每个子问题必须选择来源：
- policy：法规、认证、平台规则、许可、标签、清关
- market：市场趋势、竞品、价格、销量
- numeric：利润、成本、汇率、平台费率
只拆用户真正需要的部分；同一主题不要拆成多个子问题；不同来源可以保留。
不要生成答案；不要输出证据之外的事实。
严格按给定 JSON Schema 输出。"""

CRITIC_SYSTEM_PROMPT = """你是 RAG 答案的事实审查员。
只依据输入证据审查答案，不引入外部知识。
检查：
1. unsupported_claims：答案中是否有证据不支持的断言
2. missing_exceptions：是否遗漏证据中的例外、范围或条件
3. date_scope_issues：日期、生效范围、适用国家/平台是否错误
4. citation_issues：引用是否不支撑对应 claim
5. verdict_ok：verdict 是否与证据强度匹配

只列出确定的问题。不要列出“已覆盖”“不构成错误”“仅提示”的说明；
如果没有问题，所有数组必须为空，verdict_ok 为 true。
严格按给定 JSON Schema 输出。"""

PLAN_SCHEMA = {
    "name": "knowledge_plan",
    "schema": {
        "type": "object",
        "properties": {
            "sub_questions": {
                "type": "array",
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "question": {"type": "string"},
                        "source": {"type": "string", "enum": ["policy", "market", "numeric"]},
                        "required": {"type": "boolean"},
                    },
                    "required": ["id", "question", "source"],
                },
            },
            "needs_clarification": {"type": "boolean"},
        },
        "required": ["sub_questions"],
    },
}

CRITIC_SCHEMA = {
    "name": "knowledge_critique",
    "schema": {
        "type": "object",
        "properties": {
            "unsupported_claims": {"type": "array", "items": {"type": "string"}},
            "missing_exceptions": {"type": "array", "items": {"type": "string"}},
            "date_scope_issues": {"type": "array", "items": {"type": "string"}},
            "citation_issues": {"type": "array", "items": {"type": "string"}},
            "verdict_ok": {"type": "boolean"},
            "reason": {"type": "string"},
        },
        "required": ["unsupported_claims", "citation_issues", "verdict_ok", "reason"],
    },
}


def merge_sub_results(left: list[dict] | None, right: list[dict] | None) -> list[dict]:
    by_id = {item["sub_question_id"]: item for item in (left or [])}
    for item in right or []:
        by_id[item["sub_question_id"]] = item
    return list(by_id.values())


def merge_evidence(left: list[dict] | None, right: list[dict] | None) -> list[dict]:
    by_id: dict[str, dict] = {}
    for item in (left or []) + (right or []):
        key = item.get("chunk_id") or f"{item.get('citation_doc_id')}:{item.get('clause_id')}:{item.get('page')}"
        previous = by_id.get(key)
        if previous is None:
            by_id[key] = dict(item)
        else:
            if float(item.get("score", 0)) >= float(previous.get("score", 0)):
                merged = dict(previous)
                merged.update(item)
                by_id[key] = merged
    return list(by_id.values())


def merge_dict(left: dict | None, right: dict | None) -> dict:
    return {**(left or {}), **(right or {})}


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "").lower()


def _build_checkpointer():
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver

        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(CHECKPOINT_DB), check_same_thread=False)
        return SqliteSaver(conn)
    except Exception:
        return MemorySaver()


class KnowledgeGraphState(TypedDict, total=False):
    # input
    query: str
    country: str | None
    platform: str | None
    top_k: int
    mode: str
    rerank: bool | None
    rerank_pool: int
    session_id: str
    require_review: bool

    # intent / plan
    intent: dict
    needs_clarification: bool
    follow_ups: list[str]
    clarification: str
    needs_human_review: bool
    sub_questions: list[dict]
    pending_sub_questions: list[dict]
    retrieval_round: int
    planner_meta: dict

    # retrieval map-reduce
    sub_results: Annotated[list[dict], merge_sub_results]
    evidence: Annotated[list[dict], merge_evidence]
    numeric_data: Annotated[dict, merge_dict]
    retrieval_meta: Annotated[dict, merge_dict]
    sub_grades: list[dict]
    missing_sub_questions: list[dict]
    coverage: float
    recency: float
    conflicts: list[dict]
    evidence_sufficient: bool

    # generation / critique
    draft: dict
    generation_meta: dict
    critique: dict
    critique_issues: list[str]
    critic_meta: dict
    repair_attempts: int

    # review
    review_decision: dict

    # output
    validation: dict
    final: dict
    status: str
    errors: Annotated[list[str], operator.add]


class KnowledgeGraphRunnerV2:
    def __init__(self, agent: KnowledgeAgent):
        self.agent = agent
        self.planner = BaseAgent("KnowledgePlanner", PLAN_SYSTEM_PROMPT)
        self.critic = BaseAgent("KnowledgeCritic", CRITIC_SYSTEM_PROMPT)
        self.checkpointer = _build_checkpointer()
        self.graph = self._build()

    # ── planning ──

    def parse_intent(self, state: KnowledgeGraphState) -> dict:
        query = state["query"].strip()
        country = (state.get("country") or "").strip() or None
        platform = (state.get("platform") or "").strip() or None
        vague = any(marker in query.lower() for marker in VAGUE_MARKERS)
        needs_clarification = vague and not country and not platform
        follow_ups = [
            "目标国家/市场是什么？",
            "目标平台是什么（Shopee/Lazada/TikTok Shop 等）？",
            "具体产品、材质或用途是什么？",
        ] if needs_clarification else []
        return {
            "intent": {"query": query, "country": country, "platform": platform},
            "needs_clarification": needs_clarification,
            "needs_human_review": bool(state.get("require_review", False)),
            "follow_ups": follow_ups,
        }

    def clarify(self, state: KnowledgeGraphState) -> dict:
        answer = interrupt({
            "type": "clarify",
            "question": state["query"],
            "follow_ups": state.get("follow_ups", []),
        })
        clarification = answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False)
        return {"clarification": clarification, "needs_clarification": False}

    def _fallback_plan(self, query: str) -> list[dict]:
        sub_questions = [{
            "id": "sq1", "question": query, "source": "policy", "required": True,
        }]
        if any(k in query for k in ("市场", "趋势", "竞品", "销量", "价格", "market", "trend", "price")):
            sub_questions.append({
                "id": f"sq{len(sub_questions) + 1}",
                "question": f"{query} 市场趋势与竞品",
                "source": "market",
                "required": True,
            })
        if any(k in query for k in ("利润", "成本", "汇率", "费用", "profit", "cost", "fx")):
            sub_questions.append({
                "id": f"sq{len(sub_questions) + 1}",
                "question": f"{query} 成本与利润",
                "source": "numeric",
                "required": True,
            })
        return sub_questions[:4]

    def _sanitize_plan(self, data: dict, query: str) -> tuple[list[dict], int]:
        rows = data.get("sub_questions") or []
        result = []
        seen_ids = set()
        for i, row in enumerate(rows[:8], 1):
            if not isinstance(row, dict):
                continue
            source = row.get("source")
            question = str(row.get("question", "")).strip()
            if source not in ("policy", "market", "numeric") or not question:
                continue
            item_id = str(row.get("id") or f"sq{i}")
            if item_id in seen_ids:
                item_id = f"sq{i}"
            seen_ids.add(item_id)
            result.append({
                "id": item_id,
                "question": question,
                "source": source,
                "required": bool(row.get("required", True)),
            })
        if not result:
            return self._fallback_plan(query), 0
        if not any(item["source"] == "policy" for item in result):
            result.insert(0, {
                "id": "sq0", "question": query, "source": "policy", "required": True,
            })
        deduped = self._dedupe_sub_questions(result)
        return deduped[:4], max(0, len(result) - len(deduped))

    @staticmethod
    def _question_tokens(text: str) -> set[str]:
        text = text.lower()
        words = set(re.findall(r"[a-z0-9]{2,}", text))
        cjk = re.findall(r"[一-鿿]", text)
        return words | set(cjk) | {"".join(cjk[i:i + 2]) for i in range(len(cjk) - 1)}

    def _dedupe_sub_questions(self, rows: list[dict]) -> list[dict]:
        """Merge same-source questions that are exact duplicates, containments,
        or near-duplicates (Jaccard >= 0.8). Different sources are kept."""
        kept: list[dict] = []
        for row in rows:
            duplicate_index = None
            row_norm = _norm(row["question"])
            row_tokens = self._question_tokens(row["question"])
            for i, existing in enumerate(kept):
                if row["source"] != existing["source"]:
                    continue
                existing_norm = _norm(existing["question"])
                if (row_norm in existing_norm or existing_norm in row_norm):
                    duplicate_index = i
                    break
                existing_tokens = self._question_tokens(existing["question"])
                union = row_tokens | existing_tokens
                intersection = row_tokens & existing_tokens
                jaccard = len(intersection) / len(union) if union else 0.0
                overlap = len(intersection) / min(len(row_tokens), len(existing_tokens)) if row_tokens and existing_tokens else 0.0
                if jaccard >= 0.8 or overlap >= 0.85:
                    duplicate_index = i
                    break
            if duplicate_index is None:
                kept.append(row)
                continue
            # Keep the longer/more specific question.
            if len(row["question"]) > len(kept[duplicate_index]["question"]):
                kept[duplicate_index] = row
        return kept

    def _planner_plan(self, query: str, state: KnowledgeGraphState) -> tuple[list[dict], dict]:
        prompt = (
            f"用户问题：{query}\n"
            f"目标国家：{state.get('country') or '未指定'}\n"
            f"目标平台：{state.get('platform') or '未指定'}\n"
            "请拆解为最多 4 个子问题，并选择 policy / market / numeric 来源。"
        )
        try:
            data = self.planner.run(prompt, output_schema=PLAN_SCHEMA)
            if isinstance(data, dict) and not data.get("mock") and data.get("sub_questions"):
                sub_questions, dropped = self._sanitize_plan(data, query)
                return sub_questions, {
                    "mode": "llm", "model": self.planner.model, "mock": False,
                    "dropped_duplicates": dropped,
                }
        except Exception as exc:
            return self._fallback_plan(query), {
                "mode": "fallback", "error": str(exc)[:300],
            }
        return self._fallback_plan(query), {"mode": "fallback", "reason": "no valid plan"}

    def plan(self, state: KnowledgeGraphState) -> dict:
        query = state["query"]
        if state.get("clarification"):
            query = f"{query} {state['clarification']}"
        sub_questions, planner_meta = self._planner_plan(query, state)
        return {
            "query": query,
            "sub_questions": sub_questions,
            "pending_sub_questions": [],
            "retrieval_round": 0,
            "repair_attempts": 0,
            "sub_results": [],
            "evidence": [],
            "numeric_data": {},
            "retrieval_meta": {},
            "planner_meta": planner_meta,
            "errors": [],
        }

    # ── dynamic retrieval ──

    def route_after_plan(self, state: KnowledgeGraphState):
        pending = state.get("pending_sub_questions") or state.get("sub_questions") or []
        if not pending:
            return "synthesize"
        return [
            Send("retrieve_subquestion", {
                "sub_question": sq,
                "query": state["query"],
                "country": state.get("country"),
                "platform": state.get("platform"),
                "top_k": state.get("top_k", 5),
                "mode": state.get("mode", "auto"),
                "rerank": state.get("rerank"),
                "rerank_pool": state.get("rerank_pool", 50),
            })
            for sq in pending
        ]

    def retrieve_subquestion(self, state: KnowledgeGraphState) -> dict:
        sq = state["sub_question"]
        source = sq["source"]
        country = state.get("country") or "id"
        platform = state.get("platform")
        try:
            if source == "policy":
                evidence, meta = self.agent.retrieve(
                    sq["question"], country=state.get("country"), platform=platform,
                    top_k=state.get("top_k", 5), mode=state.get("mode", "auto"),
                    rerank=state.get("rerank"), rerank_pool=state.get("rerank_pool", 50),
                )
                for item in evidence:
                    item["sub_question_id"] = sq["id"]
                    item["source"] = source
                return {
                    "sub_results": [{
                        "sub_question_id": sq["id"], "question": sq["question"],
                        "source": source, "evidence": evidence,
                        "numeric_data": {}, "retrieval_meta": meta, "error": None,
                    }],
                }
            if source == "market":
                data = {
                    "market": get_market_summary(country),
                    "hot_categories": get_hot_search_categories(country, 5),
                    "competitors": get_competitor_products(limit=5),
                }
                return {
                    "sub_results": [{
                        "sub_question_id": sq["id"], "question": sq["question"],
                        "source": source, "evidence": [], "numeric_data": {"market": data},
                        "retrieval_meta": {"source": "data_tools"}, "error": None,
                    }],
                }
            if source == "numeric":
                data = {
                    "fees": get_platform_fees(platform or "shopee", 100),
                    "logistics": get_logistics_cost(country, 0.3),
                    "fx": get_currency_rate(country),
                }
                return {
                    "sub_results": [{
                        "sub_question_id": sq["id"], "question": sq["question"],
                        "source": source, "evidence": [], "numeric_data": {"numeric": data},
                        "retrieval_meta": {"source": "data_tools"}, "error": None,
                    }],
                }
            raise ValueError(f"Unknown source: {source}")
        except Exception as exc:
            return {
                "sub_results": [{
                    "sub_question_id": sq["id"], "question": sq["question"],
                    "source": source, "evidence": [], "numeric_data": {},
                    "retrieval_meta": {}, "error": str(exc)[:300],
                }],
                "errors": [str(exc)],
            }

    def join_sub_results(self, state: KnowledgeGraphState) -> dict:
        sub_results = state.get("sub_results", [])
        evidence = []
        numeric_data = {}
        meta = {}
        for result in sub_results:
            meta[result["sub_question_id"]] = result.get("retrieval_meta", {})
            numeric_data.update(result.get("numeric_data", {}))
            for item in result.get("evidence", []):
                item = dict(item)
                item["sub_question_id"] = result["sub_question_id"]
                evidence.append(item)
        for i, item in enumerate(evidence, 1):
            item["evidence_id"] = f"E{i}"
        return {
            "evidence": evidence,
            "numeric_data": numeric_data,
            "retrieval_meta": meta,
        }

    def grade_subquestions(self, state: KnowledgeGraphState) -> dict:
        sub_questions = state.get("sub_questions", [])
        results = {r["sub_question_id"]: r for r in state.get("sub_results", [])}
        grades = []
        missing = []
        covered_required = 0
        required_total = 0
        recency_values = []
        conflicts = []

        for sq in sub_questions:
            result = results.get(sq["id"], {})
            source = sq["source"]
            evidence = result.get("evidence", [])
            if source == "policy":
                coverage = min(1.0, len(evidence) / 2.0)
                recencies = []
                versions: dict[str, dict[str, set]] = {}
                for item in evidence:
                    effective_from = str(item.get("effective_from", "unknown"))
                    recencies.append(1.0 if effective_from and effective_from != "unknown" else 0.5)
                    title = item.get("title") or item.get("citation_doc_id") or "unknown"
                    bucket = versions.setdefault(title, {"dates": set(), "docs": set()})
                    if effective_from and effective_from != "unknown":
                        bucket["dates"].add(effective_from)
                    bucket["docs"].add(item.get("citation_doc_id") or item.get("doc_id"))
                recency = sum(recencies) / len(recencies) if recencies else 0.0
                for title, bucket in versions.items():
                    if len(bucket["dates"]) > 1 or len(bucket["docs"]) > 1:
                        conflicts.append({
                            "sub_question_id": sq["id"], "title": title,
                            "effective_dates": sorted(bucket["dates"]),
                            "doc_ids": sorted(str(doc) for doc in bucket["docs"]),
                        })
                sufficient = coverage >= 0.6 and not result.get("error")
            else:
                data = result.get("numeric_data", {})
                coverage = 1.0 if data else 0.0
                recency = 1.0 if data else 0.0
                sufficient = bool(data) and not result.get("error")
            recency_values.append(recency)
            grades.append({
                "sub_question_id": sq["id"],
                "question": sq["question"],
                "source": source,
                "evidence_count": len(evidence),
                "coverage": round(coverage, 3),
                "recency": round(recency, 3),
                "sufficient": sufficient,
                "error": result.get("error"),
            })
            if sq.get("required", True):
                required_total += 1
                if sufficient:
                    covered_required += 1
                else:
                    missing.append(sq)

        coverage = covered_required / required_total if required_total else 0.0
        recency = sum(recency_values) / len(recency_values) if recency_values else 0.0
        return {
            "sub_grades": grades,
            "missing_sub_questions": missing,
            "coverage": round(coverage, 3),
            "recency": round(recency, 3),
            "conflicts": conflicts,
            "needs_human_review": state.get("needs_human_review", False) or bool(conflicts),
            "evidence_sufficient": coverage >= 0.6,
        }

    def reformulate_subquestions(self, state: KnowledgeGraphState) -> dict:
        pending = []
        for sq in state.get("missing_sub_questions", []):
            item = dict(sq)
            if item["source"] == "policy":
                item["question"] = f"{item['question']} {state['query']}"
            pending.append(item)
        return {
            "pending_sub_questions": pending,
            "retrieval_round": int(state.get("retrieval_round", 0)) + 1,
            "platform": None,
            "top_k": max(int(state.get("top_k", 5)), 8),
        }

    def route_after_grade(self, state: KnowledgeGraphState) -> str:
        if state.get("missing_sub_questions") and int(state.get("retrieval_round", 0)) < 2:
            return "reformulate_subquestions"
        return "synthesize"

    def route_after_reformulate(self, state: KnowledgeGraphState):
        pending = state.get("pending_sub_questions") or []
        if not pending:
            return "synthesize"
        return [
            Send("retrieve_subquestion", {
                "sub_question": sq,
                "query": state["query"],
                "country": state.get("country"),
                "platform": state.get("platform"),
                "top_k": state.get("top_k", 8),
                "mode": state.get("mode", "auto"),
                "rerank": state.get("rerank"),
                "rerank_pool": state.get("rerank_pool", 50),
            })
            for sq in pending
        ]

    # ── synthesis, validation, critic ──

    def synthesize(self, state: KnowledgeGraphState) -> dict:
        evidence = state.get("evidence", [])
        if not evidence:
            draft = {
                "verdict": "信息不足",
                "summary": "未检索到相关证据。",
                "evidence": [],
                "compliance_checklist": [],
                "unknowns": ["语料未覆盖该问题或检索无结果"],
                "follow_up_questions": [],
            }
            return {"draft": draft, "generation_meta": {"generation_status": "no_evidence"}}
        context = {
            "sub_questions": state.get("sub_questions", []),
            "sub_grades": state.get("sub_grades", []),
            "missing_sub_questions": state.get("missing_sub_questions", []),
            "numeric_data": state.get("numeric_data", {}),
            "coverage": state.get("coverage", 0),
            "recency": state.get("recency", 0),
            "conflicts": state.get("conflicts", []),
            "critique": state.get("critique", ""),
        }
        draft, meta = self.agent.answer_from_evidence(state["query"], evidence, context=context)
        return {"draft": draft, "generation_meta": meta}

    def validate(self, state: KnowledgeGraphState) -> dict:
        draft = copy.deepcopy(state.get("draft") or {})
        evidence = state.get("evidence", [])
        blocking, warnings = [], []
        for field in REQUIRED_FIELDS:
            if field not in draft:
                blocking.append(f"缺少必填字段: {field}")
        if draft.get("verdict") not in VERDICT_ENUM:
            blocking.append(f"verdict 非法: {draft.get('verdict')!r}")
        by_doc: dict[str, list[str]] = {}
        for item in evidence:
            doc_id = item.get("citation_doc_id") or item.get("doc_id")
            by_doc.setdefault(doc_id, []).append(item.get("content", ""))
        cited = draft.get("evidence") or []
        if evidence and not cited:
            warnings.append("检索到证据但答案未引用任何证据")
        for i, item in enumerate(cited, 1):
            doc_id = item.get("doc_id")
            if doc_id not in by_doc:
                blocking.append(f"evidence[{i}] 引用了未检索到的 doc_id: {doc_id}")
                continue
            quote = item.get("quote") or ""
            if quote and not any(_norm(quote) in _norm(content) for content in by_doc[doc_id]):
                # A paraphrased or wrong quote is worse than no quote.
                item["quote"] = ""
                warnings.append(f"evidence[{i}] 的 quote 无法在原文中找到，已移除")
        if not evidence and draft.get("verdict") != "信息不足":
            blocking.append("无检索证据时 verdict 必须为「信息不足」")
        return {
            "draft": draft,
            "validation": {"passed": not blocking, "blocking": blocking, "warnings": warnings},
        }

    def critique(self, state: KnowledgeGraphState) -> dict:
        if self.critic.use_mock:
            return {
                "critique": {}, "critique_issues": [],
                "critic_meta": {"mock": True, "status": "skipped"},
            }
        evidence = state.get("evidence", [])
        evidence_text = "\n\n".join(
            f"[{item.get('evidence_id', f'E{i}')}] {item.get('content', '')[:800]}"
            for i, item in enumerate(evidence, 1)
        )
        prompt = (
            f"用户问题：{state['query']}\n\n"
            f"子问题评分：{json.dumps(state.get('sub_grades', []), ensure_ascii=False)}\n\n"
            f"缺失子问题：{json.dumps(state.get('missing_sub_questions', []), ensure_ascii=False)}\n\n"
            f"当前答案：{json.dumps(state.get('draft', {}), ensure_ascii=False)}\n\n"
            f"确定性校验：{json.dumps(state.get('validation', {}), ensure_ascii=False)}\n\n"
            f"证据：\n{evidence_text}\n\n"
            "请只审查当前答案是否被证据支持，输出 JSON。"
        )
        try:
            result = self.critic.run(prompt, output_schema=CRITIC_SCHEMA)
            if not isinstance(result, dict) or result.get("mock"):
                raise ValueError("critic returned no structured result")
            issues = []
            for field in ("unsupported_claims", "missing_exceptions", "date_scope_issues", "citation_issues"):
                issues.extend(str(item) for item in result.get(field, []))
            if result.get("verdict_ok") is False:
                issues.append("verdict 与证据强度不匹配")
            return {
                "critique": result, "critique_issues": issues,
                "critic_meta": {"model": self.critic.model, "status": "scored"},
            }
        except Exception as exc:
            return {
                "critique": {}, "critique_issues": [],
                "critic_meta": {"status": "failed", "error": str(exc)[:300]},
            }

    def repair(self, state: KnowledgeGraphState) -> dict:
        issues = list((state.get("validation") or {}).get("blocking", []))
        issues.extend((state.get("validation") or {}).get("warnings", []))
        issues.extend(state.get("critique_issues", []))
        return {
            "critique": "；".join(issues),
            "repair_attempts": int(state.get("repair_attempts", 0)) + 1,
            "draft": {},
        }

    def human_review(self, state: KnowledgeGraphState) -> dict:
        decision = interrupt({
            "type": "human_review",
            "question": state["query"],
            "draft": state.get("draft", {}),
            "validation": state.get("validation", {}),
            "coverage": state.get("coverage", 0),
            "recency": state.get("recency", 0),
            "conflicts": state.get("conflicts", []),
            "critique": state.get("critique", {}),
        })
        if isinstance(decision, dict):
            approved = bool(decision.get("approved"))
            comment = str(decision.get("comment", ""))
        else:
            text = str(decision).strip().lower()
            approved = text in {"approve", "approved", "yes", "y", "通过", "同意"}
            comment = str(decision)
        return {"review_decision": {"approved": approved, "comment": comment}}

    def format_output(self, state: KnowledgeGraphState) -> dict:
        validation = state.get("validation") or {}
        if validation.get("blocking"):
            return {
                "final": self.agent._mock_answer(state.get("evidence", [])),
                "status": "validation_failed",
            }
        final = state.get("draft", {})
        status = "degraded" if state.get("errors") else "done"
        review = state.get("review_decision") or {}
        if review and not review.get("approved"):
            final = dict(final)
            final["unknowns"] = list(final.get("unknowns", [])) + [
                f"人工审核未通过: {review.get('comment', '')}".strip()
            ]
            status = "review_rejected"
        return {"final": final, "status": status}

    # ── routing ──

    @staticmethod
    def route_after_intent(state: KnowledgeGraphState) -> str:
        return "clarify" if state.get("needs_clarification") else "plan"

    @staticmethod
    def route_after_validate(state: KnowledgeGraphState) -> str:
        blocking = (state.get("validation") or {}).get("blocking", [])
        if blocking and int(state.get("repair_attempts", 0)) < 1:
            return "repair"
        return "critique"

    @staticmethod
    def route_after_critique(state: KnowledgeGraphState) -> str:
        if state.get("critique_issues") and int(state.get("repair_attempts", 0)) < 1:
            return "repair"
        if state.get("needs_human_review") and not state.get("review_decision"):
            return "human_review"
        return "format"

    @staticmethod
    def route_after_review(state: KnowledgeGraphState) -> str:
        review = state.get("review_decision") or {}
        if review.get("approved"):
            return "format"
        if int(state.get("repair_attempts", 0)) < 1:
            return "repair"
        return "format"

    def _build(self):
        graph = StateGraph(KnowledgeGraphState)
        graph.add_node("parse_intent", self.parse_intent)
        graph.add_node("clarify", self.clarify)
        graph.add_node("plan", self.plan)
        graph.add_node("retrieve_subquestion", self.retrieve_subquestion)
        graph.add_node("join_sub_results", self.join_sub_results)
        graph.add_node("grade_subquestions", self.grade_subquestions)
        graph.add_node("reformulate_subquestions", self.reformulate_subquestions)
        graph.add_node("synthesize", self.synthesize)
        graph.add_node("validate", self.validate)
        graph.add_node("critique", self.critique)
        graph.add_node("repair", self.repair)
        graph.add_node("human_review", self.human_review)
        graph.add_node("format", self.format_output)

        graph.add_edge(START, "parse_intent")
        graph.add_conditional_edges(
            "parse_intent", self.route_after_intent,
            {"clarify": "clarify", "plan": "plan"},
        )
        graph.add_edge("clarify", "plan")
        graph.add_conditional_edges("plan", self.route_after_plan, ["retrieve_subquestion"])
        graph.add_edge("retrieve_subquestion", "join_sub_results")
        graph.add_edge("join_sub_results", "grade_subquestions")
        graph.add_conditional_edges(
            "grade_subquestions", self.route_after_grade,
            {"reformulate_subquestions": "reformulate_subquestions", "synthesize": "synthesize"},
        )
        graph.add_conditional_edges(
            "reformulate_subquestions", self.route_after_reformulate, ["retrieve_subquestion"],
        )
        graph.add_edge("synthesize", "validate")
        graph.add_conditional_edges(
            "validate", self.route_after_validate,
            {"repair": "repair", "critique": "critique"},
        )
        graph.add_conditional_edges(
            "critique", self.route_after_critique,
            {"repair": "repair", "human_review": "human_review", "format": "format"},
        )
        graph.add_edge("repair", "synthesize")
        graph.add_conditional_edges(
            "human_review", self.route_after_review,
            {"repair": "repair", "format": "format"},
        )
        graph.add_edge("format", END)
        return graph.compile(checkpointer=self.checkpointer)

    # ── public entry ──

    @staticmethod
    def _result_meta(result: dict, thread_id: str, status: str | None = None,
                     interrupt_payload: Any = None) -> dict:
        meta = {
            **result.get("retrieval_meta", {}),
            **result.get("generation_meta", {}),
            "graph": True,
            "graph_version": "v2",
            "thread_id": thread_id,
            "status": status or result.get("status", "done"),
            "sub_questions": result.get("sub_questions", []),
            "sub_grades": result.get("sub_grades", []),
            "missing_sub_questions": result.get("missing_sub_questions", []),
            "retrieval_round": result.get("retrieval_round", 0),
            "coverage": result.get("coverage", 0),
            "recency": result.get("recency", 0),
            "conflicts": result.get("conflicts", []),
            "numeric_data": result.get("numeric_data", {}),
            "planner_meta": result.get("planner_meta", {}),
            "critic_meta": result.get("critic_meta", {}),
            "critique_issues": result.get("critique_issues", []),
            "repair_attempts": result.get("repair_attempts", 0),
            "validation": result.get("validation", {}),
            "review_decision": result.get("review_decision", {}),
            "errors": result.get("errors", []),
        }
        if interrupt_payload is not None:
            meta["interrupt"] = interrupt_payload
        return meta

    def run(self, query: str, country: str | None = None,
            platform: str | None = None, top_k: int = 5,
            mode: str = "auto", rerank: bool | None = None,
            rerank_pool: int = 50, session_id: str | None = None,
            require_review: bool = False,
            resume: Any = None) -> tuple[dict, dict]:
        thread_id = session_id or uuid.uuid4().hex
        config = {"configurable": {"thread_id": thread_id}}
        if resume is not None:
            result = self.graph.invoke(Command(resume=resume), config=config)
        else:
            state: KnowledgeGraphState = {
                "query": query, "country": country, "platform": platform,
                "top_k": top_k, "mode": mode, "rerank": rerank,
                "rerank_pool": rerank_pool, "session_id": thread_id,
                "require_review": require_review, "errors": [],
            }
            result = self.graph.invoke(state, config=config)

        interrupts = result.get("__interrupt__") or []
        if interrupts:
            payload = getattr(interrupts[0], "value", interrupts[0])
            kind = payload.get("type") if isinstance(payload, dict) else None
            if kind == "clarify":
                final = {
                    "verdict": "信息不足",
                    "summary": "需要补充目标市场、平台或产品信息后才能给出有依据的判断。",
                    "evidence": [],
                    "compliance_checklist": [],
                    "unknowns": ["缺少目标国家/平台/产品信息"],
                    "follow_up_questions": payload.get("follow_ups", []),
                }
                return final, self._result_meta(result, thread_id, "needs_clarification", payload)
            final = payload.get("draft", {}) if isinstance(payload, dict) else {}
            return final, self._result_meta(result, thread_id, "needs_review", payload)

        final = result.get("final") or {
            "verdict": "信息不足",
            "summary": "工作流未产生结果。",
            "evidence": [],
            "compliance_checklist": [],
            "unknowns": ["graph returned no final output"],
            "follow_up_questions": [],
        }
        return final, self._result_meta(result, thread_id)


def create_knowledge_graph_v2(agent: KnowledgeAgent | None = None) -> KnowledgeGraphRunnerV2:
    return KnowledgeGraphRunnerV2(agent or KnowledgeAgent())
