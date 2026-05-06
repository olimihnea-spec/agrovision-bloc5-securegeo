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

data_finalizare = "06.05.2026"
data_azi = datetime.date.today().strftime("%d.%m.%Y")

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
# CERTIFICAT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 24px;
    border: 2px solid #f39c12;
    box-shadow: 0 8px 32px rgba(243,156,18,0.3);
    text-align: center;
    color: white;
'>
    <div style='font-size:13px; letter-spacing:4px; opacity:0.7; margin-bottom:8px;'>
        UNIVERSITATEA "CONSTANTIN BRANCUSI" TARGU JIU &nbsp;|&nbsp; APIA CJ GORJ
    </div>
    <div style='font-size:11px; letter-spacing:2px; opacity:0.5; margin-bottom:24px;'>
        CERTIFICAT DE ABSOLVIRE
    </div>

    <div style='font-size:15px; opacity:0.8; margin-bottom:8px;'>
        Se acorda prin prezenta
    </div>

    <div style='
        font-size:34px; font-weight:900;
        background: linear-gradient(90deg, #f39c12, #f1c40f, #f39c12);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 12px 0;
        line-height: 1.2;
    '>
        Prof. Asoc. Dr. Oliviu Mihnea Gamulescu
    </div>

    <div style='font-size:13px; opacity:0.75; margin-bottom:24px;'>
        Inspector Principal APIA CJ Gorj &nbsp;·&nbsp; Cadru Didactic UCB Targu Jiu
    </div>

    <div style='
        background: rgba(243,156,18,0.1);
        border: 1px solid rgba(243,156,18,0.3);
        border-radius: 10px;
        padding: 18px 28px;
        margin: 0 auto 24px auto;
        max-width: 600px;
    '>
        <div style='font-size:11px; letter-spacing:2px; opacity:0.6; margin-bottom:6px;'>
            PENTRU ABSOLVIREA PROGRAMULUI
        </div>
        <div style='font-size:22px; font-weight:800; color:#f1c40f;'>
            AI APLICAT — BLOC 5
        </div>
        <div style='font-size:13px; opacity:0.8; margin-top:4px;'>
            Inteligenta Artificiala pe Resurse 100% Gratuite
        </div>
    </div>

    <div style='display:grid; grid-template-columns: repeat(5, 1fr); gap:12px;
         margin-bottom:24px; max-width:700px; margin-left:auto; margin-right:auto;'>
        <div style='background:rgba(52,152,219,0.2); border-radius:8px; padding:10px; border-top:2px solid #3498db;'>
            <div style='font-size:11px; font-weight:700; color:#3498db;'>MODUL 1</div>
            <div style='font-size:9px; opacity:0.7; margin-top:2px;'>Machine Learning<br>scikit-learn</div>
        </div>
        <div style='background:rgba(39,174,96,0.2); border-radius:8px; padding:10px; border-top:2px solid #27ae60;'>
            <div style='font-size:11px; font-weight:700; color:#27ae60;'>MODUL 2</div>
            <div style='font-size:9px; opacity:0.7; margin-top:2px;'>Computer Vision<br>OpenCV + YOLO</div>
        </div>
        <div style='background:rgba(243,156,18,0.2); border-radius:8px; padding:10px; border-top:2px solid #f39c12;'>
            <div style='font-size:11px; font-weight:700; color:#f39c12;'>MODUL 3</div>
            <div style='font-size:9px; opacity:0.7; margin-top:2px;'>NLP<br>Hugging Face</div>
        </div>
        <div style='background:rgba(142,68,173,0.2); border-radius:8px; padding:10px; border-top:2px solid #8e44ad;'>
            <div style='font-size:11px; font-weight:700; color:#8e44ad;'>MODUL 4</div>
            <div style='font-size:9px; opacity:0.7; margin-top:2px;'>AI Generativ<br>Ollama + RAG</div>
        </div>
        <div style='background:rgba(231,76,60,0.2); border-radius:8px; padding:10px; border-top:2px solid #e74c3c;'>
            <div style='font-size:11px; font-weight:700; color:#e74c3c;'>MODUL 5</div>
            <div style='font-size:9px; opacity:0.7; margin-top:2px;'>Agenti AI<br>ReAct + Deploy</div>
        </div>
    </div>

    <div style='display:flex; justify-content:center; gap:40px; font-size:11px; opacity:0.7;'>
        <div>
            <div style='font-size:10px; letter-spacing:1px; opacity:0.6;'>DATA FINALIZARII</div>
            <div style='font-size:15px; font-weight:700; color:#f1c40f; margin-top:2px;'>{data_finalizare}</div>
        </div>
        <div>
            <div style='font-size:10px; letter-spacing:1px; opacity:0.6;'>DURATA</div>
            <div style='font-size:15px; font-weight:700; color:#f1c40f; margin-top:2px;'>30 zile</div>
        </div>
        <div>
            <div style='font-size:10px; letter-spacing:1px; opacity:0.6;'>COST TOTAL</div>
            <div style='font-size:15px; font-weight:700; color:#f1c40f; margin-top:2px;'>0 EUR</div>
        </div>
        <div>
            <div style='font-size:10px; letter-spacing:1px; opacity:0.6;'>INSTRUMENTE CONSTRUITE</div>
            <div style='font-size:15px; font-weight:700; color:#f1c40f; margin-top:2px;'>28 pagini live</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CE AM CONSTRUIT — SINTEZA COMPLETA
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("Ce am construit in 30 de zile")

col_s1, col_s2 = st.columns(2)

with col_s1:
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
    for culoare, titlu, itemi in module_sinteza:
        st.markdown(f"""
<div style='background:{culoare}15; border-left:4px solid {culoare};
     border-radius:6px; padding:10px 14px; margin-bottom:10px;'>
<div style='font-weight:700; color:{culoare}; font-size:12px; margin-bottom:6px;'>{titlu}</div>
{"".join(f'<div style="font-size:11px; color:#444; padding:1px 0;">✅ {it}</div>' for it in itemi)}
</div>
""", unsafe_allow_html=True)

with col_s2:
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
    for culoare, titlu, itemi in module_sinteza2:
        st.markdown(f"""
<div style='background:{culoare}15; border-left:4px solid {culoare};
     border-radius:6px; padding:10px 14px; margin-bottom:10px;'>
<div style='font-weight:700; color:{culoare}; font-size:12px; margin-bottom:6px;'>{titlu}</div>
{"".join(f'<div style="font-size:11px; color:#444; padding:1px 0;">✅ {it}</div>' for it in itemi)}
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style='background:linear-gradient(135deg,#f39c12,#e67e22);
     border-radius:8px; padding:12px 16px; color:white; margin-top:6px;'>
<div style='font-weight:800; font-size:13px;'>Statistici finale</div>
<div style='font-size:11px; margin-top:6px; line-height:1.9; opacity:0.95;'>
30 zile &nbsp;·&nbsp; 5 module &nbsp;·&nbsp; 28 pagini Streamlit<br>
10+ modele AI antrenate &nbsp;·&nbsp; 3 baze date academice<br>
1 aplicatie live pe Streamlit Cloud<br>
Cost total: <b>0 EUR</b>
</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROADMAP AI 2026-2027
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.subheader("Roadmap AI 2026-2027 — urmatorii pasi")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #3498db; height:100%;'>
<div style='font-weight:800; color:#3498db; font-size:13px; margin-bottom:10px;'>
    PUBLICATII ISI — 2026
</div>
<div style='font-size:11px; color:#444; line-height:1.9;'>

<b>In pregatire:</b><br>
• MDPI Drones (IF 4.4) — Phantom GPS<br>
• MDPI Sensors (IF 3.4) — GNSS fantoma<br>
• USAMV Vol.26 — AgroVision (acceptat)<br><br>

<b>De scris 2026-2027:</b><br>
• AI + control PAC — agent inspector APIA<br>
• RAG pentru documente agricole<br>
• Drone multispectrale + NDVI Romania<br>
• Dashboard AI pentru institutii publice<br><br>

<b>Reviste tinta:</b><br>
• Computers & Electronics in Agriculture<br>
• Remote Sensing (MDPI)<br>
• Precision Agriculture (Springer)
</div>
</div>
""", unsafe_allow_html=True)

with col_r2:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #27ae60; height:100%;'>
<div style='font-weight:800; color:#27ae60; font-size:13px; margin-bottom:10px;'>
    UCB TARGU JIU — Cursuri noi
</div>
<div style='font-size:11px; color:#444; line-height:1.9;'>

<b>Semestrul 1 (oct 2026):</b><br>
• AI si instrumente digitale<br>
  → Folosesti direct aplicatia Bloc5<br>
• Drone UAV in agricultura<br>
  → Metodologie din teza + AgroVision<br><br>

<b>Semestrul 2 (feb 2027):</b><br>
• Management risc in agricultura<br>
• Fonduri europene PAC 2023-2027<br>
• QGIS si sisteme informationale GIS<br><br>

<b>Materiale didactice gata:</b><br>
• Generator academic Z22 → suporturi curs<br>
• Agent articole Z26 → bibliografii<br>
• Dashboard Z28 → demo interactiv
</div>
</div>
""", unsafe_allow_html=True)

with col_r3:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid #8e44ad; height:100%;'>
<div style='font-weight:800; color:#8e44ad; font-size:13px; margin-bottom:10px;'>
    APIA + CERCETARE — 2027
</div>
<div style='font-size:11px; color:#444; line-height:1.9;'>

<b>Integrare APIA CJ Gorj:</b><br>
• Agent inspector Z27 → pilot intern<br>
• Rapoarte NDVI automatizate (Z20)<br>
• Dashboard parcele pentru control teren<br><br>

<b>Proiecte de cercetare:</b><br>
• UEFISCDI — propunere grant AI agricol<br>
• Parteneriat UCB + APIA + Prefectura<br>
• Colaborare Directii Agricole Gorj/Dolj<br><br>

<b>Certificari recomandate:</b><br>
• Google Cloud AI Fundamentals (gratuit)<br>
• DeepLearning.AI — AI for Everyone<br>
• Microsoft AI-900 (Azure AI)<br>
• Hugging Face NLP Course (gratuit)
</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MESAJ FINAL
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 14px;
    padding: 32px 40px;
    color: white;
    border: 1px solid rgba(243,156,18,0.4);
'>
    <div style='display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:20px;'>
        <div style='flex:2; min-width:300px;'>
            <div style='font-size:11px; letter-spacing:3px; opacity:0.6; margin-bottom:10px;'>
                MESAJ DE INCHEIERE
            </div>
            <div style='font-size:16px; font-weight:700; line-height:1.7; margin-bottom:16px;'>
                "Cel mai bun moment pentru a incepe sa inveti AI a fost acum 30 de zile.<br>
                Al doilea cel mai bun moment este acum."
            </div>
            <div style='font-size:12px; opacity:0.75; line-height:1.8;'>
                In 30 de zile ai trecut de la utilizator la <b>constructor de instrumente AI</b>.<br>
                Ai construit aplicatii care ruleaza complet offline, gratuit, pe calculatorul tau.<br>
                Le-ai deploy-at online. Le-ai integrat cu datele reale din teza de doctorat.<br><br>
                Urmatorul pas nu mai este sa <i>inveti</i> AI — este sa il <i>aplici</i>:<br>
                in sala de curs, in teren cu drona, in biroul APIA, in articolele ISI.
            </div>
        </div>
        <div style='flex:1; min-width:200px; text-align:right;'>
            <div style='font-size:13px; opacity:0.7; margin-bottom:8px;'>Finalizat:</div>
            <div style='font-size:20px; font-weight:800; color:#f1c40f;'>{data_finalizare}</div>
            <div style='font-size:11px; opacity:0.6; margin-top:16px; line-height:1.8;'>
                Prof. Asoc. Dr.<br>
                <b style='font-size:13px;'>Oliviu Mihnea Gamulescu</b><br>
                UCB Targu Jiu<br>
                APIA CJ Gorj
            </div>
            <div style='margin-top:16px; font-size:28px;'>AI</div>
            <div style='font-size:10px; opacity:0.5; letter-spacing:2px;'>APLICAT COMPLET</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
