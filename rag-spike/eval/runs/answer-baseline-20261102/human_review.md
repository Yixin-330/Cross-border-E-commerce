# 人工校准工作表（未评分）

请依照 [rubric](../../answer/README.md) 填写 human_review.jsonl。本表只整理待审材料，不代表人工评分已完成。

共15题；请同时检查正文证据是否支持，而非只比对标准答案。

## q-mvp-001 — answerable

Apa yang dimaksud dengan Perdagangan Melalui Sistem Elektronik (PMSE)?

必要要点：
- Perdagangan yang transaksinya dilakukan melalui serangkaian perangkat dan prosedur elektronik.

必要gold证据完整：True。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Berdasarkan Permendag No. 19 Tahun 2026, PMSE (Perdagangan Melalui Sistem Elektronik) didefinisikan sebagai perdagangan yang transaksinya dilakukan melalui serangkaian perangkat dan prosedur elektronik. Definisi ini tercantum dalam BAB I Ketentuan Umum. Perlu dicatat bahwa tanggal publikasi dan tanggal berlaku dokumen ini tidak tercantum dalam bukti, sehingga keberlakuannya pada tanggal asesmen (2026-11-02) tidak dapat dipastikan dari bukti yang tersedia.",
  "evidence": [
    {
      "claim": "PMSE adalah perdagangan yang transaksinya dilakukan melalui serangkaian perangkat dan prosedur elektronik.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "BAB I KETENTUAN UMUM",
      "clause_id": "2",
      "page": 3,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Perdagangan Melalui Sistem Elektronik yang selanjutnya disingkat PMSE adalah Perdagangan yang transaksinya dilakukan melalui serangkaian perangkat dan prosedur elektronik.",
      "evidence_id": "E1"
    },
    {
      "claim": "PPMSE adalah pelaku usaha penyedia sarana komunikasi elektronik yang digunakan untuk transaksi perdagangan (konteks terkait definisi PMSE).",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "BAB I KETENTUAN UMUM",
      "clause_id": "10",
      "page": 3,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Penyelenggara Perdagangan Melalui Sistem Elektronik yang selanjutnya disingkat PPMSE adalah Pelaku Usaha penyedia sarana komunikasi elektronik yang digunakan untuk transaksi Perdagangan.",
      "evidence_id": "E3"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Definisi PMSE sesuai Permendag No. 19 Tahun 2026",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Definisi tersedia di BAB I Ketentuan Umum angka 2, halaman 3."
    },
    {
      "item": "Status keberlakuan Permendag No. 19 Tahun 2026 pada tanggal asesmen",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Tanggal publikasi dan tanggal berlaku tidak tercantum dalam bukti."
    }
  ],
  "unknowns": [
    "Tanggal publikasi dan tanggal berlaku (effective_from) Permendag No. 19 Tahun 2026 tidak tercantum dalam bukti.",
    "Ruang lingkup lengkap dan kewajiban PPMSE di luar definisi tidak dirinci dalam bukti yang diberikan.",
    "Referensi silang dalam dokumen tidak disertakan dalam bukti."
  ],
  "follow_up_questions": [
    "Apakah Anda memerlukan rincian kewajiban PPMSE atau aspek lain dari PMSE selain definisinya?"
  ]
}
```

实际输入证据：

### E1 / ecommerce-19-2026 / 2 / PDF 3

2. Perdagangan Melalui Sistem Elektronik yang selanjutnya disingkat PMSE adalah Perdagangan yang transaksinya dilakukan melalui serangkaian perangkat dan prosedur elektronik.

### E2 / shopee-id-terms / 27 / PDF 0

lui Sistem Elektronik (PMSE) atas transaksi barang atau jasa kena pajak dari luar negeri melalui sistem elektronik (“ Pemungut PPN PMSE ”).

### E3 / ecommerce-19-2026 / 10 / PDF 3

10. Penyelenggara Perdagangan Melalui Sistem Elektronik yang selanjutnya disingkat PPMSE adalah Pelaku Usaha penyedia sarana komunikasi elektronik yang digunakan untuk transaksi Perdagangan.

### E4 / ecommerce-19-2026 / 2 / PDF 37

2. Direktur Tertib Niaga, Kementerian Perdagangan; dan 3. Direktur Perdagangan Melalui Sistem Elektronik dan Perdagangan Jasa, Kementerian Perdagangan.

### E5 / ecommerce-19-2026 / 2 / PDF 38

2. Direktur Tertib Niaga, Kementerian Perdagangan; dan 3. Direktur Perdagangan Melalui Sistem Elektronik dan Perdagangan Jasa, Kementerian Perdagangan.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-002 — answerable

Apa yang dimaksud dengan PPMSE?

必要要点：
- Pelaku Usaha penyedia sarana komunikasi elektronik untuk transaksi PMSE.

必要gold证据完整：False。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "信息不足",
  "summary": "Berdasarkan bukti yang tersedia, tidak ditemukan definisi atau kepanjangan resmi dari singkatan PPMSE. Bukti hanya menunjukkan penggunaan istilah PPMSE dalam konteks kewajiban, sanksi, dan kriteria tertentu (misalnya PPMSE luar negeri), tanpa menjelaskan apa yang dimaksud dengan PPMSE itu sendiri.",
  "evidence": [
    {
      "claim": "PPMSE disebut sebagai pihak yang dapat dikenai sanksi administratif berupa daftar hitam dan pemblokiran sementara layanan apabila tidak melaksanakan kewajiban tertentu.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Keempat Sanksi bagi PPMSE Terhadap Pelanggaran Ketentuan",
      "clause_id": "Pasal 62 ayat (5)",
      "page": 30,
      "collected_at": "2026-11-02",
      "quote": "PPMSE yang tetap tidak melaksanakan kewajiban sebagaimana dimaksud dalam Pasal 21, dikenai sanksi administratif berupa dimasukkan dalam daftar hitam dan pemblokiran sementara layanan PPMSE",
      "evidence_id": "E2"
    },
    {
      "claim": "Terdapat ketentuan mengenai kriteria tertentu bagi PPMSE luar negeri, namun definisi PPMSE tidak dijelaskan dalam kutipan ini.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Kesepuluh PMSE Lintas Batas",
      "page": 16,
      "quote": "Kriteria tertentu bagi PPMSE luar negeri sebagaimana dimaksud pada ayat (1) dengan ketentuan:",
      "evidence_id": "E3"
    },
    {
      "claim": "PPMSE dan PSP yang tidak dikecualikan dari kewajiban memiliki Perizinan Berusaha wajib menayangkan informasi kontak layanan pengaduan Konsumen.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Ketiga Layanan Pengaduan Konsumen",
      "clause_id": "Pasal 13",
      "page": 10,
      "evidence_id": "E4"
    },
    {
      "claim": "Penyelesaian sengketa antara Pedagang dengan PPMSE dan/atau PSP diutamakan melalui musyawarah untuk mufakat.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kedua Layanan Pengaduan dan",
      "clause_id": "Pasal 11 ayat (1)",
      "page": 10,
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Definisi resmi dan kepanjangan PPMSE",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Bukti yang tersedia tidak memuat definisi atau kepanjangan PPMSE; perlu merujuk pada ketentuan umum/definisi dalam Permendag No. 19 Tahun 2026 yang tidak disertakan dalam bukti."
    }
  ],
  "unknowns": [
    "Definisi dan kepanjangan resmi PPMSE tidak ditemukan dalam bukti yang diberikan.",
    "Rujukan Pasal 21 dan Pasal 4 ayat (3) yang disebut dalam bukti tidak disertakan isinya.",
    "Tanggal publikasi dan tanggal berlaku Permendag No. 19 Tahun 2026 tidak tercantum (unknown)."
  ],
  "follow_up_questions": [
    "Apakah Anda ingin penjelasan PPMSE dalam konteks kewajiban perizinan, sanksi, atau PMSE lintas batas?",
    "Apakah Anda memiliki teks bagian definisi/ketentuan umum Permendag No. 19 Tahun 2026 untuk dikutip?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-terms / huruf i / PDF 0

enagihan atau alamat pengiriman, dan membagikan informasi tersebut dengan ShopeePay, untuk dicerminkan dalam aplikasi atau situs web ShopeePay. Shopee berhak mengubah, menangguhkan, membatalkan dan/atau menetapkan ketentuan apa pun, termasuk namun tidak terbatas pada menetapkan jumlah pembelanjaan minimum, untuk metode pembayaran apa pun. iii. Akun Anda tertaut dengan Akun ShopeePay Anda, Metode P

### E2 / ecommerce-19-2026 / Pasal 62 ayat (5) / PDF 30

(5) Apabila dalam jangka waktu sebagaimana dimaksud pada ayat (4) PPMSE yang tetap tidak melaksanakan kewajiban sebagaimana dimaksud dalam Pasal 21, dikenai sanksi administratif berupa dimasukkan dalam daftar hitam dan pemblokiran sementara layanan PPMSE oleh instansi terkait yang berwenang.

### E3 / ecommerce-19-2026 / p193 / PDF 16

-16- (2) Kriteria tertentu bagi PPMSE luar negeri sebagaimana dimaksud pada ayat (1) dengan ketentuan:

### E4 / ecommerce-19-2026 / Pasal 13 / PDF 10

Pasal 13 Selain layanan pengaduan Konsumen sebagaimana dimaksud dalam Pasal 12, PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal 4 ayat (3) wajib menayangkan informasi kontak layanan pengaduan Konsumen Direktorat Jenderal Perlindungan Konsumen dan Tertib Niaga yang ditampilkan dengan jelas pada laman yang mudah dibaca oleh

### E5 / ecommerce-19-2026 / Pasal 11 ayat (1) / PDF 10

(1) Penyelesaian sengketa antara Pedagang dengan PPMSE dan/atau PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal  4 ayat (3)  diutamakan melalui mekanisme musyawarah untuk mufakat.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-003 — answerable

Apa kewajiban PPMSE dan PSP terkait Perizinan Berusaha Bidang PMSE?

必要要点：
- PPMSE dan PSP yang tidak dikecualikan wajib memiliki Perizinan Berusaha Bidang PMSE.
- Pengecualian PSP mengikuti Pasal 4 ayat (3); kewajiban ini tidak otomatis berlaku sama untuk setiap penjual.

必要gold证据完整：False。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Berdasarkan Permendag No. 19 Tahun 2026, PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha wajib memiliki Perizinan Berusaha Bidang PMSE (Pasal 7 ayat (1)). Permohonan diajukan kepada Menteri melalui Lembaga OSS (Pasal 8 ayat (1)), dan izin tersebut berlaku selama PPMSE/PSP menjalankan kegiatan usaha (Pasal 8 ayat (4)). Pedagang dalam negeri yang memiliki sarana PMSE sendiri juga termasuk kategori PPMSE dan wajib memiliki izin tersebut (Pasal 7 ayat (3)). Izin yang telah dimiliki ditampilkan pada laman khusus situs web Kementerian Perdagangan (Pasal 20 ayat (1)).",
  "evidence": [
    {
      "claim": "PPMSE dan PSP yang tidak dikecualikan wajib memiliki Perizinan Berusaha Bidang PMSE.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 7 ayat (1)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal 4 ayat (3) wajib memiliki Perizinan Berusaha Bidang PMSE.",
      "evidence_id": "E1"
    },
    {
      "claim": "Permohonan Perizinan Berusaha Bidang PMSE diajukan kepada Menteri melalui Lembaga OSS.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 8 ayat (1)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Untuk memperoleh Perizinan Berusaha Bidang PMSE, PPMSE dan PSP yang tidak dikecualikan ... mengajukan permohonan kepada Menteri melalui Lembaga OSS.",
      "evidence_id": "E2"
    },
    {
      "claim": "Perizinan Berusaha Bidang PMSE berlaku selama PPMSE dan PSP menjalankan kegiatan usaha dan/atau kegiatannya.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 8 ayat (4)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Perizinan Berusaha Bidang PMSE berlaku selama PPMSE dan PSP yang tidak dikecualikan sebagaimana dimaksud pada ayat (1) menjalankan kegiatan usaha dan/atau kegiatannya.",
      "evidence_id": "E3"
    },
    {
      "claim": "PPMSE dan/atau PSP yang telah memiliki Perizinan Berusaha Bidang PMSE ditampilkan pada laman khusus situs web Kementerian Perdagangan.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Kedelapan Publikasi Status Perizinan",
      "clause_id": "Pasal 20 ayat (1)",
      "page": 15,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "PPMSE dan/atau PSP ... yang telah memiliki Perizinan Berusaha Bidang PMSE ditampilkan dalam laman khusus pada situs web Kementerian Perdagangan.",
      "evidence_id": "E4"
    },
    {
      "claim": "Pedagang dalam negeri yang memiliki sarana PMSE sendiri termasuk kategori PPMSE dan wajib memiliki Perizinan Berusaha Bidang PMSE.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 7 ayat (3)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pedagang dalam negeri yang memiliki sarana PMSE sendiri termasuk dalam kategori PPMSE dan wajib memiliki Perizinan Berusaha Bidang PMSE sebagaimana dimaksud pada ayat (1).",
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Memiliki Perizinan Berusaha Bidang PMSE bagi PPMSE/PSP yang tidak dikecualikan",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 7 ayat (1)"
    },
    {
      "item": "Mengajukan permohonan izin kepada Menteri melalui Lembaga OSS",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 8 ayat (1)"
    },
    {
      "item": "Memastikan masa berlaku izin sesuai selama menjalankan kegiatan usaha",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 8 ayat (4)"
    },
    {
      "item": "Pedagang dalam negeri dengan sarana PMSE sendiri mendaftar sebagai PPMSE dan memiliki izin",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 7 ayat (3)"
    },
    {
      "item": "Kriteria PPMSE/PSP yang dikecualikan dari kewajiban Perizinan Berusaha",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 4 ayat (3) dirujuk tetapi isinya tidak disediakan dalam evidence"
    }
  ],
  "unknowns": [
    "Isi Pasal 4 ayat (3) mengenai PPMSE/PSP yang dikecualikan dari kewajiban memiliki Perizinan Berusaha tidak tersedia dalam evidence.",
    "Tanggal pengundangan dan tanggal mulai berlaku Permendag No. 19 Tahun 2026 tidak tercantum (unknown).",
    "Persyaratan dokumen dan prosedur rinci permohonan melalui OSS di luar Pasal 8 ayat (1) dan (4) tidak tersedia.",
    "Ketentuan sanksi atas ketidakpatuhan tidak tercakup dalam evidence."
  ],
  "follow_up_questions": [
    "Apakah Anda beroperasi sebagai PPMSE (marketplace) atau PSP (penyedia jasa pembayaran), dan apakah termasuk pihak yang dikecualikan menurut Pasal 4 ayat (3)?"
  ]
}
```

