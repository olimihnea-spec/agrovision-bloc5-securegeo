"""
Ziua 19 — CalcPAC-APIA: Calculator Scheme de Sprijin PAC
Modul 4: AI Aplicat in Administratia Agricola
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import re
import sys
import os

# Import valori PAC
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from schemes_pac_2025 import (
        BISS_EUR_HA, REDISTRIBUTIV_EUR_HA, REDISTRIBUTIV_MAX_HA,
        ECO1_EUR_HA, ECO2_EUR_HA, ECO3_EUR_HA,
        TINERI_FERMIERI_EUR_HA, TINERI_FERMIERI_MAX_HA, TINERI_FERMIERI_MAX_ANI,
        CULTURI_CUPLATE, ANIMALE_CUPLATE, BUNASTARE_ANIMALE, DR_MASURI,
        PRAG_SUPRAFATA_AVERTISMENT_PCT, PRAG_SUPRAFATA_PENALIZARE_PCT,
        PRAG_SUPRAFATA_EXCLUDERE_PCT, PRAG_SUPRAFATA_FRAUDA_PCT,
        NDVI_VEGETATIE_NORMALA, NDVI_CULTURA_ABSENTA,
        SUPRAFATA_MINIMA_ELIGIBILA_HA, CAPPING_PLATI_DIRECTE_EUR,
        DEGRESSIVITATE_PRAG_EUR, DEGRESSIVITATE_REDUCERE_PCT,
        CULORI_SCHEME, CULORI_NECONFORMITATE,
        VERSIUNE, DATA_ACTUALIZARE, SURSA_LEGALA,
    )
    SCHEMES_OK = True
except Exception as e:
    SCHEMES_OK = False
    _schemes_err = str(e)

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="Ziua 19 — CalcPAC APIA",
    page_icon="PAC",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:32px;'>PAC</div>
    <div style='font-size:16px; font-weight:700; color:#1a5276;'>ZIUA 19</div>
    <div style='font-size:11px; color:#666;'>CalcPAC-APIA — Scheme de Sprijin</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI in Administratia Agricola")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 19 / 30 zile")
st.sidebar.progress(19 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
if SCHEMES_OK:
    st.sidebar.caption(f"Scheme PAC v{VERSIUNE} | Actualizat: {DATA_ACTUALIZARE}")
else:
    st.sidebar.error("schemes_pac_2025.py: lipsa")
st.sidebar.divider()
st.sidebar.markdown("""
**Scheme acoperite:**
- Plata de baza (BISS)
- Eco-scheme 1, 2, 3
- Redistributiva + Tineri
- Plati cuplate culturi
- Plati cuplate animale
- Bunastare animale
- Dezvoltare Rurala (DR)
""")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>PAC</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1a5276; font-weight:800;'>
            Ziua 19 — CalcPAC-APIA
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Calculator automat scheme de sprijin PAC 2025 &nbsp;|&nbsp;
            Detectie neconformitati &nbsp;|&nbsp; Monitor legislatie
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#117a65 100%);
     border-radius:10px;padding:12px 20px;margin-bottom:16px;'>
<span style='color:#f9e79f;font-size:13px;font-style:italic;'>
"700 de pagini de proceduri. Legislatie care se schimba de 2-3 ori pe an.
CalcPAC automatizeaza calculul subventiilor si detecteaza neconformitatile
in secunde, nu in ore."<br>
<b style='color:white;'>Consilier Superior Dr. Oliviu Mihnea Gamulescu | APIA CJ Gorj</b>
</span></div>""", unsafe_allow_html=True)

if not SCHEMES_OK:
    st.error(f"Fisierul schemes_pac_2025.py nu a putut fi importat: {_schemes_err}")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII CALCUL
# ══════════════════════════════════════════════════════════════════════════════

