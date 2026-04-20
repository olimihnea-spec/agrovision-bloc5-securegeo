"""
GDPR & Disclaimer — Nota de conformitate si transparenta
Bloc 5 AI Aplicat
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime

st.set_page_config(
    page_title="GDPR & Disclaimer",
    page_icon="GDPR",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:32px;'>GDPR</div>
    <div style='font-size:14px; font-weight:700; color:#1a5276;'>DISCLAIMER</div>
    <div style='font-size:10px; color:#666;'>Nota de conformitate si transparenta</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.markdown("**Bloc 5 AI Aplicat** | UCB Targu Jiu")
st.sidebar.divider()
st.sidebar.markdown("""
**Sectiuni:**
- Sursa datelor
- Confidentialitate
- Date personale
- Drept de autor
- Contact
""")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#117a65 100%);
     border-radius:12px; padding:20px 28px; color:white; margin-bottom:20px;'>
    <div style='font-size:24px; font-weight:900; letter-spacing:1px;'>
        GDPR & Disclaimer — Nota de Conformitate si Transparenta
    </div>
    <div style='font-size:13px; margin-top:6px; opacity:0.9;'>
        Bloc 5 AI Aplicat | Prof. Asoc. Dr. Oliviu Mihnea Gamulescu
    </div>
    <div style='font-size:11px; margin-top:4px; opacity:0.7;'>
        Universitatea Constantin Brancusi, Targu Jiu |
        APIA Centrul Judetean Gorj | Ultima actualizare: 21 aprilie 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTIUNEA 1 — SURSA DATELOR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 1. Sursa datelor si a studiilor")

st.markdown("""
<div style='background:#eaf4fb; border-left:5px solid #1a5276; border-radius:0 10px 10px 0;
     padding:18px 24px; font-size:13px; line-height:1.9; margin-bottom:16px;'>

<b style='color:#1a5276; font-size:15px;'>Declaratie de transparenta privind originea datelor</b><br><br>

Toate informatiile, studiile, experimentele, algoritmii si rezultatele prezentate
in aceasta platforma au la baza <b>experienta profesionala proprie</b> a autorului,
acumulata in cele doua roluri simultane:

<ul style='margin-top:10px; line-height:2.1;'>
<li><b>Consilier Superior APIA</b> — Centrul Judetean Gorj, Serviciul Control pe Teren
(peste 20 de ani de activitate, din momentul constituirii agentiei)</li>
<li><b>Profesor Asociat / Cercetator</b> — Universitatea Constantin Brancusi, Targu Jiu,
Doctor in Ingineria Sistemelor, Universitatea din Petrosani (2024)</li>
<li><b>Absolvent curs postuniversitar</b> — Managementul Protectiei Infrastructurii Critice,
Academia Fortelor Terestre "Nicolae Balcescu", Sibiu</li>
<li><b>Membru Centrul Suport Situatii de Urgenta</b> — Prefectura Gorj
(Ordinul Prefectului nr. 154/17.03.2025)</li>
</ul>

<b style='color:#c0392b;'>Aceasta platforma NU utilizeaza, NU acceseaza si NU prelucreaza
date din bazele de date oficiale ale APIA</b> (IACS, LPIS, AMS sau orice alt sistem
informatic institutional).

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449; font-size:13px; margin-bottom:10px;'>
    Ce FOLOSESTE aceasta platforma
</div>
<div style='font-size:12px; line-height:1.9; color:#333;'>
<b>Date sintetice generate artificial</b><br>
→ Seturi de date simulate, create pentru scopuri educationale<br><br>
<b>Date din experiente proprii documentate</b><br>
→ Fotografii aeriene realizate personal (zbor Roma-Bucuresti, 18 apr 2026)<br>
→ Observatii de teren din activitatea de inspector<br>
→ Cunostinte dobandite din 20+ ani de control agricol<br><br>
<b>Date publice / open-source</b><br>
→ Imagini satelitare publice (Sentinel-2, Google Earth demo)<br>
→ Regulamente UE si ghiduri APIA publice<br>
→ Modele AI pre-antrenate (Hugging Face, YOLOv8 — licente deschise)<br><br>
<b>Date colectate personal</b><br>
→ EXIF din fotografii proprii (Samsung Galaxy A72)<br>
→ Trasee GPS personale, fara date ale tertilor
</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:4px solid #c0392b;'>
<div style='font-weight:700; color:#922b21; font-size:13px; margin-bottom:10px;'>
    Ce NU FOLOSESTE aceasta platforma
</div>
<div style='font-size:12px; line-height:1.9; color:#333;'>
<b>Baze de date APIA institutionale</b><br>
→ NU accesam IACS (Integrated Administration and Control System)<br>
→ NU accesam LPIS (Land Parcel Identification System)<br>
→ NU accesam AMS (Area Monitoring System)<br>
→ NU accesam datele fermierilor din cereri PAC reale<br><br>
<b>Date cu caracter personal ale tertilor</b><br>
→ NU procesam CNP-uri sau IBAN-uri reale ale fermierilor<br>
→ NU accesam registre cadastrale sau ANCPI<br>
→ NU procesam date de identificare ale persoanelor fizice<br><br>
<b>Sisteme securizate ale statului</b><br>
→ NU accesam niciun sistem informatic institutional<br>
→ NU folosim credentiale de serviciu in aplicatii civile
</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTIUNEA 2 — CONFIDENTIALITATE
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown("## 2. Confidentialitate si prelucrarea datelor")

