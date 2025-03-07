import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
st.title("Dashboard Analisis Layanan Pelanggan & Strategi Harga")

# Pertanyaan 1: Analisis Review Score
st.header("Pertanyaan 1: Peningkatan Layanan Pelanggan")
st.write("Bagaimana strategi peningkatan layanan pelanggan dapat meningkatkan rata-rata review score sebesar 10% dalam 6 bulan ke depan dan meningkatkan jumlah review positif (≥ 4) sebesar 20%?")

# Simulasi Data Review Score
min_length = 500
data_reviews = {
    "order_id": range(1, min_length + 1),
    "review_score": np.random.randint(1, 6, min_length),
    "order_date": pd.date_range(start='2023-06-01', periods=min_length, freq='D')
}
df_reviews = pd.DataFrame(data_reviews)

df_reviews['order_date'] = df_reviews['order_date'].dt.to_period('M')
monthly_review = df_reviews.groupby('order_date')['review_score'].mean()

fig, ax = plt.subplots(figsize=(10, 5))
monthly_review.plot(marker='o', color='b', ax=ax)
ax.set_title("Tren Rata-rata Review Score per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Review Score")
ax.grid()
st.pyplot(fig)

# Pertanyaan 2: Analisis Harga & Penjualan
st.header("Pertanyaan 2: Strategi Harga dan Promosi")
st.write("Bagaimana strategi harga dan promosi dapat meningkatkan total penjualan produk dalam kategori tertentu sebesar 15% dalam 6 bulan?")

# Simulasi Data Penjualan
categories = ['beleza_saude', 'telefonia_fixa', 'brinquedos', 'bebes']
data_sales = {
    'product_id': range(1, 101),
    'category': categories * 25,
    'price': np.random.uniform(10, 500, 100),
    'seler': np.random.randint(50, 500, 100),
    'order_purchase_timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D')
}
df_seler = pd.DataFrame(data_sales)
df_seler['month'] = df_seler['order_purchase_timestamp'].dt.strftime('%b')

# Filter Interaktif
selected_category = st.selectbox("Pilih Kategori Produk", categories)
filtered_sales = df_seler[df_seler['category'] == selected_category]

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month', y='seler', data=filtered_sales, estimator='sum', errorbar=None, marker='o', color='red', ax=ax)
ax.set_title("Pola Pembelian Pelanggan per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penjualan")
st.pyplot(fig)

st.write("Dengan strategi diskon, promosi, dan bundling produk, diharapkan penjualan dapat meningkat secara signifikan.")
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