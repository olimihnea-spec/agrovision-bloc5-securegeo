"""
Ziua 16 — Rezumare Automata Documente cu NLP
Modul 3: NLP Aplicat — Hugging Face summarization + extractiv demo
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import re
import math
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
    page_title="Ziua 16 — Rezumare Documente",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>📋</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 16</div>
    <div style='font-size:11px; color:#666;'>Rezumare Automata Documente NLP</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 3 — NLP Aplicat")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 16 / 30 zile")
st.sidebar.progress(16 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 16:**
- Rezumare extractiva vs abstractiva
- TF-IDF pentru selectie fraze cheie
- Hugging Face `summarization` pipeline
- Rata de compresie text
- Cuvinte cheie (keywords)
- Aplicatii: rapoarte APIA, documente PAC
""")
st.sidebar.divider()
if HF_OK:
    st.sidebar.success("transformers instalat")
else:
    st.sidebar.warning("transformers absent — rezumare extractiva activa")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>📋</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 16 — Rezumare Automata Documente
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 3 — NLP Aplicat &nbsp;|&nbsp;
            Rezumare extractiva TF-IDF + Hugging Face abstractiva — rapoarte APIA, documente PAC
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
# DOCUMENTE DEMO
# ══════════════════════════════════════════════════════════════════════════════

