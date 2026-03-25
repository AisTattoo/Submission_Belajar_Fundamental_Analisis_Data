import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# --- Helper Functions ---
def create_daily_rent_df(df):
    return df.resample(rule='D', on='dteday').agg({"cnt": "sum"}).reset_index()

def create_byseason_df(df):
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    
    df = df.copy()
    if df['season'].dtype != 'object':  
        df['season_label'] = df['season'].map(season_map)
    else:
        df['season_label'] = df['season']
    
    return df.groupby("season_label")["cnt"].mean().reset_index()

def create_byweather_df(df):
    weather_map = {
        1: "Clear/Partly Cloudy",
        2: "Misty/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow"
    }

    df = df.copy()
    if df['weathersit'].dtype != 'object':
        df['weather_label'] = df['weathersit'].map(weather_map)
    else:
        df['weather_label'] = df['weathersit']

    return df.groupby("weather_label")["cnt"].mean().reset_index()

def create_hourly_pattern_df(df):
    return df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()

# --- Load Data ---
main_df_raw = pd.read_csv("dashboard/main_data.csv")
main_df_raw['dteday'] = pd.to_datetime(main_df_raw['dteday'])

hour_df_raw = pd.read_csv("data/hour.csv")
hour_df_raw['dteday'] = pd.to_datetime(hour_df_raw['dteday'])

# --- Sidebar ---
min_date = main_df_raw["dteday"].min()
max_date = main_df_raw["dteday"].max()

with st.sidebar:
    st.title("🚲 Bike Sharing Dashboard")
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter
main_df = main_df_raw[
    (main_df_raw["dteday"] >= pd.to_datetime(start_date)) &
    (main_df_raw["dteday"] <= pd.to_datetime(end_date))
]

hour_df = hour_df_raw[
    (hour_df_raw["dteday"] >= pd.to_datetime(start_date)) &
    (hour_df_raw["dteday"] <= pd.to_datetime(end_date))
]

# Dataframe siap pakai
daily_rent_df = create_daily_rent_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)
hourly_pattern_df = create_hourly_pattern_df(hour_df)

# --- HEADER ---
st.title("📊 Bike Sharing Data Analysis Dashboard")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{main_df.cnt.sum():,}")
col2.metric("Casual Users", f"{main_df.casual.sum():,}")
col3.metric("Registered Users", f"{main_df.registered.sum():,}")

st.markdown("---")

# =========================================================
# 📈 VISUAL 1: MUSIM & CUACA
# =========================================================
st.header("🌦️ Pengaruh Musim & Cuaca")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.barplot(x="season", y="cnt", data=main_df, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Penyewaan per Musim")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    sns.barplot(x="weathersit", y="cnt", data=main_df, palette="coolwarm", ax=ax)
    ax.set_title("Rata-rata Penyewaan berdasarkan Cuaca")
    plt.xticks(rotation=30)
    st.pyplot(fig)

# INSIGHT
st.markdown("""
### 📌 Insight
- **Fall & Summer** memiliki penyewaan tertinggi → cuaca ideal untuk bersepeda  
- **Spring terendah** → kemungkinan cuaca transisi  
- Cuaca **cerah (Clear)** sangat meningkatkan penyewaan  
- Cuaca buruk (hujan/salju) menurunkan minat secara drastis  

💡 **Strategi:** Fokus armada di musim ramai & cuaca cerah
""")

st.markdown("---")

# =========================================================
# 📈 VISUAL 2: TREND BULANAN
# =========================================================
st.header("📈 Tren Penyewaan Tahunan")

main_df['year'] = main_df['dteday'].dt.year
main_df['month'] = main_df['dteday'].dt.month

monthly = main_df.groupby(["year", "month"])["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(12,5))
sns.lineplot(data=monthly, x="month", y="cnt", hue="year", marker="o", ax=ax)
ax.set_title("Tren Penyewaan (2011 vs 2012)")
st.pyplot(fig)

# INSIGHT
st.markdown("""
### 📌 Insight
- Tahun **2012 jauh lebih tinggi** dari 2011 → pertumbuhan signifikan  
- Pola musiman:
  - Naik: Maret  
  - Puncak: Juni–September  
  - Turun: Akhir tahun  

💡 **Strategi:** Siapkan armada sebelum mid-year peak
""")

st.markdown("---")

# =========================================================
# 📈 VISUAL 3: WORKING DAY VS HOLIDAY
# =========================================================
st.header("📦 Distribusi Hari Kerja vs Libur")

fig, ax = plt.subplots()
sns.boxplot(x="workingday", y="cnt", data=main_df, palette="pastel", ax=ax)
ax.set_xticklabels(["Holiday/Weekend", "Working Day"])
st.pyplot(fig)

st.markdown("""
### 📌 Insight
- Hari kerja memiliki **median lebih tinggi**
- Lebih stabil dibanding hari libur  

💡 **Artinya:** penggunaan didominasi aktivitas komuter
""")

st.markdown("---")

# =========================================================
# 📈 VISUAL 4: POLA JAM (BIMODAL)
# =========================================================
st.header("⏰ Pola Penyewaan per Jam")

fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(
    data=hourly_pattern_df,
    x="hr",
    y="cnt",
    hue="workingday",
    marker="o",
    ax=ax
)

ax.set_xticks(range(24))
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.legend(labels=["Holiday/Weekend", "Working Day"])
st.pyplot(fig)

# INSIGHT
st.markdown("""
### 📌 Insight
- **Hari kerja → bimodal (08:00 & 17:00)** → pola komuter  
- **Hari libur → satu puncak siang (12–15)** → rekreasi  
- Siang weekend > weekday → potensi market leisure  

💡 **Strategi:**
- Pagi: fokus area pemukiman  
- Sore: fokus area kantor  
- Siang weekend: boost promosi 🚀
""")

st.markdown("---")

# FOOTER
st.caption("🚀 Muhammad Adil Imamul Haq Mubarak | Submission Dicoding 2026")