import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Menambahkan logo perusahaan
st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
# Menaampilkan tampilan header
st.header('Dicoding Collection Dashboard :sparkles:')

# Membaca File CSV
orders_df = pd.read_csv("https://github.com/Alpii21/submission-data/blob/main/data/customers_dataset.csv")
payments_df = pd.read_csv("https://github.com/Alpii21/submission-data/blob/main/data/order_payments_dataset.csv")
customers_df = pd.read_csv("https://github.com/Alpii21/submission-data/blob/main/data/customers_dataset.csv")

# Menggabungkan DataFrame
order_payments_df = pd.merge(orders_df, payments_df, on="order_id", how="left")
all_data = pd.merge(order_payments_df, customers_df, on="customer_id", how="right")

# Membersihkan Data
all_data.drop(["customer_zip_code_prefix"], axis=1, inplace=True)
all_data["order_purchase_timestamp"] = pd.to_datetime(all_data["order_purchase_timestamp"])
all_data.fillna(0, inplace=True)

# Menyimpan all_data (Opsional)
all_data.to_csv("https://github.com/Alpii21/submission-data/blob/main/dashboard/all_data.csv", index=False)

# Menampilkan beberapa baris pertama dari all_data
st.write("Data Gabungan:")
st.write(all_data.head())

# Visualisasi data
top3_payment = all_data['payment_type'].value_counts().nlargest(3)
top3_status = all_data['order_status'].value_counts().nlargest(3)

# Fungsi untuk menampilkan visualisasi pertama
def visualisasi_payment():
    payment = top3_payment.index
    jumlah = top3_payment.values
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.bar(payment, jumlah)
    ax.set_title('3 Teratas Metode Pembayaran')
    ax.set_xlabel('Metode Pembayaran')
    ax.set_ylabel('Jumlah Pembayaran')
    ax.set_xticks(range(len(payment)))
    ax.set_xticklabels(payment, rotation=45)
    st.pyplot(fig)

# Fungsi untuk menampilkan visualisasi kedua
def visualisasi_status():
    kategori = top3_status.index
    jumlah_status = top3_status.values
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.bar(kategori, jumlah_status)
    ax.set_title('3 Teratas Status Produk')
    ax.set_xlabel('Status Produk')
    ax.set_ylabel('Jumlah Produk')
    ax.set_xticks(range(len(kategori)))
    ax.set_xticklabels(kategori, rotation=45)
    st.pyplot(fig)

# Widget untuk memilih visualisasi
option = st.selectbox(
    'Pilih Visualisasi:',
    ('Metode Pembayaran', 'Status Produk')
)

# Menampilkan visualisasi berdasarkan pilihan
if option == 'Metode Pembayaran':
    visualisasi_payment()
else:
    visualisasi_status()

# # Menampilkan Kesimpulan
st.subheader("Kesimpulan")
st.write(f"- Status pemesanan yang paling banyak adalah **{top3_status.index[0]}**, menunjukkan kategori yang dominan dalam transaksi.")
st.write(f"- Metode pembayaran yang paling banyak digunakan adalah **{top3_payment.index[0]}**, menunjukkan bagaimana pola pembayaran pelanggan.")
st.write("- Dari data ini, kita bisa memahami tren dan mungkin meningkatkan efisiensi pemrosesan pesanan.")