"""
Ziua 22 — Generator Continut Academic cu LLM Local
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
# CONFIG ACADEMIC
# ══════════════════════════════════════════════════════════════════════════════

DISCIPLINE = [
    "Managementul Riscului in Agricultura",
    "Politica Agricola Comuna (PAC)",
    "Sisteme Informationale Geografice (GIS)",
    "Drone si UAV in Agricultura",
    "Inteligenta Artificiala Aplicata",
    "Fonduri Europene pentru Agricultura",
    "Turism Rural si Agroturism",
    "Managementul Exploatatiilor Agricole",
]

TIPURI_CONTINUT = {
    "Suport de curs (structura)": {
        "icon": "CURS",
        "culoare": "#1a5276",
        "system": (
            "Esti profesor universitar la o universitate din Romania, specializat in agricultura si AI. "
            "Generezi materiale didactice clare, structurate, conform standardelor ARACIS. "
            "Folosesti limba romana academica, cu exemple practice din agricultura romaneasca."
        ),
        "prompt": (
            "Genereaza structura unui suport de curs universitar pentru disciplina '{disciplina}', "
            "tema '{tema}', nivel {nivel}.\n\n"
            "Include:\n"
            "1. Obiective de invatare (3-5 obiective SMART)\n"
            "2. Continut teoretic structurat pe subteme (4-6 subteme cu descriere scurta)\n"
            "3. Concepte cheie de retinut (5-8 termeni cu definitie scurta)\n"
            "4. Exemple practice din agricultura romaneasca (2-3 exemple concrete)\n"
            "5. Intrebari de autoevaluare (3-5 intrebari)\n\n"
            "Lungime: maximum 350 cuvinte — structura concisa, clara. Stil academic accesibil."
        ),
    },
    "Plan seminar": {
        "icon": "SEM",
        "culoare": "#27ae60",
        "system": (
            "Esti cadru didactic la Master Managementul Riscului in Agricultura, UCB Targu Jiu. "
            "Generezi planuri de seminar practice, interactive, cu aplicatii reale APIA/PAC."
        ),
        "prompt": (
            "Genereaza un plan detaliat de seminar pentru disciplina '{disciplina}', "
            "tema '{tema}', durata {durata} minute, {nr_studenti} studenti.\n\n"
            "Include:\n"
            "1. Obiective seminar (2-3)\n"
            "2. Materiale necesare\n"
            "3. Desfasurare activitati (cu minute alocate per activitate)\n"
            "4. Exercitiu practic principal (descriere detaliata, pas cu pas)\n"
            "5. Tema de casa (optionala)\n"
            "6. Criterii de evaluare\n\n"
            "Accentueaza aplicatiile practice pe cazuri reale din agricultura Gorj/Romania."
        ),
    },
    "Intrebari de evaluare": {
        "icon": "EVAL",
        "culoare": "#e67e22",
        "system": (
            "Esti examinator universitar. Generezi intrebari de evaluare riguroase, "
            "clare, fara ambiguitati, conform taxonomiei Bloom."
        ),
        "prompt": (
            "Genereaza {nr_intrebari} intrebari de evaluare pentru disciplina '{disciplina}', "
            "tema '{tema}', nivel cognitive '{nivel_bloom}'.\n\n"
            "Pentru fiecare intrebare include:\n"
            "- Intrebarea (clara, fara ambiguitati)\n"
            "- Tipul: grila / deschisa / aplicatie practica\n"
            "- Raspuns model (3-5 randuri)\n"
            "- Punctaj sugerat\n\n"
            "Intrebarile sa acopere cunostinte (20%), intelegere (30%), aplicare (50%)."
        ),
    },
    "Rezumat bibliografic": {
        "icon": "BIB",
        "culoare": "#8e44ad",
        "system": (
            "Esti cercetator academic specializat in agricultura si politici europene. "
            "Sintetizezi literatura stiintifica in rezumate clare si utile pentru studenti."
        ),
        "prompt": (
            "Genereaza un rezumat bibliografic de 400-500 cuvinte despre '{tema}' "
            "in contextul '{disciplina}'.\n\n"
            "Include:\n"
            "1. Introducere in tema (context si importanta)\n"
            "2. Principalele directii de cercetare (3-4 directii cu autori reprezentativi)\n"
            "3. Concluzii si tendinte actuale\n"
            "4. Relevanta pentru Romania si PAC 2023-2027\n"
            "5. Surse recomandate (5 referinte in format APA, reale sau plauzibile)\n\n"
            "Nota: marcheaza cu [de verificat] orice referinta nesigura."
        ),
    },
    "Fisa de lucru studenti": {
        "icon": "FISA",
        "culoare": "#c0392b",
        "system": (
            "Esti profesor la UCB Targu Jiu, Master MRA. "
            "Creezi fise de lucru practice, clare, cu spatii de completat pentru studenti."
        ),
        "prompt": (
            "Genereaza o fisa de lucru practica pentru studenti, "
            "disciplina '{disciplina}', tema '{tema}', durata {durata} minute.\n\n"
            "Include:\n"
            "1. Titlu si date identificare (data, grupa, student)\n"
            "2. Obiectivul activitatii\n"
            "3. Date/informatii furnizate studentului\n"
            "4. Sarcini de lucru (4-6 sarcini clare, numerotate)\n"
            "5. Spatii de completat pentru fiecare sarcina\n"
            "6. Rubrica de autoevaluare (3-4 criterii cu DA/NU/PARTIAL)\n\n"
            "Foloseste un caz real din agricultura Gorj sau Romania."
        ),
    },
}

DEMO_RASPUNSURI = {
    "Suport de curs (structura)": """SUPORT DE CURS — {disciplina}
