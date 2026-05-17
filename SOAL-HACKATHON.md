# Soal Hackathon DQLab Retail Crisis and Recovery

Converted from: `tasks/SOAL-HACKATHON.pdf`

## Daftar Isi

- Hackathon Python DQLab x UjiKompetensi
- Apa yang Perlu Dibuat dan Dikirimkan?
- Dataset yang Disediakan
- Output yang Diharapkan dari Script `solusi-retail.py`
- Kondisi untuk Menghasilkan Rising Star
- Kondisi untuk Menghasilkan Potential Packaging
- Spesifikasi Visualisasi Rising Star
- Versi Python dan Library yang Boleh Digunakan

## Hackathon Python DQLab x UjiKompetensi

DQFresh Mart Retail adalah sebuah toko retail atau mini mart dengan satu cabang saja.

Selama bertahun-tahun, perusahaan sangat sukses dalam penjualan dengan produk-produk andalan tradisional. Namun dalam 6 bulan terakhir, manajemen mulai menghadapi masalah serius: total nilai penjualan terus menurun. Secara kasat mata memang jumlah pengunjung terlihat turun.

Manajer toko awalnya menganggap kondisi ini hanya akibat pelemahan ekonomi. Karena itu strategi awal toko adalah:

- mempertahankan produk bestseller
- mengurangi eksperimen produk baru
- memperbesar stok produk historis terbaik
- menekan risiko inventory

Tetapi setelah beberapa saat, Sophia sebagai manajer toko mulai merasa ada sesuatu yang tidak sesuai. Sophia kemudian melakukan investigasi sendiri dengan menganalisis data internal toko:

- data transaksi penjualan
- data stock harian

Saat melakukan analisis lebih dalam, ia menemukan pola yang tidak terlihat di dashboard utama toko. Beberapa SKU yang tidak terlihat ternyata menunjukkan pertumbuhan penjualan yang konsisten.

Namun karena kontribusi revenue totalnya masih kecil, sistem tetap menganggap produk-produk tersebut sebagai produk yang tidak perlu diperhatikan. SKU tersebut juga luput dari perhatian kasir ketika diinterview, karena sering habis stoknya.

Dari penemuan ini, Sophia membuat keputusan untuk memperbaiki keadaan tersebut dengan:

- menambah stok dari produk yang ada
- membuat paket produk tersebut bersama produk lain yang secara historis sering dibeli barengan

Peserta diharapkan secara teknis menghasilkan analisis yang sama dengan Sophia dengan script Python, dengan detail yang dijelaskan pada bagian berikut ini. Untuk hackathon ini, data stock harian tidak disertakan.

## Apa yang Perlu Dibuat dan Dikirimkan?

Peserta perlu mengirimkan satu script Python dengan nama `solusi-retail.py` yang ketika dijalankan dengan command berikut:

```bash
python solusi-retail.py
```

akan menghasilkan tiga file pada working folder ketika script dijalankan:

- `retail_insight.xlsx`
- `rising_star_index.png`
- `rising_star_actual.png`

Script tersebut dikirimkan dalam bentuk email dengan nama subjek:

```text
Solusi hackathon untuk soal 'HACK-2026-PYTHON-01'
```

Dan hanya satu script yang boleh dikirimkan bersama email tersebut dalam bentuk attachment. File lain, termasuk ketiga file hasil output, tidak boleh disertakan dalam email.

## Dataset yang Disediakan

Peserta akan menerima beberapa file dataset yang metadatanya sama dengan yang diolah oleh Sophia, yaitu:

### 1. Sales Transaction Data

Nama file: `sales_transaction.csv`

Untuk hackathon kali ini, tidak ada yang perlu dicleansing dari dataset ini, dan untuk penyederhanaan kasus maka periode datanya hanya 30 hari.

Kolom dataset:

- `nomor_struk`: nomor struk atau invoice dari transaksi yang dilakukan
- `tgl_transaksi`: tanggal transaksi dilakukan
- `kode_produk`: kode produk yang dijual
- `nama_produk`: nama produk yang dijual
- `jumlah_terjual`: jumlah atau qty produk yang dijual
- `harga`: harga satuan produk
- `total_nilai`: total nilai penjualan dari harga dikalikan jumlah terjual

## Output yang Diharapkan dari Script `solusi-retail.py`

### File Excel

File Excel bernama `retail_insight.xlsx` harus berisi dua tab berikut:

