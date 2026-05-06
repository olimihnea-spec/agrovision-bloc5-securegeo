"""
Ziua 30 — Certificat Final + Roadmap AI 2026-2027
Modul 5: AI Agenti + Finalizare
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime

st.set_page_config(
    page_title="Ziua 30 — Certificat Final",
    page_icon="CERT",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_FINALIZARE = "06.05.2026"

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#f39c12;'>CERT</div>
    <div style='font-size:16px; font-weight:700; color:#f39c12;'>ZIUA 30</div>
    <div style='font-size:11px; color:#666;'>Certificat Final</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.progress(30 / 30)
st.sidebar.success("30 / 30 zile — COMPLET")
st.sidebar.divider()
st.sidebar.caption("Prof. Asoc. Dr. Oliviu Mihnea Gamulescu")
st.sidebar.caption("UCB Targu Jiu | APIA CJ Gorj")

# ══════════════════════════════════════════════════════════════════════════════
# HEADER CERTIFICAT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='background:#1a1a2e; border-radius:16px; padding:14px 28px 6px 28px;
     border:2px solid #f39c12; text-align:center; color:white; margin-bottom:4px;'>
    <div style='font-size:12px; letter-spacing:3px; opacity:0.6; margin-bottom:4px;'>
        UNIVERSITATEA "CONSTANTIN BRANCUSI" TARGU JIU &nbsp;|&nbsp; APIA CJ GORJ
    </div>
    <div style='font-size:10px; letter-spacing:2px; opacity:0.4; margin-bottom:14px;'>
        CERTIFICAT DE ABSOLVIRE
    </div>
    <div style='font-size:13px; opacity:0.75; margin-bottom:6px;'>Se acorda prin prezenta</div>
    <div style='font-size:30px; font-weight:900; color:#f1c40f; margin:10px 0;'>
        Prof. Asoc. Dr. Oliviu Mihnea Gamulescu
    </div>
    <div style='font-size:12px; opacity:0.7; margin-bottom:14px;'>
        Consilier Superior APIA CJ Gorj &nbsp;·&nbsp; Cadru Didactic UCB Targu Jiu
    </div>
    <div style='background:rgba(243,156,18,0.1); border:1px solid rgba(243,156,18,0.3);
         border-radius:10px; padding:14px 20px; display:inline-block; margin-bottom:16px;'>
        <div style='font-size:10px; letter-spacing:2px; opacity:0.6; margin-bottom:4px;'>
            PENTRU ABSOLVIREA PROGRAMULUI
        </div>
        <div style='font-size:20px; font-weight:800; color:#f1c40f;'>AI APLICAT — BLOC 5</div>
        <div style='font-size:12px; opacity:0.8; margin-top:4px;'>
            Inteligenta Artificiala pe Resurse 100% Gratuite
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Cele 5 module ─────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
module_cert = [
    (c1, "#3498db", "MODUL 1", "Machine Learning", "scikit-learn"),
    (c2, "#27ae60", "MODUL 2", "Computer Vision", "OpenCV + YOLO"),
    (c3, "#f39c12", "MODUL 3", "NLP", "Hugging Face"),
    (c4, "#8e44ad", "MODUL 4", "AI Generativ", "Ollama + RAG"),
    (c5, "#e74c3c", "MODUL 5", "Agenti AI", "ReAct + Deploy"),
]
for col, culoare, cod, titlu, tech in module_cert:
    with col:
        st.markdown(f"""
<div style='background:#1a1a2e; border-radius:8px; padding:10px 6px;
     border-top:3px solid {culoare}; text-align:center; color:white;'>
    <div style='font-size:11px; font-weight:700; color:{culoare};'>{cod}</div>
    <div style='font-size:10px; opacity:0.8; margin-top:3px;'>{titlu}</div>
    <div style='font-size:9px; opacity:0.5; margin-top:2px;'>{tech}</div>
