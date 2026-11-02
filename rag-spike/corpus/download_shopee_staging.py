"""Download public policy HTML without authentication or access-control bypass."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request
from html.parser import HTMLParser

OUT = Path(__file__).parent / 'staging/id-shopee-toys-20261102/platform'
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = [
 ('shopee-id-prohibited-restricted', 'https://help.shopee.co.id/portal/4/article/71189-Kebijakan-Barang-yang-dilarang-dan-dibatasi', ['Merupakan tanggung jawab', 'SNI', 'Diubah terakhir']),
 ('shopee-id-terms', 'https://help.shopee.co.id/portal/4/article/71187-Syarat-Layanan', ['PENDAHULUAN', 'PENGECUALIAN DAN BATASAN', 'Terakhir diubah']),
 ('shopee-id-community', 'https://help.shopee.co.id/portal/4/article/73507-Peraturan-Komunitas', ['Peraturan Komunitas']),
]
class TextParser(HTMLParser):
 def __init__(self):
  super().__init__(); self.parts=[]; self.skip=0
 def handle_starttag(self, tag, attrs):
  if tag in ('script','style'): self.skip += 1
 def handle_endtag(self, tag):
  if tag in ('script','style'): self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip and data.strip(): self.parts.append(data.strip())

records=[]
for doc_id,url,markers in SOURCES:
 rec={'doc_id':doc_id,'source_url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'country':'id','platform':'shopee','language':'id','document_type':'platform_policy','review_status':'staging_not_approved','scope':'General Indonesian marketplace policy; not toy-specific approval or import clearance'}
 try:
  with urllib.request.urlopen(url,timeout=30) as response:
   raw=response.read(); rec.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'))
  filename=doc_id+'.html'; (OUT/filename).write_bytes(raw)
  s=raw.decode('utf-8'); parser=TextParser(); parser.feed(s); text='\n'.join(parser.parts)
  (OUT/(doc_id+'.txt')).write_text(text,encoding='utf-8')
  rec.update(file=filename,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),text_file=doc_id+'.txt',text_characters=len(text),body_markers={m:m.lower() in text.lower() for m in markers},acquisition_status='downloaded_public_html')
  rec['completeness_status']='body_present_requires_review' if all(rec['body_markers'].values()) else 'incomplete_or_unverified'
 except Exception as exc:
  rec.update(acquisition_status='failed',error=str(exc))
 records.append(rec)
(OUT/'metadata.json').write_text(json.dumps({'collection_date':'2026-11-02','records':records,'gaps':['No toy-specific Shopee local seller certificate-submission policy obtained. These general policies do not establish SNI applicability, certification validity, importer eligibility, or toy category approval.'],'notes':['Raw HTTP response bytes retained with SHA-256. Extracted text is a convenience derivative, not the canonical original.','No login, private API, or access-control bypass used. No manifest changes.']},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
