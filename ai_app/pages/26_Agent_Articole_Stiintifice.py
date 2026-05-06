"""
Ziua 26 — Agent cautare articole stiintifice (100% gratuit, fara API key)
Modul 5: AI Agenti + Finalizare
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj

Baze de date: Semantic Scholar · arXiv · CrossRef — toate gratuite, fara cont
"""

import streamlit as st
import datetime
import time
import re
import json
import urllib.parse

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

OLLAMA_URL = "http://localhost:11434"

# ══════════════════════════════════════════════════════════════════════════════
# INSTRUMENTE CAUTARE ACADEMICA — 100% gratuite, fara API key
# ══════════════════════════════════════════════════════════════════════════════

def tool_semantic_scholar(query: str, limit: int = 5) -> str:
    """Cauta in Semantic Scholar (200M articole, gratuit)."""
    try:
        r = requests.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params={
                "query": query,
                "limit": limit,
                "fields": "title,authors,year,abstract,citationCount,externalIds,venue",
            },
            headers={"User-Agent": "AI-Aplicat-UCB/1.0"},
            timeout=15,
        )
        if r.status_code == 200:
            papers = r.json().get("data", [])
            if not papers:
                return f"Niciun rezultat pentru: {query}"
            rezultate = []
            for p in papers:
                autori = ", ".join(a["name"] for a in p.get("authors", [])[:3])
                if len(p.get("authors", [])) > 3:
                    autori += " et al."
                an = p.get("year", "?")
                titlu = p.get("title", "?")
                cit = p.get("citationCount", 0)
                doi = p.get("externalIds", {}).get("DOI", "")
                revista = p.get("venue", "")
                abstract = (p.get("abstract") or "")[:250].replace("\n", " ")
                doi_str = f"https://doi.org/{doi}" if doi else "DOI indisponibil"
                rezultate.append(
                    f"TITLU: {titlu}\n"
                    f"AUTORI: {autori} ({an})\n"
                    f"REVISTA: {revista}\n"
                    f"CITAT: de {cit} ori | {doi_str}\n"
                    f"ABSTRACT: {abstract}..."
                )
            return "\n---\n".join(rezultate)
        if r.status_code == 429:
            return "Semantic Scholar: prea multe cereri — asteapta 30 secunde si recearca."
        return f"Semantic Scholar eroare HTTP {r.status_code}"
    except requests.exceptions.Timeout:
        return "Semantic Scholar: timeout — verifica conexiunea."
    except Exception as e:
        return f"Semantic Scholar eroare: {e}"


def tool_arxiv(query: str, limit: int = 5) -> str:
    """Cauta preprint-uri pe arXiv (gratuit, fara autentificare)."""
    try:
        encoded = urllib.parse.quote(query)
        r = requests.get(
            f"https://export.arxiv.org/api/query"
            f"?search_query=all:{encoded}&start=0&max_results={limit}&sortBy=relevance",
            timeout=15,
        )
        if r.status_code != 200:
            return f"arXiv eroare HTTP {r.status_code}"

        entries = re.findall(r"<entry>(.*?)</entry>", r.text, re.DOTALL)
        if not entries:
            return f"Niciun rezultat arXiv pentru: {query}"

        rezultate = []
        for entry in entries[:limit]:
            titlu_m = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
            autori = re.findall(r"<name>(.*?)</name>", entry)
            pub_m = re.search(r"<published>(.*?)</published>", entry)
            id_m = re.search(r"<id>(.*?)</id>", entry)
            summ_m = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)

            titlu = titlu_m.group(1).strip().replace("\n", " ") if titlu_m else "?"
            autori_str = ", ".join(autori[:3]) + (" et al." if len(autori) > 3 else "")
            an = pub_m.group(1)[:4] if pub_m else "?"
            arxiv_id = id_m.group(1).strip() if id_m else ""
            abstract = summ_m.group(1).strip().replace("\n", " ")[:250] if summ_m else ""

            rezultate.append(
                f"TITLU: {titlu}\n"
                f"AUTORI: {autori_str} ({an})\n"
                f"SURSA: arXiv | {arxiv_id}\n"
                f"ABSTRACT: {abstract}..."
            )
        return "\n---\n".join(rezultate)
    except requests.exceptions.Timeout:
        return "arXiv: timeout — verifica conexiunea."
    except Exception as e:
        return f"arXiv eroare: {e}"


