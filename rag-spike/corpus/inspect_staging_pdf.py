from pathlib import Path
import pypdfium2 as pdfium
root=Path('rag-spike/corpus/staging/id-shopee-toys-20261102/government')
for k in ['sni-55-2013','sni-111-2015','import-37-2025','import-18-2026']:
 d=pdfium.PdfDocument(root/(k+'.pdf')); d[0].render(scale=1.2).to_pil().save(root/(k+'-page1.png'))
