"""
Ziua 25 — Agenti AI: ReAct manual + LangChain (100% gratuit)
Modul 5: AI Agenti + Finalizare
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import time
import json
import re

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# LangChain — optional (se instaleaza separat)
try:
    from langchain_community.llms import Ollama as LangChainOllama
    LANGCHAIN_OK = True
except ImportError:
    try:
        from langchain_ollama import OllamaLLM as LangChainOllama
        LANGCHAIN_OK = True
    except ImportError:
        LANGCHAIN_OK = False

OLLAMA_URL = "http://localhost:11434"

# ══════════════════════════════════════════════════════════════════════════════
# INSTRUMENTE AGENT (Tools) — 100% locale / gratuite
# ══════════════════════════════════════════════════════════════════════════════

def tool_calculator(expresie: str) -> str:
    """Evalueaza expresii matematice simple."""
    try:
        expresie_curata = re.sub(r"[^0-9+\-*/().% ]", "", expresie)
        rezultat = eval(expresie_curata, {"__builtins__": {}})
        return f"{rezultat:.4f}" if isinstance(rezultat, float) else str(rezultat)
    except Exception as e:
        return f"Eroare calcul: {e}"


def tool_ndvi(parametri: str) -> str:
    """Calculeaza NDVI din NIR si RED."""
    try:
        nir_match = re.search(r"NIR[=:\s]+([0-9.]+)", parametri, re.IGNORECASE)
        red_match = re.search(r"RED[=:\s]+([0-9.]+)", parametri, re.IGNORECASE)
        if not nir_match or not red_match:
            nums = re.findall(r"[0-9.]+", parametri)
            if len(nums) >= 2:
                nir, red = float(nums[0]), float(nums[1])
            else:
                return "Format: NIR=0.8, RED=0.3"
        else:
            nir, red = float(nir_match.group(1)), float(red_match.group(1))
        if (nir + red) == 0:
            return "Eroare: NIR + RED = 0"
        ndvi = (nir - red) / (nir + red)
        if ndvi < 0:
            interpretare = "Apa sau sol inundat"
        elif ndvi < 0.2:
            interpretare = "Sol gol sau vegetatie foarte slaba"
        elif ndvi < 0.4:
            interpretare = "Vegetatie slaba sau culturi in crestere"
        elif ndvi < 0.6:
            interpretare = "Vegetatie medie — culturi sanatoase"
        else:
            interpretare = "Vegetatie densa — culturi excelente"
        return f"NDVI = {ndvi:.4f} | {interpretare} (NIR={nir}, RED={red})"
    except Exception as e:
        return f"Eroare NDVI: {e}"


def tool_penalizare_pac(diferenta_str: str) -> str:
    """Calculeaza penalizarea PAC pentru o diferenta de suprafata."""
    try:
        nums = re.findall(r"[0-9.]+", diferenta_str)
        if not nums:
            return "Trimite procentul diferentei, ex: 8.5"
        dif = float(nums[0])
        if dif < 3:
            return f"Diferenta {dif}% — SUB PRAG: nicio penalizare."
        elif dif <= 20:
            return (f"Diferenta {dif}% — PENALIZARE REDUSA: "
                    f"se deduce {dif:.1f}% din plata.")
        elif dif <= 50:
            return (f"Diferenta {dif}% — PENALIZARE DUBLA: "
                    f"se deduce {2*dif:.1f}% din plata (pana la 100%).")
        else:
            return f"Diferenta {dif}% — EXCLUDERE TOTALA: plata = 0 EUR pentru aceasta parcela."
    except Exception as e:
        return f"Eroare calcul penalizare: {e}"


def tool_duckduckgo(interogare: str) -> str:
    """Cauta informatii cu DuckDuckGo Instant Answer API (gratuit, fara cheie)."""
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": interogare, "format": "json", "no_html": "1", "skip_disambig": "1"},
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        data = r.json()
        abstract = data.get("AbstractText", "")
        if abstract:
            return abstract[:600]
        topics = data.get("RelatedTopics", [])
        for t in topics:
            if isinstance(t, dict) and t.get("Text"):
                return t["Text"][:600]
        return "Niciun rezultat instant. Incearca o alta interogare."
    except requests.exceptions.ConnectionError:
        return "Fara conexiune internet."
    except Exception as e:
        return f"Cautare esuata: {e}"


TOOLS = {
    "calculator": {
        "functie": tool_calculator,
        "descriere": "Evalueaza expresii matematice: adunare, scadere, inmultire, impartire. Ex: '3.5 * 120 * 0.85'",
    },
    "ndvi": {
        "functie": tool_ndvi,
        "descriere": "Calculeaza NDVI si interpreteaza sanatatea vegetatiei. Ex: 'NIR=0.76, RED=0.12'",
    },
    "penalizare": {
        "functie": tool_penalizare_pac,
        "descriere": "Calculeaza penalizarea PAC pentru diferenta de suprafata (%). Ex: '8.5'",
    },
    "cautare": {
        "functie": tool_duckduckgo,
        "descriere": "Cauta informatii online cu DuckDuckGo (gratuit). Ex: 'NDVI agricultura Romania'",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# MOTOR ReAct MANUAL
# ══════════════════════════════════════════════════════════════════════════════

REACT_SYSTEM = """Esti un asistent AI specializat in agricultura si politici europene (PAC/APIA).
Rezolvi probleme pas cu pas folosind instrumente.