实际输入证据：

### E1 / ecommerce-19-2026 / Pasal 7 ayat (1) / PDF 9

(1) PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal  4 ayat (3) wajib memiliki Perizinan Berusaha Bidang PMSE.

### E2 / ecommerce-19-2026 / Pasal 8 ayat (1) / PDF 9

(1) Untuk memperoleh Perizinan Berusaha Bidang PMSE, PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal 7 mengajukan permohonan kepada Menteri melalui Lembaga OSS.

### E3 / ecommerce-19-2026 / Pasal 8 ayat (4) / PDF 9

(4) Perizinan Berusaha Bidang PMSE berlaku selama PPMSE dan PSP yang tidak dikecualikan sebagaimana dimaksud pada ayat (1) menjalankan kegiatan usaha dan/atau kegiatannya.

### E4 / ecommerce-19-2026 / Pasal 20 ayat (1) / PDF 15

(1) PPMSE dan/atau PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal 4 ayat (3) yang telah memiliki Perizinan Berusaha Bidang PMSE ditampilkan dalam laman khusus pada situs web Kementerian Perdagangan.

### E5 / ecommerce-19-2026 / Pasal 7 ayat (3) / PDF 9

(3) Pedagang dalam negeri yang memiliki sarana PMSE sendiri termasuk dalam kategori PPMSE dan wajib memiliki Perizinan Berusaha Bidang PMSE sebagaimana dimaksud pada ayat (1).

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-006 — answerable

Kapan Permendag Nomor 19 Tahun 2026 mulai berlaku menurut ketentuan penutupnya?

必要要点：
- Pasal 76: mulai berlaku pada tanggal diundangkan.

