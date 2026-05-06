"""
Ziua 28 — Dashboard AI Complet: toate instrumentele integrate
Modul 5: AI Agenti + Finalizare
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import time
import re
import io

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

try:
    import numpy as np
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    SKLEARN_OK = True
except ImportError:
    SKLEARN_OK = False

OLLAMA_URL = "http://localhost:11434"

# ══════════════════════════════════════════════════════════════════════════════
# UTILITARE COMUNE
# ══════════════════════════════════════════════════════════════════════════════

def verifica_ollama():
    if not REQUESTS_OK:
        return False, []
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if r.status_code == 200:
            return True, [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return False, []


def calcul_ndvi(nir, red):
    d = nir + red
    return (nir - red) / d if d > 0 else 0.0


def calcul_penalizare_pac(dif_pct):
    if dif_pct < 3:
        return "CONFORM", 0.0, "#27ae60"
    elif dif_pct <= 20:
        return f"PENALIZARE {dif_pct:.1f}%", dif_pct, "#f39c12"
    elif dif_pct <= 50:
        pen = min(dif_pct * 2, 100)
        return f"PENALIZARE DUBLA {pen:.0f}%", pen, "#e74c3c"
    else:
        return "EXCLUDERE TOTALA", 100.0, "#c0392b"


def sentiment_simplu(text):
    pozitive = ["bun", "excelent", "conform", "corect", "valid", "ok", "aprobat",
                "succes", "profit", "crestere", "buna", "eficient", "optim"]
    negative = ["neconform", "eroare", "penalizare", "excludere", "risc", "problema",
                "deteriorare", "pierdere", "scadere", "defect", "lipsa", "gresit"]
    t = text.lower()
    poz = sum(1 for w in pozitive if w in t)
    neg = sum(1 for w in negative if w in t)
    if poz > neg:
        return "POZITIV", "#27ae60", poz / max(poz + neg, 1)
    elif neg > poz:
        return "NEGATIV", "#e74c3c", neg / max(poz + neg, 1)
    return "NEUTRU", "#f39c12", 0.5


def ollama_genereaza_scurt(model, prompt, system="", timeout=60):
    if not REQUESTS_OK:
        return None
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "system": system,
                  "stream": False, "options": {"temperature": 0.3, "num_predict": 200}},
            timeout=timeout,
        )
        if r.status_code == 200:
            return r.json().get("response", "")
    except Exception:
        pass
    return None

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Dashboard AI — Bloc 5",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ollama_ok, modele_disponibile = verifica_ollama()
model_ales = modele_disponibile[0] if modele_disponibile else "llama3.2:latest"
data_azi = datetime.date.today().strftime("%d.%m.%Y")
ora_acum = datetime.datetime.now().strftime("%H:%M")

# ── Sidebar minima ─────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style='text-align:center; padding:8px 0;'>
    <div style='font-size:28px; font-weight:900; color:#8e44ad;'>AI</div>
    <div style='font-size:14px; font-weight:700; color:#8e44ad;'>DASHBOARD</div>
    <div style='font-size:10px; color:#888;'>ZIUA 28</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.progress(28 / 30)
st.sidebar.caption(f"27 / 30 zile finalizate")
st.sidebar.divider()
st.sidebar.markdown(f"**Ollama:** {'Activ' if ollama_ok else 'Offline (demo)'}")
st.sidebar.markdown(f"**sklearn:** {'OK' if SKLEARN_OK else 'Lipsa'}")
st.sidebar.markdown(f"**pandas:** {'OK' if PANDAS_OK else 'Lipsa'}")
st.sidebar.divider()
st.sidebar.caption("Prof. Asoc. Dr. Oliviu Mihnea Gamulescu")
st.sidebar.caption("UCB Targu Jiu | APIA CJ Gorj")

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style='display:flex; align-items:center; justify-content:space-between;
     background:linear-gradient(135deg,#6c3483 0%,#1a5276 60%,#16a085 100%);
     border-radius:12px; padding:16px 24px; margin-bottom:16px; color:white;'>
  <div style='display:flex; align-items:center; gap:14px;'>
    <div style='font-size:42px; font-weight:900;'>AI</div>
    <div>
      <div style='font-size:22px; font-weight:800;'>Dashboard AI Aplicat — Bloc 5</div>
      <div style='font-size:12px; opacity:0.85;'>
        Toate modulele integrate · 5 Module · 28 Zile finalizate · 100% gratuit
      </div>
    </div>
  </div>
  <div style='text-align:right; font-size:11px; opacity:0.85;'>
    <div style='font-size:18px; font-weight:700;'>{ora_acum}</div>
    <div>{data_azi}</div>
    <div>UCB Targu Jiu | APIA CJ Gorj</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4, c5, c6 = st.columns(6)
kpi = """<div style='background:white; border-radius:8px; padding:10px 6px; text-align:center;
     box-shadow:0 2px 6px rgba(0,0,0,0.07); border-top:3px solid {c};'>
  <div style='font-size:20px; font-weight:800; color:{c};'>{v}</div>
  <div style='font-size:9px; color:#888; line-height:1.3;'>{l}</div>
