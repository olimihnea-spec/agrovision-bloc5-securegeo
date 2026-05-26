"""
BLOC 5 — AI Aplicat
Pagina principala
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import pandas as pd
# Forteaza backend numpy standard (fix compatibilitate Python 3.14 + PyArrow)
try:
    pd.options.future.infer_string = False
except AttributeError:
    pass

import streamlit as st
from datetime import date

st.set_page_config(
    page_title="AI Aplicat — Bloc 5",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:40px;'>🤖</div>
    <div style='font-size:18px; font-weight:700; color:#8e44ad;'>AI APLICAT</div>
    <div style='font-size:11px; color:#666;'>Inteligenta Artificiala pe Resurse Gratuite</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Prof. Asoc. Dr. Oliviu Mihnea Gamulescu")
st.sidebar.caption("UCB Targu Jiu | APIA CJ Gorj")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 30 / 30 zile — COMPLET")
st.sidebar.progress(30/30)
st.sidebar.markdown(f"**Data curenta:** {date.today().strftime('%d.%m.%Y')}")

st.markdown("""
<div style='background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#388E3C 100%);
     border-radius:14px; padding:16px 22px; margin-bottom:18px; color:white;
     border:2px solid #A5D6A7; box-shadow:0 4px 15px rgba(27,94,32,0.3);'>
    <div style='font-size:11px; opacity:0.85; letter-spacing:1.5px; text-transform:uppercase;
         margin-bottom:5px;'>
        PUBLICATIE ACCEPTATA OFICIAL — 25 mai 2026
    </div>
    <div style='font-size:14px; font-weight:800; line-height:1.5; margin-bottom:8px;
         font-style:italic;'>
        "Agricultural Risk Assessment Using Drone Imagery and Deep Learning:
        A Case Study of the AgroVision Application in Gorj County, Romania"
    </div>
    <div style='font-size:13px; font-weight:700; line-height:1.4; margin-bottom:5px;'>
        Scientific Papers Series Management, Economic Engineering
        in Agriculture and Rural Development
    </div>
    <div style='font-size:13px; opacity:0.9; line-height:1.6;'>
        Vol. 26, Issue 3, 2026 &nbsp;|&nbsp;
        PRINT ISSN 2284-7995 &nbsp;|&nbsp; E-ISSN 2285-3952 &nbsp;|&nbsp;
        USAMVB Bucuresti &nbsp;|&nbsp; BDI Indexat
    </div>
    <div style='font-size:12px; opacity:0.8; margin-top:6px;'>
        Editor: Prof. Dr. Agatha Popescu (popescu.agatha@managusamv.ro) &nbsp;|&nbsp;
        Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu &nbsp;|&nbsp;
        Publicare: octombrie 2026
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:16px;'>
    <div style='font-size:56px;'>🤖</div>
    <div>
        <h1 style='margin:0; font-size:32px; color:#8e44ad; font-weight:800;'>
            AI APLICAT v1.0
        </h1>
        <p style='margin:0; color:#546e7a; font-size:15px;'>
            Inteligenta Artificiala pe resurse 100% gratuite
            &nbsp;|&nbsp; 30 zile &nbsp;|&nbsp;
            UCB Targu Jiu &nbsp;|&nbsp; APIA CJ Gorj
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #6c3483 0%, #1a5276 100%);
     border-radius:12px; padding:18px 22px; margin-bottom:16px; color:white;'>
    <div style='font-size:13px; opacity:0.8; margin-bottom:4px;'>
        Baza teoretica si aplicativa a acestui program
    </div>
    <div style='font-size:17px; font-weight:700; line-height:1.4;'>
        "Contributii privind recunoasterea automata a culturilor
        cu ajutorul unei Drone"
    </div>
    <div style='font-size:12px; opacity:0.75; margin-top:6px;'>
        Teza de doctorat &nbsp;|&nbsp;
        Prof. Asoc. Dr. Oliviu Mihnea Gamulescu &nbsp;|&nbsp;
        Universitatea din Petrosani, 2024
    </div>
