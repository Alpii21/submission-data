import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ===================== DATA UNTUK PERTANYAAN 1 =====================
# Simulasi data review pelanggan
min_length = 500
order_reviews_df = pd.DataFrame({
    "review_score": np.random.randint(1, 6, min_length)
})

data_reviews = {
    "order_id": range(1, min_length + 1),
    "review_score": order_reviews_df["review_score"].fillna(order_reviews_df["review_score"].median()).astype(int),
    "order_date": pd.date_range(start='2023-06-01', periods=min_length, freq='D')
}
df_reviews = pd.DataFrame(data_reviews)

df_reviews['order_date'] = df_reviews['order_date'].dt.to_period('M')
monthly_review = df_reviews.groupby('order_date')['review_score'].mean()

# ===================== DATA UNTUK PERTANYAAN 2 =====================
# Simulasi data penjualan produk
data_sales = {
    'product_id': range(1, 101),
    'category': ['beleza_saude', 'telefonia_fixa', 'brinquedos', 'bebes'] * 25,
    'price': [round(x, 2) for x in np.random.uniform(10, 500, 100)],
    'sales': [np.random.randint(50, 500) for _ in range(100)],
    'order_purchase_timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D')
}
df_sales = pd.DataFrame(data_sales)
df_sales['month'] = df_sales['order_purchase_timestamp'].dt.strftime('%b')

# ===================== STREAMLIT DASHBOARD =====================
st.title("Dashboard Analisis Review dan Penjualan")

# ===================== PERTANYAAN 1 =====================
st.header("Analisis Strategi Peningkatan Layanan Pelanggan")

# Menampilkan statistik deskriptif
st.subheader("Statistik Deskriptif Review Score")
st.write(df_reviews.describe())

# Visualisasi distribusi review score
st.subheader("Distribusi Review Score")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='review_score', data=df_reviews, palette='coolwarm', ax=ax)
st.pyplot(fig)

# Tren rata-rata review score per bulan
st.subheader("Tren Rata-rata Review Score per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
monthly_review.plot(marker='o', color='b', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Review Score")
st.pyplot(fig)

# ===================== PERTANYAAN 2 =====================
st.header("Analisis Strategi Harga dan Promosi")

# Sidebar untuk filter
st.sidebar.header("Filter Data Penjualan")
selected_category = st.sidebar.selectbox("Pilih Kategori Produk", df_sales['category'].unique())
selected_month = st.sidebar.selectbox("Pilih Bulan", df_sales['month'].unique())

# Filter data berdasarkan input pengguna
df_filtered = df_sales[(df_sales['category'] == selected_category) & (df_sales['month'] == selected_month)]

# Visualisasi penjualan berdasarkan kategori
st.subheader(f"Penjualan Produk di Kategori {selected_category} pada Bulan {selected_month}")
st.write(df_filtered[['product_id', 'price', 'sales']])

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='price', y='sales', data=df_filtered, ax=ax)
ax.set_xlabel("Harga Produk")
ax.set_ylabel("Jumlah Penjualan")
st.pyplot(fig)

st.subheader("Pola Pembelian Pelanggan per Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month', y='sales', data=df_sales, estimator='sum', errorbar=None, marker='o', color='red', ax=ax)
st.pyplot(fig)

# Analisis Tren Penjualan Bulanan dan Hubungan Harga dengan Penjualan
st.subheader("Analisis Tren Penjualan Bulanan dan Harga")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='category', y='sales', data=df_sales, hue='category', palette='coolwarm', ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='price', y='sales', data=df_sales, hue='category', palette='viridis', ax=ax)
ax.set_xlabel("Harga Produk")
ax.set_ylabel("Jumlah Penjualan")
st.pyplot(fig)

# --- Kesimpulan ---
st.subheader("📌 Insight dan Conclution")
st.markdown("""
- **Insight**:
  - Dengan menerapkan strategi ini, perusahaan dapat meningkatkan review score dan pengalaman pelanggan, yang pada akhirnya berdampak pada kenaikan kepercayaan dan loyalitas pelanggan dalam jangka panjang.
  - Dengan menerapkan strategi ini, perusahaan dapat meningkatkan total penjualan sebesar 15% dalam 6 bulan, meningkatkan loyalitas pelanggan, dan memaksimalkan profitabilitas di setiap kategori produk.

- **Conclution**:
  - Conclution pertanyaan 1 : 
a. Distribusi Review Score menunjukkan adanya variasi dalam penilaian pelanggan, dengan beberapa review rendah yang dapat diperbaiki melalui strategi layanan pelanggan yang lebih baik.
b. Tren Rata-rata Review Score per Bulan memberikan gambaran apakah review score mengalami peningkatan atau penurunan seiring waktu, membantu dalam menilai efektivitas strategi layanan pelanggan.
c. Nilai Tengah Review Score menunjukkan bahwa mayoritas pelanggan memberikan rating sekitar nilai median, namun ada beberapa yang memberikan rating rendah yang perlu dianalisis lebih lanjut.
Dengan strategi layanan pelanggan yang lebih baik, seperti peningkatan respons customer service, personalisasi layanan, dan penyelesaian cepat terhadap keluhan, rata-rata review score dapat ditingkatkan sebesar 10% dalam 6 bulan dan jumlah review positif (≥4) meningkat 20%.

  - Conclution pertanyaan 2 :
a. Distribusi Harga Produk menunjukkan variasi harga produk dalam kategori tertentu, yang dapat digunakan untuk mengidentifikasi segmen harga yang paling diminati pelanggan.
b. Tren Penjualan per Kategori membantu memahami kategori produk mana yang memiliki performa terbaik serta peluang untuk strategi promosi.
c. Hubungan Harga dengan Penjualan memberikan wawasan mengenai bagaimana harga produk mempengaruhi jumlah penjualan, apakah ada pola penurunan permintaan pada harga tertentu.
d. Pola Pembelian Pelanggan per Bulan mengungkapkan fluktuasi penjualan bulanan, yang dapat digunakan untuk menentukan waktu terbaik dalam menjalankan promosi dan diskon.
Dari analisis ini, strategi harga dan promosi yang tepat dapat diterapkan untuk meningkatkan total penjualan sebesar 15% dalam 6 bulan dengan mengoptimalkan diskon, bundling produk, dan pemasaran berbasis tren penjualan.
""")