import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Price Intelligence — Tokopedia", page_icon="💹", layout="wide")
st.title("💹 Price Intelligence — Tokopedia")
st.caption("Analisis harga, brand share, dan kompetitor. Dapat dihubungkan ke scraper Kelar.in.")

with st.sidebar:
    st.header("Data")
    sample = st.checkbox("Gunakan sample data", value=True)
    uploaded = st.file_uploader("Upload CSV hasil scraping", type=["csv"])

@st.cache_data
def load_sample():
    np.random.seed(1)
    n=300
    df = pd.DataFrame({
        "product": [f"Produk {i}" for i in range(n)],
        "brand": np.random.choice(["Brand A","Brand B","Brand C","Brand D"], size=n, p=[.35,.25,.25,.15]),
        "price": np.random.randint(20000, 1500000, size=n),
        "rating": np.round(np.random.uniform(3.0, 5.0, size=n),2),
        "sold": np.random.randint(0, 5000, size=n),
        "date": pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0,180,size=n), unit="D")
    })
    return df

if sample or uploaded is None:
    df = load_sample()
else:
    df = pd.read_csv(uploaded)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.metric("Total Produk", len(df))
c1,c2,c3 = st.columns(3)
c1.metric("Median Harga", f"Rp {int(df['price'].median()):,}".replace(",", "."))
c2.metric("Avg Rating", f"{df['rating'].mean():.2f}")
c3.metric("Total Terjual", int(df['sold'].sum()))

tab1, tab2, tab3 = st.tabs(["Brand Share", "Price vs Sold", "Trend Waktu"])

with tab1:
    share = df.groupby("brand").size().reset_index(name="count")
    fig = px.pie(share, values="count", names="brand", title="Brand Share")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Scatter tanpa statsmodels + garis tren manual
    fig = px.scatter(
        df, x="price", y="sold", color="brand",
        hover_data=["product","rating"]
    )
    # garis regresi overall
    m, b = np.polyfit(df["price"], df["sold"], 1)
    xline = np.linspace(df["price"].min(), df["price"].max(), 100)
    fig.add_trace(go.Scatter(x=xline, y=m * xline + b, mode="lines", name="Trendline (OLS approx)"))
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Ingin pakai trendline per brand dengan `trendline='ols'`? Tambahkan `statsmodels` di requirements dan ganti scatter ke `trendline='ols'`.")

with tab3:
    ts = df.groupby("date")["sold"].sum().reset_index()
    fig = px.line(ts, x="date", y="sold", title="Penjualan Harian (Proxy)")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("**Next step (production):** jadwalkan scraping harian (cron/Prefect) dan simpan ke PostgreSQL/MSSQL.")
