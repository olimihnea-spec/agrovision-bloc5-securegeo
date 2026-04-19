"""
Ziua 17 — NER: Named Entity Recognition (Extragere Entitati)
Modul 3: NLP Aplicat — Hugging Face NER + regex demo
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import re
import datetime

try:
    from transformers import pipeline as hf_pipeline
    HF_OK = True
except ImportError:
    HF_OK = False

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 17 — NER Entitati",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🔍</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 17</div>
    <div style='font-size:11px; color:#666;'>NER — Extragere Entitati din Text</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 3 — NLP Aplicat")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 17 / 30 zile")
st.sidebar.progress(17 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 17:**
- Ce este NER (Named Entity Recognition)
- Tipuri de entitati: PER, LOC, ORG, DATE, NUM
- Regex NER pentru documente APIA
- Hugging Face NER pipeline
- Vizualizare entitati in text (highlight)
- Extragere structurata date APIA
""")
st.sidebar.divider()
if HF_OK:
    st.sidebar.success("transformers instalat")
else:
    st.sidebar.warning("transformers absent — NER regex activ")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🔍</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 17 — NER: Extragere Entitati din Documente
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 3 — NLP Aplicat &nbsp;|&nbsp;
            Regex NER + Hugging Face — persoane, locatii, date, suprafete din rapoarte APIA
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px;padding:12px 20px;margin-bottom:16px;'>
<span style='color:#f9e79f;font-size:13px;font-style:italic;'>
"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"<br>
<b style='color:white;'>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | Universitatea din Petrosani, 2024</b>
</span></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TIPURI ENTITATI + CULORI
# ══════════════════════════════════════════════════════════════════════════════
TIPURI_ENTITATI = {
    "PERSOANA":      {"culoare": "#d35400", "bg": "#fdebd0", "icon": "👤", "desc": "Nume persoane fizice"},
    "ORGANIZATIE":   {"culoare": "#1a5276", "bg": "#d6eaf8", "icon": "🏛️", "desc": "Institutii, agentii, firme"},
    "LOCATIE":       {"culoare": "#1e8449", "bg": "#d5f5e3", "icon": "📍", "desc": "Judete, localitati, parcele"},
    "DATA":          {"culoare": "#6c3483", "bg": "#e8daef", "icon": "📅", "desc": "Date calendaristice, perioade"},
    "SUPRAFATA":     {"culoare": "#148f77", "bg": "#d1f2eb", "icon": "🌾", "desc": "Suprafete in hectare"},
    "NDVI":          {"culoare": "#27ae60", "bg": "#eafaf1", "icon": "📊", "desc": "Valori indice vegetatie"},
    "COD_PARCELA":   {"culoare": "#7d6608", "bg": "#fef9e7", "icon": "🗺️", "desc": "Coduri LPIS, blocuri fizice"},
    "CNP_CUI":       {"culoare": "#922b21", "bg": "#fadbd8", "icon": "🪪", "desc": "Identificatori persoane/firme"},
    "CULTURA":       {"culoare": "#6e2f8a", "bg": "#f5eef8", "icon": "🌱", "desc": "Tipuri de culturi agricole"},
    "PROCENT":       {"culoare": "#1f618d", "bg": "#eaf2ff", "icon": "%",   "desc": "Valori procentuale"},
}

CULTURI_CUNOSCUTE = [
    "grau", "grau de toamna", "floarea-soarelui", "floarea soarelui",
    "porumb", "lucerna", "fanete", "rapita", "orz", "triticale",
    "soia", "sfecla", "cartofi", "legume", "vita de vie", "livada",
]

ORGANIZATII_CUNOSCUTE = [
    "APIA", "UCB", "MADR", "OCPI", "LPIS", "IACS", "PAC",
    "Agentia de Plati", "Agentia de plati", "Ministerul Agriculturii",
    "Prefectura", "Primaria", "Directia Agricola", "Centrul Judetean",
    "Universitatea", "Academia",
]

