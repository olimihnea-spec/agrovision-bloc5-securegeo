"""
Ziua 18 — Sinteza Modul 3: Pipeline NLP Complet
Modul 3: NLP aplicat cu Hugging Face (gratuit)
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import re
import math
import io
import datetime
from collections import Counter

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 18 — Sinteza NLP",
    page_icon="NLP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>NLP</div>
    <div style='font-size:16px; font-weight:700; color:#6c3483;'>ZIUA 18</div>
    <div style='font-size:11px; color:#666;'>Sinteza Modul 3 — Pipeline NLP Complet</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 3 — NLP aplicat (Hugging Face)")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 18 / 30 zile")
st.sidebar.progress(18 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Pipeline Ziua 18:**
- Step 1: Tokenizare + statistici
- Step 2: Clasificare document
- Step 3: Rezumare extractiva
- Step 4: NER — entitati cheie
- Step 5: Raport final export
""")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>NLP</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#6c3483; font-weight:800;'>
            Ziua 18 — Sinteza Modul 3: Pipeline NLP Complet
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Tokenizare + Clasificare + Rezumare + NER + Raport &nbsp;|&nbsp;
            Modul 3 — NLP aplicat Hugging Face
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px;padding:12px 20px;margin-bottom:16px;'>
<span style='color:#f9e79f;font-size:13px;font-style:italic;'>
"Documentele APIA contin sute de pagini pe an. NLP automatizeaza extragerea informatiilor cheie —
fermier, suprafata, cultura, neconformitate — in secunde, nu ore."<br>
<b style='color:white;'>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | APIA CJ Gorj</b>
</span></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATE DEMO
# ══════════════════════════════════════════════════════════════════════════════

