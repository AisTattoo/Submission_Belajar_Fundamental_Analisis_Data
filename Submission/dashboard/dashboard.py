import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

# Set style seaborn
sns.set(style='dark')

# Helper function untuk menyiapkan berbagai dataframe
def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    return daily_rent_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    return byseason_df

# Load cleaned data
all_df = pd.read_csv("dashboard/main_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Filter Rentang Waktu
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
byseason_df = create_byseason_df(main_df)

# Header
st.header('Bike Sharing Dashboard 🚲')

# Metrik Utama
col1, col2, col3 = st.columns(3)

with col1:
    total_rent = main_df.cnt.sum()
    st.metric("Total Penyewaan", value=total_rent)

with col2:
    total_casual = main_df.casual.sum()
    st.metric("Pengguna Casual", value=total_casual)

with col3:
    total_registered = main_df.registered.sum()
    st.metric("Pengguna Terdaftar", value=total_registered)

# Visualisasi 1: Performa Penyewaan Harian
st.subheader('Daily Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Visualisasi 2: Musim & Cuaca
st.subheader('Penyewaan Berdasarkan Kondisi Lingkungan')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="season", data=byseason_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Penyewaan", fontsize=30)
ax[0].set_title("Berdasarkan Musim", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="cnt", y="weathersit", data=sum_order_items_df, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Penyewaan", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Berdasarkan Kondisi Cuaca", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Footer
st.caption('Muhammad Adil Imamul Haq Mubarak || Belajar Fundamental Analisis Data 2026')