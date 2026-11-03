"""Re-score saved answers without calling the LLM or touching frozen evidence."""
import argparse,json,math
from collections import Counter
from pathlib import Path
from answer_eval import read,write,digest,check_answer,ROOT
from schemas.agent_schemas import KNOWLEDGE_AGENT_SCHEMA
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();d=a.run
qs={q['id']:q for q in read(d/'questions.jsonl')};packs={q['question_id']:q for q in read(d/'evidence.jsonl')};answers=read(d/'answers.jsonl');checks=[]
for row in answers:
 pack=packs[row['question_id']]
 if row['evidence_sha256']!=digest(pack['results']):raise ValueError('Evidence integrity failure')
 c=check_answer(qs[row['question_id']],pack,row['answer'],row['status'],KNOWLEDGE_AGENT_SCHEMA['schema']);c['repeat']=row['repeat'];checks.append(c)
write(d/'checks.jsonl',checks)
(d/'checker-config.json').write_text(json.dumps({'checker_sha256':digest((ROOT/'scripts/answer_eval.py').read_bytes()),'rescore_script_sha256':digest(Path(__file__).read_bytes()),'schema_sha256':digest(KNOWLEDGE_AGENT_SCHEMA),'answers_sha256':digest((d/'answers.jsonl').read_bytes()),'note':'Offline recheck only; original generation config is unchanged.'},indent=2),encoding='utf8')
valid=[c for c in checks if c['valid_generation']];cit=[x for c in valid for x in c['citations']];quotes=[x for x in cit if x['quote_provided']]
def ratio(a,b):return f'{a}/{b} ({a/b:.1%})' if b else 'N/A (0 applicable)'
metrics=[('有效生成/全部尝试',len(valid),len(answers)),('Schema合法/有效生成',sum(c['schema_ok'] for c in valid),len(valid)),('输入绑定引用/全部引用',sum(c['from_input'] for c in cit),len(cit)),('定位匹配/全部引用',sum(c['locator_ok'] for c in cit),len(cit)),('摘录提供/全部引用',len(quotes),len(cit)),('摘录匹配/已提供摘录',sum(c['quote_matches'] is True for c in quotes),len(quotes)),('硬检查通过/全部尝试',sum(c.get('hard_pass',False) for c in checks),len(checks))]
lines=['# 首轮生成层评测报告','','真实模型；冻结证据重放，不重新检索；留出集未运行。语义质量待真实人工评分。','','| 指标 | 结果 |','|---|---|']
lines.extend(f'| {k} | {ratio(x,y)} |' for k,x,y in metrics)
lines+=['',f"运行状态：{dict(Counter(x['status'] for x in answers))}", '','## 证据条件分组','']
for label,flag in [('必要gold证据完整',True),('必要gold证据缺失',False),('无gold证据要求（行为题）',None)]:
 subset=[c for c in checks if packs[c['question_id']]['gold_evidence_complete'] is flag];lines.append(f"- {label}：{len(subset)}次；硬检查通过{sum(c.get('hard_pass',False) for c in subset)}次。语义判断不可直接横向混合。")
lat=sorted(r['generation_seconds'] for r in answers);lines+=['',f'生成P95：{lat[math.ceil(.95*len(lat))-1] if lat else None}秒（含失败尝试，不含检索）。','', '## 逐题硬检查失败项','','| ID | 失败项 |','|---|---|']
for c in checks:
 reasons=[]
 if not c['valid_generation']:reasons.append('运行失败/mock')
 if not c['schema_ok']:reasons.append('Schema')
 if any(not x['from_input'] for x in c['citations']):reasons.append('引用不在输入/证据ID缺失')
 if any(not x['locator_ok'] for x in c['citations']):reasons.append('条款/页码/章节不匹配')
 if any(x['quote_matches'] is False for x in c['citations']):reasons.append('摘录不是对应chunk原文子串')
 if qs[c['question_id']]['question_type']=='clarification' and not c['clarification_present']:reasons.append('无实质追问字段')
 if c['gold_document_cited'] is False:reasons.append('未引用gold文档（需结合证据完整性解释）')
 if not c['verdict_matches']:reasons.append('verdict与基准不一致（需语义复核）')
 lines.append(f"| {c['question_id']} | {'；'.join(reasons) or '无硬错误；语义仍待评分'} |")
lines+=['','## 人工校准待办','','human_review.jsonl含15题未填写评分。请按 ../../answer/README.md 的rubric填写；未使用模型冒充人工。未接judge，未报告正确性/忠实度/拒答正确率，也未宣称零编造。','', '题集gold仅经agent核对，仍需人工确认。']
configs = {json.dumps(pack.get('retrieval_config', {}), ensure_ascii=False, sort_keys=True) for pack in packs.values()}
lines.extend(['', '冻结证据的检索配置：'] + [f'- {config}' for config in sorted(configs)])
(d/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf8');print('\n'.join(lines[:18]))
