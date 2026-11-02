# 印尼语MVP评测集核对

核对日期：2026-11-02。原文件 questions.id-mvp.jsonl 未修改；全部保持draft。核对依据为项目实际manifest、评测脚本及已采集原文。

## 总体结论
20行均为合法JSON，ID唯一；12 answerable、4 clarification、4 uncovered。所有可回答题的gold文档ID均存在于当前登记中。印尼语问题整体通顺，但标准答案存在范围、完整性和时效设计问题；目前适合检索冒烟测试，不宜当作积木合规验收集。

## 逐题意见
| ID尾号 | 意见 |
|---|---|
| 001 | 定义正确，可保留；补Pasal 1 angka 2，属于基础知识题。 |
| 002 | 定义基本正确，可保留；补Pasal 1 angka 10。 |
| 003 | 答案需明确Perizinan Berusaha Bidang PMSE，并回链Pasal 4(3)的PSP例外；不能把平台经营者PPMSE义务直接套到普通Shopee卖家。依据Pasal 7(1)。 |
| 004 | 答案受Pasal 19支持；仅指该许可签发免费，不能扩大为开店/认证全部免费。 |
| 005 | 问题问AI使用规定，gold仅覆盖47(1)许可，漏47(2)-(3)责任。建议缩题为“Apakah Pelaku Usaha boleh menggunakan kecerdasan artifisial dalam penyelenggaraan PMSE?”，或扩答案覆盖标识、准确性、平台治理/投诉等。 |
| 006 | 酒精饮料超出积木场景；当前答案过泛，Pasal 3(1)、4(1)分别涉及IT、PI及进入关境前的要求。建议移至域外干扰集，不作为积木主验收题。 |
| 007 | 实质错误：LS adalah Laporan Surveyor只是缩写展开，未回答定义。必须修改。 |
| 008 | 所列处罚例子有原文支持，“antara lain”保留则不必穷举；补具体定位，不能表述为每次必然全部处罚。 |
| 009 | 与服务条款20.4一致，可保留。 |
| 010 | 与23.3首段一致；可补平台可要求支持或额外文件。23.4文本又出现23.3的交叉引用，存在源文件编号歧义，需记录，不能自行推定其法律效果。 |
| 011 | 社区规则支持印尼语或英语；建议问“Menurut Peraturan Komunitas Shopee, bahasa apa yang boleh digunakan dalam informasi pada halaman produk?”。gold明确这是线上商品信息，不代表实体包装/强制标签也可仅用英语。 |
| 012 | 社区规则禁止广告部分将外链列为例子；方向正确，补章节定位。 |
| 013 | 应追问；若国家、平台已由会话/产品固定，不应重复问，优先产品属性及销售路径。评测需要声明是否为无上下文请求。 |
| 014 | 应追问；加入材质、用途、年龄、是否带电等认证适用属性，不只问平台。 |
| 015 | 资金规划偏离政策语料；澄清经营规模后仍需成本数据，不能仅凭政策库给金额。建议移出核心集或改为双阶段行为题。 |
| 016 | 同时存在缺参数和缺销量数据；澄清后也不能凭政策库给畅销榜。gold需要求说明无销量依据。 |
| 017 | uncovered合理；税率还取决于HS归类、原产地/优惠待遇及日期，允许先追问，不能把单一拒答模板设为唯一正确输出。 |
| 018 | 当前可用索引缺完整SNI适用依据，不能给所有塑料玩具统一结论；但问题也缺年龄、用途等分类条件，允许追问+说明证据缺口。必须绑定语料快照，未来补文后标签需重审。 |
| 019 | 当前索引未覆盖，保留；应说明无法据本语料确定，不可把未覆盖解释为无需认证。 |
| 020 | 必须重写：2027-01-01相对核对日是未来；未来仍有效与历史生效日是两个问题。元数据unknown不能否定正文已有日期证据，也不能作为强制拒答的唯一依据。 |

## 建议替换文本
007 gold_answer：LS adalah dokumen tertulis hasil Verifikasi atau Penelusuran Teknis oleh surveyor yang menyatakan kesesuaian barang yang diimpor.
依据：Permendag 23/2025 Pasal 1 angka 17，PDF第4页。

020建议拆为两题：
- 可回答：Kapan Permendag Nomor 19 Tahun 2026 mulai berlaku menurut ketentuan penutupnya? 应核对正文生效条款并引用；官方目录记载2026-06-08。
- 未来时效：Dapatkah Anda memastikan bahwa Permendag Nomor 19 Tahun 2026 masih berlaku pada 1 Januari 2027? 应区分已知生效日期与未来修订/废止不确定性，不能保证未来仍有效；允许引用已知法规并说明边界，不要求完全无引用。

017—020 gold_answer目前为中文，若用于印尼语生成评测建议统一为印尼语；notes可保留中文。评测应按语义要点而非逐字匹配。

## 评测层面的缺口
- gold_doc_ids只有文档级，命中长文档不等于命中正确条款。建议加入gold_evidence（文档、条款、PDF页、必须支持的要点）。
- 12个可回答题只覆盖5份文档，其中5题来自同一法规；大部分为通用定义，缺少本地卖家身份、积木材质/年龄、材料缺口、认证证书型号覆盖、标签与页面语言差异、贸易路径和证据冲突等案例。未取得依据的主题只能做缺口/澄清题，不可编造gold。
- 当前evaluate.py仅计算有gold_doc_ids题的文档召回，8个行为题只计数，不能验证拒答/追问、引用支持度或答案正确性。gold_answer也未参与评分。
- 必须绑定corpus_snapshot_id、评估日期及会话上下文；uncovered随语料变化而变化，不能永久贴标签。
- 全部为draft，默认评测跳过；不应为满足20条ready门槛批量放行。

## 来源
- 电商法规原文：../corpus/staging/id-shopee-toys-20261102/government/ecommerce-19-2026.txt
- 消费品进口法规原文：../corpus/staging/id-shopee-toys-20261102/government/import-23-2025.txt
- Shopee原文：../corpus/staging/id-shopee-toys-20261102/platform/ 下三份TXT与HTML。
- 生效日期官方目录：https://peraturan.bpk.go.id/Details/351720/permendag-no-19-tahun-2026

本次仅核对评测资料，未修改语料审核状态、主manifest、索引或原题集。