st.markdown("""
<div style='background:#fef9e7; border-left:5px solid #f39c12; border-radius:0 10px 10px 0;
     padding:16px 22px; font-size:12px; line-height:1.8;'>

<b>Aceasta platforma este un instrument academic si educational.</b>
Nu colecteaza, nu stocheaza si nu transmite date cu caracter personal catre terti.<br><br>

<b>Streamlit Cloud (platforma de hosting):</b> Utilizeaza cookie-uri tehnice strict necesare
pentru functionare. Nu se stocheaza date ale utilizatorilor pe serverele noastre.
Consultati politica de confidentialitate Streamlit: <i>streamlit.io/privacy-policy</i><br><br>

<b>Imaginile incarcate de utilizator</b> in sectiunile de analiza (OCR, NDVI, Contururi)
sunt procesate exclusiv in sesiunea curenta, in memorie, si nu sunt salvate sau transmise.<br><br>

<b>Datele introduse in campurile de text</b> (documente APIA demo, texte NLP) sunt
procesate local si nu sunt stocate dupa inchiderea sesiunii.

</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTIUNEA 3 — DATE PERSONALE IN STUDII
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown("## 3. Date personale in studii si exemple")

st.markdown("""
<div style='background:#f9ebea; border-left:5px solid #c0392b; border-radius:0 10px 10px 0;
     padding:16px 22px; font-size:12px; line-height:1.8; margin-bottom:12px;'>

Toate documentele demo, exemplele de cereri PAC, rapoarte de control si notificari
de neconformitate utilizate in aceasta platforma sunt <b>fictive</b> — generate artificial
in scop educational. Orice asemanare cu persoane reale, CNP-uri reale, IBAN-uri reale
sau parcele LPIS reale este <b>pur intamplatoare</b> si <b>neinventionata</b>.<br><br>

Coordonatele GPS si datele EXIF utilizate in sectiunea SecureGeo Platform provin
exclusiv din fotografii realizate personal de autor in zboruri comerciale proprii,
<b>fara a implica date ale altor persoane</b>.

</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTIUNEA 4 — DREPT DE AUTOR
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown("## 4. Drept de autor si utilizare")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); font-size:12px; line-height:1.8;'>
<b style='color:#1a5276;'>Autorul platformei</b><br><br>
Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br><br>
<b>Academic:</b><br>
Profesor Asociat — Universitatea Constantin Brancusi, Targu Jiu<br>
Facultatea de Inginerie | Master Managementul Riscului in Agricultura (MRA)<br><br>
<b>Profesional APIA:</b><br>
Consilier Superior — APIA Centrul Judetean Gorj<br>
Serviciul Control pe Teren (20+ ani, din momentul constituirii agentiei)<br><br>
<b>Formare militara si securitate:</b><br>
Absolvent curs postuniversitar:<br>
<i>Managementul Protectiei Infrastructurii Critice</i><br>
Academia Fortelor Terestre "Nicolae Balcescu", Sibiu<br><br>
Membru — Centrul Suport al Situatiilor de Urgenta<br>
Prefectura Gorj (Ordinul Prefectului nr. 154/17.03.2025)<br><br>
<b>Teza de doctorat:</b><br>
<i>"Contributii privind recunoasterea automata a culturilor
cu ajutorul unei Drone"</i><br>
Universitatea din Petrosani, 2024
</div>
""", unsafe_allow_html=True)

with col4:
    st.markdown("""
<div style='background:white; border-radius:10px; padding:16px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); font-size:12px; line-height:1.8;'>
<b style='color:#1a5276;'>Utilizare permisa</b><br><br>
Aceasta platforma este destinata exclusiv:<br>
- Activitatilor educationale si de cercetare<br>
- Demonstratiilor la cursurile UCB (Master MRA)<br>
- Diseminarii rezultatelor cercetarii proprii<br>
- Propunerilor de proiecte (ACE2-EU, UEFISCDI)<br><br>
<b style='color:#c0392b;'>Utilizare interzisa:</b><br>
- Procesarea datelor reale ale fermierilor<br>
- Utilizarea ca instrument oficial de control APIA<br>
- Reproducerea comerciala fara acordul autorului<br>
- Inlocuirea procedurilor oficiale APIA/MADR
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTIUNEA 5 — BAZA LEGALA
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown("## 5. Baza legala si referinte")

st.markdown("""
| Document | Relevanta |
|---|---|
| Regulamentul UE 2016/679 (GDPR) | Protectia datelor cu caracter personal |
| Regulamentul UE 2021/2116 | PAC — Gestiune si control |
| Regulamentul UE 2022/1173 | Area Monitoring System (AMS) |
| EASA Reg. 2019/947 | Operatiuni drone categoria OPEN |
| Legea 190/2018 | Masuri nationale GDPR — Romania |
| Legea 8/1996 | Drept de autor si drepturi conexe — Romania |
""")

# ══════════════════════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown("""
<div style='background:#eaf4fb; border-radius:10px; padding:16px 22px; font-size:12px;'>
<b style='color:#1a5276; font-size:13px;'>Contact & Intrebari privind aceasta platforma</b><br><br>
Pentru orice intrebare referitoare la datele utilizate, metodologia cercetarii
sau conformitatea GDPR a acestei platforme:<br><br>
<b>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu</b><br>
Email academic: disponibil prin UCB Targu Jiu<br>
Email personal: olimihnea@gmail.com<br>
Email profesional: oliviu.gamulescu@apia.ro<br><br>
<i>Aceasta nota de conformitate a fost redactata la data de 21 aprilie 2026
si va fi actualizata periodic.</i>
</div>
""", unsafe_allow_html=True)
