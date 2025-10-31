
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="BI Market Insights", page_icon="📊", layout="wide")
st.title("📊 BI Market Insights")
st.caption("Contoh funnel penjualan, segmentasi pelanggan, dan cohort retention.")

@st.cache_data
def make_sales():
    np.random.seed(42)
    n=1200
    df = pd.DataFrame({
        "customer_id": np.random.randint(1000, 3000, n),
        "segment": np.random.choice(["SME","Enterprise","Retail"], n, p=[.4,.25,.35]),
        "stage": np.random.choice(["Visited","Trial","Qualified","Won","Churned"], n, p=[.4,.25,.2,.1,.05]),
        "revenue": np.round(np.random.lognormal(mean=9, sigma=0.7, size=n),2),
        "month": np.random.choice(pd.date_range("2024-07-01","2025-06-30",freq="MS"), n)
    })
    return df

df = make_sales()

c1,c2,c3 = st.columns(3)
c1.metric("Total Revenue", f"Rp {int(df['revenue'].sum()):,}".replace(",", "."))
c2.metric("Avg Deal", f"Rp {int(df['revenue'].mean()):,}".replace(",", "."))
c3.metric("Leads", df['customer_id'].nunique())

tab1, tab2, tab3 = st.tabs(["Funnel", "Segment", "Cohort"])

with tab1:
    funnel = df.groupby("stage").size().reindex(["Visited","Trial","Qualified","Won","Churned"]).reset_index(name="count")
    fig = px.area(funnel, x="stage", y="count", title="Sales Funnel")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    seg = df.groupby(["month","segment"])["revenue"].sum().reset_index()
    fig = px.bar(seg, x="month", y="revenue", color="segment", title="Revenue by Segment (Monthly)")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Simple cohort proxy by first-month bucket
    first = df.groupby("customer_id")["month"].min().reset_index().rename(columns={"month":"cohort"})
    merged = df.merge(first, on="customer_id", how="left")
    cohort = merged.groupby(["cohort","month"]).size().reset_index(name="active")
    pivot = cohort.pivot(index="cohort", columns="month", values="active").fillna(0)
    st.dataframe(pivot)

st.divider()
st.markdown("**Next step (production):** hubungkan ke MSSQL/PostgreSQL dan tambahkan SSO + RBAC untuk klien enterprise.")
