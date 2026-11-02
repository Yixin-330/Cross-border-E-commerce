import requests,re,json,concurrent.futures
from pathlib import Path
root=Path('rag-spike/corpus/staging/id-shopee-toys-20261102/government')
pages={'label-25-2021':'https://peraturan.bpk.go.id/Details/166549/permendag-no-25-tahun-2021','import-37-2025':'https://peraturan.bpk.go.id/Details/332972/permendag-no-37-tahun-2025','import-18-2026':'https://peraturan.bpk.go.id/Details/351566/permendag-no-18-tahun-2026','ecommerce-19-2026':'https://peraturan.bpk.go.id/Details/351720/permendag-no-19-tahun-2026'}
def fetch(item):
 k,u=item; m={'doc_id':k,'landing_url':u}
 try:
  t=requests.get(u,timeout=20).text; links=re.findall(r'href=[\"\x27]([^\"\x27]+)',t); links=[x for x in links if '/Download/' in x];m['download_links']=links
  if not links:raise ValueError('no download link')
  link=links[0];link='https://peraturan.bpk.go.id'+link if link.startswith('/') else link
  r=requests.get(link,timeout=25);r.raise_for_status()
  if not r.content.startswith(b'%PDF'):raise ValueError('not PDF')
  (root/(k+'.pdf')).write_bytes(r.content);m.update(status='downloaded',source_url=link,bytes=len(r.content))
 except Exception as e:m.update(status='failed',error=str(e))
 return m
with concurrent.futures.ThreadPoolExecutor(4) as ex:r=list(ex.map(fetch,pages.items()))
(root/'alternate-downloads.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False))