</div>
""", unsafe_allow_html=True)

# ── Statistici ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#16213e; border-radius:10px; padding:14px 28px;
     border:1px solid rgba(243,156,18,0.25); margin-top:4px; margin-bottom:4px;'>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
stat = """<div style='text-align:center;'>
    <div style='font-size:10px; letter-spacing:1px; color:#888;'>{label}</div>
    <div style='font-size:18px; font-weight:800; color:#f1c40f; margin-top:2px;'>{val}</div>
</div>"""
with s1: st.markdown(stat.format(label="DATA FINALIZARII", val=DATA_FINALIZARE), unsafe_allow_html=True)
with s2: st.markdown(stat.format(label="DURATA", val="30 zile"), unsafe_allow_html=True)
with s3: st.markdown(stat.format(label="COST TOTAL", val="0 EUR"), unsafe_allow_html=True)
with s4: st.markdown(stat.format(label="PAGINI CONSTRUITE", val="30 live"), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# CE AM CONSTRUIT
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("Ce am construit in 30 de zile")

col_st1, col_st2 = st.columns(2)

module_sinteza = [
    ("#3498db", "MODUL 1 — Machine Learning (Z1-Z6)", [
        "Clasificare culturi NDVI cu KNN si SVM",
        "Regresie: predictie productie agricola",
        "Clustering: grupare parcele APIA",
        "Evaluare: confusion matrix, ROC, cross-validation",
        "Pipeline scikit-learn complet exportabil",
    ]),
    ("#27ae60", "MODUL 2 — Computer Vision (Z7-Z12+Z14)", [
        "YOLOv8: detectie culturi in imagini drone",
        "OpenCV: filtre, Canny, morfologie, contururi",
        "Calcul NDVI din imagini multispectrale",
        "Detectie anomalii: zone uscate, inundatii",
        "OCR Tesseract: extragere text documente APIA",
    ]),
    ("#f39c12", "MODUL 3 — NLP cu Hugging Face (Z13-Z18)", [
        "Tokenizare, TF-IDF, Transformers",
        "Clasificare Zero-Shot: 6 categorii APIA",
        "Rezumare automata: TF-IDF + BART",
        "NER: persoane, locatii, suprafete, NDVI",
        "Pipeline NLP complet pentru documente agricole",
    ]),
]
module_sinteza2 = [
    ("#8e44ad", "MODUL 4 — AI Generativ Local (Z19-Z24)", [
        "Ollama: LLM local gratuit (Llama3, Mistral)",
        "Generator rapoarte APIA cu penalizari PAC",
        "Generare imagini AI: teorie + instrumente online",
        "Generator academic UCB: 5 tipuri materiale",
        "RAG: intreaba orice document PDF",
    ]),
    ("#e74c3c", "MODUL 5 — Agenti AI + Finalizare (Z25-Z30)", [
        "Agent ReAct manual: 4 instrumente + DuckDuckGo",
        "Agent articole: Semantic Scholar + arXiv + CrossRef",
        "Agent inspector APIA: CSV → raport neconformitati",
        "Dashboard AI complet: toate modulele integrate",
        "Deploy Streamlit Cloud: aplicatie live publica",
    ]),
]

with col_st1:
    for culoare, titlu, itemi in module_sinteza:
        items_html = "".join(
            f'<div style="font-size:11px; color:#333; padding:2px 0;">&#10003; {it}</div>'
            for it in itemi
        )
        st.markdown(f"""
<div style='background:{culoare}12; border-left:4px solid {culoare};
     border-radius:6px; padding:10px 14px; margin-bottom:10px;'>
<div style='font-weight:700; color:{culoare}; font-size:12px; margin-bottom:6px;'>{titlu}</div>
{items_html}
</div>
""", unsafe_allow_html=True)

with col_st2:
    for culoare, titlu, itemi in module_sinteza2:
        items_html = "".join(
            f'<div style="font-size:11px; color:#333; padding:2px 0;">&#10003; {it}</div>'
            for it in itemi
        )
        st.markdown(f"""
