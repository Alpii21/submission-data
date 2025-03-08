import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
customers_df = pd.read_csv("data/customers_dataset.csv")
orders_df = pd.read_csv("orders_dataset.csv")

# Konversi kolom tanggal ke format datetime
date_columns = [
    "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", 
    "order_delivered_customer_date", "order_estimated_delivery_date"
]
for col in date_columns:
    orders_df[col] = pd.to_datetime(orders_df[col])

# Sidebar - Filter Status Pesanan
st.sidebar.header("Filter Data")
selected_status = st.sidebar.multiselect("Pilih Status Pesanan:", orders_df["order_status"].unique(), default=orders_df["order_status"].unique())
filtered_orders = orders_df[orders_df["order_status"].isin(selected_status)]

st.title("📊 Dashboard EDA - Analisis Pesanan")

# 1. Distribusi Status Pesanan
st.subheader("Distribusi Status Pesanan")
status_counts = filtered_orders["order_status"].value_counts()
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=status_counts.index, y=status_counts.values, palette="viridis", ax=ax)
plt.xlabel("Status Pesanan")
plt.ylabel("Jumlah")
st.pyplot(fig)

# 2. Tren Pemesanan per Bulan
st.subheader("Tren Pemesanan per Bulan")
filtered_orders["order_month"] = filtered_orders["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = filtered_orders["order_month"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker="o", color="b", ax=ax)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Pesanan")
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. Distribusi Waktu Pengiriman
st.subheader("Distribusi Waktu Pengiriman")
filtered_orders["delivery_days"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_purchase_timestamp"]).dt.days
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(filtered_orders["delivery_days"].dropna(), bins=30, kde=True, color='g', ax=ax)
plt.xlabel("Jumlah Hari")
plt.ylabel("Jumlah Pesanan")
st.pyplot(fig)

# 4. Distribusi Pelanggan Berdasarkan Negara Bagian
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
fig, ax = plt.subplots(figsize=(12,5))
customers_df["customer_state"].value_counts().plot(kind="bar", color="skyblue", ax=ax)
plt.xlabel("State")
plt.ylabel("Jumlah Pelanggan")
st.pyplot(fig)

# 5. Distribusi Keterlambatan Pengiriman
st.subheader("Distribusi Keterlambatan Pengiriman")
filtered_orders["delay_time"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_estimated_delivery_date"]).dt.days
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(filtered_orders["delay_time"].dropna(), bins=30, kde=True, color="red", ax=ax)
plt.axvline(0, color='black', linestyle='--')
plt.xlabel("Hari")
plt.ylabel("Jumlah Pesanan")
st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Dashboard ini dibuat dengan Streamlit untuk eksplorasi data pesanan.**")