DOCUMENTE_DEMO = {
    "Raport control teren (lung)": """
In data de 14 aprilie 2024, echipa de inspectie APIA formata din inspectorul principal
Gam. O.M. si inspectorul de teren Pop. I.A. a efectuat un control pe teren la ferma
inregistrata cu codul GJ-2024-001847, apartinand fermierului Ionescu Gheorghe, cu
domiciliul in localitatea Bumbesti-Jiu, judetul Gorj.

Obiectul controlului a constat in verificarea conformitatii suprafetelor declarate
in cererea unica de plata pentru campania 2024 cu situatia faptica din teren.
Fermierul a declarat o suprafata totala de 45.30 hectare, din care 28.50 ha
cultivate cu grau de toamna si 16.80 ha cultivate cu floarea-soarelui.

In cadrul controlului, inspectorii au utilizat echipamentul GPS de precizie de tip
Trimble R8s pentru masurarea suprafetelor, precum si o drona DJI Phantom 4
Multispectral pentru achizitia imaginilor multispectrale. Imaginile achizitionate
la altitudinea de 100 de metri au permis calculul indicelui NDVI pentru fiecare
parcela in parte.

Masuratorile GPS au relevat urmatoarele: parcela P1 (grau de toamna) are o
suprafata efectiva de 27.85 ha, parcela P2 (floarea-soarelui) are o suprafata
efectiva de 15.90 ha, rezultand o suprafata totala efectiva de 43.75 ha.
Diferenta fata de suprafata declarata este de 1.55 ha, reprezentand 3.42%.

Analiza imaginilor multispectrale a indicat un NDVI mediu de 0.62 pentru cultura
de grau, valoare considerata normala pentru aceasta etapa de vegetatie. In schimb,
cultura de floarea-soarelui prezinta un NDVI mediu de 0.38, cu zone de stress
hidric in proportie de 12% din suprafata, identificate cu precadere in zona nordica
a parcelei P2.

In conformitate cu prevederile Regulamentului UE 2021/2116 si ale normelor de
aplicare, diferenta de suprafata de 3.42% se incadreaza sub pragul de toleranta
de 5%, motiv pentru care nu se aplica reduceri la plata pentru neconformitati
de suprafata. Cu toate acestea, situatia de stress hidric identificata in parcela
P2 va fi monitorizata printr-un control ulterior programat pentru luna iunie 2024.

Prezentul raport a fost redactat in doua exemplare, dintre care unul a fost
inmanat fermierului Ionescu Gheorghe la data controlului, iar cel de-al doilea
a fost depus la arhiva Centrului Judetean Gorj al APIA.
""",

    "Cerere PAC 2024": """
Subsemnatul Popescu Constantin, cetatean roman, identificat cu CNP 1650312180045,
cu domiciliul in comuna Turceni, judetul Gorj, in calitate de fermier activ
inregistrat la APIA Centrul Judetean Gorj cu codul de exploatatie RO123456789,
prin prezenta cerere unica de plata formulez urmatoarele solicitari pentru
campania agricola 2024.

Solicit acordarea platilor directe pentru o suprafata totala de 38.75 hectare,
repartizata pe urmatoarele parcele: parcela T45/A cu suprafata de 12.40 ha
cultivata cu porumb, parcela T46/B cu suprafata de 9.80 ha cultivata cu grau
de toamna, parcela T47/C cu suprafata de 8.20 ha cultivata cu lucerna pentru
furaj, parcela T48/D cu suprafata de 5.60 ha cultivata cu floarea-soarelui
si parcela T49/E cu suprafata de 2.75 ha reprezentand fanete naturale.

Declar pe propria raspundere ca informatiile furnizate sunt reale si complete,
ca am dreptul legal de a folosi suprafetele declarate in baza contractelor de
arenda atasate prezentei cereri si ca respect conditiile de eco-conditionalitate
prevazute de legislatia europeana si nationala in vigoare.

Atasez urmatoarele documente: copie dupa actul de identitate, extras de carte
funciara pentru terenurile proprietate personala, contracte de arenda pentru
terenurile luate in arenda, plan de parcele la scara 1:5000 vizat de OCPI Gorj
si declaratia privind suprafetele eligibile.

Solicit de asemenea includerea in schema pentru tinerii fermieri si in masura
de agromediu M10 privind pajistile cu inalta valoare naturala pentru parcela T49/E.
""",

    "Raport analiza NDVI drone": """
Prezentul raport sintetizeaza rezultatele analizei imaginilor multispectrale
achizitionate cu sistemul UAV DJI Phantom 4 Multispectral in data de 10 aprilie
2024 pentru zona agricola Gorj-Nord, cu o suprafata totala acoperita de 450 de
hectare, apartinand unui numar de 23 de fermieri.

Sistemul a zburat la altitudinea de 100 de metri, cu o suprapunere frontala de
80% si laterala de 70%, rezultand o rezolutie spatiala de 5 cm per pixel.
Procesarea fotogrametrica a fost realizata cu software-ul Agisoft Metashape,
obtinandu-se ortofotoplanuri si modele digitale ale suprafetei cu o precizie
de plus-minus 3 centimetri.

Analiza indicelui NDVI a relevat urmatoarea distributie a sanatatii vegetatiei:
suprafete cu NDVI peste 0.70 (vegetatie densa si sanatoasa) reprezinta 52% din
totalul suprafetei analizate, suprafete cu NDVI intre 0.40 si 0.70 (vegetatie
moderata, in dezvoltare normala) reprezinta 35%, suprafete cu NDVI intre 0.10
si 0.40 (vegetatie rara sau sub stress) reprezinta 10% si suprafete cu NDVI
sub 0.10 (fara vegetatie sau vegetatie extrem de rara) reprezinta 3%.

Au fost identificate 8 zone cu anomalii NDVI semnificative, dintre care 3 prezinta
caracteristici de stress hidric sever, 3 prezinta semne de atac fitosanitar si
2 prezinta suprafete neconforme cu cultura declarata. Aceste zone au fost marcate
pe harta digitala si transmise echipei de control teren pentru verificare fizica.

Concluzii: cultura de grau de toamna se afla in stadiu fenologic normal pentru
perioada analizata, cu o medie NDVI de 0.65 la nivel de zona. Riscul cel mai
ridicat il reprezinta seceta din sudul zonei, unde NDVI mediu coboara la 0.31.
Se recomanda prioritizarea controlului la fermele cu parcele in zonele de anomalie
identificate pentru a verifica conformitatea cu declaratiile PAC 2024.
""",
}

STOPWORDS_RO = {
    "si", "sau", "dar", "ca", "pe", "cu", "la", "in", "din", "de", "a", "al",
    "ale", "ai", "un", "o", "unei", "unui", "este", "sunt", "fi", "fost", "sa",
    "se", "au", "au", "nu", "mai", "prin", "pentru", "care", "ce", "cel", "cea",
    "cei", "cele", "acest", "aceasta", "acestui", "acestei", "acestia", "acestea",
    "astfel", "intre", "spre", "dupa", "inainte", "pana", "dintre", "conform",
    "privind", "precum", "cat", "iar", "deci", "fie", "tot", "toata", "toti",
    "toate", "fiecare", "oricare", "orice", "atat", "atata", "acea", "acel",
    "dintre", "insa", "desi", "decat", "chiar", "mai", "mult", "putini",
}

