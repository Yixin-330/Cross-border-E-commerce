"""LangGraph workflow for the KnowledgeAgent.

Flow:
  parse_intent -> clarify (interrupt) | plan
  plan -> retrieve_policy | retrieve_market | retrieve_numeric (parallel)
       -> merge_evidence -> grade_evidence
  grade_evidence -> reformulate (up to 2 attempts) | synthesize
  synthesize -> validate
  validate -> repair (once) | human_review (interrupt) | format
  human_review -> repair | format

The graph reuses KnowledgeAgent.retrieve() and answer_from_evidence(); it does
not duplicate the RAG layer. A SQLite checkpointer persists thread state so
clarification and human review can be resumed.
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
from langgraph.types import Command, interrupt

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
STOPWORDS = {
    "什么", "怎么", "如何", "是否", "可以", "需要", "哪些", "有关", "关于",
    "这个", "这款", "该产品", "我的产品", "apa", "yang", "dan", "untuk",
    "dengan", "bagaimana", "apakah", "bisa", "tidak", "dari", "pada", "adalah",
}
CHECKPOINT_DIR = BACKEND_ROOT / "checkpoints"
CHECKPOINT_DB = CHECKPOINT_DIR / "knowledge.sqlite"


def merge_evidence(left: list[dict] | None, right: list[dict] | None) -> list[dict]:
    """Deduplicate parallel retrieval branches by chunk_id, keeping the best score."""
    by_id: dict[str, dict] = {}
    for item in (left or []) + (right or []):
        key = item.get("chunk_id") or (
            f"{item.get('citation_doc_id')}:{item.get('clause_id')}:{item.get('page')}"
        )
        previous = by_id.get(key)
        if previous is None or float(item.get("score", 0)) >= float(previous.get("score", 0)):
            by_id[key] = item
    return list(by_id.values())


def merge_dict(left: dict | None, right: dict | None) -> dict:
    return {**(left or {}), **(right or {})}


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

    # retrieval (parallel)
    evidence: Annotated[list[dict], merge_evidence]
    numeric_data: Annotated[dict, merge_dict]
    retrieval_meta: Annotated[dict, merge_dict]
    retrieval_attempts: int
    evidence_grades: list[dict]
    coverage: float
    recency: float
    conflicts: list[dict]
    evidence_sufficient: bool

    # generation
    draft: dict
    generation_meta: dict
    critique: str
    repair_attempts: int

    # review
    review_decision: dict

    # validation / output
    validation: dict
    final: dict
    status: str
    errors: Annotated[list[str], operator.add]


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "").lower()


class KnowledgeGraphRunner:
    def __init__(self, agent: KnowledgeAgent):
        self.agent = agent
        self.checkpointer = _build_checkpointer()
        self.graph = self._build()

    # ── nodes ──

    def parse_intent(self, state: KnowledgeGraphState) -> dict:
        query = state["query"].strip()
        country = (state.get("country") or "").strip() or None
        platform = (state.get("platform") or "").strip() or None
        vague = any(marker in query.lower() for marker in VAGUE_MARKERS)
        needs_clarification = vague and not country and not platform
        follow_ups = []
        if needs_clarification:
            follow_ups = [
                "目标国家/市场是什么？",
                "目标平台是什么（Shopee/Lazada/TikTok Shop 等）？",
                "具体产品、材质或用途是什么？",
            ]
        return {
            "intent": {
                "query": query,
                "country": country,
                "platform": platform,
                "query_type": "compliance" if not vague else "needs_context",
            },
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

    def plan(self, state: KnowledgeGraphState) -> dict:
        query = state["query"]
        if state.get("clarification"):
            query = f"{query} {state['clarification']}"
        return {
            "query": query,
            "retrieval_attempts": 0,
            "repair_attempts": 0,
            "evidence": [],
            "numeric_data": {},
            "retrieval_meta": {},
            "errors": [],
        }

    def retrieve_policy(self, state: KnowledgeGraphState) -> dict:
        try:
            evidence, meta = self.agent.retrieve(
                state["query"],
                country=state.get("country"),
                platform=state.get("platform"),
                top_k=state.get("top_k", 5),
                mode=state.get("mode", "auto"),
                rerank=state.get("rerank"),
                rerank_pool=state.get("rerank_pool", 50),
            )
        except Exception as exc:
            return {
                "evidence": [],
                "retrieval_meta": {"policy": {"error": str(exc)}},
                "errors": [str(exc)],
            }
        return {"evidence": evidence, "retrieval_meta": {"policy": meta}}

    def retrieve_market(self, state: KnowledgeGraphState) -> dict:
        try:
            country = state.get("country") or "id"
            market = get_market_summary(country)
            categories = get_hot_search_categories(country, 5)
            competitors = get_competitor_products(limit=5)
            return {
                "numeric_data": {
                    "market": market,
                    "hot_categories": categories,
                    "competitors": competitors,
                },
                "retrieval_meta": {"market": {"count": len(categories), "source": "data_tools"}},
            }
        except Exception as exc:
            return {
                "retrieval_meta": {"market": {"error": str(exc)}},
                "errors": [str(exc)],
            }

    def retrieve_numeric(self, state: KnowledgeGraphState) -> dict:
        try:
            country = state.get("country") or "id"
            platform = state.get("platform") or "shopee"
            fees = get_platform_fees(platform, 100)
            logistics = get_logistics_cost(country, 0.3)
            fx = get_currency_rate(country)
            return {
                "numeric_data": {"fees": fees, "logistics": logistics, "fx": fx},
                "retrieval_meta": {"numeric": {"currency": fx["code"], "source": "data_tools"}},
            }
        except Exception as exc:
            return {
                "retrieval_meta": {"numeric": {"error": str(exc)}},
                "errors": [str(exc)],
            }

    def merge_retrieval(self, state: KnowledgeGraphState) -> dict:
        evidence = sorted(
            state.get("evidence", []),
            key=lambda item: float(item.get("score", 0)),
            reverse=True,
        )
        return {"evidence": evidence}

    def grade_evidence(self, state: KnowledgeGraphState) -> dict:
        evidence = state.get("evidence", [])
        if not evidence:
            return {
                "evidence_grades": [],
                "coverage": 0.0,
                "recency": 0.0,
                "conflicts": [],
                "evidence_sufficient": False,
            }

        max_score = max(float(item.get("score", 0)) for item in evidence) or 1.0
        grades = []
        recency_scores = []
        haystack_parts = []
        for rank, item in enumerate(evidence, 1):
            relevance = min(1.0, float(item.get("score", 0)) / max_score)
            effective_from = str(item.get("effective_from", "unknown"))
            recency = 1.0 if effective_from and effective_from != "unknown" else 0.5
            recency_scores.append(recency)
            haystack_parts.append(
                " ".join((
                    str(item.get("content", "")),
                    str(item.get("section_path", "")),
                    str(item.get("clause_id", "")),
                ))
            )
            grades.append({
                "chunk_id": item.get("chunk_id"),
                "doc_id": item.get("citation_doc_id") or item.get("doc_id"),
                "rank": rank,
                "relevance": round(relevance, 3),
                "recency": recency,
            })

        # Coverage here is retrieval coverage: 2 of 3 desired chunks is enough.
        coverage = min(1.0, len(evidence) / 3.0)
        recency = sum(recency_scores) / len(recency_scores)

        # Detect possible version conflicts: same title with different known dates/doc ids.
        versions: dict[str, dict[str, set]] = {}
        for item in evidence:
            title = item.get("title") or item.get("citation_doc_id") or "unknown"
            bucket = versions.setdefault(title, {"dates": set(), "docs": set()})
            effective_from = str(item.get("effective_from", "unknown"))
            if effective_from and effective_from != "unknown":
                bucket["dates"].add(effective_from)
            bucket["docs"].add(item.get("citation_doc_id") or item.get("doc_id"))

        conflicts = []
        for title, bucket in versions.items():
            if len(bucket["dates"]) > 1 or len(bucket["docs"]) > 1:
                conflicts.append({
                    "title": title,
                    "effective_dates": sorted(bucket["dates"]),
                    "doc_ids": sorted(str(doc) for doc in bucket["docs"]),
                })

        return {
            "evidence_grades": grades,
            "coverage": round(coverage, 3),
            "recency": round(recency, 3),
            "conflicts": conflicts,
            "needs_human_review": state.get("needs_human_review", False) or bool(conflicts),
            "evidence_sufficient": coverage >= 0.6,
        }

    def reformulate(self, state: KnowledgeGraphState) -> dict:
        return {
            "platform": None,
            "top_k": max(int(state.get("top_k", 5)), 8),
            "retrieval_attempts": int(state.get("retrieval_attempts", 0)) + 1,
        }

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
            "retrieval_meta": state.get("retrieval_meta", {}),
            "numeric_data": state.get("numeric_data", {}),
            "coverage": state.get("coverage", 0),
            "recency": state.get("recency", 0),
            "conflicts": state.get("conflicts", []),
            "critique": state.get("critique", ""),
        }
        draft, meta = self.agent.answer_from_evidence(
            state["query"], evidence, context=context,
        )
        return {"draft": draft, "generation_meta": meta}

    def validate(self, state: KnowledgeGraphState) -> dict:
        draft = copy.deepcopy(state.get("draft") or {})
        evidence = state.get("evidence", [])
        issues: list[str] = []
        blocking: list[str] = []

        for field in REQUIRED_FIELDS:
            if field not in draft:
                blocking.append(f"缺少必填字段: {field}")
        if draft.get("verdict") not in VERDICT_ENUM:
            blocking.append(f"verdict 非法: {draft.get('verdict')!r}")

        retrieved_by_doc: dict[str, list[str]] = {}
        for item in evidence:
            doc_id = item.get("citation_doc_id") or item.get("doc_id")
            retrieved_by_doc.setdefault(doc_id, []).append(item.get("content", ""))

        cited = draft.get("evidence") or []
        if evidence and not cited:
            issues.append("检索到证据但答案未引用任何证据")
        for i, item in enumerate(cited, 1):
            doc_id = item.get("doc_id")
            if doc_id not in retrieved_by_doc:
                blocking.append(f"evidence[{i}] 引用了未检索到的 doc_id: {doc_id}")
                continue
            quote = item.get("quote") or ""
            if quote:
                quote_norm = _norm(quote)
                if not any(quote_norm in _norm(content) for content in retrieved_by_doc[doc_id]):
                    item["quote"] = ""
                    issues.append(f"evidence[{i}] 的 quote 无法在原文中找到，已移除")

        if not evidence and draft.get("verdict") != "信息不足":
            blocking.append("无检索证据时 verdict 必须为「信息不足」")

        return {
            "draft": draft,
            "validation": {"passed": not blocking, "blocking": blocking, "warnings": issues},
        }

    def repair(self, state: KnowledgeGraphState) -> dict:
        validation = state.get("validation", {})
        critique = "；".join(validation.get("blocking", []) + validation.get("warnings", []))
        return {
            "critique": critique,
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
    def route_after_grade(state: KnowledgeGraphState) -> str:
        if not state.get("evidence_sufficient") and int(state.get("retrieval_attempts", 0)) < 2:
            return "reformulate"
        return "synthesize"

    @staticmethod
    def route_after_validate(state: KnowledgeGraphState) -> str:
        blocking = (state.get("validation") or {}).get("blocking", [])
        if blocking and int(state.get("repair_attempts", 0)) < 1:
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
        graph.add_node("retrieve_policy", self.retrieve_policy)
        graph.add_node("retrieve_market", self.retrieve_market)
        graph.add_node("retrieve_numeric", self.retrieve_numeric)
        graph.add_node("merge_evidence", self.merge_retrieval)
        graph.add_node("grade_evidence", self.grade_evidence)
        graph.add_node("reformulate", self.reformulate)
        graph.add_node("synthesize", self.synthesize)
        graph.add_node("validate", self.validate)
        graph.add_node("repair", self.repair)
        graph.add_node("human_review", self.human_review)
        graph.add_node("format", self.format_output)

        graph.add_edge(START, "parse_intent")
        graph.add_conditional_edges(
            "parse_intent", self.route_after_intent,
            {"clarify": "clarify", "plan": "plan"},
        )
        graph.add_edge("clarify", "plan")
        graph.add_edge("plan", "retrieve_policy")
        graph.add_edge("plan", "retrieve_market")
        graph.add_edge("plan", "retrieve_numeric")
        graph.add_edge(
            ["retrieve_policy", "retrieve_market", "retrieve_numeric"],
            "merge_evidence",
        )
        graph.add_edge("merge_evidence", "grade_evidence")
        graph.add_conditional_edges(
            "grade_evidence", self.route_after_grade,
            {"reformulate": "reformulate", "synthesize": "synthesize"},
        )
        graph.add_edge("reformulate", "retrieve_policy")
        graph.add_edge("reformulate", "retrieve_market")
        graph.add_edge("reformulate", "retrieve_numeric")
        graph.add_edge("synthesize", "validate")
        graph.add_conditional_edges(
            "validate", self.route_after_validate,
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
            "graph_version": "v1",
            "thread_id": thread_id,
            "status": status or result.get("status", "done"),
            "retrieval_attempts": result.get("retrieval_attempts", 0),
            "repair_attempts": result.get("repair_attempts", 0),
            "coverage": result.get("coverage", 0),
            "recency": result.get("recency", 0),
            "conflicts": result.get("conflicts", []),
            "evidence_grades": result.get("evidence_grades", []),
            "numeric_data": result.get("numeric_data", {}),
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
                "query": query,
                "country": country,
                "platform": platform,
                "top_k": top_k,
                "mode": mode,
                "rerank": rerank,
                "rerank_pool": rerank_pool,
                "session_id": thread_id,
                "require_review": require_review,
                "errors": [],
            }
            result = self.graph.invoke(state, config=config)

        interrupts = result.get("__interrupt__") or []
        if interrupts:
            first = interrupts[0]
            payload = getattr(first, "value", first)
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
                status = "needs_clarification"
            else:
                final = payload.get("draft", {}) if isinstance(payload, dict) else {}
                status = "needs_review"
            return final, self._result_meta(result, thread_id, status, payload)

        final = result.get("final") or {
            "verdict": "信息不足",
            "summary": "工作流未产生结果。",
            "evidence": [],
            "compliance_checklist": [],
            "unknowns": ["graph returned no final output"],
            "follow_up_questions": [],
        }
        return final, self._result_meta(result, thread_id)


def create_knowledge_graph(agent: KnowledgeAgent | None = None) -> KnowledgeGraphRunner:
    return KnowledgeGraphRunner(agent or KnowledgeAgent())