JUDETE_RO = [
    "Alba", "Arad", "Arges", "Bacau", "Bihor", "Bistrita-Nasaud",
    "Botosani", "Braila", "Brasov", "Buzau", "Caras-Severin", "Calarasi",
    "Cluj", "Constanta", "Covasna", "Dambovita", "Dolj", "Galati",
    "Giurgiu", "Gorj", "Harghita", "Hunedoara", "Ialomita", "Iasi",
    "Ilfov", "Maramures", "Mehedinti", "Mures", "Neamt", "Olt",
    "Prahova", "Salaj", "Satu Mare", "Sibiu", "Suceava", "Teleorman",
    "Timis", "Tulcea", "Vaslui", "Valcea", "Vrancea", "Bucuresti",
    "Petrosani", "Targu Jiu", "Bumbesti-Jiu", "Turceni", "Motru",
]

# ══════════════════════════════════════════════════════════════════════════════
# TEXTE DEMO
# ══════════════════════════════════════════════════════════════════════════════
TEXTE_NER = {
    "Raport control teren complet": """In data de 14 aprilie 2024, echipa de inspectie APIA formata din inspectorul \
principal Gam. O.M. si inspectorul Pop. I.A. a efectuat un control pe teren la ferma \
inregistrata cu codul GJ-2024-001847, apartinand fermierului Ionescu Gheorghe, cu \
domiciliul in localitatea Bumbesti-Jiu, judetul Gorj. Fermierul a declarat o suprafata \
totala de 45.30 ha, din care 28.50 ha cultivate cu grau de toamna si 16.80 ha cultivate \
cu floarea-soarelui. Masuratorile GPS au relevat o suprafata efectiva de 43.75 ha, \
o diferenta de 3.42% fata de suprafata declarata. Analiza NDVI indica o valoare medie \
de 0.62 pentru grau si 0.38 pentru floarea-soarelui, cu zone de stress hidric de 12% \
in parcela GORJ_BF_00234. CNP fermier: 1760412180032. Raport intocmit conform \
Regulamentului UE 2021/2116.""",

    "Cerere PAC cu parcele multiple": """Subsemnatul Popescu Constantin, CNP 1650312180045, \
cu domiciliul in comuna Turceni, judetul Gorj, depun prezenta cerere la APIA Centrul \
Judetean Gorj pentru campania 2024. Solicit plati directe pentru suprafata totala \
de 38.75 ha: parcela T45/A cu 12.40 ha porumb, parcela T46/B cu 9.80 ha grau de \
toamna, parcela T47/C cu 8.20 ha lucerna, parcela T48/D cu 5.60 ha floarea-soarelui \
si parcela T49/E cu 2.75 ha fanete. Contractele de arenda sunt vizate de OCPI Gorj. \
Data depunere: 15.03.2024. Termen limita: 30.04.2024.""",

    "Raport NDVI analiza drone": """Prezentul raport sintetizeaza analiza imaginilor \
multispectrale achizitionate cu drona DJI Phantom 4 Multispectral in data de \
10 aprilie 2024 pentru zona Gorj-Nord (450 ha, 23 fermieri). NDVI mediu cultura \
grau: 0.65. Zone cu NDVI sub 0.10: 3% din suprafata. Zone stress hidric sever: \
3 parcele identificate in Turceni si Bumbesti-Jiu. Fermieri cu risc maxim: \
Ionescu Gheorghe (parcela GORJ_BF_00234, NDVI 0.38), Stanescu Marin \
(parcela GORJ_BF_00456, NDVI 0.29). Raport transmis echipei APIA Gorj \
in data de 12.04.2024 pentru control ulterior. Inspector coordonator: \
Prof. Dr. Gam. O.M., Universitatea din Petrosani.""",
}

# ══════════════════════════════════════════════════════════════════════════════
# NER REGEX — detector entitati fara model ML
# ══════════════════════════════════════════════════════════════════════════════

