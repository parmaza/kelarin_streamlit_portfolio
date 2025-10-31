
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="IoT Telemetry Dashboard", page_icon="📡", layout="wide")
st.title("📡 IoT Telemetry Dashboard")
st.caption("Simulasi device telemetry + deteksi anomali sederhana.")

@st.cache_data
def make_data(n=500):
    t0 = datetime.now() - timedelta(hours=5)
    ts = [t0 + timedelta(minutes=i) for i in range(n)]
    temp = np.random.normal(36, 1.5, n)
    # sisipkan anomali
    for k in [120, 260, 380]:
        temp[k:k+5] += np.random.uniform(4,6)
    df = pd.DataFrame({ "ts": ts, "temperature": temp, "device_id": "SENSOR-01"})
    return df

df = make_data()
thr = st.slider("Threshold suhu (°C)", 37.5, 42.0, 39.0, 0.1)
df["anomaly"] = df["temperature"] > thr

c1,c2 = st.columns(2)
with c1:
    st.metric("Puncak Suhu", f"{df['temperature'].max():.2f} °C")
with c2:
    st.metric("Jumlah Anomali", int(df['anomaly'].sum()))

fig = px.line(df, x="ts", y="temperature", title="Temperature over Time")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df[df["anomaly"]].tail(20))

st.divider()
st.markdown("**Next step (production):** ganti sumber data dengan MQTT/Kafka atau tabel PostgreSQL realtime, lalu kirim alert ke WhatsApp/Email.")