def calculeaza_pac(parcele: list, animale: dict, bunastare: dict,
                   dr_masuri_active: list, este_tanar: bool,
                   ani_de_la_prima_cerere: int) -> dict:
    """
    Calculeaza toate schemele PAC aplicabile.
    Returneaza dict cu rezultatele per schema si totalul general.
    """
    rezultate = {}

    total_ha = sum(p["ha"] for p in parcele if p["ha"] >= SUPRAFATA_MINIMA_ELIGIBILA_HA)

    # ── BISS ──────────────────────────────────────────────────────────────────
    biss = total_ha * BISS_EUR_HA
    rezultate["BISS — Plata de baza"] = {
        "eur": round(biss, 2),
        "baza": f"{total_ha:.2f} ha x {BISS_EUR_HA} EUR/ha",
        "culoare": CULORI_SCHEME["BISS"],
    }

    # ── Redistributiva ────────────────────────────────────────────────────────
    ha_redist = min(total_ha, REDISTRIBUTIV_MAX_HA)
    redist = ha_redist * REDISTRIBUTIV_EUR_HA
    rezultate["Plata redistributiva"] = {
        "eur": round(redist, 2),
        "baza": f"{ha_redist:.2f} ha x {REDISTRIBUTIV_EUR_HA} EUR/ha (primele {REDISTRIBUTIV_MAX_HA} ha)",
        "culoare": CULORI_SCHEME["Redistributiv"],
    }

    # ── Eco-scheme 1 ─────────────────────────────────────────────────────────
    ha_eco1 = sum(p["ha"] for p in parcele if p.get("eco1") and p["ha"] >= SUPRAFATA_MINIMA_ELIGIBILA_HA)
    if ha_eco1 > 0:
        rezultate["Eco-schema 1 (rotatie)"] = {
            "eur": round(ha_eco1 * ECO1_EUR_HA, 2),
            "baza": f"{ha_eco1:.2f} ha x {ECO1_EUR_HA} EUR/ha",
            "culoare": CULORI_SCHEME["Eco-schema 1"],
        }

    # ── Eco-scheme 2 ─────────────────────────────────────────────────────────
    ha_eco2 = sum(p["ha"] for p in parcele if p.get("eco2") and p["ha"] >= SUPRAFATA_MINIMA_ELIGIBILA_HA)
    if ha_eco2 > 0:
        rezultate["Eco-schema 2 (agro-eco)"] = {
            "eur": round(ha_eco2 * ECO2_EUR_HA, 2),
            "baza": f"{ha_eco2:.2f} ha x {ECO2_EUR_HA} EUR/ha",
            "culoare": CULORI_SCHEME["Eco-schema 2"],
        }

    # ── Eco-scheme 3 ─────────────────────────────────────────────────────────
    ha_eco3 = sum(p["ha"] for p in parcele if p.get("eco3") and p["ha"] >= SUPRAFATA_MINIMA_ELIGIBILA_HA)
    if ha_eco3 > 0:
        rezultate["Eco-schema 3 (pajisti)"] = {
            "eur": round(ha_eco3 * ECO3_EUR_HA, 2),
            "baza": f"{ha_eco3:.2f} ha x {ECO3_EUR_HA} EUR/ha",
            "culoare": CULORI_SCHEME["Eco-schema 3"],
        }

    # ── Tineri fermieri ───────────────────────────────────────────────────────
    if este_tanar and ani_de_la_prima_cerere <= TINERI_FERMIERI_MAX_ANI:
        ha_tineri = min(total_ha, TINERI_FERMIERI_MAX_HA)
        rezultate["Tineri fermieri"] = {
            "eur": round(ha_tineri * TINERI_FERMIERI_EUR_HA, 2),
            "baza": f"{ha_tineri:.2f} ha x {TINERI_FERMIERI_EUR_HA} EUR/ha (an {ani_de_la_prima_cerere}/{TINERI_FERMIERI_MAX_ANI})",
            "culoare": CULORI_SCHEME["Tineri fermieri"],
        }

    # ── Plati cuplate culturi ─────────────────────────────────────────────────
    cuplate_culturi = {}
    for p in parcele:
        cultura = p.get("cultura", "")
        if cultura in CULTURI_CUPLATE and p["ha"] >= SUPRAFATA_MINIMA_ELIGIBILA_HA:
            cuplate_culturi[cultura] = cuplate_culturi.get(cultura, 0) + p["ha"]

    for cultura, ha_total in cuplate_culturi.items():
        eur_ha = CULTURI_CUPLATE[cultura]
        rezultate[f"Cuplat — {cultura}"] = {
            "eur": round(ha_total * eur_ha, 2),
            "baza": f"{ha_total:.2f} ha x {eur_ha} EUR/ha",
            "culoare": CULORI_SCHEME["Cuplate culturi"],
        }

    # ── Plati cuplate animale ─────────────────────────────────────────────────
    for specie, capete in animale.items():
        if capete > 0 and specie in ANIMALE_CUPLATE:
            eur_cap = ANIMALE_CUPLATE[specie]
            rezultate[f"Cuplat — {specie}"] = {
                "eur": round(capete * eur_cap, 2),
                "baza": f"{capete} capete x {eur_cap} EUR/cap",
                "culoare": CULORI_SCHEME["Cuplate animale"],
            }

    # ── Bunastare animale ─────────────────────────────────────────────────────
    for specie, capete in bunastare.items():
        if capete > 0 and specie in BUNASTARE_ANIMALE:
            eur_cap = BUNASTARE_ANIMALE[specie]
            rezultate[f"Bunastare — {specie}"] = {
                "eur": round(capete * eur_cap, 2),
                "baza": f"{capete} capete x {eur_cap} EUR/cap",
                "culoare": CULORI_SCHEME["Bunastare animale"],
            }

    # ── Dezvoltare Rurala ─────────────────────────────────────────────────────
    for masura in dr_masuri_active:
        if masura in DR_MASURI:
            valoare = DR_MASURI[masura]
            # Daca e plata forfetara (> 1000 EUR), nu o inmultim cu ha
            if valoare > 1000:
                rezultate[f"DR — {masura}"] = {
                    "eur": round(valoare, 2),
                    "baza": f"Plata forfetara {valoare} EUR/an",
                    "culoare": CULORI_SCHEME["DR"],
                }
            else:
                rezultate[f"DR — {masura}"] = {
                    "eur": round(total_ha * valoare, 2),
                    "baza": f"{total_ha:.2f} ha x {valoare} EUR/ha/an",
                    "culoare": CULORI_SCHEME["DR"],
                }

    # ── Total + degressivitate ────────────────────────────────────────────────
    total_pd = sum(v["eur"] for k, v in rezultate.items()
                   if not k.startswith("DR") and not k.startswith("Bunastare") and not k.startswith("Cuplat — "))
    total_general = sum(v["eur"] for v in rezultate.values())

    # Capping
    if total_pd > CAPPING_PLATI_DIRECTE_EUR:
        reducere = total_pd - CAPPING_PLATI_DIRECTE_EUR
        rezultate["_capping"] = {"eur": -round(reducere, 2),
                                  "baza": f"Reducere capping (> {CAPPING_PLATI_DIRECTE_EUR:,.0f} EUR)",
                                  "culoare": "#c0392b"}

    elif total_pd > DEGRESSIVITATE_PRAG_EUR:
        suma_peste_prag = total_pd - DEGRESSIVITATE_PRAG_EUR
        reducere = suma_peste_prag * (DEGRESSIVITATE_REDUCERE_PCT / 100)
        rezultate["_degressivitate"] = {
            "eur": -round(reducere, 2),
            "baza": f"Reducere degressivitate {DEGRESSIVITATE_REDUCERE_PCT}% pe suma > {DEGRESSIVITATE_PRAG_EUR:,.0f} EUR",
            "culoare": "#e67e22",
        }

    return rezultate


