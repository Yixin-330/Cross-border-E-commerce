# RAG Spike — 跨境电商合规与选品情报助手

与主项目隔离的实验目录，用于验证「语料 + 检索 + 引用」这一层的可行性。
这里的产出不接入 `backend/` 和 `index.html`，验证通过后再考虑集成。

## 为什么先做这一层

RAG 项目的成败主要取决于语料质量和评测标准，而不是框架选型。本目录先跑通：

```
语料 → 切分 → 检索 → 带引用提示词 → 评测
```

索引和检索目前使用**零依赖的 BM25 基线**（对中文按字 + 二元组切分），
目的不是最终方案，而是先建立一个可以和后续 embedding 方案对比的基线。

## 目录结构

```
rag-spike/
├── corpus/
│   ├── manifest.jsonl          # 文档元数据索引（每行一个文档）
│   ├── raw/                    # 原始文档（.txt / .md），按 raw/<国家>/<类型>/ 组织
│   │   └── _samples/           # 示例文档：仅用于跑通流程，必须替换
│   └── README.md               # 采集与标注规范
├── eval/
│   ├── questions.jsonl         # 评测集（status=draft 的条目会被跳过）
│   └── README.md               # 题型分布与评分说明
├── schemas/
│   └── selection_answer.schema.json   # 最终输出契约
├── prompts/
│   └── answer_with_citations.md       # 带引用的回答提示词模板
├── scripts/
│   ├── retrieval.py            # 公共库：分词、条款切分、BM25、日期/平台归一化
│   ├── vector_retrieval.py     # 向量检索 + RRF 混合检索（需 fastembed）
│   ├── embed_index.py          # 构建向量索引（需 .venv-embed）
│   ├── build_index.py          # 构建 BM25 索引（仅 approved 文档）
│   ├── review.py               # 审核门：import/list/show/set/approve/reject
│   ├── retrieve.py             # 命令行检索（bm25/vector/hybrid）
│   ├── evaluate.py             # hit@k / MRR 评测（支持三种模式）
│   └── build_prompt.py         # 根据问题 + 检索结果生成提示词
├── requirements-embed.txt      # 向量检索依赖（fastembed）
└── index/                      # 构建产物（自动生成，可删除重建）
```

## 环境要求

Python 3.10+，**无第三方依赖**。

## 快速开始

```bash
cd rag-spike

# 0. 导入 staging 批次并审核（机器提取默认 pending）
python scripts/review.py import corpus/staging/<批次>/manifest.pending.jsonl
python scripts/review.py list
# 核对官方原件后补日期/标题（不得用采集时间代替生效日期）：
python scripts/review.py set <doc_id> --title "..." --published-at 2026-01-01 --effective-from 2026-02-01
python scripts/review.py approve <doc_id> --by 你的名字
# 仅留档、暂不索引（如待 OCR）：
python scripts/review.py approve <doc_id> --by 你的名字 --no-index

# 1. 构建索引（只索引 approved 文档，可调切分参数）
python scripts/build_index.py --size 400 --overlap 80

# 2. 检索
python scripts/retrieve.py "印尼儿童玩具需要什么认证" --country id --top 5

# 3. 评测（只运行 status 为 sample/ready 的题目）
python scripts/evaluate.py --top 3

# 印尼语 MVP 初稿（draft）评测
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3

# 4. 生成带引用的回答提示词
python scripts/build_prompt.py "在印尼通过 Shopee 销售带蓝牙的儿童玩具，需要哪些认证？" --country id
```

## 向量与混合检索（可选）

BM25 是默认模式，不需要额外依赖。向量/混合检索使用 fastembed + ONNX，装在独立 venv 中：

```bash
python -m venv .venv-embed
.venv-embed/Scripts/pip install -r requirements-embed.txt

# 构建向量索引（首次会下载约 220MB 多语言模型）
.venv-embed/Scripts/python scripts/embed_index.py

# 三种检索模式 + 自动路由
.venv-embed/Scripts/python scripts/retrieve.py "Apa kewajiban pelaku usaha PMSE?" --country id --mode bm25
.venv-embed/Scripts/python scripts/retrieve.py "Apa kewajiban pelaku usaha PMSE?" --country id --mode vector
.venv-embed/Scripts/python scripts/retrieve.py "Apa kewajiban pelaku usaha PMSE?" --country id --mode hybrid
.venv-embed/Scripts/python scripts/retrieve.py "Shopee 对违规卖家有什么处罚？" --platform shopee --mode auto

# 三种模式使用同一套评测题
.venv-embed/Scripts/python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3 --mode hybrid
```