Raspunde INTOTDEAUNA in formatul urmator:

Thought: [analiza ta despre ce trebuie sa faci]
Action: [unul din: calculator | ndvi | penalizare | cautare | raspuns_direct]
Action Input: [inputul exact pentru instrument]

SAU, cand ai raspunsul complet:
Thought: Am toate informatiile pentru a raspunde.
Final Answer: [raspunsul complet si clar]

Instrumente disponibile:
- calculator: expresii matematice (ex: "235 * 0.85")
- ndvi: calculeaza NDVI (ex: "NIR=0.76, RED=0.12")
- penalizare: penalizare PAC din diferenta % (ex: "12.3")
- cautare: cauta online cu DuckDuckGo (ex: "PAC 2023 Romania plati directe")
- raspuns_direct: cand stii deja raspunsul fara instrumente

IMPORTANT: Nu inventa valori. Daca nu stii, foloseste cautarea sau spune ca nu ai informatii.
"""


def parseaza_reactie(text: str):
    """Extrage Action si Action Input din raspunsul LLM."""
    final = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL | re.IGNORECASE)
    if final:
        return "final", final.group(1).strip()

    action = re.search(r"Action:\s*(\w+)", text, re.IGNORECASE)
    action_input = re.search(r"Action Input:\s*(.+?)(?=\n|$)", text, re.DOTALL | re.IGNORECASE)

    if action:
        tool_name = action.group(1).strip().lower()
        tool_input = action_input.group(1).strip() if action_input else ""
        return tool_name, tool_input

    return "necunoscut", text[:200]


def ruleaza_agent(intrebare: str, model: str, max_pasi: int = 5, container=None):
    """Ruleaza agentul ReAct si returneaza pasii si raspunsul final."""
    pasi = []
    tools_desc = "\n".join(f"- {n}: {t['descriere']}" for n, t in TOOLS.items())
    system_complet = REACT_SYSTEM.replace(
        "Instrumente disponibile:", f"Instrumente disponibile:\n{tools_desc}\n\nInstrumente disponibile (lista):"
    )

    mesaj_curent = (
        f"Intrebare: {intrebare}\n\n"
        "Rezolva pas cu pas. Incepe cu Thought:"
    )
    istoric = ""

    for pas in range(1, max_pasi + 1):
        prompt_complet = mesaj_curent if pas == 1 else f"{mesaj_curent}\n\n{istoric}"

        if container:
            container.info(f"Pas {pas}/{max_pasi} — LLM gandeste...")

        if REQUESTS_OK:
            try:
                r = requests.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={"model": model, "prompt": prompt_complet, "system": system_complet,
                          "stream": False, "options": {"temperature": 0.1}},
                    timeout=90,
                )
                if r.status_code == 200:
                    raspuns_llm = r.json().get("response", "")
                else:
                    raspuns_llm = f"Eroare HTTP {r.status_code}"
            except Exception as e:
                raspuns_llm = f"Eroare Ollama: {e}"
        else:
            raspuns_llm = "Final Answer: Ollama nu este disponibil."

        tip_actiune, valoare = parseaza_reactie(raspuns_llm)

        if tip_actiune == "final":
            pasi.append({"pas": pas, "tip": "final", "thought": raspuns_llm, "raspuns": valoare})
            return pasi, valoare

        if tip_actiune in TOOLS:
            observatie = TOOLS[tip_actiune]["functie"](valoare)
        elif tip_actiune == "raspuns_direct":
            pasi.append({"pas": pas, "tip": "final", "thought": raspuns_llm, "raspuns": valoare})
            return pasi, valoare
        else:
            observatie = f"Instrument '{tip_actiune}' necunoscut. Alege din: {', '.join(TOOLS.keys())}."

        pasi.append({
            "pas": pas,
            "tip": "actiune",
            "thought": raspuns_llm,
            "actiune": tip_actiune,
            "input": valoare,
            "observatie": observatie,
        })

        istoric += f"\n{raspuns_llm}\nObservation: {observatie}\n"

    return pasi, "Agentul nu a gasit raspunsul in limita de pasi. Incearca sa reformulezi intrebarea."


# ══════════════════════════════════════════════════════════════════════════════
# DEMO RASPUNSURI (cand Ollama offline)
# ══════════════════════════════════════════════════════════════════════════════

DEMO_AGENT = {
    "ndvi": [
        {"pas": 1, "tip": "actiune", "actiune": "ndvi", "input": "NIR=0.78, RED=0.14",
         "observatie": "NDVI = 0.6957 | Vegetatie densa — culturi excelente (NIR=0.78, RED=0.14)",
         "thought": "Thought: Trebuie sa calculez NDVI din valorile date.\nAction: ndvi\nAction Input: NIR=0.78, RED=0.14"},
        {"pas": 2, "tip": "final",
         "thought": "Thought: Am rezultatul NDVI, pot formula raspunsul final.",
         "raspuns": "NDVI = 0.70 indica vegetatie densa si culturi sanatoase. Parcela nu prezinta risc de neconformitate."},
    ],
    "penalizare": [
        {"pas": 1, "tip": "actiune", "actiune": "penalizare", "input": "12.5",
         "observatie": "Diferenta 12.5% — PENALIZARE REDUSA: se deduce 12.5% din plata.",
         "thought": "Thought: Calculez penalizarea PAC pentru diferenta de 12.5%.\nAction: penalizare\nAction Input: 12.5"},
        {"pas": 2, "tip": "actiune", "actiune": "calculator", "input": "850 * 0.125",
         "observatie": "106.2500",
         "thought": "Thought: Acum calculez suma in EUR care se deduce.\nAction: calculator\nAction Input: 850 * 0.125"},
        {"pas": 3, "tip": "final",
         "thought": "Thought: Am toate calculele. Formulez raspunsul.",
         "raspuns": "Diferenta de 12.5% depaseste pragul de 3%. Penalizare: 12.5% din plata. "
                    "Pentru o plata de 850 EUR, se deduce 106.25 EUR. Plata finala: 743.75 EUR."},
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 25 — Agenti AI",
    page_icon="AGT",
    layout="wide",
    initial_sidebar_state="expanded"
)


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


ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#c0392b;'>AGT</div>
    <div style='font-size:16px; font-weight:700; color:#c0392b;'>ZIUA 25</div>
    <div style='font-size:11px; color:#666;'>Agenti AI — ReAct + LangChain</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 5 — AI Agenti + Finalizare")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 25 / 30 zile")
st.sidebar.progress(25 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_ales = st.sidebar.selectbox("Model:", modele_disponibile or ["llama3.2:latest"])
else:
    st.sidebar.warning("Ollama offline — mod demo")
    model_ales = "llama3.2:latest"

st.sidebar.markdown(f"""
**LangChain:** {"instalat" if LANGCHAIN_OK else "neinstalat (optional)"}

