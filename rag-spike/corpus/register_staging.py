from pathlib import Path
from pypdf import PdfReader
import json,hashlib
base=Path('rag-spike/corpus/staging/id-shopee-toys-20261102');g=base/'government'
old=json.loads((g/'metadata.json').read_text(encoding='utf8'));alt=json.loads((g/'alternate-downloads.json').read_text(encoding='utf8'));by={x['doc_id']:x for x in old}
for x in alt:by[x['doc_id']]=x
records=[]
for p in sorted(g.glob('*.pdf')):
 k=p.stem; m=by[k];ts=[x.extract_text() or '' for x in PdfReader(p).pages];empty=[i+1 for i,t in enumerate(ts) if len(t.strip())<30]
 rec=dict(doc_id=k,title=k,file=str(p.with_suffix('.txt').relative_to(Path('rag-spike/corpus'))).replace('\\','/'),original_file=str(p.relative_to(Path('rag-spike/corpus'))).replace('\\','/'),country='id',platform='any',doc_type='policy',category='toys',language='id',published_at='unknown',effective_from='unknown',effective_to='unknown',collected_at='2026-11-02',review_status='pending',source_url=m['source_url'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pages=len(ts),empty_text_pages=empty,index_eligible=False,notes='待核对修订链、生效日和适用范围；扫描页需OCR；不得据此作当前合规结论。')
 if 'RANCANGAN' in '\n'.join(ts):rec['extraction_warning']='提取文本含RANCANGAN；已渲染首面，首面可见内容无该字样，疑似隐藏文本；仍需核对正式发布及全文。'
 records.append(rec)
pm=json.loads((base/'platform/metadata.json').read_text(encoding='utf8'))
for m in pm['records']:
 records.append(dict(doc_id=m['doc_id'],title=m['doc_id'],file=str((base/'platform'/m['text_file']).relative_to(Path('rag-spike/corpus'))).replace('\\','/'),original_file=str((base/'platform'/m['file']).relative_to(Path('rag-spike/corpus'))).replace('\\','/'),country='id',platform='shopee',doc_type='platform',category='toys',language='id',published_at='unknown',effective_from='unknown',effective_to='unknown',collected_at='2026-11-02',review_status='pending',source_url=m['source_url'],sha256=m['sha256'],last_modified_at=m['last_modified_date'],index_eligible=False,notes='通用政策；不能替代玩具类目专属审核要求。'))
(base/'manifest.pending.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in records)+'\n',encoding='utf8')
rows=['| 文档 | 页数/形式 | 状态 |','|---|---|---|']
for r in records:rows.append(f"| {r['doc_id']} | {r.get('pages','HTML')} | {'需OCR或扫描页补全' if r.get('empty_text_pages') else '已提取，待审核'} |")
report='''# 印尼本地销售 / Shopee / 非电动塑料积木：采集批次

采集日期：2026-11-02。范围：商业进口→印尼本地仓→Shopee本地店；6岁及以上非电动塑料积木。年龄标识不构成自动分类依据。

## 结果
实际保存11份官方来源文件：8份政府PDF、3份Shopee HTML。保留原件、派生文本、来源与SHA256。11份均pending；没有加入主manifest或生产索引。数量达标不等于证据覆盖达标。

'''+ '\n'.join(rows)+'''

## 关键缺口：按用户要求暂停扩大采集
- SNI基础法24/2013及第三次修订29/2018：已定位官方PDF https://peraturan.go.id/files/bn566-2013.pdf 和 https://peraturan.go.id/files/bn1427-2018.pdf ，本地下载连续遇TLS超时，未保存原件。搜索可读不等于已采集全文。不能只靠55/2013和111/2015推导现行要求。
- 海关目录把24/2013与55/2013指向同一PDF；已视觉核对下载件实际上是55/2013，未重复计数。
- 55/2013（6页）和111/2015（9页）为扫描件，首面文号视觉核对通过，尚未OCR全文。16/2025的119页中有7页无足够可提取文本，需检查扫描附件及表格。
- 37/2025与18/2026提取文本含RANCANGAN，但首面渲染未显示该字样。不能仅凭隐藏文本判定为草案，也不能跳过正式发布及签署页核对；已保留异常标记。
- 尚未获得Shopee本地玩具类目专属资质提交规则。通用禁限售原文已取得，不能保证平台后台没有额外要求。
- SNI技术标准全文未获取；本批次只能朝材料/法规预检查发展，不能进行测试参数级合格判定。

## 建议
保留已确认场景，不急于更换国家或类目。先补齐两份SNI法规原件、扫描件OCR和正式版本核验，再决定是否发布语料快照。若无法补齐，首版进一步限定为“法规检索与材料整理”，暂停自动给出SNI适用性或允许销售结论。

## 文件说明
manifest.pending.jsonl 为本批次待审登记，未并入 corpus/manifest.jsonl。government/metadata.json 保留最初下载尝试，government/alternate-downloads.json 记录备用来源，登记表以实际原件及哈希为准。platform/metadata.json 保留平台页面获取与完整性记录。published_at/effective_from未知均显式unknown，未以采集时间代替。
'''
(base/'README.md').write_text(report,encoding='utf8');print('records',len(records),'unique hashes',len({r['sha256'] for r in records})); print('pdf pages',sum(r.get('pages',0) for r in records))