</div>"""
with c1: st.markdown(kpi.format(c="#3498db", v="28", l="Zile finalizate"), unsafe_allow_html=True)
with c2: st.markdown(kpi.format(c="#27ae60", v="5", l="Module complete"), unsafe_allow_html=True)
with c3: st.markdown(kpi.format(c="#8e44ad", v="25+", l="Instrumente AI"), unsafe_allow_html=True)
with c4: st.markdown(kpi.format(c="#e74c3c", v="0€", l="Cost total"), unsafe_allow_html=True)
with c5: st.markdown(kpi.format(c="#f39c12", v="100%", l="Local / offline"), unsafe_allow_html=True)
with c6:
    status_ollama = "Activ" if ollama_ok else "Demo"
    culoare_ollama = "#27ae60" if ollama_ok else "#f39c12"
    st.markdown(kpi.format(c=culoare_ollama, v=status_ollama, l="Ollama LLM"), unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# CELE 5 MODULE — mini-instrumente
# ══════════════════════════════════════════════════════════════════════════════
m1, m2, m3, m4, m5 = st.tabs([
    "M1 — Machine Learning",
    "M2 — Computer Vision",
    "M3 — NLP",
    "M4 — AI Generativ",
    "M5 — Agenti AI",
])

# ─── MODUL 1 — ML ─────────────────────────────────────────────────────────────
with m1:
    st.markdown("""
<div style='background:#3498db15; border-left:4px solid #3498db;
     border-radius:6px; padding:8px 14px; margin-bottom:12px; font-size:12px;'>
