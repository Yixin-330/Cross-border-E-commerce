# 语料采集与标注规范

## 文件组织

```
raw/
  <country>/          # 国家代码：id / th / vn / ph / my / sg
    policy/           # 海关、认证、进口限制等官方规定
    platform/         # Shopee / Lazada / TikTok Shop 的入驻、类目、费用规则
    report/           # 行业报告、品类研究、白皮书
    review/           # 商品评论、买家反馈（后续阶段）
```

文件名使用 `<doc_id>.txt` 或 `<doc_id>.md`，例如：

```
raw/id/policy/id-toy-sni-2025.txt
raw/id/platform/shopee-id-category-rules-2026-03.txt
```

## manifest.jsonl 字段

每行一个 JSON 对象：

| 字段 | 必填 | 说明 |
|---|---|---|
| `doc_id` | 是 | 全局唯一，建议 `国家-主题-来源-年月` |
| `title` | 是 | 文档标题 |
| `file` | 是 | 相对 `corpus/` 的路径 |
| `country` | 是 | `id/th/vn/ph/my/sg`；跨区域用 `sea`（视为不限国家） |
| `platform` | 是 | `shopee/lazada/tiktok/tokopedia`；国家法规用 `any`（不限平台） |
| `doc_type` | 是 | `policy/platform/report/review` |
| `category` | 否 | 品类方向，如 `toys` |
| `language` | 否 | 文档语言 `zh/id/en/th/vi` |
| `original_doc_id` | 译稿必填 | 译文对应的原文 `doc_id`；引用落回原文 |
| `source_language` | 否 | 原文语言 |
| `published_at` | 是 | 发布日期 `YYYY-MM-DD`，未知填 `unknown` |
| `effective_from` | 是 | 生效日期；判断时效以此为准 |
| `effective_to` | 否 | 失效日期，未知填 `unknown` |
| `collected_at` | 是 | 采集时间 `YYYY-MM-DD`，**不能替代生效日期** |
| `review_status` | 是 | `pending/approved/rejected`，machine 提取默认 `pending` |
| `reviewed_by` | 审核后填 | 审核人 |
| `reviewed_at` | 审核后填 | 审核时间 |
| `source_url` | 否 | 原文链接 |
| `notes` | 否 | 适用范围、失效提醒等 |

示例（国家法规，不限平台）：

```json
{"doc_id":"id-toy-sni-2025","title":"印尼儿童玩具SNI认证要求","file":"raw/id/policy/id-toy-sni-2025.txt","country":"id","platform":"any","doc_type":"policy","category":"toys","language":"zh","original_doc_id":"","published_at":"2025-06-01","effective_from":"2025-07-01","effective_to":"unknown","collected_at":"2026-11-02","review_status":"pending","reviewed_by":"","reviewed_at":"","source_url":"","notes":""}
```

## 结构约定

切分脚本会识别以下结构，采集/清洗时尽量保留：

- **中文层级**：`第一章`、`第X节`、`一、`、`（一）`；
- **印尼法规层级**：`BAB I`（章）、`Bagian Kesatu`（节）、`Pasal 5`（条）、`ayat (1)`（款）、`huruf a`（项）；
- **条款**：中文 `第X条`/印尼语 `Pasal X`、`1.`、`（1）`，每个条款独立成块，并记录相邻条款；
- **交叉引用**：正文中的「见第 X 条」「依据第 X 条」「Pasal X ayat (Y)」会被抽取到 `cross_refs`；
- **表格**：转成 Markdown 表格（`| 表头 | ... |` + `| --- |` 分隔行），切分时保留表头；
- **页码**：PDF 提取文本保留 `[[PAGE n]]` 标记，切分后会写入 chunk 的 `page` 字段；
- **译文**：译文与原文分别登记，译文用 `original_doc_id` 回链，引用只落到原文。

## 审核门

1. 机器提取的文档 `review_status` 一律写 `pending`；
2. `python scripts/review.py list` 查看待审文档；
3. 人工核对来源、日期、条款完整性和翻译质量后：
   `python scripts/review.py approve <doc_id> --by 你的名字`
4. `build_index.py` 只索引 `approved` 文档；`pending/rejected` 不会进入可用语料快照。

## 质量规则

1. **优先官方或权威来源**：政府部门、平台官方规则页、认证机构、行业协会。
2. **保留发布日期和来源链接**，无法确定日期的文档标记 `unknown`，检索结果中会一并展示。
3. **文档内容尽量完整**，不要只截取一两句话；切分由脚本完成。
4. 同一主题有多个版本时，保留最新版并在 `notes` 中注明旧版失效情况。
5. 采集前先确认**可获得性**：如果目标文档大面积无法访问或过期，应缩小场景或更换国家，不要用编造内容填补。
