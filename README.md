# 📊 Dashboard Segmentasi Pelanggan LRFM

Dashboard web interaktif untuk memvisualisasikan hasil segmentasi pelanggan berdasarkan perilaku transaksi. Proyek ini menggunakan model **LRFM (Length, Recency, Frequency, Monetary)** dan algoritma **Fuzzy C-Means (FCM) Clustering** untuk mengelompokkan pelanggan ke dalam tiga segmen: **Pelanggan Loyal, Pelanggan Potensial, dan Pelanggan Yang Hilang**.

**Demo Aplikasi:** [Customer Segmentation Dashboard](https://customer-segmentation-dashboard-by-alam.streamlit.app/)

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python
- **Dashboard:** Streamlit
- **Visualisasi Data:** Plotly Express
- **Pengolahan Data:** Pandas
- **Pembacaan File Excel:** OpenPyXL
- **Pengolahan Data dan Clustering:** Google Colab
- **Algoritma Clustering:** Fuzzy C-Means (FCM)

## ✨ Fitur Utama

- **Filter Data Interaktif:** Memfilter data pelanggan melalui sidebar.
- **Indikator Kinerja (KPI):** Menampilkan jumlah pelanggan, total pendapatan, dan rata-rata frekuensi pembelian.
- **Visualisasi Interaktif:** Menampilkan distribusi dan karakteristik segmen melalui grafik interaktif.
- **Tabel Data Pelanggan:** Menelusuri data pelanggan dengan fitur pengurutan dan pratinjau data.
- **Eksplorasi Segmen:** Membantu pengguna memahami distribusi dan karakteristik masing-masing kelompok pelanggan.

## 🔬 Metodologi

### 1. Pembentukan Fitur LRFM

Model LRFM digunakan untuk merepresentasikan perilaku pembelian pelanggan melalui empat dimensi:

- **Length:** Durasi hubungan pelanggan dengan bisnis.
- **Recency:** Jarak waktu sejak transaksi terakhir pelanggan.
- **Frequency:** Frekuensi transaksi yang dilakukan pelanggan.
- **Monetary:** Nilai transaksi pelanggan secara moneter.

Keempat fitur tersebut digunakan sebagai dasar analisis untuk membentuk segmentasi pelanggan.

### 2. Pra-pemrosesan Data

Pra-pemrosesan dilakukan menggunakan Google Colab untuk mempersiapkan data sebelum proses clustering. Tahapan yang dilakukan meliputi:

- **Penanganan Missing Values:** Mengidentifikasi dan menangani nilai yang kosong.
- **Penghapusan Duplikasi:** Menghapus catatan duplikat untuk mengurangi redundansi data.
- **Normalisasi Fitur:** Menyamakan skala fitur agar perbedaan rentang nilai tidak mendominasi proses clustering.

### 3. Fuzzy C-Means Clustering

Algoritma Fuzzy C-Means (FCM) diterapkan di Google Colab untuk mengelompokkan pelanggan berdasarkan karakteristik LRFM.

- **Algoritma:** Fuzzy C-Means (FCM)
- **Jumlah Cluster:** 3
- **Hasil Segmentasi:** Champions, Potential Loyalists, dan Hibernating/Churn

FCM menghitung derajat keanggotaan setiap data terhadap beberapa cluster. Karakteristik LRFM dari cluster yang dihasilkan kemudian dianalisis untuk menentukan label segmen pelanggan.

### 4. Evaluasi Clustering

Dua metode digunakan dalam analisis clustering:

- **Elbow Method:** Membantu menentukan jumlah cluster dengan mengamati perubahan nilai evaluasi seiring bertambahnya jumlah cluster.
- **Silhouette Score:** Mengukur seberapa baik data berada dalam clusternya dibandingkan dengan cluster lainnya.

Hasil evaluasi digunakan untuk mendukung pemilihan jumlah cluster. Analisis karakteristik LRFM selanjutnya digunakan untuk menginterpretasikan setiap cluster menjadi segmen pelanggan.

### 5. Pengembangan Dashboard

Setelah proses pengolahan data dan clustering selesai di Google Colab, dataset beserta hasil segmentasinya digunakan sebagai input untuk dashboard Streamlit.

Dashboard ini berfokus pada visualisasi dan eksplorasi hasil clustering, bukan menjalankan algoritma Fuzzy C-Means secara langsung. Pengguna dapat memfilter data, melihat indikator kinerja, mengeksplorasi grafik, dan menelusuri data pelanggan.

## 🏗️ Arsitektur Proyek

Proyek ini terdiri dari dua komponen utama:

1. **Pengolahan Data:** Google Colab digunakan untuk pembersihan data, pembentukan fitur LRFM, normalisasi, clustering, dan evaluasi hasil.
2. **Visualisasi Data:** Streamlit digunakan untuk menyajikan hasil segmentasi melalui dashboard interaktif.

### Alur Proses

```text
Data Transaksi Pelanggan
          ↓
Pembersihan Data
          ↓
Pembentukan Fitur LRFM
          ↓
Normalisasi Data
          ↓
Fuzzy C-Means Clustering
          ↓
Evaluasi Cluster
(Elbow Method & Silhouette Score)
          ↓
Interpretasi Segmen
          ↓
Dataset Hasil Segmentasi
          ↓
Dashboard Streamlit
```

## 📁 Struktur Repositori

```text
├── app.py                            # Kode utama dashboard Streamlit
├── customer_segmentation_data.csv    # Dataset pelanggan hasil segmentasi
├── requirements.txt                  # Daftar library Python yang dibutuhkan
└── README.md                         # Dokumentasi proyek
```

## ⚙️ Instalasi dan Menjalankan Aplikasi

### 1. Clone repositori

```bash
git clone URL_REPOSITORI_GITHUB
```

### 2. Masuk ke direktori proyek

```bash
cd NAMA_REPOSITORI
```

### 3. Instal dependensi

Pastikan Python sudah terinstal, lalu jalankan:

```bash
pip install -r requirements.txt
```

Perintah tersebut akan menginstal library yang tercantum dalam `requirements.txt`.

### 4. Jalankan dashboard

```bash
python -m streamlit run app.py
```

Setelah aplikasi berjalan, buka alamat lokal yang ditampilkan pada terminal.

## 🎯 Tujuan Proyek

Proyek ini menunjukkan penerapan pengolahan data, teknik clustering, evaluasi hasil segmentasi, dan visualisasi data interaktif untuk memahami perilaku pelanggan.

Hasil segmentasi disajikan dalam dashboard yang membantu pengguna mengeksplorasi karakteristik kelompok pelanggan dan memperoleh wawasan untuk mendukung analisis bisnis berbasis data.
