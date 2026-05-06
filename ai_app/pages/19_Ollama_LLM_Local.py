"""
Ziua 19 — Ollama: Modele LLM Locale (Llama 3, Mistral) Gratuit
Modul 4: AI Generativ Local
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import json
import time

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

OLLAMA_URL = "http://localhost:11434"

# ── Constante ──────────────────────────────────────────────────────────────────
MODELE_RECOMANDATE = [
    ("llama3.2:3b",  "Llama 3.2 3B",  "~2 GB",  "Rapid, ideal incepatori"),
    ("llama3.2:1b",  "Llama 3.2 1B",  "~1.3 GB","Cel mai rapid, RAM minim"),
    ("mistral:7b",   "Mistral 7B",    "~4.1 GB","Echilibru calitate/viteza"),
    ("phi3:mini",    "Phi-3 Mini",    "~2.3 GB","Microsoft, excelent cod"),
    ("gemma2:2b",    "Gemma 2 2B",    "~1.6 GB","Google, bun si usor"),
]

DEMO_RASPUNSURI = {
    "raport": """Raport de control pe teren — generat automat

Inspector: agent AI local (demo)
Data: {data}

In urma analizei datelor furnizate, parcela prezinta o suprafata eligibila
de {suprafata} hectare, cultura {cultura}.

Starea fitosanitara este buna, fara neconformitati majore identificate.
Indicele NDVI mediu calculat din imaginile satelitare este de 0.62,
ceea ce indica o vegetatie sanatoasa si o productie estimata normala.

Recomandare: dosarul poate fi procesat pentru plata subventiei PAC.
Termen estimat de plata: 30 zile lucratoare.

Semnat: Inspector AI | APIA CJ Gorj""",

    "analiza": """Analiza document APIA — Rezumat executiv

Documentul analizat contine urmatoarele elemente cheie:
- Fermier identificat cu suprafata totala declarata
- Culturi in conformitate cu normele PAC 2023-2027
- Nu s-au identificat neconformitati majore
- Subventia estimata se incadreaza in limitele normale

Concluzie: documentul este complet si poate fi procesat.""",

    "chat": """Buna ziua! Sunt un asistent AI local care ruleaza pe calculatorul dumneavoastra,
fara conexiune la internet. Pot sa va ajut cu:

- Redactarea rapoartelor APIA
- Analiza documentelor agricole
- Explicarea regulamentelor PAC
- Calcule de subventii
- Informatii despre culturi agricole

Cum va pot ajuta astazi?""",
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII OLLAMA
# ══════════════════════════════════════════════════════════════════════════════

def verifica_ollama() -> tuple[bool, list]:
    """Returneaza (disponibil, lista_modele)."""
    if not REQUESTS_OK:
        return False, []
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if r.status_code == 200:
            modele = [m["name"] for m in r.json().get("models", [])]
            return True, modele
    except Exception:
        pass
    return False, []


def genereaza_ollama(model: str, prompt: str, system: str = "") -> tuple[bool, str]:
    """Apeleaza Ollama /api/generate. Returneaza (succes, raspuns)."""
    if not REQUESTS_OK:
        return False, "requests nu este instalat."
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        if r.status_code == 200:
            return True, r.json().get("response", "")
        return False, f"Eroare HTTP {r.status_code}: {r.text[:200]}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza. Porneste cu: ollama serve"
    except requests.exceptions.Timeout:
        return False, "Timeout — modelul ia prea mult. Incearca un model mai mic."
    except Exception as e:
        return False, str(e)


def chat_ollama(model: str, mesaje: list) -> tuple[bool, str]:
    """Apeleaza Ollama /api/chat cu istoric conversatie."""
    if not REQUESTS_OK:
        return False, "requests nu este instalat."
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": mesaje, "stream": False},
            timeout=120
        )
        if r.status_code == 200:
            return True, r.json()["message"]["content"]
        return False, f"Eroare HTTP {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza. Porneste cu: ollama serve"
    except Exception as e:
        return False, str(e)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 19 — Ollama LLM Local",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🦙</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 19</div>
    <div style='font-size:11px; color:#666;'>Ollama — LLM Local Gratuit</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI Generativ Local")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 19 / 30 zile")
st.sidebar.progress(19 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    if modele_disponibile:
        model_selectat = st.sidebar.selectbox("Model activ:", modele_disponibile)
    else:
        st.sidebar.warning("Niciun model instalat.\nRuleaza: ollama pull llama3.2")
        model_selectat = "llama3.2:3b"
else:
    st.sidebar.error("Ollama offline")
    st.sidebar.info("Ruleaza: ollama serve")
    model_selectat = "llama3.2:3b"

st.sidebar.markdown("""
**Comenzi utile:**
```
ollama serve
ollama pull llama3.2
ollama pull mistral
ollama list
```
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#8e44ad; border-radius:8px; padding:10px 12px; color:white; font-size:10px; line-height:1.7;'>
<div style='font-size:11px; font-weight:900; margin-bottom:6px;'>&copy; 2026 Proprietate intelectuala</div>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj<br>
<b>Curs:</b> Master Managementul Riscului in Agricultura
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🦙</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 19 — Ollama: LLM Local Gratuit
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Llama 3 · Mistral · Phi-3 · Gemma — ruleaza pe calculatorul tau, fara internet, fara cost
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

