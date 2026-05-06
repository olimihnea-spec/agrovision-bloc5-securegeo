"""
Ziua 20 — Generator Rapoarte APIA Complet cu LLM Local
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
# TEMPLATE-URI RAPOARTE
# ══════════════════════════════════════════════════════════════════════════════

TIPURI_RAPORT = {
    "Raport control pe teren": {
        "icon": "Ctrl",
        "culoare": "#1a5276",
        "campuri": ["fermier", "judet", "parcela", "suprafata_dec", "suprafata_mas",
                    "cultura", "ndvi", "stare_fito", "obs"],
        "system": (
            "Esti inspector APIA Romania cu 20 de ani experienta. "
            "Generezi rapoarte de control pe teren formale, clare, in limba romana. "
            "Folosesti terminologia PAC corecta. Esti obiectiv si profesionist."
        ),
        "prompt_template": (
            "Genereaza un raport de control pe teren pentru APIA Romania cu datele:\n"
            "- Fermier: {fermier}, judet {judet}\n"
            "- Parcela: {parcela}, suprafata declarata {suprafata_dec} ha\n"
            "- Suprafata masurata GPS: {suprafata_mas} ha (diferenta: {diferenta:.1f}%)\n"
            "- Cultura: {cultura}, stare fitosanitara: {stare_fito}\n"
            "- NDVI mediu: {ndvi}\n"
            "- Observatii: {obs}\n"
            "- Data control: {data}\n\n"
            "Raportul trebuie sa contina: antet formal, date identificare, constatari, "
            "concluzie (conform/neconform), recomandari si semnatura inspector."
        ),
    },
    "Notificare neconformitate": {
        "icon": "Nec",
        "culoare": "#c0392b",
        "campuri": ["fermier", "judet", "parcela", "suprafata_dec", "suprafata_mas",
                    "cultura", "tip_neconformitate", "penalizare_pct"],
        "system": (
            "Esti jurist APIA Romania. Generezi notificari de neconformitate formale, "
            "cu baza legala corecta (Reg. UE 2021/2116), in limba romana."
        ),
        "prompt_template": (
            "Genereaza o notificare de neconformitate PAC 2025 pentru:\n"
            "- Fermier: {fermier}, judet {judet}\n"
            "- Parcela: {parcela}\n"
            "- Suprafata declarata: {suprafata_dec} ha, masurata: {suprafata_mas} ha\n"
            "- Diferenta: {diferenta:.1f}% — {concluzie}\n"
            "- Tip neconformitate: {tip_neconformitate}\n"
            "- Penalizare aplicata: {penalizare_pct}%\n"
            "- Data: {data}\n\n"
            "Notificarea trebuie sa contina: temeiul legal (Reg. UE 2021/2116, art. relevant), "
            "descrierea neconformitatii, penalizarea calculata, termenul de contestatie (30 zile), "
            "si instructiunile de raspuns."
        ),
    },
    "Decizie de plata": {
        "icon": "Pay",
        "culoare": "#27ae60",
        "campuri": ["fermier", "judet", "nr_parcele", "suprafata_totala",
                    "suma_solicitata", "suma_aprobata", "reducere_pct"],
        "system": (
            "Esti ofiter de plata APIA Romania. Generezi decizii de plata formale, "
            "cu sume exacte si baza legala, in limba romana."
        ),
        "prompt_template": (
            "Genereaza o decizie de plata PAC 2025 pentru:\n"
            "- Beneficiar: {fermier}, judet {judet}\n"
            "- Numar parcele eligibile: {nr_parcele}\n"
            "- Suprafata totala eligibila: {suprafata_totala} ha\n"
            "- Suma solicitata: {suma_solicitata} EUR\n"
            "- Suma aprobata: {suma_aprobata} EUR\n"
            "- Reducere aplicata: {reducere_pct}%\n"
            "- Data: {data}\n\n"
            "Decizia trebuie sa contina: temeiul legal, suma aprobata, modalitatea de plata, "
            "termenul estimat, si dreptul de contestatie."
        ),
    },
    "Adresa catre fermier": {
        "icon": "ADR",
        "culoare": "#8e44ad",
        "campuri": ["fermier", "judet", "subiect", "continut_adresa"],
        "system": (
            "Esti secretar APIA Romania. Scrii adrese oficiale catre fermieri, "
            "ton formal dar accesibil, in limba romana."
        ),
        "prompt_template": (
            "Scrie o adresa oficiala APIA catre fermierul {fermier} din judetul {judet}.\n"
            "Subiect: {subiect}\n"
            "Continut de transmis: {continut_adresa}\n"
            "Data: {data}\n\n"
            "Adresa trebuie sa fie formala, cu antet APIA, corp clar si semnatura Director Executiv."
        ),
    },
}

DEMO_RAPOARTE = {
    "Raport control pe teren": """AGENTIA DE PLATI SI INTERVENTIE PENTRU AGRICULTURA
