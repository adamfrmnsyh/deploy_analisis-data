import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_pickle("all_dfs.pkl")
    return data

data = load_data()
order_items_df = data['order_items_df']
products_df = data['products_df']
orders_df = data['orders_df']
order_reviews_df = data['order_reviews_df']

# Sidebar Navigation
st.sidebar.title("🔍 Navigasi Analisis")
option = st.sidebar.radio("Pilih Analisis:", [
    "🏆 Kategori Produk dengan Penjualan Tertinggi",
    "🔄 Kategori Produk dengan Pengembalian Tertinggi",
    "⏳📉 Hubungan Waktu Pengiriman dan Rating Produk"
])

st.title("📊 Analisis Data E-Commerce")
st.markdown("---")

if option == "🏆 Kategori Produk dengan Penjualan Tertinggi":
    st.subheader("🏆 Kategori Produk dengan Penjualan Tertinggi")
    top_10_categories = (
        order_items_df.merge(products_df, on="product_id", how="left")
        .groupby("product_category_name")["product_id"]
        .count()
        .reset_index()
        .rename(columns={"product_id": "count"})
        .sort_values(by="count", ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_10_categories["count"], y=top_10_categories["product_category_name"], palette="viridis", ax=ax)
    ax.set_xlabel("Jumlah Penjualan", fontsize=12)
    ax.set_ylabel("Kategori Produk", fontsize=12)
    ax.set_title("Top 10 Kategori Produk Terlaris", fontsize=14, fontweight='bold')
    st.pyplot(fig)

elif option == "🔄 Kategori Produk dengan Pengembalian Tertinggi":
    st.subheader("🔄 Kategori Produk dengan Pengembalian Tertinggi")
    merged_df = order_items_df.merge(orders_df, on="order_id")
    returned_orders = merged_df[merged_df["order_status"].isin(["canceled"])]
    returned_orders = returned_orders.merge(products_df, on="product_id", how="left")
    returned_counts = returned_orders.groupby("product_category_name").size().reset_index(name="count")
    returned_counts = returned_counts.sort_values(by="count", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=returned_counts["count"], y=returned_counts["product_category_name"], palette="coolwarm", ax=ax)
    ax.set_xlabel("Jumlah Pengembalian", fontsize=12)
    ax.set_ylabel("Kategori Produk", fontsize=12)
    ax.set_title("Top 10 Kategori Produk dengan Pengembalian Tertinggi", fontsize=14, fontweight='bold')
    st.pyplot(fig)

elif option == "⏳📉 Hubungan Waktu Pengiriman dan Rating Produk":
    st.subheader("⏳📉 Hubungan Waktu Pengiriman dan Rating Produk")
    orders_df["delivery_time"] = (orders_df["order_delivered_customer_date"] - orders_df["order_purchase_timestamp"]).dt.days
    avg_rating_df = order_reviews_df.groupby("order_id")["review_score"].mean().reset_index()
    delivery_rating_df = orders_df.merge(avg_rating_df, on="order_id", how="inner")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x=delivery_rating_df["delivery_time"], y=delivery_rating_df["review_score"], alpha=0.6, color='royalblue', edgecolor='black')
    ax.set_xlabel("Waktu Pengiriman (hari)", fontsize=12)
    ax.set_ylabel("Rating Produk", fontsize=12)
    ax.set_title("Hubungan antara Waktu Pengiriman dan Rating Produk", fontsize=14, fontweight='bold')
    st.pyplot(fig)

st.markdown("---")
st.write("📌 Analisis ini membantu memahami pola penjualan, pengembalian, dan kepuasan pelanggan berdasarkan rating serta waktu pengiriman.")