必要gold证据完整：True。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Menurut ketentuan penutup Permendag No. 19 Tahun 2026, Pasal 76 menyatakan bahwa Peraturan Menteri ini mulai berlaku pada tanggal diundangkan (pada tanggal pengundangannya). Namun, tanggal pengundangan itu sendiri tidak tercantum dalam bukti yang tersedia, sehingga tanggal berlaku konkretnya belum dapat dipastikan.",
  "evidence": [
    {
      "claim": "Permendag No. 19 Tahun 2026 mulai berlaku pada tanggal diundangkan.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "BAB X KETENTUAN PENUTUP",
      "clause_id": "Pasal 76",
      "page": 35,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pasal 76 Peraturan Menteri ini mulai berlaku pada tanggal diundangkan.",
      "evidence_id": "E5"
    },
    {
      "claim": "Pada saat mulai berlaku, Permendag No. 19 Tahun 2026 mencabut Permendag No. 31 Tahun 2023.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "BAB X KETENTUAN PENUTUP",
      "clause_id": "Pasal 75",
      "page": 35,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pasal 75 Pada saat Peraturan Menteri ini mulai berlaku, Peraturan Menteri Perdagangan Nomor 31 Tahun 2023 ... dicabut dan dinyatakan tidak berlaku.",
      "evidence_id": "E2"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Konfirmasi tanggal pengundangan Permendag No. 19 Tahun 2026 untuk menentukan tanggal berlaku efektif",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 76 mengikat keberlakuan pada tanggal diundangkan, tetapi tanggal tersebut tidak tercantum dalam bukti."
    }
  ],
  "unknowns": [
    "Tanggal pengundangan (diundangkan) Permendag No. 19 Tahun 2026 tidak tercantum dalam bukti, sehingga tanggal berlaku efektif belum dapat dipastikan.",
    "Tanggal penetapan/pengundangan pada halaman Berita Negara (E1) tidak terbaca dalam bukti."
  ],
  "follow_up_questions": []
}
```

实际输入证据：

### E1 / ecommerce-19-2026 / p458 / PDF 36

BERITA NEGARA REPUBLIK INDONESIA TAHUN 2026 NOMOR         Ж

### E2 / ecommerce-19-2026 / Pasal 75 / PDF 35

Pasal 75 Pada saat Peraturan Menteri ini mulai berlaku, Peraturan Menteri Perdagangan Nomor 31 Tahun 2023 tentang Perizinan Berusaha, Periklanan, Pembinaan, dan Pengawasan Pelaku Usaha dalam Perdagangan melalui Sistem Elektronik (Berita Negara Republik Indonesia Tahun 2023 Nomor 763), dicabut dan dinyatakan tidak berlaku.

### E3 / ecommerce-19-2026 / p459 / PDF 37

LAMPIRAN PERATURAN MENTERI PERDAGANGAN REPUBLIK INDONESIA NOMOR 19 TAHUN 2026xx TENTANG PENYELENGGARAAN USAHA PERDAGANGAN MELALUI SISTEM ELEKTRONIK

### E4 / import-23-2025 / Pasal 22 / PDF 14

Pasal 22 Pada saat Peraturan Menteri ini mulai berlaku:

### E5 / ecommerce-19-2026 / Pasal 76 / PDF 35

Pasal 76 Peraturan Menteri ini mulai berlaku pada tanggal diundangkan.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-013 — clarification

Apakah produk ini boleh dijual?

必要要点：
- Meminta jenis produk dan tujuan pasar/platform yang belum diketahui.
- Tidak memastikan boleh dijual sebelum informasi dan bukti cukup.

必要gold证据完整：None。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "信息不足",
  "summary": "Tidak dapat dipastikan apakah produk ini boleh dijual, karena pertanyaan tidak menyebutkan jenis produk, merek, atau kategorinya. Bukti yang tersedia hanya memuat aturan umum Shopee Indonesia tentang barang yang dilarang/dibatasi serta aturan halaman produk (satu jenis benda dan satu merek per halaman, kecuali bundling), sehingga belum bisa dinilai untuk produk tertentu.",
  "evidence": [
    {
      "claim": "Shopee Indonesia menyediakan pedoman barang yang dilarang dan dibatasi yang tidak boleh dijual di Shopee, dan pedoman ini diperbarui dari waktu ke waktu.",
      "doc_id": "shopee-id-prohibited-restricted",
      "source_title": "Shopee Indonesia - Kebijakan Barang yang Dilarang dan Dibatasi",
      "section_path": "",
      "clause_id": "p0",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Shopee telah menyediakan pedoman singkat tentang barang yang dilarang dan dibatasi yang tidak boleh dijual di Shopee.",
      "evidence_id": "E2"
    },
    {
      "claim": "Setiap halaman produk hanya boleh digunakan untuk menjual satu jenis benda dan satu merek, kecuali produk yang dijual memang berupa paket (bundling).",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "2",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Setiap halaman produk hanya dapat digunakan untuk menjual satu jenis benda dan satu merk saja, kecuali jika produk yang dijual memang merupakan produk yang dijual secara paketan(bundling).",
      "evidence_id": "E1"
    },
    {
      "claim": "Foto, nama, dan deskripsi produk harus sesuai dan benar-benar menampilkan produk yang ingin dijual.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "2",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pastikan agar Foto, Nama dan Deskripsi Produk anda sesuai dan benar benar menampilkan produk yang ingin dijual.",
      "evidence_id": "E4"
    },
    {
      "claim": "Halaman produk lama yang sudah memiliki penilaian dilarang digunakan untuk menjual produk yang berbeda.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "6",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Halaman produk yang sudah memiliki penilaian dilarang keras digunakan untuk menjual produk yang berbeda.",
      "evidence_id": "E3"
    },
    {
      "claim": "Memanipulasi harga, misalnya mendaftarkan produk dengan harga sangat rendah bukan untuk dijual/dibeli, merupakan pelanggaran dan dapat menyebabkan produk diblokir otomatis.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "7",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Memanipulasi harga adalah sebuah pelanggaran dalam peraturan Shopee ... Hal ini dapat menyebabkan produk Anda diblokir secara otomatis oleh sistem kami.",
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Produk bukan termasuk barang yang dilarang atau dibatasi Shopee Indonesia",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-prohibited-restricted"
      ],
      "note": "Daftar rincian barang terlarang/dibatasi tidak disertakan dalam bukti; perlu dicek pada halaman kebijakan terkini."
    },
    {
      "item": "Satu halaman produk hanya untuk satu jenis benda dan satu merek (kecuali bundling)",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Bergantung pada jenis produk dan merek yang belum disebutkan."
    },
    {
      "item": "Foto, nama, dan deskripsi produk sesuai dengan produk yang dijual",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Belum ada data produk untuk diverifikasi."
    },
    {
      "item": "Tidak menggunakan halaman produk lama berpenilaian untuk produk berbeda",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Bergantung pada cara penjual mengunggah produk."
    },
    {
      "item": "Tidak melakukan manipulasi harga",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Bergantung pada penetapan harga yang akan digunakan."
    }
  ],
  "unknowns": [
    "Jenis produk, merek, dan kategori produk tidak disebutkan sehingga tidak bisa dicocokkan dengan daftar barang terlarang/dibatasi.",
    "Rincian daftar barang yang dilarang dan dibatasi tidak tersedia dalam bukti (hanya pengantar kebijakan).",
    "Tanggal publikasi dan tanggal berlaku (effective_from) dokumen tidak diketahui; penilaian hanya berdasarkan waktu pengambilan data 2026-11-02.",
    "Kewajiban perizinan/sertifikasi khusus (misalnya BPOM, SNI) untuk produk tertentu tidak tercakup dalam bukti."
  ],
  "follow_up_questions": [
    "Produk apa yang ingin dijual (nama, merek, kategori, dan fungsi/kegunaan)?",
    "Apakah produk merupakan produk impor atau produksi lokal, dan apakah sudah memiliki izin/edaran yang relevan?",
    "Apakah produk akan dijual sebagai bundling atau satuan, dan di halaman produk baru atau lama?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-community / 2 / PDF 0

atu jenis benda dan satu merk saja, kecuali jika produk yang dijual memang merupakan produk yang dijual secara paketan(bundling).

### E2 / shopee-id-prohibited-restricted / p0 / PDF 0

tuan dan kebijakan Shopee sebelum pendaftaran barang pada platform penjualan. Untuk kenyamanan Penjual, di bawah ini Shopee telah menyediakan pedoman singkat tentang barang yang dilarang dan dibatasi yang tidak boleh dijual di Shopee. Shopee akan memperbarui pedoman ini dari waktu ke waktu bila diperlukan. Silakan kunjungi halaman ini secara teratur untuk melihat pembaruan.

### E3 / shopee-id-community / 6 / PDF 0

6. Menggunakan halaman produk lama untuk mengunggah produk baru Halaman produk yang sudah memiliki penilaian dilarang keras digunakan untuk menjual produk yang berbeda. Berikut contoh dari penyalahgunaan halaman produk: Produk yang pertama dijual adalah sepatu wanita dengan banyak penilaian dari Pembeli. Saat stok sepatu wanita sudah habis atau produk sudah tidak dijual, Penjual mengubah foto, nam

### E4 / shopee-id-community / 2 / PDF 0

2. Nama dan rincian produk tidak relevan Kami ingin seluruh pengguna Shopee mendapatkan informasi yang relevan ketika membuka sebuah halaman produk. Pastikan agar Foto, Nama dan Deskripsi Produk anda sesuai dan benar benar menampilkan produk yang ingin dijual. Setiap halaman produk hanya dapat digunakan untuk menjual satu jenis benda dan satu merk saja, kecuali jika produk yang dijual memang merup

### E5 / shopee-id-community / 7 / PDF 0

7. Manipulasi harga Memanipulasi harga adalah sebuah pelanggaran dalam peraturan Shopee contohnya: mendaftarkan sebuah produk dengan harga yang sangat rendah dengan tujuan bukan untuk dijual ataupun dibeli oleh pengguna Shopee. Hal ini dapat menyebabkan produk Anda diblokir secara otomatis oleh sistem kami.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-015 — clarification

Apakah produk saya memerlukan label berbahasa Indonesia?

必要要点：
- Meminta jenis produk dan pasar tujuan.
- Menjelaskan indeks belum menyediakan dasar lengkap label fisik; tidak memberi kesimpulan pasti.

必要gold证据完整：None。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "信息不足",
  "summary": "Bukti yang tersedia tidak memuat ketentuan yang secara langsung mewajibkan label berbahasa Indonesia untuk produk yang dijual di Shopee Indonesia. Bukti hanya menyebut kewajiban label tanggal kedaluwarsa/\"gunakan sebelum\" untuk produk tertentu (E3), serta ketentuan umum layanan dan daftar barang terlarang yang tidak membahas bahasa label. Karena itu, kewajiban label berbahasa Indonesia tidak dapat dipastikan dari bukti ini dan perlu verifikasi lebih lanjut.",
  "evidence": [
    {
      "claim": "Produk tertentu (makanan, kesehatan, kecantikan, perlengkapan ibu dan bayi, produk digital dan jasa) harus diberi label tanggal kedaluwarsa atau \"gunakan sebelum\" secara jelas dan benar; ketentuan ini tidak menyebut kewajiban bahasa Indonesia.",
      "doc_id": "shopee-id-prohibited-restricted",
      "source_title": "Shopee Indonesia - Kebijakan Barang yang Dilarang dan Dibatasi",
      "section_path": "",
      "clause_id": "1",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Semua produk harus diberi label tanggal kedaluwarsa atau \"gunakan sebelum\" dengan jelas dan benar.",
      "evidence_id": "E3"
    },
    {
      "claim": "Kebijakan barang terlarang dan dibatasi memuat berbagai kategori produk yang dilarang, namun tidak memuat ketentuan tentang bahasa label produk.",
      "doc_id": "shopee-id-prohibited-restricted",
      "source_title": "Shopee Indonesia - Kebijakan Barang yang Dilarang dan Dibatasi",
      "section_path": "",
      "clause_id": "1",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Produk dokumen resmi yang penerbitan dan distribusinya memerlukan izin dari pihak pemerintah/instansi/lembaga berwenang",
      "evidence_id": "E4"
    },
    {
      "claim": "Syarat Layanan Shopee Indonesia yang dikutip tidak memuat ketentuan mengenai kewajiban label berbahasa Indonesia.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "40.10",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Terakhir diubah : 13 Oktober 2026",
      "evidence_id": "E1"
    },
    {
      "claim": "Ketentuan Syarat Layanan yang dikutip hanya membahas pernyataan persetujuan pengguna dan tidak membahas persyaratan label produk.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "40.10",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "SAYA TELAH MEMBACA PERJANJIAN INI DAN MENYETUJUI SEMUA KETENTUAN YANG TERCANTUM DI ATAS",
      "evidence_id": "E2"
    },
    {
      "claim": "Pasal 5.7 Syarat Layanan membahas penghapusan akun pengguna dan tidak berkaitan dengan persyaratan label produk.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "5.7",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pengguna dapat menghapus Akun mereka jika mereka memberi tahu Shopee secara tertulis",
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Kewajiban label berbahasa Indonesia (Bahasa Indonesia) untuk produk yang dijual di Shopee Indonesia",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-terms",
        "shopee-id-prohibited-restricted"
      ],
      "note": "Bukti yang tersedia tidak memuat ketentuan yang secara langsung mengatur kewajiban bahasa label; perlu verifikasi ke regulasi pemerintah Indonesia dan kebijakan Shopee terkini."
    },
    {
      "item": "Label tanggal kedaluwarsa/\"gunakan sebelum\" untuk produk makanan, kesehatan, kecantikan, perlengkapan ibu dan bayi, produk digital dan jasa",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-prohibited-restricted"
      ],
      "note": "Wajib dicantumkan dengan jelas dan benar; produk kedaluwarsa tidak boleh didaftarkan (E3)."
    }
  ],
  "unknowns": [
    "Tidak ada bukti yang menyebut kewajiban label berbahasa Indonesia secara eksplisit, baik di Syarat Layanan Shopee maupun Kebijakan Barang Terlarang dan Dibatasi.",
    "Regulasi pemerintah Indonesia (misalnya ketentuan label pangan, kosmetik, atau perlindungan konsumen) tidak tersedia dalam bukti.",
    "Kategori produk pengguna tidak diketahui, sehingga kewajiban label spesifik per kategori tidak dapat ditentukan.",
    "Tanggal berlaku (effective_from) seluruh dokumen tidak diketahui; hanya tanggal perubahan terakhir Syarat Layanan (13 Oktober 2026) yang tercantum di E1."
  ],
  "follow_up_questions": [
    "Produk apa yang Anda jual (kategori dan jenis produknya)?",
    "Apakah produk Anda termasuk makanan, kosmetik, kesehatan, atau perlengkapan ibu dan bayi?",
    "Apakah Anda menjual melalui Shopee Indonesia saja atau juga platform/marketplace lain?",
    "Apakah produk Anda sudah memiliki label dalam bahasa lain (misalnya Inggris) dan ingin mengetahui apakah perlu terjemahan bahasa Indonesia?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-terms / 40.10 / PDF 0

UDKAN UNTUK MEMILIKI KEKUATAN DAN AKIBAT YANG SAMA SEPERTI BILA SAYA MENANDATANGANI NAMA SAYA SECARA MANUAL. Terakhir diubah : 13 Oktober 2026 Apakah kamu puas dengan artikelnya? Puas Tidak Puas

### E2 / shopee-id-terms / 40.10 / PDF 0

hat Umum”. SAYA TELAH MEMBACA PERJANJIAN INI DAN MENYETUJUI SEMUA KETENTUAN YANG TERCANTUM DI ATAS DAN SETIAP REVISI YANG DILAKUKAN ATASNYA SESUDAHNYA. DENGAN MENGEKLIK TOMBOL "DAFTAR" ATAU "HUBUNGKAN DENGAN FACEBOOK" DI PADA SAAT PENDAFTARAN, SAYA MEMAHAMI BAHWA SAYA SEDANG MEMBUAT TANDA TANGAN DIGITAL, YANG SAYA MAKSUDKAN UNTUK MEMILIKI KEKUATAN DAN AKIBAT YANG SAMA SEPERTI BILA SAYA MENANDATANG

### E3 / shopee-id-prohibited-restricted / 1 / PDF 0

; (xliii) Produk kadaluarsa, termasuk produk makanan, produk kesehatan, produk kecantikan, produk perlengkapan ibu dan bayi, produk digital dan jasa. Semua produk harus diberi label tanggal kedaluwarsa atau "gunakan sebelum" dengan jelas dan benar. Produk yang sudah kadaluarsa tidak boleh didaftarkan. (xliv) Produk tidak sesuai dengan informasi produk (nama, foto, video, deskripsi, dan keterangan

### E4 / shopee-id-prohibited-restricted / 1 / PDF 0

angko, dan materai (termasuk mata uang, prangko, dan materai palsu) yang dilarang diperjualbelikan melalui media elektronik; (xvii) Produk yang belum yang tersedia namun telah didaftarkan sebagai SKU oleh Penjual untuk keperluan pembayaran uang muka; (xviii) Produk dokumen resmi yang penerbitan dan distribusinya memerlukan izin dari pihak pemerintah/instansi/lembaga berwenang termasuk tidak terbat

### E5 / shopee-id-terms / 5.7 / PDF 0

5.7. Pengguna dapat menghapus Akun mereka jika mereka memberi tahu Shopee secara tertulis (termasuk melalui email kami tentang niatan mereka tersebut. Terlepas dari adanya penghapusan tersebut, Pengguna tetap bertanggung jawab dan berkewajiban untuk setiap transaksi yang belum selesai (baik apakah dimulai sebelum atau setelah penghapusan tersebut), pengiriman produk, pembayaran untuk produk, atau

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-016 — clarification

Mainan apa yang paling laris?

必要要点：
- Meminta pasar/platform dan rentang waktu.
- Menjelaskan tidak memiliki data penjualan untuk membuat peringkat.

必要gold证据完整：None。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "信息不足",
  "summary": "Bukti yang tersedia hanya mengatur kebijakan impor mainan (cakupan pos tarif, ketentuan peralihan, dan kewajiban impor), tidak memuat data penjualan atau daftar produk mainan terlaris. Karena itu, pertanyaan mainan apa yang paling laris tidak dapat dijawab dari bukti ini.",
  "evidence": [
    {
      "claim": "Mainan tercakup sebagai barang dalam Lampiran I kebijakan impor barang konsumsi.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XII KETENTUAN PENUTUP",
      "page": 127,
      "collected_at": "2026-11-02",
      "quote": "XX. MAINAN Cakupan Barang: Mainan pada Lampiran I -",
      "evidence_id": "E1"
    },
    {
      "claim": "Terdapat ketentuan peralihan bagi mainan dalam rangka fasilitas kemudahan impor tujuan ekspor yang tiba di pelabuhan paling lambat 30 hari setelah peraturan berlaku.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XI KETENTUAN PERALIHAN",
      "clause_id": "Pasal 22 huruf o",
      "page": 16,
      "collected_at": "2026-11-02",
      "quote": "rupa mainan dalam rangka fasilitas kemudahan Impor tujuan ekspor pembebasan yang tiba di pelabuhan tujuan paling lambat 30 (tiga puluh) hari setelah Peraturan Menteri ini berlaku.",
      "evidence_id": "E2"
    },
    {
      "claim": "Pos tarif 95.03 mencakup sepeda roda tiga, skuter, mobil berpedal, kereta boneka, boneka, mainan lainnya, model skala, dan puzzle, dengan ketentuan impor.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XII KETENTUAN PENUTUP",
      "page": 50,
      "collected_at": "2026-11-02",
      "quote": "95.03 Sepeda roda tiga, skuter, mobil berpedal dan mainan beroda semacam itu; kereta boneka; boneka; mainan lainnya; model yang diperkecil (\"skala\") dan model rekreasi semacam itu, dapat digerakkan atau tidak; puzzle dari segala jenis. KETENTUAN IMPOR",
      "evidence_id": "E3"
    },
    {
      "claim": "Rincian pos tarif mainan mencakup blok angka/huruf/binatang, set penyusun kata, set toy printing, abaci, mesin jahit mainan, mesin ketik mainan, tali lompat, dan kelereng.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XII KETENTUAN PENUTUP",
      "page": 51,
      "collected_at": "2026-11-02",
      "quote": "318. 9503.00.91 -- Blok atau potongan angka, huruf atau binatang; set penyusun kata; set penyusun dan pengucap kata; set toy printing; counting frame mainan (abaci); mesin jahit mainan; mesin ketik mainan PCE SET √ 319. 9503.00.92 -- Tali lompat PCE √ 320. 9503.00.93 -- Kelereng PCE; KGM √",
      "evidence_id": "E4"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Klasifikasi pos tarif mainan (HS 95.03) dan ketentuan impornya",
      "status": "可确认",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "Bukti E3 dan E4 memuat uraian pos tarif 95.03 beserta rincian subpos, tetapi tidak memuat persyaratan teknis atau sertifikasi produk."
    },
    {
      "item": "Kewajiban perizinan/ketentuan impor mainan (IT/IP/PI/LS/Post Border)",
      "status": "需人工复核",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "Kolom keterangan IT IP PI LS Post Border tercantum pada E3, namun isi persyaratan per kolom tidak dijelaskan dalam bukti."
    },
    {
      "item": "Batas waktu kedatangan barang untuk fasilitas impor tujuan ekspor",
      "status": "可确认",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "Pasal 22 huruf o: paling lambat 30 hari setelah peraturan berlaku (E2)."
    }
  ],
  "unknowns": [
    "Data penjualan atau daftar produk mainan terlaris tidak tersedia dalam bukti.",
    "Tanggal berlaku (effective_from) Permendag No. 23 Tahun 2025 tidak tercantum dalam bukti.",
    "Persyaratan rinci per kolom IT/IP/PI/LS/Post Border untuk mainan tidak dijelaskan dalam bukti.",
    "Standar teknis, sertifikasi, atau label mainan (misalnya SNI) tidak tercakup dalam bukti."
  ],
  "follow_up_questions": [
    "Apakah Anda ingin mengetahui mainan terlaris untuk platform tertentu (misalnya Shopee) dan kategori/rentang harga tertentu?",
    "Apakah tujuan Anda adalah analisis penjualan atau kepatuhan impor mainan ke Indonesia?"
  ]
}
```

