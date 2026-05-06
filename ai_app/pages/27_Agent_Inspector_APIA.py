"""
Ziua 27 — Agent Inspector APIA: analizeaza parcele din fisier CSV
Modul 5: AI Agenti + Finalizare
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import time
import io
import re

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

OLLAMA_URL = "http://localhost:11434"

# ══════════════════════════════════════════════════════════════════════════════
# DATE DEMO — 12 parcele judetul Gorj (fictive, dar realiste)
# ══════════════════════════════════════════════════════════════════════════════

CSV_DEMO = """ID_PARCELA,SUPRAFATA_DECLARATA_HA,SUPRAFATA_MASURATA_HA,NIR,RED,CULTURA,UAT,LATITUDINE,LONGITUDINE
GJ-2024-001,5.32,5.18,0.76,0.14,GRAU,TARGU JIU,45.0398,23.2765
GJ-2024-002,12.75,11.20,0.23,0.21,PORUMB,ROVINARI,44.9123,23.1987
GJ-2024-003,3.80,3.76,0.68,0.18,FLOAREA SOARELUI,MOTRU,44.8012,22.9834
GJ-2024-004,8.45,7.10,0.31,0.28,RAPITA,TARGU JIU,45.0501,23.3102
GJ-2024-005,22.10,21.85,0.72,0.15,GRAU,TG CARBUNESTI,44.9657,23.5021
GJ-2024-006,6.90,5.85,0.19,0.17,PASUNE,NOVACI,45.1703,23.6891
GJ-2024-007,4.15,4.12,0.81,0.11,GRAU,BUMBESTI JIU,45.1892,23.3765
GJ-2024-008,15.30,14.95,0.65,0.22,PORUMB,ROVINARI,44.9234,23.2145
GJ-2024-009,7.20,3.80,0.14,0.13,PASUNE,PADES,44.7012,22.7523
GJ-2024-010,9.85,9.71,0.59,0.25,FLOAREA SOARELUI,TARGU JIU,45.0287,23.2901
GJ-2024-011,18.60,16.80,0.42,0.31,PORUMB,MOTRU,44.8234,22.9102
GJ-2024-012,2.40,2.38,0.88,0.09,LIVADA,BUMBESTI JIU,45.2012,23.4023
"""

# ══════════════════════════════════════════════════════════════════════════════
# LOGICA ANALIZA PAC / NDVI
# ══════════════════════════════════════════════════════════════════════════════

CULTURI_NDVI_MIN = {
    "GRAU": 0.35, "PORUMB": 0.30, "FLOAREA SOARELUI": 0.25,
    "RAPITA": 0.28, "PASUNE": 0.20, "LIVADA": 0.40,
}

def calcul_ndvi(nir: float, red: float) -> float:
    denom = nir + red
    return (nir - red) / denom if denom > 0 else 0.0


def interpreteaza_ndvi(ndvi: float, cultura: str) -> tuple:
    prag = CULTURI_NDVI_MIN.get(cultura.upper().strip(), 0.25)
    if ndvi >= 0.6:
        return "EXCELENT", "#27ae60"
    elif ndvi >= 0.4:
        return "BUN", "#2ecc71"
    elif ndvi >= prag:
        return "ACCEPTABIL", "#f39c12"
    elif ndvi >= 0.15:
        return "SLAB — risc neconformitate", "#e67e22"
    else:
        return "CRITIC — posibil sol gol", "#e74c3c"


def calcul_diferenta_pct(declarata: float, masurata: float) -> float:
    if declarata <= 0:
        return 0.0
    return abs(declarata - masurata) / declarata * 100


def calcul_penalizare(dif_pct: float) -> tuple:
    if dif_pct < 3:
        return "CONFORM", 0.0, "#27ae60"
    elif dif_pct <= 20:
        return f"PENALIZARE {dif_pct:.1f}%", dif_pct, "#f39c12"
    elif dif_pct <= 50:
        pen = min(dif_pct * 2, 100)
        return f"PENALIZARE DUBLA {pen:.0f}%", pen, "#e74c3c"
    else:
        return "EXCLUDERE TOTALA", 100.0, "#c0392b"


def nivel_risc(dif_pct: float, ndvi: float, cultura: str) -> tuple:
    prag_ndvi = CULTURI_NDVI_MIN.get(cultura.upper().strip(), 0.25)
    if dif_pct >= 20 or ndvi < 0.15:
        return "ROSU", "#e74c3c"
    elif dif_pct >= 3 or ndvi < prag_ndvi:
        return "GALBEN", "#f39c12"
    else:
        return "VERDE", "#27ae60"


def analizeaza_df(df: "pd.DataFrame") -> "pd.DataFrame":
    rezultate = []
    for _, rand in df.iterrows():
        try:
            dec = float(rand["SUPRAFATA_DECLARATA_HA"])
            mas = float(rand["SUPRAFATA_MASURATA_HA"])
            nir = float(rand["NIR"])
            red = float(rand["RED"])
            cultura = str(rand.get("CULTURA", "?")).upper().strip()

            ndvi = calcul_ndvi(nir, red)
            ndvi_status, _ = interpreteaza_ndvi(ndvi, cultura)
            dif_pct = calcul_diferenta_pct(dec, mas)
            pen_status, pen_pct, _ = calcul_penalizare(dif_pct)
            risc, _ = nivel_risc(dif_pct, ndvi, cultura)

            rezultate.append({
                "ID_PARCELA":   rand.get("ID_PARCELA", "?"),
                "CULTURA":      cultura,
                "UAT":          rand.get("UAT", "?"),
                "DEC_HA":       round(dec, 2),
                "MAS_HA":       round(mas, 2),
                "DIF_PCT":      round(dif_pct, 2),
                "NDVI":         round(ndvi, 4),
                "NDVI_STATUS":  ndvi_status,
                "PENALIZARE":   pen_status,
                "PEN_PCT":      round(pen_pct, 1),
                "RISC":         risc,
            })
        except Exception as e:
            rezultate.append({
                "ID_PARCELA": rand.get("ID_PARCELA", "?"),
                "CULTURA": "EROARE", "UAT": "", "DEC_HA": 0, "MAS_HA": 0,
                "DIF_PCT": 0, "NDVI": 0, "NDVI_STATUS": str(e),
                "PENALIZARE": "EROARE", "PEN_PCT": 0, "RISC": "EROARE",
            })
    return pd.DataFrame(rezultate)

# ══════════════════════════════════════════════════════════════════════════════
# OLLAMA
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


def genereaza_raport_text(df_rez: "pd.DataFrame", model: str, tema: str = "") -> str:
    rosu = df_rez[df_rez["RISC"] == "ROSU"]
    galben = df_rez[df_rez["RISC"] == "GALBEN"]
    verde = df_rez[df_rez["RISC"] == "VERDE"]

    rezumat_date = (
        f"Total parcele analizate: {len(df_rez)}\n"
        f"RISC ROSU: {len(rosu)} parcele\n"
        f"RISC GALBEN: {len(galben)} parcele\n"
        f"RISC VERDE: {len(verde)} parcele\n\n"
        f"Parcele cu risc ridicat:\n"
    )
    for _, r in rosu.iterrows():
        rezumat_date += (
            f"- {r['ID_PARCELA']}: {r['CULTURA']}, UAT {r['UAT']}, "
            f"diferenta {r['DIF_PCT']}%, NDVI {r['NDVI']}, "
            f"penalizare {r['PENALIZARE']}\n"
        )

    prompt = (
        f"Genereaza un raport de control APIA pe baza urmatoarelor date:\n\n"
        f"{rezumat_date}\n"
        f"Raportul trebuie sa contina:\n"
        f"1. Concluzii generale (2-3 randuri)\n"
        f"2. Parcele cu risc rosu — descriere si recomandare per parcela\n"
        f"3. Recomandari generale pentru sezonul urmator\n"
        f"Stil oficial, concis, max 400 cuvinte."
    )
    system = (
        "Esti inspector APIA cu 20 ani experienta. "
        "Redactezi rapoarte de control conform procedurilor APIA. "
        "Limbaj oficial, obiectiv, fara speculatii."
    )
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "system": system,
                  "stream": False, "options": {"temperature": 0.2}},
            timeout=240,
        )
        if r.status_code == 200:
            return r.json().get("response", "")
        return f"Eroare Ollama {r.status_code}"
    except Exception as e:
        return f"Eroare: {e}"


def raport_demo(df_rez: "pd.DataFrame") -> str:
    rosu = df_rez[df_rez["RISC"] == "ROSU"]
    galben = df_rez[df_rez["RISC"] == "GALBEN"]
    verde = df_rez[df_rez["RISC"] == "VERDE"]
    linii_rosu = []
    for _, r in rosu.iterrows():
        linii_rosu.append(
            f"  - Parcela {r['ID_PARCELA']} ({r['CULTURA']}, {r['UAT']}): "
            f"diferenta suprafata {r['DIF_PCT']}%, NDVI {r['NDVI']} — {r['PENALIZARE']}"
        )
    return (
        f"RAPORT CONTROL APIA — {datetime.date.today().strftime('%d.%m.%Y')}\n"
        f"[MOD DEMO — porneste Ollama pentru raport generat de AI]\n\n"
        f"CONCLUZII GENERALE:\n"
        f"Din cele {len(df_rez)} parcele analizate, {len(rosu)} prezinta neconformitati grave "
        f"(risc rosu), {len(galben)} necesita monitorizare (risc galben) si "
        f"{len(verde)} sunt conforme (risc verde).\n\n"
        f"PARCELE CU RISC ROSU ({len(rosu)}):\n" +
        ("\n".join(linii_rosu) if linii_rosu else "  Nicio parcela cu risc rosu.") +
        f"\n\nRECOMANDARI:\n"
        f"  1. Verificare teren imediat pentru parcelele cu risc rosu\n"
        f"  2. Solicitare documente justificative pentru diferente > 20%\n"
        f"  3. Monitorizare NDVI saptamanal pentru parcelele cu risc galben\n"
    )

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 27 — Agent Inspector APIA",
    page_icon="APIA",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not PANDAS_OK:
    st.error("pandas nu este instalat. Ruleaza: pip install pandas")
    st.stop()

ollama_ok, modele_disponibile = verifica_ollama()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:26px; font-weight:900; color:#1a5276;'>APIA</div>
    <div style='font-size:16px; font-weight:700; color:#1a5276;'>ZIUA 27</div>
    <div style='font-size:11px; color:#666;'>Agent Inspector Parcele</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 5 — AI Agenti + Finalizare")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 27 / 30 zile")
st.sidebar.progress(27 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_ales = st.sidebar.selectbox("Model:", modele_disponibile or ["llama3.2:latest"])
else:
    st.sidebar.warning("Ollama offline — analiza disponibila, raport = demo")
    model_ales = "llama3.2:latest"

st.sidebar.markdown("""
**Coloane CSV obligatorii:**
- `ID_PARCELA`
- `SUPRAFATA_DECLARATA_HA`
- `SUPRAFATA_MASURATA_HA`
- `NIR` (0-1)
- `RED` (0-1)
- `CULTURA`
- `UAT`
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#1a5276; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj<br>
<b>Experienta:</b> Inspector principal 20+ ani
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:36px; font-weight:900; color:#1a5276;'>APIA</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1a5276; font-weight:800;'>
            Ziua 27 — Agent Inspector APIA
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            CSV parcele → NDVI + diferente suprafete + penalizari PAC → raport neconformitati
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Incarca parcele",
    "Analiza automata",
    "Raport neconformitati",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INCARCARE CSV
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Incarca fisier CSV cu parcele agricole")

    col_upload, col_demo = st.columns([1, 1])

    with col_upload:
        fisier = st.file_uploader(
            "Incarca CSV cu parcele:",
            type=["csv"],
            key="fisier_csv_apia",
            help="Coloane necesare: ID_PARCELA, SUPRAFATA_DECLARATA_HA, SUPRAFATA_MASURATA_HA, NIR, RED, CULTURA, UAT"
        )
        if fisier:
            try:
                df_incarcat = pd.read_csv(fisier)
                st.success(f"Fisier incarcat: {len(df_incarcat)} parcele")
                st.dataframe(df_incarcat.head(5), use_container_width=True)
                st.session_state["df_parcele"] = df_incarcat
            except Exception as e:
                st.error(f"Eroare citire CSV: {e}")

    with col_demo:
        st.markdown("**Date demo — 12 parcele judetul Gorj:**")
        st.code(CSV_DEMO[:400] + "\n...", language=None)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("Incarca date demo", type="primary", use_container_width=True, key="btn_demo_csv"):
                df_demo = pd.read_csv(io.StringIO(CSV_DEMO))
                st.session_state["df_parcele"] = df_demo
                st.success(f"{len(df_demo)} parcele demo incarcate!")
                st.rerun()
        with col_d2:
            st.download_button(
                "Descarca CSV demo",
                data=CSV_DEMO.encode("utf-8"),
                file_name="parcele_demo_gorj.csv",
                mime="text/csv",
                use_container_width=True,
            )

    if "df_parcele" in st.session_state:
        df_curent = st.session_state["df_parcele"]
        st.divider()
        st.subheader(f"Date incarcate: {len(df_curent)} parcele")
        st.dataframe(df_curent, use_container_width=True, height=300)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total parcele", len(df_curent))
        with c2:
            total_dec = df_curent["SUPRAFATA_DECLARATA_HA"].sum() if "SUPRAFATA_DECLARATA_HA" in df_curent.columns else 0
            st.metric("Suprafata declarata totala", f"{total_dec:.2f} ha")
        with c3:
            culturi_unice = df_curent["CULTURA"].nunique() if "CULTURA" in df_curent.columns else 0
            st.metric("Culturi distincte", culturi_unice)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALIZA AUTOMATA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Analiza automata — NDVI + diferente + penalizari PAC")

    if "df_parcele" not in st.session_state:
        st.info("Incarca mai intai un fisier CSV din tab-ul 'Incarca parcele'.")
    else:
        df_p = st.session_state["df_parcele"]

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            prag_rosu = st.slider("Prag risc ROSU — diferenta (%):", 5.0, 30.0, 20.0, 1.0)
            prag_galben = st.slider("Prag risc GALBEN — diferenta (%):", 1.0, 10.0, 3.0, 0.5)
        with col_opt2:
            filtra_risc = st.multiselect(
                "Afiseaza riscuri:",
                ["ROSU", "GALBEN", "VERDE"],
                default=["ROSU", "GALBEN", "VERDE"],
            )

        if st.button("Analizeaza toate parcelele", type="primary", use_container_width=True, key="btn_analiza"):
            with st.spinner(f"Analizez {len(df_p)} parcele..."):
                bara = st.progress(0)
                rezultate = []
                for i, (_, rand) in enumerate(df_p.iterrows()):
                    try:
                        dec = float(rand["SUPRAFATA_DECLARATA_HA"])
                        mas = float(rand["SUPRAFATA_MASURATA_HA"])
                        nir = float(rand["NIR"])
                        red = float(rand["RED"])
                        cultura = str(rand.get("CULTURA", "?")).upper().strip()

                        ndvi = calcul_ndvi(nir, red)
                        ndvi_st, _ = interpreteaza_ndvi(ndvi, cultura)
                        dif = calcul_diferenta_pct(dec, mas)

                        # Aplica praguri personalizate
                        if dif >= prag_rosu or ndvi < 0.15:
                            risc_val = "ROSU"
                        elif dif >= prag_galben or ndvi < CULTURI_NDVI_MIN.get(cultura, 0.25):
                            risc_val = "GALBEN"
                        else:
                            risc_val = "VERDE"

                        pen_st, pen_pct, _ = calcul_penalizare(dif)
                        rezultate.append({
                            "ID_PARCELA": rand.get("ID_PARCELA", "?"),
                            "CULTURA": cultura,
                            "UAT": rand.get("UAT", "?"),
                            "DEC_HA": round(dec, 2),
                            "MAS_HA": round(mas, 2),
                            "DIF_PCT": round(dif, 2),
                            "NDVI": round(ndvi, 4),
                            "NDVI_STATUS": ndvi_st,
                            "PENALIZARE": pen_st,
                            "PEN_PCT": round(pen_pct, 1),
                            "RISC": risc_val,
                        })
                    except Exception as e:
                        rezultate.append({
                            "ID_PARCELA": rand.get("ID_PARCELA", "?"),
                            "CULTURA": "EROARE", "UAT": "", "DEC_HA": 0, "MAS_HA": 0,
                            "DIF_PCT": 0, "NDVI": 0, "NDVI_STATUS": str(e),
                            "PENALIZARE": "EROARE", "PEN_PCT": 0, "RISC": "EROARE",
                        })
                    bara.progress((i + 1) / len(df_p))

                df_rez = pd.DataFrame(rezultate)
                st.session_state["df_rezultate"] = df_rez

        if "df_rezultate" in st.session_state:
            df_r = st.session_state["df_rezultate"]

            # KPI-uri
            nr_rosu = len(df_r[df_r["RISC"] == "ROSU"])
            nr_galben = len(df_r[df_r["RISC"] == "GALBEN"])
            nr_verde = len(df_r[df_r["RISC"] == "VERDE"])
            total_pen = df_r["PEN_PCT"].mean()

            c1, c2, c3, c4 = st.columns(4)
            kpi = """<div style='background:white; border-radius:8px; padding:12px; text-align:center;
     box-shadow:0 2px 6px rgba(0,0,0,0.08); border-top:4px solid {c};'>
    <div style='font-size:24px; font-weight:800; color:{c};'>{v}</div>
    <div style='font-size:11px; color:#666;'>{l}</div></div>"""
            with c1:
                st.markdown(kpi.format(c="#e74c3c", v=nr_rosu, l="Risc ROSU"), unsafe_allow_html=True)
            with c2:
                st.markdown(kpi.format(c="#f39c12", v=nr_galben, l="Risc GALBEN"), unsafe_allow_html=True)
            with c3:
                st.markdown(kpi.format(c="#27ae60", v=nr_verde, l="Risc VERDE"), unsafe_allow_html=True)
            with c4:
                st.markdown(kpi.format(c="#8e44ad", v=f"{total_pen:.1f}%", l="Penalizare medie"), unsafe_allow_html=True)

            st.divider()

            # Tabel rezultate cu colorare
            df_afisare = df_r[df_r["RISC"].isin(filtra_risc)].copy()

            def coloreaza_risc(val):
                culori = {"ROSU": "background-color:#fde8e8",
                          "GALBEN": "background-color:#fef9e7",
                          "VERDE": "background-color:#eafaf1"}
                return culori.get(val, "")

            st.dataframe(
                df_afisare.style.applymap(coloreaza_risc, subset=["RISC"]),
                use_container_width=True,
                height=400,
            )

            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                csv_rez = df_r.to_csv(index=False, encoding="utf-8")
                st.download_button(
                    "Descarca rezultate CSV",
                    data=csv_rez.encode("utf-8"),
                    file_name=f"analiza_apia_{datetime.date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with col_dl2:
                if nr_rosu > 0:
                    csv_rosu = df_r[df_r["RISC"] == "ROSU"].to_csv(index=False)
                    st.download_button(
                        f"Descarca doar risc ROSU ({nr_rosu})",
                        data=csv_rosu.encode("utf-8"),
                        file_name=f"parcele_risc_rosu_{datetime.date.today().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RAPORT NECONFORMITATI
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Raport de neconformitati — generat de AI")

    if "df_rezultate" not in st.session_state:
        st.info("Ruleaza mai intai analiza din tab-ul 'Analiza automata'.")
    else:
        df_r = st.session_state["df_rezultate"]
        nr_rosu = len(df_r[df_r["RISC"] == "ROSU"])
        nr_galben = len(df_r[df_r["RISC"] == "GALBEN"])

        col_rez1, col_rez2 = st.columns([1, 1])

        with col_rez1:
            st.markdown("**Rezumat rapid:**")

            for _, rand in df_r[df_r["RISC"] == "ROSU"].iterrows():
                st.markdown(f"""
<div style='background:#fde8e8; border-left:4px solid #e74c3c; border-radius:6px;
     padding:8px 12px; margin:4px 0; font-size:11px;'>
<b>ROSU — {rand["ID_PARCELA"]}</b> | {rand["CULTURA"]} | {rand["UAT"]}<br>
Diferenta: <b>{rand["DIF_PCT"]}%</b> | NDVI: <b>{rand["NDVI"]}</b> ({rand["NDVI_STATUS"]})<br>
Penalizare: <b>{rand["PENALIZARE"]}</b>
</div>
""", unsafe_allow_html=True)

            for _, rand in df_r[df_r["RISC"] == "GALBEN"].iterrows():
                st.markdown(f"""
<div style='background:#fef9e7; border-left:4px solid #f39c12; border-radius:6px;
     padding:8px 12px; margin:4px 0; font-size:11px;'>
<b>GALBEN — {rand["ID_PARCELA"]}</b> | {rand["CULTURA"]} | {rand["UAT"]}<br>
Diferenta: <b>{rand["DIF_PCT"]}%</b> | NDVI: <b>{rand["NDVI"]}</b>
</div>
""", unsafe_allow_html=True)

        with col_rez2:
            st.markdown("**Genereaza raport text cu AI:**")
            if ollama_ok:
                st.success("Ollama activ — raport generat de LLM")
            else:
                st.warning("Ollama offline — raport demo")

            if st.button(
                "Genereaza raport oficial",
                type="primary", use_container_width=True, key="btn_raport_text"
            ):
                with st.spinner("LLM redacteaza raportul..."):
                    if ollama_ok:
                        raport_text = genereaza_raport_text(df_r, model_ales)
                    else:
                        time.sleep(1.0)
                        raport_text = raport_demo(df_r)
                st.session_state["raport_generat"] = raport_text

        if "raport_generat" in st.session_state:
            st.divider()
            st.markdown("**Raport generat:**")
            raport = st.session_state["raport_generat"]
            st.markdown(
                f"<div style='background:#f8f9fa; border-radius:8px; padding:16px; "
                f"font-size:12px; line-height:1.9; font-family:monospace; "
                f"white-space:pre-wrap; border-left:4px solid #1a5276;'>{raport}</div>",
                unsafe_allow_html=True,
            )

            antet = (
                f"RAPORT CONTROL APIA — CJ GORJ\n"
                f"Data: {datetime.date.today().strftime('%d.%m.%Y')}\n"
                f"Inspector: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu\n"
                f"Total parcele: {len(df_r)} | Risc rosu: {nr_rosu} | Risc galben: {nr_galben}\n"
                f"{'='*60}\n\n"
            )
            st.download_button(
                "Descarca raport .txt",
                data=(antet + raport).encode("utf-8"),
                file_name=f"raport_control_apia_{datetime.date.today().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.divider()
        st.subheader("Statistica pe culturi")
        if len(df_r) > 0:
            stats = df_r.groupby("CULTURA").agg(
                Parcele=("ID_PARCELA", "count"),
                DIF_MEDIE=("DIF_PCT", "mean"),
                NDVI_MEDIU=("NDVI", "mean"),
                RISC_ROSU=("RISC", lambda x: (x == "ROSU").sum()),
            ).round(3)
            st.dataframe(stats, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Ziua 27 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### Agent inspector — pipeline complet

```python
# 1. Citire CSV cu pandas
df = pd.read_csv("parcele.csv")

# 2. Analiza per parcela (vectorizata)
df["NDVI"] = (df["NIR"] - df["RED"]) / (df["NIR"] + df["RED"])
df["DIF_PCT"] = abs(df["DEC"] - df["MAS"]) / df["DEC"] * 100

# 3. Clasificare risc
def risc(row):
    if row["DIF_PCT"] >= 20 or row["NDVI"] < 0.15:
        return "ROSU"
    elif row["DIF_PCT"] >= 3:
        return "GALBEN"
    return "VERDE"
df["RISC"] = df.apply(risc, axis=1)

# 4. Raport cu Ollama
raport = ollama(prompt=rezumat_date)

# 5. Export CSV filtrat
df[df["RISC"]=="ROSU"].to_csv("risc_rosu.csv")
```

**Praguri PAC:**
- < 3% diferenta → CONFORM, nicio penalizare
- 3-20% → penalizare = diferenta%
- 20-50% → penalizare dubla
- > 50% → excludere totala (plata = 0)
""")

    with col2:
        st.markdown("""
#### Impact real pentru APIA CJ Gorj

**Fara AI (metoda clasica):**
- 30 parcele analizate manual = 3-4 ore inspector
- Calcule separate in Excel
- Raport redactat manual: 1-2 ore
- **Total: 5-6 ore**

**Cu agentul Z27:**
- 30 parcele = 15 secunde calcule + 45 sec raport Ollama
- Export automat CSV + TXT
- **Total: < 2 minute**

**Scalabilitate:**
- 1.000 parcele → acelasi timp (~2 min)
- 50.000 parcele (CJ Gorj real) → ~5-10 min

**Nota:** Decizia finala ramane la inspector.
AI-ul calculeaza si organizeaza, inspectorul decide.
""")
        st.markdown("""
<div style='background:#e8f4fd; border-radius:8px; padding:12px; margin-top:10px;
     border-left:4px solid #1a5276;'>
<div style='font-weight:700; color:#1a5276;'>Conexiune cu teza de doctorat</div>
<div style='font-size:11px; color:#333; margin-top:6px; line-height:1.7;'>
Agentul Z27 implementeaza metodologia descrisa in teza:<br>
<i>"Contributii privind recunoasterea automata a culturilor
cu ajutorul unei Drone"</i><br>
NDVI calculat din imagini drone → validare conformitate PAC → raport APIA
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#c0392b 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 27 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
CSV upload · NDVI automat · Penalizari PAC · Clasificare risc (ROSU/GALBEN/VERDE) · Raport LLM · Export
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 28 — Dashboard AI complet: toate instrumentele integrate
</div>
</div>
""", unsafe_allow_html=True)
