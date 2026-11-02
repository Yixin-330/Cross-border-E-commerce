"""公共检索工具：CJK 友好分词、条款感知切分、BM25 打分。

零第三方依赖。当前作为基线，后续可替换为 embedding + rerank，
用 eval/ 里的评测集对比效果。

切分原则：
- 保留「章/节/条」层级，chunk 带 section_path 和 clause_id；
- 记录相邻条款与交叉引用（如「见第 5 条」）；
- 表格保留表头，超长表格按行拆分时重复表头；
- 翻译文档通过 original_doc_id 回链原文，引用落回原文。
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

# Windows 控制台默认可能是 GBK，统一按 UTF-8 输出，避免中文/符号乱码或崩溃
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus"
MANIFEST_PATH = CORPUS_DIR / "manifest.jsonl"
INDEX_PATH = ROOT / "index" / "index.json"

_CJK_RE = re.compile(r"[一-鿿]+")
_WORD_RE = re.compile(r"[A-Za-z0-9]+")
_SENTENCE_BREAKS = ("。", "；", "！", "？", "\n")

# 国家/平台为「不限」时，应能命中任何过滤条件
ANY_COUNTRY = {"", "sea", "any", "不限", "不限国家"}
ANY_PLATFORM = {"", "any", "general", "不限", "不限平台"}
MIN_CHUNK_CHARS = 12
FRONT_MATTER_WEIGHT = 0.35

_HEADING_CHAPTER = re.compile(r"^(第[一二三四五六七八九十百零〇0-9]+章)\s*(.*)$")
_HEADING_NUM_SECTION = re.compile(r"^(第[一二三四五六七八九十百零〇0-9]+节)\s*(.*)$")
_HEADING_ARTICLE = re.compile(r"^(第[一二三四五六七八九十百零〇0-9]+条)\s*(.*)$")
_HEADING_CN = re.compile(r"^([一二三四五六七八九十]+、)\s*(.*)$")
_HEADING_CN_PAREN = re.compile(r"^（([一二三四五六七八九十]+)）\s*(.*)$")
_ITEM_NUM = re.compile(r"^(\d+(?:\.\d+)*)[、.)]\s+(.+)$")
_ITEM_PAREN = re.compile(r"^（(\d+)）\s*(.+)$")

# 印尼法规结构：BAB（章）/ Bagian（节）/ Pasal（条）/ ayat（款）/ huruf（项）
_HEADING_BAB = re.compile(r"^(BAB\s+[IVXLCDM]+)\s*$", re.I)
_HEADING_BAGIAN = re.compile(
    r"^(Bagian\s+(?:Kesatu|Kedua|Ketiga|Keempat|Kelima|Keenam|Ketujuh|"
    r"Kedelapan|Kesembilan|Kesepuluh|[IVXLCDM]+|\d+))\b\s*(.*)$",
    re.I,
)
_HEADING_PARAGRAF = re.compile(
    r"^(Paragraf\s+(?:Kesatu|Kedua|Ketiga|Keempat|Kelima|Keenam|Ketujuh|"
    r"Kedelapan|Kesembilan|Kesepuluh|[IVXLCDM]+|\d+))\b\s*(.*)$",
    re.I,
)
_HEADING_PASAL = re.compile(r"^(Pasal\s+\d+)\s*$", re.I)
_ITEM_AYAT = re.compile(r"^\((\d+)\)\s+(.+)$")
_ITEM_HURUF = re.compile(r"^([a-z])\.\s+(.+)$", re.I)

_PAGE_MARKER = re.compile(r"^\[\[PAGE\s+(\d+)\]\]$", re.I)
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
_CROSS_REF_CN = re.compile(
    r"第[一二三四五六七八九十百零〇0-9]+条(?:第[一二三四五六七八九十百零〇0-9]+款)?"
)
_CROSS_REF_ID = re.compile(r"\bPasal\s+\d+(?:\s+ayat\s+\(\d+\))?", re.I)


def _extract_cross_refs(text: str) -> list[str]:
    return sorted(set(_CROSS_REF_CN.findall(text)) | set(_CROSS_REF_ID.findall(text)))


def tokenize(text: str) -> list[str]:
    """中文按单字 + 二元组切分，英文/数字按词切分。"""
    tokens: list[str] = []
    for match in _CJK_RE.finditer(text):
        run = match.group(0)
        tokens.extend(run)
        tokens.extend(run[i:i + 2] for i in range(len(run) - 1))
    tokens.extend(match.group(0).lower() for match in _WORD_RE.finditer(text))
    return tokens


# ── manifest 字段归一化 ──

def doc_platform(doc: dict) -> str:
    return (doc.get("platform") or "").strip().lower()


def doc_country(doc: dict) -> str:
    return (doc.get("country") or "").strip().lower()


def doc_published_at(doc: dict) -> str:
    # 兼容旧字段 publish_date
    return doc.get("published_at") or doc.get("publish_date") or "unknown"


def doc_effective_from(doc: dict) -> str:
    return doc.get("effective_from") or "unknown"


def doc_effective_to(doc: dict) -> str:
    return doc.get("effective_to") or "unknown"


def doc_collected_at(doc: dict) -> str:
    return doc.get("collected_at") or "unknown"


def doc_citation_id(doc: dict) -> str:
    """引用应落回原文文档 ID；翻译稿通过 original_doc_id 回链。"""
    return doc.get("original_doc_id") or doc["doc_id"]


# ── 文本切分 ──

def _split_long_text(text: str, size: int, overlap: int) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            window = text[start:end]
            cut = max(window.rfind(mark) for mark in _SENTENCE_BREAKS)
            if cut > size * 0.5:
                end = start + cut + 1
        piece = text[start:end].strip()
        if piece:
            pieces.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return pieces


def _split_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    return [cell.strip() for cell in line.split("|")]


_SENTENCE_ENDS = tuple("。；：！？.;:!?")


def _classify_line(stripped: str) -> tuple[str, str, str]:
    for regex, kind in (
        (_HEADING_CHAPTER, "chapter"),
        (_HEADING_NUM_SECTION, "num_section"),
        (_HEADING_ARTICLE, "article"),
        (_HEADING_BAB, "chapter"),
        (_HEADING_BAGIAN, "num_section"),
        (_HEADING_PARAGRAF, "paragraf"),
        (_HEADING_PASAL, "article"),
        (_HEADING_CN, "section"),
        (_HEADING_CN_PAREN, "subsection"),
        (_ITEM_NUM, "item"),
        (_ITEM_PAREN, "item"),
        (_ITEM_AYAT, "item"),
        (_ITEM_HURUF, "item"),
    ):
        match = regex.match(stripped)
        if match:
            marker = match.group(1)
            if regex is _ITEM_AYAT:
                marker = f"ayat ({marker})"
            elif regex is _ITEM_HURUF:
                marker = f"huruf {marker}"
            return kind, marker, stripped
    return "text", "", stripped


def _parse_blocks(text: str) -> list[dict]:
    """把文档拆成带层级的条款块。"""
    lines = text.splitlines()
    blocks: list[dict] = []
    path: list[str] = []
    buffer: list[str] = []
    buffer_path: list[str] = []
    buffer_clause = ""
    buffer_is_article = False
    current_page = 0
    current_ayat = ""
    current_article = ""
    seen_structure = False

    def flush() -> None:
        nonlocal buffer, buffer_path, buffer_clause, buffer_is_article
        content = " ".join(part.strip() for part in buffer).strip()
        if content:
            blocks.append({
                "path": list(buffer_path),
                "clause_id": buffer_clause,
                "text": content,
                "page": current_page,
                "front_matter": not seen_structure,
            })
        buffer = []
        buffer_path = []
        buffer_clause = ""
        buffer_is_article = False

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            flush()
            i += 1
            continue

        # PDF 提取文本中的页码标记，用于引用定位
        page_match = _PAGE_MARKER.match(stripped)
        if page_match:
            flush()
            current_page = int(page_match.group(1))
            i += 1
            continue

        # Markdown 表格：保留表头与行关系
        if "|" in stripped and i + 1 < len(lines) and _TABLE_SEP.match(lines[i + 1].strip()):
            flush()
            table_lines = [stripped]
            i += 1
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                table_lines.append(lines[i].strip())
                i += 1
            blocks.append({
                "path": list(path),
                "clause_id": "",
                "text": "\n".join(table_lines),
                "page": current_page,
                "front_matter": not seen_structure,
                "table_lines": table_lines,
                "table_header": _split_row(table_lines[0]),
            })
            continue

        kind, marker, full = _classify_line(stripped)

        # PDF 换行会把一句话拆到下一行；若上一行没有句末标点，
        # 形似条款编号的行应视为续行，而不是新条款。
        # 但 Pasal/第X条 标题行本身不完整，后面紧跟的 ayat 不是续行。
        if kind == "item" and buffer and not buffer_is_article:
            last_line = buffer[-1].rstrip()
            if last_line and last_line[-1] not in _SENTENCE_ENDS:
                buffer.append(stripped)
                i += 1
                continue

        if kind in ("chapter", "num_section", "paragraf", "section", "subsection"):
            flush()
            seen_structure = True
            current_ayat = ""
            current_article = ""
            # 标题写在下一行时（如 "Paragraf Kesatu" + "Perizinan Berusaha"），
            # 并入章节路径，避免产生只有标题的噪声块。
            if kind != "article" and full.strip() == marker.strip():
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    candidate = lines[j].strip()
                    if (len(candidate) <= 80
                            and candidate[-1] not in _SENTENCE_ENDS
                            and _classify_line(candidate)[0] == "text"):
                        full = f"{full} {candidate}"
                        i = j
            if kind == "chapter":
                path = [full]
            elif kind == "num_section":
                base = [p for p in path if _HEADING_CHAPTER.match(p)]
                path = base + [full]
            elif kind == "paragraf":
                base = [p for p in path if not p.startswith("Paragraf ")]
                path = base + [full]
            elif kind == "section":
                base = [p for p in path
                        if not re.match(r"^[一二三四五六七八九十]+、", p)
                        and not p.startswith("（")]
                path = base + [full]
            else:
                base = [p for p in path if not p.startswith("（")]
                path = base + [full]
            i += 1
            continue

        if kind == "article":
            flush()
            seen_structure = True
            current_ayat = ""
            current_article = marker
            buffer = [full]
            buffer_path = list(path)
            buffer_clause = marker
            buffer_is_article = True
            i += 1
            continue

        if kind == "item":
            flush()
            buffer_is_article = False
            if marker.startswith("ayat ("):
                current_ayat = marker
                clause = " ".join(part for part in (current_article, marker) if part)
            elif marker.startswith("huruf "):
                clause = " ".join(
                    part for part in (current_article, current_ayat, marker) if part
                )
            else:
                clause = marker
            buffer = [full]
            buffer_path = list(path)
            buffer_clause = clause
            i += 1
            continue

        if not buffer:
            buffer_path = list(path)
        buffer_is_article = False
        buffer.append(stripped)
        i += 1

    flush()
    return blocks


def _split_table_block(block: dict, size: int) -> list[dict]:
    lines = block["table_lines"]
    header, separator, rows = lines[0], lines[1], lines[2:]
    if not rows:
        return [{"text": "\n".join(lines), "table_header": block["table_header"]}]

    groups: list[list[str]] = []
    current: list[str] = []
    current_len = len(header) + len(separator)
    for row in rows:
        if current and current_len + len(row) > size:
            groups.append(current)
            current = []
            current_len = len(header) + len(separator)
        current.append(row)
        current_len += len(row) + 1
    if current:
        groups.append(current)

    return [
        {
            "text": "\n".join([header, separator, *group]),
            "table_header": block["table_header"],
        }
        for group in groups
    ]


def chunk_document(text: str, size: int = 400, overlap: int = 80) -> list[dict]:
    """按条款结构切分文档，返回带层级、相邻关系和交叉引用的 chunk。"""
    blocks = _parse_blocks(text)
    clause_ids = {
        idx: (block.get("clause_id") or f"p{idx}")
        for idx, block in enumerate(blocks)
    }

    expanded: list[tuple[int, int, dict]] = []
    for idx, block in enumerate(blocks):
        if block.get("table_lines"):
            for part_no, part in enumerate(_split_table_block(block, size)):
                expanded.append((idx, part_no, part))
            continue
        body = block["text"]
        if len(body) <= size:
            expanded.append((idx, 0, {"text": body}))
        else:
            for part_no, piece in enumerate(_split_long_text(body, size, overlap)):
                expanded.append((idx, part_no, {"text": piece}))

    chunks: list[dict] = []
    for chunk_no, (idx, part_no, part) in enumerate(expanded):
        if len(part["text"].strip()) < MIN_CHUNK_CHARS:
            continue
        block = blocks[idx]
        section_path = " > ".join(block["path"])
        clause_id = clause_ids[idx]
        searchable = "\n".join(
            item for item in (section_path, clause_id, part["text"]) if item
        )
        chunks.append({
            "chunk_id": f"#{chunk_no:04d}",
            "block_index": idx,
            "section_path": section_path,
            "clause_id": clause_id,
            "part": part_no,
            "page": block.get("page", 0),
            "front_matter": block.get("front_matter", False),
            "text": searchable,
            "content": part["text"],
            "cross_refs": _extract_cross_refs(block["text"]),
            "table_header": part.get("table_header") or block.get("table_header") or [],
        })

    # 没有法条结构的文档（如平台帮助页）不应被当成“前言”
    if chunks and all(chunk["front_matter"] for chunk in chunks):
        for chunk in chunks:
            chunk["front_matter"] = False

    block_order: list[int] = []
    for chunk in chunks:
        if not block_order or block_order[-1] != chunk["block_index"]:
            block_order.append(chunk["block_index"])

    prev_map: dict[int, str] = {}
    next_map: dict[int, str] = {}
    for i, idx in enumerate(block_order):
        prev_map[idx] = clause_ids[block_order[i - 1]] if i > 0 else ""
        next_map[idx] = clause_ids[block_order[i + 1]] if i + 1 < len(block_order) else ""

    for chunk in chunks:
        chunk["prev_clause_id"] = prev_map.get(chunk["block_index"], "")
        chunk["next_clause_id"] = next_map.get(chunk["block_index"], "")
    return chunks


# ── 索引与检索 ──

def load_manifest() -> list[dict]:
    documents = []
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                documents.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"manifest.jsonl 第 {line_no} 行不是合法 JSON: {exc}") from exc
    return documents


def load_index() -> dict:
    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            f"索引不存在: {INDEX_PATH}\n请先运行: python scripts/build_index.py"
        )
    with open(INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)


def _matches(chunk: dict, country: str | None, platform: str | None, doc_type: str | None) -> bool:
    if country and doc_country(chunk) not in ANY_COUNTRY and doc_country(chunk) != country.lower():
        return False
    if platform and doc_platform(chunk) not in ANY_PLATFORM and doc_platform(chunk) != platform.lower():
        return False
    if doc_type and chunk.get("doc_type") != doc_type:
        return False
    return True


def build_result(score: float, chunk: dict) -> dict:
    """统一的检索结果结构，BM25 / 向量 / 混合检索共用。"""
    return {
        "score": round(score, 4),
        "chunk_id": chunk["chunk_id"],
        "doc_id": chunk["doc_id"],
        "citation_doc_id": chunk.get("citation_doc_id") or chunk["doc_id"],
        "title": chunk.get("title", ""),
        "section_path": chunk.get("section_path", ""),
        "clause_id": chunk.get("clause_id", ""),
        "page": chunk.get("page", 0),
        "front_matter": chunk.get("front_matter", False),
        "prev_clause_id": chunk.get("prev_clause_id", ""),
        "next_clause_id": chunk.get("next_clause_id", ""),
        "cross_refs": chunk.get("cross_refs", []),
        "table_header": chunk.get("table_header", []),
        "text": chunk["text"],
        "content": chunk.get("content", chunk["text"]),
        "country": chunk.get("country", ""),
        "platform": chunk.get("platform", ""),
        "doc_type": chunk.get("doc_type", ""),
        "published_at": chunk.get("published_at", "unknown"),
        "effective_from": chunk.get("effective_from", "unknown"),
        "effective_to": chunk.get("effective_to", "unknown"),
        "collected_at": chunk.get("collected_at", "unknown"),
        "source_url": chunk.get("source_url", ""),
    }


def bm25_search(index: dict, query: str, top_k: int = 5, country: str | None = None,
                platform: str | None = None, doc_type: str | None = None,
                aggregate_docs: bool = False,
                k1: float = 1.5, b: float = 0.75) -> list[dict]:
    """对 chunks 做 BM25 检索，返回带分数和元数据的结果。

    aggregate_docs=True 时按「引用文档」聚合（取每篇文档的最高分块），
    适合评测/文档级召回；生成提示词时应保持 chunk 级，以保留不同条款。
    """
    chunks = [c for c in index["chunks"]
              if _matches(c, country, platform, doc_type)]
    if not chunks:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    n = len(chunks)
    avgdl = sum(len(c["tokens"]) for c in chunks) / n
    doc_freq: Counter = Counter()
    for chunk in chunks:
        doc_freq.update(set(chunk["tokens"]))

    scored = []
    for chunk in chunks:
        term_freq = Counter(chunk["tokens"])
        length = len(chunk["tokens"])
        score = 0.0
        for token in query_tokens:
            if token not in term_freq:
                continue
            idf = math.log(1 + (n - doc_freq[token] + 0.5) / (doc_freq[token] + 0.5))
            denom = term_freq[token] + k1 * (1 - b + b * length / avgdl)
            score += idf * term_freq[token] * (k1 + 1) / denom
        if chunk.get("front_matter"):
            score *= FRONT_MATTER_WEIGHT
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)

    if aggregate_docs:
        best_by_doc: dict[str, tuple[float, dict]] = {}
        for score, chunk in scored:
            key = chunk.get("citation_doc_id") or chunk["doc_id"]
            best_by_doc.setdefault(key, (score, chunk))
        scored = list(best_by_doc.values())

    results = []
    for score, chunk in scored[:top_k]:
        results.append(build_result(score, chunk))
    return results


def format_evidence(results: list[dict]) -> str:
    if not results:
        return "（未检索到相关证据）"
    blocks = []
    for i, item in enumerate(results, 1):
        lines = [
            f"[证据 {i}]",
            f"引用 doc_id: {item['citation_doc_id']}",
            f"标题: {item['title']}",
            f"章节/条款: {item['section_path']} / {item['clause_id']}",
            f"页码: {item.get('page') or 'unknown'}",
            f"国家/平台/类型: {item['country']}/{item['platform']}/{item['doc_type']}",
            f"发布/生效/采集: {item['published_at']} / {item['effective_from']} / {item['collected_at']}",
        ]
        if item["prev_clause_id"] or item["next_clause_id"]:
            lines.append(f"相邻条款: 上 {item['prev_clause_id'] or '—'} / 下 {item['next_clause_id'] or '—'}")
        if item["cross_refs"]:
            lines.append(f"交叉引用: {', '.join(item['cross_refs'])}")
        if item["table_header"]:
            lines.append(f"表格表头: {' | '.join(item['table_header'])}")
        lines.append(f"内容:\n{item['content']}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)