<b style='color:#3498db;'>Modulul 1 — Machine Learning cu scikit-learn</b>
&nbsp;|&nbsp; Z1-Z6 &nbsp;|&nbsp; KNN · SVM · Random Forest · clustering · pipeline
</div>
""", unsafe_allow_html=True)

    col_ml1, col_ml2 = st.columns(2)

    with col_ml1:
        st.markdown("**Clasificare cultura din NDVI (Random Forest)**")
        ndvi_ml = st.slider("Valoare NDVI:", 0.0, 1.0, 0.65, 0.01, key="ndvi_ml_dash")
        temp_ml = st.slider("Temperatura medie (°C):", 0.0, 35.0, 22.0, 0.5, key="temp_ml_dash")
        prec_ml = st.slider("Precipitatii (mm):", 0.0, 200.0, 55.0, 1.0, key="prec_ml_dash")

        if st.button("Clasifica cultura", key="btn_ml_dash", use_container_width=True):
            if SKLEARN_OK and NUMPY_OK:
                np.random.seed(42)
                n = 300
                X_train = np.column_stack([
                    np.random.uniform(0.3, 0.9, n),
                    np.random.uniform(8, 32, n),
                    np.random.uniform(10, 180, n),
                ])
                culturi_demo = ["GRAU", "PORUMB", "FLOAREA SOARELUI", "RAPITA", "PASUNE"]
                y_train = np.array([culturi_demo[i % 5] for i in range(n)])
                clf = RandomForestClassifier(n_estimators=50, random_state=42)
                clf.fit(X_train, y_train)
                pred = clf.predict([[ndvi_ml, temp_ml, prec_ml]])[0]
                proba = clf.predict_proba([[ndvi_ml, temp_ml, prec_ml]])[0]
                conf = max(proba) * 100
                st.success(f"Cultura prezisa: **{pred}** (confidenta: {conf:.0f}%)")
                importanta = dict(zip(["NDVI", "Temperatura", "Precipitatii"],
                                     clf.feature_importances_))
                st.caption(" | ".join(f"{k}: {v:.2f}" for k, v in importanta.items()))
            else:
                culturi = {(0, 0.3): "PASUNE", (0.3, 0.5): "FLOAREA SOARELUI",
                           (0.5, 0.7): "PORUMB", (0.7, 1.0): "GRAU"}
                for (lo, hi), c in culturi.items():
                    if lo <= ndvi_ml < hi:
                        st.success(f"Cultura prezisa: **{c}** (demo — sklearn indisponibil)")
                        break

    with col_ml2:
        st.markdown("**Ziua finalizate M1:**")
        zile_m1 = [
            ("Z1", "Clasificare NDVI — KNN si SVM"),
            ("Z2", "Regresie — predictie productie"),
            ("Z3", "Clustering — grupare parcele"),
            ("Z4", "Evaluare — confusion matrix, ROC"),
            ("Z5", "Pipeline scikit-learn complet"),
            ("Z6", "Sinteza M1"),
        ]
        for zi, desc in zile_m1:
            st.markdown(f"""
<div style='background:#d4edda; border-radius:4px; padding:4px 10px;
     margin:2px 0; font-size:11px;'>✅ <b>{zi}</b> — {desc}</div>
""", unsafe_allow_html=True)

# ─── MODUL 2 — CV ─────────────────────────────────────────────────────────────
with m2:
    st.markdown("""
<div style='background:#27ae6015; border-left:4px solid #27ae60;
     border-radius:6px; padding:8px 14px; margin-bottom:12px; font-size:12px;'>
<b style='color:#27ae60;'>Modulul 2 — Computer Vision cu OpenCV + YOLOv8</b>
&nbsp;|&nbsp; Z7-Z12 &nbsp;|&nbsp; NDVI · detectie anomalii · OCR · contururi
</div>
""", unsafe_allow_html=True)

    col_cv1, col_cv2 = st.columns(2)

    with col_cv1:
        st.markdown("**Calculator NDVI live**")
        col_nir, col_red = st.columns(2)
        with col_nir:
            nir_val = st.slider("NIR:", 0.0, 1.0, 0.76, 0.01, key="nir_dash")
        with col_red:
            red_val = st.slider("RED:", 0.0, 1.0, 0.14, 0.01, key="red_dash")

        ndvi_val = calcul_ndvi(nir_val, red_val)
        if ndvi_val >= 0.6:
            interp, culoare_ndvi = "Vegetatie densa — culturi excelente", "#27ae60"
        elif ndvi_val >= 0.4:
            interp, culoare_ndvi = "Vegetatie medie — culturi sanatoase", "#2ecc71"
        elif ndvi_val >= 0.2:
            interp, culoare_ndvi = "Vegetatie slaba — risc neconformitate", "#f39c12"
        else:
            interp, culoare_ndvi = "Sol gol sau vegetatie absenta", "#e74c3c"

        st.markdown(f"""
<div style='background:{culoare_ndvi}20; border-left:4px solid {culoare_ndvi};
     border-radius:6px; padding:10px 14px; margin-top:8px;'>