Tema: {tema} | Nivel: {nivel}
Generat: {data} [MOD DEMO]

1. OBIECTIVE DE INVATARE
   • Studentul va defini conceptele de baza ale temei
   • Studentul va aplica metodele invatate pe cazuri reale APIA
   • Studentul va analiza riscurile asociate in contextul PAC 2023-2027

2. CONTINUT TEORETIC
   2.1 Introducere si context european
   2.2 Cadrul legislativ (Reg. UE 2021/2116)
   2.3 Instrumente si metode practice
   2.4 Studiu de caz Romania/Gorj

3. CONCEPTE CHEIE
   • PAC = Politica Agricola Comuna (buget 387 miliarde EUR / 2021-2027)
   • IACS = Sistemul Integrat de Administrare si Control
   • LPIS = Sistemul de Identificare a Parcelelor Agricole

4. EXEMPLE PRACTICE
   • Calculul subventiei pentru o parcela de 5 ha grau, judetul Gorj
   • Detectia neconformitatilor prin analiza NDVI cu drone

5. INTREBARI DE AUTOEVALUARE
   • Ce este LPIS si ce rol are in sistemul PAC?
   • Calculati penalizarea pentru o diferenta de suprafata de 8%.""",

    "Plan seminar": """PLAN SEMINAR — {disciplina}
Tema: {tema} | Durata: {durata} min | {nr_studenti} studenti
[MOD DEMO]

OBIECTIVE: (1) Aplicarea conceptelor pe date reale; (2) Lucru in echipa

MATERIALE: laptop, date EXIF fotografii, platforma SecureGeo

DESFASURARE:
0-10 min  — Recapitulare teorie (intrebari rapide)
10-30 min — Exercitiu individual: analiza parcela reala
30-45 min — Lucru in echipe de 3: comparatie rezultate
45-55 min — Prezentare concluzii per echipa
55-60 min — Feedback si tema de casa

EXERCITIU PRINCIPAL:
Fiecare student primeste 10 fotografii GPS si trebuie sa identifice
secventele GPS Fantoma folosind criteriile din curs.

