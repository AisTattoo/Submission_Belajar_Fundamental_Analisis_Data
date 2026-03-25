# Bike Sharing Data Analysis Dashboard 🚲

## Project Overview
Proyek ini merupakan analisis data dari dataset **Bike Sharing** untuk mengidentifikasi tren penyewaan sepeda berdasarkan parameter waktu (jam, bulan, tahun), kondisi lingkungan (cuaca dan musim), serta menganalisis tingkat permintaan harian (Demand Category). Hasil analisis ini kemudian disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Project Analysis Questions
1. Bagaimana tren jumlah total penyewaan sepeda dari bulan ke bulan pada tahun 2012 dibandingkan dengan tahun 2011?
2. Pada musim apa penyewaan sepeda mencapai angka tertinggi dan terendah selama periode pengamatan (2011-2012)?
3. Bagaimana perbandingan pola rata-rata penyewaan sepeda per jam antara hari kerja (*working day*) dan hari libur (*holiday/weekend*) selama tahun 2011-2012?

## File Structure
- `dashboard/`: Berisi file dashboard utama (`dashboard.py`) dan dataset hasil pembersihan (`main_data.csv`).
- `data/`: Berisi dataset mentah (`day.csv` dan `hour.csv`).
- `Proyek_Analisis_Data.ipynb`: Dokumentasi lengkap proses Data Wrangling, Exploratory Data Analysis (EDA), Analisis Lanjutan (Binning), hingga Visualisasi.
- `requirements.txt`: Daftar versi *library* yang dibutuhkan untuk menjalankan proyek.
- `url.txt`: Tautan menuju dashboard yang sudah di-*deploy* ke Streamlit Cloud.
- `README.md`: Informasi lengkap mengenai proyek dan cara menjalankan *dashboard*.
- `runtime.txt` : Informasi runtime menggunakan python versi 3.10

## Setup Environment & Installation
Untuk menjalankan dashboard secara lokal, ikuti langkah-langkah berikut:

### 1. Clone Repositori
Buka terminal/command prompt, lalu jalankan:
```bash
git clone [https://github.com/username-anda/Submission_Belajar_Fundamental_Analisis_Data.git](https://github.com/username-anda/Submission_Belajar_Fundamental_Analisis_Data.git)
cd bike-sharing-analysis
```
### 2. Setup Virtual Environtment
- Menggunakan Anaconda
```bash
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```
- Menggunakan venv (bawaan python)
```bash
python -m venv venv
```
### 3. Menjalankan Dashboard Streamlit
```bash
cd dashboard
streamlit run dashboard.py
```