# ══════════════════════════════════════════════════════════════════════════════
# ALGORITM REZUMARE EXTRACTIVA (TF-IDF pe fraze)
# ══════════════════════════════════════════════════════════════════════════════

def tokenizeaza_fraze(text: str) -> list[str]:
    """Imparte textul in fraze la punct, semn de intrebare, exclamare."""
    fraze = re.split(r'(?<=[.!?])\s+', text.strip())
    return [f.strip() for f in fraze if len(f.strip()) > 20]


def tokenizeaza_cuvinte(text: str) -> list[str]:
    """Tokenizare cuvinte, elimina stopwords si cuvinte scurte."""
    cuvinte = re.findall(r'\b[a-zA-ZăâîșțĂÂÎȘȚ]{3,}\b', text.lower())
    return [c for c in cuvinte if c not in STOPWORDS_RO]


def calcul_tfidf_fraze(fraze: list[str]) -> dict[str, float]:
    """
    Calculeaza scorul TF-IDF pentru fiecare cuvant din corpus de fraze.
    Returneaza dict {cuvant: scor_tfidf}.
    """
    N = len(fraze)
    tf_per_fraza = []
    df = {}

    for fraza in fraze:
        cuvinte = tokenizeaza_cuvinte(fraza)
        tf = {}
        for cuv in cuvinte:
            tf[cuv] = tf.get(cuv, 0) + 1
        if cuvinte:
            for cuv in tf:
                tf[cuv] /= len(cuvinte)
        tf_per_fraza.append(tf)
        for cuv in set(cuvinte):
            df[cuv] = df.get(cuv, 0) + 1

    # Scor global per cuvant: suma TF * IDF peste toate frazele
    scor_cuv = {}
    for cuv, freq_doc in df.items():
        idf = math.log((N + 1) / (freq_doc + 1)) + 1
        for tf in tf_per_fraza:
            if cuv in tf:
                scor_cuv[cuv] = scor_cuv.get(cuv, 0) + tf[cuv] * idf

    return scor_cuv


def scor_fraza(fraza: str, scor_cuv: dict[str, float]) -> float:
    """Scorul unei fraze = suma scorurilor TF-IDF ale cuvintelor sale."""
    cuvinte = tokenizeaza_cuvinte(fraza)
    if not cuvinte:
        return 0.0
    return sum(scor_cuv.get(c, 0) for c in cuvinte) / len(cuvinte)


def rezumare_extractiva(text: str, n_fraze: int = 3) -> dict:
    """
    Rezumare extractiva bazata pe TF-IDF:
    selecteaza cele mai importante n_fraze din text,
    pastrand ordinea originala.
    """
    fraze = tokenizeaza_fraze(text)
    if len(fraze) <= n_fraze:
        return {
            "rezumat": text.strip(),
            "fraze_selectate": list(range(len(fraze))),
            "scoruri": {},
            "total_fraze": len(fraze),
            "cuvinte_originale": len(tokenizeaza_cuvinte(text)),
            "cuvinte_rezumat": len(tokenizeaza_cuvinte(text)),
        }

    scor_cuv = calcul_tfidf_fraze(fraze)
    scoruri_fraze = [(i, fraza, scor_fraza(fraza, scor_cuv))
                     for i, fraza in enumerate(fraze)]

    # Selecteaza top n_fraze dupa scor
    top = sorted(scoruri_fraze, key=lambda x: x[2], reverse=True)[:n_fraze]
    top_idx = sorted([t[0] for t in top])  # pastreaza ordinea originala

    rezumat = " ".join(fraze[i] for i in top_idx)
    cuv_orig = len(tokenizeaza_cuvinte(text))
    cuv_rez  = len(tokenizeaza_cuvinte(rezumat))

    return {
        "rezumat":           rezumat,
        "fraze_selectate":   top_idx,
        "scoruri":           {i: s for i, _, s in scoruri_fraze},
        "total_fraze":       len(fraze),
        "fraze_all":         fraze,
        "cuvinte_originale": cuv_orig,
        "cuvinte_rezumat":   cuv_rez,
        "rata_compresie":    round((1 - cuv_rez / cuv_orig) * 100, 1) if cuv_orig else 0,
    }