</div>
""", unsafe_allow_html=True)

st.info("""
**AI Aplicat** este un program practic de 30 de zile construit pe baza cercetarii din teza de doctorat.
Fiecare instrument — clasificare culturi, detectie YOLO, analiza NDVI — are corespondent direct
in metodologia aplicata pe parcele agricole din judetul Gorj cu ajutorul dronelor.
Toate instrumentele ruleaza local sau pe servicii gratuite, fara costuri.
""")

# ── CERCETARE ISI — acces rapid ─────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#0D47A1 0%,#1565C0 60%,#283593 100%);
     border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:1rem; color:white;'>
  <div style='font-size:0.8rem; opacity:0.8; margin-bottom:0.4rem;'>
    🆕 NOU — Cercetare ISI originala 2026
  </div>
  <div style='font-size:1.15rem; font-weight:800; margin-bottom:0.3rem;'>
    🛰️ Geolocalizare Fantomă & Securitate Geospațială
  </div>
  <div style='font-size:0.85rem; opacity:0.9;'>
    Phantom Geolocation · AGRO-GEO TRUST Framework · PGRS · Anti-Spoofing · Anti-Tampering · Anti-Sniffing
  </div>
</div>
""", unsafe_allow_html=True)

col_r1, col_r2, col_r3 = st.columns([1, 1, 1])
with col_r1:
    st.page_link(
        "pages/32_PhantomGeo_Research.py",
        label="🛰️  PhantomGeo Research — Articol ISI",
    )
with col_r2:
    st.page_link(
        "pages/31_SecureGeo_Defense.py",
        label="🔐  SecureGeo Defense — Anti-Spoofing/Tampering",
    )
with col_r3:
    st.page_link(
        "pages/10b_SecureGeo_Platform.py",
        label="🗺️  SecureGeo Platform — Harta GNSS",
    )

st.divider()

# ── DESCOPERIRI CHEIE CERCETARE ISI ─────────────────────────────────
st.subheader("🔬 Descoperiri cheie — Cercetare ISI 2026: Geolocalizare Fantomă")

st.markdown("""
<div style='background:#E3F2FD; border-left:5px solid #1565C0; border-radius:8px;
     padding:0.9rem 1.2rem; margin-bottom:1rem; font-size:0.9rem; line-height:1.6;'>
  <strong>Definiție formală introdusă:</strong>
  Un eveniment de <em>Geolocalizare Fantomă (GF)</em> apare când coordonatele (φ, λ, h) încorporate
  în metadatele EXIF ale imaginii la momentul achiziției <strong>t₁</strong> corespund unui fix GNSS
  obținut la un moment anterior <strong>t₀ &lt; t₁</strong>, din cauza pierderii semnalului în
  intervalul [t₀, t₁] — generând dovezi geospațiale aparent valide, dar contextual false.<br>
  <code style='background:#BBDEFB; padding:0.15rem 0.4rem; border-radius:4px;'>
    GF(I) = ADEVĂRAT ⟺ ||P_EXIF(I) − P_actual(I)|| &gt; ε_GNSS
  </code>
</div>
""", unsafe_allow_html=True)

d1, d2, d3, d4, d5 = st.columns(5)
rezultate = [
    ("EXP04 Dubai\n(OPPO)", "100%", "#C62828", "FM-1, FM-2\nPGRS = 0.11\nFANTOMĂ"),
    ("EXP07 Istanbul\n(OPPO)", "84.2%", "#D32F2F", "FM-1, FM-2\nPGRS = 0.18\nFANTOMĂ"),
    ("EXP07 Istanbul\n(Samsung)", "3.6%", "#2E7D32", "FM-1\nPGRS = 0.79\nCONDIȚIONAT"),
    ("EXP10 Lisabona\n(Samsung)", "4.7%", "#388E3C", "FM-1\nPGRS = 0.81\nCONDIȚIONAT"),
    ("EXP11 Târgu Jiu\n(Samsung)", "15.0%", "#F57F17", "FM-1, FM-3\nPGRS = 0.71\nCONDIȚIONAT"),
]
for col, (exp, pgr, color, detalii) in zip([d1,d2,d3,d4,d5], rezultate):
    with col:
        st.markdown(f"""
<div style='background:{color}; color:white; border-radius:10px; padding:0.8rem;
     text-align:center; font-size:0.78rem; line-height:1.5;'>
  <div style='font-size:0.75rem; opacity:0.85; margin-bottom:0.3rem;'>{exp}</div>
  <div style='font-size:1.6rem; font-weight:900; line-height:1;'>PGR<br>{pgr}</div>
  <div style='font-size:0.7rem; opacity:0.85; margin-top:0.3rem;
       white-space:pre-line;'>{detalii}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

ccc1, ccc2, ccc3 = st.columns(3)
with ccc1:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:1rem;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #0D47A1;'>
  <div style='font-weight:700; color:#0D47A1; margin-bottom:0.5rem;'>
    🏗️ AGRO-GEO TRUST Framework
  </div>
  <div style='font-size:0.83rem; color:#444; line-height:1.6;'>
    <strong>Strat 1:</strong> Geo-Integrity Layer<br>
    <strong>Strat 2:</strong> Metadata Trust Layer<br>
    <strong>Strat 3:</strong> Secure Transmission Layer<br>
    <strong>Strat 4:</strong> AI Validation Layer
  </div>
</div>""", unsafe_allow_html=True)

