import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Menambahkan logo perusahaan
st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
# Menaampilkan tampilan header
st.header('Dicoding Collection Dashboard :sparkles:')

st.title("Dashboard Analisis Data Pelanggan & Produk")

# Simulasi data pelanggan (Contoh dataset)
data_pelanggan = {
    'order_id': range(1, 501),
    'review_score': np.random.randint(1, 6, 500),  # Skala 1-5
    'delivery_time_days': np.random.randint(1, 15, 500),  # Lama pengiriman dalam hari
    'order_date': pd.date_range(start='2023-06-01', periods=500, freq='D')
}
df_pelanggan = pd.DataFrame(data_pelanggan)

# Simulasi data produk (Contoh dataset)
data_produk = {
    'product_id': range(1, 101),
    'category': ['A', 'B', 'C', 'D'] * 25,
    'price': [round(x, 2) for x in list(np.random.uniform(10, 500, 100))],
    'sales': [np.random.randint(50, 500) for _ in range(100)],
    'month': ['Jan', 'Feb', 'Mar'] * 33 + ['Jan']
}
df_produk = pd.DataFrame(data_produk)

# Judul Dashboard
st.title("Dashboard Analisis Pelanggan dan Produk")

# Bagian Analisis Pelanggan
st.header("Analisis Pelanggan")

# Statistik deskriptif
st.subheader("Statistik Deskriptif Data Pelanggan")
st.write(df_pelanggan.describe())

# Visualisasi distribusi review score
st.subheader("Distribusi Review Score")
fig_review, ax_review = plt.subplots(figsize=(8, 5))
sns.countplot(x='review_score', data=df_pelanggan, hue='review_score', palette='coolwarm', legend=False, ax=ax_review)
ax_review.set_title('Distribusi Review Score')
ax_review.set_xlabel('Review Score')
ax_review.set_ylabel('Jumlah')
st.pyplot(fig_review)

# Tren rata-rata review score per bulan
st.subheader("Tren Rata-rata Review Score per Bulan")
df_pelanggan['order_month'] = df_pelanggan['order_date'].dt.to_period('M')
monthly_review = df_pelanggan.groupby('order_month')['review_score'].mean()
fig_tren_review, ax_tren_review = plt.subplots(figsize=(10, 5))
monthly_review.plot(marker='o', color='b', ax=ax_tren_review)
ax_tren_review.set_title('Tren Rata-rata Review Score per Bulan')
ax_tren_review.set_xlabel('Bulan')
ax_tren_review.set_ylabel('Rata-rata Review Score')
ax_tren_review.grid()
st.pyplot(fig_tren_review)

# Hubungan antara waktu pengiriman dan review score
st.subheader("Waktu Pengiriman vs Review Score")
fig_delivery_review, ax_delivery_review = plt.subplots(figsize=(8, 5))
sns.boxplot(x='review_score', y='delivery_time_days', data=df_pelanggan, hue='review_score', palette='viridis', legend=False, ax=ax_delivery_review)
ax_delivery_review.set_title('Waktu Pengiriman vs Review Score')
ax_delivery_review.set_xlabel('Review Score')
ax_delivery_review.set_ylabel('Waktu Pengiriman (hari)')
st.pyplot(fig_delivery_review)

# Korelasi
st.subheader("Korelasi antara Review Score dan Waktu Pengiriman")
correlation = df_pelanggan[['review_score', 'delivery_time_days']].corr()
st.write(correlation)

# Bagian Analisis Produk
st.header("Analisis Produk")

# Distribusi Harga Produk
st.subheader("Distribusi Harga Produk")
fig_dist_harga, ax_dist_harga = plt.subplots(figsize=(10, 5))
sns.histplot(df_produk['price'], bins=20, kde=True, color='blue', ax=ax_dist_harga)
ax_dist_harga.set_title("Distribusi Harga Produk")
ax_dist_harga.set_xlabel("Harga")
ax_dist_harga.set_ylabel("Frekuensi")
st.pyplot(fig_dist_harga)

# Tren Penjualan per Kategori Produk
st.subheader("Tren Penjualan per Kategori Produk")
fig_tren_kategori, ax_tren_kategori = plt.subplots(figsize=(12, 6))
sns.boxplot(x='category', y='sales', data=df_produk, hue='category', palette='coolwarm', legend=False, ax=ax_tren_kategori)
ax_tren_kategori.set_title("Tren Penjualan per Kategori Produk")
ax_tren_kategori.set_xlabel("Kategori Produk")
ax_tren_kategori.set_ylabel("Penjualan")
st.pyplot(fig_tren_kategori)

# Hubungan Harga dengan Penjualan
st.subheader("Hubungan Harga dengan Penjualan")
fig_harga_penjualan, ax_harga_penjualan = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='price', y='sales', data=df_produk, hue='category', palette='viridis', ax=ax_harga_penjualan)
ax_harga_penjualan.set_title("Hubungan Harga dengan Penjualan")
ax_harga_penjualan.set_xlabel("Harga Produk")
ax_harga_penjualan.set_ylabel("Jumlah Penjualan")
st.pyplot(fig_harga_penjualan)

# Analisis Tren Pola Pembelian Pelanggan per Bulan
st.subheader("Pola Pembelian Pelanggan per Bulan")
fig_pola_pembelian, ax_pola_pembelian = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month', y='sales', data=df_produk, estimator='sum', errorbar=None, marker='o', color='red', ax=ax_pola_pembelian)
ax_pola_pembelian.set_title("Pola Pembelian Pelanggan per Bulan")
ax_pola_pembelian.set_xlabel("Bulan")
ax_pola_pembelian.set_ylabel("Total Penjualan")
st.pyplot(fig_pola_pembelian)