CENTRUL JUDETEAN {judet}

RAPORT DE CONTROL PE TEREN
Nr. {nr_raport} / {data}

I. DATE DE IDENTIFICARE
Fermier: {fermier}, judet {judet}
Parcela: {parcela} | Suprafata declarata: {suprafata_dec} ha

II. CONSTATARI
Suprafata masurata GPS: {suprafata_mas} ha
Diferenta: {diferenta:.1f}% — {concluzie}
Cultura: {cultura} | Stare fitosanitara: {stare_fito}
NDVI mediu: {ndvi}

III. CONCLUZIE
Parcela se incadreaza in parametrii eligibili PAC 2025.
{obs_text}

Inspector: ___________________
Data: {data}

[DEMO — porneste Ollama pentru raport generat de AI]""",

    "Notificare neconformitate": """AGENTIA DE PLATI SI INTERVENTIE PENTRU AGRICULTURA
CENTRUL JUDETEAN {judet}

NOTIFICARE DE NECONFORMITATE
Nr. APIA-{judet}-NECONF-2025 / {data}

Catre: {fermier}, judet {judet}

In conformitate cu Reg. UE 2021/2116, art. 59-60, va notificam
neconformitatea constatata la parcela {parcela}.

Diferenta suprafata: {diferenta:.1f}% (prag admis: 3%)
Penalizare aplicata: {penalizare_pct}%
Tip neconformitate: {tip_neconformitate}

Aveti dreptul de a contesta in 30 de zile lucratoare.

Director Executiv APIA CJ {judet}
[DEMO — porneste Ollama pentru notificare generata de AI]""",
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
            modele = [m["name"] for m in r.json().get("models", [])]
            return True, modele
    except Exception:
        pass
    return False, []


def genereaza_ollama(model: str, prompt: str, system: str = "") -> tuple:
    payload = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=180)
        if r.status_code == 200:
            return True, r.json().get("response", "")
        return False, f"Eroare HTTP {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza. Porneste cu: ollama serve"
    except requests.exceptions.Timeout:
        return False, "Timeout — incearca un model mai mic."
    except Exception as e:
        return False, str(e)


def calcul_penalizare(diferenta_pct: float) -> tuple:
    """Returneaza (concluzie, penalizare_pct, culoare)."""
    if diferenta_pct < 3:
        return "conforma — fara penalizare", 0, "#27ae60"
    elif diferenta_pct < 20:
        return f"penalizare {diferenta_pct:.1f}%", diferenta_pct, "#e67e22"
    elif diferenta_pct < 50:
        return "excludere partiala + penalizare suplimentara", 30, "#e74c3c"
    else:
        return "excludere totala + penalizare 100%", 100, "#922b21"

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 20 — Generator Rapoarte APIA",
    page_icon="APIA",
    layout="wide",
    initial_sidebar_state="expanded"
)

ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:30px; font-weight:900; color:#1a5276;'>APIA</div>
    <div style='font-size:16px; font-weight:700; color:#27ae60;'>ZIUA 20</div>
    <div style='font-size:11px; color:#666;'>Generator Rapoarte cu LLM Local</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI Generativ Local")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 20 / 30 zile")
st.sidebar.progress(20 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_selectat = st.sidebar.selectbox(
        "Model:",
        modele_disponibile if modele_disponibile else ["llama3.2:3b"]
    )
else:
    st.sidebar.error("Ollama offline — mod demo")
    model_selectat = "llama3.2:3b"

st.sidebar.markdown("""
**Tipuri rapoarte disponibile:**
- Raport control pe teren
- Notificare neconformitate
- Decizie de plata
- Adresa catre fermier
- Procesare lot (multiple)
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#1a5276; border-radius:8px; padding:10px 12px; color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj<br>
<b>Curs:</b> Master MRA
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:42px; font-weight:900; color:#1a5276;'>APIA</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1a5276; font-weight:800;'>
            Ziua 20 — Generator Rapoarte APIA cu LLM Local
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Raport control · Notificare · Decizie plata · Adresa · Lot multiplu
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

