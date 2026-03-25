import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='darkgrid')

# --- Helper Functions ---
def create_monthly_trend_df(df):
    df_trend = df.copy()
    df_trend['year'] = df_trend['dteday'].dt.year
    df_trend['month'] = df_trend['dteday'].dt.month
    return df_trend.groupby(["year", "month"])["cnt"].sum().reset_index()

def create_byseason_df(df):
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df_season = df.copy()
    df_season['season_label'] = df_season['season'].map(season_map)
    return df_season.groupby("season_label")["cnt"].sum().reset_index()

def create_hourly_pattern_df(df):
    return df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()

# Fungsi Analisis Lanjutan (Binning Permintaan Harian)
def create_demand_category_df(df):
    df_bin = df.copy()
    bins = [0, 2500, 5500, float('inf')]
    labels = ['Low Demand', 'Medium Demand', 'High Demand']
    df_bin['demand_category'] = pd.cut(df_bin['cnt'], bins=bins, labels=labels)
    # Menghitung jumlah hari untuk masing-masing kategori
    return df_bin.groupby('demand_category')['cnt'].count().reset_index(name='jumlah_hari')

# --- Load Data ---
main_df_raw = pd.read_csv("dashboard/main_data.csv")
main_df_raw['dteday'] = pd.to_datetime(main_df_raw['dteday'])

hour_df_raw = pd.read_csv("data/hour.csv")
hour_df_raw['dteday'] = pd.to_datetime(hour_df_raw['dteday'])

# --- Sidebar & Filter ---
min_date = main_df_raw["dteday"].min()
max_date = main_df_raw["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Bike Sharing App")
    
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data
main_df = main_df_raw[
    (main_df_raw["dteday"] >= pd.to_datetime(start_date)) &
    (main_df_raw["dteday"] <= pd.to_datetime(end_date))
]

hour_df = hour_df_raw[
    (hour_df_raw["dteday"] >= pd.to_datetime(start_date)) &
    (hour_df_raw["dteday"] <= pd.to_datetime(end_date))
]

# Siapkan Dataframe
monthly_trend_df = create_monthly_trend_df(main_df)
byseason_df = create_byseason_df(main_df)
hourly_pattern_df = create_hourly_pattern_df(hour_df)
demand_category_df = create_demand_category_df(main_df) # Menggunakan main_df (data harian)

# --- HEADER & METRICS ---
st.title("📊 Bike Sharing Data Analysis Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{main_df.cnt.sum():,}")
col2.metric("Pengguna Casual", f"{main_df.casual.sum():,}")
col3.metric("Pengguna Terdaftar", f"{main_df.registered.sum():,}")

st.markdown("---")

# =========================================================
# PERTANYAAN 1: TREN BULANAN 2011 VS 2012
# =========================================================
st.subheader("1. Tren Penyewaan Sepeda (2011 vs 2012)")

fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=monthly_trend_df, x="month", y="cnt", hue="year", 
    marker="o", palette={2011: '#B0BEC5', 2012: '#1E88E5'}, ax=ax1
)
ax1.set_title("Jumlah Total Penyewaan Sepeda per Bulan", fontsize=14)
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agt','Sep','Okt','Nov','Des'])
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Total Penyewaan")
ax1.legend(title="Tahun", labels=['2011', '2012'])
st.pyplot(fig1)

with st.expander("📌 Lihat Insight: Tren Bulanan"):
    st.write("- **Pertumbuhan:** Terjadi peningkatan signifikan pada tahun 2012 dibandingkan 2011.\n- **Pola:** Terdapat tren musiman di mana penyewaan memuncak di pertengahan tahun (Juni-September) dan menurun di akhir tahun.")

st.markdown("---")

# =========================================================
# PERTANYAAN 2: PENGARUH MUSIM & CUACA
# =========================================================
st.subheader("2. Rata-rata Penyewaan Berdasarkan Musim & Cuaca")

fig2, ax = plt.subplots(1, 2, figsize=(16, 6))

# --- Visualisasi Musim ---
# Highlight index 2 (Fall) dengan warna biru
colors_season = ["#D3D3D3", "#D3D3D3", "#1E88E5", "#D3D3D3"]

# Gunakan main_df agar mengikuti filter sidebar
sns.barplot(x='season', y='cnt', data=main_df, ax=ax[0], palette=colors_season, errorbar=None)
ax[0].set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim', fontsize=14)
ax[0].set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
ax[0].set_xlabel('Musim')
ax[0].set_ylabel('Rata-rata Penyewaan')