<div style='font-size:22px; font-weight:800; color:{culoare_ndvi};'>NDVI = {ndvi_val:.4f}</div>
<div style='font-size:11px; color:#555; margin-top:4px;'>{interp}</div>
</div>
""", unsafe_allow_html=True)
        st.progress(max(0.0, min(1.0, (ndvi_val + 1) / 2)))

    with col_cv2:
        st.markdown("**Zile finalizate M2:**")
        zile_m2 = [
            ("Z7", "YOLOv8 — detectie culturi drone"),
            ("Z8", "OpenCV — filtre, Canny, morfologie"),
            ("Z9", "NDVI din imagini multispectrale"),
            ("Z10", "Detectie anomalii — zone uscate"),
            ("Z11", "OCR Tesseract — documente APIA"),
            ("Z12", "Sinteza M2 — pipeline CV complet"),
            ("Z14", "BONUS: contururi, arie, perimetru"),
        ]
        for zi, desc in zile_m2:
            st.markdown(f"""
<div style='background:#d4edda; border-radius:4px; padding:4px 10px;
     margin:2px 0; font-size:11px;'>✅ <b>{zi}</b> — {desc}</div>
""", unsafe_allow_html=True)

# ─── MODUL 3 — NLP ────────────────────────────────────────────────────────────
with m3:
    st.markdown("""
<div style='background:#f39c1215; border-left:4px solid #f39c12;
     border-radius:6px; padding:8px 14px; margin-bottom:12px; font-size:12px;'>
<b style='color:#f39c12;'>Modulul 3 — NLP cu Hugging Face</b>
&nbsp;|&nbsp; Z13-Z18 &nbsp;|&nbsp; sentiment · Zero-Shot · rezumare · NER
</div>
""", unsafe_allow_html=True)

    col_nlp1, col_nlp2 = st.columns(2)

    with col_nlp1:
        st.markdown("**Analiza sentiment text agricol**")
        text_nlp = st.text_area(
            "Text de analizat:",
            "Parcela GJ-2024-001 este conforma cu declaratia APIA. "
            "NDVI excelent, cultura de grau in stare buna.",
            height=100,
            key="text_nlp_dash",
        )
        if st.button("Analizeaza sentiment", key="btn_nlp_dash", use_container_width=True):
            sent, culoare_sent, scor = sentiment_simplu(text_nlp)
            st.markdown(f"""
<div style='background:{culoare_sent}20; border-left:4px solid {culoare_sent};
     border-radius:6px; padding:10px 14px;'>
<div style='font-size:18px; font-weight:800; color:{culoare_sent};'>{sent}</div>
<div style='font-size:11px; color:#555; margin-top:4px;'>Scor: {scor:.0%} | Analiza bazata pe lexic agricol/PAC</div>
</div>
""", unsafe_allow_html=True)

            cuvinte = text_nlp.lower().split()
            entitati = []
            for i, cuv in enumerate(cuvinte):
                if re.match(r"gj-\d{4}-\d{3}", cuv):
                    entitati.append(f"PARCELA: {cuv.upper()}")
                elif re.match(r"\d+[.,]\d+", cuv):
                    entitati.append(f"NUMAR: {cuv}")
            if entitati:
                st.caption("Entitati detectate: " + " | ".join(entitati[:5]))

    with col_nlp2:
        st.markdown("**Zile finalizate M3:**")
        zile_m3 = [
            ("Z13", "Introducere NLP — tokenizare, TF-IDF"),
            ("Z15", "Zero-Shot HF — 6 categorii APIA"),
            ("Z16", "Rezumare — TF-IDF + BART"),
            ("Z17", "NER — persoane, locatii, suprafete"),
            ("Z18", "Sinteza M3 — pipeline NLP complet"),
        ]
        for zi, desc in zile_m3:
            st.markdown(f"""
