"""
Ziua 15 — Clasificare Texte Agricole cu NLP
Modul 3: NLP Aplicat — Hugging Face Zero-Shot + TF-IDF + Naive Bayes
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import re
import math
import datetime
from collections import defaultdict

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
    page_title="Ziua 15 — Clasificare Texte NLP",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🏷️</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 15</div>
    <div style='font-size:11px; color:#666;'>Clasificare Texte Agricole NLP</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 3 — NLP Aplicat")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 15 / 30 zile")
st.sidebar.progress(15 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 15:**
- Clasificare text supervizata
- Zero-shot classification (HF)
- TF-IDF + Naive Bayes (demo)
- Categorii documente APIA
- Evaluare clasificator (acuratete)
- Clasificare multipla simultana
""")
st.sidebar.divider()
if HF_OK:
    st.sidebar.success("transformers instalat")
else:
    st.sidebar.warning("transformers absent — demo activ")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🏷️</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 15 — Clasificare Texte Agricole
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 3 — NLP Aplicat &nbsp;|&nbsp;
            Zero-Shot Classification + TF-IDF Naive Bayes — sortare automata documente APIA
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
# DATE DEMO — texte si categorii APIA
# ══════════════════════════════════════════════════════════════════════════════

CATEGORII_APIA = [
    "Cerere PAC",
    "Raport control teren",
    "Reclamatie fermier",
    "Notificare APIA",
    "Decizie sanctiune",
    "Raport NDVI analiza",
]

