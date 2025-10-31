# Kelar.in — Streamlit Portfolio Hub

A multipage Streamlit app showcasing portfolio-ready demos you can customize for client presentations.

## Features
- 🧭 Hub landing page with project cards
- 📄 4 example projects (RAG Doc QA, Price Intelligence, IoT Telemetry, BI Market Insights)
- 🧩 Clean, modular structure
- 🧪 Works offline with mock data; easy to wire to live sources (PostgreSQL, MSSQL, Qdrant, APIs)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
streamlit run app.py
```

## Project Pages
1. **RAG Doc QA** — Upload PDFs/DOCs, ask questions, show sources. Ready for Qdrant/OpenAI.
2. **Price Intelligence (Tokopedia)** — Load CSV sample, analyze price trends, brand share, scrape skeleton.
3. **IoT Telemetry Dashboard** — Simulated device data with real-time-like updates and anomaly flags.
4. **BI Market Insights** — Sales & marketing funnel sample with segmentation and cohort charts.

## Configure Keys (optional)
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY="sk-..."
QDRANT_URL="http://localhost:6333"
QDRANT_API_KEY=""
MSSQL_CONN="Driver={ODBC Driver 17 for SQL Server};Server=10.0.0.1;Database=db;UID=user;PWD=pass;"
```

---
© 2025 Kelar.in Studio