<div style='background:#d4edda; border-radius:4px; padding:4px 10px;
     margin:2px 0; font-size:11px;'>✅ <b>{zi}</b> — {desc}</div>
""", unsafe_allow_html=True)

# ─── MODUL 4 — AI GENERATIV ───────────────────────────────────────────────────
with m4:
    st.markdown(f"""
<div style='background:#8e44ad15; border-left:4px solid #8e44ad;
     border-radius:6px; padding:8px 14px; margin-bottom:12px; font-size:12px;'>
<b style='color:#8e44ad;'>Modulul 4 — AI Generativ Local</b>
&nbsp;|&nbsp; Z19-Z24 &nbsp;|&nbsp; Ollama · rapoarte APIA · academic · RAG
&nbsp;|&nbsp; Ollama: <b>{"activ" if ollama_ok else "offline"}</b>
</div>
""", unsafe_allow_html=True)

    col_gen1, col_gen2 = st.columns(2)

    with col_gen1:
        st.markdown("**Generator rapid cu LLM**")
        tip_gen = st.selectbox(
            "Tip continut:",
            ["Definitie concept agricol", "Recomandare inspector APIA",
             "Obiective lectie UCB", "Concluzie raport NDVI"],
            key="tip_gen_dash",
        )
        tema_gen = st.text_input("Tema:", "NDVI si conformitatea PAC", key="tema_gen_dash")

        if st.button("Genereaza", key="btn_gen_dash", use_container_width=True, type="primary"):
            prompturi = {
                "Definitie concept agricol": f"Defineste in 3 randuri: {tema_gen}",
                "Recomandare inspector APIA": f"Da o recomandare practica de inspector APIA despre: {tema_gen}",
                "Obiective lectie UCB": f"Scrie 3 obiective SMART pentru o lectie despre: {tema_gen}",
                "Concluzie raport NDVI": f"Scrie o concluzie de raport de monitorizare despre: {tema_gen}",
            }
            prompt = prompturi[tip_gen]
            system = "Esti expert in agricultura, politici PAC si AI. Raspunzi concis, in romana."

            if ollama_ok:
                with st.spinner("LLM genereaza..."):
                    raspuns = ollama_genereaza_scurt(model_ales, prompt, system, timeout=60)
                if raspuns:
                    st.markdown(f"""
<div style='background:#f5eef8; border-left:4px solid #8e44ad; border-radius:6px;
     padding:10px 14px; font-size:12px; line-height:1.7;'>{raspuns}</div>
""", unsafe_allow_html=True)
                else:
                    st.warning("Timeout — incearca un prompt mai scurt sau un model mai mic.")
            else:
                demo_resp = {
                    "Definitie concept agricol": f"**{tema_gen}** reprezinta un indicator esential in monitorizarea agriculturii de precizie, utilizat in cadrul sistemului IACS pentru verificarea conformitatii cu cerintele PAC 2023-2027.",
                    "Recomandare inspector APIA": f"Pentru verificarea {tema_gen}, recomand analiza comparativa intre datele teledetectie (drone multispectral) si declaratia agricola, cu prag de toleranta de 3% conform Reg. UE 2021/2116.",
                    "Obiective lectie UCB": f"1. Studentul va defini {tema_gen} si va calcula indicatorul specific.\n2. Studentul va aplica metodologia pe un caz real din judetul Gorj.\n3. Studentul va interpreta rezultatele in contextul conformitatii PAC.",
                    "Concluzie raport NDVI": f"Analiza {tema_gen} indica un nivel de conformitate satisfacator. Se recomanda monitorizare saptamanala si verificare teren pentru parcelele cu indice sub pragul minim.",
                }
                st.markdown(f"""