def analizeaza_neconformitati(parcele: list) -> list:
    """Returneaza lista de neconformitati detectate."""
    neconf = []
    for p in parcele:
        ha_decl = p.get("ha", 0)
        ha_mas  = p.get("ha_masurat", None)
        ndvi    = p.get("ndvi", None)
        cultura = p.get("cultura", "")
        cultura_ndvi = p.get("cultura_ndvi", "")
        lpis    = p.get("lpis", f"Parcela {p.get('idx', '?')}")

        # Suprafata
        if ha_mas is not None and ha_decl > 0:
            diff_pct = abs(ha_decl - ha_mas) / ha_decl * 100
            if diff_pct >= PRAG_SUPRAFATA_FRAUDA_PCT:
                neconf.append({
                    "lpis": lpis, "tip": "FRAUDA SUSPECTATA",
                    "mesaj": f"Diferenta suprafata {diff_pct:.1f}% (> {PRAG_SUPRAFATA_FRAUDA_PCT}%). Declarata: {ha_decl} ha, Masurata: {ha_mas} ha.",
                    "actiune": "Sesizare control special + excludere 3 ani urmatori",
                    "nivel": "frauda",
                })
            elif diff_pct >= PRAG_SUPRAFATA_EXCLUDERE_PCT:
                neconf.append({
                    "lpis": lpis, "tip": "EXCLUDERE PARCELA",
                    "mesaj": f"Diferenta suprafata {diff_pct:.1f}% (> {PRAG_SUPRAFATA_EXCLUDERE_PCT}%). Declarata: {ha_decl} ha, Masurata: {ha_mas} ha.",
                    "actiune": "Excludere parcela + penalizare an urmator",
                    "nivel": "penalizare",
                })
            elif diff_pct >= PRAG_SUPRAFATA_PENALIZARE_PCT:
                neconf.append({
                    "lpis": lpis, "tip": "PENALIZARE SUPRAFATA",
                    "mesaj": f"Diferenta suprafata {diff_pct:.1f}% (> {PRAG_SUPRAFATA_PENALIZARE_PCT}%). Declarata: {ha_decl} ha, Masurata: {ha_mas} ha.",
                    "actiune": "Reducere proportionala subventie parcela afectata",
                    "nivel": "penalizare",
                })
            elif diff_pct >= PRAG_SUPRAFATA_AVERTISMENT_PCT:
                neconf.append({
                    "lpis": lpis, "tip": "AVERTISMENT SUPRAFATA",
                    "mesaj": f"Diferenta suprafata {diff_pct:.1f}% (> {PRAG_SUPRAFATA_AVERTISMENT_PCT}%). Sub pragul de penalizare.",
                    "actiune": "Nota in dosar. Monitorizare an urmator.",
                    "nivel": "avertisment",
                })

        # Cultura vs NDVI
        if ndvi is not None and cultura_ndvi and cultura:
            if ndvi < NDVI_CULTURA_ABSENTA:
                neconf.append({
                    "lpis": lpis, "tip": "CULTURA ABSENTA (NDVI)",
                    "mesaj": f"NDVI = {ndvi:.2f} < {NDVI_CULTURA_ABSENTA} — teren posibil necultivat sau cultura distrusa. Cultura declarata: {cultura}.",
                    "actiune": "Verificare teren obligatorie. Pierdere plati cuplate daca se confirma.",
                    "nivel": "penalizare",
                })
            elif cultura_ndvi.lower() != cultura.lower() and cultura_ndvi != "Necunoscuta":
                neconf.append({
                    "lpis": lpis, "tip": "CULTURA NEPOTRIVITA (NDVI)",
                    "mesaj": f"Declarata: {cultura} | Identificata NDVI: {cultura_ndvi}.",
                    "actiune": "Control teren. Daca se confirma: pierdere plati cuplate cultura declarata.",
                    "nivel": "avertisment",
                })

    return neconf