def ner_regex(text: str) -> list[dict]:
    """
    Extrage entitati din text folosind expresii regulate.
    Returneaza lista de dict: {text, tip, start, end}.
    """
    entitati = []

    patterns = [
        # DATE — DD.MM.YYYY sau DD/MM/YYYY
        ("DATA",
         r'\b\d{1,2}[./]\d{1,2}[./]\d{4}\b'),
        # DATE — luna YYYY
        ("DATA",
         r'\b(?:ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|'
         r'septembrie|octombrie|noiembrie|decembrie)\s+\d{4}\b'),
        # DATA — campania YYYY
        ("DATA",
         r'\bcampania\s+\d{4}\b'),

        # SUPRAFATA — numere cu ha
        ("SUPRAFATA",
         r'\b\d+[.,]\d+\s*ha\b|\b\d+\s*ha\b|\b\d+[.,]\d+\s*hectare?\b'),

        # NDVI — valori 0.xx
        ("NDVI",
         r'\bNDVI(?:\s+(?:mediu|minim|maxim|de|masurat|verificat))?\s*(?:de\s*)?:?\s*'
         r'(0[.,]\d{1,3})\b|'
         r'\b(?:valoare|indice)\s+NDVI\s*(?:de\s*)?(0[.,]\d{1,3})\b'),

        # PROCENTE
        ("PROCENT",
         r'\b\d+[.,]?\d*\s*%'),

        # COD PARCELA — format LPIS
        ("COD_PARCELA",
         r'\b[A-Z]{2,5}[-_][A-Z]{2,5}[-_]\d{3,6}\b|'
         r'\b[A-Z]{1,2}\d+/[A-Z]\b|'
         r'\bGJ-\d{4}-\d{3,8}\b'),

        # CNP / CUI
        ("CNP_CUI",
         r'\bCNP\s*:?\s*(\d{13})\b|'
         r'\bCUI\s*:?\s*([A-Z]{0,2}\d{6,10})\b|'
         r'\b(\d{13})\b'),

        # ORGANIZATII
        ("ORGANIZATIE",
         r'\b(?:APIA|MADR|OCPI|UCB|LPIS|IACS)\b|'
         r'\bCentrul\s+Judetean\s+\w+\b|'
         r'\bUniversitatea\s+din\s+\w+\b|'
         r'\bUniversitatea\s+[\w\s"]+\b(?=,|\s)'),

        # JUDETE SI LOCALITATI
        ("LOCATIE",
         r'\bjudetul?\s+(' + '|'.join(JUDETE_RO) + r')\b|'
         r'\b(?:localitatea|comuna|satul|orasul|municipiul)\s+[\w\-]+\b|'
         r'\b(' + '|'.join(JUDETE_RO) + r')\b'),

        # CULTURI
        ("CULTURA",
         r'\b(?:' + '|'.join(re.escape(c) for c in sorted(
             CULTURI_CUNOSCUTE, key=len, reverse=True)) + r')\b'),

        # PERSOANE — Nume Prenume (initiale sau cuvinte cu majuscula)
        ("PERSOANA",
         r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b(?!\s*(?:ha|%|km))|'
         r'\b[A-Z][a-z]+\.\s*[A-Z]\.[A-Z]\.\b'),
    ]

    for tip, pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            # Evita suprapuneri cu entitati deja gasite
            start, end = m.start(), m.end()
            overlap = any(
                not (end <= e["start"] or start >= e["end"])
                for e in entitati
            )
            if not overlap:
                # Curata textul gasit
                txt_gasit = m.group(0).strip()
                # Filtru calitate: ignora valori prea scurte
                if len(txt_gasit) < 2:
                    continue
                entitati.append({
                    "text":  txt_gasit,
                    "tip":   tip,
                    "start": start,
                    "end":   end,
                })

    return sorted(entitati, key=lambda x: x["start"])