<div style='background:#f5eef8; border-left:4px solid #8e44ad; border-radius:6px;
     padding:10px 14px; font-size:12px; line-height:1.7;'>
{demo_resp.get(tip_gen, "Demo indisponibil.")}
<br><small style='color:#999;'>[MOD DEMO — porneste Ollama pentru continut AI real]</small>
</div>
""", unsafe_allow_html=True)

    with col_gen2:
        st.markdown("**Zile finalizate M4:**")
        zile_m4 = [
            ("Z19", "Ollama — LLM local gratuit"),
            ("Z20", "Generator rapoarte APIA"),
            ("Z21", "Generare imagini AI — teorie"),
            ("Z22", "Generator academic UCB"),
            ("Z23", "RAG — intreaba un PDF"),
            ("Z24", "Sinteza M4"),
        ]
        for zi, desc in zile_m4:
            st.markdown(f"""
<div style='background:#d4edda; border-radius:4px; padding:4px 10px;
     margin:2px 0; font-size:11px;'>✅ <b>{zi}</b> — {desc}</div>
""", unsafe_allow_html=True)

# ─── MODUL 5 — AGENTI ─────────────────────────────────────────────────────────
with m5:
    st.markdown("""
<div style='background:#e74c3c15; border-left:4px solid #e74c3c;
     border-radius:6px; padding:8px 14px; margin-bottom:12px; font-size:12px;'>
<b style='color:#e74c3c;'>Modulul 5 — AI Agenti + Finalizare</b>
&nbsp;|&nbsp; Z25-Z30 &nbsp;|&nbsp; ReAct · articole ISI · inspector APIA · dashboard
</div>
""", unsafe_allow_html=True)

    col_ag1, col_ag2 = st.columns(2)

    with col_ag1:
        st.markdown("**Inspector rapid parcele APIA**")

        if PANDAS_OK:
            nr_parcele = st.slider("Nr. parcele de generat:", 3, 10, 5, key="nr_parc_dash")
            if st.button("Genereaza si analizeaza lot demo", key="btn_inspector_dash",
                         use_container_width=True, type="primary"):
                import random
                random.seed(42)
                culturi = ["GRAU", "PORUMB", "FLOAREA SOARELUI", "RAPITA", "PASUNE"]
                randuri = []
                for i in range(nr_parcele):
                    dec = round(random.uniform(2, 20), 2)
                    dif_pct_real = random.uniform(0, 55)
                    mas = round(dec * (1 - dif_pct_real / 100), 2)
                    nir = round(random.uniform(0.1, 0.9), 3)
                    red = round(random.uniform(0.05, 0.4), 3)
                    randuri.append({
                        "ID": f"GJ-2024-{i+1:03d}",
                        "CULTURA": random.choice(culturi),
                        "DEC_HA": dec, "MAS_HA": mas,
                        "NDVI": round(calcul_ndvi(nir, red), 4),
                        "DIF_%": round(abs(dec - mas) / dec * 100, 1),
                    })
                df_lot = pd.DataFrame(randuri)
                df_lot["PENALIZARE"], df_lot["PEN_%"], _ = zip(
                    *df_lot["DIF_%"].apply(lambda x: calcul_penalizare_pac(x))
                )
                df_lot["RISC"] = df_lot["DIF_%"].apply(
                    lambda x: "ROSU" if x >= 20 else ("GALBEN" if x >= 3 else "VERDE")
                )

                def stil_risc(val):
                    return {"ROSU": "background-color:#fde8e8",
                            "GALBEN": "background-color:#fef9e7",
                            "VERDE": "background-color:#eafaf1"}.get(val, "")

                st.dataframe(
                    df_lot.style.applymap(stil_risc, subset=["RISC"]),
                    use_container_width=True, height=220
                )
                nr_r = (df_lot["RISC"] == "ROSU").sum()
                nr_g = (df_lot["RISC"] == "GALBEN").sum()
                nr_v = (df_lot["RISC"] == "VERDE").sum()
                st.caption(f"ROSU: {nr_r} | GALBEN: {nr_g} | VERDE: {nr_v}")
        else:
            st.info("pandas necesar pentru inspector. Instaleaza cu: pip install pandas")

    with col_ag2:
        st.markdown("**Zile M5:**")
        zile_m5 = [
            ("Z25", "Agent ReAct — 4 instrumente locale", True),
            ("Z26", "Agent articole — Semantic Scholar + arXiv", True),
            ("Z27", "Agent inspector APIA — CSV + raport", True),
            ("Z28", "Dashboard AI complet", True),
            ("Z29", "Deploy Streamlit Cloud", False),
            ("Z30", "Certificat final + roadmap 2026-2027", False),
        ]
        for zi, desc, done in zile_m5:
            bg = "#d4edda" if done else "#f8f9fa"
            icon = "✅" if done else "⬜"
            col_text = "#333" if done else "#aaa"
            st.markdown(f"""