TEXTE_DEMO = [
    {
        "text": "Subsemnatul Ionescu Gheorghe, fermier inregistrat la APIA Gorj, "
                "depun prezenta cerere unica de plata pentru suprafata de 45.3 ha "
                "cultivata cu grau de toamna si floarea-soarelui in campania 2024. "
                "Anexez documentele cadastrale si contractele de arendare.",
        "categorie_reala": "Cerere PAC",
    },
    {
        "text": "In urma controlului pe teren efectuat in data de 14 aprilie 2024 "
                "la parcela GJ-045, s-a constatat ca suprafata efectiv cultivata "
                "este de 38.7 ha, cu o diferenta de 6.6 ha fata de suprafata "
                "declarata. NDVI mediu masurat: 0.42. Se propune reducerea platii.",
        "categorie_reala": "Raport control teren",
    },
    {
        "text": "Subsemnata Popescu Maria formulez urmatoarea reclamatie: in urma "
                "controlului APIA din 10 martie, inspectorul a masurat incorect "
                "suprafata parcelei mele. Solicit reverificarea datelor si "
                "corectarea erorii comise in raportul de control.",
        "categorie_reala": "Reclamatie fermier",
    },
    {
        "text": "APIA Centrul Judetean Gorj va notifica prin prezenta ca in "
                "perioada 15-30 aprilie 2024 se efectueaza verificari LPIS in "
                "zona Targu Jiu. Fermierii sunt rugati sa asigure accesul "
                "inspectorilor pe parcele si sa prezinte documentele solicitate.",
        "categorie_reala": "Notificare APIA",
    },
    {
        "text": "In temeiul Regulamentului UE 2021/2116, ca urmare a constatarii "
                "neconformitatilor la controlul din data de 20 martie 2024, "
                "se aplica o reducere de 15% din plata directa pentru campania "
                "2024. Decizia poate fi contestata in 30 de zile.",
        "categorie_reala": "Decizie sanctiune",
    },
    {
        "text": "Analiza imaginilor multispectrale achizitionate cu drona DJI "
                "Phantom 4 Multispectral la altitudinea de 100m a indicat un "
                "NDVI mediu de 0.61 pentru cultura de grau. Zona de stress "
                "hidric reprezinta 8.3% din suprafata totala a parcelei GJ-112.",
        "categorie_reala": "Raport NDVI analiza",
    },
    {
        "text": "Solicit sprijin financiar prin schema de plata de baza pentru "
                "suprafata de 22 ha situata in judetul Gorj, localitatea Bumbesti. "
                "Culturile declarate: porumb 14 ha, lucerna 8 ha. Documente "
                "atasate: act identitate, extras CF, plan parcele.",
        "categorie_reala": "Cerere PAC",
    },
    {
        "text": "In urma sesizarii primite, echipa de inspectie APIA a efectuat "
                "un control inopinant la ferma Agricola Sud SRL. "
                "S-au constatat culturi nedeclarate pe o suprafata de 3.2 ha. "
                "Se intocmeste proces verbal de constatare a neconformitatii.",
        "categorie_reala": "Raport control teren",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# CLASIFICATOR DEMO (TF-IDF + Naive Bayes simplificat)
# ══════════════════════════════════════════════════════════════════════════════

# Vocabular caracteristic per categorie
VOCABULAR_CATEGORII = {
    "Cerere PAC": [
        "cerere", "solicit", "depun", "plata", "subventie", "campanie",
        "suprafata", "cultivata", "anexez", "documente", "cadastrale",
        "arendare", "fermier", "inregistrat", "schema", "baza", "directa"
    ],
    "Raport control teren": [
        "control", "teren", "constatat", "inspector", "verificare",
        "diferenta", "masurat", "efectiv", "reducere", "propune",
        "inopinant", "sesizare", "echipa", "inspectie", "proces", "verbal"
    ],
    "Reclamatie fermier": [
        "reclamatie", "formulez", "subsemnata", "subsemnatul", "incorect",
        "eroare", "solicit", "reverificare", "corectarea", "contestatie",
        "nemultumire", "problema", "gresit", "eronat"
    ],
    "Notificare APIA": [
        "notifica", "notificare", "informam", "perioada", "rugati",
        "asigure", "accesul", "prezinte", "atentie", "anuntam",
        "programul", "calendar", "termen", "data"
    ],
    "Decizie sanctiune": [
        "temeiul", "regulamentului", "reducere", "sanctiune", "decizie",
        "neconformitate", "aplicare", "procent", "contestata", "zile",
        "penalizare", "retinere", "suma", "amenda"
    ],
    "Raport NDVI analiza": [
        "ndvi", "multispectral", "drona", "analiza", "imagini", "altitudine",
        "stress", "hidric", "zona", "procent", "indice", "vegetatie",
        "spectral", "pixel", "harta", "culoare"
    ],
}

def calculeaza_scor_categorie(text: str, vocabular: list[str]) -> float:
    """Calculeaza un scor simplu: cate cuvinte din vocabular apar in text."""
    cuvinte_text = set(re.findall(r'\b\w+\b', text.lower()))
    potriviri = sum(1 for c in vocabular if c in cuvinte_text)
    return potriviri / len(vocabular) if vocabular else 0.0

def clasificare_demo(text: str) -> list[dict]:
    """Clasificare bazata pe vocabular caracteristic per categorie."""
    scoruri = []
    for categorie, vocabular in VOCABULAR_CATEGORII.items():
        scor = calculeaza_scor_categorie(text, vocabular)
        scoruri.append({"label": categorie, "score": scor})

    # Normalizeaza scorurile
    total = sum(s["score"] for s in scoruri) or 1.0
    for s in scoruri:
        s["score"] = round(s["score"] / total, 4) if total > 0 else round(1/len(scoruri), 4)

    return sorted(scoruri, key=lambda x: x["score"], reverse=True)

def evalueaza_clasificator(texte: list[dict]) -> dict:
    """Evalueaza acuratetea clasificatorului demo pe textele de test."""
    corecte = 0
    rezultate = []
    for item in texte:
        scoruri = clasificare_demo(item["text"])
        prezis = scoruri[0]["label"]
        corect = prezis == item["categorie_reala"]
        if corect:
            corecte += 1
        rezultate.append({
            "text_preview": item["text"][:60] + "...",
            "categorie_reala": item["categorie_reala"],
            "categorie_prezisa": prezis,
            "corect": corect,
            "incredere": f"{scoruri[0]['score']*100:.1f}%"
        })
    acuratete = corecte / len(texte) if texte else 0
    return {"acuratete": acuratete, "corecte": corecte,
            "total": len(texte), "detalii": rezultate}

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠 Teorie",
    "🏷️ Clasificare Document",
    "📦 Clasificare in Lot",
    "📊 Evaluare Clasificator",
    "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Clasificarea textelor — sortare automata documente APIA")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**Clasificarea textelor** = atribuirea automata a unei etichete (categorie)
unui text dat, pe baza continutului sau.

#### Tipuri de clasificare
| Tip | Descriere | Exemplu APIA |
|---|---|---|
| **Binara** | 2 clase | Cerere valida / Cerere invalida |
| **Multiclasa** | N clase, o singura eticheta | Tip document (6 categorii) |
| **Multi-label** | N clase, mai multe etichete | Document cu cerere + reclamatie |
| **Zero-shot** | Fara antrenare pe date noi | Orice categorii definite ad-hoc |

#### Abordari tehnice

**1. TF-IDF + Naive Bayes (clasic)**
```
Text → TF-IDF vectorizare → Naive Bayes → Eticheta
Avantaj: rapid, interpretabil, functioneaza pe date putine
Dezavantaj: nu intelege contextul, sensibil la vocabular
```

**2. Zero-Shot Classification (Hugging Face)**
```
Text + Lista categorii → Model BART/NLI → Scoruri per categorie
Avantaj: nu necesita antrenare, categorii definite liber
Dezavantaj: mai lent, necesita GPU pentru productie
```

**3. Fine-tuning BERT (avansat)**
```
Date antrenare (text + eticheta) → Fine-tune BERT → Clasificator
Avantaj: performanta maxima pe domeniu specific
Dezavantaj: necesita 500-1000 exemple etichetate
```

#### Aplicatii APIA practice
- Sortare automata a cererilor la primire (6 tipuri)
- Prioritizare reclamatii urgente
- Rutare automata catre departamentul potrivit
- Detectie duplicate (aceeasi cerere trimisa de mai multe ori)
- Clasificare documente istorice scanate
""")

    with col2:
        st.markdown("""
<div style='background:#f3e5f5; border-radius:10px; padding:14px;
     border-top:4px solid #8e44ad;'>
<div style='font-weight:700; color:#8e44ad;'>Zero-Shot Classification</div>
<div style='font-size:11px; color:#333; margin-top:10px; line-height:1.7;'>
Cel mai puternic instrument NLP pentru clasificare <b>fara date de antrenare</b>.<br><br>
Modelul (BART-large-mnli) a invatat sa inteleaga relatia dintre un text
si o ipoteza: <i>"Acest text este despre [categorie]"</i><br><br>
Daca ipoteza este <b>adevarata</b> → scor mare → categorie prezisa.<br><br>
<code>
pipeline("zero-shot-classification",<br>
&nbsp;&nbsp;model="facebook/bart-large-mnli")
</code><br><br>
Functioeaza in <b>orice limba</b> cu modelul multilingual:<br>
<code>joeddav/xlm-roberta-large-xnli</code>
</div></div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f5e9; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Categorii documente APIA</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.8;'>
""" + "".join([
    f"<span style='background:#e8f5e9; padding:2px 8px; margin:2px; "
    f"border-radius:4px; display:inline-block;'>{cat}</span>"
    for cat in CATEGORII_APIA
]) + """
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.subheader("Teorema Bayes in clasificarea textelor")
    st.markdown(r"""
**Naive Bayes** calculeaza probabilitatea ca un text sa apartina unei categorii:

$$P(Categorie | Text) = \frac{P(Text | Categorie) \times P(Categorie)}{P(Text)}$$

**"Naive"** = presupune independenta cuvintelor (simplificare utila in practica).

Exemplu intuitiv:
- Daca textul contine cuvantul *"reclamatie"* → probabilitate mare pentru categoria `Reclamatie fermier`
- Daca contine *"NDVI"* + *"drona"* → probabilitate mare pentru `Raport NDVI analiza`
- Combina toate cuvintele si alege categoria cu probabilitate maxima
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CLASIFICARE DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Clasificare document individual")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Selector text predefinit
        optiuni = ["(text propriu)"] + [
            f"{t['categorie_reala']} — exemplu {i+1}"
            for i, t in enumerate(TEXTE_DEMO)
        ]
        selectie = st.selectbox("Alege un text predefinit:", optiuni, key="sel_doc")

        if selectie == "(text propriu)":
            text_clasificare = st.text_area(
                "Introdu textul documentului APIA:",
                value="",
                height=160,
                placeholder="Ex: Subsemnatul Ionescu Gheorghe depun cerere de plata...",
                key="text_custom"
            )
        else:
            idx = optiuni.index(selectie) - 1
            text_clasificare = st.text_area(
                "Text selectat (editabil):",
                value=TEXTE_DEMO[idx]["text"],
                height=160,
                key="text_predef"
            )
            st.info(f"Categoria reala: **{TEXTE_DEMO[idx]['categorie_reala']}**")

        # Categorii custom
        with st.expander("Modifica categoriile de clasificare"):
            categorii_input = st.text_area(
                "Categorii (una per linie):",
                value="\n".join(CATEGORII_APIA),
                height=150,
                key="categorii_custom"
            )
            categorii_folosite = [c.strip() for c in categorii_input.split("\n") if c.strip()]
        if not categorii_folosite:
            categorii_folosite = CATEGORII_APIA

        clasifica_btn = st.button("Clasifica Documentul", type="primary",
                                   use_container_width=True, key="btn_cls")

    with col_right:
        st.markdown("""
<div style='background:#f3e5f5; border-radius:10px; padding:14px;'>
<div style='font-weight:700; color:#8e44ad;'>Metoda activa</div>
<div style='font-size:12px; color:#333; margin-top:8px; line-height:1.7;'>
""" + (
    "Hugging Face <b>Zero-Shot Classification</b><br>"
    "Model: joeddav/xlm-roberta-large-xnli<br>"
    "Suporta texte romanesti."
    if HF_OK else
    "<b>Demo — vocabular caracteristic</b><br>"
    "Numara cuvinte specifice per categorie,<br>"
    "normalizeaza si returneaza scoruri.<br>"
    "Instaleaza <code>transformers torch</code>"
    " pentru model real."
) + """
</div></div>
""", unsafe_allow_html=True)

        st.markdown("**Categorii active:**")
        for cat in categorii_folosite:
            st.markdown(f"""
<span style='display:inline-block; background:#e8eaf6; padding:3px 10px;
margin:2px; border-radius:12px; font-size:12px; color:#3949ab;'>{cat}</span>""",
unsafe_allow_html=True)

    # ─── Rezultat clasificare ─────────────────────────────────────────────────
    if clasifica_btn and text_clasificare and text_clasificare.strip():
        st.divider()

        if HF_OK:
            with st.spinner("Se incarca modelul (prima rulare ~1.5GB)..."):
                try:
                    @st.cache_resource(show_spinner=False)
                    def incarca_zero_shot():
                        return hf_pipeline(
                            "zero-shot-classification",
                            model="joeddav/xlm-roberta-large-xnli"
                        )
                    clf = incarca_zero_shot()
                    rez_hf = clf(text_clasificare[:512], candidate_labels=categorii_folosite)
                    scoruri = [{"label": l, "score": round(s, 4)}
                               for l, s in zip(rez_hf["labels"], rez_hf["scores"])]
                    metoda = "Hugging Face XLM-RoBERTa (Zero-Shot)"
                except Exception as e:
                    st.warning(f"Model HF indisponibil ({e}), folosesc demo.")
                    scoruri = clasificare_demo(text_clasificare)
                    metoda = "Demo (vocabular)"
        else:
            scoruri = clasificare_demo(text_clasificare)
            metoda = "Demo (vocabular caracteristic)"

        # Categoria principala
        top = scoruri[0]
        culoare_top = "#8e44ad"
        st.markdown(f"""
<div style='background:{culoare_top}22; border:2px solid {culoare_top};
     border-radius:12px; padding:16px 20px; margin-bottom:16px;'>
<div style='font-size:13px; color:#555;'>Categorie detectata</div>
<div style='font-size:26px; font-weight:800; color:{culoare_top};'>{top["label"]}</div>
<div style='font-size:14px; color:#555; margin-top:4px;'>
    Incredere: <b>{top["score"]*100:.1f}%</b> &nbsp;|&nbsp; Metoda: {metoda}
</div>
</div>""", unsafe_allow_html=True)

        # Toate scorurile
        col_sc, col_gr = st.columns([1, 2])
        with col_sc:
            st.markdown("**Toate categoriile:**")
            for s in scoruri:
                procent = s["score"] * 100
                culoare = "#8e44ad" if s == top else "#bdc3c7"
                st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center;
     padding:5px 10px; margin:3px 0; border-radius:6px;
     background:{"#f3e5f5" if s==top else "#f8f9fa"};
     border-left:4px solid {culoare}; font-size:12px;'>
<span style='color:#333;'>{s["label"]}</span>
<b style='color:{culoare};'>{procent:.1f}%</b>
</div>""", unsafe_allow_html=True)

        with col_gr:
            if PLOTLY_OK:
                fig = go.Figure(go.Bar(
                    x=[s["score"] * 100 for s in reversed(scoruri)],
                    y=[s["label"] for s in reversed(scoruri)],
                    orientation="h",
                    marker_color=[
                        "#8e44ad" if s == top else "#bdc3c7"
                        for s in reversed(scoruri)
                    ],
                    text=[f"{s['score']*100:.1f}%" for s in reversed(scoruri)],
                    textposition="outside",
                ))
                fig.update_layout(
                    height=280,
                    xaxis=dict(range=[0, 105], title="Incredere (%)"),
                    margin=dict(t=10, b=30, l=10, r=60),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

    elif clasifica_btn:
        st.warning("Introdu un text pentru clasificare.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CLASIFICARE IN LOT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Clasificare in lot — multiple documente simultan")

    st.markdown("""
Clasifica automat toate textele demo si afiseaza un tabel cu rezultatele.
Util pentru procesarea unui inbox de documente APIA.
""")

    clasifica_tot = st.button("Clasifica toate documentele demo",
                               type="primary", key="btn_lot")

    if clasifica_tot:
        with st.spinner("Clasificare in curs..."):
            rezultate_lot = []
            for item in TEXTE_DEMO:
                scoruri = clasificare_demo(item["text"])
                top_cat = scoruri[0]
                corect  = top_cat["label"] == item["categorie_reala"]
                rezultate_lot.append({
                    "Text (preview)":     item["text"][:70] + "...",
                    "Categorie reala":    item["categorie_reala"],
                    "Categorie prezisa":  top_cat["label"],
                    "Incredere":          f"{top_cat['score']*100:.1f}%",
                    "Corect":             "✓" if corect else "✗",
                })

        import pandas as pd
        df_lot = pd.DataFrame(rezultate_lot)

        def stil_corect(val):
            if val == "✓":
                return "background-color:#d5f5e3; color:#1e8449; font-weight:700"
            return "background-color:#fadbd8; color:#922b21; font-weight:700"

        def stil_categorie(val):
            culori = {
                "Cerere PAC":          "#e8eaf6",
                "Raport control teren":"#e8f5e9",
                "Reclamatie fermier":  "#fce4ec",
                "Notificare APIA":     "#fff8e1",
                "Decizie sanctiune":   "#fbe9e7",
                "Raport NDVI analiza": "#e0f7fa",
            }
            return f"background-color:{culori.get(val, '#f5f5f5')}"

        st.dataframe(
            df_lot.style
                  .applymap(stil_corect, subset=["Corect"])
                  .applymap(stil_categorie, subset=["Categorie prezisa"]),
            use_container_width=True,
            hide_index=True
        )

        # Metrici sumar
        n_corecte = sum(1 for r in rezultate_lot if r["Corect"] == "✓")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Documente clasificate", len(rezultate_lot))
        with col2:
            st.metric("Clasificari corecte", n_corecte)
        with col3:
            st.metric("Acuratete",
                      f"{n_corecte/len(rezultate_lot)*100:.1f}%")

        # Distributie categorii prezise
        if PLOTLY_OK:
            from collections import Counter
            distributie = Counter(r["Categorie prezisa"] for r in rezultate_lot)
            fig_pie = go.Figure(go.Pie(
                labels=list(distributie.keys()),
                values=list(distributie.values()),
                hole=0.4,
                marker_colors=["#8e44ad", "#27ae60", "#e74c3c",
                                "#f39c12", "#2471a3", "#16a085"],
            ))
            fig_pie.update_layout(
                title="Distributia categoriilor detectate",
                height=320,
                margin=dict(t=40, b=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EVALUARE CLASIFICATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Evaluarea performantei clasificatorului")

    st.markdown("""
Cum stim daca clasificatorul nostru este bun?
Folosim metrici standard de evaluare.
""")

    evalueaza_btn = st.button("Evalueaza clasificatorul demo",
                               type="primary", key="btn_eval")

    if evalueaza_btn:
        eval_rez = evalueaza_clasificator(TEXTE_DEMO)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Acuratete", f"{eval_rez['acuratete']*100:.1f}%")
        with col2:
            st.metric("Clasificari corecte",
                      f"{eval_rez['corecte']} / {eval_rez['total']}")
        with col3:
            st.metric("Documente testate", eval_rez["total"])

        # Tabel detaliat
        import pandas as pd
        df_eval = pd.DataFrame(eval_rez["detalii"])
        df_eval.rename(columns={
            "text_preview":      "Text",
            "categorie_reala":   "Categorie reala",
            "categorie_prezisa": "Categorie prezisa",
            "corect":            "Corect",
            "incredere":         "Incredere",
        }, inplace=True)
        df_eval["Corect"] = df_eval["Corect"].map({True: "✓ DA", False: "✗ NU"})

        def stil_c(val):
            if "DA" in str(val):
                return "background-color:#d5f5e3; color:#1e8449; font-weight:700"
            return "background-color:#fadbd8; color:#922b21; font-weight:700"

        st.dataframe(
            df_eval.style.applymap(stil_c, subset=["Corect"]),
            use_container_width=True,
            hide_index=True
        )

    st.divider()
    st.markdown("### Metrici de evaluare NLP")

    metrici = [
        ("Acuratete (Accuracy)",
         "% clasificari corecte din total. Simplu dar poate fi inselator pe clase dezechilibrate."),
        ("Precizie (Precision)",
         "Din toate documentele clasificate ca X, cate chiar sunt X? (evita false pozitive)"),
        ("Recall (Sensibilitate)",
         "Din toate documentele X reale, cate au fost detectate? (evita false negative)"),
        ("F1-Score",
         "Media armonica Precizie-Recall. Echilibru intre cele doua."),
        ("Confusion Matrix",
         "Tabel N×N cu clasificarile corecte si gresite per categorie — vizualizare completa."),
        ("ROC-AUC",
         "Aria sub curba ROC — performanta la diferite praguri de decizie."),
    ]

    for metric, desc in metrici:
        st.markdown(f"""
<div style='display:flex; gap:12px; padding:8px 14px; margin:4px 0;
     background:#f8f9fa; border-radius:8px; font-size:13px;
     border-left:4px solid #8e44ad;'>
<b style='color:#8e44ad; min-width:200px;'>{metric}</b>
<span style='color:#333;'>{desc}</span>
</div>""", unsafe_allow_html=True)

    st.code("""
from sklearn.metrics import classification_report, confusion_matrix

# Calculeaza metrici complete
print(classification_report(
    y_true=categorii_reale,
    y_pred=categorii_prezise,
    target_names=CATEGORII_APIA
))
""", language="python")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ce am invatat azi — Ziua 15")

    concepte = [
        ("Clasificare text", "Atribuirea automata a unei etichete unui text pe baza continutului"),
        ("Zero-Shot", "Clasificare fara antrenare — categoriile se definesc ca text liber"),
        ("Naive Bayes", "Clasificator probabilistic bazat pe frecventa cuvintelor per categorie"),
        ("TF-IDF", "Vectorizare text: importanta relativa a cuvintelor in colectie"),
        ("pipeline() HF", "zero-shot-classification cu model BART/XLM-RoBERTa"),
        ("Acuratete", "% clasificari corecte — metrica principala de evaluare"),
        ("F1-Score", "Media armonica Precizie-Recall — metrica echilibrata"),
        ("Lot (batch)", "Clasificarea mai multor documente simultan — flux productie"),
        ("Categorii APIA", "Cerere PAC / Control / Reclamatie / Notificare / Decizie / NDVI"),
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
# Instalare
# pip install transformers torch

from transformers import pipeline

# Zero-Shot Classification — fara antrenare suplimentara
classifier = pipeline(
    "zero-shot-classification",
    model="joeddav/xlm-roberta-large-xnli"
)

text = "Depun cerere de plata pentru 45 ha grau, campania 2024."

rezultat = classifier(
    text,
    candidate_labels=[
        "Cerere PAC",
        "Raport control teren",
        "Reclamatie fermier",
        "Notificare APIA",
    ]
)

for label, score in zip(rezultat["labels"], rezultat["scores"]):
    print(f"{label:<25}: {score*100:.1f}%")
# Cerere PAC              : 87.3%
# Notificare APIA         : 6.1%
# Raport control teren    : 4.2%
# Reclamatie fermier      : 2.4%
""", language="python")

    st.info("""
**Ziua 16 — Rezumare Automata Documente**

Vom folosi Hugging Face `summarization` pipeline pentru a:
- Rezuma automat rapoarte lungi de control APIA
- Extrage ideile principale din cereri PAC
- Genera rezumate pentru articole agricole
""")

    st.markdown("""
---
*Referinta: "Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"
— Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, Universitatea din Petrosani, 2024*
""")