with ccc2:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:1rem;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #6A1B9A;'>
  <div style='font-weight:700; color:#6A1B9A; margin-bottom:0.5rem;'>
    📊 Phantom Geolocation Risk Score
  </div>
  <div style='font-size:0.83rem; color:#444; line-height:1.6;'>
    <strong>Formula:</strong> PGRS ∈ [0, 1]<br>
    7 sub-indicatori ponderați<br>
    <strong>TRUSTED:</strong> PGRS ≥ 0.85<br>
    <strong>FANTOMĂ:</strong> PGRS &lt; 0.40<br>
    <em>Calculator interactiv disponibil →</em>
  </div>
</div>""", unsafe_allow_html=True)

with ccc3:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:1rem;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #B71C1C;'>
  <div style='font-weight:700; color:#B71C1C; margin-bottom:0.5rem;'>
    🔐 Dimensiuni de Securitate
  </div>
  <div style='font-size:0.83rem; color:#444; line-height:1.6;'>
    <strong>Anti-Spoofing:</strong> OSNMA Galileo, RAIM, IMU<br>
    <strong>Anti-Tampering:</strong> SHA-256, eIDAS, TPM<br>
    <strong>Anti-Sniffing:</strong> TLS 1.3, DTLS, VPN<br>
    <em>Aliniat AI Act Art. 10(3) — UE 2024/1689</em>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; font-size:0.78rem; color:#78909C; margin-top:0.5rem;'>
  © 2026 Oliviu Mihnea Gămulescu — Cercetare academică independentă, UCB Târgu Jiu.
  Articol ISI în pregătire pentru Remote Sensing / Sensors (MDPI, Q1/Q2).
</div>
""", unsafe_allow_html=True)

st.divider()

# KPI-uri
c1, c2, c3, c4 = st.columns(4)
kpi_style = """
<div style='background:white; border-radius:10px; padding:16px; text-align:center;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid {color};'>
    <div style='font-size:28px; font-weight:800; color:{color};'>{val}</div>
    <div style='font-size:12px; color:#666;'>{label}</div>
</div>"""

with c1:
    st.markdown(kpi_style.format(color="#8e44ad", val="30", label="Zile planificate"),
                unsafe_allow_html=True)
with c2:
    st.markdown(kpi_style.format(color="#2980b9", val="5",  label="Module tematice"),
                unsafe_allow_html=True)
with c3:
    st.markdown(kpi_style.format(color="#27ae60", val="30", label="Zile finalizate"),
                unsafe_allow_html=True)
with c4:
    st.markdown(kpi_style.format(color="#e74c3c", val="10+", label="Modele AI antrenate"),
                unsafe_allow_html=True)

st.divider()

# Tehnologii folosite
st.subheader("Tehnologii — 100% gratuite")
tech = [
    ("scikit-learn",    "#3498db", "Machine Learning clasic — clasificare, regresie, clustering"),
    ("OpenCV",          "#27ae60", "Computer Vision — procesare imagini, detectie obiecte"),
    ("Hugging Face",    "#f39c12", "NLP — modele preantrenate, sentiment, rezumare"),
    ("Ollama",          "#8e44ad", "LLM local — Llama 3, Mistral ruleaza pe calculatorul tau"),
    ("LangChain",       "#e74c3c", "Agenti AI — automatizare fluxuri, RAG, chatboti pe documente"),
    ("Streamlit",       "#1abc9c", "Interfata web — aplicatii AI interactive in Python"),
]