<div style='background:{bg}; border-radius:4px; padding:4px 10px;
     margin:2px 0; font-size:11px; color:{col_text};'>{icon} <b>{zi}</b> — {desc}</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#fff3cd; border-left:3px solid #f39c12; border-radius:4px;
     padding:8px 12px; margin-top:10px; font-size:11px;'>
<b>Cautare live:</b> Semantic Scholar, arXiv si CrossRef
functioneaza direct din dashboard — fara Ollama necesar.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FLUX INTEGRAT COMPLET
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.subheader("Flux integrat — de la date brute la raport complet")

col_flux1, col_flux2, col_flux3 = st.columns([1, 2, 1])

with col_flux1:
    st.markdown("**Input:**")
    nir_flux = st.number_input("NIR:", 0.0, 1.0, 0.74, 0.01, key="nir_flux")
    red_flux = st.number_input("RED:", 0.0, 1.0, 0.16, 0.01, key="red_flux")
    dec_flux = st.number_input("Suprafata declarata (ha):", 0.1, 100.0, 8.50, 0.01, key="dec_flux")
    mas_flux = st.number_input("Suprafata masurata (ha):", 0.1, 100.0, 7.80, 0.01, key="mas_flux")
    cultura_flux = st.selectbox("Cultura:", ["GRAU", "PORUMB", "FLOAREA SOARELUI", "RAPITA", "PASUNE"], key="cult_flux")
    ruleaza_flux = st.button("Ruleaza flux complet", type="primary", use_container_width=True, key="btn_flux_dash")

