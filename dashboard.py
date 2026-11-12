import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Dashboard Bike Sharing", page_icon="🚲", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))
BLUE, ORANGE, GREY, RED = "#2E75B6", "#E08A2E", "#BFBFBF", "#C0504D"

# ---------- Load data ----------
day_all = pd.read_csv(os.path.join(BASE, "main_data.csv"), parse_dates=["dteday"])
hour_all = pd.read_csv(os.path.join(BASE, "hour_data.csv"), parse_dates=["dteday"])

# ---------- Filter tanggal ----------
st.sidebar.title("🚲 Bike Sharing")
min_d, max_d = day_all["dteday"].min().date(), day_all["dteday"].max().date()
rentang = st.sidebar.date_input("Rentang tanggal", (min_d, max_d), min_value=min_d, max_value=max_d)

if len(rentang) != 2:
    st.info("Pilih tanggal awal dan akhir.")
    st.stop()

start, end = pd.Timestamp(rentang[0]), pd.Timestamp(rentang[1])
day = day_all[day_all["dteday"].between(start, end)]
hour = hour_all[hour_all["dteday"].between(start, end)]

# ---------- Header & metrik ----------
st.title("Dashboard Analisis Penyewaan Sepeda")
c1, c2, c3 = st.columns(3)
c1.metric("Total penyewaan", f"{day['cnt'].sum():,}")
c2.metric("Rata-rata per hari", f"{day['cnt'].mean():,.0f}")
c3.metric("Pengguna registered", f"{day['registered'].sum() / day['cnt'].sum():.1%}")

# ---------- Pertanyaan 1: pola per jam ----------
st.subheader("Pertanyaan 1: Pola penyewaan per jam (hari kerja vs akhir pekan/libur)")
hourly = hour.groupby(["day_type", "hr"])["cnt"].mean().unstack(0)

fig, ax = plt.subplots(figsize=(11, 4.5))
for tipe, warna in {"Hari Kerja": BLUE, "Akhir Pekan/Libur": ORANGE}.items():
    ax.plot(hourly.index, hourly[tipe], marker="o", color=warna, label=tipe)
ax.set_xticks(range(24))
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata penyewaan per jam")
ax.legend()
st.pyplot(fig)

# ---------- Pertanyaan 2: musim & cuaca ----------
st.subheader("Pertanyaan 2: Pengaruh musim dan cuaca terhadap penyewaan harian")
col1, col2 = st.columns(2)

season = day.groupby("season")["cnt"].mean().reindex(["Spring", "Summer", "Fall", "Winter"])
weather = day.groupby("weathersit")["cnt"].mean().sort_values(ascending=False)

for col, data, judul in [(col1, season, "Per Musim"), (col2, weather, "Per Kondisi Cuaca")]:
    warna = [RED if v == data.min() else BLUE if v == data.max() else GREY for v in data]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(data.index, data.values, color=warna)
    ax.bar_label(ax.containers[0], fmt="%.0f")
    ax.set_title(judul)
    ax.set_ylabel("Rata-rata penyewaan per hari")
    col.pyplot(fig)

# ---------- Analisis lanjutan: binning suhu ----------
st.subheader("Analisis Lanjutan: Penyewaan per kelompok suhu")
day = day.copy()
day["temp_group"] = pd.cut(day["temp"], bins=[-10, 10, 20, 30, 50],
                           labels=["Dingin (<10°C)", "Sejuk (10-20°C)", "Hangat (20-30°C)", "Panas (>30°C)"])
temp = day.groupby("temp_group", observed=True)[["registered", "casual"]].mean()

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(temp.index.astype(str), temp["registered"], color=BLUE, label="Registered")
ax.bar(temp.index.astype(str), temp["casual"], bottom=temp["registered"], color=ORANGE, label="Casual")
ax.set_ylabel("Rata-rata penyewaan per hari")
ax.legend()
st.pyplot(fig)

# ---------- Kesimpulan ----------
st.subheader("Kesimpulan & Rekomendasi")
st.markdown("""
- Hari kerja punya dua puncak (jam 08.00 dan 17.00), akhir pekan memuncak sekitar jam 13.00.
- Musim Fall tertinggi dan Spring terendah; cuaca hujan/salju ringan menurunkan penyewaan paling drastis.
- Penyewaan paling tinggi pada suhu 20-30°C.
- **Rekomendasi:** siapkan sepeda sebelum jam sibuk hari kerja, lakukan perawatan pada dini hari, beri promosi saat Spring dan cuaca mendung.
""")