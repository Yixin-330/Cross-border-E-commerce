"""根据问题 + 检索结果，生成带引用的回答提示词。

用法:
  python scripts/build_prompt.py "在印尼销售儿童玩具需要哪些认证？" --country id
  python scripts/build_prompt.py "..." --country id --out prompt.txt
"""
import argparse
from pathlib import Path

from retrieval import ROOT, bm25_search, format_evidence, load_index

TEMPLATE_PATH = ROOT / "prompts" / "answer_with_citations.md"
SCHEMA_PATH = ROOT / "schemas" / "selection_answer.schema.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="生成带引用的提示词")
    parser.add_argument("question")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--country", default=None)
    parser.add_argument("--platform", default=None)
    parser.add_argument("--out", default=None, help="输出文件；默认打印到 stdout")
    args = parser.parse_args()

    index = load_index()
    results = bm25_search(
        index, args.question, top_k=args.top,
        country=args.country, platform=args.platform,
    )

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    prompt = (
        template
        .replace("{{QUESTION}}", args.question)
        .replace("{{CONTEXT}}", format_evidence(results))
        .replace("{{SCHEMA}}", schema)
    )

    if args.out:
        Path(args.out).write_text(prompt, encoding="utf-8")
        print(f"提示词已写入: {args.out}（检索到 {len(results)} 条证据）")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
