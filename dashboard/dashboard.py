import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency 
sns.set(style='dark')

# Judul Dashboard
st.title("📊 Analisis Pengguna Sepeda")

# Load data
all_data = pd.read_csv("dashboard/all_data.csv")

# Konversi kolom 'dteday' ke format datetime
all_data["dteday"] = pd.to_datetime(all_data["dteday"], errors='coerce')

# Mapping nilai season ke deskripsi
season_mapping = {
    1: "Musim Semi",
    2: "Musim Panas",
    3: "Musim Gugur",
    4: "Musim Dingin"
}
all_data["season"] = all_data["season"].map(season_mapping)

# Mapping nilai weathersit ke deskripsi
weather_mapping = {
    1: "Cerah / Sedikit Berawan",
    2: "Berawan / Kabut",
    3: "Hujan Ringan / Salju Ringan",
    4: "Hujan Lebat / Salju Lebat"
}
all_data["weathersit"] = all_data["weathersit"].map(weather_mapping)

# Mapping nilai workingday ke deskripsi hari kerja atau bukan
workingday_mapping = {
    0: "Bukan Hari Kerja",
    1: "Hari Kerja"
}
all_data["workingday"] = all_data["workingday"].map(workingday_mapping)

# Membuat binning untuk suhu
temp_bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
temp_labels = ['Sangat Dingin', 'Dingin', 'Sedang', 'Hangat', 'Panas']
all_data['temp_category'] = pd.cut(all_data['temp'], bins=temp_bins, labels=temp_labels)
# Menentukan rentang waktu
min_date = all_data["dteday"].min()
max_date = all_data["dteday"].max()

# Sidebar
with st.sidebar:
    st.header("📅 Pilih Rentang Waktu")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Multiselect untuk Season
    season = st.multiselect(
        label="Pilih Musim",
        options=all_data["season"].dropna().unique()
    )
    
    # Multiselect untuk Weather
    weather = st.multiselect(
        label="Pilih Kondisi Cuaca",
        options=all_data["weathersit"].dropna().unique()
    )
    
    # Multiselect untuk Working Day
    workingday = st.multiselect(
        label="Pilih Hari Kerja atau Bukan",
        options=all_data["workingday"].dropna().unique()
    )
    
    # Multiselect untuk Suhu
    temp_category = st.multiselect(
        label="Pilih Kategori Suhu",
        options=all_data["temp_category"].dropna().unique()
    )
# Filter data berdasarkan rentang waktu
filtered_data = all_data[(all_data["dteday"] >= pd.to_datetime(start_date)) &
                         (all_data["dteday"] <= pd.to_datetime(end_date))]

# Filter berdasarkan Season jika dipilih
if season:
    filtered_data = filtered_data[filtered_data["season"].isin(season)]

# Filter berdasarkan Weather jika dipilih
if weather:
    filtered_data = filtered_data[filtered_data["weathersit"].isin(weather)]

# Filter berdasarkan Working Day jika dipilih
if workingday:
    filtered_data = filtered_data[filtered_data["workingday"].isin(workingday)]

# Filter berdasarkan Kategori Suhu jika dipilih
if temp_category:
    filtered_data = filtered_data[filtered_data["temp_category"].isin(temp_category)]
st.write(f"### Menampilkan data dari {start_date} hingga {end_date}:")
st.dataframe(filtered_data)
st.write(f"Jumlah data setelah difilter: {filtered_data.shape[0]} baris")

# Histogram distribusi jumlah penyewaan
st.subheader("📊 Distribusi Penyewaan Sepeda")
x = np.random.normal(filtered_data['cnt'].mean(), filtered_data['cnt'].std(), 250)
fig, ax = plt.subplots()
ax.hist(x, bins=15, color='skyblue', edgecolor='black')
plt.xlabel("Jumlah Penyewaan")
plt.ylabel("Frekuensi")
st.pyplot(fig)

# Visualisasi Data
col1, col2 = st.columns(2)

# Grafik jumlah penyewaan berdasarkan kategori cuaca
with col1:
    st.subheader("📌 Penyewaan Berdasarkan Cuaca")
    plt.figure(figsize=(6, 4))
    weather_counts = filtered_data.groupby("weathersit")["cnt"].sum().reset_index()
    sns.barplot(y="cnt", x="weathersit", data=weather_counts, palette="coolwarm")
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Total Penyewaan")
    plt.xticks(rotation=20)
    st.pyplot(plt)

# Grafik jumlah penyewaan berdasarkan kategori musim
with col2:
    st.subheader("📌 Penyewaan Berdasarkan Musim")
    season_counts = filtered_data.groupby("season")["cnt"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(y="cnt", x="season", data=season_counts, palette="coolwarm", ax=ax)
    plt.xlabel("Musim")
    plt.ylabel("Total Penyewaan")
    st.pyplot(fig)



    # Visualisasi Data
col_1, col_2= st.columns(2)


# Grafik pola pengguna sepeda per jam
with col_1:
    st.subheader("📌 Pola Pengguna Sepeda per Jam Berdasarkan Cuaca")
    hourly_weather = filtered_data.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()
    plt.figure(figsize=(6, 4))
    sns.lineplot(x='hr', y='cnt', hue='weathersit', data=hourly_weather, marker='o', palette='coolwarm')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Rata-rata Jumlah Pengguna')
    plt.xticks(range(0, 24))
    st.pyplot(plt)


# Grafik pola pengguna sepeda per jam
with col_2:
    st.subheader("📌 Pola Pengguna Sepeda per Jam Berdasarkan Musim")
    hourly_season = filtered_data.groupby(['hr', 'season'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(x='hr', y='cnt', hue='season', data=hourly_season, marker='o', palette='coolwarm', ax=ax)
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Rata-rata Jumlah Pengguna')
    plt.xticks(range(0, 24))
    st.pyplot(fig)



# Mengelompokkan data berdasarkan kategori suhu dan hari kerja
temp_grouped_df = filtered_data.groupby(['temp_category', 'workingday']).agg({
    "casual": "sum",
    "registered": "sum"
}).reset_index()

# Mengelompokkan data berdasarkan kategori suhu dan hari kerja
temp_grouped_df = filtered_data.groupby(['temp_category', 'workingday']).agg({
    "casual": "sum",
    "registered": "sum"
}).reset_index()

# Mengelompokkan data berdasarkan kategori suhu dan hari kerja
temp_grouped_df = filtered_data.groupby(['temp_category', 'workingday']).agg({
    "casual": "sum",
    "registered": "sum"
}).reset_index()

# Membuat plot bar dengan setiap kategori memiliki dua batang terpisah
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.2
x = np.arange(len(temp_labels))

for i, (label, group) in enumerate(temp_grouped_df.groupby("workingday")):
    casual_values = group["casual"].values if not group.empty else np.zeros(len(temp_labels))
    registered_values = group["registered"].values if not group.empty else np.zeros(len(temp_labels))
    ax.bar(x - bar_width / 2 + i * bar_width, casual_values, bar_width, label=f'Casual ({label})', alpha=0.7)
    ax.bar(x - bar_width / 2 + i * bar_width, registered_values, bar_width, bottom=casual_values, label=f'Registered ({label})', alpha=0.7)

ax.set_xlabel('Kategori Suhu', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax.set_title('Distribusi Penyewaan Sepeda berdasarkan Suhu dan Hari Kerja', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(temp_labels, fontsize=11)
ax.legend()
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=20)

st.subheader("📌 Distribusi Penyewaan Sepeda berdasarkan Suhu dan Hari Kerja")
st.pyplot(fig)
