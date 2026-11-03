"""Frozen-evidence answer evaluation. No gold/rubric is sent to the generator."""
import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'backend'))

def digest(value):
    b=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,sort_keys=True).encode('utf8')
    return hashlib.sha256(b).hexdigest()
def read(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf8').splitlines() if x.strip()]
def write(path,rows):
    Path(path).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf8')
def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s or ''))
def gold_match(r,g):
    if g['doc_id'] not in {r.get('doc_id'),r.get('citation_doc_id')}:return False
    # Locators and content requirements are conjunctive, unlike legacy retrieval metrics.
    if g.get('clause_id') and norm(g['clause_id']).lower()!=norm(r.get('clause_id','')).lower():return False
    if g.get('page') and g['page']!=r.get('page'):return False
    text=norm(r.get('content','')).lower()
    if g.get('must_contain_any') and not any(norm(k).lower() in text for k in g['must_contain_any']):return False
    if g.get('must_contain_all') and not all(norm(k).lower() in text for k in g['must_contain_all']):return False
    return True

def freeze(args):
    from retrieval import load_index,bm25_search
    from query_expansion import expand_query
    qs=read(args.questions);index=load_index();before=digest((ROOT/'index/index.json').read_bytes());packs=[]
    for q in qs:
        query,terms=expand_query(q['question'])
        rs=bm25_search(index,query,top_k=args.top,country=q.get('country') or None,platform=q.get('platform') or None)
        for i,r in enumerate(rs,1):r['evidence_id']=f'E{i}'
        matched=[any(gold_match(r,g) for r in rs) for g in q.get('gold_evidence',[])]
        pack={'question_id':q['id'],'question_hash':digest(q),'index_snapshot':index.get('snapshot_id'),'index_sha256':before,'results':rs,'expanded_terms':terms,'gold_evidence_matches':matched,'gold_evidence_complete':all(matched) if matched else None,'retrieval_config':{'mode':'bm25','expand':True,'rerank':False,'top_k':args.top}}
        pack['evidence_sha256']=digest(rs);packs.append(pack)
    if before!=digest((ROOT/'index/index.json').read_bytes()):raise RuntimeError('Index changed while freezing')
    args.output.parent.mkdir(parents=True,exist_ok=True);write(args.output,packs)
    (args.output.parent/'freeze-config.json').write_text(json.dumps({'questions_sha256':digest(args.questions.read_bytes()),'index_sha256':before,'snapshot':index.get('snapshot_id'),'retrieval':'bm25 + zh expansion, no rerank','note':'Embedding venv launcher unavailable; explicit baseline, not auto/rerank','source_hashes':{p.name:digest(p.read_bytes()) for p in [Path(__file__),ROOT/'scripts/retrieval.py',ROOT/'scripts/query_expansion.py']}},ensure_ascii=False,indent=2),encoding='utf8')
    print('Frozen',len(packs),'complete gold evidence',sum(p['gold_evidence_complete'] is True for p in packs))

