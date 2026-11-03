"""检索层评测：计算 answerable 题的 hit@k 和 MRR。

只运行 status 为 sample/ready 的题目；draft 会被跳过。
clarification / uncovered 题不参与检索指标，但会单独统计数量，
其回答行为需要人工检查或后续接入 LLM 自动评测。
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from retrieval import ROOT, bm25_search, load_index

QUESTIONS_PATH = ROOT / "eval" / "questions.jsonl"


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "").lower()


def evidence_match(result: dict, evidence: dict) -> bool:
    """判断一条检索结果是否命中 gold_evidence。

    支持三种定位方式：条款 ID、PDF 页码、内容关键词；文档 ID 必须匹配。
    """
    doc_id = evidence.get("doc_id", "")
    if doc_id and doc_id not in {result["doc_id"], result.get("citation_doc_id", "")}:
        return False

    checks: list[bool] = []
    clause = evidence.get("clause_id")
    if clause:
        expected, actual = _norm(clause), _norm(result.get("clause_id", ""))
        if expected.isdigit():
            # 纯数字条款（如 "2"、"17"）必须精确匹配，避免匹配到 Pasal 20 等
            checks.append(expected == actual)
        else:
            checks.append(bool(expected and actual) and (expected in actual or actual in expected))

    page = evidence.get("page")
    if page:
        checks.append(int(page) == int(result.get("page", 0) or 0))

    keys = evidence.get("must_contain_any") or []
    if keys:
        haystack = _norm(result.get("content", "") + " " + result.get("section_path", ""))
        checks.append(any(_norm(key) in haystack for key in keys))

    if not checks:
        return bool(doc_id)
    return any(checks)


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict]:
    questions = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                questions.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name} 第 {line_no} 行不是合法 JSON: {exc}") from exc
    return questions


def main() -> None:
    parser = argparse.ArgumentParser(description="检索评测")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--questions", default=str(QUESTIONS_PATH),
                        help="评测集路径，默认 eval/questions.jsonl")
    parser.add_argument("--include-draft", action="store_true",
                        help="连同 status=draft 的题目一起评测（初稿校对用）")
    parser.add_argument("--mode", choices=["bm25", "vector", "hybrid", "auto"], default="bm25")
    parser.add_argument("--pool", type=int, default=20, help="混合检索每个通道的候选数")
    parser.add_argument("--evidence-top", type=int, default=10,
                        help="条款级证据检索的 chunk 候选数")
    parser.add_argument("--rerank", action="store_true",
                        help="对第一阶段候选做 cross-encoder 重排")
    parser.add_argument("--rerank-pool", type=int, default=50,
                        help="第一阶段召回、用于重排的候选数")
    parser.add_argument("--rerank-model", default="BAAI/bge-reranker-v2-m3-int8")
    parser.add_argument("--expand", action="store_true",
                        help="中文查询追加印尼语同义词后再召回（rerank 仍用原查询）")
    args = parser.parse_args()

    allowed = {"sample", "ready"}
    if args.include_draft:
        allowed.add("draft")
    questions = [
        q for q in load_questions(Path(args.questions))
        if q.get("status") in allowed
    ]
    answerable = [q for q in questions if q.get("gold_doc_ids")]
    behavior_only = [q for q in questions if not q.get("gold_doc_ids")]

    if not questions:
        print("没有可评测的题目（status 需为 sample 或 ready）。")
        return

    index = load_index()
    doc_count = len({
        c.get("citation_doc_id") or c["doc_id"] for c in index["chunks"]
    })
    if args.top >= doc_count:
        print(f"警告: top-{args.top} 覆盖了全部 {doc_count} 篇文档，"
              "hit@k 结构性为 100%，请用更小的 --top 或扩充语料。\n")
    hits = 0
    reciprocal_ranks = 0.0
    evidence_ranks: list[int | None] = []
    evidence_recalls: list[float] = []
    failures = []

    print(f"检索模式: {args.mode}{' + rerank' if args.rerank else ''}")
    print(f"评测集: {args.questions}")
    print(f"索引快照: {index.get('snapshot_id', '')}")
    print(f"评测日期: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"可评测题目: {len(questions)} 条（其中检索题 {len(answerable)} 条）\n")

    def search(question: str, country: str | None, platform: str | None,
               aggregate_docs: bool, top_k: int) -> list[dict]:
        if args.mode == "vector":
            from vector_retrieval import vector_search
            return vector_search(
                index, question, top_k=top_k, country=country,
                platform=platform, aggregate_docs=aggregate_docs,
            )
        if args.mode == "hybrid":
            from vector_retrieval import hybrid_search
            return hybrid_search(
                index, question, top_k=top_k, country=country,
                platform=platform, aggregate_docs=aggregate_docs, pool=args.pool,
            )
        if args.mode == "auto":
            from vector_retrieval import auto_search
            return auto_search(
                index, question, top_k=top_k, country=country,
                platform=platform, aggregate_docs=aggregate_docs, pool=args.pool,
            )
        return bm25_search(
            index, question, top_k=top_k, country=country,
            platform=platform, aggregate_docs=aggregate_docs,
        )

    for q in answerable:
        search_query = q["question"]
        expanded_terms: list[str] = []
        from query_expansion import expand_query, should_expand
        if should_expand(q["question"], args.mode, args.expand):
            search_query, expanded_terms = expand_query(q["question"])

        if args.rerank:
            from vector_retrieval import aggregate_by_doc, rerank_results
            stage1 = search(
                search_query,
                q.get("country") or None,
                q.get("platform") or None,
                aggregate_docs=False,
                top_k=args.rerank_pool,
            )
            reranked = rerank_results(
                search_query, stage1, top_k=args.rerank_pool,
                model_name=args.rerank_model,
            )
            results = aggregate_by_doc(reranked, args.top)
            evidence_results = reranked[:args.evidence_top] if q.get("gold_evidence") else []
        else:
            results = search(
                search_query,
                q.get("country") or None,
                q.get("platform") or None,
                aggregate_docs=True,
                top_k=args.top,
            )
            evidence_results = search(
                search_query,
                q.get("country") or None,
                q.get("platform") or None,
                aggregate_docs=False,
                top_k=args.evidence_top,
            ) if q.get("gold_evidence") else []
        gold = set(q["gold_doc_ids"])
        # 译文文档的引用应落回原文，因此同时接受 doc_id 和 citation_doc_id
        ranked_docs = [r.get("citation_doc_id") or r["doc_id"] for r in results]
        first_hit_rank = next(
            (i + 1 for i, result in enumerate(results)
             if {result["doc_id"], result.get("citation_doc_id", result["doc_id"])} & gold),
            None,
        )
        hit = first_hit_rank is not None
        hits += int(hit)
        if hit:
            reciprocal_ranks += 1.0 / first_hit_rank

        gold_evidence = q.get("gold_evidence") or []
        evidence_rank = None
        evidence_recall = None
        if gold_evidence:
            evidence_rank = next(
                (i + 1 for i, result in enumerate(evidence_results)
                 if any(evidence_match(result, item) for item in gold_evidence)),
                None,
            )
            matched = sum(
                1 for item in gold_evidence
                if any(evidence_match(result, item) for result in evidence_results)
            )
            evidence_recall = matched / len(gold_evidence)
            evidence_ranks.append(evidence_rank)
            evidence_recalls.append(evidence_recall)

        status = f"✅ 文档命中@{first_hit_rank}" if hit else "❌ 文档未命中"
        print(f"[{q['id']}] {q['question']}")
        if expanded_terms:
            print(f"  扩展词: {' '.join(expanded_terms)}")
        print(f"  期望文档: {sorted(gold)}")
        print(f"  检索文档: {ranked_docs or '（无结果）'}")
        print(f"  文档结果: {status}")
        if gold_evidence:
            evidence_status = f"证据命中@{evidence_rank}" if evidence_rank else "证据未命中"
            print(f"  条款结果: {evidence_status}，证据覆盖 {evidence_recall:.0%}")
            shown = [f"{r['citation_doc_id']}/{r['clause_id']}" for r in evidence_results[:3]]
            print(f"  证据检索: {shown}")
        if not hit:
            failures.append(q["id"])
        print()

    hit_rate = hits / len(answerable) if answerable else 0.0
    mrr = reciprocal_ranks / len(answerable) if answerable else 0.0

    print("=" * 50)
    print(f"hit@{args.top}: {hit_rate:.2%} ({hits}/{len(answerable)})")
    print(f"MRR:      {mrr:.3f}")
    if evidence_ranks:
        ev_hits = sum(1 for rank in evidence_ranks if rank)
        ev_mrr = sum((1.0 / rank if rank else 0.0) for rank in evidence_ranks) / len(evidence_ranks)
        ev_recall = sum(evidence_recalls) / len(evidence_recalls)
        print(f"evidence hit@{args.evidence_top}: {ev_hits / len(evidence_ranks):.2%} "
              f"({ev_hits}/{len(evidence_ranks)})")
        print(f"evidence MRR:      {ev_mrr:.3f}")
        print(f"evidence recall@{args.evidence_top}: {ev_recall:.2%}")
    print(f"行为类题: {len(behavior_only)} 条（需人工检查追问/拒答是否符合预期）")
    for q in behavior_only:
        print(f"  - {q['id']} [{q.get('question_type')}] {q.get('expected_behavior')}")
    if failures:
        print(f"未命中题目: {', '.join(failures)}")
    if len(questions) < 20:
        print("提示: 可评测题目少于 20 条，指标仅供参考，不满足验收门槛。")
    elif hit_rate < 0.8:
        print("提示: hit@k 低于 0.80，未达到进入集成阶段的门槛。")
    else:
        print("提示: hit@k 达到 0.80 门槛（仍需人工核对引用是否支撑结论）。")


if __name__ == "__main__":
    main()
