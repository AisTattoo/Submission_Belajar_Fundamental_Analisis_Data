# Bike Sharing Analysis Project 🚲

## Project Overview
Proyek ini merupakan analisis data dari dataset **Bike Sharing** untuk mengidentifikasi tren penyewaan sepeda berdasarkan parameter waktu (jam, hari, bulan, tahun) serta kondisi lingkungan (cuaca dan musim). Hasil analisis ini kemudian disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## File Structure
- `dashboard/`: Berisi file dashboard utama (`dashboard.py`) dan dataset hasil pembersihan (`main_data.csv`).
- `data/`: Berisi dataset mentah (`day.csv` dan `hour.csv`).
- `notebook.ipynb`: Dokumentasi lengkap proses Data Wrangling, EDA, hingga Visualisasi.
- `requirements.txt`: Daftar library yang dibutuhkan untuk menjalankan proyek.
- `url.txt`: Tautan menuju dashboard yang sudah dideploy.

## Project Analysis Questions
1. Bagaimana pengaruh musim dan kondisi cuaca terhadap rata-rata jumlah penyewaan sepeda harian?
2. Bagaimana tren pertumbuhan penyewaan sepeda dari tahun 2011 ke 2012 dan bagaimana pola distribusinya pada hari kerja vs hari libur?
3. Bagaimana pola penggunaan sepeda per jam pada hari kerja dibandingkan dengan hari libur/akhir pekan?

## Installation
Untuk menjalankan dashboard secara lokal, ikuti langkah berikut:

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/username-anda/bike-sharing-analysis.git](https://github.com/username-anda/bike-sharing-analysis.git)
   cd bike-sharing-analysis
