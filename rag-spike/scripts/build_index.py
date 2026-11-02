"""构建检索索引：只索引 review_status=approved 的文档 → 条款切分 → 保存快照。

审核门：机器提取的文档默认 review_status=pending，必须先用 review.py 审核通过。
"""
import argparse
import json
from datetime import datetime, timezone

from retrieval import (
    CORPUS_DIR,
    INDEX_PATH,
    chunk_document,
    doc_citation_id,
    doc_collected_at,
    doc_country,
    doc_effective_from,
    doc_effective_to,
    doc_platform,
    doc_published_at,
    load_manifest,
    tokenize,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="构建检索索引")
    parser.add_argument("--size", type=int, default=400, help="每块最大字符数")
    parser.add_argument("--overlap", type=int, default=80, help="相邻块重叠字符数")
    args = parser.parse_args()

    documents = load_manifest()
    approved = [d for d in documents if (d.get("review_status") or "pending") == "approved"]
    eligible = [d for d in approved if d.get("index_eligible", True) is not False]
    blocked = [d for d in approved if d.get("index_eligible", True) is False]
    pending = [d for d in documents if (d.get("review_status") or "pending") == "pending"]
    rejected = [d for d in documents if d.get("review_status") == "rejected"]

    if not eligible:
        raise SystemExit(
            "没有可索引的文档（需要 review_status=approved 且 index_eligible=true）。\n"
            "先运行: python scripts/review.py list，审核通过后再构建索引。"
        )

    chunks: list[dict] = []
    missing: list[str] = []
    per_doc: list[tuple[str, int, int]] = []

    for doc in eligible:
        path = CORPUS_DIR / doc["file"]
        if not path.exists():
            missing.append(doc["file"])
            continue
        text = path.read_text(encoding="utf-8")
        pieces = chunk_document(text, size=args.size, overlap=args.overlap)
        per_doc.append((doc["doc_id"], len(text), len(pieces)))
        for piece in pieces:
            piece.update({
                "chunk_id": f"{doc['doc_id']}{piece['chunk_id']}",
                "doc_id": doc["doc_id"],
                "citation_doc_id": doc_citation_id(doc),
                "title": doc.get("title", ""),
                "tokens": tokenize(piece["text"]),
                "country": doc_country(doc) or "any",
                "platform": doc_platform(doc) or "any",
                "doc_type": doc.get("doc_type", ""),
                "language": doc.get("language", ""),
                "original_doc_id": doc.get("original_doc_id", ""),
                "category": doc.get("category", ""),
                "published_at": doc_published_at(doc),
                "effective_from": doc_effective_from(doc),
                "effective_to": doc_effective_to(doc),
                "collected_at": doc_collected_at(doc),
                "source_url": doc.get("source_url", ""),
            })
            chunks.append(piece)

    built_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    index = {
        "snapshot_id": built_at,
        "built_at": built_at,
        "chunk_size": args.size,
        "chunk_overlap": args.overlap,
        "documents": eligible,
        "chunks": chunks,
    }
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"快照: {built_at}")
    print(f"已索引文档: {len(eligible)} 份，切分: {len(chunks)} 块"
          f"（size={args.size}, overlap={args.overlap}）")
    for doc_id, char_count, chunk_count in per_doc:
        print(f"  - {doc_id}: {char_count} 字符 → {chunk_count} 块")
    if blocked:
        print(f"已审核但禁止索引: {len(blocked)} 份（index_eligible=false，需补 OCR/核验后开启）")
    if pending:
        print(f"待审核文档: {len(pending)} 份（未进入索引，运行 review.py 处理）")
    if rejected:
        print(f"已拒绝文档: {len(rejected)} 份")
    if missing:
        print("以下文件在 manifest 中登记但不存在:")
        for name in missing:
            print(f"  - {name}")
    print(f"索引已写入: {INDEX_PATH}")


if __name__ == "__main__":
    main()