def extrage_cuvinte_cheie(text: str, top_n: int = 10) -> list[tuple[str, float]]:
    """Extrage cuvintele cheie dintr-un text pe baza scorului TF-IDF."""
    fraze = tokenizeaza_fraze(text)
    scor_cuv = calcul_tfidf_fraze(fraze)
    sortate = sorted(scor_cuv.items(), key=lambda x: x[1], reverse=True)
    return sortate[:top_n]


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠 Teorie",
    "✂️ Rezumare Extractiva",
    "🤖 Rezumare Abstractiva (HF)",
    "🔑 Cuvinte Cheie",
    "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Rezumarea automata a documentelor")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**Rezumarea automata** = condensarea unui text lung intr-un rezumat scurt care
pastreaza informatiile esentiale.

#### Doua abordari fundamentale

**1. Rezumare Extractiva**
Selecteaza si combina fraze existente din textul original.
```
Text original (20 fraze)
  ↓
Scor TF-IDF per fraza
  ↓
Selecteaza top 3 fraze
  ↓
Rezumat (3 fraze din original)
```
Avantaje: simplu, rapid, nu necesita model ML, texte coerente
Dezavantaje: rezumatul poate fi disconex, nu reformuleaza

---

**2. Rezumare Abstractiva**
Genereaza text nou, reformuleaza — ca un om care citeste si rescrie.
```
Text original
  ↓
Encoder (BERT/T5) — intelege textul
  ↓
Decoder (GPT/T5) — genereaza rezumat nou
  ↓
Rezumat (formulare noua)
```
Avantaje: rezumat natural, coerent, poate scurta drastic
Dezavantaje: necesita model mare (~500MB-1GB), poate halucina

#### Aplicatii APIA
| Document | Utilitate rezumare |
|---|---|
| Raport control (3 pagini) | Rezumat 1 paragraf pentru director |
| Cerere PAC (complex) | Extras date cheie: suprafata, culturi, parcele |
| Raport NDVI (tehnic) | Concluzii accesibile pentru inspector non-tehnic |
| Contestatie fermier | Puncte principale ale contestatiei |
""")

    with col2:
        st.markdown("""
<div style='background:#f3e5f5; border-radius:10px; padding:14px;
     border-top:4px solid #8e44ad;'>
<div style='font-weight:700; color:#8e44ad;'>Algoritm TF-IDF pentru fraze</div>
<div style='font-size:11px; color:#333; margin-top:10px; line-height:1.8;'>
<b>Pas 1.</b> Imparte textul in fraze<br>
<b>Pas 2.</b> Calculeaza TF-IDF per cuvant<br>
<b>Pas 3.</b> Scorul frazei = media TF-IDF a cuvintelor sale<br>
<b>Pas 4.</b> Sorteaza frazele dupa scor<br>
<b>Pas 5.</b> Selecteaza top N, pastreaza ordinea<br><br>
<b>Intuitie:</b> frazele cu multi termeni importanti
(rari in corpus dar frecventi in fraza) primesc scor mare.
</div></div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f5e9; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Rata de compresie</div>
<div style='font-size:12px; color:#333; margin-top:8px; line-height:1.7;'>
<b>Rata compresie</b> = cat % din text eliminam:<br>
<code>(1 - cuvinte_rezumat / cuvinte_original) × 100</code><br><br>
Tipic:<br>
• Extractiva: 60-80% compresie<br>
• Abstractiva: 70-90% compresie<br>
• Rezumat executiv: 90-95% compresie
</div></div>
""", unsafe_allow_html=True)

        st.info("**Instalare HF pentru rezumare abstractiva:**\n```\npip install transformers torch sentencepiece\n```")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REZUMARE EXTRACTIVA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Rezumare extractiva cu TF-IDF — selectie fraze importante")

    col_l, col_r = st.columns([1, 2])

    with col_l:
        doc_ales = st.selectbox(
            "Alege document:",
            ["(text propriu)"] + list(DOCUMENTE_DEMO.keys()),
            key="doc_ext"
        )
        if doc_ales == "(text propriu)":
            text_ext = st.text_area(
                "Introdu textul:", value="", height=200,
                placeholder="Introdu un document APIA lung...",
                key="text_ext_custom"
            )
        else:
            text_ext = st.text_area(
                "Document selectat (editabil):",
                value=DOCUMENTE_DEMO[doc_ales].strip(),
                height=200, key="text_ext_sel"
            )

        n_fraze = st.slider("Numar fraze in rezumat:", 1, 8, 3, key="n_fraze")
        ruleaza_ext = st.button("Genereaza Rezumat Extractiv",
                                 type="primary", use_container_width=True,
                                 key="btn_ext")

    with col_r:
        if ruleaza_ext and text_ext and text_ext.strip():
            with st.spinner("Calculez scorurile TF-IDF..."):
                rez = rezumare_extractiva(text_ext, n_fraze)

            # Metrici
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Cuvinte original", rez["cuvinte_originale"])
            with c2:
                st.metric("Cuvinte rezumat", rez["cuvinte_rezumat"])
            with c3:
                st.metric("Rata compresie", f"{rez['rata_compresie']}%")

            st.markdown("**Rezumat generat:**")
            st.markdown(f"""