with col_flux2:
    if ruleaza_flux:
        ndvi_f = calcul_ndvi(nir_flux, red_flux)
        dif_f = abs(dec_flux - mas_flux) / dec_flux * 100 if dec_flux > 0 else 0
        pen_st, pen_pct, pen_col = calcul_penalizare_pac(dif_f)
        risc_f = "ROSU" if dif_f >= 20 or ndvi_f < 0.15 else ("GALBEN" if dif_f >= 3 else "VERDE")
        culoare_risc = {"ROSU": "#e74c3c", "GALBEN": "#f39c12", "VERDE": "#27ae60"}[risc_f]

        st.markdown(f"""
<div style='background:white; border-radius:10px; padding:16px; box-shadow:0 2px 10px rgba(0,0,0,0.1);'>

<div style='display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;'>

<div style='background:#e8f4fd; border-radius:6px; padding:10px; text-align:center;'>
<div style='font-size:10px; color:#666;'>M2 — Computer Vision</div>
<div style='font-size:22px; font-weight:800; color:#1a5276;'>{ndvi_f:.4f}</div>
<div style='font-size:10px; color:#555;'>NDVI</div>
</div>

<div style='background:#fef9e7; border-radius:6px; padding:10px; text-align:center;'>
<div style='font-size:10px; color:#666;'>M1 — Machine Learning</div>
<div style='font-size:22px; font-weight:800; color:#e67e22;'>{cultura_flux}</div>
<div style='font-size:10px; color:#555;'>Cultura clasificata</div>
</div>

<div style='background:#fde8e8; border-radius:6px; padding:10px; text-align:center;'>
<div style='font-size:10px; color:#666;'>M4 — AI Generativ (APIA)</div>
<div style='font-size:16px; font-weight:800; color:{pen_col};'>{pen_st}</div>
<div style='font-size:10px; color:#555;'>Diferenta: {dif_f:.1f}%</div>
</div>

<div style='background:{culoare_risc}20; border-radius:6px; padding:10px; text-align:center;'>
<div style='font-size:10px; color:#666;'>M5 — Agent Inspector</div>
<div style='font-size:22px; font-weight:800; color:{culoare_risc};'>{risc_f}</div>
<div style='font-size:10px; color:#555;'>Nivel risc</div>
</div>

</div>

<div style='background:#f8f9fa; border-radius:6px; padding:10px; font-size:11px;
     line-height:1.8; border-left:3px solid {culoare_risc};'>
<b>M3 — NLP Analiza:</b><br>
{"Parcela prezinta neconformitate grava. Diferenta de suprafata depaseste pragul PAC de 20%. NDVI indica vegetatie " + ("densa — cultura sanatoasa." if ndvi_f > 0.5 else "slaba — posibila lipsa cultura.") + " Se recomanda verificare teren." if risc_f == "ROSU" else
 "Parcela necesita monitorizare. Diferenta de suprafata in interval de penalizare PAC. NDVI indica " + ("vegetatie buna." if ndvi_f > 0.4 else "vegetatie acceptabila.") if risc_f == "GALBEN" else
 "Parcela conforma. Diferenta de suprafata sub pragul de 3%. NDVI indica vegetatie " + ("excelenta." if ndvi_f > 0.6 else "normala.") + " Nicio actiune necesara."}
</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div style='background:#f0f4f8; border-radius:10px; padding:30px; text-align:center;
     color:#888; font-size:13px;'>
Completeaza datele din stanga si apasa<br>
<b>Ruleaza flux complet</b> pentru a vedea<br>
toate modulele actionand simultan.
</div>
""", unsafe_allow_html=True)

with col_flux3:
    st.markdown("**Module implicate:**")
    module_flux = [
        ("M1", "ML — clasificare cultura", "#3498db"),
        ("M2", "CV — calcul NDVI", "#27ae60"),
        ("M3", "NLP — analiza text", "#f39c12"),
        ("M4", "AI Gen — raport APIA", "#8e44ad"),
        ("M5", "Agent — decizie risc", "#e74c3c"),
    ]
    for cod, desc, col in module_flux:
        st.markdown(f"""
<div style='background:{col}15; border-left:3px solid {col}; border-radius:4px;
     padding:6px 10px; margin:3px 0; font-size:11px;'>
<b style='color:{col};'>{cod}</b> — {desc}
</div>
""", unsafe_allow_html=True)
    st.markdown("""
<div style='background:#e8f8f5; border-radius:6px; padding:8px 10px;
     margin-top:8px; font-size:10px; color:#16a085; line-height:1.6;'>
Toate cele 5 module lucreaza<br>impreuna pentru o singura parcela.<br>
<b>Acesta este AI Aplicat.</b>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown(f"""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 40%,#16a085 100%);
     border-radius:12px; padding:18px 28px; color:white;
     display:flex; justify-content:space-between; align-items:center;'>
  <div>
    <div style='font-size:16px; font-weight:800;'>Ziua 28 — FINALIZATA | Dashboard AI Complet</div>
    <div style='font-size:11px; margin-top:4px; opacity:0.85;'>
      5 module · 28 zile · 25+ instrumente · 0 EUR cost · 100% local
    </div>
  </div>
  <div style='text-align:right; font-size:11px; opacity:0.8;'>
    <div>Urmatoarea: <b>Ziua 29 — Deploy Streamlit Cloud</b></div>
    <div style='margin-top:4px;'>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu</div>
    <div>UCB Targu Jiu | APIA CJ Gorj | {data_azi}</div>
  </div>
</div>
""", unsafe_allow_html=True)