实际输入证据：

### E1 / import-23-2025 / p1053 / PDF 127

XX. MAINAN Cakupan Barang: Mainan pada Lampiran I -

### E2 / import-23-2025 / Pasal 22 huruf o / PDF 16

rupa mainan dalam rangka fasilitas kemudahan Impor tujuan ekspor pembebasan yang tiba di pelabuhan tujuan paling lambat 30 (tiga puluh) hari setelah Peraturan Menteri ini berlaku.

### E3 / import-23-2025 / p498 / PDF 50

IV. MAINAN No Pos Tarif/HS Uraian Barang Satuan Barang Keterangan IT IP PI LS Post Border 95.03 Sepeda roda tiga, skuter, mobil berpedal dan mainan beroda semacam itu; kereta boneka; boneka; mainan lainnya; model yang diperkecil ("skala") dan model rekreasi semacam itu, dapat digerakkan atau tidak; puzzle dari segala jenis. KETENTUAN IMPOR

### E4 / import-23-2025 / 318 / PDF 51

318.  9503.00.91 -- Blok atau potongan angka, huruf atau binatang; set penyusun kata; set penyusun dan pengucap kata; set toy printing; counting frame mainan (abaci); mesin jahit mainan; mesin ketik mainan PCE; SET    √ 319.  9503.00.92 -- Tali lompat PCE    √ 320.  9503.00.93 -- Kelereng PCE; KGM √

### E5 / shopee-id-terms / 6.2 / PDF 0

apa fitur yang tersedia bagi Penjual, termasuk namun tidak terbatas pada kehilangan akses untuk menarik Saldo Penjual.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-017 — uncovered

Berapa tarif bea masuk untuk mainan anak dari Tiongkok ke Indonesia?

必要要点：
- Tidak menetapkan tarif dari korpus ini.
- Memerlukan klasifikasi HS, asal barang/perlakuan preferensi dan tanggal yang relevan.

必要gold证据完整：None。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "信息不足",
  "summary": "Bukti yang tersedia tidak memuat tarif bea masuk (besaran tarif/HS code) untuk mainan anak dari Tiongkok. Permendag No. 23 Tahun 2025 yang dikutip hanya memuat definisi kawasan bebas bea, tempat penimbunan berikat, ketentuan minuman beralkohol, dan uraian pos tarif untuk olahan makanan bayi/anak (HS 1901.10), bukan mainan anak. Oleh karena itu tarif bea masuk tidak dapat ditentukan dari bukti ini.",
  "evidence": [
    {
      "claim": "KPBPB didefinisikan sebagai kawasan bebas dari pengenaan bea masuk, PPN, PPnBM, dan cukai — hanya definisi kawasan, bukan tarif mainan.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB I KETENTUAN UMUM",
      "clause_id": "20",
      "page": 4,
      "collected_at": "2026-11-02",
      "quote": "Kawasan Perdagangan Bebas dan Pelabuhan Bebas ... bebas dari pengenaan bea masuk, pajak pertambahan nilai, pajak penjualan atas Barang mewah, dan cukai.",
      "evidence_id": "E1"
    },
    {
      "claim": "TPB memperoleh penangguhan bea masuk — hanya definisi fasilitas, bukan tarif mainan.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB I KETENTUAN UMUM",
      "clause_id": "22",
      "page": 5,
      "collected_at": "2026-11-02",
      "quote": "Tempat Penimbunan Berikat ... digunakan untuk menimbun Barang dengan tujuan tertentu dengan mendapatkan penangguhan bea masuk.",
      "evidence_id": "E4"
    },
    {
      "claim": "Ketentuan penutup hanya membahas minuman beralkohol Duty Not Paid, tidak relevan dengan mainan anak.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XII KETENTUAN PENUTUP",
      "clause_id": "64",
      "page": 650,
      "collected_at": "2026-11-02",
      "quote": "Minuman Beralkohol Duty Not Paid yang dikeluarkan dari Pusat Logistik Berikat hanya untuk tujuan distribusi ke Toko Bebas Bea.",
      "evidence_id": "E2"
    },
    {
      "claim": "Uraian pos tarif yang tersedia adalah HS 1901.10 untuk olahan makanan bayi/anak, bukan pos tarif mainan anak.",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XII KETENTUAN PENUTUP",
      "clause_id": "25",
      "page": 320,
      "collected_at": "2026-11-02",
      "quote": "1901.10 - Olahan yang cocok untuk bayi atau anak- anak, disiapkan untuk penjualan eceran:",
      "evidence_id": "E5"
    },
    {
      "claim": "Syarat Layanan Shopee hanya mengatur pengembalian dana, tidak memuat tarif bea masuk.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "clause_id": "22.8",
      "collected_at": "2026-11-02",
      "quote": "pengembalian dana kepada Pembeli akan dilakukan menggunakan metode pembayaran yang sama ...",
      "evidence_id": "E3"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Tarif bea masuk mainan anak (HS 9503) dari Tiongkok",
      "status": "需人工复核",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "Bukti tidak memuat pos tarif maupun besaran tarif mainan anak."
    },
    {
      "item": "Ketentuan impor barang konsumsi (Permendag 23/2025) untuk mainan anak",
      "status": "需人工复核",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "Hanya definisi umum dan ketentuan lain yang tersedia; ketentuan khusus mainan tidak ditemukan."
    }
  ],
  "unknowns": [
    "Besaran tarif bea masuk (persentase) untuk mainan anak tidak ada dalam bukti.",
    "Kode HS/pos tarif untuk mainan anak (mis. HS 9503) tidak tercantum dalam bukti.",
    "Tarif preferensi/FTAPerjanjian perdagangan Tiongkok–Indonesia (mis. ACFTA) tidak dibahas dalam bukti.",
    "Tanggal berlaku (effective_from) Permendag 23/2025 tidak diketahui dari bukti.",
    "Ketentuan perizinan (IT/IP/PI/LS) khusus mainan anak tidak ditemukan dalam bukti."
  ],
  "follow_up_questions": [
    "Jenis mainan anak apa yang dimaksud (mis. mainan plastik, elektronik, boneka) agar kode HS dapat ditentukan?",
    "Apakah barang diimpor sebagai barang konsumsi eceran atau bahan baku/komponen?",
    "Apakah Anda ingin memanfaatkan skema preferensi tarif (mis. ACFTA) atau tarif MFN biasa?"
  ]
}
```

实际输入证据：

### E1 / import-23-2025 / 20 / PDF 4

20. Kawasan Perdagangan Bebas dan Pelabuhan Bebas yang selanjutnya disingkat KPBPB adalah suatu kawasan yang berada dalam wilayah hukum Negara Kesatuan Republik Indonesia yang terpisah dari Daerah Pabean sehingga bebas dari pengenaan bea masuk, pajak pertambahan nilai, pajak penjualan atas Barang mewah, dan cukai.

### E2 / import-23-2025 / p650 / PDF 64

Minuman Beralkohol Duty Not Paid yang dikeluarkan dari Pusat Logistik Berikat hanya untuk tujuan distribusi ke Toko Bebas Bea.

### E3 / shopee-id-terms / 22.8 / PDF 0

22.8. Tunduk pada Pasal 22.9, pengembalian dana kepada Pembeli akan dilakukan menggunakan metode pembayaran yang sama yang digunakan oleh Pembeli untuk pembelian awal (“ Metode Pembayaran Awal ”) dalam jangka waktu yang berlaku yang dipublikasikan dari waktu ke waktu di [Pengembalian Dana] Berapa lama proses pengembalian dana di Shopee? di Pusat Bantuan Shopee Indonesia (atau URL atau lokasi lain

### E4 / import-23-2025 / 22 / PDF 5

22. Tempat Penimbunan Berikat yang selanjutnya disingkat TPB adalah bangunan, tempat, atau kawasan yang memenuhi persyaratan tertentu yang digunakan untuk menimbun Barang dengan tujuan tertentu dengan mendapatkan penangguhan bea masuk.

### E5 / import-23-2025 / p320 / PDF 25

No Pos Tarif/HS Uraian Barang Keterangan IT IP PI LS Post Border kurang dari 5 % menurut beratnya yang dihitung atas dasar kakao yang dihilangkan seluruh lemaknya, tidak dirinci atau termasuk pos lainnya. 1901.10 - Olahan yang cocok untuk bayi atau anak- anak, disiapkan untuk penjualan eceran:

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-020 — uncovered

Dapatkah Anda memastikan bahwa Permendag Nomor 19 Tahun 2026 masih berlaku pada 1 Januari 2027?

必要要点：
- Tidak menjamin status hukum pada 1 Januari 2027 dari snapshot 2 November 2026.
- Membedakan ketentuan mulai berlaku dengan kemungkinan perubahan atau pencabutan di masa depan.

必要gold证据完整：None。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "信息不足",
  "summary": "Tidak dapat dipastikan dari bukti yang tersedia apakah Permendag No. 19 Tahun 2026 masih berlaku pada 1 Januari 2027. Bukti E1 hanya memuat halaman BAB X KETENTUAN PENUTUP tanpa teks ketentuan mengenai masa berlaku, dan tanggal terbit maupun tanggal berlaku tidak tercantum (unknown).",
  "evidence": [
    {
      "claim": "Permendag No. 19 Tahun 2026 memiliki BAB X KETENTUAN PENUTUP, tetapi isi ketentuan penutup (termasuk klausul masa berlaku) tidak tersedia dalam kutipan bukti.",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "BAB X KETENTUAN PENUTUP",
      "page": 36,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "BERITA NEGARA REPUBLIK INDONESIA TAHUN 2026 NOMOR",
      "evidence_id": "E1"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Konfirmasi masa berlaku Permendag No. 19 Tahun 2026 pada 1 Januari 2027",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Bukti hanya memuat judul BAB X KETENTUAN PENUTUP tanpa teks klausul berlaku/tidak berlaku; tanggal terbit dan tanggal berlaku tidak tercantum."
    }
  ],
  "unknowns": [
    "Teks lengkap BAB X KETENTUAN PENUTUP Permendag No. 19 Tahun 2026 (klausul mulai berlaku dan kemungkinan masa berlaku) tidak tersedia dalam bukti.",
    "Tanggal pengundangan/terbit dan tanggal mulai berlaku Permendag No. 19 Tahun 2026 tidak tercantum (unknown).",
    "Tidak ada bukti mengenai pencabutan atau perubahan Permendag No. 19 Tahun 2026 sebelum 1 Januari 2027."
  ],
  "follow_up_questions": [
    "Apakah Anda memiliki salinan lengkap BAB X KETENTUAN PENUTUP atau halaman pengundangan Permendag No. 19 Tahun 2026 yang memuat klausul mulai berlaku?"
  ]
}
```

