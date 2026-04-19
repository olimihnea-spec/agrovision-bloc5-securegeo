"""
Ziua 13 — NLP: Procesarea Limbajului Natural cu Hugging Face
Modul 3: NLP Aplicat
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import re
import math
from datetime import date

# ─── Import optional transformers ─────────────────────────────────────────────
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
    page_title="Ziua 13 — NLP Introducere",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>📝</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 13</div>
    <div style='font-size:11px; color:#666;'>NLP — Procesarea Limbajului Natural</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 3 — NLP Aplicat")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 13 / 30 zile")
st.sidebar.progress(13/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 13:**
- Ce este NLP
- Tokenizare si vocabular
- Embeddings (reprezentare text)
- Arhitectura Transformer
- Hugging Face `pipeline`
- Aplicatii agricole NLP
""")
st.sidebar.divider()
if HF_OK:
    st.sidebar.success("Hugging Face transformers instalat")
else:
    st.sidebar.warning("transformers absent — mod demo activ")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>📝</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 13 — NLP: Procesarea Limbajului Natural
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 3 — NLP Aplicat &nbsp;|&nbsp;
            Hugging Face Transformers — analiza text, clasificare, documente APIA
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Banner teza
st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px;padding:12px 20px;margin-bottom:16px;'>
<span style='color:#f9e79f;font-size:13px;font-style:italic;'>
"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone" &nbsp;|&nbsp;
<b style='color:white;'>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | Universitatea din Petrosani, 2024</b>
</span></div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie",
    "🔤 Tokenizare & Vocabular",
    "🎯 Analiza Sentiment (demo)",
    "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# FUNCȚII NLP DEMO (fara transformers)
# ══════════════════════════════════════════════════════════════════════════════

CUVINTE_POZITIVE = {
    "bun", "buna", "excelent", "excelenta", "corect", "corecta", "conform",
    "aprobat", "aprobata", "valid", "valida", "clar", "clara", "complet",
    "completa", "normal", "sanatoasa", "sanatos", "verde", "productiv",
    "productiva", "ok", "satisfacator", "satisfacatoare", "adecvat", "adecvata"
}
CUVINTE_NEGATIVE = {
    "problema", "eroare", "gresit", "gresita", "lipsa", "absent", "absenta",
    "neconform", "neconforma", "respins", "respinsa", "invalid", "invalida",
    "stress", "seceta", "inundatie", "deteriorat", "deteriorata", "defect",
    "defecta", "incorect", "incorecta", "depasit", "depasita", "risc", "pericol"
}

def sentiment_demo(text: str) -> dict:
    """Analiza sentiment simpla bazata pe dictionar (fallback fara transformers)."""
    cuvinte = re.findall(r'\b\w+\b', text.lower())
    pos = sum(1 for c in cuvinte if c in CUVINTE_POZITIVE)
    neg = sum(1 for c in cuvinte if c in CUVINTE_NEGATIVE)
    total = pos + neg or 1
    scor_pos = pos / total
    scor_neg = neg / total
    if pos > neg:
        label, scor = "POZITIV", scor_pos
    elif neg > pos:
        label, scor = "NEGATIV", scor_neg
    else:
        label, scor = "NEUTRU", 0.5
    return {
        "label": label,
        "score": round(scor, 3),
        "pozitive": pos,
        "negative": neg,
        "cuvinte_cheie_pos": [c for c in cuvinte if c in CUVINTE_POZITIVE],
        "cuvinte_cheie_neg": [c for c in cuvinte if c in CUVINTE_NEGATIVE],
    }

def tokenizeaza_simplu(text: str) -> dict:
    """Tokenizare simpla: spatii + punctuatie."""
    tokens_spatiu = text.split()
    tokens_cuvinte = re.findall(r'\b\w+\b', text)
    tokens_caractere = list(text)
    subwords = []
    for cuv in tokens_cuvinte:
        if len(cuv) > 6:
            jumatate = len(cuv) // 2
            subwords.extend([cuv[:jumatate] + "##", "##" + cuv[jumatate:]])
        else:
            subwords.append(cuv)
    return {
        "original": text,
        "tokens_spatiu": tokens_spatiu,
        "tokens_cuvinte": tokens_cuvinte,
        "tokens_subword": subwords,
        "tokens_caractere": tokens_caractere,
    }

