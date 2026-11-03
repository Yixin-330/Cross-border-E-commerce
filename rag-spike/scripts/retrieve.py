"""命令行检索。

用法:
  python scripts/retrieve.py "印尼儿童玩具需要什么认证" --country id --top 5
  python scripts/retrieve.py "佣金" --platform shopee --json
"""
import argparse
import json

from retrieval import bm25_search, load_index


def main() -> None:
    parser = argparse.ArgumentParser(description="检索")
    parser.add_argument("query", help="检索问题")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--country", default=None)
    parser.add_argument("--platform", default=None)
    parser.add_argument("--doc-type", default=None)
    parser.add_argument("--mode", choices=["bm25", "vector", "hybrid", "auto"], default="bm25",
                        help="检索模式；auto 按查询语言路由（中文→hybrid，其他→bm25）")
    parser.add_argument("--pool", type=int, default=20, help="混合检索每个通道的候选数")
    parser.add_argument("--rerank", action="store_true", help="对第一阶段候选做 cross-encoder 重排")
    parser.add_argument("--rerank-pool", type=int, default=50, help="第一阶段召回、用于重排的候选数")
    parser.add_argument("--rerank-model", default="BAAI/bge-reranker-v2-m3-int8")
    parser.add_argument("--expand", action="store_true",
                        help="中文查询追加印尼语领域同义词后再召回（rerank 仍用原查询）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    search_query = args.query
    expanded_terms: list[str] = []
    from query_expansion import expand_query, should_expand
    if should_expand(args.query, args.mode, args.expand):
        search_query, expanded_terms = expand_query(args.query)

    index = load_index()
    retrieval_top = args.rerank_pool if args.rerank else args.top
    if args.mode == "vector":
        from vector_retrieval import vector_search
        results = vector_search(
            index, search_query, top_k=retrieval_top,
            country=args.country, platform=args.platform, doc_type=args.doc_type,
            aggregate_docs=False,
        )
    elif args.mode == "hybrid":
        from vector_retrieval import hybrid_search
        results = hybrid_search(
            index, search_query, top_k=retrieval_top,
            country=args.country, platform=args.platform, doc_type=args.doc_type,
            pool=args.pool, aggregate_docs=False,
        )
    elif args.mode == "auto":
        from vector_retrieval import auto_search
        results = auto_search(
            index, search_query, top_k=retrieval_top,
            country=args.country, platform=args.platform, doc_type=args.doc_type,
            pool=args.pool, aggregate_docs=False,
        )
    else:
        results = bm25_search(
            index, search_query, top_k=retrieval_top,
            country=args.country, platform=args.platform, doc_type=args.doc_type,
            aggregate_docs=False,
        )

    if args.rerank:
        from vector_retrieval import rerank_results
        results = rerank_results(
            search_query, results, top_k=args.top, model_name=args.rerank_model,
        )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    print(f"模式: {args.mode}{' + rerank' if args.rerank else ''}")
    if expanded_terms:
        print(f"扩展词: {' '.join(expanded_terms)}")
    if not results:
        print("未检索到结果。")
        return

    for i, item in enumerate(results, 1):
        print(f"{i}. [{item['score']}] {item['citation_doc_id']} — {item['title']}")
        print(f"   章节/条款: {item['section_path']} / {item['clause_id']} | "
              f"生效: {item['effective_from']} | 采集: {item['collected_at']}")
        if item["cross_refs"]:
            print(f"   交叉引用: {', '.join(item['cross_refs'])}")
        print(f"   {item['content'][:160]}...")
    print(f"\n共 {len(results)} 条结果。")


if __name__ == "__main__":
    main()
