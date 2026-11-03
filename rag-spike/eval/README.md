# 评测集说明

## 题型

| 类型 | 说明 | 期望行为 |
|---|---|---|
| `answerable` | 语料中可以找到依据的问题 | 给出结论并引用 `gold_doc_ids` 中的文档 |
| `clarification` | 信息不足、需要追问的问题 | 提出澄清问题，而不是直接给结论 |
| `uncovered` | 语料未覆盖的问题 | 明确说明"信息不足/未检索到依据"，不得编造 |

建议 20 条 ready 题的分布：12 条 answerable、4 条 clarification、4 条 uncovered。
**不要把同一批题同时用于调参和最终汇报**，至少留出 1/3 作为 hold-out。

## 字段

| 字段 | 说明 |
|---|---|
| `id` | 唯一编号 |
| `status` | `draft` 的题会被评测跳过；填写完整后改为 `ready` |
| `question_type` | `answerable/clarification/uncovered` |
| `question` | 用户问题原文 |
| `country` / `platform` | 检索过滤条件，可留空 |
| `gold_answer` | 人工撰写的标准答案要点 |
| `gold_doc_ids` | 应被引用到的原文文档 ID 列表（译文题填 `original_doc_id`）；clarification/uncovered 留空 |
| `expected_behavior` | `answer_with_citation / ask_clarification / refuse_uncovered` |
| `notes` | 出题依据或备注 |

## 运行

```bash
# 只跑 sample/ready 题（默认）
python scripts/evaluate.py --top 3

# 跑印尼语 MVP 初稿（status=draft），用于校对前看基线
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3

# 对比三种检索模式（vector/hybrid 需要 .venv-embed）
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3 --mode bm25
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3 --mode vector
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3 --mode hybrid
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --include-draft --top 3 --mode auto

# 中文跨语言冒烟集（验证中文 UI 查询印尼语语料）
python scripts/evaluate.py --questions eval/questions.zh-smoke.jsonl --include-draft --top 3 --evidence-top 20 --mode auto

# rerank（第一阶段 top-50 → cross-encoder → top-5）
python scripts/evaluate.py --questions eval/questions.id-mvp.jsonl --top 3 --evidence-top 5 --mode auto --rerank --rerank-pool 50

# 中文查询 + 自动扩展 + rerank；无扩展对照用 --mode hybrid
python scripts/evaluate.py --questions eval/questions.zh-smoke.jsonl --include-draft --top 3 --evidence-top 5 --mode auto --rerank --rerank-pool 50
python scripts/evaluate.py --questions eval/questions.zh-smoke.jsonl --include-draft --top 3 --evidence-top 5 --mode hybrid --rerank --rerank-pool 50
```

注意：当 `--top` 大于等于语料文档数时，hit@k 结构性为 100%，没有区分度；当前 5 篇文档建议用 `--top 3`。

## 指标

`evaluate.py` 目前计算检索层指标：

- **hit@k**：top-k 检索结果中是否命中任一 `gold_doc_ids`；
- **MRR**：第一个命中文档的排名倒数。

clarification / uncovered 题不参与检索指标，单独统计数量，回答行为需要人工检查或后续接入 LLM 自动评测。

生成层（接入模型后）还需要检查：

- 每条结论的 `doc_id` 是否真实存在，且内容能支撑结论；
- 生效日期是否覆盖问题所处时间，是否误把采集时间当生效时间；
- 译文题是否引用回原文 `doc_id`；
- uncovered 题是否正确拒答，而不是编造；
- 表格类引用是否保留表头语义。

## 扩充流程

1. 每收集一批新文档，就为它出 2–3 道题；
2. 至少包含一道"文档没写、容易被模型编造"的 uncovered 题；
3. 标准答案先人工写，不参考模型输出；
4. 定期抽查模型回答是否真的被引用的文档支撑；
5. **题目语言要与语料语言一致**：语料是印尼语时用印尼语出题（或先做译文并用 `original_doc_id` 回链），否则 BM25 无法跨语言命中。


## 答案级冻结证据评测

执行方式、数据划分及人工评分规则见 [answer/README.md](answer/README.md)。首轮报告见 [runs/answer-baseline-20261102/report.md](runs/answer-baseline-20261102/report.md)。人工评分尚待填写，不能把硬检查通过率作为答案正确率。
