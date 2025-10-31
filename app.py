import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="Kelar.in Portfolio Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"  # ✅ menu selalu terbuka
)

# ✅ CSS
st.markdown("""
<style>
:root {
  --k-primary: #6d28d9;
  --k-accent: #facc15;
  --k-ink: #0f172a;
}
h1, h2, h3 { color: var(--k-ink); }
.big-tag {
  background: linear-gradient(90deg, var(--k-primary), var(--k-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  letter-spacing: 0.3px;
}
.card {
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
.k-badge {
  display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px;
  background:#eef2ff; color:#3730a3; margin-right:6px;
}
/* hanya sembunyikan footer dan menu default, jangan header */
footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ✅ Sidebar Navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/01_RAG Doc QA — Upload & Ask.py", label="📚 RAG Doc QA — Upload & Ask")
    st.page_link("pages/02_Price Intelligence — Tokopedia.py", label="💹 Price Intelligence — Tokopedia")
    st.page_link("pages/03_IoT Telemetry Dashboard.py", label="📡 IoT Telemetry Dashboard")
    st.page_link("pages/04_BI Market Insights.py", label="📊 BI Market Insights")

st.markdown("<h1 class='big-tag'>Kelar.in Studio — Portfolio Hub</h1>", unsafe_allow_html=True)
st.write("Solusi data scraping, BI, AI (GenAI/RAG), integrasi dashboard, dan aplikasi mobile.")

cols = st.columns(4)
titles = [
    {"title": "RAG Doc QA — Upload & Ask", "emoji": "📚"},
    {"title": "Price Intelligence — Tokopedia", "emoji": "💹"},
    {"title": "IoT Telemetry Dashboard", "emoji": "📡"},
    {"title": "BI Market Insights", "emoji": "📊"}
]

for i in range(4):
    with cols[i]:
        st.markdown(
            f"""
            <div class='card'>
              <div style='font-size:40px'>{titles[i]["emoji"]}</div>
              <h3 style='margin:6px 0'>{titles[i]["title"]}</h3>
              <p>Demo siap presentasi untuk klien.</p>
              <p><em>Gunakan menu di sidebar untuk navigasi.</em></p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("### Kenapa Kelar.in?")
st.markdown("""
- <span class='k-badge'>On-Prem AI</span> <span class='k-badge'>Scraping</span> <span class='k-badge'>BI & Dashboard</span>  
- Integrasi **Qdrant**, **Open-WebUI**, **MSSQL/PostgreSQL**, **Node-RED**, **Grafana**  
- Fokus solusi nyata: cepat, aman, bisa di-scale
""", unsafe_allow_html=True)