- `Rising Star`: produk yang tidak kasat mata secara agregasi tradisional, tetapi memiliki moving average yang naik terus
- `Potential Packaging`: kombinasi produk dalam bentuk frequent itemset yang dihasilkan oleh algoritma apriori

Contoh layout dan beberapa baris hasil diberikan dalam file:

- `retail_insight_example.xlsx`

## Kondisi untuk Menghasilkan Rising Star

Gunakan library `pandas` dan `matplotlib` untuk mengolah data dengan ketentuan teknis berikut.

### A. Penghalusan Data atau Smoothing

- Hitung nilai Moving Average (MA) dari total nilai penjualan dengan window waktu 3 hari untuk setiap produk guna meminimalkan fluktuasi harian yang ekstrem.

### B. Identifikasi Tren Naik atau Rising Trend

- Sebuah produk dinyatakan dalam sesi tren naik jika nilai MA hari ini lebih tinggi dari MA hari sebelumnya.
- Hitung berapa hari kenaikan tersebut terjadi secara berurutan atau consecutive days.

### C. Kriteria Filter

- Tampilkan hanya produk yang pernah mengalami tren kenaikan konsisten minimal selama 12 hari berturut-turut.

### D. Perhitungan Pertumbuhan atau Growth %

- Hitung persentase pertumbuhan menggunakan metode titik akhir versus titik awal pada sesi tren tersebut.

Contoh output data pertama untuk rising star diberikan di file contoh Excel.

## Kondisi untuk Menghasilkan Potential Packaging

Pada sheet `Potential Packaging`, hasil yang diminta adalah kombinasi produk yang sering dibeli secara bersamaan oleh pelanggan agar dapat digunakan untuk strategi bundling produk, promo paket, cross selling, dan lain-lain.

Untuk hackathon ini, Anda diharuskan menggunakan algoritma Apriori dari package `mlxtend`.

Berikut kondisi filtering yang harus digunakan untuk mendapatkan frequent itemset yang sesuai dengan penemuan Sophia:

- Minimal support adalah `0.01` atau `1%` dari total transaksi yang akan diproses.
- Bentuk association rules dengan `metric='lift'` dan `min_threshold=1`.
- Tidak semua rules ditampilkan. Hanya rules yang memenuhi syarat berikut yang boleh masuk hasil akhir:
  - Salah satu produk dalam rule harus termasuk dalam produk Rising Star, baik pada `antecedents` maupun `consequents`.
  - Nilai `lift` minimal `2`.
- Hasil akhir harus diurutkan dari yang paling tinggi dengan hirarki berikut:
  - `Lift`
  - `Support`
  - `Confidence`

Beberapa contoh output data pertama dari kondisi filtering di atas diberikan dalam file contoh Excel.

## Spesifikasi Visualisasi Rising Star

Terdapat dua tipe visualisasi terhadap data rising star.

### 1. Visualisasi Pertumbuhan Relatif atau Index / Normalisasi

Buat grafik garis atau line chart untuk seluruh produk rising star seperti kriteria di atas dan bandingkan dengan top 3 produk dengan ketentuan:

1. Normalisasi base 100: transformasikan nilai MA setiap produk sehingga semua garis dimulai dari titik 100 pada awal periode pengamatan.
2. Sumbu Y: `Indeks Pertumbuhan (Base 100)`.
3. Sumbu X: `Tanggal`.
4. Legend: menampilkan nama produk untuk seluruh produk.

Contoh gambar output diberikan dalam file:

- `rising_star_index_incomplete.png`

Tugas peserta adalah melengkapi visualisasi ini.

### 2. Visualisasi Pertumbuhan dengan Nilai Aktual

Anda juga perlu menghasilkan grafik yang menunjukkan nilai sebenarnya selain indeks pertumbuhan.

Contoh untuk tiga top product sales dengan top 1 rising star product diberikan dalam file:

- `rising_star_actual_incomplete.png`

Untuk membantu, diberikan juga file:

- `snippet_code_matplotlib.py`

File tersebut merupakan potongan kode untuk dianalisis yang digunakan untuk menghasilkan grafik, tetapi tidak bisa dijalankan mandiri karena hanya berupa snippet.

Grafik yang dihasilkan harus persis atau sangat mendekati dari sisi:

- warna
- dimensi
- style

## Versi Python dan Library yang Boleh Digunakan

1. Python versi `3.10` sampai `3.14`
2. `matplotlib` versi `3.10.7`
3. `pandas` versi `2.3.1`
4. `mlxtend` versi `0.23.4`
5. `openpyxl` versi `3.1.5`