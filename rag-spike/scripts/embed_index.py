"""构建向量索引：读取 index.json → 用 fastembed 编码 → 保存 embeddings.npz。

必须使用 rag-spike/.venv-embed 的 Python 运行：
  .venv-embed/Scripts/python scripts/embed_index.py
"""
import argparse
import json
import time
from datetime import datetime, timezone

import numpy as np

from retrieval import INDEX_PATH, ROOT
from vector_retrieval import CACHE_DIR, DEFAULT_MODEL, EMBEDDINGS_PATH, text_hash


def load_existing(model_name: str) -> dict[str, tuple[str, np.ndarray]]:
    if not EMBEDDINGS_PATH.exists():
        return {}
    try:
        with np.load(EMBEDDINGS_PATH, allow_pickle=False) as data:
            if str(data["model_name"]) != model_name:
                return {}
            chunk_ids = data["chunk_ids"].tolist()
            hashes = data["text_hashes"].tolist()
            vectors = data["vectors"]
            return {
                chunk_id: (hash_value, vectors[i].copy())
                for i, (chunk_id, hash_value) in enumerate(zip(chunk_ids, hashes))
            }
    except Exception:
        return {}


def main() -> None:
    parser = argparse.ArgumentParser(description="构建向量索引")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--force", action="store_true", help="忽略缓存，全部重算")
    args = parser.parse_args()

    try:
        from fastembed import TextEmbedding
    except ImportError as exc:
        raise SystemExit(
            "缺少 fastembed。请使用 rag-spike/.venv-embed 的 Python 运行。"
        ) from exc

    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    chunks = index["chunks"]
    old = {} if args.force else load_existing(args.model)

    pending: list[tuple[int, str]] = []
    old_hashes: dict[int, str] = {}
    for i, chunk in enumerate(chunks):
        hash_value = text_hash(chunk["text"])
        old_hashes[i] = hash_value
        cached = old.get(chunk["chunk_id"])
        if cached is None or cached[0] != hash_value:
            pending.append((i, chunk["text"]))

    print(f"文档块: {len(chunks)}，需编码: {len(pending)}，复用缓存: {len(chunks) - len(pending)}")
    print(f"模型: {args.model}")

    model = TextEmbedding(model_name=args.model, cache_dir=str(CACHE_DIR))
    vectors = np.zeros((len(chunks), 0), dtype=np.float32)
    if pending:
        start = time.time()
        embedded = np.array(
            list(model.embed([text for _, text in pending], batch_size=args.batch_size)),
            dtype=np.float32,
        )
        print(f"编码完成: {len(pending)} 块，用时 {time.time() - start:.1f}s，维度 {embedded.shape[1]}")
        vectors = np.zeros((len(chunks), embedded.shape[1]), dtype=np.float32)
        for row, (i, _) in enumerate(pending):
            vectors[i] = embedded[row]
    else:
        sample = next(iter(old.values()))[1]
        vectors = np.zeros((len(chunks), len(sample)), dtype=np.float32)

    # 复用缓存向量
    pending_positions = {pos for pos, _ in pending}
    for i, chunk in enumerate(chunks):
        if i in pending_positions:
            continue
        cached = old.get(chunk["chunk_id"])
        if cached is not None and cached[0] == old_hashes[i]:
            vectors[i] = cached[1]

    # 归一化，向量检索时直接用点积算余弦相似度
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    vectors = vectors / norms

    built_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        EMBEDDINGS_PATH,
        chunk_ids=np.array([chunk["chunk_id"] for chunk in chunks]),
        vectors=vectors,
        text_hashes=np.array([old_hashes[i] for i in range(len(chunks))]),
        model_name=np.array(args.model),
        built_at=np.array(built_at),
        index_snapshot=np.array(str(index.get("snapshot_id", ""))),
    )
    print(f"向量索引已写入: {EMBEDDINGS_PATH}")
    print(f"矩阵形状: {vectors.shape}，构建时间: {built_at}")


if __name__ == "__main__":
    main()