if not ollama_ok:
    st.warning(
        "Ollama nu ruleaza — **mod demo** activ. "
        "Ruleaza `ollama serve` + `ollama pull llama3.2` pentru rapoarte generate de AI."
    )

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Generator individual",
    "Procesare lot",
    "Sabloane & Prompturi",
    "Istoric rapoarte",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GENERATOR INDIVIDUAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Genereaza un raport complet")

    tip_ales = st.selectbox(
        "Tipul raportului:",
        list(TIPURI_RAPORT.keys()),
        key="tip_raport_individual"
    )
    config = TIPURI_RAPORT[tip_ales]

    st.markdown(f"""
<div style='background:{config["culoare"]}18; border-left:4px solid {config["culoare"]};
     border-radius:4px; padding:8px 14px; margin-bottom:12px; font-size:12px; color:#333;'>
<b>{tip_ales}</b> — completeaza campurile de mai jos si apasa Genereaza.
</div>
""", unsafe_allow_html=True)

    col_form, col_preview = st.columns([1, 1])

    with col_form:
        # Campuri comune
        fermier = st.text_input("Fermier (Nume Prenume):", "Popescu Ion", key="f_fermier")
        judet   = st.selectbox("Judet:", ["Gorj", "Dolj", "Olt", "Valcea", "Mehedinti",
                                           "Hunedoara", "Caras-Severin"], key="f_judet")

        if tip_ales in ("Raport control pe teren", "Notificare neconformitate"):
            parcela      = st.text_input("Cod parcela LPIS:", "GJ-001-A", key="f_parcela")
            sup_dec      = st.number_input("Suprafata declarata (ha):", 0.1, 500.0, 4.52, 0.01, key="f_supdec")
            sup_mas      = st.number_input("Suprafata masurata GPS (ha):", 0.1, 500.0, 4.31, 0.01, key="f_supmas")
            diferenta    = abs(sup_dec - sup_mas) / sup_dec * 100 if sup_dec > 0 else 0
            concluzie, pen_pct, culoare_c = calcul_penalizare(diferenta)

            st.markdown(
                f"Diferenta: **{diferenta:.1f}%** → "
                f"<span style='color:{culoare_c};font-weight:700'>{concluzie}</span>",
                unsafe_allow_html=True
            )

            if tip_ales == "Raport control pe teren":
                cultura    = st.selectbox("Cultura:", ["Grau", "Porumb", "Floarea-soarelui",
                                                        "Lucerna", "Fanete", "Rapita"], key="f_cult")
                ndvi_v     = st.slider("NDVI mediu:", 0.0, 1.0, 0.62, 0.01, key="f_ndvi")
                stare_fito = st.selectbox("Stare fitosanitara:", ["Buna", "Satisfacatoare",
                                                                   "Problematica", "Critica"], key="f_fito")
                obs        = st.text_area("Observatii:", "", height=70, key="f_obs")

            elif tip_ales == "Notificare neconformitate":
                tip_nec    = st.selectbox("Tip neconformitate:", [
                    "Diferenta suprafata > 3%",
                    "Cultura declarata diferita de cea identificata",
                    "Parcela neeligibila (element fix depasit)",
                    "Eco-schema nerespectata",
                ], key="f_tipnec")

        elif tip_ales == "Decizie de plata":
            nr_parc    = st.number_input("Nr. parcele eligibile:", 1, 50, 3, key="f_nrp")
            sup_tot    = st.number_input("Suprafata totala eligibila (ha):", 0.1, 1000.0, 10.47, 0.01, key="f_supt")
            suma_sol   = st.number_input("Suma solicitata (EUR):", 0.0, 500000.0, 3500.0, 10.0, key="f_sumsol")
            suma_apr   = st.number_input("Suma aprobata (EUR):", 0.0, 500000.0, 3360.0, 10.0, key="f_sumapr")
            red_pct    = round((1 - suma_apr / suma_sol) * 100, 1) if suma_sol > 0 else 0.0
            st.markdown(f"Reducere calculata: **{red_pct}%**")

        elif tip_ales == "Adresa catre fermier":
            subiect    = st.text_input("Subiect adresa:", "Solicitare documente suplimentare", key="f_subj")
            continut   = st.text_area("Continut de transmis:", height=100,
                                       value="Va rugam sa prezentati actele de proprietate "
                                             "pentru parcela GJ-001-A in termen de 10 zile lucratoare.",
                                       key="f_cont")

        genereaza_btn = st.button(
            f"Genereaza {tip_ales}",
            type="primary", use_container_width=True, key="btn_gen"
        )

    with col_preview:
        st.markdown("**Previzualizare / Raport generat:**")

        if genereaza_btn:
            data_azi = datetime.date.today().strftime("%d.%m.%Y")
            nr_raport = f"{datetime.datetime.now().strftime('%H%M%S')}"

            # Construieste prompt
            if tip_ales == "Raport control pe teren":
                obs_text = f"Observatii: {obs}" if obs else "Fara observatii suplimentare."
                prompt = config["prompt_template"].format(
                    fermier=fermier, judet=judet, parcela=parcela,
                    suprafata_dec=sup_dec, suprafata_mas=sup_mas,
                    diferenta=diferenta, concluzie=concluzie,
                    cultura=cultura, stare_fito=stare_fito,
                    ndvi=ndvi_v, obs=obs or "niciuna", data=data_azi,
                )
            elif tip_ales == "Notificare neconformitate":
                prompt = config["prompt_template"].format(
                    fermier=fermier, judet=judet, parcela=parcela,
                    suprafata_dec=sup_dec, suprafata_mas=sup_mas,
                    diferenta=diferenta, concluzie=concluzie,
                    tip_neconformitate=tip_nec, penalizare_pct=round(pen_pct, 1),
                    data=data_azi,
                )
            elif tip_ales == "Decizie de plata":
                prompt = config["prompt_template"].format(
                    fermier=fermier, judet=judet,
                    nr_parcele=nr_parc, suprafata_totala=sup_tot,
                    suma_solicitata=suma_sol, suma_aprobata=suma_apr,
                    reducere_pct=red_pct, data=data_azi,
                )
            else:
                prompt = config["prompt_template"].format(
                    fermier=fermier, judet=judet,
                    subiect=subiect, continut_adresa=continut, data=data_azi,
                )

            with st.spinner("LLM genereaza raportul..."):
                if ollama_ok:
                    ok, raport_text = genereaza_ollama(
                        model_selectat, prompt, config["system"]
                    )
                    if not ok:
                        raport_text = f"Eroare: {raport_text}"
                else:
                    time.sleep(1.5)
                    tmpl = DEMO_RAPOARTE.get(tip_ales, "Raport demo generat.\n[porneste Ollama pentru AI real]")
                    obs_text_d = f"Observatii: {obs}" if (tip_ales == "Raport control pe teren" and obs) else ""
                    raport_text = tmpl.format(
                        fermier=fermier, judet=judet,
                        parcela=parcela if tip_ales in ("Raport control pe teren", "Notificare neconformitate") else "—",
                        suprafata_dec=sup_dec if tip_ales in ("Raport control pe teren", "Notificare neconformitate") else "—",
                        suprafata_mas=sup_mas if tip_ales in ("Raport control pe teren", "Notificare neconformitate") else "—",
                        diferenta=diferenta if tip_ales in ("Raport control pe teren", "Notificare neconformitate") else 0,
                        concluzie=concluzie if tip_ales in ("Raport control pe teren", "Notificare neconformitate") else "—",
                        cultura=cultura if tip_ales == "Raport control pe teren" else "—",
                        stare_fito=stare_fito if tip_ales == "Raport control pe teren" else "—",
                        ndvi=ndvi_v if tip_ales == "Raport control pe teren" else "—",
                        obs_text=obs_text_d,
                        tip_neconformitate=tip_nec if tip_ales == "Notificare neconformitate" else "—",
                        penalizare_pct=round(pen_pct, 1) if tip_ales == "Notificare neconformitate" else 0,
                        nr_raport=nr_raport, data=data_azi,
                    )

            st.session_state.setdefault("istoric_rapoarte", []).append({
                "tip": tip_ales,
                "fermier": fermier,
                "data": data_azi,
                "text": raport_text,
            })

            st.markdown(
                f"<div style='background:#f8f9fa; border-radius:8px; padding:14px; "
                f"font-size:12px; line-height:1.8; border-left:4px solid {config['culoare']}; "
                f"white-space:pre-wrap; font-family:monospace; max-height:420px; "
                f"overflow-y:auto;'>{raport_text}</div>",
                unsafe_allow_html=True
            )
            st.download_button(
                "Descarca .txt",
                data=raport_text.encode("utf-8"),
                file_name=f"raport_{tip_ales[:8].replace(' ','_')}_{fermier.split()[0]}_{data_azi.replace('.','')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.info("Completeaza formularul si apasa Genereaza.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PROCESARE LOT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Procesare lot — rapoarte multiple automat")
    st.markdown(
        "Introdu datele pentru mai multi fermieri. LLM-ul genereaza rapoartele pe rand, "
        "una dupa alta. Ideal pentru sfarsitul campaniei PAC."
    )

    DATE_LOT_DEMO = [
        {"fermier": "Popescu Ion",     "parcela": "GJ-001-A", "sup_dec": 4.52, "sup_mas": 4.31,
         "cultura": "Grau",           "ndvi": 0.62, "stare": "Buna"},
        {"fermier": "Ionescu Maria",   "parcela": "GJ-045-B", "sup_dec": 7.20, "sup_mas": 6.94,
         "cultura": "Porumb",         "ndvi": 0.55, "stare": "Satisfacatoare"},
        {"fermier": "Stanescu Vasile", "parcela": "GJ-088-A", "sup_dec": 8.50, "sup_mas": 6.20,
         "cultura": "Grau",           "ndvi": 0.40, "stare": "Problematica"},
        {"fermier": "Dumitru Gh.",     "parcela": "GJ-103-C", "sup_dec": 2.10, "sup_mas": 2.08,
         "cultura": "Lucerna",        "ndvi": 0.70, "stare": "Buna"},
        {"fermier": "Marinescu Al.",   "parcela": "GJ-201-D", "sup_dec": 15.0, "sup_mas": 14.6,
         "cultura": "Floarea-soarelui","ndvi": 0.58, "stare": "Buna"},
    ]

    col_t, col_s = st.columns([3, 1])
    with col_t:
        st.markdown("**Date lot (editabile):**")
        try:
            import pandas as pd
            PANDAS_OK = True
        except ImportError:
            PANDAS_OK = False

        if PANDAS_OK:
            df_lot = st.data_editor(
                pd.DataFrame(DATE_LOT_DEMO),
                use_container_width=True,
                num_rows="dynamic",
                key="editor_lot"
            )
            date_lot = df_lot.to_dict("records")
        else:
            date_lot = DATE_LOT_DEMO
            for d in DATE_LOT_DEMO:
                dif = abs(d["sup_dec"] - d["sup_mas"]) / d["sup_dec"] * 100
                _, pen, col = calcul_penalizare(dif)
                st.markdown(
                    f"**{d['fermier']}** — {d['parcela']} — {dif:.1f}% — "
                    f"<span style='color:{col}'>{pen}%</span>",
                    unsafe_allow_html=True
                )

    with col_s:
        judet_lot = st.selectbox("Judet lot:", ["Gorj", "Dolj", "Olt", "Valcea"], key="jud_lot")
        tip_lot   = st.selectbox("Tip raport lot:", ["Raport control pe teren",
                                                      "Notificare neconformitate"], key="tip_lot")
        if st.button("Genereaza toate rapoartele", type="primary", use_container_width=True, key="btn_lot"):
            st.session_state["run_lot"] = True

    if st.session_state.get("run_lot"):
        st.session_state["run_lot"] = False
        st.markdown("---")
        st.markdown(f"**Generare {len(date_lot)} rapoarte...**")

        rapoarte_lot = []
        bара_progres = st.progress(0)
        status_text  = st.empty()

        for i, row in enumerate(date_lot):
            fermier_r = str(row.get("fermier", "Necunoscut"))
            parcela_r = str(row.get("parcela", "—"))
            sup_d     = float(row.get("sup_dec", 1.0))
            sup_m     = float(row.get("sup_mas", 1.0))
            cultura_r = str(row.get("cultura", "—"))
            ndvi_r    = float(row.get("ndvi", 0.5))
            stare_r   = str(row.get("stare", "Buna"))
            dif_r     = abs(sup_d - sup_m) / sup_d * 100 if sup_d > 0 else 0
            concl_r, pen_r, _ = calcul_penalizare(dif_r)

            status_text.markdown(f"Procesez {i+1}/{len(date_lot)}: **{fermier_r}**...")

            if ollama_ok:
                config_lot = TIPURI_RAPORT[tip_lot]
                if tip_lot == "Raport control pe teren":
                    prompt_lot = config_lot["prompt_template"].format(
                        fermier=fermier_r, judet=judet_lot, parcela=parcela_r,
                        suprafata_dec=sup_d, suprafata_mas=sup_m,
                        diferenta=dif_r, concluzie=concl_r,
                        cultura=cultura_r, stare_fito=stare_r,
                        ndvi=ndvi_r, obs="niciuna",
                        data=datetime.date.today().strftime("%d.%m.%Y"),
                    )
                else:
                    prompt_lot = config_lot["prompt_template"].format(
                        fermier=fermier_r, judet=judet_lot, parcela=parcela_r,
                        suprafata_dec=sup_d, suprafata_mas=sup_m,
                        diferenta=dif_r, concluzie=concl_r,
                        tip_neconformitate="Diferenta suprafata" if dif_r >= 3 else "Conforme",
                        penalizare_pct=round(pen_r, 1),
                        data=datetime.date.today().strftime("%d.%m.%Y"),
                    )
                ok, text_r = genereaza_ollama(model_selectat, prompt_lot, config_lot["system"])
                if not ok:
                    text_r = f"[EROARE] {text_r}"
            else:
                time.sleep(0.5)
                text_r = (
                    f"RAPORT {tip_lot.upper()} — {fermier_r}\n"
                    f"Parcela: {parcela_r} | Diferenta: {dif_r:.1f}% | {concl_r}\n"
                    f"Cultura: {cultura_r} | NDVI: {ndvi_r} | Stare: {stare_r}\n"
                    f"[DEMO — porneste Ollama pentru raport complet]"
                )

            rapoarte_lot.append({
                "fermier": fermier_r,
                "tip": tip_lot,
                "text": text_r,
                "diferenta": dif_r,
                "concluzie": concl_r,
            })
            bара_progres.progress((i + 1) / len(date_lot))

        status_text.success(f"Gata! {len(rapoarte_lot)} rapoarte generate.")

        for rap in rapoarte_lot:
            _, _, col_rap = calcul_penalizare(rap["diferenta"])
            with st.expander(f"{rap['fermier']} — {rap['diferenta']:.1f}% — {rap['concluzie']}"):
                st.markdown(
                    f"<div style='font-size:11px; font-family:monospace; "
                    f"white-space:pre-wrap; line-height:1.7;'>{rap['text']}</div>",
                    unsafe_allow_html=True
                )

        rapoarte_unite = "\n\n" + "="*60 + "\n\n".join(
            f"{r['fermier']} — {r['tip']}\n{r['text']}" for r in rapoarte_lot
        )
        st.download_button(
            f"Descarca toate {len(rapoarte_lot)} rapoartele .txt",
            data=rapoarte_unite.encode("utf-8"),
            file_name=f"lot_rapoarte_{datetime.date.today().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SABLOANE & PROMPTURI
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Sabloane de prompturi — inginerire prompt pentru APIA")
    st.markdown(
        "Promptul este 'instructiunea' data LLM-ului. Un prompt bun = raport bun. "
        "Invata sa scrii si sa modifici prompturi pentru uz propriu."
    )

    tip_sablon = st.selectbox("Tip sablon:", list(TIPURI_RAPORT.keys()), key="tip_sab")
    config_s   = TIPURI_RAPORT[tip_sablon]

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("**System prompt (rolul asistentului):**")
        system_editat = st.text_area("", value=config_s["system"], height=120, key="sys_edit")
        st.markdown("**Prompt template:**")
        prompt_editat = st.text_area("", value=config_s["prompt_template"], height=250, key="prm_edit")

    with col_s2:
        st.markdown("**Tehnici de prompt engineering:**")
        st.markdown("""
**1. Defineste rolul clar (system prompt)**
```
"Esti inspector APIA cu 20 ani experienta.
Raspunzi formal, in romana, cu terminologie PAC."
```

**2. Date structurate in prompt**
```
- Fermier: {fermier}
- Suprafata: {ha} ha
- Diferenta: {pct}%
```

**3. Specifica formatul output**
```
"Raportul trebuie sa contina:
I. Date identificare
II. Constatari
III. Concluzie
IV. Semnatura"
```

**4. Tone control**
```
"Ton formal dar accesibil fermierului."
"Foloseste terminologia Reg. UE 2021/2116."
```

**5. Lungime**
```
"Raport concis, max 300 cuvinte."
"Raport detaliat, minim 5 paragrafe."
```
""")

        if ollama_ok:
            st.markdown("**Test prompt personalizat:**")
            test_prompt = st.text_area(
                "Prompt de test:",
                "Genereaza un raport de control scurt pentru parcela GJ-999-Z, "
                "fermier Test Ion, suprafata declarata 5 ha, masurata 4.8 ha, cultura grau.",
                height=100, key="test_prm"
            )
            if st.button("Testeaza prompt", use_container_width=True, key="btn_test_prm"):
                with st.spinner("Generez..."):
                    ok, rez = genereaza_ollama(model_selectat, test_prompt, system_editat)
                if ok:
                    st.success("Raspuns LLM:")
                    st.markdown(
                        f"<div style='font-size:11px; font-family:monospace; "
                        f"white-space:pre-wrap; line-height:1.7; background:#f8f9fa; "
                        f"padding:10px; border-radius:6px;'>{rez}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.error(rez)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ISTORIC
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Istoric rapoarte generate in aceasta sesiune")

    istoric = st.session_state.get("istoric_rapoarte", [])

    if not istoric:
        st.info("Nu ai generat niciun raport inca. Foloseste tab-ul 'Generator individual'.")
    else:
        st.metric("Rapoarte generate in sesiune", len(istoric))

        for i, rap in enumerate(reversed(istoric)):
            config_i = TIPURI_RAPORT.get(rap["tip"], {"culoare": "#666"})
            with st.expander(
                f"[{len(istoric)-i}] {rap['tip']} — {rap['fermier']} — {rap['data']}"
            ):
                st.markdown(
                    f"<div style='font-size:11px; font-family:monospace; "
                    f"white-space:pre-wrap; line-height:1.7;'>{rap['text']}</div>",
                    unsafe_allow_html=True
                )
                st.download_button(
                    "Descarca .txt",
                    data=rap["text"].encode("utf-8"),
                    file_name=f"raport_{rap['fermier'].split()[0]}_{rap['data'].replace('.','')}.txt",
                    mime="text/plain",
                    key=f"dl_ist_{i}",
                )

        if st.button("Sterge istoricul sesiunii", key="btn_sterg_ist"):
            st.session_state["istoric_rapoarte"] = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Ziua 20 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### Concepte noi

**Prompt Engineering**
- System prompt = defineste rolul si comportamentul LLM
- User prompt = instructiunea concreta
- Template = prompt reutilizabil cu variabile `{fermier}`, `{suprafata}`
- Temperature = creativitate (0=precis, 1=creativ); pentru rapoarte formale: 0.1-0.3

**Structura apel Ollama pentru rapoarte:**
```python
requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "system": "Esti inspector APIA...",
    "prompt": f"Raport pentru {fermier}...",
    "stream": False,
    "options": {"temperature": 0.2}
})
```

**Procesare lot:**
```python
for fermier in lista_fermieri:
    prompt = template.format(**fermier)
    ok, raport = genereaza_ollama(model, prompt, system)
    salveaza(raport)
```
""")

    with col2:
        st.markdown("""
#### Impact practic APIA

**Fara AI (acum):**
- 1 raport control = 30–45 min redactare
- 200 rapoarte/an = 100–150 ore/inspector
- Stiluri diferite per inspector
- Erori de completare frecvente

**Cu LLM local (Z20):**
- 1 raport = 10–30 secunde
- 200 rapoarte = 1–2 ore
- Stil uniform, terminologie corecta
- Inspector verifica si semneaza, nu scrie

**ROI estimat per inspector/an:**
- Timp economisit: ~130 ore
- La 50 lei/ora = 6.500 lei economisiti
- Cost Ollama: 0 lei
""")
        st.markdown("""
<div style='background:#e8f8f5; border-radius:8px; padding:14px; margin-top:8px;
     border-top:3px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Concluzie Ziua 20</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.7;'>
LLM-ul local + template-uri bune = generator de rapoarte APIA
profesionale, gratuite, offline si confidentiale.
Inspector-ul devine validator, nu redactor.
<br><br>
Urmatoarea: <b>Ziua 21 — Generare imagini gratuit</b>.
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#27ae60 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 20 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
Generator APIA complet | 4 tipuri rapoarte | Procesare lot | Prompt engineering | Istoric sesiune
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 21 — Generare imagini gratuit (Stable Diffusion local)
</div>
</div>
""", unsafe_allow_html=True)
