"""
BLOC 5 — AI Aplicat
Pagina principala
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

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
st.sidebar.markdown("**Progres:** 17 / 30 zile")
st.sidebar.progress(17/30)
st.sidebar.markdown(f"**Data curenta:** {date.today().strftime('%d.%m.%Y')}")

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
    st.markdown(kpi_style.format(color="#27ae60", val="17", label="Zile finalizate"),
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
        ("18", "Sinteza M3 — pipeline NLP complet", False),
    ],
    "Modulul 4 (Zilele 19-24) — AI Generativ Local": [
        ("19", "Ollama — modele LLM locale (Llama 3, Mistral) gratuit", False),
        ("20", "Generator rapoarte APIA cu LLM local", False),
        ("21", "Generare imagini gratuit — Stable Diffusion local", False),
        ("22", "Generator continut academic cu LLM", False),
        ("23", "RAG simplu — intreaba un document PDF", False),
        ("24", "Sinteza M4", False),
    ],
    "Modulul 5 (Zilele 25-30) — AI Agenti + Finalizare": [
        ("25", "Agenti AI — automatizare fluxuri cu LangChain", False),
        ("26", "Agent care cauta articole stiintifice automat", False),
        ("27", "Agent inspector APIA — analizeaza parcele din fisier", False),
        ("28", "Dashboard AI complet — toate instrumentele integrate", False),
        ("29", "Deploy pe Streamlit Cloud", False),
        ("30", "Certificat final + roadmap AI 2026-2027", False),
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
    "**Modul 1 (ML) si Modul 2 (CV) — FINALIZATE** | "
    "**Modul 3 (NLP) — in curs** (Z13, Z15, Z16, Z17 gata). "
    "Urmatoarea: **Ziua 18 — Sinteza NLP**."
)
