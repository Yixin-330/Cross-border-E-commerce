import urllib.request,concurrent.futures,json,hashlib
from pathlib import Path
from pypdf import PdfReader
root=Path('rag-spike/corpus/staging/id-shopee-toys-20261102/government')
docs=[('label-25-2021','https://peraturan.bpk.go.id/Download/269197/Permendag%20Nomor%2025%20Tahun%202021%20%281%29.pdf'),('import-37-2025','https://peraturan.bpk.go.id/Download/395126/Permendag%20Nomor%2037%20Tahun%202025.pdf'),('import-18-2026','https://peraturan.bpk.go.id/Download/415349/permendag-no-18-tahun-2026.pdf'),('ecommerce-19-2026','https://peraturan.bpk.go.id/Download/415514/permendag-no-19-tahun-2026.pdf'),('sni-111-2015','https://kualanamu.beacukai.go.id/upload/7421_permenperin_no.pdf')]
def fetch(item):
 k,u=item;m=dict(doc_id=k,source_url=u,collected_at='2026-11-02',review_status='pending')
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:b=r.read()
  if not b.startswith(b'%PDF'):raise ValueError('not PDF')
  (root/(k+'.pdf')).write_bytes(b);m.update(status='downloaded',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
 except Exception as e:m.update(status='failed',error=str(e))
 return m
with concurrent.futures.ThreadPoolExecutor(5) as ex:r=list(ex.map(fetch,docs))
(root/'alternate-downloads.json').write_text(json.dumps(r,indent=2),encoding='utf8')
for m in r:print(m['doc_id'],m['status'],m.get('error',''))
for p in root.glob('*.pdf'):
 reader=PdfReader(p);ts=[x.extract_text() or '' for x in reader.pages];p.with_suffix('.txt').write_text('\n\n'.join(f'[[PAGE {i+1}]]\n{t}' for i,t in enumerate(ts)),encoding='utf8');print(p.stem,len(ts),'empty',sum(len(t.strip())<30 for t in ts))