def calcul_tf_idf_demo(documente: list[str], cuvant: str) -> list[dict]:
    """Calcul TF-IDF simplificat pentru ilustrare."""
    rezultate = []
    cuvant = cuvant.lower()
    for i, doc in enumerate(documente):
        cuvinte = re.findall(r'\b\w+\b', doc.lower())
        tf = cuvinte.count(cuvant) / len(cuvinte) if cuvinte else 0
        n_docs_cu_cuv = sum(1 for d in documente
                            if cuvant in re.findall(r'\b\w+\b', d.lower()))
        idf = math.log((len(documente) + 1) / (n_docs_cu_cuv + 1)) + 1
        tfidf = tf * idf
        rezultate.append({
            "Document": f"Doc {i+1}",
            "Preview": doc[:50] + "..." if len(doc) > 50 else doc,
            "TF": round(tf, 4),
            "IDF": round(idf, 4),
            "TF-IDF": round(tfidf, 4),
        })
    return rezultate

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Ce este NLP — Procesarea Limbajului Natural?")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**NLP** (Natural Language Processing) = domeniu AI care permite calculatoarelor
sa inteleaga, interpreteze si genereze text uman.

#### Problema fundamentala
Calculatoarele nu inteleg cuvinte — lucreaza cu numere.
NLP rezolva **transformarea textului in numere** (vectori) pe care modelele ML le pot procesa.

#### Pipeline NLP clasic
```
Text brut
  ↓
[Preprocesare] Tokenizare, lowercase, eliminare stopwords
  ↓
[Reprezentare] Bag-of-Words / TF-IDF / Word2Vec / BERT embeddings
  ↓
[Model] Clasificare / Regresie / Generare / Extractie
  ↓
Rezultat: eticheta, raspuns, rezumat, entitati
```

#### Aplicatii NLP la APIA si agricultura
| Task NLP | Aplicatie practica APIA |
|---|---|
| **Clasificare text** | Categorizeaza automat tipul cererii PAC |
| **Analiza sentiment** | Evalueaza reclamatiile fermierilor |
| **Named Entity Recognition** | Extrage nume parcele, judete, culturi din documente |
| **Rezumare** | Condenseaza rapoarte de control lungi |
| **Traducere** | Documente PAC in limba romana ↔ engleza |
| **Clasificare documente** | Separa cereri valide de cele incomplete |
""")

    with col2:
        st.markdown("""
<div style='background:#f3e5f5; border-radius:10px; padding:14px;
     border-top:4px solid #8e44ad;'>
<div style='font-weight:700; color:#8e44ad; font-size:14px;'>
    Evolutia NLP — de la reguli la Transformers
</div>
<div style='font-size:11px; color:#444; margin-top:10px; line-height:1.7;'>
<b>1950-1980:</b> Reguli manuale (if/else pe text)<br>
<b>1990-2000:</b> Statistica — HMM, n-grams<br>
<b>2000-2013:</b> Machine Learning — SVM pe text<br>
<b>2013:</b> Word2Vec — primul embedding neural<br>
<b>2015:</b> LSTM/GRU — retele recurente<br>
<b>2017:</b> <b style='color:#8e44ad;'>Transformer</b> ("Attention is all you need")<br>
<b>2018:</b> BERT (Google) — revolutie NLP<br>
<b>2019:</b> GPT-2 → GPT-3 → LLM-uri<br>
<b>2022+:</b> ChatGPT, Claude, Gemini
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f5e9; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#27ae60; font-size:14px;'>
    Hugging Face
