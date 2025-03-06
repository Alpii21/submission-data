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

# Simulasi data pelanggan
df_pelanggan = pd.DataFrame({
    'order_id': range(1, 501),
    'review_score': np.random.randint(1, 6, 500),
    'delivery_time_days': np.random.randint(1, 15, 500),
    'order_date': pd.date_range(start='2023-06-01', periods=500, freq='D')
})
df_pelanggan['order_month'] = df_pelanggan['order_date'].dt.to_period('M')

# Simulasi data produk
df_produk = pd.DataFrame({
    'product_id': range(1, 101),
    'category': ['A', 'B', 'C', 'D'] * 25,
    'price': np.random.uniform(10, 500, 100).round(2),
    'sales': np.random.randint(50, 500, 100),
    'month': ['Jan', 'Feb', 'Mar'] * 33 + ['Jan']
})

# Tab untuk analisis data pelanggan dan produk
tab1, tab2 = st.tabs(["Analisis Pelanggan", "Analisis Produk"])

with tab1:
    st.subheader("Statistik Deskriptif Pelanggan")
    st.write(df_pelanggan.describe())
    
    st.subheader("Distribusi Review Score")
    fig, ax = plt.subplots()
    sns.countplot(x='review_score', data=df_pelanggan, palette='coolwarm', ax=ax)
    st.pyplot(fig)
    
    st.subheader("Tren Rata-rata Review Score per Bulan")
    monthly_review = df_pelanggan.groupby('order_month')['review_score'].mean()
    fig, ax = plt.subplots()
    monthly_review.plot(marker='o', color='b', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Review Score")
    st.pyplot(fig)
    
    st.subheader("Hubungan Waktu Pengiriman vs Review Score")
    fig, ax = plt.subplots()
    sns.boxplot(x='review_score', y='delivery_time_days', data=df_pelanggan, palette='viridis', ax=ax)
    st.pyplot(fig)
    
    st.subheader("Korelasi antara Review Score dan Waktu Pengiriman")
    st.write(df_pelanggan[['review_score', 'delivery_time_days']].corr())

with tab2:
    st.subheader("Distribusi Harga Produk")
    fig, ax = plt.subplots()
    sns.histplot(df_produk['price'], bins=20, kde=True, color='blue', ax=ax)
    st.pyplot(fig)
    
    st.subheader("Tren Penjualan per Kategori Produk")
    fig, ax = plt.subplots()
    sns.boxplot(x='category', y='sales', data=df_produk, palette='coolwarm', ax=ax)
    st.pyplot(fig)
    
    st.subheader("Hubungan Harga dengan Penjualan")
    fig, ax = plt.subplots()
    sns.scatterplot(x='price', y='sales', data=df_produk, hue='category', palette='viridis', ax=ax)
    st.pyplot(fig)
    
    st.subheader("Pola Pembelian Pelanggan per Bulan")
    fig, ax = plt.subplots()
    sns.lineplot(x='month', y='sales', data=df_produk, estimator='sum', marker='o', color='red', ax=ax)
    st.pyplot(fig)

st.write("Dashboard ini dibuat dengan Streamlit untuk analisis data pelanggan dan produk.")

# # Menampilkan Kesimpulan
st.subheader("Kesimpulan")
st.write(f"Conclution pertanyaan 1 : Berdasarkan analisis data review score dan waktu pengiriman pesanan, terdapat hubungan antara kepuasan pelanggan dan kecepatan pengiriman. Untuk meningkatkan tingkat kepuasan pelanggan sebesar 10% dalam 6 bulan ke depan, strategi yang dapat diterapkan meliputi: a. Mempercepat Waktu Pengiriman : Mengurangi keterlambatan dan meningkatkan efisiensi logistik. b. Meningkatkan Kualitas Layanan : Respon cepat terhadap keluhan pelanggan dan peningkatan layanan pelanggan. c. Analisis Umpan Balik Pelanggan : Mengidentifikasi faktor utama yang mempengaruhi review score rendah dan memperbaikinya. d. Optimasi Proses Pemrosesan Pesanan : Menggunakan teknologi atau AI untuk memprediksi dan mempercepat proses pemenuhan pesanan.")
st.write(f"Conclution pertanyaan 2 : a. Kategori produk dengan harga lebih rendah cenderung memiliki penjualan lebih tinggi. b. Penjualan mengalami tren tertentu setiap bulannya, perlu strategi promo musiman. c. Strategi diskon atau bundle dapat meningkatkan penjualan sebesar 15% dalam 3 bulan ke depan.")