### MVP 检索结论

| 查询语言 | 最优模式 | 说明 |
|---|---|---|
| 印尼语 | BM25 | 法律文本术语精确，词面匹配强；向量/混合没有超过 BM25 |
| 中文 | hybrid | BM25 无法跨语言；hybrid 的中文条款证据命中从 33% 提升到 83% |

因此 `--mode auto` 默认按查询语言路由：检测到中文 → hybrid，否则 → BM25。该结论基于当前 5 篇文档和 26 条题，属于方向性结论，扩充语料后需重跑。

- 模型：`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`（384 维，多语言，CPU 可跑）；
- 向量索引保存在 `index/embeddings.npz`，按 `chunk_id + text_hash` 增量更新；
- 混合检索用 RRF（reciprocal rank fusion），不直接比较 BM25 与余弦分数的绝对大小；
- 语料只有几千块时用 numpy 计算即可，不需要向量数据库。

## 切分与召回口径

- **条款感知切分**：识别中文 `第一章/第X节/第X条/一、/第X条` 和印尼法规 `BAB/Bagian/Pasal/ayat (n)/huruf a`，每个条款独立成块，chunk 携带 `section_path`、`clause_id`、相邻条款和 `cross_refs`；超长条款才按 `--size/--overlap` 二次切分。
- **页码**：PDF 提取文本中的 `[[PAGE n]]` 会记录到 chunk 的 `page` 字段，用于引用定位。
- **表格**：清洗阶段转成 Markdown 表格；切分时保留表头，超长表格按行拆分并重复表头。
- **按文档召回**：`evaluate.py` 使用 `aggregate_docs=True`，按引用文档取最高分块后再排名，避免长文档的多个块挤占其他文档。
- **日期语义**：`published_at` 是发布日期，`effective_from/effective_to` 是生效/失效日期，`collected_at` 是采集时间。判断时效以生效日期为准，采集时间不能替代。
- **平台语义**：`platform=any` 表示不限平台（国家法规），按 Shopee 过滤时不会被排除。
- **译文**：译文文档用 `original_doc_id` 回链原文，检索可用译文，但引用必须落回原文。
- **语言**：当前 BM25 不做跨语言检索。语料是印尼语时，评测问题必须用印尼语或补充中文译文（`original_doc_id` 回链），否则中文问题无法命中。

## 审核门

机器提取的文档先进入 `review_status=pending`，不会进入索引。人工核对来源、日期、条款完整性和翻译质量后，用 `review.py approve` 放行；`rejected` 文档永久排除。仅审核通过还不够：只有 `index_eligible=true` 的文档才会进入语料快照，扫描件、待 OCR、待核验发布的文档用 `approve --no-index` 留档。`build_index.py` 生成的是只包含「approved + index_eligible」文档的快照。

## 接入真实语料的步骤

1. 按 `corpus/README.md` 的规范收集文档，放入 `corpus/raw/<国家>/<类型>/`。
2. 在 `corpus/manifest.jsonl` 中为每份文档补一行元数据，机器提取的文档先标 `review_status: pending`。
3. 删除 `_samples/` 下的示例文档及其 manifest 条目（或保留，但不要让它们出现在真实评测里）。
4. 运行 `python scripts/review.py list`，逐份核对来源、日期、条款完整性和译文质量后 `approve`。
5. 按 `eval/README.md` 扩充到 **至少 20 条** `status=ready` 的评测题。
6. 重新构建索引并运行 `evaluate.py`。

## 进入下一阶段的门槛

- 至少 20 条 ready 评测题；
- `hit@5 >= 0.80`，失败案例逐条过一遍；
- 所有政策类结论都能回溯到具体 `doc_id` 和发布日期；
- 语料覆盖的时效性经过人工确认。

达到门槛后再做：封装 `KnowledgeAgent` → 接入 FastAPI → 用 LangGraph 增加证据评分/重查/反思分支 → 前端结论页。

## 注意

- `corpus/raw/_samples/` 中的文档是**合成的示例内容**，仅用于验证脚本可运行，不得用于任何真实分析或对外演示。
- 本目录不修改主项目任何文件。
