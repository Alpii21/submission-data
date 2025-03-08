import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
orders_df = pd.read_csv("C:\dicoding\submission\data\orders_dataset.xls", parse_dates=["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]),
customers_df = pd.read_csv("C:\dicoding\submission\data\customers_dataset.xls")

# Sidebar - Filter
st.sidebar.header("Filter Data")
status_options = orders_df["order_status"].unique()
selected_status = st.sidebar.multiselect("Pilih Status Pesanan", status_options, default=status_options)

# Filter berdasarkan tanggal
start_date = st.sidebar.date_input("Mulai Tanggal", orders_df["order_purchase_timestamp"].min().date())
end_date = st.sidebar.date_input("Sampai Tanggal", orders_df["order_purchase_timestamp"].max().date())

# Terapkan Filter
df_filtered = orders_df[(orders_df["order_status"].isin(selected_status)) & 
                         (orders_df["order_purchase_timestamp"].dt.date >= start_date) & 
                         (orders_df["order_purchase_timestamp"].dt.date <= end_date)]

# Dashboard Title
st.title("Dashboard EDA - Analisis Pesanan")

# Distribusi Status Pesanan
st.subheader("Distribusi Status Pesanan")
order_status_counts = df_filtered["order_status"].value_counts()
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=order_status_counts.index, y=order_status_counts.values, palette="viridis", ax=ax)
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Jumlah")
ax.set_xticklabels(order_status_counts.index, rotation=45)
st.pyplot(fig)

# Tren Pemesanan per Bulan
st.subheader("Tren Pemesanan per Bulan")
df_filtered["order_month"] = df_filtered["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = df_filtered["order_month"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker="o", color="b", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_xticklabels(monthly_orders.index.astype(str), rotation=45)
ax.grid(True)
st.pyplot(fig)

# Distribusi Waktu Pengiriman
st.subheader("Distribusi Waktu Pengiriman")
df_filtered["delivery_days"] = (df_filtered["order_delivered_customer_date"] - df_filtered["order_purchase_timestamp"]).dt.days
df_filtered = df_filtered.dropna(subset=["delivery_days"])
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df_filtered["delivery_days"], bins=30, kde=True, color='g', ax=ax)
ax.set_xlabel("Jumlah Hari")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Distribusi Pelanggan Berdasarkan Negara Bagian
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
fig, ax = plt.subplots(figsize=(12, 5))
customers_df["customer_state"].value_counts().plot(kind="bar", color="skyblue", ax=ax)
ax.set_xlabel("State")
ax.set_ylabel("Jumlah Pelanggan")
ax.set_xticklabels(customers_df["customer_state"].unique(), rotation=45)
st.pyplot(fig)

# Distribusi Keterlambatan Pengiriman
st.subheader("Distribusi Keterlambatan Pengiriman")
df_filtered["delay_time"] = (df_filtered["order_delivered_customer_date"] - df_filtered["order_estimated_delivery_date"]).dt.days
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df_filtered["delay_time"].dropna(), bins=30, kde=True, color="red", ax=ax)
ax.axvline(0, color='black', linestyle='--')
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Pertanyaan 1: Bagaimana meningkatkan jumlah pesanan bulanan sebesar 15% dalam 6 bulan ke depan?
st.subheader("Analisis Peningkatan Pesanan")
st.write("Dari analisis tren pemesanan bulanan, ditemukan bahwa jumlah pesanan berfluktuasi. Dengan mengidentifikasi bulan dengan penjualan terendah, strategi pemasaran dapat difokuskan untuk meningkatkan pesanan. Target peningkatan sebesar 15% dari rata-rata bulanan telah ditentukan.")

# Menentukan bulan dengan jumlah pesanan terendah
low_sales_month = monthly_orders.idxmin()
st.write(f"Bulan dengan jumlah pesanan terendah: {low_sales_month}")

# Menentukan target peningkatan 15%
current_avg_orders = monthly_orders.mean()
target_orders = current_avg_orders * 1.15
st.write(f"Target pesanan per bulan setelah peningkatan 15%: {round(target_orders)}")

st.subheader("Kesimpulan Pertanyaan 1")
st.write("- Tren pemesanan per bulan menunjukkan fluktuasi jumlah pesanan.")
st.write(f"- Bulan dengan jumlah pesanan terendah adalah {low_sales_month}, yang dapat menjadi fokus strategi pemasaran.")
st.write("- Target peningkatan 15% telah ditentukan untuk meningkatkan jumlah pesanan.")

# Pertanyaan 2: Bagaimana mengurangi keterlambatan pengiriman hingga 30% dalam 3 bulan ke depan?
st.subheader("Analisis Keterlambatan Pengiriman")
st.write("Banyak pesanan mengalami keterlambatan lebih dari 0 hari. Dengan memahami pola keterlambatan dan faktor penyebabnya, langkah-langkah perbaikan dapat diambil untuk mengurangi keterlambatan hingga 30%, meningkatkan kepuasan pelanggan.")

# Filter hanya pesanan yang mengalami keterlambatan
delayed_orders = df_filtered[df_filtered["delay_time"] > 0]
current_delays = len(delayed_orders)
target_delays = current_delays * 0.7  # Target -30%

st.write(f"Total pesanan yang mengalami keterlambatan: {current_delays}")
st.write(f"Target pesanan terlambat setelah pengurangan 30%: {round(target_delays)}")

st.subheader("Kesimpulan Pertanyaan 2")
st.write("- Sejumlah pesanan mengalami keterlambatan pengiriman lebih dari 0 hari.")
st.write(f"- Total keterlambatan saat ini adalah {current_delays} pesanan.")
st.write("- Target penurunan keterlambatan sebesar 30% telah ditetapkan untuk meningkatkan kepuasan pelanggan.")
st.write("- Mayoritas keterlambatan berkisar antara 1-7 hari, dengan beberapa kasus lebih lama.")