def highlight_entitati(text: str, entitati: list[dict]) -> str:
    """
    Construieste HTML cu entitati evidentiate in culori diferite.
    """
    if not entitati:
        return f"<span>{text}</span>"

    html = ""
    cursor = 0
    for ent in entitati:
        start, end = ent["start"], ent["end"]
        if start < cursor:
            continue
        # Text normal inainte de entitate
        html += text[cursor:start].replace("\n", "<br>")
        # Entitate colorata
        cfg = TIPURI_ENTITATI.get(ent["tip"], {"culoare": "#888", "bg": "#eee", "icon": "•"})
        tip_label = ent["tip"]
        txt_label = ent["text"]
        html += (
            f"<span style='background:{cfg['bg']}; color:{cfg['culoare']}; "
            f"border-radius:4px; padding:1px 5px; margin:0 1px; "
            f"border-bottom:2px solid {cfg['culoare']}; font-weight:600; "
            f"font-size:13px; white-space:nowrap;' "
            f"title='{tip_label}'>"
            f"{txt_label}"
            f"<sup style='font-size:9px; margin-left:2px; opacity:0.7;'>"
            f"{cfg['icon']}</sup></span>"
        )
        cursor = end

    html += text[cursor:].replace("\n", "<br>")
    return html


def grupeaza_entitati(entitati: list[dict]) -> dict[str, list[str]]:
    """Grupeaza entitatile extrase pe tip, elimina duplicate."""
    grupuri = {}
    for ent in entitati:
        tip = ent["tip"]
        if tip not in grupuri:
            grupuri[tip] = []
        val = ent["text"].strip()
        if val not in grupuri[tip]:
            grupuri[tip].append(val)
    return grupuri


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠 Teorie",
    "🔍 NER pe Document",
    "📊 Entitati Structurate",
    "📁 Procesare in Lot",
    "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Ce este Named Entity Recognition (NER)?")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**NER** = identificarea si clasificarea automata a **entitatilor** dintr-un text:
persoane, locatii, organizatii, date, valori numerice.

#### Exemplu concret APIA

```
"Inspectorul Ionescu Gheorghe a verificat la data de 14.04.2024
 parcela GORJ_BF_00234 (12.40 ha grau) din judetul Gorj.
 NDVI masurat: 0.62. Diferenta suprafata: 3.42%."

         ↓ NER ↓

PERSOANA:    Ionescu Gheorghe
DATA:        14.04.2024
COD_PARCELA: GORJ_BF_00234
SUPRAFATA:   12.40 ha
CULTURA:     grau
LOCATIE:     judetul Gorj
NDVI:        0.62
PROCENT:     3.42%
```

#### Abordari NER

| Abordare | Tehnica | Avantaj |
|---|---|---|
| **Regex** | Expresii regulate per tip | Rapid, fara model, precis pe date structurate |
| **Dictionar** | Lista de entitati cunoscute | Bun pentru vocabular fix (judete, culturi) |
| **CRF** | Conditional Random Fields | Clasic ML pentru secvente |
| **BERT NER** | Fine-tuned BERT | Cel mai precis, intelege contextul |

#### Tipuri standard de entitati (CoNLL-2003)
- **PER** — Persoane (Person)
- **LOC** — Locatii (Location)
- **ORG** — Organizatii (Organization)
- **MISC** — Diverse (Miscellaneous)

#### Extensii pentru domeniu agricol APIA
- **SUPRAFATA** — valori in hectare
- **NDVI** — indici de vegetatie
- **COD_PARCELA** — coduri LPIS/IACS
- **CULTURA** — tipuri de culturi
- **CNP_CUI** — identificatori fermieri
""")

    with col2:
        st.markdown("""
<div style='background:#f3e5f5; border-radius:10px; padding:14px;
     border-top:4px solid #8e44ad;'>
<div style='font-weight:700; color:#8e44ad;'>Tipuri de entitati — Ziua 17</div>
<div style='font-size:11px; margin-top:10px;'>
""", unsafe_allow_html=True)

        for tip, cfg in TIPURI_ENTITATI.items():
            st.markdown(f"""