<div style='background:#f3e5f5; border-left:4px solid #8e44ad;
     padding:14px 16px; border-radius:0 8px 8px 0; font-size:14px;
     line-height:1.7; color:#333;'>
{rez["rezumat"]}
</div>""", unsafe_allow_html=True)

            # Vizualizare fraze cu scoruri
            st.markdown("**Toate frazele cu scoruri TF-IDF:**")
            fraze_all = rez.get("fraze_all", tokenizeaza_fraze(text_ext))
            for i, fraza in enumerate(fraze_all):
                selectata = i in rez["fraze_selectate"]
                scor_val  = rez["scoruri"].get(i, 0)
                culoare   = "#f3e5f5" if selectata else "#f8f9fa"
                border    = "#8e44ad" if selectata else "#ddd"
                badge     = f"<b style='color:#8e44ad;'> SELECTATA (scor: {scor_val:.3f})</b>" if selectata else f"<span style='color:#aaa;font-size:11px;'> scor: {scor_val:.3f}</span>"
                st.markdown(f"""
<div style='background:{culoare}; border-left:4px solid {border};
     padding:6px 12px; margin:3px 0; border-radius:0 6px 6px 0; font-size:12px;'>
<b style='color:#555;'>F{i+1}</b>{badge}<br>
<span style='color:#333;'>{fraza[:120]}{"..." if len(fraza)>120 else ""}</span>
</div>""", unsafe_allow_html=True)

            # Download
            st.download_button(
                "Descarca rezumat TXT",
                data=rez["rezumat"].encode("utf-8"),
                file_name=f"rezumat_extractiv_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

        elif ruleaza_ext:
            st.warning("Introdu un text pentru rezumare.")
        else:
            st.info("Alege un document si apasa **Genereaza Rezumat Extractiv**.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REZUMARE ABSTRACTIVA (HF)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Rezumare abstractiva cu Hugging Face (T5 / BART)")

    if not HF_OK:
        st.warning("""
**`transformers` nu este instalat.**

Rezumarea abstractiva necesita un model neural pre-antrenat.
Instaleaza cu:
```
pip install transformers torch sentencepiece
```
Dupa instalare, reporneste aplicatia.
""")

    col_l2, col_r2 = st.columns([1, 2])

    with col_l2:
        doc_hf = st.selectbox(
            "Alege document:",
            ["(text propriu)"] + list(DOCUMENTE_DEMO.keys()),
            key="doc_hf"
        )
        if doc_hf == "(text propriu)":
            text_hf = st.text_area(
                "Introdu textul:", value="", height=180,
                key="text_hf_custom"
            )
        else:
            text_hf = st.text_area(
                "Document:",
                value=DOCUMENTE_DEMO[doc_hf].strip(),
                height=180, key="text_hf_sel"
            )

        st.markdown("**Parametri model:**")
        max_len  = st.slider("Lungime maxima rezumat (tokeni)", 30, 200, 80,  key="max_len")
        min_len  = st.slider("Lungime minima rezumat (tokeni)", 10, 100, 30,  key="min_len")

        ruleaza_hf = st.button(
            "Genereaza Rezumat Abstractiv",
            type="primary",
            use_container_width=True,
            key="btn_hf",
            disabled=(not HF_OK)
        )

    with col_r2:
        st.markdown("""
