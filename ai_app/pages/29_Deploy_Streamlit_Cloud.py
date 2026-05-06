"""
Ziua 29 — Deploy pe Streamlit Cloud
Modul 5: AI Agenti + Finalizare
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 29 — Deploy Streamlit Cloud",
    page_icon="CLOUD",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:26px; font-weight:900; color:#1abc9c;'>CLOUD</div>
    <div style='font-size:16px; font-weight:700; color:#1abc9c;'>ZIUA 29</div>
    <div style='font-size:11px; color:#666;'>Deploy Streamlit Cloud</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 5 — AI Agenti + Finalizare")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 29 / 30 zile")
st.sidebar.progress(29 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Repo GitHub:**
`olimihnea-spec/`
`agrovision-bloc5-securegeo`

**Main file:**
`ai_app/Acasa.py`

**Status:** Deployed
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#1abc9c; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:36px; font-weight:900; color:#1abc9c;'>CLOUD</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1abc9c; font-weight:800;'>
            Ziua 29 — Deploy pe Streamlit Cloud
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            GitHub → Streamlit Cloud → URL public · gratuit · actualizare automata la push
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.success(
    "Aplicatia **AI Aplicat — Bloc 5** este deja live pe Streamlit Cloud. "
    "Aceasta pagina documenteaza cum a fost facut deploy-ul si cum se mentine."
)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Cum functioneaza",
    "Checklist deploy",
    "Configurare",
    "Troubleshooting",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CUM FUNCTIONEAZA
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ce este Streamlit Cloud?")
        st.markdown("""
**Streamlit Cloud** (share.streamlit.io) este platforma gratuita Streamlit
care gazduieste aplicatii Python direct din GitHub.

**Avantaje:**
- **Gratuit** pentru aplicatii publice (1 app privata inclusa)
- **Zero configurare server** — nu ai nevoie de hosting, Docker, AWS
- **Deploy automat** — orice `git push` redeploya aplicatia in 2-3 minute
- **URL public** — share cu studenti, colegi, comisii APIA
- **Logs in timp real** — vezi erorile direct din browser

**Cum functioneaza:**
```
Tu scrii cod local
       ↓
git push → GitHub repo
       ↓
Streamlit Cloud detecteaza push-ul
       ↓
Instaleaza requirements.txt (~2-5 min)
       ↓
Ruleaza Acasa.py
       ↓
URL public disponibil
```

**Limitari gratuit:**
- 1 GB RAM per aplicatie
- Fara GPU (Ollama nu ruleaza pe Cloud)
- Aplicatia "doarme" dupa 7 zile inactivitate
  (se trezeste la primul acces, ~30 sec)
""")

    with col2:
        st.subheader("Arhitectura acestei aplicatii pe Cloud")
        st.markdown("""
```
GitHub: olimihnea-spec/agrovision-bloc5-securegeo
│
├── ai_app/
│   ├── Acasa.py              ← main file
│   ├── requirements.txt      ← pachete Python
│   ├── .streamlit/
│   │   └── config.toml       ← tema, setari
│   └── pages/
│       ├── 01_...py
│       ├── ...
│       └── 29_Deploy.py      ← aceasta pagina
│
└── (alte fisiere proiect)
```

**Ce functioneaza pe Cloud (fara Ollama):**
| Instrument | Status Cloud |
|---|---|
| Calcule NDVI, PAC | Functioneaza |
| Machine Learning (sklearn) | Functioneaza |
| NLP (reguli, TF-IDF) | Functioneaza |
| Semantic Scholar / arXiv | Functioneaza |
| Upload CSV parcele | Functioneaza |
| RAG (fara LLM) | Partial |
| Ollama / LLM local | Demo mode |
| Stable Diffusion | Indisponibil |

