import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
customers_df = pd.read_csv("data/customers_dataset.csv")
orders_df = pd.read_csv("data/orders_dataset.csv")

customers_df, orders_df = load_data()

# Convert date columns to datetime
date_columns = [
    "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
    "order_delivered_customer_date", "order_estimated_delivery_date"
]
for col in date_columns:
    orders_df[col] = pd.to_datetime(orders_df[col])

# Sidebar filter
st.sidebar.header("Filter")
selected_status = st.sidebar.multiselect("Pilih Status Pesanan:", orders_df["order_status"].unique(), default=orders_df["order_status"].unique())

# Filter by date range
st.sidebar.subheader("Filter Berdasarkan Tanggal Pemesanan")
start_date = st.sidebar.date_input("Tanggal Mulai", orders_df["order_purchase_timestamp"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", orders_df["order_purchase_timestamp"].max().date())

filtered_orders = orders_df[(orders_df["order_status"].isin(selected_status)) & 
                            (orders_df["order_purchase_timestamp"].dt.date >= start_date) & 
                            (orders_df["order_purchase_timestamp"].dt.date <= end_date)]

# Dashboard Title
st.title("📊 E-Commerce Public Dataset")

# Order Status Distribution
st.subheader("Distribusi Status Pesanan")
fig, ax = plt.subplots(figsize=(10, 5))
order_status_counts = filtered_orders["order_status"].value_counts()
sns.barplot(x=order_status_counts.index, y=order_status_counts.values, ax=ax, palette="viridis")
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Jumlah")
ax.set_title("Distribusi Status Pesanan")
st.pyplot(fig)

# Trend of Orders Over Time
st.subheader("Tren Pemesanan per Bulan")
filtered_orders["order_month"] = filtered_orders["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = filtered_orders["order_month"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker="o", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Tren Pemesanan per Bulan")
ax.grid(True)
st.pyplot(fig)

# Delivery Time Analysis
st.subheader("Analisis Waktu Pengiriman")
filtered_orders["delivery_days"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_purchase_timestamp"]).dt.days
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_orders["delivery_days"].dropna(), bins=30, kde=True, color='g', ax=ax)
ax.set_xlabel("Jumlah Hari")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Distribusi Waktu Pengiriman")
st.pyplot(fig)

# Customer Distribution by State
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
fig, ax = plt.subplots(figsize=(12, 5))
customers_df["customer_state"].value_counts().plot(kind="bar", color="skyblue", ax=ax)
ax.set_xlabel("State")
ax.set_ylabel("Jumlah Pelanggan")
ax.set_title("Distribusi Pelanggan Berdasarkan Negara Bagian")
st.pyplot(fig)

# Delivery Delays Analysis
st.subheader("Distribusi Keterlambatan Pengiriman")
filtered_orders["delay_time"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_estimated_delivery_date"]).dt.days
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_orders["delay_time"].dropna(), bins=30, kde=True, color="red", ax=ax)
ax.axvline(0, color='black', linestyle='--')
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Distribusi Keterlambatan Pengiriman")
st.pyplot(fig)

# Insights
st.subheader("📌 Insights")
st.markdown("**Pertanyaan 1: Bagaimana meningkatkan jumlah pesanan bulanan sebesar 15% dalam 6 bulan ke depan?**")
st.markdown("- Tren pemesanan menunjukkan fluktuasi jumlah pesanan per bulan.")
st.markdown("- Bulan dengan jumlah pesanan terendah dapat menjadi target untuk strategi promosi.")
st.markdown("- Dengan target peningkatan 15% per bulan, strategi pemasaran seperti diskon dan kampanye digital dapat diterapkan.")

st.markdown("**Pertanyaan 2: Bagaimana mengurangi keterlambatan pengiriman hingga 30% dalam 3 bulan ke depan?**")
st.markdown("- Beberapa pesanan mengalami keterlambatan lebih dari 0 hari.")
st.markdown("- Target pengurangan keterlambatan sebesar 30% untuk meningkatkan kepuasan pelanggan.")
st.markdown("- Perbaikan efisiensi logistik dan pengiriman dapat membantu mencapai target ini.")

st.subheader("✅ Conclusion")
st.markdown("**Tren Pemesanan:**")
st.markdown("- Strategi peningkatan pesanan bisa difokuskan pada bulan dengan penjualan terendah.")
st.markdown("- Peningkatan pesanan dapat didorong melalui diskon, promosi, dan kampanye pemasaran.")

st.markdown("**Keterlambatan Pengiriman:**")
st.markdown("- Analisis keterlambatan menunjukkan beberapa pesanan mengalami keterlambatan yang cukup lama.")
st.markdown("- Meningkatkan efisiensi logistik dan pemrosesan pesanan dapat mengurangi keterlambatan hingga 30%.")