def fetch_monitorul_oficial_rss() -> list:
    """Preia ultimele acte din RSS Monitorul Oficial filtrate pe APIA/PAC."""
    if not REQUESTS_OK:
        return []
    try:
        url = "https://www.monitoruloficial.ro/rss/monitor_oficial.xml"
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.content)
        items = []
        cuvinte_cheie = ["apia", "pac", "scheme de sprijin", "plati directe",
                         "madr", "subventii", "fermieri", "dezvoltare rurala"]
        for item in root.iter("item"):
            titlu = (item.findtext("title") or "").lower()
            link  = item.findtext("link") or ""
            data  = item.findtext("pubDate") or ""
            desc  = (item.findtext("description") or "").lower()
            if any(c in titlu or c in desc for c in cuvinte_cheie):
                items.append({"titlu": item.findtext("title"), "link": link, "data": data})
        return items[:10]
    except Exception:
        return []


def extrage_valori_din_text(text: str) -> list:
    """NLP simplu: extrage valori EUR/ha sau EUR/cap din text legislativ."""
    rezultate = []
    pattern_eur_ha  = re.compile(r'(\d+[.,]?\d*)\s*(?:euro|EUR|lei)(?:/ha|\s+pe\s+hectar)', re.IGNORECASE)
    pattern_eur_cap = re.compile(r'(\d+[.,]?\d*)\s*(?:euro|EUR|lei)(?:/cap|\s+pe\s+cap)', re.IGNORECASE)
    pattern_pct     = re.compile(r'(\d+[.,]?\d*)\s*(?:%|la suta|procente)', re.IGNORECASE)
    for m in pattern_eur_ha.finditer(text):
        rezultate.append({"tip": "EUR/ha", "valoare": m.group(1), "context": text[max(0,m.start()-40):m.end()+40]})
    for m in pattern_eur_cap.finditer(text):
        rezultate.append({"tip": "EUR/cap", "valoare": m.group(1), "context": text[max(0,m.start()-40):m.end()+40]})
    for m in pattern_pct.finditer(text):
        rezultate.append({"tip": "Prag %", "valoare": m.group(1), "context": text[max(0,m.start()-40):m.end()+40]})
    return rezultate


