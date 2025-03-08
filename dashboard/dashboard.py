import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
@st.cache_data
def load_data():
    customers_df = pd.read_csv("data/customers_dataset.csv")
    orders_df = pd.read_csv("data/orders_dataset.csv")
    return customers_df, orders_df

customers_df, orders_df = load_data()

# Convert date columns to datetime
date_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
for col in date_columns:
    orders_df[col] = pd.to_datetime(orders_df[col])

# Sidebar Filters
st.sidebar.header("Filter")
selected_status = st.sidebar.multiselect("Pilih Status Pesanan", orders_df["order_status"].unique(), default=orders_df["order_status"].unique())
filtered_orders = orders_df[orders_df["order_status"].isin(selected_status)]

# Main Dashboard
st.title("📊 E-Commerce Orders Dashboard")

# Order Status Distribution
st.subheader("Distribusi Status Pesanan")
fig, ax = plt.subplots(figsize=(10, 5))
order_status_counts = filtered_orders["order_status"].value_counts()
sns.barplot(x=order_status_counts.index, y=order_status_counts.values, palette="viridis", ax=ax)
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Jumlah")
ax.set_xticklabels(order_status_counts.index, rotation=45)
st.pyplot(fig)

# Monthly Orders Trend
st.subheader("Tren Pemesanan per Bulan")
filtered_orders["order_month"] = filtered_orders["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = filtered_orders["order_month"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker="o", color="b", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_xticklabels(monthly_orders.index.astype(str), rotation=45)
st.pyplot(fig)

# Delivery Time Distribution
st.subheader("Distribusi Waktu Pengiriman (Hari)")
filtered_orders["delivery_days"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_purchase_timestamp"]).dt.days
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_orders["delivery_days"].dropna(), bins=30, kde=True, color='g', ax=ax)
ax.set_xlabel("Jumlah Hari")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Customer Distribution by State
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
fig, ax = plt.subplots(figsize=(12, 5))
customers_df["customer_state"].value_counts().plot(kind="bar", color="skyblue", ax=ax)
ax.set_xlabel("State")
ax.set_ylabel("Jumlah Pelanggan")
st.pyplot(fig)

# Delivery Delay Analysis
st.subheader("Distribusi Keterlambatan Pengiriman (Hari)")
filtered_orders["delay_time"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_estimated_delivery_date"]).dt.days
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_orders["delay_time"].dropna(), bins=30, kde=True, color="red", ax=ax)
ax.axvline(0, color='black', linestyle='--')
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Insights and Conclusions
st.header("📌 Insights & Conclusions")
st.subheader("1. Tren Pemesanan per Bulan")
low_sales_month = monthly_orders.idxmin()
st.write(f"Bulan dengan jumlah pesanan terendah: {low_sales_month}")
st.write("Strategi: Promosi dan diskon dapat diterapkan di bulan dengan penjualan rendah untuk meningkatkan jumlah pesanan.")

st.subheader("2. Analisis Keterlambatan Pengiriman")
delayed_orders = filtered_orders[filtered_orders["delay_time"] > 0]
st.write(f"Total pesanan yang mengalami keterlambatan: {len(delayed_orders)}")
st.write("Strategi: Optimalisasi rantai pasokan dan peningkatan efisiensi logistik dapat mengurangi keterlambatan pengiriman.")

st.write("Terima kasih telah menggunakan dashboard ini! 🚀")