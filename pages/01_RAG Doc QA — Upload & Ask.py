import streamlit as st
import pandas as pd
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from openai import OpenAI

st.set_page_config(page_title="RAG Doc QA — Kelar.in", page_icon="📚", layout="wide")

st.title("📚 RAG Doc QA — Upload & Ask")
st.caption("Contoh tanya-jawab dokumen *tanpa* vector DB. Menggunakan OpenAI API langsung.")

# --- Helper: extract text ---
def extract_text(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(file)
        txt = []
        for page in reader.pages:
            try:
                txt.append(page.extract_text() or "")
            except Exception:
                pass
        return "\n".join(txt)
    elif name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        # txt fallback
        return file.read().decode("utf-8", errors="ignore")

def summarize_chunks(chunks, client, model="gpt-4o-mini"):
    # ringkas tiap chunk agar hemat token
    summarized = []
    for i, ch in enumerate(chunks, 1):
        prompt = f"Ringkas isi berikut secara padat (maks 5-7 kalimat), fokuskan ke fakta kunci.\n\n{ch}"
        resp = client.responses.create(
            model=model,
            input=[{"role":"user","content":prompt}]
        )
        summarized.append(resp.output_text.strip())
    return "\n\n".join(summarized)

def smart_split(text, max_chars=6000):
    # pecah teks panjang menjadi potongan
    text = text.replace("\r"," ")
    parts, cur = [], []
    size = 0
    for para in text.split("\n"):
        if size + len(para) + 1 > max_chars:
            parts.append("\n".join(cur))
            cur, size = [para], len(para)
        else:
            cur.append(para)
            size += len(para) + 1
    if cur:
        parts.append("\n".join(cur))
    return parts

uploaded = st.file_uploader("Upload dokumen (PDF/DOCX/TXT)", type=["pdf","docx","txt"], accept_multiple_files=True)
question = st.text_input("Pertanyaan Anda")
go = st.button("Jalankan Demo")

colL, colR = st.columns([2,1])
with colL:
    st.subheader("Hasil")

    if go:
        # cek API key
        if not st.secrets.get("OPENAI_API_KEY"):
            st.error("OPENAI_API_KEY belum diisi. Buka Settings → Secrets di Streamlit Cloud (atau .streamlit/secrets.toml) lalu isi.")
        else:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            # gabungkan teks dari dokumen
            texts, sources = [], []
            for f in uploaded or []:
                try:
                    t = extract_text(f)
                    if t.strip():
                        texts.append(t)
                        sources.append(f.name)
                except Exception as e:
                    st.warning(f"Gagal membaca {f.name}: {e}")

            if not texts:
                st.warning("Tidak ada teks yang bisa diproses. Pastikan file berisi teks.")
            else:
                # potong & ringkas agar hemat token
                chunks = smart_split("\n\n".join(texts), max_chars=5000)
                summary = summarize_chunks(chunks, client)

                # tanya ke OpenAI dengan konteks ringkasan
                sys_msg = (
                    "Kamu adalah asisten RAG sederhana. Jawab pertanyaan berdasarkan ringkasan yang diberikan. "
                    "Jika tidak cukup bukti, jawab jujur. Berikan jawaban singkat dan jelas."
                )
                user_msg = f"Konteks ringkas:\n{summary}\n\nPertanyaan: {question}"
                resp = client.responses.create(
                    model="gpt-4o-mini",
                    input=[
                        {"role":"system","content":sys_msg},
                        {"role":"user","content":user_msg}
                    ]
                )
                answer = resp.output_text.strip()
                st.success(answer)
                if sources:
                    st.caption("Sumber: " + ", ".join(sources))
    else:
        st.write("Tunggu pertanyaan…")

with colR:
    st.subheader("Status")
    st.write("• Mode: **OpenAI direct** (tanpa vector DB)")
    st.write("• Model: `gpt-4o-mini` (hemat & cepat)")
    st.write("• File didukung: PDF, DOCX, TXT")

st.divider()
st.markdown("**Catatan:** Versi ini contoh minimal. Produksi: tambahkan pemotongan cerdas, sitasi halaman, dan cache indexing.")