if ollama_ok:
    st.success(
        f"Ollama ruleaza local | Model selectat: **{model_selectat}** | "
        f"Modele disponibile: {', '.join(modele_disponibile) or 'niciun model instalat'}"
    )
else:
    st.warning(
        "Ollama nu este pornit — aplicatia ruleaza in **modul demo**. "
        "Instaleaza Ollama de la https://ollama.com si ruleaza `ollama serve` pentru AI real."
    )

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teorie & Instalare",
    "Chat cu LLM",
    "Generator Rapoarte APIA",
    "Comparatie Modele",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Ce este Ollama?")
        st.markdown("""
Ollama este un instrument **gratuit, open-source** care iti permite sa rulezi modele LLM mari
(Large Language Models) direct pe calculatorul tau, fara internet si fara costuri de API.

**Avantaje fata de ChatGPT / Claude API:**
| Criteriu | Ollama local | API cloud |
|---|---|---|
| Cost | **Gratuit** | $0.01–$0.06 / 1K tokens |
| Internet | **Nu e necesar** | Obligatoriu |
| Confidentialitate | **100% local** | Date trimise extern |
| Viteza | Depinde de hardware | Rapida |
| Modele disponibile | Llama, Mistral, Phi, Gemma | GPT-4, Claude |

**Cerinte minime hardware:**
- RAM: 8 GB pentru modele 3B–7B
- Spatiu disk: 2–5 GB per model
- GPU (optional): accelereaza x5–x10
""")

        st.subheader("Instalare pas cu pas")
        st.markdown("**Windows:**")
        st.code("""# 1. Descarca de la https://ollama.com/download
# 2. Instaleaza (dublu-click pe .exe)
# 3. Porneste serverul:
ollama serve

# 4. Descarca un model (intr-un terminal separat):
ollama pull llama3.2
ollama pull mistral
ollama pull phi3:mini

# 5. Testeaza direct in terminal:
ollama run llama3.2 "Ce este NDVI?"
""", language="bash")

        st.subheader("API Ollama — cum functioneaza")
        st.code("""import requests

# Verifica modele disponibile
r = requests.get("http://localhost:11434/api/tags")
modele = [m["name"] for m in r.json()["models"]]

# Generare text simpla
r = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": "Explica ce este PAC in agricultura.",
    "stream": False,
})
raspuns = r.json()["response"]

# Chat cu context (mai precis)
r = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2",
    "messages": [
        {"role": "system", "content": "Esti expert in agricultura si APIA Romania."},
        {"role": "user",   "content": "Ce culturi sunt eligibile PAC 2025?"},
    ],
    "stream": False,
})
raspuns = r.json()["message"]["content"]
""", language="python")

    with col2:
        st.subheader("Modele recomandate")
        for model_id, model_name, ram, desc in MODELE_RECOMANDATE:
            st.markdown(f"""
<div style='background:white; border-radius:8px; padding:10px 14px; margin:6px 0;
     box-shadow:0 2px 6px rgba(0,0,0,0.07); border-left:4px solid #8e44ad;'>
    <div style='font-weight:700; color:#8e44ad; font-size:13px;'>{model_name}</div>
    <div style='font-size:10px; color:#888; font-family:monospace;'>{model_id}</div>
    <div style='font-size:11px; color:#555; margin-top:4px;'>{desc}</div>
    <div style='font-size:10px; color:#27ae60; font-weight:600; margin-top:2px;'>RAM necesar: {ram}</div>
    <code style='font-size:10px; background:#f5f5f5; padding:2px 6px; border-radius:3px;
          display:block; margin-top:6px;'>ollama pull {model_id}</code>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
<div style='background:#fef9e7; border-radius:8px; padding:12px;
     border-top:3px solid #f39c12;'>
<div style='font-weight:700; color:#d35400;'>De ce Modul 4 = AI Generativ?</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.8;'>
Modulele 1-3 <b>analizeaza</b> date existente.<br>
Modul 4 <b>genereaza</b> continut nou:<br>
- Rapoarte APIA complete<br>
- Explicatii pentru fermieri<br>
- Raspunsuri la intrebari complexe<br>
- Continut academic<br><br>
Combinat cu NLP (M3), formeaza un<br>
pipeline complet: <b>citeste → intelege → scrie</b>.
</div></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Chat cu LLM local")

    SYSTEM_APIA = (
        "Esti un expert in agricultura, politica agricola comuna (PAC) si APIA Romania. "
        "Raspunzi concis, in limba romana, cu informatii practice pentru inspectori si fermieri. "
        "Daca nu stii ceva, spui clar ca nu stii."
    )

    if "chat_istoric" not in st.session_state:
        st.session_state.chat_istoric = []

    col_chat, col_opt = st.columns([3, 1])

    with col_opt:
        system_prompt = st.text_area(
            "Rol asistent (system prompt):",
            value=SYSTEM_APIA,
            height=140,
            key="system_p"
        )
        if st.button("Sterge conversatia", use_container_width=True):
            st.session_state.chat_istoric = []
            st.rerun()
        st.markdown("**Intrebari rapide:**")
        intrebari_rapide = [
            "Ce este NDVI si cum se calculeaza?",
            "Care este pragul de penalizare APIA pentru diferenta de suprafata?",
            "Explica eco-schema PAC 2023-2027.",
            "Ce culturi sunt eligibile pentru plata de baza?",
            "Cum se face controlul pe teren la APIA?",
        ]
        for intrebare in intrebari_rapide:
            if st.button(intrebare[:45] + "…" if len(intrebare) > 45 else intrebare,
                         use_container_width=True, key=f"q_{intrebare[:10]}"):
                st.session_state["chat_input_rapid"] = intrebare

    with col_chat:
        # Afiseaza istoricul
        for mesaj in st.session_state.chat_istoric:
            with st.chat_message(mesaj["role"]):
                st.markdown(mesaj["content"])

        # Input utilizator
        val_initiala = st.session_state.pop("chat_input_rapid", "")
        user_input = st.chat_input(
            "Introdu intrebarea ta...",
            key="chat_main_input"
        )
        if val_initiala and not user_input:
            user_input = val_initiala

        if user_input:
            st.session_state.chat_istoric.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Generez raspuns..."):
                    if ollama_ok:
                        mesaje_api = [{"role": "system", "content": system_prompt}] + \
                                     st.session_state.chat_istoric
                        ok, raspuns = chat_ollama(model_selectat, mesaje_api)
                        if not ok:
                            raspuns = f"Eroare: {raspuns}"
                    else:
                        time.sleep(1)
                        raspuns = DEMO_RASPUNSURI["chat"]
                        if any(k in user_input.lower() for k in ["ndvi", "vegetatie"]):
                            raspuns = "NDVI (Normalized Difference Vegetation Index) = (NIR - RED) / (NIR + RED). Valorile tipice: <0.2 = sol gol sau stres sever; 0.2–0.4 = vegetatie slaba; 0.4–0.7 = vegetatie sanatoasa; >0.7 = vegetatie densa. [MOD DEMO — porneste Ollama pentru AI real]"
                        elif any(k in user_input.lower() for k in ["penalizare", "prag", "diferenta"]):
                            raspuns = "Conform regulamentelor PAC: diferenta 0–3% = fara penalizare; 3–20% = penalizare egala cu diferenta detectata; >20% = excludere partiala; >50% = excludere totala + penalizare suplimentara. [MOD DEMO]"
                        else:
                            raspuns += "\n\n*[MOD DEMO — instalati Ollama pentru raspunsuri reale]*"

                st.markdown(raspuns)

            st.session_state.chat_istoric.append({"role": "assistant", "content": raspuns})
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GENERATOR RAPOARTE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Generator Rapoarte APIA cu LLM local")
    st.markdown("Completeaza datele parcelei — LLM-ul genereaza raportul formal automat.")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fermier       = st.text_input("Numele fermierului:", "Popescu Ion")
        judet         = st.selectbox("Judet:", ["Gorj", "Dolj", "Olt", "Valcea", "Mehedinti", "Hunedoara"])
        parcela_cod   = st.text_input("Cod parcela LPIS:", "GJ-001-A")
        suprafata_dec = st.number_input("Suprafata declarata (ha):", 0.1, 500.0, 4.52, 0.01)
        suprafata_mas = st.number_input("Suprafata masurata GPS (ha):", 0.1, 500.0, 4.31, 0.01)
    with col_f2:
        cultura       = st.selectbox("Cultura:", ["Grau", "Floarea-soarelui", "Porumb", "Lucerna", "Fanete", "Rapita", "Orz"])
        ndvi_mediu    = st.slider("NDVI mediu:", 0.0, 1.0, 0.62, 0.01)
        stare_fito    = st.selectbox("Stare fitosanitara:", ["Buna", "Satisfacatoare", "Problematica", "Critica"])
        neconformitati= st.text_area("Neconformitati observate (optional):", "", height=80)
        tip_raport    = st.selectbox("Tip raport:", ["Control pe teren", "Notificare neconformitate", "Raport final plata"])

    diferenta_pct = abs(suprafata_dec - suprafata_mas) / suprafata_dec * 100 if suprafata_dec > 0 else 0
    if diferenta_pct < 3:
        concluzie_auto = "conforma — fara penalizare"
        culoare_conc = "#27ae60"
    elif diferenta_pct < 20:
        concluzie_auto = f"penalizare {diferenta_pct:.1f}% aplicata"
        culoare_conc = "#e67e22"
    else:
        concluzie_auto = "excludere partiala + penalizare suplimentara"
        culoare_conc = "#e74c3c"

    st.markdown(
        f"**Diferenta suprafata:** {diferenta_pct:.1f}% → "
        f"<span style='color:{culoare_conc};font-weight:700'>{concluzie_auto}</span>",
        unsafe_allow_html=True
    )

    genereaza_btn = st.button("Genereaza raport cu LLM", type="primary", use_container_width=True)

    if genereaza_btn:
        prompt_raport = f"""Genereaza un {tip_raport} formal pentru APIA Romania cu urmatoarele date:
- Fermier: {fermier}, judet {judet}
- Parcela: {parcela_cod}, suprafata declarata {suprafata_dec} ha, suprafata masurata {suprafata_mas} ha
- Diferenta suprafata: {diferenta_pct:.1f}% ({concluzie_auto})
- Cultura: {cultura}, stare fitosanitara: {stare_fito}
- NDVI mediu: {ndvi_mediu}
- Neconformitati: {neconformitati if neconformitati else 'niciuna'}
- Data: {datetime.date.today().strftime('%d.%m.%Y')}

Raportul trebuie sa fie formal, in romana, cu concluzii clare si recomandari practice."""

        with st.spinner("LLM genereaza raportul..."):
            if ollama_ok:
                system_raport = (
                    "Esti un inspector APIA expert. Generezi rapoarte formale clare, concise, "
                    "in limba romana. Folosesti terminologia PAC corecta."
                )
                ok, raport_generat = genereaza_ollama(model_selectat, prompt_raport, system_raport)
                if not ok:
                    raport_generat = f"Eroare Ollama: {raport_generat}"
            else:
                time.sleep(1.5)
                raport_generat = DEMO_RASPUNSURI["raport"].format(
                    data=datetime.date.today().strftime("%d.%m.%Y"),
                    suprafata=suprafata_mas,
                    cultura=cultura.lower()
                ) + "\n\n*[MOD DEMO — porneste Ollama pentru raport generat de AI real]*"

        st.markdown("---")
        st.markdown("**Raport generat:**")
        st.markdown(
            f"<div style='background:#f8f9fa; border-radius:8px; padding:16px; "
            f"font-size:12px; line-height:1.8; border-left:4px solid #8e44ad; "
            f"white-space:pre-wrap; font-family:monospace;'>{raport_generat}</div>",
            unsafe_allow_html=True
        )
        st.download_button(
            "Descarca raport .txt",
            data=raport_generat.encode("utf-8"),
            file_name=f"raport_{parcela_cod.replace('-','_')}_{datetime.date.today().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — COMPARATIE MODELE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Comparatie modele LLM locale")

    st.markdown("""
<div style='background:linear-gradient(135deg,#8e44ad 0%,#1a5276 100%);
     border-radius:10px; padding:14px 20px; color:white; margin-bottom:16px;'>
<div style='font-size:13px; font-weight:700;'>Cum alegi modelul potrivit?</div>
<div style='font-size:11px; margin-top:6px; opacity:0.9;'>
Nu exista un model "cel mai bun" universal. Alegerea depinde de RAM disponibil,
viteza dorita si tipul de sarcina. Pentru APIA: Llama 3.2 3B sau Mistral 7B.
</div></div>
""", unsafe_allow_html=True)

    date_comparatie = [
        ("Llama 3.2 1B",  "~1.3 GB", "Foarte rapid", "Baza", "Conversatii scurte, clasificare",    "#27ae60"),
        ("Llama 3.2 3B",  "~2 GB",   "Rapid",        "Bun",  "Rapoarte APIA, chat, NLP",           "#2ecc71"),
        ("Gemma 2 2B",    "~1.6 GB", "Rapid",        "Bun",  "Conversatie, rezumare",              "#1abc9c"),
        ("Phi-3 Mini",    "~2.3 GB", "Mediu",        "Bun",  "Cod Python, analiza date",           "#3498db"),
        ("Mistral 7B",    "~4.1 GB", "Mediu",        "Excelent", "Texte complexe, rapoarte lungi", "#9b59b6"),
        ("Llama 3.1 8B",  "~4.7 GB", "Lent pe CPU",  "Excelent", "Calitate maxima, GPU recomandat","#8e44ad"),
    ]

    for model_n, ram, viteza, calitate, utilizare, culoare in date_comparatie:
        stele_v = {"Rapid": "★★★", "Mediu": "★★☆", "Lent pe CPU": "★☆☆", "Foarte rapid": "★★★"}.get(viteza, "★★")
        stele_c = {"Baza": "★★☆", "Bun": "★★★", "Excelent": "★★★★"}.get(calitate, "★★")
        st.markdown(f"""
<div style='display:flex; align-items:center; gap:12px; padding:10px 14px; margin:4px 0;
     background:white; border-radius:8px; box-shadow:0 1px 4px rgba(0,0,0,0.06);
     border-left:4px solid {culoare};'>
    <div style='min-width:130px; font-weight:700; color:{culoare};'>{model_n}</div>
    <div style='min-width:70px; font-size:11px; color:#555;'><b>RAM:</b> {ram}</div>
    <div style='min-width:80px; font-size:11px;'><b>Vit.:</b> {stele_v}</div>
    <div style='min-width:90px; font-size:11px;'><b>Cal.:</b> {stele_c}</div>
    <div style='font-size:11px; color:#555; flex:1;'>{utilizare}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Test prompt live pe modele instalate")

    if ollama_ok and len(modele_disponibile) > 1:
        modele_test = st.multiselect(
            "Selecteaza modele pentru test comparativ:",
            modele_disponibile,
            default=modele_disponibile[:2]
        )
        prompt_test = st.text_input(
            "Prompt test:",
            "In 2 propozitii: ce este NDVI si de ce e important in agricultura?"
        )
        if st.button("Ruleaza test comparativ", type="primary"):
            cols = st.columns(len(modele_test)) if modele_test else []
            for i, (m, col) in enumerate(zip(modele_test, cols)):
                with col:
                    with st.spinner(f"Rulam {m}..."):
                        t0 = time.time()
                        ok, rez = genereaza_ollama(m, prompt_test)
                        durata = time.time() - t0
                    st.markdown(f"**{m}** ({durata:.1f}s)")
                    if ok:
                        st.success(rez)
                    else:
                        st.error(rez)
    elif ollama_ok and len(modele_disponibile) == 1:
        st.info(f"Ai un singur model instalat ({modele_disponibile[0]}). Instaleaza un al doilea pentru comparatie.")
    else:
        st.info(
            "Instalati minim 2 modele pentru test comparativ:\n"
            "```\nollama pull llama3.2\nollama pull mistral\n```"
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ziua 19 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### Concepte noi — Ollama & LLM local

**Ce este un LLM (Large Language Model)?**
- Model antrenat pe miliarde de texte
- Poate genera, rezuma, traduce, explica text
- Exemple: Llama (Meta), Mistral, Phi (Microsoft), Gemma (Google)

**Ce este Ollama?**
- Runtime care ruleaza LLM-uri local
- API simplu REST (http://localhost:11434)
- Gratuit, open-source, offline complet
- Suporta zeci de modele

**Diferenta fata de alte tehnici NLP:**
| Tehnica | Tip | Exemplu |
|---|---|---|
| TF-IDF (Z13) | Statistica | Frecventa cuvinte |
| Naive Bayes (Z15) | ML clasic | Clasificare |
| BERT HF (Z17) | DL pretrained | NER |
| **LLM Ollama (Z19)** | **Generativ** | **Scrie text nou** |

**Arhitectura Transformer — baza LLM:**
- Atentie multi-cap (Multi-Head Attention)
- Context window: 4K–128K tokens
- Temperature: 0 = determinist, 1 = creativ
""")

    with col2:
        st.markdown("""
#### Aplicatii practice APIA

**1. Asistent inspector**
```python
raspuns = chat_ollama("llama3.2", [
    {"role": "system", "content": "Expert APIA"},
    {"role": "user",
     "content": "Ce penalizare se aplica la 15% diferenta?"}
])
```

**2. Generator rapoarte automat**
```python
raport = genereaza_ollama(
    "llama3.2",
    f"Genereaza raport control pentru parcela "
    f"{cod}, suprafata {sup} ha, cultura {cultura}.",
    system="Inspector APIA, limbaj formal."
)
```

**3. Pipeline complet M1+M2+M3+M4**
```
Imagine aeriana
    → Z14 (CV): suprafata masurata = 4.31 ha
    → Z10 (NDVI): stare = buna, NDVI=0.62
    → Z18 (NLP): suprafata declarata = 4.52 ha
    → Z19 (LLM): genereaza raport formal complet
```
""")
        st.markdown("""
<div style='background:#f5eef8; border-radius:8px; padding:14px; margin-top:12px;
     border-top:3px solid #8e44ad;'>
<div style='font-weight:700; color:#6c3483;'>Concluzie Ziua 19</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.7;'>
Ollama aduce AI generativ pe calculatorul tau fara niciun cost.
Combinat cu pipeline-ul construit in M1-M3, poti automatiza integral
fluxul de inspectie APIA: de la imaginea aeriana la raportul final generat de AI.
<br><br>
Urmatoarea: <b>Ziua 20 — Generator rapoarte APIA complet cu LLM</b>.
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#8e44ad 0%,#1a5276 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 19 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
Ollama | Llama 3 | Mistral | Phi-3 | API REST local | Chat | Generator rapoarte APIA | Comparatie modele
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 20 — Generator Rapoarte APIA Complet cu LLM Local
</div>
</div>
""", unsafe_allow_html=True)