def tool_crossref(query: str, limit: int = 5) -> str:
    """Cauta in CrossRef (metadate + DOI, gratuit)."""
    try:
        r = requests.get(
            "https://api.crossref.org/works",
            params={"query": query, "rows": limit,
                    "select": "title,author,published,DOI,container-title,is-referenced-by-count"},
            headers={"User-Agent": "AI-Aplicat-UCB/1.0 (mailto:olimihnea@gmail.com)"},
            timeout=15,
        )
        if r.status_code != 200:
            return f"CrossRef eroare HTTP {r.status_code}"

        items = r.json()["message"]["items"]
        if not items:
            return f"Niciun rezultat CrossRef pentru: {query}"

        rezultate = []
        for item in items[:limit]:
            titlu = (item.get("title") or ["?"])[0]
            autori_raw = item.get("author", [])
            autori_str = ", ".join(
                f"{a.get('family', '')} {(a.get('given') or ' ')[:1]}."
                for a in autori_raw[:3]
            )
            if len(autori_raw) > 3:
                autori_str += " et al."
            pub = item.get("published", {})
            parts = pub.get("date-parts", [[]])
            an = str(parts[0][0]) if parts and parts[0] else "?"
            doi = item.get("DOI", "")
            revista = (item.get("container-title") or ["?"])[0]
            cit = item.get("is-referenced-by-count", 0)

            rezultate.append(
                f"TITLU: {titlu}\n"
                f"AUTORI: {autori_str} ({an})\n"
                f"REVISTA: {revista} | Citat: {cit} ori\n"
                f"DOI: https://doi.org/{doi}"
            )
        return "\n---\n".join(rezultate)
    except requests.exceptions.Timeout:
        return "CrossRef: timeout."
    except Exception as e:
        return f"CrossRef eroare: {e}"


def tool_formateaza_apa(text_articole: str) -> str:
    """Formateaza articolele gasite in stil APA din sesiunea curenta."""
    bibliografie = st.session_state.get("articole_gasite", [])
    if not bibliografie:
        return "Nu am articole salvate inca. Cauta intai cu semantic_scholar sau arxiv."
    linii = []
    for i, art in enumerate(bibliografie, 1):
        autori = art.get("autori", "Autor necunoscut")
        an = art.get("an", "?")
        titlu = art.get("titlu", "?")
        revista = art.get("revista", "")
        doi = art.get("doi", "")
        doi_str = f" https://doi.org/{doi}" if doi else ""
        linii.append(f"[{i}] {autori} ({an}). {titlu}. {revista}.{doi_str}")
    return "\n".join(linii)


def salveaza_articole_din_text(text: str, sursa: str):
    """Parseaza textul returnat de tool si salveaza articolele in session_state."""
    if "articole_gasite" not in st.session_state:
        st.session_state["articole_gasite"] = []

    bucati = text.split("---")
    for bucata in bucati:
        titlu_m = re.search(r"TITLU:\s*(.+)", bucata)
        autori_m = re.search(r"AUTORI:\s*(.+)", bucata)
        doi_m = re.search(r"DOI.*?doi\.org/(\S+)", bucata)
        arxiv_m = re.search(r"arXiv.*?(arxiv\.org\S+)", bucata)
        revista_m = re.search(r"REVISTA:\s*(.+)", bucata)

        if titlu_m:
            titlu = titlu_m.group(1).strip()
            autori_raw = (autori_m.group(1) if autori_m else "").strip()
            an_m = re.search(r"\((\d{4})\)", autori_raw)
            an = an_m.group(1) if an_m else "?"
            autori = autori_raw.replace(f"({an})", "").strip()

            articol = {
                "titlu": titlu,
                "autori": autori,
                "an": an,
                "revista": (revista_m.group(1).split("|")[0].strip() if revista_m else sursa),
                "doi": doi_m.group(1) if doi_m else (arxiv_m.group(1) if arxiv_m else ""),
                "sursa": sursa,
            }
            exista = any(a["titlu"] == titlu for a in st.session_state["articole_gasite"])
            if not exista:
                st.session_state["articole_gasite"].append(articol)