</div>
<div style='font-size:11px; color:#444; margin-top:8px; line-height:1.6;'>
Platforma open-source cu <b>500.000+ modele</b> pre-antrenate,
gratuite, descarcabile local.<br><br>
<code>pip install transformers torch</code><br><br>
O singura linie de cod pentru orice task NLP:
<code>pipeline("sentiment-analysis")</code>
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.subheader("Cum functioneaza un Transformer?")

    st.markdown("""
Arhitectura **Transformer** (Vaswani et al., 2017) are doua componente principale:

```
INPUT TEXT: "Parcela GJ-045 are NDVI scazut"
     ↓
[ENCODER] — intelege textul
  • Tokenizare: ["Par", "##cela", "GJ", "-", "045", "are", "NDVI", "sc", "##azut"]
  • Embeddings: fiecare token → vector de 768 numere
  • Self-Attention: fiecare token "priveste" toti ceilalti
  • Feed-Forward: transformare nonlineara
     ↓
[REPREZENTARE CONTEXTUALA] — vector de 768 dimensiuni per token
     ↓
[CLASIFICATOR / DECODOR] — produce rezultatul final
     ↓
OUTPUT: "NEGATIV" (0.94 incredere)
```

**Self-Attention** = mecanismul cheie: modelul invata ce cuvinte
sunt importante unul pentru altul in context.

> *"NDVI scazut"* → modelul invata ca "scazut" modifica "NDVI"
> si impreuna indica o problema — nu o stare pozitiva.
""")

    st.info("""
**Instalare Hugging Face (toate paginile M3):**
```
pip install transformers torch sentencepiece
```
Modelele se descarca automat din cloud la prima rulare (~200-500 MB per model).
Dupa descarcare — functioneaza complet offline.
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TOKENIZARE & VOCABULAR
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Tokenizare — cum transforma NLP textul in unitati procesabile")

    st.markdown("""
**Tokenizarea** = primul pas in orice pipeline NLP.
Imparte textul in **tokeni** (unitati minime).
""")

    text_tokenizare = st.text_area(
        "Introdu un text pentru tokenizare:",
        value="Parcela agricola din judetul Gorj are o suprafata de 12.45 ha cultivata cu grau de toamna.",
        height=80,
        key="tok_text"
    )

    if text_tokenizare:
        rez_tok = tokenizeaza_simplu(text_tokenizare)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Tokeni pe spatiu:**")
            st.metric("Numar tokeni", len(rez_tok["tokens_spatiu"]))
            for t in rez_tok["tokens_spatiu"]:
                st.markdown(f"""
<span style='display:inline-block; background:#e8eaf6; padding:2px 8px;
margin:2px; border-radius:4px; font-size:12px; color:#3949ab;'>{t}</span>""",
unsafe_allow_html=True)

        with col2:
            st.markdown("**Tokeni cuvinte (regex):**")
            st.metric("Numar tokeni", len(rez_tok["tokens_cuvinte"]))
            for t in rez_tok["tokens_cuvinte"]:
                st.markdown(f"""
<span style='display:inline-block; background:#e8f5e9; padding:2px 8px;
margin:2px; border-radius:4px; font-size:12px; color:#2e7d32;'>{t}</span>""",
unsafe_allow_html=True)

        with col3:
            st.markdown("**Subword tokenizare (BERT-style):**")
            st.metric("Numar tokeni", len(rez_tok["tokens_subword"]))
            for t in rez_tok["tokens_subword"]:
                culoare = "#f3e5f5" if "##" in t else "#fce4ec"
                text_c  = "#6a1b9a" if "##" in t else "#880e4f"
                st.markdown(f"""
<span style='display:inline-block; background:{culoare}; padding:2px 8px;
margin:2px; border-radius:4px; font-size:12px; color:{text_c};'>{t}</span>""",
unsafe_allow_html=True)

        st.info("""
**De ce subword?** Tokenizarea BERT (WordPiece) imparte cuvintele rare in parti mai mici.
Prefixul `##` = continua cuvantul anterior.
Asta permite modelului sa inteleaga cuvinte noi (ex: "GORJ_BF_00234") fara sa le fi vazut la antrenare.
""")

    st.divider()
    st.subheader("TF-IDF — importanta cuvintelor in documente")

    st.markdown("""
**TF-IDF** (Term Frequency — Inverse Document Frequency) masoara cat de important
este un cuvant *intr-un document specific* comparativ cu *toata colectia*.
""")

    documente_demo = [
        "Parcela GJ-045 are suprafata de 12 ha cultivata cu grau de toamna in judetul Gorj.",
        "NDVI-ul masurat in parcela din Gorj indica stress hidric sever in zona centrala.",
        "Cererea PAC 2024 pentru ferma din Gorj a fost aprobata cu suprafata de 45 ha.",
        "Cultura de floarea-soarelui din parcela IF-012 are productie estimata la 2.8 tone per ha.",
        "Inspectia APIA a constatat neconformitati privind suprafata declarata in cerere.",
    ]

    col_a, col_b = st.columns([2, 1])
    with col_a:
        cuvant_cautat = st.text_input("Cauta importanta cuvantului:", value="parcela", key="tfidf_cuv")
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        calculeaza = st.button("Calculeaza TF-IDF", key="btn_tfidf")

    if calculeaza and cuvant_cautat:
        rezultate_tfidf = calcul_tf_idf_demo(documente_demo, cuvant_cautat)
        import pandas as pd
        df_tfidf = pd.DataFrame(rezultate_tfidf)
        st.dataframe(df_tfidf, use_container_width=True, hide_index=True)

        if PLOTLY_OK:
            fig = go.Figure(go.Bar(
                x=[r["Document"] for r in rezultate_tfidf],
                y=[r["TF-IDF"] for r in rezultate_tfidf],
                marker_color="#8e44ad",
                text=[r["Preview"] for r in rezultate_tfidf],
                hovertemplate="%{text}<extra></extra>"
            ))
            fig.update_layout(
                title=f'TF-IDF pentru "{cuvant_cautat}"',
                yaxis_title="Scor TF-IDF",
                height=300,
                margin=dict(t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
**Interpretare:** Un scor TF-IDF ridicat inseamna ca "{cuvant_cautat}" este
*important si specific* acelui document. Scor 0 = cuvantul nu apare in document.
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANALIZA SENTIMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Analiza de Sentiment pe Texte Agricole / APIA")

    st.markdown("""
**Analiza sentiment** = clasificarea unui text ca **pozitiv / negativ / neutru**.
Aplicatie APIA: evaluarea automata a rapoartelor de control, reclamatii, feedback fermieri.
""")

    if not HF_OK:
        st.warning("""
**Mod demo activ** — biblioteca `transformers` nu este instalata.
Analiza se face cu un clasificator bazat pe dictionar de cuvinte cheie.
Pentru model real: `pip install transformers torch`
""")
    else:
        st.success("Hugging Face `transformers` disponibil — se poate folosi model real.")

    # Texte predefinite APIA
    texte_demo = {
        "Raport pozitiv — parcela conforma": (
            "Parcela agricola GJ-045 este in stare buna. Cultura de grau este "
            "completa si conforma cu declaratia. NDVI-ul masurat este normal, "
            "suprafata corecta. Cererea este valida si aprobata."
        ),
        "Raport negativ — neconformitate": (
            "S-a constatat o problema grava: suprafata declarata este incorecta. "
            "Cultura lipseste din zona centrala a parcelei. NDVI indica stress sever. "
            "Cererea a fost respinsa din cauza neconformitatilor identificate."
        ),
        "Raport neutru — control standard": (
            "Inspectia a fost efectuata in data de 15 aprilie 2024. "
            "Ferma se afla in judetul Gorj. Suprafata totala este de 12 ha. "
            "Cultura declarata este grau de toamna. Documentele au fost verificate."
        ),
        "Sesizare fermier — seceta": (
            "Reclamatie: seceta severa a afectat cultura de porumb din parcela IF-089. "
            "Productia este deteriorata, pierderile sunt estimate la 60%. "
            "Solicitam sprijin de urgenta si reevaluarea situatiei."
        ),
    }

    col_left, col_right = st.columns([3, 2])

    with col_left:
        selectie = st.selectbox(
            "Alege un text predefinit sau scrie mai jos:",
            ["(text propriu)"] + list(texte_demo.keys()),
            key="sel_text"
        )

        if selectie == "(text propriu)":
            text_input = st.text_area(
                "Text de analizat:",
                value="Scrie aici textul tau agricol sau APIA...",
                height=120,
                key="text_propriu"
            )
        else:
            text_input = st.text_area(
                "Text selectat (editabil):",
                value=texte_demo[selectie],
                height=120,
                key="text_sel"
            )

        analizeaza = st.button("Analizeaza Sentiment", type="primary",
                               use_container_width=True, key="btn_sent")

    with col_right:
        st.markdown("""
<div style='background:#f3e5f5; border-radius:10px; padding:14px;
     border-top:4px solid #8e44ad;'>
<div style='font-weight:700; color:#8e44ad;'>Cum functioneaza?</div>
<div style='font-size:11px; color:#444; margin-top:8px; line-height:1.6;'>
<b>Model Hugging Face:</b><br>
Text → BERT tokenizer → BERT encoder →
classifier layer → [POZITIV / NEGATIV] + scor incredere<br><br>
<b>Demo (fara transformers):</b><br>
Numara cuvinte pozitive vs negative dintr-un dictionar
predefinit → atribuie eticheta pe baza majoritatii.
</div>
</div>
""", unsafe_allow_html=True)

    if analizeaza and text_input and text_input.strip():
        st.divider()

        if HF_OK:
            with st.spinner("Se incarca modelul Hugging Face (prima rulare ~200MB)..."):
                try:
                    @st.cache_resource(show_spinner=False)
                    def incarca_sentiment_model():
                        return hf_pipeline(
                            "sentiment-analysis",
                            model="nlptown/bert-base-multilingual-uncased-sentiment",
                            truncation=True,
                            max_length=512
                        )
                    classifier = incarca_sentiment_model()
                    rez_hf = classifier(text_input[:512])
                    label_hf = rez_hf[0]["label"]
                    score_hf = rez_hf[0]["score"]
                    # Normalizeaza eticheta (modelul multilingual returneaza stele)
                    if "1" in label_hf or "2" in label_hf:
                        label_norm = "NEGATIV"
                    elif "4" in label_hf or "5" in label_hf:
                        label_norm = "POZITIV"
                    else:
                        label_norm = "NEUTRU"
                    rez = {"label": label_norm, "score": round(score_hf, 3),
                           "pozitive": 0, "negative": 0,
                           "cuvinte_cheie_pos": [], "cuvinte_cheie_neg": []}
                    sursa = "Hugging Face (BERT multilingual)"
                except Exception as e:
                    st.warning(f"Model HF indisponibil ({e}), folosesc demo.")
                    rez = sentiment_demo(text_input)
                    sursa = "Demo (dictionar)"
        else:
            rez = sentiment_demo(text_input)
            sursa = "Demo (dictionar cuvinte cheie)"

        # Afisare rezultat
        culoare_label = {"POZITIV": "#27ae60", "NEGATIV": "#e74c3c", "NEUTRU": "#f39c12"}
        emoji_label   = {"POZITIV": "✅", "NEGATIV": "⚠️", "NEUTRU": "➡️"}
        culoare = culoare_label.get(rez["label"], "#888")
        emoji   = emoji_label.get(rez["label"], "•")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
<div style='background:{culoare}22; border:2px solid {culoare};
     border-radius:12px; padding:16px; text-align:center;'>
<div style='font-size:36px;'>{emoji}</div>
<div style='font-size:22px; font-weight:800; color:{culoare};'>{rez["label"]}</div>
<div style='font-size:12px; color:#555; margin-top:4px;'>Sentiment detectat</div>
</div>""", unsafe_allow_html=True)

        with col2:
            st.metric("Incredere model", f"{rez['score']*100:.1f}%")
            st.metric("Sursa analiza", sursa)

        with col3:
            st.metric("Cuvinte pozitive", rez.get("pozitive", "—"))
            st.metric("Cuvinte negative", rez.get("negative", "—"))

        if rez.get("cuvinte_cheie_pos"):
            st.markdown("**Cuvinte pozitive detectate:**")
            for c in set(rez["cuvinte_cheie_pos"]):
                st.markdown(f"""<span style='background:#d5f5e3; padding:2px 8px;
margin:2px; border-radius:4px; font-size:12px; color:#1e8449;'>{c}</span>""",
unsafe_allow_html=True)

        if rez.get("cuvinte_cheie_neg"):
            st.markdown("**Cuvinte negative detectate:**")
            for c in set(rez["cuvinte_cheie_neg"]):
                st.markdown(f"""<span style='background:#fadbd8; padding:2px 8px;
margin:2px; border-radius:4px; font-size:12px; color:#922b21;'>{c}</span>""",
unsafe_allow_html=True)

        # Grafic bara incredere
        if PLOTLY_OK:
            fig_sent = go.Figure(go.Bar(
                x=["Incredere sentiment"],
                y=[rez["score"] * 100],
                marker_color=culoare,
                text=[f"{rez['score']*100:.1f}%"],
                textposition="outside"
            ))
            fig_sent.update_layout(
                height=200,
                yaxis=dict(range=[0, 110], title="Incredere (%)"),
                showlegend=False,
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig_sent, use_container_width=True)

    st.divider()
    st.markdown("### Analiza multipla — toate textele demo")

    if st.button("Analizeaza toate textele predefinite", key="btn_all"):
        rezultate_multiple = []
        for titlu, text in texte_demo.items():
            rez = sentiment_demo(text)
            rezultate_multiple.append({
                "Text": titlu,
                "Sentiment": rez["label"],
                "Incredere": f"{rez['score']*100:.1f}%",
                "Cuvinte+": rez["pozitive"],
                "Cuvinte-": rez["negative"],
            })

        import pandas as pd
        df_mult = pd.DataFrame(rezultate_multiple)

        def coloreaza_sentiment(val):
            if val == "POZITIV":
                return "background-color:#d5f5e3; color:#1e8449"
            elif val == "NEGATIV":
                return "background-color:#fadbd8; color:#922b21"
            return "background-color:#fef9e7; color:#b7950b"

        st.dataframe(
            df_mult.style.applymap(coloreaza_sentiment, subset=["Sentiment"]),
            use_container_width=True,
            hide_index=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Ce am invatat azi — Ziua 13")

    concepte = [
        ("NLP", "Procesarea Limbajului Natural — AI care intelege textul uman"),
        ("Tokenizare", "Impartirea textului in unitati minime (tokeni / subwords)"),
        ("Embeddings", "Reprezentarea cuvintelor ca vectori numerici in spatiu multidimensional"),
        ("TF-IDF", "Masura importantei unui cuvant intr-un document relativ la colectie"),
        ("Transformer", "Arhitectura revolutionara (2017) bazata pe Self-Attention"),
        ("BERT", "Model pre-antrenat Google — baza majoritatii modelelor NLP moderne"),
        ("Hugging Face", "Platforma 500k+ modele gratuite, pip install transformers"),
        ("pipeline()", "API simplu HF: o linie de cod pentru orice task NLP"),
        ("Analiza sentiment", "Clasificare text: POZITIV / NEGATIV / NEUTRU + scor incredere"),
    ]

    for concept, descriere in concepte:
        st.markdown(f"""
<div style='display:flex; gap:12px; padding:8px 14px; margin:4px 0;
     background:#f8f9fa; border-radius:8px; font-size:13px;
     border-left:4px solid #8e44ad;'>
<b style='color:#8e44ad; min-width:140px;'>{concept}</b>
<span style='color:#333;'>{descriere}</span>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Cod minimal Ziua 13")

    st.code("""
# Instalare
# pip install transformers torch

from transformers import pipeline

# Analiza sentiment (descarca model automat ~200MB)
classifier = pipeline("sentiment-analysis",
                       model="nlptown/bert-base-multilingual-uncased-sentiment")

texte = [
    "Parcela este in stare buna, cultura conforma.",
    "Neconformitate grava: suprafata declarata incorecta.",
]

for text in texte:
    rez = classifier(text)
    print(f"{text[:40]}... → {rez[0]['label']} ({rez[0]['score']:.2f})")
""", language="python")

    st.markdown("### Urmatoarea zi — Ziua 14")
    st.info("""
**Ziua 14 — Clasificare Texte Agricole**

Vom folosi Hugging Face pentru a **clasifica automat** tipul unui document APIA:
- Cerere PAC, Raport control, Reclamatie, Notificare, Decizie
- Zero-shot classification (fara antrenare suplimentara)
- Aplicatie practica: sortare automata documente APIA
""")

    st.markdown("""
---
*Referinta: "Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"
— Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, Universitatea din Petrosani, 2024*
""")
