import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
orders_df = pd.read_csv("orders_dataset.csv", parse_dates=["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"])
customers_df = pd.read_csv("customers_dataset.csv")

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

# Distribusi Keterlambatan Pengiriman
st.subheader("Distribusi Keterlambatan Pengiriman")
df_filtered["delay_time"] = (df_filtered["order_delivered_customer_date"] - df_filtered["order_estimated_delivery_date"]).dt.days
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df_filtered["delay_time"].dropna(), bins=30, kde=True, color="red", ax=ax)
ax.axvline(0, color='black', linestyle='--')
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)