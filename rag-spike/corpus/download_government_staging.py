import urllib.request, json, hashlib, concurrent.futures, io
from pathlib import Path
from pypdf import PdfReader
root=Path('rag-spike/corpus/staging/id-shopee-toys-20261102/government'); root.mkdir(parents=True,exist_ok=True)
docs=[
('sni-24-2013','https://peraturan.go.id/files/bn566-2013.pdf'),
('sni-55-2013','https://kualanamu.beacukai.go.id/upload/permenperind_no.pdf'),
('sni-111-2015','https://peraturan.go.id/files/bn2009-2015.pdf'),
('sni-29-2018','https://peraturan.go.id/files/bn1427-2018.pdf'),
('label-25-2021','https://jdih.kemendag.go.id/pdf/Regulasi/2021/PERMENDAG%20NOMOR%2025%20TAHUN%202021.pdf'),
('import-23-2025','https://peraturan.bpk.go.id/Download/392412/Permendag%20Nomor%2023%20Tahun%202025%20tentang%20Kebijakan%20dan%20Pengaturan%20Impor%20Barang%20Konsumsi.pdf'),
('import-16-2025','https://peraturan.bpk.go.id/Download/384921/Permendag%20Nomor%2016%20tahun%202025.pdf'),
('import-37-2025','https://jdih.kemendag.go.id/pdf/Regulasi/2025/Permendag%20Nomor%2037%20Tahun%202025%20tentang%20Perubahan%20atas%20Permendag%20Nomor%2016%20Tahun%202025.pdf'),
('import-18-2026','https://jdih.kemendag.go.id/peraturan/download/3357/2'),
('ecommerce-19-2026','https://jdih.kemendag.go.id/pdf/Regulasi/2026/PERMENDAG%2019%20TAHUN%202026.pdf')]
def fetch(item):
 id,url=item; m=dict(doc_id=id,source_url=url,collected_at='2026-11-02',review_status='pending')
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r: b=r.read(); m['final_url']=r.url
  if not b.startswith(b'%PDF'): raise ValueError('Response is not PDF')
  (root/(id+'.pdf')).write_bytes(b); reader=PdfReader(io.BytesIO(b)); texts=[p.extract_text() or '' for p in reader.pages]
  (root/(id+'.txt')).write_text('\n\n'.join(f'[[PAGE {n+1}]]\n{t}' for n,t in enumerate(texts)),encoding='utf-8')
  m.update(status='downloaded',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),pages=len(texts),empty_pages=[n+1 for n,t in enumerate(texts) if len(t.strip())<30],first_page=texts[0][:1200],last_page=texts[-1][-1000:])
 except Exception as e:m.update(status='failed',error=str(e))
 return m
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: results=list(ex.map(fetch,docs))
(root/'metadata.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for m in results:print(m['doc_id'],m['status'],m.get('pages'),m.get('error',''),m.get('first_page','')[:160].replace('\n',' '))
