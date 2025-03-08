import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
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

# Sidebar filters
st.sidebar.header("Filter")
selected_status = st.sidebar.multiselect("Pilih Status Pesanan", orders_df["order_status"].unique(), default=orders_df["order_status"].unique())
filtered_orders = orders_df[orders_df["order_status"].isin(selected_status)]

# Dashboard title
st.title("Dashboard Analisis Pesanan & Pelanggan")

# Order status distribution
st.subheader("Distribusi Status Pesanan")
fig, ax = plt.subplots(figsize=(10, 5))
order_status_counts = filtered_orders["order_status"].value_counts()
sns.barplot(x=order_status_counts.index, y=order_status_counts.values, palette="viridis", ax=ax)
ax.set_xlabel("Status Pesanan")
ax.set_ylabel("Jumlah")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Order trend per month
st.subheader("Tren Pemesanan per Bulan")
filtered_orders["order_month"] = filtered_orders["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = filtered_orders["order_month"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker="o", color="b", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Delivery time analysis
st.subheader("Distribusi Waktu Pengiriman")
filtered_orders["delivery_days"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_purchase_timestamp"]).dt.days
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_orders["delivery_days"].dropna(), bins=30, kde=True, color='g', ax=ax)
ax.set_xlabel("Jumlah Hari")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Customer distribution by state
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
fig, ax = plt.subplots(figsize=(12, 5))
customers_df["customer_state"].value_counts().plot(kind="bar", color="skyblue", ax=ax)
ax.set_xlabel("State")
ax.set_ylabel("Jumlah Pelanggan")
st.pyplot(fig)

# Delivery delay analysis
st.subheader("Distribusi Keterlambatan Pengiriman")
filtered_orders["delay_time"] = (filtered_orders["order_delivered_customer_date"] - filtered_orders["order_estimated_delivery_date"]).dt.days
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_orders["delay_time"].dropna(), bins=30, kde=True, color="red", ax=ax)
ax.axvline(0, color='black', linestyle='--')
st.pyplot(fig)

# Conclusion
st.header("Kesimpulan")
st.write("1. Tren pemesanan menunjukkan pola tertentu yang bisa dimanfaatkan untuk strategi pemasaran.")
st.write("2. Beberapa pesanan mengalami keterlambatan pengiriman, yang dapat dikurangi dengan optimasi logistik.")
st.write("3. Distribusi pelanggan berdasarkan negara bagian dapat membantu strategi ekspansi bisnis.")