# ══════════════════════════════════════════════════════════════════════════════
# INTERFATA
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "Formular Fermier",
    "Rezultate & Subventii",
    "Neconformitati",
    "Monitor Legislatie",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — FORMULAR FERMIER
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Date fermier — introducere date pentru calcul PAC")

    with st.expander("Date generale fermier", expanded=True):
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            nume_fermier = st.text_input("Nume fermier:", value="Popescu Ion", key="f_nume")
            judet = st.selectbox("Judet:", ["Gorj","Dolj","Olt","Valcea","Mehedinti",
                                             "Hunedoara","Alba","Cluj","Timis","Iasi",
                                             "Bacau","Suceava","Botosani","Altul"], key="f_jud")
        with col_g2:
            este_tanar = st.checkbox("Tanar fermier (< 41 ani la prima cerere)", key="f_tanar")
            ani_prima_cerere = 1
            if este_tanar:
                ani_prima_cerere = st.number_input("Ani de la prima cerere PAC:",
                                                    1, 5, 1, key="f_ani_cerere")
        with col_g3:
            nr_parcele = st.number_input("Numar parcele:", 1, 20, 3, key="f_nr_parcele",
                                          format="%d")

    st.divider()

    # ── Parcele ───────────────────────────────────────────────────────────────
    st.markdown("**Parcele agricole:**")
    parcele = []
    for i in range(int(nr_parcele)):
        with st.expander(f"Parcela {i+1}", expanded=(i == 0)):
            c1, c2, c3 = st.columns(3)
            with c1:
                lpis = st.text_input(f"Cod LPIS:", value=f"GJ-{100+i:03d}-A", key=f"lpis_{i}")
                ha   = st.number_input(f"Suprafata declarata (ha):", 0.1, 500.0,
                                        round(3.5 + i * 1.2, 1), 0.1, key=f"ha_{i}")
            with c2:
                cultura = st.selectbox(f"Cultura principala:",
                                        ["Grau", "Porumb", "Floarea-soarelui", "Orz",
                                         "Rapita", "Soia", "Sfecla de zahar", "Lucerna",
                                         "Mazare/Fasole", "Fanete/Pajisti", "Necultivat"],
                                        key=f"cult_{i}")
                ha_masurat = st.number_input(f"Suprafata masurata CV (ha, optional):",
                                              0.0, 500.0, 0.0, 0.01, key=f"ha_mas_{i}",
                                              help="Lasati 0 daca nu aveti masurare drone/CV")
            with c3:
                eco1 = st.checkbox("Eco-schema 1 (rotatie)", key=f"eco1_{i}")
                eco2 = st.checkbox("Eco-schema 2 (agro-eco)", key=f"eco2_{i}")
                eco3 = st.checkbox("Eco-schema 3 (pajisti)", key=f"eco3_{i}")
                ndvi_val = st.number_input(f"NDVI masurat (optional):",
                                            0.0, 1.0, 0.0, 0.01, key=f"ndvi_{i}",
                                            help="NDVI din analiza drone/satelit. Lasati 0 daca nu aveti.")

            parcele.append({
                "idx": i+1, "lpis": lpis, "ha": ha,
                "ha_masurat": ha_masurat if ha_masurat > 0 else None,
                "cultura": cultura, "eco1": eco1, "eco2": eco2, "eco3": eco3,
                "ndvi": ndvi_val if ndvi_val > 0 else None,
                "cultura_ndvi": "",
            })

    st.divider()

    # ── Animale ───────────────────────────────────────────────────────────────
    col_an, col_dr = st.columns(2)
    with col_an:
        with st.expander("Animale (plati cuplate)", expanded=False):
            animale = {}
            bunastare = {}
            for specie in list(ANIMALE_CUPLATE.keys()):
                animale[specie] = st.number_input(f"{specie}:", 0, 5000, 0,
                                                   key=f"an_{specie}", format="%d")
            st.markdown("**Bunastare animale:**")
            for specie in list(BUNASTARE_ANIMALE.keys()):
                bunastare[specie] = st.number_input(f"{specie} (bunastare):", 0, 10000, 0,
                                                     key=f"bun_{specie}", format="%d")

    with col_dr:
        with st.expander("Angajamente Dezvoltare Rurala", expanded=False):
            dr_active = []
            for masura in DR_MASURI:
                if st.checkbox(masura, key=f"dr_{masura}"):
                    dr_active.append(masura)

    st.divider()
    calculeaza_btn = st.button("Calculeaza subventii PAC", type="primary",
                                use_container_width=True, key="btn_calc")

    if calculeaza_btn:
        st.session_state["pac_parcele"]       = parcele
        st.session_state["pac_animale"]       = animale
        st.session_state["pac_bunastare"]     = bunastare
        st.session_state["pac_dr"]            = dr_active
        st.session_state["pac_tanar"]         = este_tanar
        st.session_state["pac_ani_cerere"]    = ani_prima_cerere
        st.session_state["pac_nume"]          = nume_fermier
        st.session_state["pac_judet"]         = judet

        rezultate = calculeaza_pac(
            parcele, animale, bunastare, dr_active,
            este_tanar, ani_prima_cerere
        )
        neconformitati = analizeaza_neconformitati(parcele)
        st.session_state["pac_rezultate"]     = rezultate
        st.session_state["pac_neconformitati"]= neconformitati

        total = sum(v["eur"] for v in rezultate.values())
        n_neconf = len(neconformitati)
        culoare_status = "#27ae60" if n_neconf == 0 else ("#e67e22" if n_neconf < 3 else "#c0392b")

        st.success(f"Calcul finalizat pentru **{nume_fermier}** — {judet}")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total subventii estimate", f"{total:,.0f} EUR")
        with m2:
            st.metric("Scheme aplicabile", len(rezultate))
        with m3:
            st.metric("Neconformitati detectate", n_neconf,
                      delta=None if n_neconf == 0 else f"{n_neconf} atentionari")

        st.info("Mergi la tab-urile **Rezultate & Subventii** si **Neconformitati** pentru detalii.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REZULTATE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if "pac_rezultate" not in st.session_state:
        st.info("Completeaza formularul si apasa **Calculeaza subventii PAC**.")
    else:
        rezultate = st.session_state["pac_rezultate"]
        nume = st.session_state.get("pac_nume", "Fermier")
        judet_r = st.session_state.get("pac_judet", "")
        total = sum(v["eur"] for v in rezultate.values())
        total_pozitiv = sum(v["eur"] for v in rezultate.values() if v["eur"] > 0)

        st.subheader(f"Rezultate calcul PAC — {nume} | {judet_r}")

        # Tabel scheme
        col_t, col_g = st.columns([3, 2])
        with col_t:
            for schema, date in rezultate.items():
                if schema.startswith("_"):
                    semn = "-"
                    bg = "#fff5f5"
                    border = "#c0392b"
                else:
                    semn = ""
                    bg = "white"
                    border = date["culoare"]
                st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center;
     background:{bg}; border-radius:8px; padding:10px 14px; margin:4px 0;
     border-left:5px solid {border}; box-shadow:0 1px 3px rgba(0,0,0,0.05);
     font-size:12px;'>
    <div>
        <div style='font-weight:700; color:#333;'>{schema.lstrip("_")}</div>
        <div style='color:#888; font-size:10px; margin-top:2px;'>{date["baza"]}</div>
    </div>
    <div style='font-size:16px; font-weight:900;
         color:{border};'>{semn}{date["eur"]:,.0f} EUR</div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center;
     background:#1a5276; border-radius:10px; padding:14px 18px; margin-top:10px;'>
    <div style='color:white; font-weight:700; font-size:15px;'>TOTAL ESTIMAT</div>
    <div style='color:#f9e79f; font-size:22px; font-weight:900;'>{total:,.0f} EUR</div>
</div>
""", unsafe_allow_html=True)

        with col_g:
            if PLOTLY_OK:
                scheme_poz = {k: v for k, v in rezultate.items()
                              if not k.startswith("_") and v["eur"] > 0}
                if scheme_poz:
                    fig = go.Figure(go.Pie(
                        labels=list(scheme_poz.keys()),
                        values=[v["eur"] for v in scheme_poz.values()],
                        marker_colors=[v["culoare"] for v in scheme_poz.values()],
                        hole=0.4,
                        textinfo="percent",
                        hovertemplate="%{label}<br>%{value:,.0f} EUR<extra></extra>",
                    ))
                    fig.update_layout(
                        height=350, margin=dict(l=10, r=10, t=30, b=10),
                        title=dict(text="Distributie scheme", font_size=13),
                        showlegend=True,
                        legend=dict(font_size=9, orientation="v"),
                    )
                    st.plotly_chart(fig, use_container_width=True)

        st.divider()
        # Export raport
        azi = datetime.date.today().strftime("%d.%m.%Y")
        raport = f"""RAPORT CALCUL PAC 2025
Generat: {azi} | CalcPAC-APIA v{VERSIUNE}
Fermier: {nume} | Judet: {judet_r}
{"="*55}
"""
        for schema, date in rezultate.items():
            raport += f"{schema.lstrip('_'):40s} {date['eur']:>10,.0f} EUR\n"
            raport += f"  Baza calcul: {date['baza']}\n"
        raport += f"\n{'TOTAL ESTIMAT':40s} {total:>10,.0f} EUR\n"
        raport += f"\nNota: Valorile sunt estimative. Suma finala depinde de \n"
        raport += f"incadrarea conditionalitatilor si verificarea pe teren.\n"
        raport += f"\nSurse legale:\n"
        for s in SURSA_LEGALA:
            raport += f"  - {s}\n"

        st.download_button("Descarca raport .txt", data=raport.encode("utf-8"),
                           file_name=f"calcpac_{nume.replace(' ','_')}_{azi.replace('.','')}.txt",
                           mime="text/plain", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — NECONFORMITATI
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if "pac_neconformitati" not in st.session_state:
        st.info("Ruleaza calculul din tab-ul **Formular Fermier**.")
    else:
        neconf = st.session_state["pac_neconformitati"]
        st.subheader(f"Analiza neconformitati — {len(neconf)} semnale detectate")

        if not neconf:
            st.success("Nu au fost detectate neconformitati pe baza datelor introduse.")
        else:
            iconite = {"frauda": "FRAUDA", "penalizare": "PENALIZARE",
                       "avertisment": "ATENTIE", "ok": "OK"}
            for nc in neconf:
                nivel = nc.get("nivel", "avertisment")
                culoare = CULORI_NECONFORMITATE.get(nivel, "#999")
                icon = iconite.get(nivel, "!")
                st.markdown(f"""
<div style='background:white; border-radius:10px; padding:14px 18px; margin:6px 0;
     border-left:6px solid {culoare}; box-shadow:0 2px 6px rgba(0,0,0,0.07);'>
    <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
        <div style='flex:1;'>
            <div style='display:flex; align-items:center; gap:8px; margin-bottom:6px;'>
                <span style='background:{culoare}; color:white; padding:2px 10px;
                     border-radius:4px; font-size:10px; font-weight:700;'>{icon}</span>
                <span style='font-weight:700; color:#333;'>{nc["lpis"]} — {nc["tip"]}</span>
            </div>
            <div style='font-size:12px; color:#555; line-height:1.6;'>{nc["mesaj"]}</div>
            <div style='font-size:11px; color:{culoare}; font-weight:600; margin-top:6px;'>
                Actiune: {nc["actiune"]}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        st.divider()
        st.markdown("### Praguri de referinta APIA")
        praguri = [
            (f"> {PRAG_SUPRAFATA_AVERTISMENT_PCT}%", "Avertisment", "Nota in dosar", "#e67e22"),
            (f"> {PRAG_SUPRAFATA_PENALIZARE_PCT}%",  "Penalizare", "Reducere subventie proportionala", "#e74c3c"),
            (f"> {PRAG_SUPRAFATA_EXCLUDERE_PCT}%",   "Excludere parcela", "Excludere + penalizare an urmator", "#c0392b"),
            (f"> {PRAG_SUPRAFATA_FRAUDA_PCT}%",      "Frauda suspectata", "Sesizare control special + excludere 3 ani", "#922b21"),
        ]
        for prag, tip, actiune, culoare in praguri:
            st.markdown(f"""
<div style='display:flex; gap:12px; align-items:center; padding:6px 12px; margin:3px 0;
     background:white; border-radius:6px; font-size:11px;
     border-left:4px solid {culoare};'>
    <span style='background:{culoare}; color:white; padding:2px 8px; border-radius:4px;
         font-weight:700; min-width:60px; text-align:center;'>{prag}</span>
    <span style='font-weight:700; color:#333;'>{tip}</span>
    <span style='color:#666;'>{actiune}</span>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MONITOR LEGISLATIE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Monitor legislatie — Monitorul Oficial + Legis.ro + NLP")

    col_mon, col_nlp = st.columns([1, 1])

    with col_mon:
        st.markdown("#### Acte recente Monitorul Oficial")
        st.caption("Filtru: APIA, PAC, scheme de sprijin, MADR, fermieri")

        if st.button("Verifica acte noi", key="btn_rss"):
            with st.spinner("Preiau RSS Monitorul Oficial..."):
                acte = fetch_monitorul_oficial_rss()
            if acte:
                for act in acte:
                    st.markdown(f"""
<div style='background:white; border-radius:8px; padding:10px 12px; margin:4px 0;
     border-left:4px solid #1a5276; font-size:11px;'>
    <div style='font-weight:700; color:#1a5276;'>{act["titlu"]}</div>
    <div style='color:#888; margin-top:2px;'>{act["data"]}</div>
    <div style='margin-top:4px;'><a href='{act["link"]}' target='_blank'
         style='color:#117a65;'>Deschide act</a></div>
</div>""", unsafe_allow_html=True)
            else:
                st.info("Nu am putut prelua RSS-ul (verifica conexiunea) sau nu sunt acte noi.")

        st.divider()
        st.markdown("#### Versiune curenta scheme")
        st.markdown(f"""
<div style='background:#eaf4fb; border-radius:8px; padding:12px; font-size:12px;'>
<b>schemes_pac_2025.py</b> | Versiune: {VERSIUNE}<br>
Ultima actualizare: {DATA_ACTUALIZARE}<br><br>
<b>Surse legale incluse:</b><br>
""" + "<br>".join(f"• {s}" for s in SURSA_LEGALA) + "</div>",
            unsafe_allow_html=True)

    with col_nlp:
        st.markdown("#### Extragere automata valori din text legislativ")
        st.caption("Lipeste textul unui act normativ — NLP extrage valorile EUR/ha si pragurile")

        text_lege = st.text_area(
            "Text act normativ (extras relevant):",
            height=200,
            placeholder="Ex: Art. 7. Plata de baza se stabileste la 135 euro pe hectar...",
            key="text_lege"
        )

        if st.button("Extrage valori din text", key="btn_nlp_lege"):
            if text_lege.strip():
                valori = extrage_valori_din_text(text_lege)
                if valori:
                    st.markdown("**Valori detectate:**")
                    for v in valori:
                        st.markdown(f"""
<div style='background:white; border-radius:6px; padding:8px 12px; margin:3px 0;
     border-left:4px solid #27ae60; font-size:11px;'>
    <span style='background:#27ae60; color:white; padding:1px 6px; border-radius:3px;
         font-weight:700; font-size:10px;'>{v["tip"]}</span>
    <b style='color:#1a5276; margin-left:8px;'>{v["valoare"]}</b><br>
    <span style='color:#888; font-style:italic;'>...{v["context"]}...</span>
</div>""", unsafe_allow_html=True)
                    st.warning("Verifica valorile extrase si actualizeaza `schemes_pac_2025.py` daca sunt corecte.")
                else:
                    st.info("Nu au fost detectate valori EUR/ha sau praguri in textul introdus.")
            else:
                st.warning("Introdu textul actului normativ.")

        st.divider()
        st.markdown("#### Legis.ro — cautare rapida")
        termen_legis = st.text_input("Cauta pe Legis.ro:", placeholder="APIA scheme sprijin 2025", key="legis_search")
        if st.button("Cauta pe Legis.ro", key="btn_legis"):
            if termen_legis:
                url_legis = f"https://legislatie.just.ro/Public/CautareRapida?cuvinte={termen_legis.replace(' ', '+')}"
                st.markdown(f"**Link cautare:** [Deschide pe Legis.ro]({url_legis})")
                st.caption("Legis.ro nu permite scraping direct — link-ul deschide cautarea in browser.")
            else:
                st.warning("Introdu un termen de cautare.")
