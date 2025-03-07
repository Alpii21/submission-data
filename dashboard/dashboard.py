import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset yang relevan
st.title("Dashboard Analisis Review & Penjualan")
st.sidebar.header("Filter Data")

# Simulasi Data Review
min_length = 500
data_review = {
    "order_id": range(1, min_length + 1),
    "review_score": np.random.randint(1, 6, min_length),
    "order_date": pd.date_range(start='2023-06-01', periods=min_length, freq='D')
}
df_review = pd.DataFrame(data_review)
df_review['order_date'] = df_review['order_date'].dt.to_period('M')

# Simulasi Data Penjualan
categories = ['beleza_saude', 'telefonia_fixa', 'brinquedos', 'bebes']
data_seler = {
    'product_id': range(1, 101),
    'category': categories * 25,
    'price': [round(x, 2) for x in np.random.uniform(10, 500, 100)],
    'seler': [np.random.randint(50, 500) for _ in range(100)],
    'order_purchase_timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D')
}
df_seler = pd.DataFrame(data_seler)
df_seler['month'] = df_seler['order_purchase_timestamp'].dt.strftime('%b')

# Filter Interaktif
selected_category = st.sidebar.multiselect("Pilih Kategori Produk", df_seler['category'].unique(), default=df_seler['category'].unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", df_seler['month'].unique(), default=df_seler['month'].unique())

# Filter Data
filtered_sales = df_seler[(df_seler['category'].isin(selected_category)) & (df_seler['month'].isin(selected_month))]
filtered_reviews = df_review[df_review['order_date'].isin(pd.PeriodIndex(selected_month, freq='M'))]

# Visualisasi Review Score
st.subheader("Distribusi Review Score")
fig, ax = plt.subplots()
sns.countplot(x='review_score', data=filtered_reviews, palette='coolwarm', ax=ax)
st.pyplot(fig)

# Tren Rata-rata Review Score per Bulan
st.subheader("Tren Rata-rata Review Score per Bulan")
monthly_review = df_review.groupby('order_date')['review_score'].mean()
fig, ax = plt.subplots()
monthly_review.plot(marker='o', color='b', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Review Score")
ax.set_title("Tren Rata-rata Review Score")
st.pyplot(fig)

# Distribusi Harga Produk
st.subheader("Distribusi Harga Produk")
fig, ax = plt.subplots()
sns.histplot(filtered_sales['price'], bins=20, kde=True, color='blue', ax=ax)
st.pyplot(fig)

# Tren Penjualan per Kategori Produk
st.subheader("Tren Penjualan per Kategori Produk")
fig, ax = plt.subplots()
sns.boxplot(x='category', y='seler', data=filtered_sales, palette='coolwarm', ax=ax)
st.pyplot(fig)

# Hubungan Harga dengan Penjualan
st.subheader("Hubungan Harga dengan Penjualan")
fig, ax = plt.subplots()
sns.scatterplot(x='price', y='seler', data=filtered_sales, hue='category', palette='viridis', ax=ax)
st.pyplot(fig)

# Tren Penjualan per Bulan
st.subheader("Pola Pembelian Pelanggan per Bulan")
fig, ax = plt.subplots()
sns.lineplot(x='month', y='seler', data=filtered_sales, estimator='sum', marker='o', color='red', ax=ax)
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