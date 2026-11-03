# 答案级评测：第一阶段操作与评分规范

## 边界
这是独立的生成层回放基线，不是端到端验收。原检索题集不变，修订派生集为 `../questions.answer-eval.jsonl`。32题按语义案例分组：开发14、回归7、留出11。源题此前已经被讨论/用于检索实验，留出集只是从本轮生成调参起保留，不是全新盲测集。后续正式发布应补充未见案例。

语料尚不支持完整积木合规判定。题集主要验证通用政策问答、拒答和追问；酒精饮料题明确是域外控制题，不能证明积木合规能力。

## 已完成的执行链路
1. `python rag-spike/scripts/prepare_answer_eval.py` 创建修订派生集，按案例分组而不是逐题随机切分；评分要点按语义理解，允许跨语言表达。gold为agent核对、待人审，不宣称人类专家已认可。
2. `python rag-spike/scripts/answer_eval.py freeze --output rag-spike/eval/answer/<new-batch>/evidence.jsonl` 固定实际召回正文、顺序和证据ID；记录问题/索引/证据哈希。默认top5、BM25+中文扩展，无重排。本机embedding venv启动失败，因此该基线明确区别于线上auto+rerank。
3. `python rag-spike/scripts/answer_eval.py run --evidence rag-spike/eval/answer/<batch>/evidence.jsonl --output rag-spike/eval/runs/<new-run>` 使用真实provider，默认只运行dev,regression一次。mock必须显式`--mock`，不得计为有效回答；留出集需显式`--splits holdout --allow-holdout`，本轮未运行。
4. 线上answer()与评测answer_from_evidence()复用同一生成函数。评测不重新检索，不向生成模型发送gold、评分要点、禁止项或分组标签。空证据也允许模型提出必要追问。
5. 确定性检查仅验证结构、输入绑定的引用、定位、摘录和追问字段等，禁句仅为人工复核预警；不把硬检查通过解释为语义正确。
6. 首轮输出原始答案、硬检查和15条人审校准表。人工尚未填写，不能称已完成judge校准。

## 人工校准方法（每个维度0–2）
先读questions.jsonl的题目/上下文、gold_answer_points及原文，再读evidence.jsonl中实际送入模型的证据，最后看answers.jsonl。不可只看gold_answer或检索文档标题。

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| correctness | 核心结论错误/适用主体或范围错误 | 部分正确但有实质偏差 | 核心结论正确且范围准确 |
| completeness | 主要必要要点缺失 | 覆盖部分必要要点 | 完整覆盖适用于本题的必要要点 |
| faithfulness | 核心结论超出实际输入证据 | 次要推断缺依据 | 实质性断言均有输入依据，缺口明确 |
| citation_support | 引用不支持核心claim | 仅部分支持或条件遗漏 | 逐项支持且保留条件/例外 |

behavior_ok：检查是否真正回答/提出必要追问/说明证据不足。字段非空、verdict正确都不是行为正确的充分条件。多个acceptable_behaviors为可接受的行为组合，不能仅按标签字面判断。

引用无需出现的纯追问/拒答案例，citation_support填null并在reason标明不适用；不要自动给满分。必要gold证据没有进入冻结包时，完整性按“说明证据缺口和适当保留判断”审阅，不因模型没有补出缺失事实而直接扣分；同时记录missing_points由证据还是生成造成。

must_not_say命中需判断语义：否定、转述风险、指出无法推断不算作出该断言。日期、平台政策与国家法规、经营者与普通卖家、网页语言与包装标签是重点。

填写human_review.jsonl：reviewer、reviewed_at、各维度、behavior_ok、unsupported_claims、missing_points、reason；完成后review_status改为completed。只有真实人类审核人填写才计作人工评分。模型不得代填人工评分。

目前没有LLM judge，不报告judge与人工一致率、语义通过率或“未编造合规要求”。每个比率保留分母，mock/失败不能伪装成成功拒答。P95为生成调用耗时，不含检索或judge。

## 后续
完成15条人工校准后再接judge。日常跑dev/regression；发布候选同题三次，留出集只在配置确定后运行。后续建立auto+rerank冻结包时必须新建批次，不能覆盖旧包，并把两种检索配置分开报告。
