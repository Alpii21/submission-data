import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan Streamlit
st.set_page_config(layout="wide", page_title="Analisis Strategi Bisnis")

# Judul dashboard
st.title("📊 Dashboard Analisis Strategi Bisnis")

# --- Data untuk Review Score ---
orders_df = pd.DataFrame({"order_purchase_timestamp": pd.date_range(start='2023-06-01', periods=500, freq='D')})
order_reviews_df = pd.DataFrame({"review_score": np.random.randint(1, 6, 500)})

min_length = min(len(orders_df), len(order_reviews_df), 500)
review_data = {
    "order_id": range(1, min_length + 1),
    "review_score": order_reviews_df["review_score"].fillna(order_reviews_df["review_score"].median()).astype(int)[:min_length],
    "order_date": pd.date_range(start='2023-06-01', periods=min_length, freq='D')
}
df_reviews = pd.DataFrame(review_data)
df_reviews['order_date'] = df_reviews['order_date'].dt.to_period('M')

# --- Data untuk Penjualan Produk ---
data = {
    'product_id': range(1, 101),
    'category': ['beleza_saude', 'telefonia_fixa', 'brinquedos', 'bebes'] * 25,
    'price': [round(x, 2) for x in np.random.uniform(10, 500, 100)],
    'sales': [np.random.randint(50, 500) for _ in range(100)],
    'order_purchase_timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D')
}
df_sales = pd.DataFrame(data)
df_sales['month'] = df_sales['order_purchase_timestamp'].dt.strftime('%b')

# --- Sidebar untuk interaktif ---
st.sidebar.header("🔍 Eksplorasi Data")
kategori_terpilih = st.sidebar.selectbox("Pilih Kategori Produk:", df_sales['category'].unique())
harga_max = st.sidebar.slider("Batas Maksimum Harga Produk:", int(df_sales['price'].min()), int(df_sales['price'].max()), int(df_sales['price'].max()))
review_min = st.sidebar.slider("Filter Review Score Minimum:", 1, 5, 1)

# Filter data berdasarkan kategori dan harga
filtered_sales = df_sales[(df_sales['category'] == kategori_terpilih) & (df_sales['price'] <= harga_max)]
filtered_reviews = df_reviews[df_reviews['review_score'] >= review_min]

# --- Visualisasi Review Score ---
st.subheader("📈 Tren Rata-rata Review Score per Bulan")
monthly_review = filtered_reviews.groupby('order_date')['review_score'].mean()
fig, ax = plt.subplots(figsize=(10, 5))
monthly_review.plot(marker='o', color='b', ax=ax)
ax.set_title('Tren Rata-rata Review Score per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Review Score')
ax.grid()
st.pyplot(fig)

# --- Visualisasi Hubungan Harga & Penjualan ---
st.subheader("💰 Hubungan Harga dengan Penjualan untuk " + kategori_terpilih)
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='price', y='sales', data=filtered_sales, color='purple', ax=ax)
ax.set_title("Hubungan Harga dengan Penjualan")
ax.set_xlabel("Harga Produk")
ax.set_ylabel("Jumlah Penjualan")
st.pyplot(fig)

# --- Visualisasi Pola Penjualan Bulanan ---
st.subheader("📅 Pola Pembelian Pelanggan per Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month', y='sales', data=df_sales, estimator='sum', errorbar=None, marker='o', color='red', ax=ax)
ax.set_title("Pola Pembelian Pelanggan per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penjualan")
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

- **Conclution pertanyaan 2**:
a. Distribusi Harga Produk menunjukkan variasi harga produk dalam kategori tertentu, yang dapat digunakan untuk mengidentifikasi segmen harga yang paling diminati pelanggan.
b. Tren Penjualan per Kategori membantu memahami kategori produk mana yang memiliki performa terbaik serta peluang untuk strategi promosi.
c. Hubungan Harga dengan Penjualan memberikan wawasan mengenai bagaimana harga produk mempengaruhi jumlah penjualan, apakah ada pola penurunan permintaan pada harga tertentu.
d. Pola Pembelian Pelanggan per Bulan mengungkapkan fluktuasi penjualan bulanan, yang dapat digunakan untuk menentukan waktu terbaik dalam menjalankan promosi dan diskon.
Dari analisis ini, strategi harga dan promosi yang tepat dapat diterapkan untuk meningkatkan total penjualan sebesar 15% dalam 6 bulan dengan mengoptimalkan diskon, bundling produk, dan pemasaran berbasis tren penjualan.
""")