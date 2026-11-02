"""向量检索与 RRF 混合检索。

依赖 fastembed（只装在 rag-spike/.venv-embed 中），因此这里延迟导入：
BM25 模式不需要 fastembed，向量/混合模式请用 venv 的 Python 运行。
"""
import hashlib
import re
from pathlib import Path

import numpy as np

from retrieval import (
    ROOT,
    _matches,
    bm25_search,
    build_result,
)

EMBEDDINGS_PATH = ROOT / "index" / "embeddings.npz"
CACHE_DIR = ROOT / ".cache" / "fastembed"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_RERANK_MODEL = "BAAI/bge-reranker-v2-m3-int8"
VECTOR_FRONT_MATTER_WEIGHT = 0.7

_model = None
_model_name = None
_embeddings_cache = None
_embeddings_key = None
_reranker = None
_reranker_name = None


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_model(model_name: str = DEFAULT_MODEL):
    global _model, _model_name
    if _model is None or _model_name != model_name:
        try:
            from fastembed import TextEmbedding
        except ImportError as exc:
            raise SystemExit(
                "缺少 fastembed。请使用 rag-spike/.venv-embed 的 Python 运行，"
                "或先执行: .venv-embed/Scripts/pip install -r requirements-embed.txt"
            ) from exc
        _model = TextEmbedding(model_name=model_name, cache_dir=str(CACHE_DIR))
        _model_name = model_name
    return _model


def get_reranker(model_name: str = DEFAULT_RERANK_MODEL):
    global _reranker, _reranker_name
    if _reranker is None or _reranker_name != model_name:
        try:
            from fastembed.rerank.cross_encoder import TextCrossEncoder
        except ImportError as exc:
            raise SystemExit(
                "缺少 fastembed。请使用 rag-spike/.venv-embed 的 Python 运行。"
            ) from exc
        _reranker = TextCrossEncoder(model_name=model_name, cache_dir=str(CACHE_DIR))
        _reranker_name = model_name
    return _reranker


def rerank_results(query: str, results: list[dict], top_k: int = 5,
                   model_name: str = DEFAULT_RERANK_MODEL) -> list[dict]:
    """用 cross-encoder 对候选 chunk 逐对打分并重排。"""
    if not results:
        return []
    encoder = get_reranker(model_name)
    scores = list(encoder.rerank(query, [result["content"] for result in results]))
    ranked = sorted(zip(scores, results), key=lambda item: item[0], reverse=True)
    output = []
    for score, result in ranked[:top_k]:
        item = dict(result)
        item["first_stage_score"] = item.get("score")
        item["rerank_score"] = round(float(score), 6)
        item["score"] = round(float(score), 6)
        output.append(item)
    return output


def aggregate_by_doc(results: list[dict], top_k: int) -> list[dict]:
    """按引用文档聚合，保留每篇文档排名最靠前的 chunk。"""
    best: dict[str, dict] = {}
    for result in results:
        best.setdefault(result["citation_doc_id"], result)
    return list(best.values())[:top_k]


def _normalize(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def load_embeddings() -> dict:
    global _embeddings_cache, _embeddings_key
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            f"向量索引不存在: {EMBEDDINGS_PATH}\n"
            "请先运行: .venv-embed/Scripts/python scripts/embed_index.py"
        )
    key = (str(EMBEDDINGS_PATH), EMBEDDINGS_PATH.stat().st_mtime)
    if _embeddings_key != key:
        with np.load(EMBEDDINGS_PATH, allow_pickle=False) as data:
            _embeddings_cache = {
                "chunk_ids": data["chunk_ids"].tolist(),
                "vectors": _normalize(data["vectors"]),
                "text_hashes": data["text_hashes"].tolist(),
                "model_name": str(data["model_name"]),
                "built_at": str(data["built_at"]),
                "index_snapshot": str(data["index_snapshot"]) if "index_snapshot" in data.files else "",
            }
        _embeddings_key = key
    return _embeddings_cache


def vector_search(index: dict, query: str, top_k: int = 5,
                  country: str | None = None, platform: str | None = None,
                  doc_type: str | None = None,
                  aggregate_docs: bool = False) -> list[dict]:
    embeddings = load_embeddings()
    chunk_map = {chunk["chunk_id"]: chunk for chunk in index["chunks"]}
    ids = embeddings["chunk_ids"]
    vectors = embeddings["vectors"]

    positions = [
        i for i, chunk_id in enumerate(ids)
        if chunk_id in chunk_map
        and _matches(chunk_map[chunk_id], country, platform, doc_type)
    ]
    if not positions:
        return []

    model = get_model(embeddings["model_name"])
    query_vector = np.array(next(model.embed([query])), dtype=np.float32)
    norm = np.linalg.norm(query_vector)
    if norm == 0:
        return []
    query_vector /= norm

    scores = vectors[positions] @ query_vector
    order = np.argsort(-scores)
    results = []
    limit = len(order) if aggregate_docs else min(top_k, len(order))
    for idx in order[:limit]:
        score = float(scores[idx])
        chunk = chunk_map[ids[positions[idx]]]
        if chunk.get("front_matter"):
            score *= VECTOR_FRONT_MATTER_WEIGHT
        results.append(build_result(score, chunk))

    if aggregate_docs:
        best: dict[str, dict] = {}
        for result in results:
            best.setdefault(result["citation_doc_id"], result)
        results = list(best.values())
    return results[:top_k]


def hybrid_search(index: dict, query: str, top_k: int = 5,
                  country: str | None = None, platform: str | None = None,
                  doc_type: str | None = None,
                  aggregate_docs: bool = False,
                  pool: int = 20, rrf_k: int = 60) -> list[dict]:
    """BM25 + 向量检索，使用 reciprocal rank fusion 融合。"""
    bm25_results = bm25_search(
        index, query, top_k=pool, country=country, platform=platform,
        doc_type=doc_type, aggregate_docs=False,
    )
    vector_results = vector_search(
        index, query, top_k=pool, country=country, platform=platform,
        doc_type=doc_type, aggregate_docs=False,
    )

    fused: dict[str, float] = {}
    meta: dict[str, dict] = {}
    for results in (bm25_results, vector_results):
        for rank, result in enumerate(results):
            chunk_id = result["chunk_id"]
            fused[chunk_id] = fused.get(chunk_id, 0.0) + 1.0 / (rrf_k + rank + 1)
            meta.setdefault(chunk_id, result)

    ranked = sorted(fused.items(), key=lambda item: item[1], reverse=True)
    results = []
    for chunk_id, score in ranked:
        result = dict(meta[chunk_id])
        result["score"] = round(score, 6)
        results.append(result)

    if aggregate_docs:
        best: dict[str, dict] = {}
        for result in results:
            best.setdefault(result["citation_doc_id"], result)
        results = list(best.values())
    return results[:top_k]


_CJK_QUERY = re.compile(r"[一-鿿]")


def auto_search(index: dict, query: str, **kwargs) -> list[dict]:
    """按查询语言路由：中文查询走混合检索，否则走 BM25。

    语料是印尼语，BM25 无法跨语言；中文 UI 用户的问题需要多语言向量检索。
    """
    if _CJK_QUERY.search(query):
        return hybrid_search(index, query, **kwargs)
    return bm25_search(
        index, query,
        top_k=kwargs.get("top_k", 5),
        country=kwargs.get("country"),
        platform=kwargs.get("platform"),
        doc_type=kwargs.get("doc_type"),
        aggregate_docs=kwargs.get("aggregate_docs", False),
    )