<div style='background:#e8f5e9; border-radius:10px; padding:14px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Model recomandat</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.7;'>
<code>facebook/bart-large-cnn</code><br>
Antrenat pe CNN/DailyMail — excelent pentru documente.<br>
Dimensiune: ~1.6GB. Prima rulare descarca automat.<br><br>
<b>Alternativa mai mica:</b><br>
<code>sshleifer/distilbart-cnn-12-6</code><br>
~700MB, viteza dubla, calitate similara.<br><br>
<b>Nota:</b> Modelele sunt antrenate pe text englezesc.
Pentru romana optima, traduce mai intai sau foloseste
rezumarea extractiva de la tab-ul anterior.
</div></div>
""", unsafe_allow_html=True)

        if ruleaza_hf and HF_OK and text_hf and text_hf.strip():
            with st.spinner("Se incarca modelul BART (~700MB prima rulare)..."):
                try:
                    @st.cache_resource(show_spinner=False)
                    def incarca_summarizer():
                        return hf_pipeline(
                            "summarization",
                            model="sshleifer/distilbart-cnn-12-6",
                            truncation=True
                        )
                    summarizer = incarca_summarizer()
                    # Truncheaza inputul la 1024 tokeni (limita BART)
                    text_trunc = text_hf[:2000]
                    rez_hf = summarizer(
                        text_trunc,
                        max_length=max_len,
                        min_length=min_len,
                        do_sample=False
                    )
                    rezumat_hf = rez_hf[0]["summary_text"]
                    cuv_orig  = len(text_hf.split())
                    cuv_rez   = len(rezumat_hf.split())
                    compresie = round((1 - cuv_rez / cuv_orig) * 100, 1)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Cuvinte original", cuv_orig)
                    with c2:
                        st.metric("Cuvinte rezumat", cuv_rez)
                    with c3:
                        st.metric("Compresie", f"{compresie}%")

                    st.markdown("**Rezumat abstractiv generat:**")
                    st.markdown(f"""
<div style='background:#e8f5e9; border-left:4px solid #27ae60;
     padding:14px 16px; border-radius:0 8px 8px 0; font-size:14px;
     line-height:1.7; color:#333;'>
{rezumat_hf}
</div>""", unsafe_allow_html=True)

                    st.download_button(
                        "Descarca rezumat abstractiv",
                        data=rezumat_hf.encode("utf-8"),
                        file_name="rezumat_abstractiv.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Eroare model: {e}")

        elif not HF_OK:
            st.info("Instaleaza `transformers torch` pentru a activa rezumarea abstractiva.")
        elif ruleaza_hf:
            st.warning("Introdu un text.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CUVINTE CHEIE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Extragere cuvinte cheie (keyword extraction)")

    st.markdown("""
**Cuvintele cheie** = termenii cei mai importanti si reprezentativi dintr-un text.
Utile pentru: indexare, cautare, tagging automat, clasificare rapida.
""")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        doc_kw = st.selectbox(
            "Alege document:",
            list(DOCUMENTE_DEMO.keys()),
            key="doc_kw"
        )
        top_n_kw = st.slider("Numar cuvinte cheie:", 5, 20, 10, key="top_n_kw")
        extrage_btn = st.button("Extrage Cuvinte Cheie",
                                 type="primary", use_container_width=True,
                                 key="btn_kw")

    with col_b:
        if extrage_btn:
            text_kw = DOCUMENTE_DEMO[doc_kw]
            keywords = extrage_cuvinte_cheie(text_kw, top_n_kw)

            st.markdown("**Cuvinte cheie extrase (TF-IDF):**")
            max_scor = keywords[0][1] if keywords else 1.0
            for cuv, scor in keywords:
                latime_pct = int((scor / max_scor) * 100)
                st.markdown(f"""
<div style='display:flex; align-items:center; gap:12px; margin:4px 0;'>
<span style='min-width:140px; font-weight:600; color:#8e44ad;'>{cuv}</span>
<div style='flex:1; background:#f0f0f0; border-radius:4px; height:18px; position:relative;'>
  <div style='width:{latime_pct}%; background:#8e44ad; height:100%;
       border-radius:4px;'></div>
</div>
<span style='min-width:50px; font-size:11px; color:#555;'>{scor:.3f}</span>
</div>""", unsafe_allow_html=True)

            # Norul de cuvinte — simulat ca badge-uri proportionale
            st.markdown("**Cloud vizual:**")
            cloud_html = ""
            for cuv, scor in keywords:
                size = int(12 + (scor / max_scor) * 16)
                opacity = 0.5 + (scor / max_scor) * 0.5
                cloud_html += (
                    f"<span style='font-size:{size}px; opacity:{opacity:.2f}; "
                    f"color:#6c3483; margin:4px 8px; display:inline-block; "
                    f"font-weight:600;'>{cuv}</span>"
                )
            st.markdown(f"""
<div style='background:#f9f0ff; border-radius:10px; padding:16px;
     text-align:center; line-height:2.2;'>{cloud_html}</div>