TEMA CASA: Analizeaza 20 fotografii proprii si raporteaza.""",
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII OLLAMA
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


def genereaza_ollama(model, prompt, system=""):
    payload = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=360)
        if r.status_code == 200:
            return True, r.json().get("response", "")
        return False, f"Eroare HTTP {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza — porneste cu: ollama serve"
    except Exception as e:
        return False, str(e)


def genereaza_ollama_stream(model, prompt, system, container):
    import json as _json
    payload = {"model": model, "prompt": prompt, "stream": True}
    if system:
        payload["system"] = system
    text = ""
    try:
        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=360,
        ) as r:
            if r.status_code != 200:
                return False, f"Eroare HTTP {r.status_code}"
            for line in r.iter_lines():
                if not line:
                    continue
                chunk = _json.loads(line)
                text += chunk.get("response", "")
                if not chunk.get("done"):
                    container.markdown(
                        f"<div style='background:#f0f4f8; border-radius:8px; padding:14px; "
                        f"font-size:12px; line-height:1.8; font-family:monospace; "
                        f"white-space:pre-wrap; max-height:480px; overflow-y:auto;'>"
                        f"{text} ▌</div>",
                        unsafe_allow_html=True,
                    )
        return True, text
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza — porneste cu: ollama serve"
    except Exception as e:
        return False, str(e)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 22 — Generator Academic",
    page_icon="UCB",
    layout="wide",
    initial_sidebar_state="expanded"
)

ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#1a5276;'>UCB</div>
    <div style='font-size:16px; font-weight:700; color:#1a5276;'>ZIUA 22</div>
    <div style='font-size:11px; color:#666;'>Generator Continut Academic</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI Generativ Local")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 22 / 30 zile")
st.sidebar.progress(22 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_selectat = st.sidebar.selectbox("Model:", modele_disponibile or ["llama3.2:latest"])
else:
    st.sidebar.error("Ollama offline — mod demo")
    model_selectat = "llama3.2:latest"

st.sidebar.markdown("""
**Continut disponibil:**
- Suport de curs
- Plan seminar
- Intrebari evaluare
- Rezumat bibliografic
- Fisa de lucru studenti
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#1a5276; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj<br>
<b>Curs:</b> Master MRA
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:38px; font-weight:900; color:#1a5276;'>UCB</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1a5276; font-weight:800;'>
            Ziua 22 — Generator Continut Academic cu LLM Local
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Suporturi curs · Seminare · Evaluare · Rezumate bibliografice · Fise de lucru
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

