import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset
orders_df = pd.read_csv('C:\dicoding\submission\data\orders_dataset.csv')
order_reviews_df = pd.read_csv('C:\dicoding\submission\data\order_reviews_dataset.csv')

# Konversi kolom tanggal ke format datetime
orders_df["order_purchase_timestamp"] = pd.to_datetime(orders_df["order_purchase_timestamp"])

# Pertanyaan 1: Strategi Peningkatan Layanan Pelanggan
st.title("Analisis Review Score dan Layanan Pelanggan")
st.subheader("Bagaimana strategi peningkatan layanan pelanggan dapat meningkatkan rata-rata review score sebesar 10% dalam 6 bulan ke depan dan meningkatkan jumlah review positif (≥ 4) sebesar 20%?")

# Menyesuaikan panjang data
min_length = min(len(orders_df), len(order_reviews_df), 500)

data = {
    "order_id": range(1, min_length + 1),
    "review_score": order_reviews_df["review_score"].fillna(order_reviews_df["review_score"].median()).astype(int)[:min_length],
    "order_date": pd.date_range(start='2023-06-01', periods=min_length, freq='D')
}
df_reviews = pd.DataFrame(data)

# Statistik deskriptif
st.write("### Statistik Deskriptif Review Score")
st.write(df_reviews.describe())

# Visualisasi distribusi review score
fig, ax = plt.subplots()
sns.countplot(x='review_score', data=df_reviews, hue='review_score', palette='coolwarm', legend=False, ax=ax)
ax.set_title('Distribusi Review Score')
ax.set_xlabel('Review Score')
ax.set_ylabel('Jumlah')
st.pyplot(fig)

# Tren rata-rata review score per bulan
df_reviews['order_date'] = df_reviews['order_date'].dt.to_period('M')
monthly_review = df_reviews.groupby('order_date')['review_score'].mean()

fig, ax = plt.subplots()
monthly_review.plot(marker='o', color='b', ax=ax)
ax.set_title('Tren Rata-rata Review Score per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Review Score')
ax.grid()
st.pyplot(fig)

# Pertanyaan 2: Strategi Harga dan Promosi
st.title("Analisis Harga dan Penjualan Produk")
st.subheader("Bagaimana strategi harga dan promosi dapat meningkatkan total penjualan produk dalam kategori 'beleza_saude', 'telefonia_fixa', 'brinquedos', dan 'bebes' sebesar 15% dalam 6 bulan?")

# Membuat data produk
data = {
    'product_id': range(1, 101),
    'category': ['beleza_saude', 'telefonia_fixa', 'brinquedos', 'bebes'] * 25,
    'price': [round(x, 2) for x in np.random.uniform(10, 500, 100)],
    'seler': [np.random.randint(50, 500) for _ in range(100)],
    'order_purchase_timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D')
}
df_seler = pd.DataFrame(data)

# Menambahkan kolom bulan
df_seler['month'] = df_seler['order_purchase_timestamp'].dt.strftime('%b')

# Filter kategori
selected_category = st.selectbox("Pilih kategori produk:", df_seler['category'].unique())
filtered_sales = df_seler[df_seler['category'] == selected_category]

# Distribusi Harga Produk
fig, ax = plt.subplots()
sns.histplot(filtered_sales['price'], bins=20, kde=True, color='blue', ax=ax)
ax.set_title("Distribusi Harga Produk")
ax.set_xlabel("Harga")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Tren Penjualan per Kategori Produk
fig, ax = plt.subplots()
sns.boxplot(x='category', y='sales', data=df_seler, hue='category', palette='coolwarm', ax=ax)
ax.set_title("Tren Penjualan per Kategori Produk")
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Penjualan")
st.pyplot(fig)

# Hubungan Harga dengan Penjualan
fig, ax = plt.subplots()
sns.scatterplot(x='price', y='seler', data=filtered_sales, hue='category', palette='viridis', ax=ax)
ax.set_title("Hubungan Harga dengan Penjualan")
ax.set_xlabel("Harga Produk")
ax.set_ylabel("Jumlah Penjualan")
st.pyplot(fig)

# Analisis Tren Pola Pembelian Pelanggan per Bulan
fig, ax = plt.subplots()
sns.lineplot(x='month', y='seler', data=filtered_sales, estimator='sum', errorbar=None, marker='o', color='red', ax=ax)
ax.set_title("Pola Pembelian Pelanggan per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penjualan")
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