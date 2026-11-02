"""审核门：机器提取的文档先进入 pending，人工确认后改为 approved 才能入索引。

用法:
  python scripts/review.py list
  python scripts/review.py show <doc_id>
  python scripts/review.py approve <doc_id> --by 你的名字
  python scripts/review.py reject <doc_id> --by 你的名字 --reason "来源不可靠"
"""
import argparse
import getpass
import json
from datetime import datetime, timezone
from pathlib import Path

from retrieval import CORPUS_DIR, MANIFEST_PATH, load_manifest


def write_manifest(documents: list[dict]) -> None:
    # 先写临时文件再替换，避免中途失败破坏 manifest
    temp = MANIFEST_PATH.with_name(MANIFEST_PATH.name + ".tmp")
    with open(temp, "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    temp.replace(MANIFEST_PATH)


def find_document(documents: list[dict], doc_id: str) -> dict:
    for doc in documents:
        if doc.get("doc_id") == doc_id:
            return doc
    raise SystemExit(f"未找到文档: {doc_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="语料审核")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="列出文档及审核状态")

    show_parser = sub.add_parser("show", help="查看单份文档的元数据")
    show_parser.add_argument("doc_id")

    import_parser = sub.add_parser("import", help="导入 staging 批次的 manifest.pending.jsonl")
    import_parser.add_argument("path")

    set_parser = sub.add_parser("set", help="更新文档元数据（核对日期/标题后使用）")
    set_parser.add_argument("doc_id")
    set_parser.add_argument("--title")
    set_parser.add_argument("--published-at")
    set_parser.add_argument("--effective-from")
    set_parser.add_argument("--effective-to")
    set_parser.add_argument("--source-url")
    set_parser.add_argument("--notes")
    set_parser.add_argument("--index-eligible", choices=["true", "false"])

    for name in ("approve", "reject"):
        p = sub.add_parser(name, help=f"{name} 文档")
        p.add_argument("doc_id")
        p.add_argument("--by", default=getpass.getuser())
        p.add_argument("--reason", default="")
        p.add_argument("--no-index", action="store_true",
                       help="审核通过但不进入索引（如仅留档、待 OCR）")

    args = parser.parse_args()
    documents = load_manifest()

    if args.command == "import":
        source = Path(args.path)
        if not source.exists():
            raise SystemExit(f"找不到待导入文件: {source}")
        existing = {doc.get("doc_id") for doc in documents}
        added = 0
        missing_files = []
        with open(source, encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    doc = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{source} 第 {line_no} 行不是合法 JSON: {exc}") from exc
                if doc.get("doc_id") in existing:
                    continue
                doc["review_status"] = "pending"
                doc.setdefault("index_eligible", False)
                if not (CORPUS_DIR / doc.get("file", "")).exists():
                    missing_files.append(doc.get("doc_id", "?"))
                documents.append(doc)
                existing.add(doc.get("doc_id"))
                added += 1
        write_manifest(documents)
        print(f"已导入 {added} 份文档为 pending（不会进入索引）。")
        if missing_files:
            print("以下文档在 manifest 中登记但文件不存在:")
            for doc_id in missing_files:
                print(f"  - {doc_id}")
        return

    if args.command == "list":
        if not documents:
            print("manifest 为空。")
            return
        print(f"{'状态':<10} {'索引':<6} {'doc_id':<36} {'平台':<10} {'生效日期':<12} 标题")
        for doc in documents:
            status = doc.get("review_status") or "pending"
            eligible = "yes" if doc.get("index_eligible", True) else "no"
            warning = " [!]" if doc.get("extraction_warning") else ""
            print(f"{status:<10} {eligible:<6} {doc.get('doc_id', ''):<36} "
                  f"{doc.get('platform', ''):<10} {doc.get('effective_from', 'unknown'):<12} "
                  f"{doc.get('title', '')}{warning}")
        return

    if args.command == "show":
        print(json.dumps(find_document(documents, args.doc_id), ensure_ascii=False, indent=2))
        return

    if args.command == "set":
        doc = find_document(documents, args.doc_id)
        mapping = {
            "title": args.title,
            "published_at": args.published_at,
            "effective_from": args.effective_from,
            "effective_to": args.effective_to,
            "source_url": args.source_url,
            "notes": args.notes,
        }
        for key, value in mapping.items():
            if value is not None:
                doc[key] = value
        if args.index_eligible is not None:
            doc["index_eligible"] = args.index_eligible == "true"
        write_manifest(documents)
        print(f"{doc['doc_id']} 元数据已更新。")
        return

    doc = find_document(documents, args.doc_id)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    doc["review_status"] = "approved" if args.command == "approve" else "rejected"
    doc["reviewed_by"] = args.by
    doc["reviewed_at"] = now
    if args.command == "approve":
        doc["index_eligible"] = not args.no_index
        if str(doc.get("effective_from", "unknown")) == "unknown":
            print("警告: effective_from 仍为 unknown，该文档不能用于时点合规结论。")
        if doc.get("extraction_warning") and not args.no_index:
            print("警告: 存在 extraction_warning，建议先核验或使用 --no-index。")
    else:
        doc["index_eligible"] = False
    if args.command == "reject" and args.reason:
        doc["review_notes"] = args.reason

    write_manifest(documents)
    print(f"{doc['doc_id']} → {doc['review_status']}（审核人: {args.by}）")
    if args.command == "approve":
        if args.no_index:
            print("已标记为暂不索引（index_eligible=false），补齐 OCR/核验后再开启。")
        else:
            print("可运行 python scripts/build_index.py 重建索引。")


if __name__ == "__main__":
    main()