def check_answer(q,pack,answer,status,schema):
    from jsonschema import Draft202012Validator
    errors=list(Draft202012Validator(schema).iter_errors(answer))
    out={'question_id':q['id'],'runtime_status':status,'valid_generation':status=='generated','schema_ok':not errors,'schema_errors':[e.message for e in errors],'citations':[],'warnings':[],'semantic_review_required':True}
    if not isinstance(answer,dict):return out
    evidence=answer.get('evidence',[])
    if not isinstance(evidence,list):return out
    inputs={r['evidence_id']:r for r in pack['results']}
    gold=set(q.get('gold_doc_ids',[]));cited=set()
    for c in evidence:
        if not isinstance(c,dict):continue
        r=inputs.get(c.get('evidence_id'));doc=c.get('doc_id');cited.add(doc)
        doc_ok=r is not None and doc==(r.get('citation_doc_id') or r.get('doc_id'))
        quote=c.get('quote');quote_present=isinstance(quote,str) and bool(quote.strip())
        loc_ok=doc_ok and all(not c.get(k) or c[k]==r.get(k) for k in ['clause_id','page','section_path'])
        out['citations'].append({'evidence_id':c.get('evidence_id'),'doc_id':doc,'from_input':doc_ok,'locator_ok':loc_ok,'quote_provided':quote_present,'quote_matches':norm(quote) in norm(r['content']) if quote_present and r else None})
    out['gold_document_cited']=bool(cited&gold) if gold else None
    out['verdict_matches']=answer.get('verdict')==q.get('expected_verdict')
    follow=answer.get('follow_up_questions',[])
    out['clarification_present']=isinstance(follow,list) and any(isinstance(x,str) and x.strip() for x in follow)
    input_docs={r.get('citation_doc_id') or r.get('doc_id') for r in inputs.values()}
    checklist=answer.get('compliance_checklist',[])
    out['checklist_references_ok']=isinstance(checklist,list) and all(
        isinstance(item,dict) and isinstance(item.get('basis_doc_ids',[]),list)
        and all(doc in input_docs for doc in item.get('basis_doc_ids',[])) for item in checklist)
    text=json.dumps(answer,ensure_ascii=False)
    out['warnings']=[{'kind':'must_not_say_lexical_hit','text':s,'requires_semantic_confirmation':True} for s in q.get('must_not_say',[]) if norm(s).lower() in norm(text).lower()]
    out['hard_pass']=out['valid_generation'] and out['schema_ok'] and out['checklist_references_ok'] and all(c['from_input'] and c['locator_ok'] and c['quote_matches'] is not False for c in out['citations'])
    if q['question_type']=='answerable' and pack.get('gold_evidence_complete') is True:out['hard_pass'] &= out['gold_document_cited']
    if q['question_type']=='clarification':out['hard_pass'] &= out['clarification_present']
    # Verdict alone never proves correct refusal; lexical hits never prove hallucination.
    return out