**Instrumente agent:**
- calculator — matematica
- ndvi — vegetatie drone
- penalizare — PAC APIA
- cautare — DuckDuckGo
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#c0392b; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:38px; font-weight:900; color:#c0392b;'>AGT</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#c0392b; font-weight:800;'>
            Ziua 25 — Agenti AI: ReAct manual + LangChain
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            ReAct · Ollama local · DuckDuckGo gratuit · NDVI · Penalizari PAC
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

if not ollama_ok:
    st.warning("Ollama offline — mod demo activ. Porneste `ollama serve` pentru agent real.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoria agentilor",
    "Agent ReAct — demo",
    "Instrumente",
    "LangChain — teorie",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIA AGENTILOR
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ce este un agent AI?")
        st.markdown("""
Un **agent AI** nu este un chatbot care raspunde si asteapta.
Agentul primeste un **obiectiv** si actioneaza autonom:

1. **Analizeaza** problema
2. **Decide** ce instrument sa foloseasca
3. **Executa** instrumentul
4. **Citeste** rezultatul
5. **Repeta** pana rezolva obiectivul

**Diferenta fata de un simplu LLM:**

| LLM simplu | Agent AI |
|---|---|
| Raspunde din memorie | Cauta informatii reale |
| Un singur pas | Multi-step (plan → actiune → verificare) |
| Poate inventa date | Foloseste instrumente pentru date reale |
| Stie doar ce a invatat | Extinde cunoasterea prin tools |

**Exemplu concret:**
Intrebare: *"Care este penalizarea pentru parcela X cu NDVI 0.15 si diferenta de suprafata 8.5%?"*

- LLM simplu: inventeaza un raspuns plauzibil
- Agent: calculeaza NDVI → interpreteaza → calculeaza penalizare → combina raspunsul
""")

    with col2:
        st.subheader("Patternul ReAct")
        st.markdown("""
**ReAct = Reasoning + Acting** (Yao et al., 2022)

Bucla unui agent ReAct:
```
Thought:  Ce trebuie sa fac?
Action:   [numele instrumentului]
Action Input: [parametrii]
Observation: [rezultatul instrumentului]
... (se repeta pana la)
Thought:  Am raspunsul.
Final Answer: [raspunsul complet]
```

**Exemplu real (agentul din aceasta pagina):**
```
Intrebare: "Calculeaza NDVI pentru NIR=0.76, RED=0.18"

Thought: Trebuie sa calculez NDVI.
Action: ndvi
Action Input: NIR=0.76, RED=0.18
Observation: NDVI = 0.6154 | Vegetatie medie

Thought: Am rezultatul, pot raspunde.
Final Answer: NDVI = 0.62 — vegetatie medie,
culturi sanatoase dar cu potential de imbunatatire.
```

**De ce ReAct?**
- Transparent: vezi exact ce gandeste agentul
- Verificabil: fiecare pas e traceable
- Robust: daca un tool esueaza, agentul alege altul
""")

    st.divider()
    st.subheader("Arhitectura agentului din aceasta pagina")
    st.markdown("""
```
┌─────────────────────────────────────────────────────────┐
│                    AGENT ReAct (Z25)                     │
│                                                          │
│  Intrebare → [LLM Ollama local]                          │
│                    │                                     │
│              Thought + Action                            │
│                    │                                     │
│        ┌──────────────────────┐                          │
│        │    DISPATCHER        │                          │
│        │  (parseaza actiunea) │                          │
│        └──────────────────────┘                          │
│                    │                                     │
│     ┌──────┬───────┼────────┬──────────┐                 │
│  calc  ndvi  penalizare  cautare  raspuns_direct          │
│  (local)(local) (local)  (DDG API)  (direct)              │
│     └──────┴───────┴────────┴──────────┘                 │
│                    │                                     │
│              Observation → LLM → urmator pas             │
│                    │                                     │
│              Final Answer                                │
└─────────────────────────────────────────────────────────┘
```

**Cost total: 0 EUR** — Ollama local + DuckDuckGo gratuit + instrumente Python
""")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DEMO AGENT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Agent ReAct — demonstratie live")

    intrebari_exemple = [
        "Calculeaza NDVI pentru NIR=0.78 si RED=0.14. Ce inseamna?",
        "O parcela are diferenta de suprafata de 12.5% si plata de 850 EUR. Care e penalizarea si suma finala?",
        "Ce este PAC 2023-2027? Cauta online.",
        "Calculeaza: 47.3 hectare * 253 EUR/ha. Aplica o reducere de 15%.",
        "Parcela are NIR=0.31, RED=0.28. Calculeaza NDVI si spune daca e nevoie de interventie.",
    ]

    col_intrebare, col_settings = st.columns([2, 1])
    with col_intrebare:
        intrebare_custom = st.text_area(
            "Intrebare pentru agent:",
            value=intrebari_exemple[0],
            height=80,
            key="intrebare_agent"
        )
    with col_settings:
        max_pasi_ales = st.slider("Pasi max:", 2, 6, 4, key="max_steps_agent")
        st.markdown(f"**Model:** {model_ales}")
        arata_pasi = st.checkbox("Arata toti pasii ReAct", value=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        ruleaza = st.button("Lanseaza agentul", type="primary", use_container_width=True, key="btn_agent")
    with col_btn2:
        if st.button("Alege exemplu aleator", use_container_width=True, key="btn_exemplu"):
            import random
            st.session_state["intrebare_agent"] = random.choice(intrebari_exemple)
            st.rerun()

    st.markdown("**Exemple rapide:**")
    cols_ex = st.columns(len(intrebari_exemple))
    for i, (col_ex, ex) in enumerate(zip(cols_ex, intrebari_exemple)):
        with col_ex:
            if st.button(f"Ex {i+1}", key=f"ex_btn_{i}", use_container_width=True):
                st.session_state["intrebare_agent"] = ex
                st.rerun()

    if ruleaza and intrebare_custom.strip():
        st.markdown("---")
        st.markdown(f"**Intrebare:** {intrebare_custom}")

        progress_container = st.empty()

        if ollama_ok:
            with st.spinner("Agentul ruleaza..."):
                pasi_agent, raspuns_final = ruleaza_agent(
                    intrebare_custom, model_ales, max_pasi_ales, progress_container
                )
            progress_container.empty()
        else:
            time.sleep(1.0)
            progress_container.empty()
            cuvinte = intrebare_custom.lower()
            if "ndvi" in cuvinte:
                pasi_agent = DEMO_AGENT["ndvi"]
                raspuns_final = DEMO_AGENT["ndvi"][-1]["raspuns"]
            else:
                pasi_agent = DEMO_AGENT["penalizare"]
                raspuns_final = DEMO_AGENT["penalizare"][-1]["raspuns"]

        if arata_pasi:
            st.markdown("**Traseul agentului (ReAct):**")
            for pas_info in pasi_agent:
                culoare_pas = "#27ae60" if pas_info["tip"] == "final" else "#2980b9"
                icon_pas = "FINAL" if pas_info["tip"] == "final" else f"PAS {pas_info['pas']}"

                with st.expander(
                    f"{icon_pas} — {'Raspuns final' if pas_info['tip'] == 'final' else pas_info.get('actiune','?').upper()}",
                    expanded=True
                ):
                    thought_text = pas_info.get("thought", "")
                    thought_lines = [l for l in thought_text.split("\n") if l.startswith("Thought:")]
                    if thought_lines:
                        st.markdown(f"*{thought_lines[0]}*")

                    if pas_info["tip"] == "actiune":
                        col_act1, col_act2 = st.columns(2)
                        with col_act1:
                            st.markdown(f"""
<div style='background:#e8f4fd; border-radius:6px; padding:8px 12px; font-size:11px;'>
<b>Instrument:</b> {pas_info.get('actiune','')}<br>
<b>Input:</b> {pas_info.get('input','')}
</div>
""", unsafe_allow_html=True)
                        with col_act2:
                            st.markdown(f"""
<div style='background:#e9f7ef; border-radius:6px; padding:8px 12px; font-size:11px;'>
<b>Observatie:</b><br>{pas_info.get('observatie','')}
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div style='background:linear-gradient(135deg, #c0392b 0%, #8e44ad 100%);
     border-radius:10px; padding:16px 20px; color:white; margin-top:12px;'>
<div style='font-size:12px; opacity:0.8; margin-bottom:4px;'>RASPUNS FINAL AGENT</div>
<div style='font-size:14px; font-weight:600; line-height:1.7;'>{raspuns_final}</div>
</div>
""", unsafe_allow_html=True)

        nr_pasi_reali = len([p for p in pasi_agent if p["tip"] == "actiune"])
        st.caption(f"Agent finalizat in {len(pasi_agent)} pasi | {nr_pasi_reali} instrumente apelate")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — INSTRUMENTE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Instrumente disponibile — testa-le direct")

    col_tool1, col_tool2 = st.columns(2)

    with col_tool1:
        st.markdown("**Calculator**")
        expr_test = st.text_input("Expresie:", "47.3 * 253 * 0.85", key="calc_test")
        if st.button("Calculeaza", key="btn_calc"):
            st.success(f"Rezultat: {tool_calculator(expr_test)}")

        st.markdown("---")
        st.markdown("**NDVI Calculator**")
        nir_test = st.slider("NIR:", 0.0, 1.0, 0.78, 0.01, key="nir_sl")
        red_test = st.slider("RED:", 0.0, 1.0, 0.14, 0.01, key="red_sl")
        if st.button("Calculeaza NDVI", key="btn_ndvi"):
            rez_ndvi = tool_ndvi(f"NIR={nir_test}, RED={red_test}")
            st.success(rez_ndvi)
            ndvi_val = (nir_test - red_test) / (nir_test + red_test) if (nir_test + red_test) > 0 else 0
            st.progress(max(0.0, min(1.0, (ndvi_val + 1) / 2)))

    with col_tool2:
        st.markdown("**Penalizare PAC**")
        dif_test = st.slider("Diferenta suprafata (%):", 0.0, 60.0, 8.5, 0.5, key="dif_sl")
        if st.button("Calculeaza penalizare", key="btn_pen"):
            st.info(tool_penalizare_pac(str(dif_test)))

        st.markdown("---")
        st.markdown("**Cautare DuckDuckGo** (necesita internet)")
        query_test = st.text_input("Interogare:", "PAC 2023 Romania plati directe", key="ddg_test")
        if st.button("Cauta online", key="btn_ddg"):
            with st.spinner("Cautare..."):
                rez_ddg = tool_duckduckgo(query_test)
            st.info(rez_ddg)

    st.divider()
    st.subheader("Adauga un instrument nou — cum se face")
    st.code("""
# Orice functie Python devine un instrument al agentului
def tool_convertor_ha(text: str) -> str:
    \"\"\"Converteste suprafata intre hectare si mp.\"\"\"
    nums = re.findall(r"[0-9.]+", text)
    if not nums:
        return "Ex: '3.5 ha' sau '35000 mp'"
    val = float(nums[0])
    if "ha" in text.lower():
        return f"{val} ha = {val * 10000:.0f} mp"
    return f"{val} mp = {val / 10000:.4f} ha"

# Inregistreaza in dictionar
TOOLS["convertor_ha"] = {
    "functie": tool_convertor_ha,
    "descriere": "Converteste ha <-> mp. Ex: '3.5 ha'"
}

# Agentul il va folosi automat cand intrebarea cere conversii de suprafata
""", language="python")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — LANGCHAIN TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("LangChain — framework oficial pentru agenti AI")

    if LANGCHAIN_OK:
        st.success("LangChain este instalat pe acest sistem.")
    else:
        st.info("LangChain nu este instalat. Instaleaza cu: `pip install langchain langchain-community langchain-ollama`")

    col_lc1, col_lc2 = st.columns(2)

    with col_lc1:
        st.markdown("""
#### Ce este LangChain?

LangChain este un framework open-source care simplifica
constructia de agenti AI si aplicatii cu LLM-uri.

**Componente principale:**
- **LLMs** — interfata unificata pentru orice model
- **Tools** — instrumente pe care agentul le poate apela
- **Agents** — motorul de decizie (ReAct, OpenAI Functions, etc.)
- **Chains** — secvente de pasi predefinite
- **Memory** — memorie conversationala
- **VectorStores** — baze de cunostinte pentru RAG

**De ce LangChain in loc de cod manual?**
- Ecosistem mare: 200+ instrumente gata facute
- Abstractie: schimbi LLM-ul fara sa rescrii tot
- Comunitate activa: actualizari frecvente
""")

    with col_lc2:
        st.markdown("**Echivalentul agentului nostru ReAct in LangChain:**")
        st.code("""
# pip install langchain langchain-community langchain-ollama
from langchain_ollama import OllamaLLM
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain import hub

# 1. LLM local gratuit
llm = OllamaLLM(model="llama3.2:latest")

# 2. Instrumente
tools = [
    Tool(name="calculator",
         func=tool_calculator,
         description="Evalueaza expresii matematice"),
    Tool(name="ndvi",
         func=tool_ndvi,
         description="Calculeaza NDVI din NIR si RED"),
    Tool(name="penalizare",
         func=tool_penalizare_pac,
         description="Penalizare PAC din diferenta %"),
]

# 3. Prompt ReAct (de pe hub.langchain.com)
prompt = hub.pull("hwchase17/react")

# 4. Agent
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Ruleaza
rezultat = executor.invoke({
    "input": "Calculeaza penalizarea pentru diferenta 8.5%"
})
print(rezultat["output"])
""", language="python")

    st.divider()
    st.markdown("**Comparatie: ReAct manual vs. LangChain**")
    st.markdown("""
| Criteriu | ReAct manual (Z25) | LangChain |
|---|---|---|
| Instalare | Doar `requests` | 5+ pachete, ~500MB |
| Transparenta | Cod 100% al tau | Framework black-box |
| Flexibilitate | Modifici orice | Constrans de API |
| Ecosistem | Doar ce scrii | 200+ tools gata |
| Stabilitate API | Stabil (codul tau) | Se schimba frecvent |
| Recomandat pentru | Invatare, proiecte mici | Productie, complexitate mare |

**Concluzie:** Intelegi ReAct manual → folosesti LangChain eficient.
""")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ziua 25 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### Concepte noi

**ReAct pattern:**
```
Thought → Action → Observation → (repeta) → Final Answer
```

**Dispatcher de instrumente:**
```python
TOOLS = {
    "ndvi": {"functie": tool_ndvi, "descriere": "..."},
    "calc": {"functie": tool_calculator, "descriere": "..."},
}
# Agentul alege singur ce tool sa apeleze
tip, val = parseaza_reactie(raspuns_llm)
observatie = TOOLS[tip]["functie"](val)
```

**DuckDuckGo Instant Answer API:**
```python
requests.get("https://api.duckduckgo.com/",
    params={"q": query, "format": "json"})
# Gratuit, fara cont, fara API key
```

**Temperature scazuta pentru agenti:**
```python
"options": {"temperature": 0.1}
# Mai deterministic = comportament predictibil
```
""")
    with col2:
        st.markdown("""
#### Aplicatii concrete APIA / UCB

**Agent inspector APIA (Z27):**
- Citeste CSV cu parcele
- Calculeaza NDVI per parcela
- Aplica reguli PAC
- Genereaza raport de neconformitati automat

**Agent cautare articole (Z26):**
- Primeste o tema de cercetare
- Cauta articole relevante online
- Rezuma abstract-urile
- Propune bibliografie structurata

**Economie reala:**
- Inspector APIA: 30 parcele analizate in 2 min vs. 3 ore manual
- Profesor UCB: bibliografie pentru un curs in 5 min vs. 2 ore
""")
        st.markdown("""
<div style='background:#fdecea; border-radius:8px; padding:12px; margin-top:10px;
     border-left:4px solid #c0392b;'>
<div style='font-weight:700; color:#c0392b;'>Limitare importanta</div>
<div style='font-size:11px; color:#333; margin-top:6px; line-height:1.7;'>
Modelele mici (3B parametri) pot gresi formatul ReAct.
Mistral 7B sau Llama 3.1 8B sunt mai fiabile pentru agenti.
Intotdeauna verifica raspunsul final inainte de a-l folosi.
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#c0392b 0%,#8e44ad 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 25 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
ReAct pattern · Motor agent manual · 4 instrumente · DuckDuckGo gratuit · LangChain teorie
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 26 — Agent care cauta articole stiintifice automat
</div>
</div>
""", unsafe_allow_html=True)
