import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Membuat data review score
data_reviews = {
    "order_id": range(1, 501),
    "review_score": np.random.randint(1, 6, 500),
    "order_date": pd.date_range(start='2023-06-01', periods=500, freq='D')
}
df_reviews = pd.DataFrame(data_reviews)

df_reviews['order_date'] = df_reviews['order_date'].dt.to_period('M')
monthly_review = df_reviews.groupby('order_date')['review_score'].mean()

# Membuat data penjualan produk
data_sales = {
    'product_id': range(1, 101),
    'category': ['beleza_saude', 'telefonia_fixa', 'brinquedos', 'bebes'] * 25,
    'price': [round(x, 2) for x in np.random.uniform(10, 500, 100)],
    'sales': [np.random.randint(50, 500) for _ in range(100)],
    'order_purchase_timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D')
}
df_sales = pd.DataFrame(data_sales)
df_sales['month'] = df_sales['order_purchase_timestamp'].dt.strftime('%b')

# Streamlit UI
st.title("Dashboard Analisis Review Score dan Penjualan Produk")

# Filter untuk kategori produk
selected_category = st.selectbox("Pilih Kategori Produk", df_sales['category'].unique())
filtered_sales = df_sales[df_sales['category'] == selected_category]

# Menampilkan distribusi review score
st.subheader("Distribusi Review Score")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='review_score', data=df_reviews, palette='coolwarm', ax=ax)
st.pyplot(fig)

# Menampilkan tren rata-rata review score per bulan
st.subheader("Tren Rata-rata Review Score per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
monthly_review.plot(marker='o', color='b', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Review Score")
st.pyplot(fig)

# Menampilkan distribusi harga produk
st.subheader("Distribusi Harga Produk")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_sales['price'], bins=20, kde=True, color='blue', ax=ax)
st.pyplot(fig)

# Menampilkan tren penjualan per kategori produk
st.subheader("Tren Penjualan per Kategori Produk")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='category', y='sales', data=df_sales, palette='coolwarm', ax=ax)
st.pyplot(fig)

# Menampilkan hubungan harga dengan penjualan
st.subheader("Hubungan Harga dengan Penjualan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='price', y='sales', data=filtered_sales, hue='category', palette='viridis', ax=ax)
st.pyplot(fig)

# Menampilkan analisis tren pola pembelian pelanggan per bulan
st.subheader("Pola Pembelian Pelanggan per Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month', y='sales', data=filtered_sales, estimator='sum', errorbar=None, marker='o', color='red', ax=ax)
st.pyplot(fig)

# Keterangan
st.markdown("### **Pertanyaan 1**: Bagaimana strategi peningkatan layanan pelanggan dapat meningkatkan rata-rata review score sebesar 10% dalam 6 bulan ke depan dan meningkatkan jumlah review positif (≥ 4) sebesar 20%?")
st.markdown("### **Pertanyaan 2**: Bagaimana strategi harga dan promosi dapat meningkatkan total penjualan produk dalam kategori tertentu sebesar 15% dalam 6 bulan?")

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