cols = st.columns(3)
for i, (tech_name, culoare, desc) in enumerate(tech):
    with cols[i % 3]:
        st.markdown(f"""
        <div style='background:white; border-radius:10px; padding:14px; margin:6px 0;
             box-shadow:0 2px 8px rgba(0,0,0,0.06); border-left:4px solid {culoare};'>
            <div style='font-weight:700; color:{culoare}; font-size:14px;'>{tech_name}</div>
            <div style='font-size:12px; color:#555; margin-top:4px;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Plan 30 zile
st.subheader("Plan Bloc 5 — 30 zile")

module = {
    "Modulul 1 (Zilele 1-6) — Machine Learning cu scikit-learn": [
        ("1",  "Clasificare culturi din date NDVI — KNN si SVM", True),
        ("2",  "Regresie — predictie productie agricola din date meteo", True),
        ("3",  "Clustering — grupare parcele APIA dupa profil vegetal", True),
        ("4",  "Evaluare modele — confusion matrix, ROC, cross-validation", True),
        ("5",  "Pipeline scikit-learn — preprocesare + model + export", True),
        ("6",  "Sinteza M1 + aplicatie interactiva ML", True),
    ],
    "Modulul 2 (Zilele 7-12) — Computer Vision cu OpenCV + YOLOv8": [
        ("7",  "YOLOv8 — detectie culturi agricole in imagini drone", True),
        ("8",  "OpenCV bazele — filtre, culori, Canny, Sobel, morfologie", True),
        ("9",  "Calcul NDVI din imagini multispectrale + harta culori", True),
        ("10", "Detectie anomalii in parcele — zone uscate, inundatii", True),
        ("11", "OCR Tesseract — extragere text din documente APIA", True),
        ("12", "Sinteza M2 + pipeline complet Computer Vision", True),
        ("14", "BONUS: Detectie contururi — arie (ha), perimetru, ID parcela", True),
    ],
    "Modulul 3 (Zilele 13-18) — NLP Aplicat cu Hugging Face": [
        ("13", "Introducere NLP — tokenizare, TF-IDF, Transformer, sentiment", True),
        ("15", "Clasificare texte agricole — Zero-Shot HF, 6 categorii APIA", True),
        ("16", "Rezumare automata — extractiva TF-IDF + abstractiva BART", True),
        ("17", "NER — extragere entitati: persoane, locatii, suprafete, NDVI", True),
        ("18", "Sinteza M3 — pipeline NLP complet", True),
    ],
    "Modulul 4 (Zilele 19-24) — AI Generativ Local": [
        ("19", "Ollama — modele LLM locale (Llama 3, Mistral) gratuit", True),
        ("20", "Generator rapoarte APIA cu LLM local", True),
        ("21", "Generare imagini AI — teorie si instrumente online", True),
        ("22", "Generator continut academic cu LLM", True),
        ("23", "RAG simplu — intreaba un document PDF", True),
        ("24", "Sinteza M4", True),
    ],
    "Modulul 5 (Zilele 25-30) — AI Agenti + Finalizare": [
        ("25", "Agenti AI — automatizare fluxuri cu LangChain", True),
        ("26", "Agent care cauta articole stiintifice automat", True),
        ("27", "Agent inspector APIA — analizeaza parcele din fisier", True),
        ("28", "Dashboard AI complet — toate instrumentele integrate", True),
        ("29", "Deploy pe Streamlit Cloud", True),
        ("30", "Certificat final + roadmap AI 2026-2027", True),
    ],
}

culori_module = {
    "Modulul 1": "#3498db",
    "Modulul 2": "#27ae60",
    "Modulul 3": "#f39c12",
    "Modulul 4": "#8e44ad",
    "Modulul 5": "#e74c3c",
}

for modul, zile in module.items():
    cheie = modul[:9]
    culoare_m = culori_module.get(cheie, "#666")
    st.markdown(f"""
    <div style='background:{culoare_m}; color:white; border-radius:8px;
         padding:10px 16px; font-weight:700; font-size:14px; margin:16px 0 8px 0;'>
        {modul}
    </div>""", unsafe_allow_html=True)
    for nr, desc, done in zile:
        icon   = "✅" if done else "⬜"
        bg     = "#d4edda" if done else "#f8f9fa"
        border = "#28a745" if done else "#dee2e6"
        color  = "#999" if not done else "#333"
        st.markdown(f"""
        <div style='background:{bg}; border-left:4px solid {border}; border-radius:8px;
             padding:8px 14px; margin:4px 0; font-size:13px; color:{color};'>
            {icon} <b>Ziua {nr}</b> — {desc}
        </div>""", unsafe_allow_html=True)

st.divider()
st.success(
    "**TOATE CELE 5 MODULE FINALIZATE** | 30 / 30 zile complete | "
    "Aplicatie live pe Streamlit Cloud | Cost total: 0 EUR"
)