实际输入证据：

### E1 / ecommerce-19-2026 / p458 / PDF 36

BERITA NEGARA REPUBLIK INDONESIA TAHUN 2026 NOMOR         Ж

### E2 / shopee-id-prohibited-restricted / 1 / PDF 0

mkan pemberitahuan push kepada Pembeli tentang daftar tersebut. Anda bertanggung jawab untuk memastikan bahwa Pengaturan telepon Anda memungkinkan Anda untuk menerima pemberitahuan push. Apabila Anda memiliki pertanyaan lebih lanjut, Anda dapat menghubungi kami di Live Chat Customer Service Shopee (24 Jam) Senin - Minggu termasuk hari libur nasional. Diubah terakhir: 31 Juli 2026 Apakah kamu puas

### E3 / shopee-id-terms / 5.5 / PDF 0

5.5. Anda setuju untuk (a) menjaga kerahasiaan kata sandi anda dan hanya menggunakan ID Pengguna dan kata sandi anda saat login, (b) memastikan bahwa anda keluar dari Akun anda pada akhir setiap sesi di Situs, (c) segera memberi tahu Shopee tentang penggunaan tanpa izin atas Akun, ID Pengguna dan/atau kata sandi anda, dan (d) memastikan bahwa informasi Akun anda akurat dan terkini. Anda sepenuhnya

### E4 / import-23-2025 / 1 / PDF 132

1. PI yang masih berlaku; dan 2. Perubahan rencana Impor dalam 1 (satu) tahun takwim.

### E5 / import-23-2025 / 1 / PDF 139

1. PI yang masih berlaku; dan 2. Perubahan rencana Impor dalam 1 (satu) tahun takwim.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-zh-012 — uncovered

在印尼进口商品需要什么营业许可？

必要要点：
- Tidak memperluas persyaratan khusus alkohol menjadi semua barang impor.
- Meminta kategori/HS dan jalur impor; korpus yang tersedia belum cukup untuk jawaban menyeluruh.

