"""Meaningful boundary tests; no model/network calls."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
from answer_eval import check_answer,digest,gold_match,ROOT,read
sys.path.insert(0,str(ROOT.parent/'backend'))
from agents.knowledge_agent import KnowledgeAgent
from schemas.agent_schemas import KNOWLEDGE_AGENT_SCHEMA

class AnswerEvalTests(unittest.TestCase):
 def setUp(self):
  self.q={'id':'test','question_type':'answerable','gold_doc_ids':['d'],'expected_verdict':'谨慎','must_not_say':['所有玩具都需要SNI']}
  self.pack={'results':[{'evidence_id':'E1','doc_id':'d','content':'Original text.','page':2,'clause_id':'3'}],'gold_evidence_complete':True}
  self.a={'verdict':'谨慎','summary':'Supported','evidence':[{'evidence_id':'E1','doc_id':'d','claim':'Supported','quote':'Original text.','page':2,'clause_id':'3'}],'unknowns':[],'follow_up_questions':[],'compliance_checklist':[]}
 def check(self):return check_answer(self.q,self.pack,self.a,'generated',KNOWLEDGE_AGENT_SCHEMA['schema'])
 def test_valid_input_bound_citation(self):self.assertTrue(self.check()['hard_pass'])
 def test_index_document_not_in_input(self):
  self.a['evidence'][0]['evidence_id']='E99';self.assertFalse(self.check()['hard_pass'])
 def test_wrong_doc_same_evidence(self):
  self.a['evidence'][0]['doc_id']='another';self.assertFalse(self.check()['hard_pass'])
 def test_invented_quote(self):
  self.a['evidence'][0]['quote']='invented';self.assertFalse(self.check()['hard_pass'])
 def test_whitespace_only_normalization(self):
  self.a['evidence'][0]['quote']='Original\n text.';self.assertTrue(self.check()['hard_pass'])
 def test_wrong_locator(self):
  self.a['evidence'][0]['page']=99;self.assertFalse(self.check()['hard_pass'])
 def test_negated_forbidden_phrase_is_warning(self):
  self.a['summary']='不能断言所有玩具都需要SNI';c=self.check();self.assertTrue(c['hard_pass']);self.assertTrue(c['warnings'])
 def test_absent_quote_not_counted_as_match(self):
  del self.a['evidence'][0]['quote'];c=self.check()['citations'][0];self.assertFalse(c['quote_provided']);self.assertIsNone(c['quote_matches'])
 def test_mock_never_passes(self):
  c=check_answer(self.q,self.pack,self.a,'mock',KNOWLEDGE_AGENT_SCHEMA['schema']);self.assertFalse(c['hard_pass'])
 def test_schema_error(self):
  self.a['verdict']='yes';self.assertFalse(self.check()['schema_ok'])
 def test_gold_requirements_conjunctive(self):
  self.assertFalse(gold_match(self.pack['results'][0],{'doc_id':'d','page':99,'must_contain_any':['Original']}))
 def test_hash_detects_order_change(self):self.assertNotEqual(digest([1,2]),digest([2,1]))
 def test_splits_no_case_leak(self):
  qs=read(ROOT/'eval/questions.answer-eval.jsonl');groups={}
  for q in qs:groups.setdefault(q['case_group'],set()).add(q['split'])
  self.assertTrue(all(len(s)==1 for s in groups.values()));self.assertEqual(len(qs),32)
 def test_replay_never_retrieves_and_empty_context_can_clarify(self):
  a=KnowledgeAgent();a.use_mock=False
  with patch.object(KnowledgeAgent,'retrieve',side_effect=AssertionError('retrieved')),patch('agents.base_agent.BaseAgent.run',return_value=self.a) as run:
   result,meta=a.answer_from_evidence('Which product?',[],{'country':'id'})
   self.assertEqual(meta['generation_status'],'generated');self.assertIn('country',run.call_args.args[0])
 def test_failure_explicitly_marked(self):
  a=KnowledgeAgent();a.use_mock=False
  with patch('agents.base_agent.BaseAgent.run',side_effect=TimeoutError('test')):
   result,meta=a.answer_from_evidence('question',self.pack['results']);self.assertTrue(meta['mock']);self.assertEqual(meta['generation_status'],'generation_failed')
if __name__=='__main__':unittest.main()
