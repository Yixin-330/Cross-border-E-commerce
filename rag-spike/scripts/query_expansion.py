"""中文查询 → 印尼语领域同义词扩展。

仅扩展中文查询；印尼语查询保持原样，避免改变已经验证的 BM25 基线。
扩展词只用于第一阶段召回，rerank 仍使用原始用户查询。
"""
import re

_CJK = re.compile(r"[一-鿿]")

# 关键词 → 印尼语检索词。按中文词长度从长到短匹配，避免短词抢先。
EXPANSIONS: dict[str, list[str]] = {
    "处罚措施": ["sanksi", "tindakan", "penangguhan", "pengakhiran akun", "tindakan hukum"],
    "处罚": ["sanksi", "tindakan", "penangguhan", "pengakhiran akun", "tindakan hukum"],
    "措施": ["tindakan", "sanksi", "penangguhan"],
    "违规": ["pelanggaran", "melanggar"],
    "违反": ["pelanggaran", "melanggar"],
    "禁限售": ["barang yang dilarang dan dibatasi", "dilarang", "dibatasi"],
    "禁止": ["dilarang", "larangan"],
    "限制": ["dibatasi", "pembatasan"],
    "营业许可": ["perizinan berusaha", "perizinan"],
    "许可": ["perizinan", "perizinan berusaha", "izin"],
    "执照": ["perizinan", "perizinan berusaha"],
    "认证": ["sertifikasi", "sertifikat"],
    "标签": ["label", "label berbahasa indonesia"],
    "进口": ["impor"],
    "关税": ["bea masuk", "tarif"],
    "卖家": ["penjual"],
    "买家": ["pembeli"],
    "平台": ["platform", "ppmse"],
    "语言": ["bahasa indonesia", "bahasa inggris"],
    "重量": ["berat"],
    "尺寸": ["dimensi"],
    "验证": ["verifikasi"],
    "数据": ["data"],
    "人工智能": ["kecerdasan artifisial"],
    "收费": ["biaya", "dipungut biaya"],
    "生效": ["mulai berlaku", "diundangkan"],
    "失效": ["tidak berlaku", "dicabut"],
    "商品页面": ["halaman produk"],
    "链接": ["menghubungkan", "situs web lain"],
    "网站": ["situs web"],
    "外链": ["menghubungkan", "situs web lain"],
    "经营者": ["pelaku usaha"],
    "政策": ["kebijakan"],
}


def is_cjk(text: str) -> bool:
    return bool(_CJK.search(text))


def should_expand(query: str, mode: str, explicit: bool = False) -> bool:
    """auto 模式对中文默认扩展；其他模式仅在显式 --expand 时扩展。"""
    return explicit or (mode == "auto" and is_cjk(query))


def expand_query(query: str, max_terms: int = 24) -> tuple[str, list[str]]:
    """返回 (扩展后的查询, 命中的印尼语词)。非中文查询原样返回。"""
    if not _CJK.search(query):
        return query, []

    matched: list[str] = []
    for term in sorted(EXPANSIONS, key=len, reverse=True):
        if term in query:
            matched.extend(EXPANSIONS[term])

    seen: set[str] = set()
    terms: list[str] = []
    for term in matched:
        key = term.lower()
        if key not in seen:
            seen.add(key)
            terms.append(term)
        if len(terms) >= max_terms:
            break

    if not terms:
        return query, []
    return f"{query} {' '.join(terms)}", terms