必要gold证据完整：None。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "根据现有证据，在印尼从事进口业务需要持有「进口领域营业许可（Perizinan Berusaha di bidang Impor）」，该许可属于进口监管的检查对象；若通过PPMSE（电子系统交易平台）注册经营，注册时尚未满足营业许可要求的，最迟须在注册后6个月内取得营业许可。证据未列明进口营业许可的具体类型、申请条件与办理流程，也未说明一般消费品进口的完整许可清单，需人工复核。",
  "evidence": [
    {
      "claim": "进口领域的营业许可（Perizinan Berusaha di bidang Impor）是进口监管的检查事项之一，说明进口经营活动须具备该营业许可。",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB X PENGAWASAN",
      "clause_id": "Pasal 21 ayat (2) huruf b",
      "page": 14,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "b. Perizinan Berusaha di bidang Impor;",
      "evidence_id": "E5"
    },
    {
      "claim": "通过PPMSE注册的经营者，注册时尚未满足营业许可要求的，须自注册起最长6个月内取得营业许可。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Kelima Fasilitasi Perizinan Berusaha oleh PPMSE",
      "clause_id": "Pasal 17 ayat (4)",
      "page": 14,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "(4) Pedagang yang belum memenuhi ketentuan Perizinan Berusaha pada saat pendaftaran sebagaimana dimaksud pada ayat (3), wajib memiliki Perizinan Berusaha paling lama 6 (enam) bulan sejak mendaftar pada PPMSE.",
      "evidence_id": "E4"
    },
    {
      "claim": "PMSE领域的营业许可发放不收取费用。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketujuh Biaya Penerbitan Perizinan Berusaha Bidang PMSE",
      "clause_id": "Pasal 19",
      "page": 15,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pasal 19 Penerbitan Perizinan Berusaha Bidang PMSE tidak dipungut biaya.",
      "evidence_id": "E1"
    },
    {
      "claim": "PPMSE可为经营者提供提交营业许可申请及满足商品/服务标准方面的协助。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Kelima Fasilitasi Perizinan Berusaha oleh PPMSE",
      "page": 14,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "d. pendampingan dalam mengajukan Perizinan Berusaha dan pemenuhan standar Barang dan/atau Jasa.",
      "evidence_id": "E3"
    },
    {
      "claim": "酒精饮料进口领域的营业许可由多项许可组成（原文列举未在证据中展开）。",
      "doc_id": "import-23-2025",
      "source_title": "Permendag No. 23 Tahun 2025 tentang Kebijakan dan Pengaturan Impor Barang Konsumsi",
      "section_path": "BAB XII KETENTUAN PENUTUP",
      "page": 57,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Perizinan Berusaha di bidang Impor untuk Impor Minuman Beralkohol terdiri atas:",
      "evidence_id": "E2"
    }
  ],
  "compliance_checklist": [
    {
      "item": "取得进口领域营业许可（Perizinan Berusaha di bidang Impor）",
      "status": "需人工复核",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "证据仅表明该许可属于进口监管检查事项，未列明具体许可类型、申请条件与流程。"
    },
    {
      "item": "通过PPMSE注册经营时，在注册后6个月内补齐营业许可",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 17 ayat (4) 明确6个月期限。"
    },
    {
      "item": "PMSE领域营业许可费用",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "Pasal 19 规定不收费。"
    },
    {
      "item": "酒精饮料进口所需营业许可的具体构成",
      "status": "需人工复核",
      "basis_doc_ids": [
        "import-23-2025"
      ],
      "note": "证据仅引出列举句，未提供具体许可项目。"
    }
  ],
  "unknowns": [
    "进口营业许可（Perizinan Berusaha di bidang Impor）的具体类型、申请条件、办理机构与流程，证据未提供。",
    "一般消费品（非酒精饮料）进口的完整许可与认证清单，证据未提供。",
    "酒精饮料进口营业许可的具体组成条款内容，证据未展开。",
    "相关法规的发布日期与生效日期均为unknown，无法确认时效。",
    "证据未说明进口许可与PMSE许可之间的关系及是否需同时具备。"
  ],
  "follow_up_questions": [
    "您计划进口的商品类别是什么（如一般消费品、食品饮料、酒精饮料等）？",
    "您是否通过电商平台（PPMSE）销售，还是以传统进口商/批发方式经营？",
    "您目前是否已持有任何印尼营业许可（NIB等）？"
  ]
}
```

实际输入证据：

### E1 / ecommerce-19-2026 / Pasal 19 / PDF 15

Pasal 19 Penerbitan Perizinan Berusaha Bidang PMSE tidak dipungut biaya.

### E2 / import-23-2025 / p556 / PDF 57

Perizinan Berusaha di bidang Impor untuk Impor Minuman Beralkohol terdiri atas:

### E3 / ecommerce-19-2026 / p169 / PDF 14

-14- d. pendampingan dalam mengajukan Perizinan Berusaha dan pemenuhan standar Barang dan/atau Jasa.

### E4 / ecommerce-19-2026 / Pasal 17 ayat (4) / PDF 14

(4) Pedagang yang belum memenuhi ketentuan Perizinan Berusaha pada saat pendaftaran sebagaimana dimaksud pada ayat (3), wajib memiliki Perizinan Berusaha paling lama 6 (enam) bulan sejak mendaftar pada PPMSE.

### E5 / import-23-2025 / Pasal 21 ayat (2) huruf b / PDF 14

b. Perizinan Berusaha di bidang Impor;

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-009 — answerable

Apa kewajiban penjual terkait informasi berat dan dimensi barang menurut Syarat Layanan Shopee?

必要要点：
- Informasi setiap barang yang dikirim harus akurat, termasuk berat dan/atau dimensi.

必要gold证据完整：True。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Menurut Pasal 20.4 Syarat Layanan Shopee Indonesia, penjual wajib memberikan informasi yang akurat mengenai berat dan/atau dimensi setiap barang yang dikirim kepada Pembeli melalui Platform Shopee. Jika informasi tidak akurat atau terdapat perbedaan antara pernyataan penjual dan berat/dimensi paket sebenarnya, Shopee berhak mengambil tindakan atas kebijakannya sendiri, antara lain sanksi poin penalti terkait kampanye, menahan dan/atau mengurangi Saldo Penjual, meminta pembayaran biaya tambahan atau kompensasi kerugian, menyesuaikan berat/dimensi untuk perhitungan Biaya Pengiriman berdasarkan data historis dan membagikannya kepada penyedia logistik pihak ketiga, serta meminta penjual menandatangani pernyataan atau formulir. Rincian teknis seperti cara pengukuran, batas toleransi, dan prosedur keberatan tidak diatur dalam kutipan yang tersedia.",
  "evidence": [
    {
      "claim": "Penjual wajib memberikan informasi yang akurat, termasuk berat dan/atau dimensi, atas setiap barang yang dikirim kepada Pembeli melalui Platform Shopee.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "20.4",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Penjual wajib memberikan informasi yang akurat (termasuk berat dan/atau dimensi) atas setiap barang yang dikirimkan kepada Pembeli melalui Platform Shopee",
      "evidence_id": "E1"
    },
    {
      "claim": "Jika informasi berat/dimensi tidak akurat atau terdapat perbedaan dengan pernyataan penjual, Shopee berhak mengambil tindakan atas kebijakannya sendiri, termasuk sanksi poin penalti terkait kampanye, menahan dan/atau mengurangi Saldo Penjual, serta meminta pembayaran biaya tambahan atau kompensasi kerugian.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "20.4",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Shopee berhak untuk mengambil tindakan terhadap Penjual atas kebijakannya sendiri, termasuk namun tidak terbatas pada (i) memberikan sanksi poin penalti sehubungan dengan kampanye, (ii) menahan, dan/atau mengurangi Saldo Penjual, dan/atau (iii) meminta Penjual untuk membayar biaya tambahan, dan/atau meminta kompensasi dari Penjual",
      "evidence_id": "E2"
    },
    {
      "claim": "Shopee dapat menyesuaikan berat/dimensi untuk tujuan menghitung Biaya Pengiriman berdasarkan data historis dan membagikan informasi tersebut kepada penyedia logistik pihak ketiga Shopee, serta meminta penjual menandatangani pernyataan atau formulir yang dianggap perlu.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "20.4",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "menyesuaikan berat/dimensi tersebut untuk tujuan menghitung Biaya Pengiriman berdasarkan data historis dan dapat membagikan informasi tersebut dengan penyedia logistik pihak ketiga Shopee ... meminta penjual menandatangani setiap pernyataan atau formulir sebagaimana dirasa perlu berdasarkan kebijakan Shopee",
      "evidence_id": "E4"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Kewajiban memberikan informasi berat dan/atau dimensi barang yang akurat kepada Pembeli melalui Platform Shopee",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Diatur dalam Pasal 20.4; berlaku untuk setiap barang yang dikirim melalui Platform Shopee."
    },
    {
      "item": "Kepatuhan terhadap standar pengukuran berat/dimensi dan batas toleransi yang ditetapkan Shopee",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Kutipan Pasal 20.4 tidak memuat metode pengukuran, batas toleransi, atau ambang selisih yang memicu tindakan."
    },
    {
      "item": "Pemahaman atas konsekuensi ketidakakuratan informasi (poin penalti, penahanan/pengurangan saldo, biaya tambahan, kompensasi, penyesuaian berat/dimensi)",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Tindakan diambil atas kebijakan Shopee dan bersifat tidak terbatas pada yang disebutkan."
    }
  ],
  "unknowns": [
    "Tanggal publikasi dan tanggal berlaku (effective_from) Pasal 20.4 tidak tercantum dalam bukti; hanya diketahui waktu pengambilan data 2026-11-02.",
    "Metode pengukuran berat/dimensi yang diwajibkan, batas toleransi selisih, dan ambang pemicu sanksi tidak dijelaskan dalam kutipan.",
    "Prosedur pengajuan keberatan atau banding atas sanksi/penyesuaian berat/dimensi tidak tercakup dalam bukti.",
    "Rujukan ke Bagian 20.2 dalam Pasal 20.4 tidak disertakan teks lengkapnya dalam bukti."
  ],
  "follow_up_questions": [
    "Apakah Anda ingin mengetahui ketentuan Pasal 20.2 yang dirujuk, atau prosedur keberatan atas sanksi penyesuaian berat/dimensi?",
    "Apakah Anda memerlukan informasi ini untuk kategori produk tertentu (misalnya barang besar/berat) agar dapat ditelusuri ketentuan tambahannya?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-terms / 20.4 / PDF 0

20.4. Penjual wajib memberikan informasi yang akurat (termasuk berat dan/atau dimensi) atas setiap barang yang dikirimkan kepada Pembeli melalui Platform Shopee berdasarkan Layanan sebagaimana yang dimaksud dalam Syarat Layanan ini. Dalam hal Penjual tidak memberikan informasi yang akurat untuk setiap barang, atau terdapat perbedaan dalam pernyataan Penjual tentang berat/dimensi paket, atau untuk

### E2 / shopee-id-terms / 20.4 / PDF 0

apat perbedaan dalam pernyataan Penjual tentang berat/dimensi paket, atau untuk memastikan informasi yang diberikan akurat, Shopee berhak untuk mengambil tindakan terhadap Penjual atas kebijakannya sendiri, termasuk namun tidak terbatas pada (i) memberikan sanksi poin penalti sehubungan dengan kampanye, (ii) menahan, dan/atau mengurangi Saldo Penjual, dan/atau (iii) meminta Penjual untuk membayar

### E3 / shopee-id-terms / 20.4 / PDF 0

an/atau mengurangi Saldo Penjual, dan/atau (iii) meminta Penjual untuk membayar biaya tambahan, dan/atau meminta kompensasi dari Penjual untuk segala kerugian yang diderita oleh Shopee yang timbul akibat penyediaan informasi yang tidak akurat, dalam situasi masing-masing dengan mengurangi Saldo Penjual, (iv) menyesuaikan berat/dimensi tersebut untuk tujuan menghitung Biaya Pengiriman berdasarkan d

### E4 / shopee-id-terms / 20.4 / PDF 0

an berat/dimensi tersebut untuk tujuan menghitung Biaya Pengiriman berdasarkan data historis dan dapat membagikan informasi tersebut dengan penyedia logistik pihak ketiga Shopee, atau tindakan lainnya dan/atau (v) meminta penjual menandatangani setiap pernyataan atau formulir sebagaimana dirasa perlu berdasarkan kebijakan Shopee 20.5. Dengan mengacu pada ketentuan di Bagian 20.2 di atas, pengirima

### E5 / shopee-id-terms / p0 / PDF 0

Syarat Layanan Shopee | Pusat Bantuan Shopee ID Hai, ada yang bisa kami bantu? Syarat Layanan Shopee 1. PENDAHULUAN 1.1. Selamat datang di platform Shopee (" Situs "). Silakan baca Syarat Layanan berikut dengan cermat sebelum menggunakan Situs ini atau membuka akun (" Akun ") agar anda mengetahui tentang hak dan kewajiban hukum anda sehubungan dengan PT Shopee International Indonesia dan afiliasin

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-010 — answerable

Apakah penjual wajib menyerahkan data untuk verifikasi oleh Shopee?

必要要点：
- Menyerahkan data yang diminta Shopee dan memastikan kebenaran serta keakuratannya.
- Shopee dapat meminta dokumen pendukung atau tambahan.

必要gold证据完整：False。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Ya, berdasarkan Syarat Layanan Shopee Indonesia, Penjual wajib dan bertanggung jawab menyerahkan data yang diminta Shopee untuk tujuan verifikasi Penjual, serta memastikan kebenaran dan keakuratan data tersebut. Shopee juga dapat sewaktu-waktu meminta dokumen pendukung atau dokumen tambahan. Bagi calon Penjual, data diminta dalam proses onboarding, dan hasil verifikasi ditentukan oleh Shopee. Namun, tanggal publikasi/efektif dokumen tidak tercantum dalam bukti, sehingga keberlakuan versi terbaru perlu dikonfirmasi.",
  "evidence": [
    {
      "claim": "Penjual wajib dan bertanggung jawab menyerahkan data yang diminta Shopee serta memastikan kebenaran dan keakuratan data yang diserahkan.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "23",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Penjual wajib dan bertanggung jawab untuk menyerahkan data-data yang diminta oleh Shopee serta memastikan kebenaran dan keakuratan data yang diserahkan oleh Penjual kepada Shopee.",
      "evidence_id": "E1"
    },
    {
      "claim": "Shopee dapat sewaktu-waktu meminta Penjual menyerahkan dokumen pendukung atau dokumen tambahan untuk mendukung verifikasi Penjual.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "23",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Shopee dapat sewaktu-waktu meminta Penjual untuk menyerahkan dokumen dukungan atau dokumen tambahan lainnya untuk mendukung verifikasi Penjual.",
      "evidence_id": "E1"
    },
    {
      "claim": "Untuk tujuan verifikasi Penjual yang dilakukan Shopee, Penjual wajib dan bertanggung jawab menyerahkan data-data yang diminta.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "23.3",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Untuk tujuan verifikasi Penjual yang dilakukan oleh Shopee, Penjual wajib dan bertanggung jawab untuk menyerahkan data-data yang diminta oleh Shopee",
      "evidence_id": "E2"
    },
    {
      "claim": "Dalam proses onboarding, Shopee akan meminta calon Penjual memberikan data untuk proses verifikasi oleh Shopee.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "6.2(a)",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Shopee akan meminta calon Penjual untuk memberikan data-data calon Penjual untuk proses verifikasi oleh Shopee.",
      "evidence_id": "E3"
    },
    {
      "claim": "Shopee berhak menilai dan menentukan hasil verifikasi calon Penjual serta memberikan keputusan akhir atas hasil verifikasi data.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "6.2(b)",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Shopee berhak untuk menilai dan menentukan hasil verifikasi calon Penjual serta memberikan keputusan akhir atas hasil verifikasi data calon Penjual.",
      "evidence_id": "E3"
    },
    {
      "claim": "Penjual yang telah terdaftar sebelum 31 Mei 2024 wajib segera memberikan data yang diperlukan paling lambat 1 Juli 2024.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "6.2(c)",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Penjual wajib untuk segera memberikan data yang diperlukan oleh Shopee kepada Shopee selambat-lambatnya pada tanggal 1 Juli 2024.",
      "evidence_id": "E5"
    },
    {
      "claim": "Kegagalan menyelesaikan proses verifikasi data dapat membuat Penjual kehilangan akses sementara terhadap beberapa fitur.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "6.2(c)",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "kegagalan untuk menyelesaikan proses verifikasi data dapat membuat Penjual kehilangan akses sementara terhadap beberapa fitur yang tersedia bagi Penjual",
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Penyerahan data Penjual untuk verifikasi oleh Shopee",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Diwajibkan berdasarkan klausul 23 dan 23.3; Shopee dapat meminta dokumen tambahan."
    },
    {
      "item": "Verifikasi data calon Penjual saat onboarding",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Diatur dalam klausul 6.2(a)-(b); keputusan akhir verifikasi ada pada Shopee."
    },
    {
      "item": "Kewajiban penyerahan data bagi Penjual terdaftar sebelum 31 Mei 2024",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Batas waktu 1 Juli 2024 tercantum, namun relevansi bagi Penjual yang mendaftar setelah tanggal tersebut tidak dijelaskan dalam bukti."
    },
    {
      "item": "Konsekuensi kegagalan verifikasi",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Bukti hanya menyebut kehilangan akses sementara terhadap beberapa fitur; rincian fitur dan prosedur pemulihan tidak dijelaskan."
    }
  ],
  "unknowns": [
    "Tanggal publikasi dan tanggal efektif Syarat Layanan tidak tercantum dalam bukti, sehingga keberlakuan versi dokumen pada 2026-11-02 tidak dapat dipastikan.",
    "Rincian fitur yang dapat hilang sementara akibat kegagalan verifikasi tidak dijelaskan.",
    "Prosedur pengajuan banding atau verifikasi ulang tidak dijelaskan dalam bukti.",
    "Ketentuan lanjutan setelah klausul 23.4 tidak tersedia dalam kutipan bukti."
  ],
  "follow_up_questions": [
    "Apakah Anda Penjual baru (onboarding) atau Penjual yang sudah terdaftar sebelum 31 Mei 2024?",
    "Jenis data atau dokumen apa yang diminta Shopee dari Anda saat ini?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-terms / 23 / PDF 0

leh Shopee, Penjual wajib dan bertanggung jawab untuk menyerahkan data-data yang diminta oleh Shopee serta memastikan kebenaran dan keakuratan data yang diserahkan oleh Penjual kepada Shopee. Penjual setuju bahwa Shopee dapat sewaktu-waktu meminta Penjual untuk menyerahkan dokumen dukungan atau dokumen tambahan lainnya untuk mendukung verifikasi Penjual. 23.4 Tanpa mengenyampingkan ketentuan di da

### E2 / shopee-id-terms / 23 / PDF 0

us dan bertanggung jawab penuh untuk tunduk dan memenuhi ketentuan hukum dan peraturan perundang-undangan yang berlaku, termasuk namun tidak terbatas untuk memenuhi seluruh ketentuan dan memiliki perizinan yang diwajibkan oleh hukum dan ketentuan perundang-undangan. 23.3 Untuk tujuan verifikasi Penjual yang dilakukan oleh Shopee, Penjual wajib dan bertanggung jawab untuk menyerahkan data-data yang

### E3 / shopee-id-terms / 6.2 / PDF 0

6.2. Sehubungan dengan pengoperasian atau proses onboarding sebagai Penjual: (a) Shopee akan meminta calon Penjual untuk memberikan data-data calon Penjual untuk proses verifikasi oleh Shopee. (b) Shopee berhak untuk menilai dan menentukan hasil verifikasi calon Penjual serta memberikan keputusan akhir atas hasil verifikasi data calon Penjual. Calon Penjual dapat memulai menggunakan fitur untuk Pe

### E4 / shopee-id-terms / 6.2 / PDF 0

ikasi data calon Penjual. Calon Penjual dapat memulai menggunakan fitur untuk Penjual setelah hasil verifikasi diberitahukan oleh Shopee kepada Penjual, selambat-lambatnya dalam 2x24 jam setelah data-data diberikan. (c) Khusus bagi Penjual yang telah terdaftar sebagai Penjual sebelum 31 Mei 2024, ketentuan pada ayat (b) di atas akan berlaku bagi Penjual dan Penjual wajib untuk segera memberikan da

### E5 / shopee-id-terms / 6.2 / PDF 0

) di atas akan berlaku bagi Penjual dan Penjual wajib untuk segera memberikan data yang diperlukan oleh Shopee kepada Shopee selambat-lambatnya pada tanggal 1 Juli 2024. Penjual setuju dan memahami bahwa kegagalan untuk menyelesaikan proses verifikasi data dapat membuat Penjual kehilangan akses sementara terhadap beberapa fitur yang tersedia bagi Penjual, termasuk namun tidak terbatas pada kehilan

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-011 — answerable

Menurut Peraturan Komunitas Shopee, bahasa apa yang boleh digunakan dalam informasi pada halaman produk?

必要要点：
- Informasi halaman produk menggunakan bahasa Indonesia atau bahasa Inggris.
- Tidak memperluas aturan halaman produk menjadi izin label kemasan hanya berbahasa Inggris.

必要gold证据完整：True。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Menurut Peraturan Komunitas Shopee Indonesia, informasi pada halaman produk hanya boleh menggunakan Bahasa Indonesia atau Bahasa Inggris; produk yang menggunakan bahasa lain akan dihapus oleh sistem. Ketentuan ini berlaku untuk produk yang dijual di Shopee, namun tanggal publikasi/berlakunya tidak tercantum dalam bukti sehingga perlu verifikasi keberlakuan terkini.",
  "evidence": [
    {
      "claim": "Produk yang dijual di Shopee harus menampilkan informasi yang jelas dan dapat dimengerti, dan hanya boleh menggunakan Bahasa Indonesia atau Bahasa Inggris; sistem akan menghapus produk yang menggunakan bahasa lain.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "Hal yang Dilarang",
      "clause_id": "1",
      "page": 4,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Mohon untuk hanya menggunakan Bahasa Indonesia atau Bahasa Inggris untuk setiap produk yang dijual, karena sistem kami akan menghapus produk yang menggunakan bahasa lain demi kenyamanan pengguna.",
      "evidence_id": "E1"
    },
    {
      "claim": "Halaman produk harus menampilkan foto, nama, dan deskripsi produk yang sesuai dan benar-benar menggambarkan produk yang dijual.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "2",
      "page": 2,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pastikan agar Foto, Nama dan Deskripsi Produk anda sesuai dan benar benar menampilkan produk yang ingin dijual.",
      "evidence_id": "E2"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Bahasa informasi halaman produk hanya Bahasa Indonesia atau Bahasa Inggris",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Berdasarkan Peraturan Komunitas Shopee bagian Hal yang Dilarang angka 1; produk berbahasa lain akan dihapus sistem."
    },
    {
      "item": "Kesesuaian foto, nama, dan deskripsi produk dengan produk yang dijual",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Peraturan Komunitas angka 2."
    },
    {
      "item": "Keberlakuan terkini peraturan (tanggal publikasi/efektif)",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Bukti tidak mencantumkan tanggal publikasi maupun tanggal efektif."
    }
  ],
  "unknowns": [
    "Tanggal publikasi dan tanggal efektif Peraturan Komunitas Shopee tidak tercantum dalam bukti (published_at/effective_from unknown).",
    "Tidak ada bukti mengenai ketentuan bahasa untuk konten non-teks seperti gambar atau video pada halaman produk.",
    "Tidak ada bukti mengenai prosedur banding atau pemulihan produk yang dihapus karena penggunaan bahasa lain."
  ],
  "follow_up_questions": [
    "Apakah Anda ingin memeriksa ketentuan bahasa untuk elemen selain teks (misalnya teks dalam gambar/video) pada halaman produk?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-community / 4 / PDF 0

ng jelas Hal yang Dilarang 1. Melanggar Ketentuan Umum Produk Shopee Produk yang dijual di Shopee harus menampilkan informasi yang jelas dan dapat dimengerti. Mohon untuk hanya menggunakan Bahasa Indonesia atau Bahasa Inggris untuk setiap produk yang dijual, karena sistem kami akan menghapus produk yang menggunakan bahasa lain demi kenyamanan pengguna. Kami juga akan membatasi jenis produk yang da

### E2 / shopee-id-community / 2 / PDF 0

2. Nama dan rincian produk tidak relevan Kami ingin seluruh pengguna Shopee mendapatkan informasi yang relevan ketika membuka sebuah halaman produk. Pastikan agar Foto, Nama dan Deskripsi Produk anda sesuai dan benar benar menampilkan produk yang ingin dijual. Setiap halaman produk hanya dapat digunakan untuk menjual satu jenis benda dan satu merk saja, kecuali jika produk yang dijual memang merup

### E3 / ecommerce-19-2026 / Pasal 40 ayat (2) / PDF 21

(2) Informasi sebagaimana dimaksud pada ayat (1) disampaikan pada halaman yang mudah diakses oleh Pedagang.

### E4 / shopee-id-community / p0 / PDF 0

Peraturan Komunitas | Pusat Bantuan Shopee ID Hai, ada yang bisa kami bantu? Peraturan Komunitas Kami bertujuan membangun komunitas yang bersahabat dan positif di Shopee. Oleh karena itu kami membuat Peraturan Komunitas sebagai petunjuk bagi semua pembeli dan penjual agar tetap terjaga lingkungan online yang aman dan menyenangkan dalam kegiatan transaksi. Melalui petunjuk ini Anda dapat mengetahui

### E5 / shopee-id-community / 6 / PDF 0

6. Menggunakan halaman produk lama untuk mengunggah produk baru Halaman produk yang sudah memiliki penilaian dilarang keras digunakan untuk menjual produk yang berbeda. Berikut contoh dari penyalahgunaan halaman produk: Produk yang pertama dijual adalah sepatu wanita dengan banyak penilaian dari Pembeli. Saat stok sepatu wanita sudah habis atau produk sudah tidak dijual, Penjual mengubah foto, nam

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-mvp-012 — answerable

Apakah penjual boleh menautkan halaman produk di Shopee ke situs web lain?

必要要点：
- Menghubungkan halaman produk ke situs web lain termasuk contoh iklan yang dilarang.

必要gold证据完整：True。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "Tidak, penjual tidak boleh menautkan halaman produk di Shopee ke situs web lain. Peraturan Komunitas Shopee Indonesia secara eksplisit mencantumkan \"Menghubungkan halaman produk Anda ke situs web yang lain\" sebagai contoh iklan yang dilarang, karena Shopee dirancang untuk transaksi, bukan pemasangan iklan. Perlu dicatat bahwa ketentuan ini bersifat umum dan tanggal berlaku dokumen tidak tercantum dalam bukti.",
  "evidence": [
    {
      "claim": "Shopee dirancang sebagai tempat transaksi antara pembeli dan penjual, bukan platform untuk memasang iklan; semua produk yang didaftarkan harus berupa produk yang ingin dijual.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Shopee dirancang sebagai tempat untuk membantu transaksi antara pembeli dan penjual, bukan platform untuk memasang iklan. Oleh karena itu, semua produk yang Anda daftarkan harus berupa produk yang ingin Anda jual.",
      "evidence_id": "E1"
    },
    {
      "claim": "Menghubungkan halaman produk ke situs web lain secara eksplisit disebut sebagai contoh iklan yang dilarang.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Berikut adalah beberapa contoh dari iklan : Menghubungkan halaman produk Anda ke situs web yang lain.",
      "evidence_id": "E1"
    },
    {
      "claim": "Deskripsi produk atau gambar yang mengarahkan pembeli menghubungi penjual via platform lain (misalnya WhatsApp atau Facebook) juga termasuk contoh iklan yang dilarang; komunikasi difasilitasi melalui fitur Chat & Tawar.",
      "doc_id": "shopee-id-community",
      "source_title": "Shopee Indonesia - Peraturan Komunitas",
      "section_path": "",
      "clause_id": "",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Deskripsi produk atau gambar yang mengarahkan pembeli untuk menghubungi Anda via platform lain seperti Whatsapp atau Facebook dan platform komunikasi lainnya",
      "evidence_id": "E2"
    },
    {
      "claim": "Syarat Layanan mengizinkan pembuatan tautan dari situs web penjual ke Situs Shopee dengan syarat situs web tersebut tidak menyiratkan dukungan atau asosiasi dengan Shopee; ketentuan ini mengatur arah tautan yang berbeda (dari situs eksternal ke Shopee), bukan tautan dari halaman produk Shopee ke situs lain.",
      "doc_id": "shopee-id-terms",
      "source_title": "Shopee Indonesia - Syarat Layanan",
      "section_path": "",
      "clause_id": "3.4",
      "page": 0,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Anda boleh membuat tautan ke Situs dari situs web anda, asalkan situs web anda tidak menyiratkan adanya dukungan oleh atau asosiasi dengan Shopee.",
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "Larangan menautkan halaman produk Shopee ke situs web lain",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Dinyatakan sebagai contoh iklan yang dilarang dalam Peraturan Komunitas; tanggal berlaku tidak tercantum."
    },
    {
      "item": "Larangan mengarahkan pembeli ke platform komunikasi eksternal (WhatsApp, Facebook, dll.)",
      "status": "可确认",
      "basis_doc_ids": [
        "shopee-id-community"
      ],
      "note": "Komunikasi sebaiknya melalui fitur Chat & Tawar."
    },
    {
      "item": "Kewajiban mematuhi pedoman barang dilarang dan dibatasi sebelum pendaftaran barang",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-prohibited-restricted"
      ],
      "note": "Bukti hanya menyebut adanya pedoman dan pembaruan berkala; daftar barang tidak disediakan dalam bukti."
    },
    {
      "item": "Kepatuhan terhadap ketentuan Iklan Berbayar Shopee",
      "status": "需人工复核",
      "basis_doc_ids": [
        "shopee-id-terms"
      ],
      "note": "Pasal 24 hanya menjelaskan jenis layanan iklan berbayar; tidak mengatur secara rinci larangan tautan eksternal."
    }
  ],
  "unknowns": [
    "Tanggal publikasi dan tanggal berlaku (effective_from) Peraturan Komunitas dan Syarat Layanan tidak tercantum dalam bukti, sehingga ketepatan waktu ketentuan tidak dapat dipastikan.",
    "Sanksi atau konsekuensi spesifik atas pelanggaran larangan tautan eksternal tidak dijelaskan dalam bukti.",
    "Prosedur banding atau pengajuan keberatan tidak tercakup dalam bukti.",
    "Rincian daftar barang yang dilarang dan dibatasi tidak disediakan dalam bukti."
  ],
  "follow_up_questions": [
    "Apakah tautan yang dimaksud berada di halaman produk, deskripsi toko, atau materi iklan berbayar?",
    "Apakah tujuan tautan adalah situs web toko sendiri, katalog eksternal, atau platform komunikasi lain?"
  ]
}
```