<div style='background:{culoare}12; border-left:4px solid {culoare};
     border-radius:6px; padding:10px 14px; margin-bottom:10px;'>
<div style='font-weight:700; color:{culoare}; font-size:12px; margin-bottom:6px;'>{titlu}</div>
{items_html}
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style='background:linear-gradient(135deg,#f39c12,#e67e22);
     border-radius:8px; padding:12px 16px; color:white;'>
<div style='font-weight:800; font-size:13px; margin-bottom:6px;'>Statistici finale</div>
<div style='font-size:11px; line-height:1.9; opacity:0.95;'>
30 zile &nbsp;·&nbsp; 5 module &nbsp;·&nbsp; 30 pagini Streamlit<br>
10+ modele AI &nbsp;·&nbsp; 3 baze de date academice<br>
1 aplicatie live pe Streamlit Cloud &nbsp;·&nbsp; <b>0 EUR</b>
</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.subheader("Roadmap AI 2026-2027 — urmatorii pasi")

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #3498db;'>
<div style='font-weight:800; color:#3498db; font-size:13px; margin-bottom:10px;'>
    PUBLICATII ISI — 2026
</div>
<div style='font-size:11px; color:#444; line-height:1.9;'>
<b>In pregatire:</b><br>
&#8226; MDPI Drones (IF 4.4) — Phantom GPS<br>
&#8226; MDPI Sensors (IF 3.4) — GNSS fantoma<br>
&#8226; USAMV Vol.26 — AgroVision (acceptat)<br><br>
<b>De scris 2026-2027:</b><br>
&#8226; AI + control PAC — agent inspector APIA<br>
&#8226; RAG pentru documente agricole<br>
&#8226; Drone multispectrale + NDVI Romania<br><br>
<b>Reviste tinta:</b><br>
&#8226; Computers &amp; Electronics in Agriculture<br>
&#8226; Remote Sensing (MDPI)<br>
&#8226; Precision Agriculture (Springer)
</div>
</div>
""", unsafe_allow_html=True)

with r2:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #27ae60;'>
<div style='font-weight:800; color:#27ae60; font-size:13px; margin-bottom:10px;'>
    UCB TARGU JIU — Cursuri noi
</div>
<div style='font-size:11px; color:#444; line-height:1.9;'>
<b>Semestrul 1 (oct 2026):</b><br>
&#8226; AI si instrumente digitale<br>
&#8226; Drone UAV in agricultura<br><br>
<b>Semestrul 2 (feb 2027):</b><br>
&#8226; Management risc in agricultura<br>
&#8226; Fonduri europene PAC 2023-2027<br>
&#8226; QGIS si sisteme geografice<br><br>
<b>Materiale gata (din aceasta aplicatie):</b><br>
&#8226; Generator academic Z22 &#8594; suporturi curs<br>
&#8226; Agent articole Z26 &#8594; bibliografii<br>
&#8226; Dashboard Z28 &#8594; demo interactiv
</div>
</div>
""", unsafe_allow_html=True)

with r3:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #8e44ad;'>
<div style='font-weight:800; color:#8e44ad; font-size:13px; margin-bottom:10px;'>
    APIA + CERCETARE — 2027
</div>
<div style='font-size:11px; color:#444; line-height:1.9;'>
<b>Integrare APIA CJ Gorj:</b><br>
&#8226; Agent inspector Z27 &#8594; pilot intern<br>
&#8226; Rapoarte NDVI automatizate (Z20)<br>
&#8226; Dashboard parcele pentru control<br><br>
<b>Proiecte de cercetare:</b><br>
&#8226; Grant UEFISCDI — AI agricol<br>
&#8226; Parteneriat UCB + APIA + Prefectura<br>
&#8226; Directii Agricole Gorj / Dolj / Olt<br><br>
<b>Certificari recomandate:</b><br>
&#8226; Google Cloud AI Fundamentals<br>
&#8226; Hugging Face NLP Course<br>
&#8226; Microsoft AI-900
</div>
</div>
""", unsafe_allow_html=True)