**Concluzie:** 80% din instrumentele
aplicatiei functioneaza complet pe Cloud.
Ollama ramane un avantaj al versiunii locale.
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHECKLIST DEPLOY
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Checklist complet — deploy pe Streamlit Cloud")
    st.markdown("Toate pasii au fost deja parcursi pentru aceasta aplicatie.")

    sectiuni = {
        "Pregatire cod": [
            ("Acasa.py functional local", True, "Fisierul principal ruleaza fara erori pe calculatorul tau"),
            ("Toate paginile din pages/ testate", True, "Fiecare pagina incarcata cel putin o data"),
            ("Imports cu try/except pentru pachete optionale", True, "Pachete grele (torch, cv2) au fallback graceful"),
            ("Demo mode pentru instrumente offline", True, "Ollama offline → raspunsuri demo prestabilite"),
            ("Fara cai absolute Windows in cod", True, "Niciun 'C:\\Users\\...' hardcodat"),
        ],
        "GitHub": [
            ("Cont GitHub creat", True, "github.com/olimihnea-spec"),
            ("Repository creat (public)", True, "agrovision-bloc5-securegeo"),
            ("git init + git remote add origin", True, "Repo local conectat la GitHub"),
            ("requirements.txt comis", True, "Toate pachetele necesare listate"),
            ("Acasa.py si pages/ comise si urcate", True, "git push origin main"),
            ("Fisiere sensibile excluse (.gitignore)", True, ".env, chei API, date personale"),
        ],
        "Streamlit Cloud": [
            ("Cont Streamlit Cloud creat cu GitHub", True, "share.streamlit.io → Sign in with GitHub"),
            ("New app → repo selectat", True, "olimihnea-spec/agrovision-bloc5-securegeo"),
            ("Main file path setat corect", True, "ai_app/Acasa.py"),
            ("Branch: main", True, ""),
            ("Deploy click → asteptat build", True, "Prima data dureaza 5-10 min"),
            ("URL public generat", True, "Partajabil cu studenti si colegi"),
        ],
        "Mentenanta": [
            ("git push = actualizare automata", True, "Nu mai trebuie nimic altceva"),
            ("Logs accesibile din dashboard Streamlit", True, "Buton '...' → Manage app → Logs"),
            ("Reboot app daca ingheata", True, "Manage app → Reboot"),
            ("Secrets pentru chei API (daca ai)", True, "Streamlit Cloud → Settings → Secrets"),
        ],
    }

    for sectiune, itemi in sectiuni.items():
        st.markdown(f"""
<div style='background:#1abc9c20; border-left:4px solid #1abc9c; border-radius:6px;
     padding:8px 14px; margin:14px 0 6px 0; font-weight:700; font-size:13px;
     color:#1abc9c;'>{sectiune}</div>
""", unsafe_allow_html=True)
        for text, done, explicatie in itemi:
            bg = "#d4edda" if done else "#f8f9fa"
            icon = "✅" if done else "⬜"
            col_text = "#333" if done else "#aaa"
            exp_html = f"<br><span style='color:#888; font-size:10px;'>{explicatie}</span>" if explicatie else ""
            st.markdown(f"""
<div style='background:{bg}; border-radius:4px; padding:6px 12px;
     margin:2px 0; font-size:11px; color:{col_text};'>
{icon} {text}{exp_html}
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.success("Toate cele 4 sectiuni sunt complete. Aplicatia este live pe Streamlit Cloud.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CONFIGURARE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Fisiere de configurare")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown("**requirements.txt — pachete instalate pe Cloud**")
        st.code("""streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0,<2.0.0
plotly>=5.18.0
scikit-learn>=1.3.0
Pillow>=10.0.0
cryptography>=42.0.0
joblib>=1.3.0
scipy>=1.10.0
opencv-python-headless>=4.8.0
scikit-image>=0.21.0
pypdf>=4.0.0
langchain>=0.2.0
langchain-community>=0.2.0
langchain-ollama>=0.1.0
duckduckgo-search>=6.0.0
""", language="text")

        st.markdown("""
**Nota importanta:**
- `opencv-python-headless` in loc de `opencv-python`
  (versiunea headless nu are nevoie de display grafic)
- `numpy<2.0.0` pentru compatibilitate PyArrow/Streamlit
- `langchain-ollama` se instaleaza dar nu are efect pe Cloud
  (Ollama nu ruleaza, paginile cad in demo mode)
""")

    with col_c2:
        st.markdown("**`.streamlit/config.toml` — tema aplicatiei**")
        st.code("""[theme]
primaryColor = "#8e44ad"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 50

[browser]
gatherUsageStats = false
""", language="toml")

        st.markdown("**Secrets — pentru chei API (optional)**")
        st.code("""# In Streamlit Cloud:
# Settings → Secrets → editezi direct

# Format TOML:
[openai]
api_key = "sk-..."

[apia]
token = "..."

# Accesezi in Python:
import streamlit as st
cheie = st.secrets["openai"]["api_key"]
""", language="python")

        st.info(
            "Aceasta aplicatie nu foloseste chei API platite. "
            "Toate serviciile sunt gratuite (Semantic Scholar, arXiv, CrossRef, DuckDuckGo)."
        )

    st.divider()
    st.subheader("Fluxul de actualizare")
    st.markdown("""
```bash
# 1. Modifici un fisier local (ex. adaugi o pagina noua)
# Editezi pages/30_Certificat_Final.py

# 2. Comiti modificarile
git add pages/30_Certificat_Final.py
git commit -m "Z30: Certificat final si roadmap AI 2026-2027"

# 3. Urcoci pe GitHub
git push origin main

# 4. Streamlit Cloud detecteaza push-ul automat
# Aplicatia se redeploya in 2-3 minute
# URL-ul ramane acelasi — nu trebuie facut nimic altceva
```

**Verificare deploy:** In Streamlit Cloud dashboard → aplicatia ta → statusul devine verde cand e gata.
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TROUBLESHOOTING
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Probleme frecvente si solutii")

    probleme = [
        {
            "problema": "ModuleNotFoundError: No module named 'cv2'",
            "cauza": "opencv-python (cu GUI) nu functioneaza pe server fara display.",
            "solutie": "Foloseste `opencv-python-headless` in requirements.txt in loc de `opencv-python`.",
            "cod": "# requirements.txt\nopencv-python-headless>=4.8.0  # NU opencv-python",
            "culoare": "#e74c3c",
        },
        {
            "problema": "App ingheata / spinner infinit",
            "cauza": "Un import greu la startup (ex. torch, transformers) blocheaza incarcarea.",
            "solutie": "Muta importul greu in interiorul functiei/butonului, nu la nivel de modul.",
            "cod": "# Nu la nivel de fisier:\n# import torch  ← blocheaza startup\n\n# Da, in interiorul functiei:\nif st.button('Ruleaza'):\n    import torch  # importat doar cand e nevoie",
            "culoare": "#e67e22",
        },
        {
            "problema": "UnicodeEncodeError / diacritice corupte",
            "cauza": "Windows foloseste cp1250, serverul Cloud foloseste UTF-8.",
            "solutie": "Toate fisierele .py salvate UTF-8. Nu folosi print() cu diacritice in terminal.",
            "cod": "# La inceputul fisierului (optional, dar sigur):\n# -*- coding: utf-8 -*-\n\n# Sau la scriere fisiere:\nwith open('fisier.txt', 'w', encoding='utf-8') as f:\n    f.write('continut cu diacritice: ă â î ș ț')",
            "culoare": "#f39c12",
        },
        {
            "problema": "Pagina nu apare in sidebar (lipseste din navigatie)",
            "cauza": "Fisierul nu este comis pe GitHub (git add + git commit uitat).",
            "solutie": "Verifica cu `git status` ca fisierul este comis si `git push` e facut.",
            "cod": "# Verificare:\ngit status\n# Daca fisierul apare ca 'Untracked':\ngit add pages/numele_paginii.py\ngit commit -m 'Add pagina noua'\ngit push origin main",
            "culoare": "#8e44ad",
        },
        {
            "problema": "Build esuat: 'ERROR: Could not find a version...'",
            "cauza": "Versiune de pachet specificata gresit sau incompatibila.",
            "solutie": "Sterge versiunea exacta si lasa pip sa aleaga: `pandas` in loc de `pandas==2.1.4`.",
            "cod": "# requirements.txt — versiuni flexibile:\npandas>=2.0.0      # NU pandas==2.1.4\nnumpy>=1.24.0,<2.0.0  # interval acceptat",
            "culoare": "#1a5276",
        },
        {
            "problema": "App 'doarme' (sleeping) dupa inactivitate",
            "cauza": "Streamlit Cloud pune in sleep aplicatiile inactive 7+ zile (plan gratuit).",
            "solutie": "Primul acces dupa sleep dureaza ~30 secunde pentru trezire. Normal, nu e eroare.",
            "cod": "# Nu exista solutie tehnica pentru planul gratuit.\n# Optional: upgrade la plan platit (~$20/luna)\n# sau acceseaza periodic aplicatia.",
            "culoare": "#27ae60",
        },
    ]

    for pb in probleme:
        with st.expander(f"**{pb['problema']}**", expanded=False):
            col_pb1, col_pb2 = st.columns([1, 1])
            with col_pb1:
                st.markdown(f"""
<div style='background:{pb["culoare"]}15; border-left:3px solid {pb["culoare"]};
     border-radius:4px; padding:8px 12px; font-size:11px; margin-bottom:8px;'>
<b>Cauza:</b> {pb["cauza"]}
</div>
<div style='background:#e8f8f5; border-left:3px solid #27ae60;
     border-radius:4px; padding:8px 12px; font-size:11px;'>
<b>Solutie:</b> {pb["solutie"]}
</div>
""", unsafe_allow_html=True)
            with col_pb2:
                st.code(pb["cod"], language="python")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ziua 29 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### Deploy complet in 4 comenzi

```bash
# 1. Initializare (o singura data)
git init
git remote add origin https://github.com/...

# 2. Fiecare actualizare
git add .
git commit -m "Descriere modificare"
git push origin main

# 3. Streamlit Cloud face restul automat
# (instaleaza pachete, porneste serverul,
#  genereaza URL public)
```

#### Structura minima pentru deploy

```
proiect/
├── Acasa.py          ← main file (setat in Cloud)
├── requirements.txt  ← pachete necesare
├── pages/            ← pagini suplimentare
│   └── *.py
└── .streamlit/       ← optional
    └── config.toml   ← tema, setari
```

**Nu ai nevoie de:**
- Docker / containerizare
- Nginx / server web
- Certificat SSL (Cloud il face automat)
- Domeniu (primesti subdomain gratuit)
""")

    with col2:
        st.markdown("""
#### Ce inseamna asta pentru UCB si APIA

**Fara deploy** — aplicatia ta exista doar pe laptop:
- Studenti nu pot accesa
- Nu functioneaza cand laptopul e inchis
- Nu poate fi partajat cu comisii, inspectori

**Cu deploy Streamlit Cloud** — aplicatia e live:
- URL public, accesibil de oriunde
- Studenti acceseaza de pe telefon / acasa
- Colegi APIA folosesc instrumentele online
- Comisii de evaluare UCB vad aplicatia live
- Functioneaza 24/7 fara interventia ta

**Scenarii reale:**
- Prezentare teza → link live in loc de demo local
- Curs UCB → studenti acceseaza dashboard-ul
- Inspector APIA → incarca CSV de pe birou, primeste raport
- Conferinta ISI → demo online disponibil audientei
""")

        st.markdown("""
<div style='background:#e8f8f5; border-radius:8px; padding:12px;
     border-left:4px solid #1abc9c; margin-top:10px;'>
<div style='font-weight:700; color:#1abc9c;'>Concluzie Ziua 29</div>
<div style='font-size:11px; color:#333; margin-top:6px; line-height:1.7;'>
De la cod local la aplicatie publica accesibila global:
<b>git push</b> este tot ce trebuie.<br><br>
Gratuit, automat, profesional.
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#1abc9c 0%,#1a5276 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 29 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
Streamlit Cloud · GitHub CI/CD · requirements.txt · config.toml · Secrets · Troubleshooting
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.75;'>
Urmatoarea si ultima: <b>Ziua 30 — Certificat final + Roadmap AI 2026-2027</b>
</div>
</div>
""", unsafe_allow_html=True)