实际输入证据：

### E1 / shopee-id-community / p0 / PDF 0

arankan 1. Berjualan, bukan memasang iklan Shopee dirancang sebagai tempat untuk membantu transaksi antara pembeli dan penjual, bukan platform untuk memasang iklan. Oleh karena itu, semua produk yang Anda daftarkan harus berupa produk yang ingin Anda jual. Berikut adalah beberapa contoh dari iklan : Menghubungkan halaman produk Anda ke situs web yang lain. Deskripsi produk atau gambar yang mengara

### E2 / shopee-id-community / p0 / PDF 0

an produk Anda ke situs web yang lain. Deskripsi produk atau gambar yang mengarahkan pembeli untuk menghubungi Anda via platform lain seperti Whatsapp atau Facebook dan platform komunikasi lainnya (Kami mengerti pentingnya komunikasi antara pembeli dan penjual. Oleh karena itu, Shopee telah menyediakan fitur Chat & Tawar untuk memfasilitasi hal tersebut).

### E3 / shopee-id-terms / 24 / PDF 0

24. IKLAN SHOPEE 24.1. Shopee menawarkan layanan Iklan seperti Iklan Produk, Iklan Produk Baru, Iklan Toko, Iklan Banner Max, Iklan Banner Halaman Pencarian,Iklan Live, Iklan Video, dan layanan solusi pemasaran (marketing solutions) selanjutnya disebut bersama-sama sebagai "Iklan Berbayar") di Situs Iklan Berbayar nya dan situs lain secara berkelanjutan. Penjual dapat membeli layanan Iklan Berbaya