DOCUMENTE_DEMO = {
    "Cerere PAC — Popescu Ion": """
Cerere unica de plata PAC 2025
Fermier: Popescu Ion, CNP 1750312180042
Adresa: sat Bumbesti, comuna Bumbesti-Jiu, judet Gorj
Nr. cerere: APIA-GJ-2025-00741

Parcela 1: suprafata declarata 4,52 ha, cultura grau, cod LPIS GJ-001-A
Parcela 2: suprafata declarata 3,80 ha, cultura floarea-soarelui, cod LPIS GJ-001-B
Parcela 3: suprafata declarata 2,15 ha, cultura lucerna, cod LPIS GJ-001-C

Subventie solicitata: plata de baza 285 EUR/ha, eco-schema 50 EUR/ha
Total suprafata: 10,47 ha
Banca: BCR, IBAN RO49RNCB0080012345678901

Cerere depusa: 15 mai 2025. Termen control: 30 septembrie 2025.
Neconformitate detectata: suprafata masurat prin drone 9,83 ha, diferenta 6.1%.
""",
    "Raport Control Teren — Ionescu Maria": """
Raport de control pe teren
Inspector: Ionescu Maria, APIA CJ Gorj, data: 12 iunie 2025
Fermier controlat: Dumitru Gheorghe, CNP 1620514180031

Parcela verificata: LPIS GJ-045-B, suprafata declarata 7,20 ha
Metoda masurare: drone DJI Phantom 4, altitudine 120m, GSD 3.2 cm/px
Suprafata masurata prin CV: 6,94 ha

Cultura identificata: porumb, stadiu vegetatie 30-40 cm
NDVI mediu: 0.62 (vegetatie sanatoasa)
Anomalii detectate: zona de 0.45 ha cu NDVI < 0.20, posibila seceta locala

Concluzie: diferenta suprafata 3.6%, sub pragul de 5% — fara penalizare
Recomandare: monitorizare zona stresata prin zbor suplimentar in august.
""",
    "Notificare Neconformitate — Stanescu Vasile": """
Notificare de neconformitate PAC 2025
Nr.: APIA-GJ-NECONF-2025-0089
Data: 20 iulie 2025

Catre: Stanescu Vasile, judet Gorj, cod postal 217500
CNP: 1810924180055

In urma controlului pe teren si a analizei imaginilor drone din 5 iulie 2025,
s-a constatat urmatoarea neconformitate:

Parcela LPIS GJ-088-A: suprafata declarata 8,50 ha, suprafata masurata 6,20 ha.
Diferenta: 2,30 ha (27,1%) — depaseste pragul admis de 25%.

Cultura declarata: grau. Cultura identificata prin NDVI si imagini satelitare: partial lucerna.
Perioada de raspuns: 15 zile lucratoare de la data primirii prezentei.

Penalizare estimata: reducere subventie cu 30% pentru parcela mentionata.
Valoare subventie afectata: 1.240 EUR.
""",
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII NLP OFFLINE (fara dependente externe)
# ══════════════════════════════════════════════════════════════════════════════

STOPWORDS_RO = {
    "si", "sau", "in", "la", "de", "cu", "pe", "din", "pentru", "care",
    "este", "sunt", "a", "al", "ale", "cei", "cel", "cea", "un", "o",
    "nu", "sa", "se", "ca", "mai", "prin", "fie", "daca", "dar", "iar",
    "fost", "avea", "avea", "fi", "au", "am", "ai", "a", "an",
    "acest", "aceasta", "aceste", "acestor", "acestui", "acestei",
    "urma", "data", "nr", "cod", "total", "sub",
}

def tokenizeaza(text: str) -> list:
    tokens = re.findall(r'\b[a-zA-ZăâîșțĂÂÎȘȚ]{3,}\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS_RO]

def statistici_text(text: str) -> dict:
    cuvinte = text.split()
    propozitii = [p.strip() for p in re.split(r'[.!?]\s+', text) if len(p.strip()) > 10]
    tokens = tokenizeaza(text)
    frecvente = Counter(tokens).most_common(10)
    return {
        "nr_cuvinte": len(cuvinte),
        "nr_propozitii": len(propozitii),
        "nr_caractere": len(text),
        "vocabular_unic": len(set(tokens)),
        "densitate_lexicala": round(len(set(tokens)) / max(len(tokens), 1), 3),
        "frecvente": frecvente,
        "propozitii": propozitii,
    }

def clasifica_document(text: str) -> dict:
    text_l = text.lower()
    scoruri = {}

    reguli = {
        "Cerere PAC": ["cerere", "plata", "pac", "subventie", "declarata", "depusa"],
        "Raport Control": ["raport", "control", "inspector", "verificata", "masurata", "drone"],
        "Notificare Neconformitate": ["notificare", "neconformitate", "penalizare", "diferenta", "depaseste"],
        "Comunicare Administrativa": ["comunicare", "adresa", "decizie", "ordinul", "conform"],
        "Situatie de Urgenta": ["urgenta", "catastrofa", "inundatie", "seceta", "calamitate"],
    }

    for categorie, cuvinte_cheie in reguli.items():
        scor = sum(1 for c in cuvinte_cheie if c in text_l)
        scoruri[categorie] = scor

    categorie_max = max(scoruri, key=scoruri.get)
    scor_max = scoruri[categorie_max]
    total = sum(scoruri.values()) or 1
    confidenta = round(scor_max / total, 2)

    return {
        "categorie": categorie_max,
        "confidenta": confidenta,
        "toate_scorurile": scoruri,
    }

def rezuma_document(text: str, n_propozitii: int = 3) -> str:
    propozitii = [p.strip() for p in re.split(r'[.!?]\n?', text) if len(p.strip()) > 20]
    if len(propozitii) <= n_propozitii:
        return text.strip()

    tokens_doc = tokenizeaza(text)
    freq = Counter(tokens_doc)

    scoruri = {}
    for i, prop in enumerate(propozitii):
        tokens_p = tokenizeaza(prop)
        scor = sum(freq.get(t, 0) for t in tokens_p) / max(len(tokens_p), 1)
        # Bonus pentru propozitii de inceput
        if i == 0:
            scor *= 1.3
        scoruri[i] = scor

    top_idx = sorted(scoruri, key=scoruri.get, reverse=True)[:n_propozitii]
    top_idx_sortat = sorted(top_idx)

    return ". ".join(propozitii[i] for i in top_idx_sortat) + "."

def extrage_entitati(text: str) -> list:
    entitati = []

    # CNP
    for m in re.finditer(r'\b[12]\d{12}\b', text):
        entitati.append({"tip": "CNP", "valoare": m.group(), "pozitie": m.start()})

    # IBAN
    for m in re.finditer(r'\bRO\d{2}[A-Z]{4}\d{16}\b', text):
        entitati.append({"tip": "IBAN", "valoare": m.group(), "pozitie": m.start()})

    # Cod LPIS
    for m in re.finditer(r'\bGJ-\d{3}-[A-Z]\b', text):
        entitati.append({"tip": "COD_LPIS", "valoare": m.group(), "pozitie": m.start()})

    # Suprafata (ha)
    for m in re.finditer(r'(\d+[,.]?\d*)\s*ha\b', text, re.IGNORECASE):
        entitati.append({"tip": "SUPRAFATA_HA", "valoare": m.group(), "pozitie": m.start()})

    # Valoare EUR
    for m in re.finditer(r'(\d+[.,]?\d*)\s*EUR\b', text, re.IGNORECASE):
        entitati.append({"tip": "VALOARE_EUR", "valoare": m.group(), "pozitie": m.start()})

    # Data (zz luna aaaa sau zz.ll.aaaa)
    for m in re.finditer(r'\b\d{1,2}[. /]\d{1,2}[. /]\d{4}\b|\b\d{1,2}\s+\w+\s+\d{4}\b', text):
        entitati.append({"tip": "DATA", "valoare": m.group(), "pozitie": m.start()})

    # Cultura
    culturi = ["grau", "porumb", "floarea-soarelui", "floarea soarelui",
               "lucerna", "fanete", "rapita", "soia", "orz", "sfecla"]
    for cultura in culturi:
        for m in re.finditer(r'\b' + re.escape(cultura) + r'\b', text.lower()):
            entitati.append({"tip": "CULTURA", "valoare": cultura.title(), "pozitie": m.start()})

    # Judet
    judete = ["gorj", "dolj", "olt", "valcea", "mehedinti", "hunedoara"]
    for jud in judete:
        for m in re.finditer(r'\b' + jud + r'\b', text.lower()):
            entitati.append({"tip": "JUDET", "valoare": jud.title(), "pozitie": m.start()})

    # Fermier (dupa cuvantul "Fermier:" sau "catre:")
    for m in re.finditer(
        r'(?:Fermier|Catre|fermier controlat)\s*:\s*([A-ZAÂÎȘȚ][a-zaâîșț]+\s+[A-ZAÂÎȘȚ][a-zaâîșț]+)',
        text, re.IGNORECASE
    ):
        entitati.append({"tip": "FERMIER", "valoare": m.group(1), "pozitie": m.start()})

    return sorted(entitati, key=lambda x: x["pozitie"])

def highlight_entitati_html(text: str, entitati: list) -> str:
    culori_tip = {
        "CNP":          "#e74c3c",
        "IBAN":         "#8e44ad",
        "COD_LPIS":     "#1a5276",
        "SUPRAFATA_HA": "#27ae60",
        "VALOARE_EUR":  "#d35400",
        "DATA":         "#2980b9",
        "CULTURA":      "#117a65",
        "JUDET":        "#7f8c8d",
        "FERMIER":      "#c0392b",
    }
    offset = 0
    rezultat = text
    for ent in sorted(entitati, key=lambda x: x["pozitie"]):
        val = ent["valoare"]
        pos = ent["pozitie"] + offset
        culoare = culori_tip.get(ent["tip"], "#999")
        idx = rezultat.lower().find(val.lower(), max(0, pos - 5))
        if idx == -1:
            continue
        fragment_original = rezultat[idx:idx + len(val)]
        inlocuire = (
            f'<mark style="background:{culoare}22; border:1px solid {culoare}; '
            f'border-radius:3px; padding:1px 4px; color:{culoare}; '
            f'font-weight:600; font-size:12px;">'
            f'{fragment_original}'
            f'<sup style="font-size:9px; color:{culoare};">{ent["tip"]}</sup>'
            f'</mark>'
        )
        rezultat = rezultat[:idx] + inlocuire + rezultat[idx + len(val):]
        offset += len(inlocuire) - len(val)
    return rezultat.replace("\n", "<br>")

def genereaza_raport(text_original: str, clasificare: dict, rezumat: str,
                     entitati: list, statistici: dict, doc_name: str) -> str:
    azi = datetime.date.today().strftime("%d.%m.%Y")
    linii = [
        "=" * 65,
        "RAPORT NLP AUTOMAT — ANALIZA DOCUMENT APIA",
        f"Generat: {azi} | Ziua 18 — Sinteza Modul 3 NLP",
        f"Autor pipeline: Prof. Asoc. Dr. O.M. Gamulescu | UCB Targu Jiu",
        "=" * 65,
        "",
        f"Document: {doc_name}",
        "",
        "── STATISTICI TEXT ─────────────────────────────────────",
        f"  Cuvinte:          {statistici['nr_cuvinte']}",
        f"  Propozitii:       {statistici['nr_propozitii']}",
        f"  Vocabular unic:   {statistici['vocabular_unic']}",
        f"  Densitate lex.:   {statistici['densitate_lexicala']}",
        "",
        "── CLASIFICARE DOCUMENT ────────────────────────────────",
        f"  Categorie:        {clasificare['categorie']}",
        f"  Confidenta:       {int(clasificare['confidenta']*100)}%",
        "",
        "── REZUMAT AUTOMAT ─────────────────────────────────────",
    ]
    for prop in rezumat.split(". "):
        if prop.strip():
            linii.append(f"  {prop.strip()}.")
    linii += [
        "",
        "── ENTITATI DETECTATE ──────────────────────────────────",
    ]
    tipuri_unice = {}
    for e in entitati:
        tipuri_unice.setdefault(e["tip"], []).append(e["valoare"])
    for tip, valori in tipuri_unice.items():
        unice = list(dict.fromkeys(valori))
        linii.append(f"  {tip:16s}: {', '.join(unice)}")
    linii += [
        "",
        "── CUVINTE CHEIE (top 10) ──────────────────────────────",
        "  " + ", ".join(f"{c}({n})" for c, n in statistici["frecvente"]),
        "",
        "=" * 65,
        "Generat automat prin pipeline NLP | Bloc 5 AI Aplicat",
        "Universitatea Constantin Brancusi | APIA CJ Gorj",
        "=" * 65,
    ]
    return "\n".join(linii)


# ══════════════════════════════════════════════════════════════════════════════
# INTERFATA
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teorie & Pipeline",
    "Analiza Document",
    "Rezultate detaliate",
    "Pipeline Integrat (Date Reale)",
    "Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Pipeline NLP complet pentru documente APIA")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
**Modulul 3 NLP — ce am acoperit:**

| Ziua | Tehnica | Aplicatie |
|---|---|---|
| Z13 | Tokenizare, TF-IDF, Transformer | Baza teoretica NLP |
| Z15 | Clasificare Zero-Shot + Naive Bayes | Categorii documente APIA |
| Z16 | Rezumare TF-IDF + BART | Sinteza rapoarte lungi |
| Z17 | NER regex + BERT multilingual | Entitati: fermier, suprafata, CNP |
| **Z18** | **Pipeline integrat** | **Document → Raport complet** |

#### Fluxul pipeline Z18
```
Text document APIA
    ↓
[1] Tokenizare + Statistici
    → nr cuvinte, propozitii, vocabular, densitate lexicala
    ↓
[2] Clasificare document
    → Cerere PAC / Raport Control / Notificare Neconformitate
    → confidenta estimata
    ↓
[3] Rezumare extractiva (TF-IDF)
    → top 3 propozitii cheie (offline, fara model)
    ↓
[4] NER — Entitati cheie
    → CNP, IBAN, Cod LPIS, Suprafata, EUR, Data, Cultura, Fermier
    ↓
[5] Raport final
    → export .txt complet
```
""")

    with col2:
        st.markdown("""
<div style='background:#f5eef8; border-radius:10px; padding:14px;
     border-top:4px solid #6c3483;'>
<div style='font-weight:700; color:#6c3483;'>De ce NLP pentru APIA?</div>
<div style='font-size:11px; color:#333; margin-top:10px; line-height:1.8;'>

Inspector APIA primeste anual:<br>
<b>200+ cereri PAC</b><br>
<b>50+ rapoarte control</b><br>
<b>30+ notificari neconformitate</b><br><br>

Fara NLP: citire manuala 280 documente<br>
= ~140 ore/an per inspector<br><br>

Cu NLP automat:<br>
- Clasificare instantanee<br>
- Extragere CNP / suprafata / cultura<br>
- Rezumat in 3 propozitii<br>
= <b>~5 minute/document → 140h → 24h</b>
</div></div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f4fd; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #1a5276;'>
<div style='font-weight:700; color:#1a5276;'>Tehnici folosite (offline)</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.8;'>
<b>Tokenizare:</b> regex \b[a-z]{3,}\b<br>
<b>Frecventa:</b> collections.Counter<br>
<b>Clasificare:</b> reguli cuvinte cheie<br>
<b>Rezumare:</b> TF-IDF simplificat<br>
<b>NER:</b> regex specializate APIA<br><br>
100% offline, fara API, fara cost.
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Arhitectura pipeline completa")
    st.markdown("""
<div style='display:flex; gap:0; align-items:center; flex-wrap:wrap; margin:8px 0;'>
""" + "".join(f"""
    <div style='background:{c}; color:white; padding:8px 14px; border-radius:6px;
         font-size:11px; font-weight:700; margin:3px;'>
        {s}
    </div>
    <div style='color:#aaa; margin:3px; font-size:18px;'>{arrow}</div>
""" for (c, s), arrow in zip(
    [("#6c3483","Text input"),("# 1a5276","Tokenizare"),("#117a65","Clasificare"),
     ("#d35400","Rezumare"),("#c0392b","NER"),("#27ae60","Raport")],
    ["→","→","→","→","→",""]
)) + """
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALIZA DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Analiza automata document APIA")

    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.markdown("**Selecteaza document:**")
        sursa = st.radio("Sursa:", ["Document demo", "Text propriu"], key="sursa_nlp", horizontal=True)

        if sursa == "Document demo":
            doc_ales = st.selectbox("Alege documentul demo:", list(DOCUMENTE_DEMO.keys()), key="doc_demo")
            text_input = DOCUMENTE_DEMO[doc_ales]
            doc_name = doc_ales
        else:
            text_input = st.text_area(
                "Introdu textul documentului APIA:",
                height=280,
                placeholder="Lipeste aici textul unui document APIA: cerere PAC, raport control, notificare...",
                key="text_propriu"
            )
            doc_name = "Document utilizator"

        st.divider()
        st.markdown("**Parametri analiza:**")
        n_prop_rezumat = st.slider("Propozitii in rezumat:", 1, 5, 3, key="n_prop")
        arata_highlight = st.checkbox("Highlight entitati in text", value=True, key="highlight")

        ruleaza = st.button("Analizeaza document", type="primary",
                            use_container_width=True, key="btn_nlp")

    with col_out:
        if sursa == "Document demo":
            st.markdown("**Previzualizare document:**")
            st.markdown(
                f"<div style='background:#f9f9f9; border-radius:8px; padding:12px; "
                f"font-size:11px; line-height:1.7; height:320px; overflow-y:auto; "
                f"border:1px solid #ddd;'>{text_input.replace(chr(10), '<br>')}</div>",
                unsafe_allow_html=True
            )
        else:
            if text_input:
                st.markdown("**Text introdus:**")
                st.markdown(
                    f"<div style='background:#f9f9f9; border-radius:8px; padding:12px; "
                    f"font-size:11px; line-height:1.7; height:320px; overflow-y:auto; "
                    f"border:1px solid #ddd;'>{text_input.replace(chr(10), '<br>')}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.info("Introdu un text in campul din stanga.")

    if ruleaza and text_input and text_input.strip():
        with st.spinner("Procesez documentul..."):
            stats      = statistici_text(text_input)
            clasificare = clasifica_document(text_input)
            rezumat    = rezuma_document(text_input, n_prop_rezumat)
            entitati   = extrage_entitati(text_input)

        st.session_state["nlp_stats"]      = stats
        st.session_state["nlp_cls"]        = clasificare
        st.session_state["nlp_rezumat"]    = rezumat
        st.session_state["nlp_entitati"]   = entitati
        st.session_state["nlp_text"]       = text_input
        st.session_state["nlp_doc_name"]   = doc_name
        st.session_state["nlp_n_prop"]     = n_prop_rezumat

        st.divider()

        # ── Metrici rapide ────────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric("Cuvinte", stats["nr_cuvinte"])
        with c2:
            st.metric("Propozitii", stats["nr_propozitii"])
        with c3:
            st.metric("Vocabular unic", stats["vocabular_unic"])
        with c4:
            st.metric("Categorie", clasificare["categorie"].split()[0])
        with c5:
            st.metric("Entitati detectate", len(entitati))

        st.success(
            f"Document clasificat ca **{clasificare['categorie']}** "
            f"(confidenta {int(clasificare['confidenta']*100)}%) | "
            f"{len(entitati)} entitati extrase"
        )

        # ── Highlight text ────────────────────────────────────────────────────
        if arata_highlight and entitati:
            st.markdown("**Text cu entitati evidentiate:**")
            html_hl = highlight_entitati_html(text_input, entitati)
            st.markdown(
                f"<div style='background:#fefefe; border-radius:8px; padding:14px; "
                f"font-size:12px; line-height:1.9; border:1px solid #e0e0e0; "
                f"max-height:300px; overflow-y:auto;'>{html_hl}</div>",
                unsafe_allow_html=True
            )

    elif ruleaza:
        st.warning("Introdu un text pentru a analiza.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REZULTATE DETALIATE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if "nlp_stats" not in st.session_state:
        st.info("Ruleaza analiza in tab-ul 'Analiza Document' pentru a vedea rezultatele.")
    else:
        stats      = st.session_state["nlp_stats"]
        clasificare = st.session_state["nlp_cls"]
        rezumat    = st.session_state["nlp_rezumat"]
        entitati   = st.session_state["nlp_entitati"]
        text_orig  = st.session_state["nlp_text"]
        doc_name   = st.session_state["nlp_doc_name"]

        col_a, col_b = st.columns(2)

        with col_a:
            # ── Clasificare ───────────────────────────────────────────────────
            st.markdown("#### Clasificare document")
            culori_cat = {
                "Cerere PAC": "#1a5276",
                "Raport Control": "#117a65",
                "Notificare Neconformitate": "#c0392b",
                "Comunicare Administrativa": "#8e44ad",
                "Situatie de Urgenta": "#e67e22",
            }
            for cat, scor in sorted(clasificare["toate_scorurile"].items(),
                                     key=lambda x: -x[1]):
                total_scor = max(sum(clasificare["toate_scorurile"].values()), 1)
                pct = scor / total_scor
                culoare = culori_cat.get(cat, "#999")
                st.markdown(f"""
                <div style='margin:4px 0;'>
                    <div style='display:flex; justify-content:space-between;
                         font-size:11px; margin-bottom:2px;'>
                        <span style='color:#333;'>{cat}</span>
                        <span style='color:{culoare}; font-weight:700;'>{scor} cuvinte cheie</span>
                    </div>
                    <div style='background:#eee; border-radius:4px; height:10px;'>
                        <div style='background:{culoare}; width:{int(pct*100)}%;
                             height:10px; border-radius:4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # ── Rezumat ───────────────────────────────────────────────────────
            st.markdown("#### Rezumat automat (TF-IDF)")
            st.markdown(
                f"<div style='background:#f0f8ff; border-radius:8px; padding:12px; "
                f"font-size:12px; line-height:1.7; border-left:4px solid #1a5276;'>"
                f"{rezumat}</div>",
                unsafe_allow_html=True
            )

            st.divider()

            # ── Frecventa cuvinte ─────────────────────────────────────────────
            st.markdown("#### Top 10 cuvinte cheie")
            if PLOTLY_OK and stats["frecvente"]:
                cuvinte_f = [c for c, _ in stats["frecvente"]]
                frecvente_f = [n for _, n in stats["frecvente"]]
                fig = go.Figure(go.Bar(
                    x=frecvente_f[::-1], y=cuvinte_f[::-1],
                    orientation="h",
                    marker_color="#6c3483",
                    text=frecvente_f[::-1], textposition="outside"
                ))
                fig.update_layout(
                    height=260, margin=dict(l=10, r=10, t=10, b=10),
                    xaxis_title="Frecventa", yaxis_title="",
                    plot_bgcolor="white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                for cuv, freq in stats["frecvente"]:
                    st.markdown(f"- **{cuv}**: {freq}")

        with col_b:
            # ── Entitati ──────────────────────────────────────────────────────
            st.markdown("#### Entitati detectate (NER)")

            if entitati and PANDAS_OK:
                df_ent = pd.DataFrame(entitati)[["tip", "valoare"]]
                df_ent.columns = ["Tip entitate", "Valoare"]

                culori_tip = {
                    "CNP": "#e74c3c", "IBAN": "#8e44ad", "COD_LPIS": "#1a5276",
                    "SUPRAFATA_HA": "#27ae60", "VALOARE_EUR": "#d35400",
                    "DATA": "#2980b9", "CULTURA": "#117a65",
                    "JUDET": "#7f8c8d", "FERMIER": "#c0392b",
                }
                for _, row in df_ent.iterrows():
                    culoare = culori_tip.get(row["Tip entitate"], "#999")
                    st.markdown(f"""
                    <div style='display:flex; align-items:center; gap:8px;
                         padding:5px 10px; margin:3px 0; background:white;
                         border-radius:6px; border-left:4px solid {culoare};
                         box-shadow:0 1px 3px rgba(0,0,0,0.05); font-size:12px;'>
                        <span style='background:{culoare}; color:white; padding:2px 8px;
                             border-radius:4px; font-size:10px; font-weight:700;
                             min-width:110px; text-align:center;'>
                            {row["Tip entitate"]}</span>
                        <span style='color:#333; font-weight:600;'>{row["Valoare"]}</span>
                    </div>
                    """, unsafe_allow_html=True)
            elif not entitati:
                st.info("Nicio entitate detectata in acest document.")

            st.divider()

            # ── Raport export ─────────────────────────────────────────────────
            st.markdown("#### Export raport")
            raport_txt = genereaza_raport(
                text_orig, clasificare, rezumat, entitati, stats, doc_name
            )
            st.text_area("Raport generat:", raport_txt, height=220, key="raport_preview")
            st.download_button(
                "Descarca raport .txt",
                data=raport_txt.encode("utf-8"),
                file_name=f"raport_nlp_{datetime.date.today().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PIPELINE INTEGRAT CU DATE REALE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Pipeline integrat: SecureGeo + Anomalii + Contururi + NLP")

    st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#117a65 50%,#6c3483 100%);
     border-radius:10px; padding:14px 20px; color:white; margin-bottom:16px;'>
<div style='font-size:14px; font-weight:700;'>
    De ce aceste trei module sunt vitale pentru SecureGeo?
</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9; line-height:1.7;'>
    Detectia contururilor (Z14) masoara suprafata reala a parcelelor din imagini georeferentiate (Z10b).
    Detectia anomaliilor NDVI (Z10) identifica zone de stres sau culturi gresite.
    NLP (Z18) extrage datele declarate din documentele PAC si genereaza raportul de neconformitate.
    Impreuna formeaza un sistem complet de inspectie agricola automatizata.
</div>
</div>
""", unsafe_allow_html=True)

    # ── Diagrama flux integrat ────────────────────────────────────────────────
    st.markdown("### Fluxul complet al inspectiei agricole automatizate")

    etape = [
        {
            "nr": "1",
            "modul": "Z10b — SecureGeo",
            "titlu": "Georeferentiere imagine",
            "detalii": "Fotografie aeriana cu EXIF complet (lat, lon, altitudine 11.439m). Timestamp Camera — singura aplicatie cu EXIF altitudine confirmat. Offline, GDPR-evaluat.",
            "output": "Imagine georeferentiata + coordonate GPS verificate",
            "culoare": "#1a5276",
        },
        {
            "nr": "2",
            "modul": "Z14 — Contururi",
            "titlu": "Detectie contururi parcele",
            "detalii": "SLIC + Watershed pe imaginea aeriana. Calcul suprafata reala in pixeli → conversie ha prin GSD. Rezultat: suprafata masurata obiectiv, independent de declaratia fermierului.",
            "output": "Suprafata masurata [ha] + perimetru [m] per parcela",
            "culoare": "#117a65",
        },
        {
            "nr": "3",
            "modul": "Z10 — Anomalii",
            "titlu": "Detectie anomalii NDVI",
            "detalii": "Calcul NDVI din canale multispectrale sau RGB proxy. Identificare zone cu NDVI < 0.2 (stres, seceta, cultura gresita). Scoring risc per parcela.",
            "output": "Harta anomalii + scor risc + cultura identificata",
            "culoare": "#8e44ad",
        },
        {
            "nr": "4",
            "modul": "Z18 — NLP",
            "titlu": "Analiza document PAC",
            "detalii": "Extragere date declarate: fermier (NER), suprafata declarata (regex ha), cultura declarata, CNP, cod LPIS. Comparare automata cu datele masurate din pasii 2-3.",
            "output": "Suprafata declarata + cultura declarata + identitate fermier",
            "culoare": "#d35400",
        },
        {
            "nr": "5",
            "modul": "Z18 — Raport",
            "titlu": "Generare raport neconformitate",
            "detalii": "Comparare suprafata declarata (NLP) vs. masurata (CV+drone). Daca diferenta > 5%: flag automat neconformitate. Raport formal generat, gata de semnat.",
            "output": "Raport PDF/TXT cu concluzie si penalizare calculata",
            "culoare": "#c0392b",
        },
    ]

    for i, etapa in enumerate(etape):
        st.markdown(f"""
<div style='display:flex; gap:0; align-items:stretch; margin:6px 0;'>
    <div style='background:{etapa["culoare"]}; color:white; border-radius:8px 0 0 8px;
         padding:12px 16px; min-width:130px; text-align:center; display:flex;
         flex-direction:column; justify-content:center;'>
        <div style='font-size:20px; font-weight:900;'>{etapa["nr"]}</div>
        <div style='font-size:9px; font-weight:700; margin-top:4px;
             opacity:0.85; line-height:1.3;'>{etapa["modul"]}</div>
    </div>
    <div style='background:white; border-radius:0 8px 8px 0; flex:1; padding:12px 16px;
         box-shadow:0 2px 6px rgba(0,0,0,0.06); border-top:1px solid #eee;
         border-right:1px solid #eee; border-bottom:1px solid #eee;'>
        <div style='font-weight:700; color:#333; font-size:13px;'>{etapa["titlu"]}</div>
        <div style='font-size:11px; color:#555; margin-top:4px;
             line-height:1.6;'>{etapa["detalii"]}</div>
        <div style='margin-top:8px; font-size:11px; background:#f5f5f5;
             border-radius:4px; padding:4px 10px; color:{etapa["culoare"]};
             font-weight:600;'>Output: {etapa["output"]}</div>
    </div>
</div>
{"<div style='margin-left:65px; color:#bbb; font-size:18px; line-height:1;'>↓</div>" if i < len(etape)-1 else ""}
""", unsafe_allow_html=True)

    st.divider()

    # ── Exemplu concret ───────────────────────────────────────────────────────
    st.markdown("### Exemplu concret: inspectie parcela GJ-001-A")

    col_ex1, col_ex2 = st.columns(2)

    with col_ex1:
        st.markdown("""
<div style='background:#eaf4fb; border-radius:10px; padding:14px;
     border-left:4px solid #1a5276;'>
<div style='font-weight:700; color:#1a5276; margin-bottom:8px;'>
    Date din SecureGeo + Computer Vision (obiective)
</div>
<div style='font-size:12px; line-height:2.0;'>
<b>Georeferentiere:</b> 45.0341°N, 23.1452°E<br>
<b>Altitudine fotografie:</b> 432m (drone)<br>
<b>GSD calculat:</b> 0.22 cm/px<br>
<b>Suprafata masurata CV:</b> 4.31 ha<br>
<b>Perimetru masurat:</b> 842 m<br>
<b>NDVI mediu:</b> 0.58 (vegetatie normala)<br>
<b>Zona anomalie NDVI &lt; 0.2:</b> 0.12 ha (2.8%)<br>
<b>Cultura identificata NDVI:</b> grau (confirmat)
</div>
</div>
""", unsafe_allow_html=True)

    with col_ex2:
        st.markdown("""
<div style='background:#fef9e7; border-radius:10px; padding:14px;
     border-left:4px solid #d35400;'>
<div style='font-weight:700; color:#d35400; margin-bottom:8px;'>
    Date din documentul PAC (declarate)
</div>
<div style='font-size:12px; line-height:2.0;'>
<b>Fermier (NER):</b> Popescu Ion<br>
<b>CNP (NER):</b> 1750312180042<br>
<b>Cod LPIS (NER):</b> GJ-001-A<br>
<b>Suprafata declarata (NER):</b> 4.52 ha<br>
<b>Cultura declarata (NER):</b> Grau<br>
<b>Subventie solicitata:</b> 285 EUR/ha<br>
<b>Total subventie parcela:</b> 1.288 EUR<br>
<b>Data cerere:</b> 15 mai 2025
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style='background:#fdedec; border-radius:10px; padding:14px; margin-top:8px;
     border-left:4px solid #c0392b;'>
<div style='font-weight:700; color:#922b21; font-size:13px;'>
    Concluzie automata — Raport neconformitate
</div>
<div style='font-size:12px; line-height:1.8; margin-top:6px;'>
<b>Diferenta suprafata:</b> 4.52 ha (declarata) vs 4.31 ha (masurata) = <b>0.21 ha = 4.6%</b><br>
<b>Prag APIA:</b> 5% → <b style='color:#27ae60;'>SUB PRAG — fara penalizare</b><br>
<b>Cultura:</b> Grau declarata = Grau identificat NDVI → <b style='color:#27ae60;'>CONFORM</b><br>
<b>Anomalie NDVI:</b> 0.12 ha zona stresata → <b style='color:#e67e22;'>MONITORIZARE recomandata</b><br><br>
<i>Raport generat automat in 3 secunde. Manual: ~45 minute per parcela.</i>
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Valoare academica ─────────────────────────────────────────────────────
    st.markdown("### Valoarea academica si institutionala a acestui pipeline")

    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.markdown("""
<div style='background:white; border-radius:10px; padding:14px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:4px solid #1a5276;
     text-align:center; font-size:12px;'>
<div style='font-size:28px; font-weight:900; color:#1a5276;'>MDPI</div>
<div style='font-weight:700; margin:6px 0;'>Drones IF 4.8 Q1</div>
<div style='color:#555; line-height:1.6;'>Articol ISI in pregatire.
Datele reale din zbor sunt baza empirica unica in literatura de specialitate.</div>
</div>
""", unsafe_allow_html=True)

    with col_v2:
        st.markdown("""
<div style='background:white; border-radius:10px; padding:14px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:4px solid #8e44ad;
     text-align:center; font-size:12px;'>
<div style='font-size:28px; font-weight:900; color:#8e44ad;'>ACE2-EU</div>
<div style='font-weight:700; margin:6px 0;'>ARIES Incubator</div>
<div style='color:#555; line-height:1.6;'>Propunere depusa 20 apr 2026.
Pipeline integrat = demonstrator pentru Cybersecurity + Digital Sovereignty.</div>
</div>
""", unsafe_allow_html=True)

    with col_v3:
        st.markdown("""
<div style='background:white; border-radius:10px; padding:14px;
     box-shadow:0 2px 8px rgba(0,0,0,0.07); border-top:4px solid #117a65;
     text-align:center; font-size:12px;'>
<div style='font-size:28px; font-weight:900; color:#117a65;'>UCB</div>
<div style='font-weight:700; margin:6px 0;'>Master MRA</div>
<div style='color:#555; line-height:1.6;'>Suport de curs Master Managementul
Riscului in Agricultura. Studenti invata AI aplicat pe cazuri reale APIA.</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Modul 3 NLP — Sinteza cunostintelor")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
#### Ce am invatat in Zilele 13-18

**Ziua 13 — Bazele NLP**
- Tokenizare: impartirea textului in unitati
- TF-IDF: importanta relativa a unui cuvant
- Arhitectura Transformer (Attention is All You Need)
- Modele pre-antrenate: BERT, RoBERTa, GPT

**Ziua 15 — Clasificare texte**
- Zero-Shot Classification (HuggingFace) — fara date de antrenare
- Naive Bayes — clasificator probabilistic simplu si rapid
- Evaluare: Accuracy, F1, matrice de confuzie

**Ziua 16 — Rezumare documente**
- Rezumare extractiva: selecteaza propozitii originale (TF-IDF)
- Rezumare abstractiva: genereaza text nou (BART, T5)
- Aplicatie: rezumarea rapoartelor APIA lungi

**Ziua 17 — NER (Named Entity Recognition)**
- NER cu regex: rapid, offline, controlabil
- NER cu BERT multilingual: invata din context
- Entitati APIA: CNP, LPIS, suprafata, cultura, EUR

**Ziua 18 — Pipeline integrat**
- Combinarea tuturor tehnicilor intr-un flux coerent
- Offline-first: functioneaza fara internet
- Export raport complet pentru uz profesional
""")

    with col2:
        st.markdown("""
#### Aplicatii practice APIA

**1. Procesare cereri PAC in lot**
```
for cerere in lista_cereri:
    stats = statistici_text(cerere)
    cls   = clasifica_document(cerere)
    ent   = extrage_entitati(cerere)
    # extrage suprafata, CNP, cultura
    # compara cu LPIS
    # flag neconformitati
```

**2. Detectie automata neconformitati**
- Extrage suprafata declarata din text
- Compara cu suprafata masurata (drone/CV)
- Flag automat daca diferenta > 5%

**3. Generare rapoarte automate**
- Inspector introduce constatarile
- NLP extrage datele cheie
- Raport formal generat automat

**4. Clasificare urgenta documente**
- Prioritizeaza notificarile de neconformitate
- Identifica documentele care necesita
  actiune imediata vs. arhivare
""")

        st.markdown("""
<div style='background:#e8f8f5; border-radius:10px; padding:14px; margin-top:8px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Concluzie Modul 3</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.7;'>
NLP reduce timpul de procesare a documentelor APIA de la ore la secunde.
Combinat cu Computer Vision (Module 2) si Machine Learning (Modul 1),
formeaza un sistem complet AI pentru inspectie agricola automatizata.
Urmatorul pas: Modul 4 — AI Generativ (Ollama local).
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Modul 3 NLP — FINALIZAT</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
Zilele 13-18 | Tokenizare | TF-IDF | Transformers | Clasificare | Rezumare | NER | Pipeline integrat
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea etapa: Modul 4 — AI Generativ cu Ollama local (Zilele 19-24)
</div>
</div>
""", unsafe_allow_html=True)