""", unsafe_allow_html=True)

        else:
            st.info("Alege un document si apasa **Extrage Cuvinte Cheie**.")

    st.divider()
    st.markdown("### Comparatie cuvinte cheie — toate documentele")

    if st.button("Compara cuvinte cheie intre documente", key="btn_cmp"):
        import pandas as pd
        date_cmp = {}
        for titlu, text in DOCUMENTE_DEMO.items():
            kws = extrage_cuvinte_cheie(text, 8)
            date_cmp[titlu[:30]] = [k for k, _ in kws]

        # Tabel comparativ
        max_len_kw = max(len(v) for v in date_cmp.values())
        rows = []
        for i in range(max_len_kw):
            row = {"#": i + 1}
            for titlu, kws in date_cmp.items():
                row[titlu] = kws[i] if i < len(kws) else "—"
            rows.append(row)
        df_cmp = pd.DataFrame(rows)
        st.dataframe(df_cmp, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ce am invatat azi — Ziua 16")

    concepte = [
        ("Rezumare extractiva", "Selecteaza fraze din textul original pe baza scorului TF-IDF"),
        ("Rezumare abstractiva", "Genereaza text nou reformulat cu model neural (BART, T5)"),
        ("TF-IDF per fraza",   "Scorul frazei = media TF-IDF a cuvintelor importante din ea"),
        ("Rata de compresie",  "(1 - cuvinte_rezumat / cuvinte_original) × 100%"),
        ("Stopwords",          "Cuvinte comune eliminate: si, sau, in, la, de — nu aduc informatie"),
        ("BART / T5",          "Modele Transformer pentru generare text, excelente la rezumare"),
        ("Cuvinte cheie",      "Termenii cu cel mai mare TF-IDF = reprezentativi pentru document"),
        ("Keyword cloud",      "Vizualizare cuvinte cheie proportional cu importanta lor"),
    ]

    for concept, descriere in concepte:
        st.markdown(f"""
<div style='display:flex; gap:12px; padding:8px 14px; margin:4px 0;
     background:#f8f9fa; border-radius:8px; font-size:13px;
     border-left:4px solid #8e44ad;'>
<b style='color:#8e44ad; min-width:180px;'>{concept}</b>
<span style='color:#333;'>{descriere}</span>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.code("""
# Rezumare extractiva — fara dependente externe
import re, math

def rezumare_extractiva(text, n=3):
    fraze = re.split(r'(?<=[.!?])\\s+', text.strip())
    # TF-IDF per cuvant
    df = {}
    tf_list = []
    for fraza in fraze:
        cuv = re.findall(r'\\b\\w{4,}\\b', fraza.lower())
        tf = {}
        for c in cuv:
            tf[c] = tf.get(c,0) + 1/len(cuv) if cuv else 0
        tf_list.append(tf)
        for c in set(cuv):
            df[c] = df.get(c,0) + 1
    N = len(fraze)
    scor_cuv = {c: sum(tf.get(c,0) for tf in tf_list) *
                   math.log((N+1)/(d+1)+1)
                for c, d in df.items()}
    # Scor fraze
    scoruri = [sum(scor_cuv.get(c,0) for c in re.findall(r'\\b\\w{4,}\\b', f.lower()))
               for f in fraze]
    top = sorted(range(len(fraze)), key=lambda i: scoruri[i], reverse=True)[:n]
    return ' '.join(fraze[i] for i in sorted(top))

# Rezumare abstractiva — Hugging Face
from transformers import pipeline
summarizer = pipeline("summarization",
                       model="sshleifer/distilbart-cnn-12-6")
rez = summarizer(text, max_length=80, min_length=30)
print(rez[0]['summary_text'])
""", language="python")

    st.info("""
**Ziua 17 — Named Entity Recognition (NER)**

Extrage automat entitati din text:
- **Persoane:** Ionescu Gheorghe, inspector Pop. I.A.
- **Locatii:** Gorj, Bumbesti-Jiu, parcela GJ-045
- **Organizatii:** APIA, UCB Targu Jiu, Prefectura Gorj
- **Date:** 14 aprilie 2024, campania 2024
- **Numere/Cantitati:** 45.30 ha, NDVI 0.62, 3.42%

Aplicatie: extragere automata date structurate din rapoarte APIA.
""")

    st.markdown("""
---
*Referinta: "Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"
— Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, Universitatea din Petrosani, 2024*
""")