# --- Visualisasi Cuaca ---
# Cuaca 1 (Clear) adalah yang tertinggi, sisanya abu-abu
# Ambil jumlah unik cuaca dari data yang difilter agar tidak error index
num_weather = main_df['weathersit'].nunique()
colors_weather = ["#1E88E5", "#D3D3D3", "#D3D3D3", "#D3D3D3"][:num_weather]

sns.barplot(x='weathersit', y='cnt', data=main_df, ax=ax[1], palette=colors_weather, errorbar=None)
ax[1].set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=14)

# Mengganti label angka menjadi teks cuaca
labels_weather = ['Clear', 'Misty', 'Light Rain/Snow', 'Heavy Rain']
ax[1].set_xticklabels(labels_weather[:num_weather])
ax[1].set_xlabel('Kondisi Cuaca')
ax[1].set_ylabel('Rata-rata Penyewaan')

plt.tight_layout()
st.pyplot(fig2)

with st.expander("📌 Lihat Insight: Musim & Cuaca"):
    st.write("""
    - **Musim:** Rata-rata penyewaan sepeda mencapai angka tertinggi pada **Musim Gugur (Fall)**. Suhu yang sejuk sangat ideal untuk aktivitas luar ruangan dibandingkan musim semi (Spring) yang menjadi titik terendah.
    - **Cuaca:** Pengguna sangat menyukai cuaca **Cerah/Sedikit Berawan (Clear)**. Saat cuaca memburuk menjadi hujan atau salju, rata-rata penyewaan menurun secara drastis.
    """)

st.markdown("---")

# =========================================================
# PERTANYAAN 3: POLA JAM (HARI KERJA VS LIBUR)
# =========================================================
st.subheader("3. Pola Penyewaan per Jam (Hari Kerja vs Libur)")

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hourly_pattern_df, x="hr", y="cnt", hue="workingday", 
    marker="o", palette={0: '#FF9800', 1: '#1E88E5'}, ax=ax3
)
ax3.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
ax3.set_xticks(range(24))
ax3.set_xlabel("Jam (0-23)")
ax3.set_ylabel("Rata-rata Penyewaan")
handles, labels = ax3.get_legend_handles_labels()
ax3.legend(handles=handles, labels=["Libur/Akhir Pekan", "Hari Kerja"], title="Tipe Hari")
st.pyplot(fig3)

with st.expander("📌 Lihat Insight: Pola Waktu"):
    st.write("- **Hari Kerja:** Pola *bimodal* dengan lonjakan pada jam komuter (08:00 dan 17:00).\n- **Hari Libur:** Pola *unimodal* di mana penggunaan menumpuk di siang hari (12:00 - 15:00) untuk rekreasi.")

st.markdown("---")

# =========================================================
# ANALISIS LANJUTAN: BINNING KATEGORI PERMINTAAN
# =========================================================
st.subheader("🔍 Analisis Lanjutan: Pengelompokan Tingkat Permintaan")
st.markdown("Data harian dikelompokkan ke dalam 3 kategori permintaan (Demand) berdasarkan jumlah penyewaan: **Low** (< 2500), **Medium** (2500 - 5500), dan **High** (> 5500).")

fig4, ax4 = plt.subplots(figsize=(10, 5))
colors_bin = ["#D3D3D3", "#1E88E5", "#D3D3D3"] 
sns.barplot(
    x="demand_category", y="jumlah_hari", 
    data=demand_category_df, 
    palette=colors_bin, ax=ax4
)
ax4.set_title("Distribusi Kategori Permintaan Sepeda Harian", fontsize=14)
ax4.set_xlabel("Kategori Permintaan")
ax4.set_ylabel("Jumlah Hari")
st.pyplot(fig4)

with st.expander("📌 Lihat Insight: Analisis Lanjutan"):
    st.write("Sebagian besar hari operasional berada pada kategori **Medium Demand** (2500 hingga 5500 penyewaan). Namun, jumlah hari dengan tingkat **High Demand** (di atas 5500 penyewaan) juga cukup banyak, membuktikan bahwa tren bersepeda cukup kuat dan menjanjikan, terutama saat cuaca dan musim sedang mendukung.")

# --- FOOTER ---
st.caption("Muhammad Adil Imamul Haq Mubarak | Submission Dicoding 2026")