TOOLS_BIBLIO = {
    "semantic_scholar": {
        "functie": tool_semantic_scholar,
        "descriere": "Cauta in 200 milioane articole academice. Query in engleza. Ex: 'NDVI drone crop detection Romania'",
    },
    "arxiv": {
        "functie": tool_arxiv,
        "descriere": "Cauta preprint-uri STEM (AI, matematica, fizica, biologie). Ex: 'deep learning agriculture remote sensing'",
    },
    "crossref": {
        "functie": tool_crossref,
        "descriere": "Cauta metadate si DOI-uri. Ex: 'unmanned aerial vehicle agricultural monitoring'",
    },
    "formateaza": {
        "functie": tool_formateaza_apa,
        "descriere": "Formateaza articolele gasite in bibliografie APA. Nu necesita input.",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# MOTOR ReAct PENTRU BIBLIOGRAFIE
# ══════════════════════════════════════════════════════════════════════════════

REACT_SYSTEM_BIBLIO = """Esti un asistent de cercetare academic specializat in agricultura, drone, AI si politici europene (PAC).
Ajuti profesori sa gaseasca articole stiintifice relevante si sa construiasca bibliografii corecte.

Raspunde INTOTDEAUNA in formatul:
Thought: [analiza ta]
Action: [semantic_scholar | arxiv | crossref | formateaza | raspuns_direct]
Action Input: [query-ul sau comanda]

SAU cand ai terminat:
Thought: Am gasit suficiente articole.
Final Answer: [lista articolelor gasite + recomandare]

REGULI:
1. Traduce query-ul in ENGLEZA pentru cautare (rezultate mult mai bune)
2. Fa 2-3 cautari cu termeni diferiti, nu repeta aceeasi cautare
3. Dupa cautari, apeleaza 'formateaza' pentru bibliografie APA
4. Mentioneaza numarul de citatii ca indicator de calitate
5. Nu inventa titluri sau autori

Instrumente: semantic_scholar | arxiv | crossref | formateaza
"""


def parseaza_reactie_biblio(text: str):
    final = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL | re.IGNORECASE)
    if final:
        return "final", final.group(1).strip()
    action = re.search(r"Action:\s*(\S+)", text, re.IGNORECASE)
    action_input = re.search(r"Action Input:\s*(.+?)(?=\nThought|\nAction|\Z)", text, re.DOTALL | re.IGNORECASE)
    if action:
        tool_name = action.group(1).strip().lower().rstrip(".,:")
        tool_input = action_input.group(1).strip() if action_input else ""
        return tool_name, tool_input
    return "necunoscut", text[:150]


def ollama_genereaza(model: str, prompt: str, system: str = "") -> str:
    if not REQUESTS_OK:
        return "Final Answer: Ollama indisponibil."
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "system": system,
                  "stream": False, "options": {"temperature": 0.1}},
            timeout=90,
        )
        if r.status_code == 200:
            return r.json().get("response", "")
        return f"Final Answer: Eroare Ollama {r.status_code}"
    except Exception as e:
        return f"Final Answer: {e}"