### E4 / shopee-id-prohibited-restricted / p0 / PDF 0

tuan dan kebijakan Shopee sebelum pendaftaran barang pada platform penjualan. Untuk kenyamanan Penjual, di bawah ini Shopee telah menyediakan pedoman singkat tentang barang yang dilarang dan dibatasi yang tidak boleh dijual di Shopee. Shopee akan memperbarui pedoman ini dari waktu ke waktu bila diperlukan. Silakan kunjungi halaman ini secara teratur untuk melihat pembaruan.

### E5 / shopee-id-terms / 3.4 / PDF 0

3.4. Anda boleh membuat tautan ke Situs dari situs web anda, asalkan situs web anda tidak menyiratkan adanya dukungan oleh atau asosiasi dengan Shopee. Anda mengakui bahwa atas kebijakannya sendiri dan setiap saat Shopee dapat berhenti menyediakan Layanan, baik sebagian atau secara keseluruhan, tanpa pemberitahuan. 4. PERANGKAT LUNAK Setiap perangkat lunak yang disediakan oleh kami kepada anda seb

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。

## q-zh-001 — answerable

印尼 PMSE 法规对 PPMSE 和不属于豁免范围的中介服务提供者（PSP）有什么营业许可要求？

必要要点：
- PPMSE dan PSP yang tidak dikecualikan wajib memiliki Perizinan Berusaha Bidang PMSE.
- Pengecualian PSP mengikuti Pasal 4 ayat (3); kewajiban ini tidak otomatis berlaku sama untuk setiap penjual.

必要gold证据完整：False。None表示本题无gold证据要求。

生成答案：

```json
{
  "verdict": "谨慎",
  "summary": "根据 Permendag No. 19 Tahun 2026，未被豁免的 PPMSE 和 PSP 必须持有 PMSE 领域的营业许可（Perizinan Berusaha Bidang PMSE）；申请须通过 OSS 机构向贸易部长提出，许可在经营者持续开展经营活动期间有效。拥有自有 PMSE 设施的国内商家也属于 PPMSE，同样须持有该许可。已持证者将在贸易部网站专门页面公示。",
  "evidence": [
    {
      "claim": "未被豁免的 PPMSE 和 PSP 必须持有 PMSE 领域营业许可。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 7 ayat (1)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "PPMSE dan PSP yang tidak dikecualikan ... wajib memiliki Perizinan Berusaha Bidang PMSE.",
      "evidence_id": "E1"
    },
    {
      "claim": "申请 PMSE 营业许可须通过 OSS 机构向贸易部长提出。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 8 ayat (1)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "... mengajukan permohonan kepada Menteri melalui Lembaga OSS.",
      "evidence_id": "E2"
    },
    {
      "claim": "PMSE 营业许可在 PPMSE/PSP 持续开展经营活动期间有效。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 8 ayat (4)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Perizinan Berusaha Bidang PMSE berlaku selama ... menjalankan kegiatan usaha dan/atau kegiatannya.",
      "evidence_id": "E3"
    },
    {
      "claim": "拥有自有 PMSE 设施的国内商家属于 PPMSE，须持有 PMSE 营业许可。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Ketiga PPMSE dan PSP yang Tidak Dikecualikan > Paragraf Kesatu Perizinan Berusaha",
      "clause_id": "Pasal 7 ayat (3)",
      "page": 9,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "Pedagang dalam negeri yang memiliki sarana PMSE sendiri termasuk dalam kategori PPMSE dan wajib memiliki Perizinan Berusaha Bidang PMSE ...",
      "evidence_id": "E4"
    },
    {
      "claim": "已持有 PMSE 营业许可的 PPMSE/PSP 将在贸易部网站专门页面公示。",
      "doc_id": "ecommerce-19-2026",
      "source_title": "Permendag No. 19 Tahun 2026 tentang Penyelenggaraan Usaha Perdagangan melalui Sistem Elektronik",
      "section_path": "Bagian Kedelapan Publikasi Status Perizinan",
      "clause_id": "Pasal 20 ayat (1)",
      "page": 15,
      "published_at": "unknown",
      "effective_from": "unknown",
      "effective_to": "unknown",
      "collected_at": "2026-11-02",
      "quote": "... ditampilkan dalam laman khusus pada situs web Kementerian Perdagangan.",
      "evidence_id": "E5"
    }
  ],
  "compliance_checklist": [
    {
      "item": "确认自身是否属于未被豁免的 PPMSE 或 PSP",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "证据仅指向 Pasal 4 ayat (3) 的豁免条款，但该条款原文未提供，无法自行判定豁免范围。"
    },
    {
      "item": "通过 OSS 机构向贸易部长申请 PMSE 领域营业许可（Perizinan Berusaha Bidang PMSE）",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "依据 Pasal 7 ayat (1) 与 Pasal 8 ayat (1)。"
    },
    {
      "item": "许可持续有效性的维持：在持续经营期间保持许可有效",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "依据 Pasal 8 ayat (4)。"
    },
    {
      "item": "拥有自有 PMSE 设施的国内商家按 PPMSE 办理许可",
      "status": "可确认",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "依据 Pasal 7 ayat (3)。"
    },
    {
      "item": "核实许可公示状态（贸易部网站专门页面）",
      "status": "需人工复核",
      "basis_doc_ids": [
        "ecommerce-19-2026"
      ],
      "note": "证据仅说明公示机制，未提供具体查询入口与核验方式。"
    }
  ],
  "unknowns": [
    "Pasal 4 ayat (3) 关于豁免的具体范围与条件未在证据中提供，无法判断哪些 PPMSE/PSP 属于豁免对象。",
    "该法规的发布日期与生效日期在证据中均为 unknown，无法确认自 assessment_date（2026-11-02）起是否已生效。",
    "申请所需的具体材料、审批时限与流程细则未在证据中提供。",
    "未取得许可的后果、处罚及申诉流程未在证据中提供。"
  ],
  "follow_up_questions": [
    "您的业务属于 PPMSE（如电商平台/自有在线销售渠道）还是 PSP（中介服务提供者）？是否可能落入豁免范围？",
    "您是否已在 OSS 系统注册并持有相关营业许可（NIB 等）？"
  ]
}
```

实际输入证据：

### E1 / ecommerce-19-2026 / Pasal 7 ayat (1) / PDF 9

(1) PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal  4 ayat (3) wajib memiliki Perizinan Berusaha Bidang PMSE.

### E2 / ecommerce-19-2026 / Pasal 8 ayat (1) / PDF 9

(1) Untuk memperoleh Perizinan Berusaha Bidang PMSE, PPMSE dan PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal 7 mengajukan permohonan kepada Menteri melalui Lembaga OSS.

### E3 / ecommerce-19-2026 / Pasal 8 ayat (4) / PDF 9

(4) Perizinan Berusaha Bidang PMSE berlaku selama PPMSE dan PSP yang tidak dikecualikan sebagaimana dimaksud pada ayat (1) menjalankan kegiatan usaha dan/atau kegiatannya.

### E4 / ecommerce-19-2026 / Pasal 7 ayat (3) / PDF 9

(3) Pedagang dalam negeri yang memiliki sarana PMSE sendiri termasuk dalam kategori PPMSE dan wajib memiliki Perizinan Berusaha Bidang PMSE sebagaimana dimaksud pada ayat (1).

### E5 / ecommerce-19-2026 / Pasal 20 ayat (1) / PDF 15

(1) PPMSE dan/atau PSP yang tidak dikecualikan dari ketentuan kewajiban memiliki Perizinan Berusaha sebagaimana dimaksud dalam Pasal 4 ayat (3) yang telah memiliki Perizinan Berusaha Bidang PMSE ditampilkan dalam laman khusus pada situs web Kementerian Perdagangan.

人工评分：未填写。请记录0–2各维度、behavior_ok、具体错误句及理由；无适用引用时citation_support填null。