<div style='display:flex; align-items:center; gap:8px; padding:4px 8px;
     margin:3px 0; border-radius:6px; background:{cfg["bg"]};'>
<span style='font-size:14px;'>{cfg["icon"]}</span>
<b style='color:{cfg["culoare"]}; min-width:110px; font-size:12px;'>{tip}</b>
<span style='color:#555; font-size:11px;'>{cfg["desc"]}</span>
</div>""", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f5e9; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Aplicatie APIA directa</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.7;'>
Din rapoartele de control (PDF/Word scanat → OCR → NER):<br><br>
→ Extrage automat <b>toti fermierii</b> mentionati<br>
→ Identifica <b>toate parcelele</b> cu coduri LPIS<br>
→ Colecteaza <b>toate valorile NDVI</b> intr-un tabel<br>
→ Detecteaza <b>toate suprafetele</b> si diferentele<br><br>
Rezultat: baza de date structurata din text nestructurat.
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.subheader("Cum functioneaza BERT NER?")
    st.markdown("""
```
Input: "Ionescu Gheorghe a verificat parcela GORJ_BF_00234"
         ↓ Tokenizare
["Ion", "##escu", "Ghe", "##orghe", "a", "verificat", "parcela", "GOR", "##J", "_", "BF", "_", "00234"]
         ↓ BERT Encoder → vector 768D per token
         ↓ Classification Head (Linear layer)
Token   →  Eticheta BIO
"Ion"   →  B-PER   (Beginning of Person)
"##escu"→  I-PER   (Inside Person)
"Ghe"   →  B-PER
"##orghe" → I-PER
"a"     →  O       (Outside — nu e entitate)
"GOR"   →  B-LOC
...
         ↓ Agregare tokeni → entitati complete
PERSOANA: "Ionescu Gheorghe"
COD:      "GORJ_BF_00234"
```
**Schema BIO** = **B**eginning / **I**nside / **O**utside — standard NER.
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — NER PE DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Extragere entitati dintr-un document APIA")

    col_l, col_r = st.columns([1, 2])

    with col_l:
        doc_ales = st.selectbox(
            "Alege document:",
            ["(text propriu)"] + list(TEXTE_NER.keys()),
            key="doc_ner"
        )
        if doc_ales == "(text propriu)":
            text_ner = st.text_area(
                "Introdu textul:",
                value="",
                height=220,
                placeholder="Scrie sau lipeste un document APIA...",
                key="text_ner_custom"
            )
        else:
            text_ner = st.text_area(
                "Document (editabil):",
                value=TEXTE_NER[doc_ales],
                height=220,
                key="text_ner_sel"
            )

        # Tipuri active
        st.markdown("**Tipuri entitati active:**")
        tipuri_active = {}
        cols_tip = st.columns(2)
        for i, (tip, cfg) in enumerate(TIPURI_ENTITATI.items()):
            with cols_tip[i % 2]:
                tipuri_active[tip] = st.checkbox(
                    f"{cfg['icon']} {tip}", value=True, key=f"tip_{tip}"
                )

        ruleaza_ner = st.button("Extrage Entitati", type="primary",
                                 use_container_width=True, key="btn_ner")

    with col_r:
        if ruleaza_ner and text_ner and text_ner.strip():
            # Alegere motor
            if HF_OK:
                metoda_info = "Hugging Face NER (multilingual BERT)"
            else:
                metoda_info = "Regex NER (expresii regulate APIA)"

            with st.spinner("Extrag entitati..."):
                # NER Regex (mereu disponibil)
                entitati_toate = ner_regex(text_ner)

                # Filtreaza dupa tipuri active
                entitati = [e for e in entitati_toate
                            if tipuri_active.get(e["tip"], True)]

                # Optiune HF NER (daca e instalat)
                if HF_OK:
                    try:
                        @st.cache_resource(show_spinner=False)
                        def incarca_ner_model():
                            return hf_pipeline(
                                "ner",
                                model="Davlan/bert-base-multilingual-cased-ner-hrl",
                                aggregation_strategy="simple"
                            )
                        ner_hf = incarca_ner_model()
                        rez_hf = ner_hf(text_ner[:512])
                        # Adauga entitatile HF la cele regex
                        MAP_HF = {"PER": "PERSOANA", "LOC": "LOCATIE",
                                  "ORG": "ORGANIZATIE", "MISC": "ORGANIZATIE"}
                        for ent_hf in rez_hf:
                            tip_map = MAP_HF.get(ent_hf["entity_group"], None)
                            if tip_map and tipuri_active.get(tip_map, True):
                                overlap = any(
                                    not (ent_hf["end"] <= e["start"]
                                         or ent_hf["start"] >= e["end"])
                                    for e in entitati
                                )
                                if not overlap:
                                    entitati.append({
                                        "text":  ent_hf["word"],
                                        "tip":   tip_map,
                                        "start": ent_hf["start"],
                                        "end":   ent_hf["end"],
                                        "scor":  round(ent_hf["score"], 3),
                                    })
                        entitati = sorted(entitati, key=lambda x: x["start"])
                        metoda_info = "Regex + HF BERT multilingual"
                    except Exception:
                        pass

            # Salveaza in session state
            st.session_state["entitati_ner"]  = entitati
            st.session_state["text_ner_curent"] = text_ner

            # Metrici
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Entitati gasite", len(entitati))
            with c2:
                tipuri_gasite = len(set(e["tip"] for e in entitati))
                st.metric("Tipuri distincte", tipuri_gasite)
            with c3:
                st.metric("Motor NER", metoda_info.split(" ")[0])

            # Text cu highlight
            st.markdown("**Text cu entitati evidentiate:**")
            html_highlight = highlight_entitati(text_ner, entitati)
            st.markdown(f"""
<div style='background:#fdfcff; border:1px solid #e0d7f0; border-radius:10px;
     padding:16px 20px; font-size:14px; line-height:1.9; color:#333;'>
{html_highlight}
</div>""", unsafe_allow_html=True)

            # Legenda culori
            st.markdown("**Legenda:**")
            legenda_html = ""
            tipuri_prezente = set(e["tip"] for e in entitati)
            for tip in tipuri_prezente:
                cfg = TIPURI_ENTITATI.get(tip, {"culoare": "#888", "bg": "#eee", "icon": "•"})
                legenda_html += (
                    f"<span style='background:{cfg['bg']}; color:{cfg['culoare']}; "
                    f"border-radius:4px; padding:3px 10px; margin:3px; "
                    f"border-bottom:2px solid {cfg['culoare']}; "
                    f"font-size:12px; font-weight:600; display:inline-block;'>"
                    f"{cfg['icon']} {tip}</span>"
                )
            st.markdown(legenda_html, unsafe_allow_html=True)

        elif ruleaza_ner:
            st.warning("Introdu un text pentru analiza.")
        else:
            st.info("Alege un document si apasa **Extrage Entitati**.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ENTITATI STRUCTURATE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Entitati structurate — tabel si statistici")

    if "entitati_ner" not in st.session_state or not st.session_state["entitati_ner"]:
        st.info("Mergi la **NER pe Document** si extrage entitatile mai intai.")
    else:
        entitati = st.session_state["entitati_ner"]
        grupuri  = grupeaza_entitati(entitati)

        # Carduri per tip
        tipuri_ord = [t for t in TIPURI_ENTITATI if t in grupuri]
        cols_cards = st.columns(min(len(tipuri_ord), 3))
        for i, tip in enumerate(tipuri_ord):
            cfg = TIPURI_ENTITATI[tip]
            with cols_cards[i % 3]:
                valori = grupuri[tip]
                val_html = "".join(
                    f"<div style='padding:3px 8px; margin:2px 0; background:white; "
                    f"border-radius:4px; font-size:12px; color:#333;'>{v}</div>"
                    for v in valori
                )
                st.markdown(f"""
<div style='background:{cfg["bg"]}; border-radius:10px; padding:12px;
     border-top:3px solid {cfg["culoare"]}; margin-bottom:10px;'>
<div style='font-size:16px;'>{cfg["icon"]} <b style='color:{cfg["culoare"]};'>{tip}</b>
<span style='float:right; background:{cfg["culoare"]}; color:white;
font-size:12px; padding:1px 8px; border-radius:10px;'>{len(valori)}</span></div>
<div style='margin-top:8px;'>{val_html}</div>
</div>""", unsafe_allow_html=True)

        # Tabel complet
        st.divider()
        st.markdown("**Tabel complet entitati:**")
        import pandas as pd
        df_ent = pd.DataFrame([{
            "Tip":    e["tip"],
            "Entitate": e["text"],
            "Pozitie": f"{e['start']}-{e['end']}",
        } for e in entitati])

        def stil_tip(val):
            cfg = TIPURI_ENTITATI.get(val, {"bg": "#f5f5f5", "culoare": "#888"})
            return f"background-color:{cfg['bg']}; color:{cfg['culoare']}; font-weight:600"

        st.dataframe(
            df_ent.style.applymap(stil_tip, subset=["Tip"]),
            use_container_width=True,
            hide_index=True
        )

        # Grafic distributie tipuri
        if PLOTLY_OK:
            frecvente = df_ent["Tip"].value_counts()
            culori_bar = [
                TIPURI_ENTITATI.get(t, {}).get("culoare", "#888")
                for t in frecvente.index
            ]
            fig = go.Figure(go.Bar(
                x=frecvente.index.tolist(),
                y=frecvente.values.tolist(),
                marker_color=culori_bar,
                text=frecvente.values.tolist(),
                textposition="outside"
            ))
            fig.update_layout(
                title="Distributia entitatilor per tip",
                yaxis_title="Numar entitati",
                height=300,
                margin=dict(t=40, b=40),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        # Download
        csv_ent = df_ent.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descarca entitati CSV",
            data=csv_ent,
            file_name=f"entitati_ner_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PROCESARE IN LOT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Procesare in lot — extragere entitati din multiple documente")

    st.markdown("""
Simuleaza procesarea unui inbox APIA: extrage automat date cheie
din toate documentele si consolideaza intr-un singur tabel.
""")

    if st.button("Proceseaza toate documentele demo", type="primary", key="btn_lot_ner"):
        import pandas as pd

        randuri = []
        for titlu, text in TEXTE_NER.items():
            ents = ner_regex(text)
            grupuri = grupeaza_entitati(ents)
            randuri.append({
                "Document":    titlu[:40],
                "Persoane":    ", ".join(grupuri.get("PERSOANA", ["—"])[:3]),
                "Locatii":     ", ".join(grupuri.get("LOCATIE",  ["—"])[:3]),
                "Organizatii": ", ".join(grupuri.get("ORGANIZATIE", ["—"])[:2]),
                "Date":        ", ".join(grupuri.get("DATA",     ["—"])[:3]),
                "Suprafete":   ", ".join(grupuri.get("SUPRAFATA",["—"])[:3]),
                "NDVI":        ", ".join(grupuri.get("NDVI",     ["—"])[:3]),
                "Coduri parc.":  ", ".join(grupuri.get("COD_PARCELA", ["—"])[:2]),
                "Nr. entitati":  len(ents),
            })

        df_lot = pd.DataFrame(randuri)
        st.dataframe(df_lot, use_container_width=True, hide_index=True)

        st.success(f"""
**Rezultat procesare lot:**
- {len(randuri)} documente procesate
- {sum(r['Nr. entitati'] for r in randuri)} entitati totale extrase
- Date disponibile imediat pentru baza de date APIA
""")

        # Export
        csv_lot = df_lot.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descarca tabel consolidat CSV",
            data=csv_lot,
            file_name=f"entitati_lot_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

    else:
        st.info("Apasa butonul pentru a procesa toate documentele simultan.")

    st.divider()
    st.markdown("### Flux complet OCR → NER → Baza de date")
    st.markdown("""
```
Document fizic (hartie)
    ↓
[Scanner / Fotografie drone]
    ↓
[Z11 — OCR Tesseract] → Text brut
    ↓
[Z17 — NER Regex/BERT] → Entitati structurate
    ↓
[Export CSV / JSON] → Baza de date APIA
    ↓
[Cautare / Filtrare / Raportare]
```

Aceasta este pipline-ul complet de digitalizare automata a documentelor APIA,
direct aplicabil in activitatea de control pe teren.
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ce am invatat azi — Ziua 17")

    concepte = [
        ("NER", "Named Entity Recognition — identificare si clasificare entitati in text"),
        ("Tipuri entitati", "PER, LOC, ORG, DATE standard + SUPRAFATA, NDVI, COD specific APIA"),
        ("Schema BIO",   "B=Beginning, I=Inside, O=Outside — etichetare standard NER"),
        ("Regex NER",    "Expresii regulate pentru tipuri structurate: date, suprafete, coduri"),
        ("BERT NER",     "Fine-tuned BERT clasificare per token → entitati cu context"),
        ("highlight()",  "Vizualizare HTML cu fundal colorat per tip de entitate"),
        ("grupeaza()",   "Consolideaza entitati duplicate, organizeaza per tip"),
        ("Procesare lot","Extragere entitati din multiple documente → tabel consolidat"),
        ("OCR + NER",    "Pipeline complet: document fizic → text → date structurate"),
    ]

    for concept, descriere in concepte:
        st.markdown(f"""
<div style='display:flex; gap:12px; padding:8px 14px; margin:4px 0;
     background:#f8f9fa; border-radius:8px; font-size:13px;
     border-left:4px solid #8e44ad;'>
<b style='color:#8e44ad; min-width:160px;'>{concept}</b>
<span style='color:#333;'>{descriere}</span>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.code("""
# NER Regex — fara dependente externe
import re

patterns = {
    "SUPRAFATA":   r'\\b\\d+[.,]\\d+\\s*ha\\b',
    "DATA":        r'\\b\\d{1,2}[./]\\d{1,2}[./]\\d{4}\\b',
    "NDVI":        r'\\bNDVI\\s*:?\\s*(0[.,]\\d{2,3})\\b',
    "COD_PARCELA": r'\\b[A-Z]{2,5}[-_][A-Z]{2,5}[-_]\\d{3,6}\\b',
    "CNP":         r'\\bCNP\\s*:?\\s*(\\d{13})\\b',
}

text = "Parcela GORJ_BF_00234 are 12.40 ha, NDVI 0.62, data 14.04.2024"

for tip, pat in patterns.items():
    for m in re.finditer(pat, text, re.IGNORECASE):
        print(f"{tip}: {m.group(0)!r}")

# NER Hugging Face — multilingual BERT
from transformers import pipeline
ner = pipeline("ner",
               model="Davlan/bert-base-multilingual-cased-ner-hrl",
               aggregation_strategy="simple")
entitati = ner("Ionescu Gheorghe a verificat parcela din Gorj.")
for e in entitati:
    print(f"{e['entity_group']}: {e['word']} ({e['score']:.2f})")
""", language="python")

    st.info("""
**Ziua 18 — Sinteza Modul 3: NLP Complet**

Pipeline integrat NLP:
- Clasificare document (Z15) → ce tip de document e
- Rezumare (Z16) → rezumat scurt
- NER (Z17) → extrage toate datele structurate
- Export final → raport complet + CSV pentru APIA
""")

    st.markdown("""
---
*Referinta: "Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"
— Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, Universitatea din Petrosani, 2024*
""")
