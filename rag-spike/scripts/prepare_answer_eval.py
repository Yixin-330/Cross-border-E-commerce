"""Build a reviewed answer-eval derivative; never modify retrieval datasets."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines() if x.strip()]
qs=read(ROOT/'eval/questions.id-mvp.jsonl')+read(ROOT/'eval/questions.zh-smoke.jsonl')
# Semantic families are kept together across languages and paraphrases.
zh_family={1:'permit',2:'fee',3:'alcohol',4:'sanctions',5:'dimensions',6:'language',7:'ai',8:'effective',9:'verification',10:'links',11:'fee',12:'import_scope'}
id_family={1:'pmse',2:'ppmse',3:'permit',4:'fee',5:'ai',6:'effective',7:'ls',8:'sanctions',9:'dimensions',10:'verification',11:'language',12:'links',13:'sale_clarify',14:'cert_clarify',15:'label_clarify',16:'sales_clarify',17:'tariff',18:'sni',19:'halal',20:'future'}
# 11/32 reserved; previously exposed source questions are not pristine unseen tests.
holdout={'fee','sanctions','ls','cert_clarify','sni','ai','halal'}
regression={'dimensions','language','label_clarify','tariff','future'}
points={
'pmse':['Perdagangan yang transaksinya dilakukan melalui serangkaian perangkat dan prosedur elektronik.'],
'ppmse':['Pelaku Usaha penyedia sarana komunikasi elektronik untuk transaksi PMSE.'],
'permit':['PPMSE dan PSP yang tidak dikecualikan wajib memiliki Perizinan Berusaha Bidang PMSE.','Pengecualian PSP mengikuti Pasal 4 ayat (3); kewajiban ini tidak otomatis berlaku sama untuk setiap penjual.'],
'fee':['Penerbitan Perizinan Berusaha Bidang PMSE tidak dipungut biaya.','Tidak menyimpulkan seluruh biaya usaha atau sertifikasi gratis.'],
'ai':['Pelaku Usaha boleh menggunakan AI dalam PMSE sesuai peraturan perundang-undangan.'],
'effective':['Pasal 76: mulai berlaku pada tanggal diundangkan.'],
'ls':['Dokumen tertulis hasil verifikasi atau penelusuran teknis oleh surveyor.','Menyatakan kesesuaian barang yang diimpor.'],
'sanctions':['Penghapusan daftar produk.','Pembatasan hak akun.','Penangguhan atau pengakhiran akun.','Tindakan hukum; tidak semua tindakan pasti dijatuhkan sekaligus.'],
'dimensions':['Informasi setiap barang yang dikirim harus akurat, termasuk berat dan/atau dimensi.'],
'verification':['Menyerahkan data yang diminta Shopee dan memastikan kebenaran serta keakuratannya.','Shopee dapat meminta dokumen pendukung atau tambahan.'],
'language':['Informasi halaman produk menggunakan bahasa Indonesia atau bahasa Inggris.','Tidak memperluas aturan halaman produk menjadi izin label kemasan hanya berbahasa Inggris.'],
'links':['Menghubungkan halaman produk ke situs web lain termasuk contoh iklan yang dilarang.'],
'sale_clarify':['Meminta jenis produk dan tujuan pasar/platform yang belum diketahui.','Tidak memastikan boleh dijual sebelum informasi dan bukti cukup.'],
'cert_clarify':['Meminta jenis, bahan, tujuan penggunaan, usia pengguna dan fitur listrik/baterai.','Meminta pasar tujuan jika belum diketahui; tidak menetapkan sertifikasi tanpa dasar.'],
'label_clarify':['Meminta jenis produk dan pasar tujuan.','Menjelaskan indeks belum menyediakan dasar lengkap label fisik; tidak memberi kesimpulan pasti.'],
'sales_clarify':['Meminta pasar/platform dan rentang waktu.','Menjelaskan tidak memiliki data penjualan untuk membuat peringkat.'],
'tariff':['Tidak menetapkan tarif dari korpus ini.','Memerlukan klasifikasi HS, asal barang/perlakuan preferensi dan tanggal yang relevan.'],
'sni':['Tidak menyimpulkan semua mainan plastik wajib atau bebas SNI.','Menjelaskan kekurangan bukti ruang lingkup SNI; meminta karakteristik produk yang relevan.'],
'halal':['Bukti yang tersedia tidak cukup untuk menentukan kewajiban halal mainan.','Tidak menyamakan ketiadaan bukti dengan pembebasan sertifikasi.'],
'future':['Tidak menjamin status hukum pada 1 Januari 2027 dari snapshot 2 November 2026.','Membedakan ketentuan mulai berlaku dengan kemungkinan perubahan atau pencabutan di masa depan.'],
'alcohol':['Minuman beralkohol memerlukan IT dan PI sebelum memasuki Daerah Pabean menurut Pasal 3(1) dan 4(1).'],
'import_scope':['Tidak memperluas persyaratan khusus alkohol menjadi semua barang impor.','Meminta kategori/HS dan jalur impor; korpus yang tersedia belum cukup untuk jawaban menyeluruh.']}
for q in qs:
 n=int(q['id'].split('-')[-1]);lang='zh' if q['id'].startswith('q-zh') else 'id';f=(zh_family if lang=='zh' else id_family)[n]
 q.update(source_question_id=q['id'],case_group=f,language=lang,split='holdout' if f in holdout else 'regression' if f in regression else 'dev',holdout=f in holdout,status='ready',assessment_date='2026-11-02',context={'assessment_date':'2026-11-02'},gold_answer_points=points[f],must_not_say=[],rubric_review_status='agent_reviewed_pending_human',holdout_provenance='source questions previously exposed; not a pristine unseen test')
 q['acceptable_behaviors']=[q['expected_behavior']]
 q['expected_verdict']='谨慎' if q['question_type']=='answerable' else '信息不足'
 q['required_clarifications']=points[f][:1] if q['question_type']=='clarification' else []
 if f in {'tariff','sni','import_scope'}:q['acceptable_behaviors']=['refuse_uncovered','ask_clarification']
 if f=='permit' and lang=='zh':q['question']='印尼 PMSE 法规对 PPMSE 和不属于豁免范围的中介服务提供者（PSP）有什么营业许可要求？'
 if f=='ai' and lang=='zh':q['question']='印尼 PMSE 法规是否允许经营者在经营中使用人工智能？'
 if f=='sanctions':q['gold_answer']='; '.join(points[f]);q['must_not_say']=['所有站点统一处罚','semua sanksi pasti dijatuhkan','固定罚款金额']
 if f=='import_scope':
  q.update(question_type='uncovered',expected_behavior='refuse_uncovered',expected_verdict='信息不足',gold_doc_ids=[],gold_evidence=[])
 if f in {'sni','halal','tariff','import_scope'}:q['gold_answer']='; '.join(points[f])
 if f=='sni':q['must_not_say']=['所有塑料玩具都必须SNI','semua mainan plastik wajib SNI','semua mainan plastik bebas SNI']
 if f=='effective':q['gold_answer']='根据 Pasal 76 自颁布之日起生效；如提供日历日期，需引用输入证据中含该日期的段落。' if lang=='zh' else 'Menurut Pasal 76, mulai berlaku pada tanggal diundangkan; tanggal kalender harus didukung bukti yang diberikan.'
 if f=='alcohol':q['gold_answer']='进口酒精饮料须在进入关境前取得 IT 和 PI；该结论仅限所问商品与条款范围。';q['scope']='out_of_mvp_control';q['gold_evidence']=[{'doc_id':'import-23-2025','clause_id':'Pasal 3 ayat (1)','must_contain_all':['IT','minuman']},{'doc_id':'import-23-2025','clause_id':'Pasal 4 ayat (1)','must_contain_all':['PI','minuman']}]
 if f=='verification':q['notes']+='；23.4交叉引用23.3存在源文歧义，不自行推定法律效果。'
 if f=='permit':q.setdefault('gold_evidence',[]).append({'doc_id':'ecommerce-19-2026','clause_id':'Pasal 4 ayat (3)','must_contain_all':['PSP','dikecualikan']})
 if q.get('country'):q['context']['country']=q['country']
 if q.get('platform'):q['context']['platform']=q['platform']
 q['gold_evidence']=q.get('gold_evidence',[])
(ROOT/'eval/questions.answer-eval.jsonl').write_text('\n'.join(json.dumps(q,ensure_ascii=False) for q in qs)+'\n',encoding='utf8')
print('questions',len(qs),'holdout',sum(q['holdout'] for q in qs))
