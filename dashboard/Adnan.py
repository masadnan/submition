import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='dark')


# Set tema Streamlit
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Membaca data CSV dari GitHub
alldata_df = pd.read_csv("https://raw.githubusercontent.com/masadnan/submition/main/dashboard/all_data_ecommerce.csv")

# Header Streamlit dengan judul menarik
st.title('🛒 E-Commerce Dashboard 🚀')

# Menambahkan deskripsi untuk memberikan konteks
st.markdown(
    "Selamat datang di E-Commerce Dashboard! Dashboard ini memberikan informasi terkait review produk, "
    "penjualan per negara bagian, tipe pembayaran yang digunakan oleh pelanggan, dan korelasi antara ongkir dan nilai pembayaran."
)


# Mengatur tema background
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Membuat tab untuk subheader
selected_tab = st.sidebar.radio("Pilih Menu", ["Hubungan", "Persentase Tipe Pembayaran", "Review Customer"])

if selected_tab == "Hubungan":
    st.subheader("Hubungan")

    #melihat korelasi antara price dan freight_value
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(24, 6)) #bikin kanvasnya dulu
    colors = ["#BBF90F", "#E6E6FA", "#E6E6FA", "#E6E6FA", "#E6E6FA"]

    sns.regplot(x=alldata_df['product_weight_g'], y=alldata_df['freight_value'])
    st.pyplot() # Menampilkan plot di Streamlit

    # Membuat plot bar untuk rating produk
    selected_columns = alldata_df[['freight_value','product_weight_g']]
    selected_columns.head(15)
    correlation_mat = selected_columns.corr()
    sns.heatmap(correlation_mat, annot=True, cmap='GnBu', fmt='.2f', linewidths=0.1)
    plt.title('Matriks Korelasi')
    st.pyplot() # Menampilkan plot di Streamlit


# Tab "Produk Terjual"
elif selected_tab == "Persentase Tipe Pembayaran":
    st.subheader("Persentase Tipe Pembayaran")

    #menentukan persentase tipe payment yang digunakan
    count_payment_type_df = alldata_df.groupby("payment_type").order_id.count().sort_values(ascending=False).reset_index()
    count_payment_type_df.head(15)

    #membuat diagram lingkaran proporsi penggunaan tipe payment
    payment_count = alldata_df['payment_type'].value_counts()
    colors = sns.color_palette("deep", len(payment_count))
    explode = (0.1, 0, 0, 0)

    plt.pie(
        x=payment_count,
        labels=payment_count.index,
        autopct='%1.1f%%',
        colors=colors,
        explode=explode
    )
    plt.title('Persentase Tipe Payment yang Digunakan')

    plt.show()
    st.pyplot() # Menampilkan plot di Streamlit

# Tab "Review Customer"
elif selected_tab == "Review Customer":
    st.subheader("Review Customer")

    #menentukan proporsi penilaian customer
    sum_order_items_df = alldata_df.groupby("review_score").order_id.count().sort_values(ascending=False).reset_index()
    sum_order_items_df.head(15)

    #membuat diagram batang untuk proporsi penilaian
    bycategory_df = alldata_df.groupby(by=["review_score"]).order_id.nunique().reset_index()
    bycategory_df.rename(columns={
    "order_id": "cust_count"
    }, inplace=True)

    plt.figure(figsize=(10, 5))

    sns.barplot(
        y="cust_count",
        x="review_score",
        hue="cust_count",
        data=bycategory_df.sort_values(by="cust_count", ascending=False),
        palette="viridis", legend=False
    )
    plt.title("Proporsi Penilaian Customer", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    plt.show()
    st.pyplot() # Menampilkan plot di Streamlit

st.caption("Copyright by AdnanSyawal")