def verifica_ollama():
    if not REQUESTS_OK:
        return False, []
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if r.status_code == 200:
            return True, [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return False, []


def ruleaza_agent_biblio(tema: str, model: str, max_pasi: int = 6):
    pasi = []
    istoric = ""
    prompt_initial = (
        f"Tema de cercetare: {tema}\n\n"
        "Cauta articole stiintifice relevante folosind instrumentele disponibile. "
        "Fa cel putin 2 cautari cu termeni diferiti in engleza, "
        "apoi formateaza bibliografia APA. Incepe cu Thought:"
    )

    for pas in range(1, max_pasi + 1):
        prompt_complet = prompt_initial if pas == 1 else f"{prompt_initial}\n\n{istoric}"
        raspuns_llm = ollama_genereaza(model, prompt_complet, REACT_SYSTEM_BIBLIO)

        tip, valoare = parseaza_reactie_biblio(raspuns_llm)

        if tip == "final":
            pasi.append({"pas": pas, "tip": "final", "raspuns": valoare, "thought": raspuns_llm})
            return pasi, valoare

        if tip in TOOLS_BIBLIO:
            with st.spinner(f"Pas {pas} — cautare {tip}..."):
                observatie = TOOLS_BIBLIO[tip]["functie"](valoare)
            if tip in ("semantic_scholar", "arxiv", "crossref"):
                salveaza_articole_din_text(observatie, tip)
        elif tip == "raspuns_direct":
            pasi.append({"pas": pas, "tip": "final", "raspuns": valoare, "thought": raspuns_llm})
            return pasi, valoare
        else:
            observatie = f"Instrument '{tip}' necunoscut. Foloseste: semantic_scholar, arxiv, crossref, formateaza."

        pasi.append({
            "pas": pas, "tip": "actiune",
            "actiune": tip, "input": valoare,
            "observatie": observatie[:800],
            "thought": raspuns_llm,
        })
        istoric += f"\n{raspuns_llm}\nObservation: {observatie[:800]}\n"

    return pasi, "Agentul a epuizat pasii. Rezultatele partiale sunt afisate mai jos."


# ══════════════════════════════════════════════════════════════════════════════
# DATE DEMO
# ══════════════════════════════════════════════════════════════════════════════

DEMO_ARTICOLE = [
    {
        "titlu": "UAV-based NDVI estimation for crop monitoring in Romanian agricultural areas",
        "autori": "Ionescu M., Popescu A., Gheorghe C.",
        "an": "2023",
        "revista": "Computers and Electronics in Agriculture",
        "doi": "10.1016/j.compag.2023.108234",
        "sursa": "semantic_scholar",
    },
    {
        "titlu": "Deep learning approaches for agricultural land use classification using satellite imagery",
        "autori": "Zhang W., Liu H., Wang X. et al.",
        "an": "2022",
        "revista": "Remote Sensing",
        "doi": "10.3390/rs14051145",
        "sursa": "crossref",
    },
    {
        "titlu": "Automated crop disease detection using convolutional neural networks and drone imagery",
        "autori": "Patel R., Kumar S., Mishra P.",
        "an": "2023",
        "revista": "arXiv",
        "doi": "arxiv.org/abs/2301.09876",
        "sursa": "arxiv",
    },
    {
        "titlu": "PAC 2023-2027 compliance monitoring through geospatial AI: A Romanian case study",
        "autori": "Dumitrescu B., Florescu I.",
        "an": "2024",
        "revista": "Land Use Policy",
        "doi": "10.1016/j.landusepol.2024.107123",
        "sursa": "semantic_scholar",
    },
    {
        "titlu": "Multispectral drone imaging for vineyard stress detection in South Romania",
        "autori": "Costache R., Marin D., Tudor E.",
        "an": "2023",
        "revista": "Precision Agriculture",
        "doi": "10.1007/s11119-023-10045-8",
        "sursa": "crossref",
    },
]

DEMO_PASI = [
    {
        "pas": 1, "tip": "actiune",
        "actiune": "semantic_scholar",
        "input": "NDVI drone crop detection Romania agriculture",
        "observatie": "TITLU: UAV-based NDVI estimation for crop monitoring in Romanian agricultural areas\nAUTORI: Ionescu M., Popescu A. (2023)\nCITAT: de 47 ori | https://doi.org/10.1016/j.compag.2023.108234",
        "thought": "Thought: Voi cauta pe Semantic Scholar cu termeni in engleza.\nAction: semantic_scholar\nAction Input: NDVI drone crop detection Romania agriculture",
    },
    {
        "pas": 2, "tip": "actiune",
        "actiune": "arxiv",
        "input": "deep learning agricultural monitoring unmanned aerial vehicle",
        "observatie": "TITLU: Automated crop disease detection using convolutional neural networks and drone imagery\nAUTORI: Patel R., Kumar S. (2023)\nSURSA: arXiv",
        "thought": "Thought: Caut si pe arXiv preprint-uri despre UAV si deep learning.\nAction: arxiv\nAction Input: deep learning agricultural monitoring unmanned aerial vehicle",
    },
    {
        "pas": 3, "tip": "actiune",
        "actiune": "formateaza",
        "input": "",
        "observatie": "[1] Ionescu M., Popescu A., Gheorghe C. (2023). UAV-based NDVI estimation... https://doi.org/10.1016/j.compag.2023.108234\n[2] Patel R., Kumar S. (2023). Automated crop disease detection...",
        "thought": "Thought: Am suficiente articole. Formateaza bibliografia APA.\nAction: formateaza\nAction Input: ",
    },
    {
        "pas": 4, "tip": "final",
        "raspuns": "Am gasit 5 articole relevante pentru tema aleasa. Cele mai citate sunt din Computers and Electronics in Agriculture si Remote Sensing. Recomand in special lucrarile din 2023-2024 pentru actualitate. Bibliografia APA este formatata mai sus.",
        "thought": "Thought: Am finalizat cautarea si formatarea.\nFinal Answer: ...",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 26 — Agent Articole",
    page_icon="ISI",
    layout="wide",
    initial_sidebar_state="expanded"
)

ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#16a085;'>ISI</div>
    <div style='font-size:16px; font-weight:700; color:#16a085;'>ZIUA 26</div>
    <div style='font-size:11px; color:#666;'>Agent Articole Stiintifice</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 5 — AI Agenti + Finalizare")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 26 / 30 zile")
st.sidebar.progress(26 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_ales = st.sidebar.selectbox("Model:", modele_disponibile or ["llama3.2:latest"])
else:
    st.sidebar.warning("Ollama offline — cautare directa disponibila")
    model_ales = "llama3.2:latest"

st.sidebar.markdown("""
**Baze de date (gratuite):**
- Semantic Scholar — 200M articole
- arXiv — preprint-uri STEM
- CrossRef — DOI + metadate

**Fara API key, fara cont.**
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#16a085; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:38px; font-weight:900; color:#16a085;'>ISI</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#16a085; font-weight:800;'>
            Ziua 26 — Agent cautare articole stiintifice
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Semantic Scholar · arXiv · CrossRef — 100% gratuit, fara API key
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Agent automat",
    "Cautare manuala",
    "Bibliografie acumulata",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — AGENT AUTOMAT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Agent ReAct — cauta si compileaza bibliografie automat")

    teme_exemple = [
        "Detectia neconformitatilor PAC cu drone si algoritmi AI",
        "NDVI si teledetectie pentru monitorizarea culturilor agricole",
        "Inteligenta artificiala in controlul subventiilor agricole europene",
        "Drone UAV in agricultura de precizie Romania",
        "Phantom GPS geolocation EXIF metadata agriculture",
    ]

    col_tema, col_opt = st.columns([2, 1])
    with col_tema:
        tema_cercetare = st.text_area(
            "Tema de cercetare:",
            value=teme_exemple[0],
            height=80,
            key="tema_agent_biblio",
        )
    with col_opt:
        max_pasi_biblio = st.slider("Pasi max agent:", 3, 7, 5, key="pasi_biblio")
        nr_rezultate = st.slider("Rezultate per baza:", 3, 8, 5, key="nr_rez")
        arata_pasi_biblio = st.checkbox("Arata pasii ReAct", value=True, key="show_steps_b")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        lanseaza = st.button(
            "Lanseaza agent cautare",
            type="primary", use_container_width=True, key="btn_agent_biblio"
        )
    with col_b2:
        if not ollama_ok:
            demo_btn = st.button(
                "Demo (fara Ollama)",
                use_container_width=True, key="btn_demo_biblio"
            )
        else:
            demo_btn = False

    st.markdown("**Teme rapide:**")
    cols_teme = st.columns(len(teme_exemple))
    for i, (col_t, tema_ex) in enumerate(zip(cols_teme, teme_exemple)):
        with col_t:
            if st.button(f"T{i+1}", key=f"tema_btn_{i}", use_container_width=True,
                         help=tema_ex):
                st.session_state["tema_agent_biblio"] = tema_ex
                st.rerun()

    if lanseaza or (not ollama_ok and "demo_btn" in dir() and demo_btn):
        st.markdown("---")
        st.markdown(f"**Tema:** {tema_cercetare}")

        if ollama_ok:
            pasi_biblio, raspuns_final_biblio = ruleaza_agent_biblio(
                tema_cercetare, model_ales, max_pasi_biblio
            )
        else:
            time.sleep(0.8)
            st.session_state["articole_gasite"] = DEMO_ARTICOLE.copy()
            pasi_biblio = DEMO_PASI
            raspuns_final_biblio = DEMO_PASI[-1]["raspuns"]

        if arata_pasi_biblio:
            st.markdown("**Traseul agentului:**")
            for pas_info in pasi_biblio:
                if pas_info["tip"] == "actiune":
                    culori_tool = {
                        "semantic_scholar": "#1a5276",
                        "arxiv": "#c0392b",
                        "crossref": "#8e44ad",
                        "formateaza": "#27ae60",
                    }
                    culoare_tool = culori_tool.get(pas_info["actiune"], "#666")
                    with st.expander(
                        f"Pas {pas_info['pas']} — {pas_info['actiune'].upper()}",
                        expanded=False
                    ):
                        thought_lines = [l for l in pas_info["thought"].split("\n") if "Thought:" in l]
                        if thought_lines:
                            st.caption(thought_lines[0])
                        st.markdown(f"""
<div style='background:{culoare_tool}15; border-left:3px solid {culoare_tool};
     border-radius:4px; padding:6px 10px; font-size:11px; margin:4px 0;'>
<b>Query:</b> {pas_info["input"]}
</div>
""", unsafe_allow_html=True)
                        st.code(pas_info["observatie"][:600], language=None)

        st.success(f"Agent finalizat — {len(st.session_state.get('articole_gasite', []))} articole gasite")
        st.markdown(f"""
<div style='background:linear-gradient(135deg,#16a085 0%,#1a5276 100%);
     border-radius:10px; padding:14px 20px; color:white; margin-top:8px;'>
<div style='font-size:12px; opacity:0.8; margin-bottom:4px;'>CONCLUZIE AGENT</div>
<div style='font-size:13px; line-height:1.7;'>{raspuns_final_biblio}</div>
</div>
""", unsafe_allow_html=True)

        if st.session_state.get("articole_gasite"):
            st.markdown("**Bibliografie APA generata:**")
            linii_apa = []
            for i, art in enumerate(st.session_state["articole_gasite"], 1):
                doi_str = f" https://doi.org/{art['doi']}" if art.get("doi") else ""
                linii_apa.append(
                    f"[{i}] {art['autori']} ({art['an']}). {art['titlu']}. "
                    f"*{art['revista']}*.{doi_str}"
                )
            bibliografie_text = "\n\n".join(linii_apa)
            st.text_area("", bibliografie_text, height=200, key="biblio_output")
            st.download_button(
                "Descarca bibliografie .txt",
                data=bibliografie_text.encode("utf-8"),
                file_name=f"bibliografie_{datetime.date.today().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CAUTARE MANUALA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Cautare manuala — testa fiecare baza de date")
    st.info("Cautarea manuala functioneaza fara Ollama — necesita doar conexiune internet.")

    query_manual = st.text_input(
        "Termen de cautare (in engleza pentru rezultate mai bune):",
        "NDVI unmanned aerial vehicle crop monitoring",
        key="query_manual",
    )
    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        if st.button("Semantic Scholar", use_container_width=True, key="btn_ss_manual",
                     type="primary"):
            with st.spinner("Caut Semantic Scholar..."):
                rez = tool_semantic_scholar(query_manual, limit=5)
            salveaza_articole_din_text(rez, "semantic_scholar")
            st.markdown(f"""
<div style='background:#e8f4fd; border-left:4px solid #1a5276; border-radius:6px;
     padding:12px; font-size:11px; font-family:monospace; white-space:pre-wrap;
     max-height:400px; overflow-y:auto;'>{rez}</div>
""", unsafe_allow_html=True)

    with col_m2:
        if st.button("arXiv", use_container_width=True, key="btn_arxiv_manual"):
            with st.spinner("Caut arXiv..."):
                rez = tool_arxiv(query_manual, limit=5)
            salveaza_articole_din_text(rez, "arxiv")
            st.markdown(f"""
<div style='background:#fdecea; border-left:4px solid #c0392b; border-radius:6px;
     padding:12px; font-size:11px; font-family:monospace; white-space:pre-wrap;
     max-height:400px; overflow-y:auto;'>{rez}</div>
""", unsafe_allow_html=True)

    with col_m3:
        if st.button("CrossRef", use_container_width=True, key="btn_cr_manual"):
            with st.spinner("Caut CrossRef..."):
                rez = tool_crossref(query_manual, limit=5)
            salveaza_articole_din_text(rez, "crossref")
            st.markdown(f"""
<div style='background:#f5eef8; border-left:4px solid #8e44ad; border-radius:6px;
     padding:12px; font-size:11px; font-family:monospace; white-space:pre-wrap;
     max-height:400px; overflow-y:auto;'>{rez}</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
**Sfaturi pentru query-uri eficiente:**

| In loc de... | Foloseste... |
|---|---|
| "drone agricultura" | "UAV unmanned aerial vehicle crop monitoring" |
| "NDVI Romania" | "NDVI remote sensing agricultural Romania" |
| "AI pentru APIA" | "machine learning EU agricultural subsidy compliance" |
| "GPS fantoma" | "phantom GPS EXIF metadata geolocation spoofing" |
""")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BIBLIOGRAFIE ACUMULATA
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Bibliografie acumulata in aceasta sesiune")

    articole = st.session_state.get("articole_gasite", [])

    if not articole:
        st.info("Niciun articol inca. Foloseste agentul sau cautarea manuala.")
    else:
        st.metric("Articole gasite", len(articole))

        col_surse = st.columns(3)
        surse_count = {}
        for art in articole:
            surse_count[art.get("sursa", "?")] = surse_count.get(art.get("sursa", "?"), 0) + 1
        for i, (sursa, cnt) in enumerate(surse_count.items()):
            with col_surse[i % 3]:
                st.metric(sursa, cnt)

        st.markdown("---")
        format_ales = st.radio(
            "Format bibliografie:", ["APA", "IEEE", "BibTeX"], horizontal=True
        )

        linii = []
        for i, art in enumerate(articole, 1):
            autori = art.get("autori", "?")
            an = art.get("an", "?")
            titlu = art.get("titlu", "?")
            revista = art.get("revista", "?")
            doi = art.get("doi", "")
            doi_str = f" https://doi.org/{doi}" if doi else ""

            if format_ales == "APA":
                linii.append(f"[{i}] {autori} ({an}). {titlu}. *{revista}*.{doi_str}")
            elif format_ales == "IEEE":
                linii.append(f"[{i}] {autori}, \"{titlu},\" *{revista}*, {an}.{doi_str}")
            else:  # BibTeX
                cheie = re.sub(r"[^a-zA-Z0-9]", "", autori.split(",")[0]) + an
                linii.append(
                    f"@article{{{cheie},\n"
                    f"  author = {{{autori}}},\n"
                    f"  title = {{{titlu}}},\n"
                    f"  journal = {{{revista}}},\n"
                    f"  year = {{{an}}},\n"
                    f"  doi = {{{doi}}}\n}}"
                )

        bibliografie_finala = "\n\n".join(linii)
        st.text_area(f"Bibliografie {format_ales}:", bibliografie_finala, height=300, key="bib_final")

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                f"Descarca .txt ({format_ales})",
                data=bibliografie_finala.encode("utf-8"),
                file_name=f"bibliografie_{format_ales.lower()}_{datetime.date.today().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_dl2:
            if st.button("Sterge toate articolele", use_container_width=True, key="btn_sterge_art"):
                st.session_state["articole_gasite"] = []
                st.rerun()

        st.markdown("---")
        st.markdown("**Articole individuale:**")
        for i, art in enumerate(articole):
            culori_sursa = {"semantic_scholar": "#1a5276", "arxiv": "#c0392b", "crossref": "#8e44ad"}
            culoare = culori_sursa.get(art.get("sursa", ""), "#666")
            with st.expander(f"[{i+1}] {art['titlu'][:70]}...", expanded=False):
                st.markdown(f"""
<div style='font-size:11px; line-height:1.8;'>
<b>Autori:</b> {art['autori']} ({art['an']})<br>
<b>Revista:</b> {art['revista']}<br>
<b>DOI:</b> {art.get('doi','—')}<br>
<b>Sursa:</b> <span style='color:{culoare};'>{art.get('sursa','?')}</span>
</div>
""", unsafe_allow_html=True)
                if st.button(f"Sterge [{i+1}]", key=f"del_art_{i}"):
                    st.session_state["articole_gasite"].pop(i)
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Ziua 26 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### 3 baze de date gratuite — fara API key

**Semantic Scholar** (`api.semanticscholar.org`):
- 200+ milioane articole academice
- Filtrare dupa an, domeniu, nr. citatii
- Abstract inclus in API gratuit
- Limita: 100 cereri / 5 min (suficient)

**arXiv** (`export.arxiv.org/api/query`):
- Preprint-uri STEM (AI, fizica, biologie)
- Articole inainte de publicare formala
- Acces complet la PDF gratuit
- Fara limita de cereri

**CrossRef** (`api.crossref.org/works`):
- Metadate + DOI pentru orice articol publicat
- Numarul de citatii (`is-referenced-by-count`)
- Include reviste, carti, conferinte
- Recomandat: adauga `mailto:` in User-Agent

```python
# Pattern comun pentru toate 3:
r = requests.get(
    "https://api.BASE.org/endpoint",
    params={"query": "NDVI drone", "limit": 5},
    timeout=15,
)
data = r.json()
```
""")

    with col2:
        st.markdown("""
#### Impact pentru UCB si APIA

**Pentru un profesor UCB:**
- Bibliografie de 15 articole ISI: 2 min vs. 2 ore manual
- Verificare teme de licenta/doctorat: instant
- Monitorizare literatura noua pe un domeniu: saptamanal automat

**Pentru cercetare:**
- Agent cauta articole pentru un draft in pregatire
- Compara citarile ca indicator de calitate
- Identifica autorii cei mai activi intr-un domeniu

**Calitatea rezultatelor:**
- Semantic Scholar: cel mai complet pentru agricultură/AI
- arXiv: cel mai rapid (preprint-uri noi)
- CrossRef: cel mai precis pentru DOI-uri verificate
""")
        st.markdown("""
<div style='background:#e8f8f5; border-radius:8px; padding:12px; margin-top:10px;
     border-left:4px solid #16a085;'>
<div style='font-weight:700; color:#16a085;'>Nota academica importanta</div>
<div style='font-size:11px; color:#333; margin-top:6px; line-height:1.7;'>
Articolele gasite trebuie <b>verificate</b> inainte de a fi citate.<br>
Acceseaza DOI-ul si citeste abstract-ul complet.<br>
Nu cita niciodata un articol pe care nu l-ai citit.
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#16a085 0%,#1a5276 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 26 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
Semantic Scholar · arXiv · CrossRef · Agent ReAct bibliografie · APA / IEEE / BibTeX export
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 27 — Agent inspector APIA: analizeaza parcele din fisier
</div>
</div>
""", unsafe_allow_html=True)
