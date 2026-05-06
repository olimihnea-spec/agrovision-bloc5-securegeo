"""
Ziua 24 — Sinteza Modul 4: AI Generativ Local
Modul 4: AI Generativ Local
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import time

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

OLLAMA_URL = "http://localhost:11434"

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

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


def genereaza_ollama(model, prompt, system="", timeout=300):
    payload = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
        if r.status_code == 200:
            return True, r.json().get("response", "")
        return False, f"Eroare HTTP {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza — porneste cu: ollama serve"
    except Exception as e:
        return False, str(e)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 24 — Sinteza Modul 4",
    page_icon="M4",
    layout="wide",
    initial_sidebar_state="expanded"
)

ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#8e44ad;'>M4</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 24</div>
    <div style='font-size:11px; color:#666;'>Sinteza Modul 4 — AI Generativ</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI Generativ Local")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 24 / 30 zile")
st.sidebar.progress(24 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_selectat = st.sidebar.selectbox("Model:", modele_disponibile or ["llama3.2:latest"])
else:
    st.sidebar.warning("Ollama offline — mod demo")
    model_selectat = "llama3.2:latest"

st.sidebar.markdown("""
**Zilele din Modul 4:**
- Z19 — Ollama LLM local
- Z20 — Generator rapoarte APIA
- Z21 — Generare imagini (teorie)
- Z22 — Generator academic UCB
- Z23 — RAG: intreaba un PDF
- **Z24 — Sinteza** ← esti aici
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#8e44ad; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:38px; font-weight:900; color:#8e44ad;'>M4</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 24 — Sinteza Modul 4: AI Generativ Local
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Ollama · Rapoarte APIA · Imagini AI · Generator Academic · RAG PDF
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.info(
    "Modulul 4 este complet. Aceasta pagina recapituleaza toate instrumentele construite, "
    "prezinta un flux de lucru integrat si propune urmatoarele pasi catre Modulul 5."
)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Recapitulare Modul 4",
    "Flux integrat M4",
    "Autoevaluare",
    "Urmatoarele etape",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RECAPITULARE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Ce am construit in Modulul 4")

    zile_m4 = [
        {
            "zi": "Z19",
            "titlu": "Ollama — LLM Local",
            "culoare": "#6c3483",
            "icon": "LLM",
            "ce_am_invatat": [
                "Ollama ruleaza modele AI pe calculatorul tau — gratuit, offline, privat",
                "API REST simplu: POST /api/generate + POST /api/chat",
                "Modele disponibile: llama3.2:3B (~2GB), mistral:7B (~4GB), phi3:mini (~2GB)",
                "Integrare directa in Python cu requests",
                "Mod demo cu raspunsuri presetate cand Ollama nu ruleaza",
            ],
            "cod_cheie": 'requests.post("http://localhost:11434/api/generate",\n  json={"model":"llama3.2:latest","prompt":"...","stream":False})',
        },
        {
            "zi": "Z20",
            "titlu": "Generator Rapoarte APIA",
            "culoare": "#1a5276",
            "icon": "APIA",
            "ce_am_invatat": [
                "4 tipuri de rapoarte: control teren, conformitate NDVI, incident meteo, analiza lot",
                "calcul_penalizare(): praguri PAC — <3% fara penalizare, 3-20% penalizare=diferenta, >50% penalizare=100%",
                "LLM genereaza text profesional din date structurate (suprafata, NDVI, coordonate)",
                "Procesare lot: mai multe parcele dintr-un click",
                "Export .txt pentru arhivare APIA",
            ],
            "cod_cheie": 'def calcul_penalizare(dif_pct):\n  if dif_pct < 3: return "Fara penalizare", 0\n  elif dif_pct <= 20: return "Penalizare", dif_pct\n  ...',
        },
        {
            "zi": "Z21",
            "titlu": "Generare Imagini AI — Teorie",
            "culoare": "#e74c3c",
            "icon": "IMG",
            "ce_am_invatat": [
                "Stable Diffusion, DALL-E 3, Midjourney — arhitecturi si diferente",
                "Procesul: noise → denoising 20-50 pasi → imaginea finala",
                "Prompt engineering: subiect + stil + calitate + iluminare + unghi",
                "Instrumente gratuite: Ideogram (10/zi), Bing Creator (DALL-E 3 gratuit), Leonardo (150 credite/zi)",
                "De ce nu rulam local: min 4GB VRAM GPU — prea lent pe CPU",
            ],
            "cod_cheie": '# Prompt agricol exemplu:\n"aerial view wheat field Romania,\ndrone photography, golden hour,\nhigh resolution, professional"',
        },
        {
            "zi": "Z22",
            "titlu": "Generator Continut Academic",
            "culoare": "#1a5276",
            "icon": "UCB",
            "ce_am_invatat": [
                "5 tipuri materiale: suport curs, plan seminar, intrebari evaluare, rezumat bibliografic, fisa lucru",
                "System prompt specializat per tip — da rolul profesorului LLM-ului",
                "Generator lot: 4 materiale dintr-o singura apasare pentru o tema",
                "Streaming output — textul apare progresiv, fara timeout",
                "Economie estimata: 35-55 ore/semestru per disciplina",
            ],
            "cod_cheie": 'system = "Esti profesor UCB Targu Jiu, Master MRA."\nprompt = f"Genereaza suport curs pentru {disciplina},\ntema {tema}, nivel {nivel}. Max 350 cuvinte."',
        },
        {
            "zi": "Z23",
            "titlu": "RAG — Intreaba un PDF",
            "culoare": "#27ae60",
            "icon": "RAG",
            "ce_am_invatat": [
                "RAG = Retrieval-Augmented Generation: nu memorezi documentul, il cauti",
                "Pipeline: PDF → text → chunks (300 cuvinte, 60 overlap) → TF-IDF retrieval → LLM cu context",
                "TF-IDF gaseste top-3 chunk-uri relevante pentru fiecare intrebare",
                "LLM raspunde EXCLUSIV din context — nu inventeaza informatii",
                "Avantaj vs. fine-tuning: functioneaza pe orice document fara antrenare",
            ],
            "cod_cheie": 'chunks = chunking(text, size=300, overlap=60)\nrelevante = tfidf_retrieval(intrebare, chunks, top_k=3)\nraspuns = ollama(prompt + context_relevant)',
        },
    ]

    for zi in zile_m4:
        with st.expander(f"**{zi['zi']} — {zi['titlu']}**", expanded=False):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown(f"""
<div style='background:{zi["culoare"]}15; border-left:4px solid {zi["culoare"]};
     border-radius:4px; padding:10px 14px; margin-bottom:8px;'>
<div style='font-weight:700; color:{zi["culoare"]}; font-size:13px;'>{zi["zi"]} — {zi["titlu"]}</div>
</div>
""", unsafe_allow_html=True)
                for punct in zi["ce_am_invatat"]:
                    st.markdown(f"- {punct}")
            with col_b:
                st.markdown("**Cod cheie:**")
                st.code(zi["cod_cheie"], language="python")

    st.divider()

    # Statistici modul
    st.subheader("Modul 4 — statistici")
    c1, c2, c3, c4 = st.columns(4)
    kpi = """
<div style='background:white; border-radius:10px; padding:14px; text-align:center;
     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid {color};'>
    <div style='font-size:26px; font-weight:800; color:{color};'>{val}</div>
    <div style='font-size:11px; color:#666;'>{label}</div>
</div>"""
    with c1:
        st.markdown(kpi.format(color="#8e44ad", val="6", label="Zile finalizate"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi.format(color="#1a5276", val="5", label="Instrumente construite"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi.format(color="#27ae60", val="0€", label="Cost total"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi.format(color="#e74c3c", val="100%", label="Local / offline"), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FLUX INTEGRAT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Flux de lucru integrat — de la tema la material complet")
    st.markdown("""
Combina toate instrumentele din Modul 4 intr-un singur flux:
**PDF document → RAG intrebare → context → Generator academic → Material didactic**
""")

    col_flux1, col_flux2 = st.columns([1, 1])

    with col_flux1:
        st.markdown("**Configurare flux:**")
        disciplina_flux = st.selectbox(
            "Disciplina:",
            ["Managementul Riscului in Agricultura",
             "Politica Agricola Comuna (PAC)",
             "Drone si UAV in Agricultura",
             "Inteligenta Artificiala Aplicata"],
            key="disc_flux"
        )
        tema_flux = st.text_input(
            "Tema:",
            "Detectia neconformitatilor PAC cu drone si AI",
            key="tema_flux"
        )
        tip_material_flux = st.selectbox(
            "Material de generat:",
            ["Suport de curs (scurt)", "Intrebari de evaluare (5)", "Rezumat pentru studenti"],
            key="tip_flux"
        )

        if st.button("Lanseaza flux integrat M4", type="primary", use_container_width=True, key="btn_flux"):
            st.session_state["run_flux"] = True

    with col_flux2:
        st.markdown("**Diagrama flux:**")
        st.markdown("""
```
[1] SURSA — tema + disciplina definite
        |
        v
[2] RAG (Z23) — cauta in baza de cunostinte PAC
        |
        v
[3] CONTEXT — top-3 paragrafe relevante
        |
        v
[4] GENERATOR (Z22) — LLM + context + system prompt
        |
        v
[5] MATERIAL DIDACTIC — gata de descarcat
```
""")

    if st.session_state.get("run_flux"):
        st.session_state["run_flux"] = False
        st.markdown("---")

        # Baza cunostinte integrata
        baza_cunostinte = {
            "pac": "PAC 2023-2027: buget 387 miliarde EUR. Romania primeste ~10.4 miliarde EUR. "
                   "Platile directe = 70% din buget. Conditionalitate: respectarea normelor de mediu, "
                   "bunastarea animalelor, managementul terenurilor. IACS verifica conformitatea.",
            "ndvi": "NDVI (Normalized Difference Vegetation Index) = (NIR - RED) / (NIR + RED). "
                    "Valori: -1 la 0 = sol gol/apa, 0-0.3 = vegetatie slaba, 0.3-0.6 = vegetatie medie, "
                    "0.6-1 = vegetatie densa. Drone multispectrale calculeaza NDVI per parcela.",
            "penalizare": "Penalizari APIA: diferenta suprafata < 3% = fara penalizare, "
                          "3-20% = penalizare egala cu diferenta declarata, "
                          "> 20% = penalizare dubla, > 50% = excludere totala.",
            "drone": "Drone agricole: categorii EASA OPEN A1/A2/A3. Senzori: RGB, multispectral, termal. "
                     "Rezolutie tipica: 2-5 cm/pixel la 100m altitudine. "
                     "Aplicatii: NDVI, detectie daunatori, numarare plante, cartografiere parcele.",
        }

        # Step 1: RAG mock
        with st.status("Pasul 1/3 — RAG: caut informatii relevante...", expanded=True) as status:
            time.sleep(0.8)
            cuvinte_cheie = tema_flux.lower()
            context_rag = []
            for cheie, text in baza_cunostinte.items():
                if cheie in cuvinte_cheie or any(c in cuvinte_cheie for c in cheie.split()):
                    context_rag.append(text)
            if not context_rag:
                context_rag = list(baza_cunostinte.values())[:2]
            context_final = "\n\n".join(context_rag[:3])
            st.markdown(f"Gasit {len(context_rag)} paragrafe relevante din baza de cunostinte.")
            status.update(label="Pasul 1/3 — RAG: context extras", state="complete")

        # Step 2: Prompt
        with st.status("Pasul 2/3 — Construiesc promptul cu context...", expanded=True) as status:
            time.sleep(0.5)
            prompturi = {
                "Suport de curs (scurt)": (
                    f"Pe baza contextului de mai jos, genereaza un suport de curs SCURT (max 250 cuvinte) "
                    f"pentru disciplina '{disciplina_flux}', tema '{tema_flux}'.\n\n"
                    f"Include: 3 obiective, 3 concepte cheie, 1 exemplu practic.\n\n"
                    f"CONTEXT:\n{context_final}"
                ),
                "Intrebari de evaluare (5)": (
                    f"Pe baza contextului, genereaza 5 intrebari de evaluare pentru '{tema_flux}' "
                    f"la disciplina '{disciplina_flux}'. "
                    f"Include raspuns model de 2-3 randuri pentru fiecare.\n\n"
                    f"CONTEXT:\n{context_final}"
                ),
                "Rezumat pentru studenti": (
                    f"Pe baza contextului, scrie un rezumat de 200-250 cuvinte despre '{tema_flux}' "
                    f"pentru studenti de Master la '{disciplina_flux}'. "
                    f"Limbaj accesibil, structurat pe paragrafe scurte.\n\n"
                    f"CONTEXT:\n{context_final}"
                ),
            }
            prompt_ales = prompturi[tip_material_flux]
            system_ales = (
                "Esti profesor universitar la UCB Targu Jiu, Master Managementul Riscului in Agricultura. "
                "Generezi materiale didactice clare, in romana academica, bazate EXCLUSIV pe contextul furnizat."
            )
            st.markdown("Prompt construit cu context RAG integrat.")
            status.update(label="Pasul 2/3 — Prompt gata", state="complete")

        # Step 3: LLM generation
        with st.status("Pasul 3/3 — LLM genereaza materialul...", expanded=True) as status:
            if ollama_ok:
                ok, material = genereaza_ollama(model_selectat, prompt_ales, system_ales, timeout=240)
                if not ok:
                    material = f"[EROARE LLM] {material}"
                status.update(
                    label="Pasul 3/3 — Material generat de LLM",
                    state="complete" if ok else "error"
                )
            else:
                time.sleep(1.0)
                material = (
                    f"[MOD DEMO] {tip_material_flux.upper()}\n"
                    f"Disciplina: {disciplina_flux}\nTema: {tema_flux}\n\n"
                    "Context PAC integrat: platile directe reprezinta 70% din bugetul PAC, "
                    "verificate prin sistemul IACS. NDVI-ul calculat din imagini drone permite "
                    "detectia suprafetelor neconforme cu declaratia APIA.\n\n"
                    "Obiective:\n"
                    "1. Studentul va explica rolul NDVI in controlul PAC\n"
                    "2. Studentul va calcula penalizarile pentru neconformitati\n"
                    "3. Studentul va propune un flux de control cu drone\n\n"
                    "Concepte cheie: NDVI, IACS, LPIS, penalizare PAC, drone multispectral\n\n"
                    "*[Porneste Ollama pentru continut real generat de AI]*"
                )
                status.update(label="Pasul 3/3 — Material demo generat", state="complete")

        st.success(f"Flux complet! {tip_material_flux} generat pentru: **{tema_flux}**")

        st.markdown("**Rezultat flux integrat M4:**")
        st.markdown(
            f"<div style='background:#f8f9fa; border-radius:8px; padding:14px; "
            f"font-size:12px; line-height:1.8; font-family:monospace; "
            f"white-space:pre-wrap; border-left:4px solid #8e44ad;'>{material}</div>",
            unsafe_allow_html=True,
        )
        st.download_button(
            "Descarca material .txt",
            data=material.encode("utf-8"),
            file_name=f"flux_m4_{tema_flux[:15].replace(' ','_')}_{datetime.date.today().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — AUTOEVALUARE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Autoevaluare Modul 4 — AI Generativ Local")
    st.markdown("Verifica ce ai retinut din cele 6 zile ale Modulului 4.")

    intrebari = [
        {
            "q": "Ce port foloseste Ollama implicit pentru API-ul sau REST?",
            "optiuni": ["8080", "5000", "11434", "3000"],
            "corect": 2,
            "explicatie": "Ollama ruleaza la http://localhost:11434. Endpoint-ul de generare este /api/generate.",
        },
        {
            "q": "Care este pragul PAC sub care NU se aplica penalizare pentru diferenta de suprafata?",
            "optiuni": ["1%", "3%", "5%", "10%"],
            "corect": 1,
            "explicatie": "Daca diferenta intre suprafata declarata si cea masurata este < 3%, nu se aplica penalizare.",
        },
        {
            "q": "Ce inseamna RAG in contextul AI?",
            "optiuni": [
                "Rapid AI Generation",
                "Retrieval-Augmented Generation",
                "Random Answer Generator",
                "Recursive Algorithm Graph",
            ],
            "corect": 1,
            "explicatie": "RAG = Retrieval-Augmented Generation: modelul cauta context relevant in documente si raspunde bazat pe acesta.",
        },
        {
            "q": "De ce nu rulam Stable Diffusion local pe acest sistem?",
            "optiuni": [
                "Este prea scump",
                "Nu este open-source",
                "Necesita minim 4 GB VRAM GPU dedicat",
                "Nu functioneaza pe Windows",
            ],
            "corect": 2,
            "explicatie": "Stable Diffusion necesita GPU dedicat cu min 4GB VRAM. Pe CPU, o imagine dureaza 5-20 minute.",
        },
        {
            "q": "In RAG, ce rol are TF-IDF?",
            "optiuni": [
                "Genereaza textul final",
                "Chunking-ul documentului",
                "Selecteaza chunk-urile relevante pentru intrebare",
                "Compresia documentului PDF",
            ],
            "corect": 2,
            "explicatie": "TF-IDF calculeaza similaritatea intre intrebare si fiecare chunk, selectand top-k cele mai relevante.",
        },
    ]

    if "raspunsuri_m4" not in st.session_state:
        st.session_state["raspunsuri_m4"] = {}

    for i, item in enumerate(intrebari):
        st.markdown(f"**{i+1}. {item['q']}**")
        ales = st.radio(
            f"Raspuns {i+1}:",
            item["optiuni"],
            index=None,
            key=f"quiz_m4_{i}",
            label_visibility="collapsed",
        )
        if ales is not None:
            idx_ales = item["optiuni"].index(ales)
            if idx_ales == item["corect"]:
                st.success(f"Corect! {item['explicatie']}")
            else:
                st.error(f"Raspuns gresit. Corect: **{item['optiuni'][item['corect']]}**. {item['explicatie']}")
        st.markdown("")

    raspunsuri_completate = sum(
        1 for i in range(len(intrebari))
        if st.session_state.get(f"quiz_m4_{i}") is not None
    )
    raspunsuri_corecte = sum(
        1 for i, item in enumerate(intrebari)
        if st.session_state.get(f"quiz_m4_{i}") is not None
        and item["optiuni"].index(st.session_state[f"quiz_m4_{i}"]) == item["corect"]
    )

    if raspunsuri_completate == len(intrebari):
        scor = raspunsuri_corecte / len(intrebari)
        if scor >= 0.8:
            st.balloons()
            st.success(f"Scor: {raspunsuri_corecte}/{len(intrebari)} — Excelent! Modulul 4 este asimilat.")
        elif scor >= 0.6:
            st.warning(f"Scor: {raspunsuri_corecte}/{len(intrebari)} — Bine! Revizuieste zilele cu greseli.")
        else:
            st.error(f"Scor: {raspunsuri_corecte}/{len(intrebari)} — Revizuieste Modulul 4 inainte de a continua.")
    else:
        st.info(f"Completate: {raspunsuri_completate}/{len(intrebari)} intrebari")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — URMATOARELE ETAPE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Modulul 5 — AI Agenti + Finalizare")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
#### Ce urmeaza (Zilele 25-30)

| Zi | Tema |
|---|---|
| **Z25** | Agenti AI — automatizare cu LangChain |
| **Z26** | Agent cauta articole stiintifice automat |
| **Z27** | Agent inspector APIA — analizeaza parcele |
| **Z28** | Dashboard AI complet — toate instrumentele |
| **Z29** | Deploy pe Streamlit Cloud |
| **Z30** | Certificat final + roadmap AI 2026-2027 |

#### De ce agenti AI?

Un **agent AI** nu doar raspunde — el:
1. Primeste un obiectiv
2. Decide singur ce actiuni sa faca
3. Apeleaza instrumente (search, calcul, fisiere)
4. Verifica rezultatele
5. Repeta pana atinge obiectivul

Exemplu: *"Cauta ultimele 5 articole ISI despre drone agricole si
rezuma concluziile"* — agentul face tot singur.
""")

    with col2:
        st.markdown("""
#### Ce am construit pana acum — sinteza completa

**Modul 1 (Z1-Z6) — Machine Learning:**
scikit-learn · clasificare · regresie · clustering · pipeline

**Modul 2 (Z7-Z12) — Computer Vision:**
YOLOv8 · OpenCV · NDVI · detectie anomalii · OCR · contururi

**Modul 3 (Z13-Z18) — NLP:**
tokenizare · sentiment · Zero-Shot · rezumare · NER · pipeline

**Modul 4 (Z19-Z24) — AI Generativ:**
Ollama · rapoarte APIA · imagini AI · generator academic · RAG
""")

        st.markdown("""
<div style='background:#f0e6ff; border-radius:8px; padding:12px; margin-top:10px;
     border-left:4px solid #8e44ad;'>
<div style='font-weight:700; color:#8e44ad; font-size:13px;'>Progres total</div>
<div style='font-size:12px; color:#333; margin-top:6px; line-height:1.7;'>
24 zile finalizate din 30 — <b>80% complet</b><br>
4 module finalizate din 5<br>
Instrumentele construite ruleaza 100% local, 0 cost
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Badge Modul 4
    st.markdown("""
<div style='background:linear-gradient(135deg, #6c3483 0%, #1a5276 50%, #27ae60 100%);
     border-radius:12px; padding:20px 28px; color:white; margin-bottom:16px;'>
<div style='font-size:18px; font-weight:900; margin-bottom:8px;'>
    MODUL 4 FINALIZAT — AI Generativ Local
</div>
<div style='font-size:12px; opacity:0.9; line-height:1.8;'>
    Ollama LLM local &nbsp;·&nbsp;
    Generator rapoarte APIA &nbsp;·&nbsp;
    Imagini AI (teorie + instrumente) &nbsp;·&nbsp;
    Generator academic UCB &nbsp;·&nbsp;
    RAG Document PDF &nbsp;·&nbsp;
    Flux integrat M4
</div>
<div style='font-size:11px; margin-top:10px; opacity:0.75;'>
    Prof. Asoc. Dr. Oliviu Mihnea Gamulescu &nbsp;·&nbsp; UCB Targu Jiu &nbsp;·&nbsp;
    APIA CJ Gorj &nbsp;·&nbsp; 2026
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style='background:#fff3cd; border-radius:8px; padding:14px 18px;
     border-left:4px solid #f39c12;'>
<div style='font-weight:700; color:#856404;'>Urmatoarea: Ziua 25 — Agenti AI cu LangChain</div>
<div style='font-size:12px; color:#333; margin-top:6px; line-height:1.7;'>
Vom construi primul agent AI care primeste un obiectiv complex si il rezolva automat,
apeland instrumente multiple (LLM + search + fisiere) fara interventia utilizatorului.
</div>
</div>
""", unsafe_allow_html=True)