if not ollama_ok:
    st.warning("Ollama offline — mod demo activ. Porneste `ollama serve` pentru continut generat de AI.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Generator continut",
    "Generator rapid (lot)",
    "Istoric sesiune",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GENERATOR INDIVIDUAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Genereaza material didactic")

    col_stanga, col_dreapta = st.columns([1, 1])

    with col_stanga:
        tip_ales = st.selectbox(
            "Tip material:",
            list(TIPURI_CONTINUT.keys()),
            key="tip_material"
        )
        config = TIPURI_CONTINUT[tip_ales]

        st.markdown(f"""
<div style='background:{config["culoare"]}15; border-left:4px solid {config["culoare"]};
     border-radius:4px; padding:8px 14px; margin-bottom:10px; font-size:12px;'>
<b>{tip_ales}</b>
</div>
""", unsafe_allow_html=True)

        disciplina = st.selectbox("Disciplina:", DISCIPLINE, key="disciplina_gen")
        tema       = st.text_input("Tema specifica:", "Detectia neconformitatilor PAC cu drone si AI", key="tema_gen")

        # Campuri specifice per tip
        if tip_ales == "Suport de curs (structura)":
            nivel = st.selectbox("Nivel:", ["Master", "Licenta", "Doctorat", "Formare profesionala"], key="nivel_gen")
        elif tip_ales == "Plan seminar":
            durata       = st.slider("Durata (minute):", 30, 120, 60, 10, key="dur_sem")
            nr_studenti  = st.slider("Nr. studenti:", 5, 30, 12, 1, key="nr_stud")
        elif tip_ales == "Intrebari de evaluare":
            nr_intrebari = st.slider("Nr. intrebari:", 3, 15, 5, 1, key="nr_int")
            nivel_bloom  = st.selectbox("Nivel Bloom:", [
                "Cunoastere (definitii, termeni)",
                "Intelegere (explicatii, rezumate)",
                "Aplicare (calcule, cazuri practice)",
                "Analiza (comparatii, diagnoze)",
                "Mixt (toate nivelurile)",
            ], key="bloom_lev")
        elif tip_ales in ("Plan seminar", "Fisa de lucru studenti"):
            durata = st.slider("Durata activitate (minute):", 20, 90, 45, 5, key="dur_fisa")

        genereaza = st.button(
            f"Genereaza {tip_ales}",
            type="primary", use_container_width=True, key="btn_gen_ac"
        )

    with col_dreapta:
        st.markdown("**Material generat:**")

        if genereaza:
            data_azi = datetime.date.today().strftime("%d.%m.%Y")

            # Construieste promptul
            if tip_ales == "Suport de curs (structura)":
                prompt_final = config["prompt"].format(
                    disciplina=disciplina, tema=tema, nivel=nivel
                )
            elif tip_ales == "Plan seminar":
                prompt_final = config["prompt"].format(
                    disciplina=disciplina, tema=tema,
                    durata=durata, nr_studenti=nr_studenti
                )
            elif tip_ales == "Intrebari de evaluare":
                prompt_final = config["prompt"].format(
                    disciplina=disciplina, tema=tema,
                    nr_intrebari=nr_intrebari, nivel_bloom=nivel_bloom
                )
            elif tip_ales == "Rezumat bibliografic":
                prompt_final = config["prompt"].format(
                    disciplina=disciplina, tema=tema
                )
            else:
                prompt_final = config["prompt"].format(
                    disciplina=disciplina, tema=tema,
                    durata=durata if "durata" in locals() else 45
                )

            if ollama_ok:
                stream_ph = st.empty()
                stream_ph.info("Generare in curs (streaming)... textul apare mai jos pe masura ce e generat.")
                ok, rezultat = genereaza_ollama_stream(
                    model_selectat, prompt_final, config["system"], stream_ph
                )
                stream_ph.empty()
                if not ok:
                    rezultat = f"Eroare: {rezultat}"
            else:
                with st.spinner("Generare demo..."):
                    time.sleep(1.5)
                tmpl_key = tip_ales if tip_ales in DEMO_RASPUNSURI else "Suport de curs (structura)"
                rezultat = DEMO_RASPUNSURI[tmpl_key].format(
                    disciplina=disciplina, tema=tema,
                    nivel=nivel if "nivel" in locals() else "Master",
                    durata=durata if "durata" in locals() else 60,
                    nr_studenti=nr_studenti if "nr_studenti" in locals() else 12,
                    data=data_azi,
                ) + "\n\n*[MOD DEMO — porneste Ollama pentru continut real]*"

            st.session_state.setdefault("istoric_academic", []).append({
                "tip": tip_ales,
                "disciplina": disciplina,
                "tema": tema,
                "data": data_azi,
                "text": rezultat,
            })

            st.markdown(
                f"<div style='background:#f8f9fa; border-radius:8px; padding:14px; "
                f"font-size:12px; line-height:1.8; border-left:4px solid {config['culoare']}; "
                f"white-space:pre-wrap; font-family:monospace; max-height:500px; "
                f"overflow-y:auto;'>{rezultat}</div>",
                unsafe_allow_html=True
            )

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    "Descarca .txt",
                    data=rezultat.encode("utf-8"),
                    file_name=f"{tip_ales[:6].replace(' ','_')}_{tema[:15].replace(' ','_')}_{data_azi.replace('.','')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="dl_gen_ac"
                )
            with col_d2:
                if st.button("Regenereaza (alt raspuns)", use_container_width=True, key="btn_regen"):
                    st.rerun()
        else:
            st.markdown("""
<div style='background:#f0f4f8; border-radius:8px; padding:20px; text-align:center;
     color:#888; font-size:13px; margin-top:20px;'>
Selecteaza tipul de material, completeaza campurile<br>
si apasa <b>Genereaza</b>.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — GENERATOR RAPID LOT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Generator rapid — pachet complet pentru o disciplina")
    st.markdown(
        "Genereaza dintr-o singura apasare: suport curs + plan seminar + "
        "5 intrebari de evaluare + fisa de lucru — pentru aceeasi tema."
    )

    col_lot1, col_lot2 = st.columns([1, 1])
    with col_lot1:
        disc_lot  = st.selectbox("Disciplina:", DISCIPLINE, key="disc_lot")
        tema_lot  = st.text_input("Tema:", "Riscuri climatice in agricultura si fondul de asigurare PAC", key="tema_lot")
        nivel_lot = st.selectbox("Nivel:", ["Master", "Licenta"], key="nivel_lot")

        if st.button("Genereaza pachet complet", type="primary", use_container_width=True, key="btn_lot_ac"):
            st.session_state["run_lot_ac"] = True

    with col_lot2:
        st.markdown("""
**Pachetul generat contine:**

| # | Material | Timp estimat |
|---|---|---|
| 1 | Suport de curs (structura) | ~20 sec |
| 2 | Plan seminar 60 min | ~15 sec |
| 3 | 5 intrebari de evaluare | ~15 sec |
| 4 | Fisa de lucru studenti | ~20 sec |

**Total: ~70 secunde** cu Ollama local.
Manual: 3-4 ore per material.
""")

    if st.session_state.get("run_lot_ac"):
        st.session_state["run_lot_ac"] = False
        st.markdown("---")
        data_azi = datetime.date.today().strftime("%d.%m.%Y")
        pachet = {}

        materiale_lot = [
            ("Suport de curs (structura)", {"disciplina": disc_lot, "tema": tema_lot, "nivel": nivel_lot}),
            ("Plan seminar",               {"disciplina": disc_lot, "tema": tema_lot, "durata": 60, "nr_studenti": 12}),
            ("Intrebari de evaluare",      {"disciplina": disc_lot, "tema": tema_lot, "nr_intrebari": 5, "nivel_bloom": "Mixt (toate nivelurile)"}),
            ("Fisa de lucru studenti",     {"disciplina": disc_lot, "tema": tema_lot, "durata": 45}),
        ]

        bara = st.progress(0)
        for i, (tip_lot, params) in enumerate(materiale_lot):
            cfg = TIPURI_CONTINUT[tip_lot]
            st.markdown(f"**Generez {i+1}/4: {tip_lot}...**")
            prompt_lot = cfg["prompt"].format(**params)

            if ollama_ok:
                ok, text_lot = genereaza_ollama(model_selectat, prompt_lot, cfg["system"])
                if not ok:
                    text_lot = f"[EROARE] {text_lot}"
            else:
                time.sleep(0.8)
                text_lot = (
                    f"{tip_lot.upper()} — {disc_lot}\nTema: {tema_lot}\n"
                    f"[MOD DEMO — porneste Ollama pentru continut real]"
                )

            pachet[tip_lot] = text_lot
            bara.progress((i + 1) / len(materiale_lot))

        st.success(f"Pachet complet generat pentru: **{disc_lot}** — **{tema_lot}**")

        for tip_p, text_p in pachet.items():
            cfg_p = TIPURI_CONTINUT[tip_p]
            with st.expander(f"{tip_p}"):
                st.markdown(
                    f"<div style='font-size:11px; font-family:monospace; "
                    f"white-space:pre-wrap; line-height:1.7;'>{text_p}</div>",
                    unsafe_allow_html=True
                )

        pachet_complet = "\n\n" + "="*60 + "\n\n".join(
            f"{tip}\n{'='*40}\n{text}" for tip, text in pachet.items()
        )
        st.download_button(
            f"Descarca pachet complet .txt",
            data=pachet_complet.encode("utf-8"),
            file_name=f"pachet_{disc_lot[:10].replace(' ','_')}_{data_azi.replace('.','')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ISTORIC
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Materiale generate in aceasta sesiune")
    istoric = st.session_state.get("istoric_academic", [])

    if not istoric:
        st.info("Niciun material generat inca. Foloseste tab-ul 'Generator continut'.")
    else:
        st.metric("Materiale generate", len(istoric))
        for i, item in enumerate(reversed(istoric)):
            cfg_i = TIPURI_CONTINUT.get(item["tip"], {"culoare": "#666"})
            with st.expander(f"[{len(istoric)-i}] {item['tip']} — {item['tema'][:40]} — {item['data']}"):
                st.markdown(
                    f"<div style='font-size:11px; font-family:monospace; "
                    f"white-space:pre-wrap; line-height:1.7;'>{item['text']}</div>",
                    unsafe_allow_html=True
                )
                st.download_button(
                    "Descarca .txt",
                    data=item["text"].encode("utf-8"),
                    file_name=f"material_{i}_{item['data'].replace('.','')}.txt",
                    mime="text/plain",
                    key=f"dl_ist_ac_{i}",
                )
        if st.button("Sterge istoricul", key="btn_sterg_ac"):
            st.session_state["istoric_academic"] = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Ziua 22 — Ce am invatat")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
#### Generator academic cu LLM — rezumat

**Ce am construit:**
- 5 tipuri de materiale didactice generate automat
- System prompt academic specializat per tip
- Generator lot (pachet complet dintr-o apasare)
- Export .txt pentru editare ulterioara in Word

**Principiu cheie — prompt academic:**
```python
system = (
    "Esti profesor universitar la UCB Targu Jiu. "
    "Generezi materiale conform ARACIS. "
    "Limba romana academica, exemple din Romania."
)

prompt = f\"\"\"
Genereaza suport de curs pentru {disciplina},
tema {tema}, nivel {nivel}.
Include: obiective, continut, concepte cheie,
exemple practice, intrebari.
\"\"\"
```

**Calitatea output-ului depinde de:**
1. Promptul (mai specific = mai bun)
2. Modelul (Mistral 7B > Llama 3.2 3B pentru texte lungi)
3. Temperature (0.3-0.5 pentru continut academic)
""")

    with col2:
        st.markdown("""
#### Impact pentru activitatea la UCB

**Fara AI:**
- 1 suport curs = 4-6 ore redactare
- 1 plan seminar = 1-2 ore
- Set 10 intrebari = 1 ora
- Total per disciplina/semestru: 40-60 ore

**Cu AI (Ziua 22):**
- 1 suport curs = 30-60 secunde + revizie 15 min
- 1 plan seminar = 20 secunde + revizie 5 min
- Set 10 intrebari = 20 secunde + revizie 10 min
- Total: 2-3 ore (revizie + personalizare)

**Economie: 35-55 ore/semestru per disciplina**

**Important:** AI genereaza scheletul.
Profesorul adauga experienta, datele reale,
referintele verificate si aprobarea finala.
""")
        st.markdown("""
<div style='background:#e8f4fd; border-radius:8px; padding:12px; margin-top:10px;
     border-top:3px solid #1a5276;'>
<div style='font-weight:700; color:#1a5276;'>Concluzie Ziua 22</div>
<div style='font-size:11px; color:#333; margin-top:6px; line-height:1.7;'>
LLM-ul local devine asistent academic personal —
gratuit, confidential, disponibil 24/7.
Genereaza scheletul, tu pui substanta.<br><br>
Urmatoarea: <b>Ziua 23 — RAG: intreaba un document PDF</b>
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#27ae60 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 22 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
5 tipuri materiale didactice | Suport curs | Seminar | Evaluare | Rezumat bibliografic | Fisa lucru
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 23 — RAG simplu: intreaba un document PDF
</div>
</div>
""", unsafe_allow_html=True)