def run(args):
    from dotenv import load_dotenv
    load_dotenv(ROOT.parent/'backend/.env')
    from agents.knowledge_agent import KnowledgeAgent,KNOWLEDGE_SYSTEM_PROMPT
    from schemas.agent_schemas import KNOWLEDGE_AGENT_SCHEMA
    qs=read(args.questions);packs={x['question_id']:x for x in read(args.evidence)}
    selected=[q for q in qs if q['split'] in args.splits.split(',') and q['status']=='ready']
    if any(q['holdout'] for q in selected) and not args.allow_holdout:raise ValueError('Holdout requires explicit --allow-holdout')
    for q in selected:
        p=packs[q['id']]
        if p['question_hash']!=digest(q) or p['evidence_sha256']!=digest(p['results']):raise ValueError('Question/evidence hash mismatch')
    agent=KnowledgeAgent();agent.temperature=0
    if agent.use_mock and not args.mock:raise RuntimeError('Real provider unavailable; refusing to count mock answers')
    if args.mock:agent.use_mock=True
    if args.output.exists():raise ValueError('Run directory already exists; choose a new path')
    args.output.mkdir(parents=True)
    config={'started_at':datetime.now(timezone.utc).isoformat(),'provider':agent.provider,'model':agent.model,'temperature':agent.temperature,'mock_requested':args.mock,'splits':args.splits,'repeats':args.repeats,'questions_sha256':digest(args.questions.read_bytes()),'evidence_file_sha256':digest(args.evidence.read_bytes()),'prompt_sha256':digest(KNOWLEDGE_SYSTEM_PROMPT),'schema_sha256':digest(KNOWLEDGE_AGENT_SCHEMA),'source_hashes':{str(p.relative_to(ROOT.parent)):digest(p.read_bytes()) for p in [Path(__file__),ROOT.parent/'backend/agents/knowledge_agent.py',ROOT.parent/'backend/agents/base_agent.py']},'semantic_scoring':'pending human; no judge implemented'}
    (args.output/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf8')
    write(args.output/'questions.jsonl',selected);write(args.output/'evidence.jsonl',[packs[q['id']] for q in selected])
    answers=[];checks=[];humans=[]
    for q in selected:
      for repeat in range(args.repeats):
        started=time.monotonic()
        try:a,m=agent.answer_from_evidence(q['question'],packs[q['id']]['results'],context=q['context']);status=m['generation_status']
        except Exception as exc:a=None;m={'error_type':type(exc).__name__};status='generation_failed'
        rec={'question_id':q['id'],'repeat':repeat,'answer':a,'meta':m,'status':status,'generation_seconds':round(time.monotonic()-started,3),'evidence_sha256':packs[q['id']]['evidence_sha256']};answers.append(rec)
        c=check_answer(q,packs[q['id']],a,status,KNOWLEDGE_AGENT_SCHEMA['schema']);c['repeat']=repeat;checks.append(c)
        # Save after every request; interruptions do not erase completed answers.
        write(args.output/'answers.jsonl',answers);write(args.output/'checks.jsonl',checks)
        print(q['id'],status,'hard_pass',c.get('hard_pass',False),flush=True)
    # Deterministic calibration sample: cover every behavior then fill to 15.
    unique={q['id']:q for q in selected};sample=[]
    for typ in ['answerable','clarification','uncovered']:
        sample.extend([q for q in selected if q['question_type']==typ][:4])
    sample_ids={q['id'] for q in sample}
    sample.extend([q for q in selected if q['id'] not in sample_ids][:max(0,15-len(sample))])
    for q in sample:
        humans.append({'question_id':q['id'],'repeat':0,'review_status':'pending','reviewer':None,'reviewed_at':None,'correctness':None,'completeness':None,'faithfulness':None,'citation_support':None,'behavior_ok':None,'unsupported_claims':[],'missing_points':[],'reason':None})
    write(args.output/'human_review.jsonl',humans)
    valid=[c for c in checks if c['valid_generation']];cit=[x for c in valid for x in c['citations']];quotes=[c for c in cit if c['quote_provided']]
    def ratio(a,b):return f'{a}/{b}' if b else 'N/A (0 applicable)'
    lat=sorted(a['generation_seconds'] for a in answers);p95=lat[max(0,__import__('math').ceil(.95*len(lat))-1)] if lat else None
    report=f'''# Answer evaluation run\n\nGeneration-only replay; no live retrieval. Holdout excluded unless explicitly requested.\n\n- Attempts: {len(answers)}\n- Runtime states: {dict(Counter(a['status'] for a in answers))}\n- Valid generation / all attempts: {ratio(len(valid),len(answers))}\n- Schema / valid generations: {ratio(sum(c['schema_ok'] for c in valid),len(valid))}\n- Input-bound citations: {ratio(sum(c['from_input'] for c in cit),len(cit))}\n- Citation locator matches: {ratio(sum(c['locator_ok'] for c in cit),len(cit))}\n- Quote provision / citations: {ratio(len(quotes),len(cit))}\n- Quote matching / provided: {ratio(sum(c['quote_matches'] is True for c in quotes),len(quotes))}\n- Generation P95 seconds (includes failed attempts): {p95}\n- Human calibration rows pending: {len(humans)}\n\nNo correctness, faithfulness, hallucination-free or refusal-success claims are made by deterministic checks. Evidence completeness is reported separately in evidence.jsonl. No human scores have been fabricated.\n'''
    (args.output/'report.md').write_text(report,encoding='utf8')
    print('Saved',args.output)

def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
 for name in ['freeze','run']:
  s=sub.add_parser(name);s.add_argument('--questions',type=Path,default=ROOT/'eval/questions.answer-eval.jsonl');s.add_argument('--output',type=Path,required=True)
  if name=='freeze':s.add_argument('--top',type=int,default=5)
  else:
   s.add_argument('--evidence',type=Path,required=True);s.add_argument('--splits',default='dev,regression');s.add_argument('--repeats',type=int,default=1);s.add_argument('--mock',action='store_true');s.add_argument('--allow-holdout',action='store_true')
 a=p.parse_args()
 if getattr(a,'repeats',1)<1:raise ValueError('repeats must be positive')
 if a.command=='freeze' and a.output.exists():raise ValueError('Refusing to overwrite frozen evidence')
 (freeze if a.command=='freeze' else run)(a)
if __name__=='__main__':main()
