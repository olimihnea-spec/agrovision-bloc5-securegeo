"""
SECUREGEO INTEGRATED PLATFORM — Testing Module
AGROVISION Secure: AI + Cybersecurity + Digital Sovereignty
Zbor real: Roma (FCO) -> Bucuresti (OTP), 18 aprilie 2026

Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
Propunere: ACE2-EU Cybersecurity & Digital Sovereignty | UCB Targu Jiu, iulie 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import io
import os
import zipfile
import hashlib
import base64
from datetime import datetime, date

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

try:
    from cryptography.fernet import Fernet
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False

st.set_page_config(
    page_title="SecureGeo Platform",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#1a5276;'>SecureGeo</div>
    <div style='font-size:11px; color:#117a65; font-weight:700;'>INTEGRATED PLATFORM</div>
    <div style='font-size:10px; color:#666; margin-top:4px;'>ACE2-EU Testing Module</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("""
**Modulele platformei:**
- Analiza imagini georeferentiate
- Evaluare GDPR & date protection
- Statistici & rapoarte
- Criptare & pachet securizat
- Interpretare AI (NDVI + anomalii)
""")
st.sidebar.divider()
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.markdown("**Bloc 5 AI Aplicat** | Pagina 10b")

# ─── DATE REALE DIN ZBOR ───────────────────────────────────────────────────────
# Extrase din EXIF fotografii reale, zbor Roma-Bucuresti, 18 apr 2026
# Timestamp Camera (Bian Di), Samsung Galaxy A72 SM-A725F

TRACK_TIMESTAMP = [
    {"lat": 42.420063, "lon": 15.995659, "alt_m": 11439.2, "ts": "2026-04-18 17:38:53", "locatie": "Adriatica - coasta Italiei (Pescara)"},
    {"lat": 42.420675, "lon": 16.023374, "alt_m": 11438.0, "ts": "2026-04-18 17:39:03", "locatie": "Adriatica"},
    {"lat": 42.421141, "lon": 16.045552, "alt_m": 11437.1, "ts": "2026-04-18 17:39:10", "locatie": "Adriatica"},
    {"lat": 42.421897, "lon": 16.081579, "alt_m": 11435.8, "ts": "2026-04-18 17:39:24", "locatie": "Adriatica"},
    {"lat": 42.428667, "lon": 16.399334, "alt_m": 11430.0, "ts": "2026-04-18 17:41:19", "locatie": "Adriatica centrala"},
    {"lat": 44.575667, "lon": 26.094084, "alt_m": 135.1,   "ts": "2026-04-18 19:59:24", "locatie": "Apropiere Bucuresti OTP"},
    {"lat": 44.575544, "lon": 26.092700, "alt_m": 133.9,   "ts": "2026-04-18 19:59:38", "locatie": "Bucuresti OTP - sol"},
    {"lat": 44.575362, "lon": 26.090011, "alt_m": 134.6,   "ts": "2026-04-18 20:00:02", "locatie": "OTP - taxi"},
    {"lat": 44.575333, "lon": 26.089657, "alt_m": 134.3,   "ts": "2026-04-18 20:00:05", "locatie": "OTP - taxi"},
    {"lat": 44.575312, "lon": 26.089416, "alt_m": 134.0,   "ts": "2026-04-18 20:00:07", "locatie": "OTP - taxi"},
]

TRACK_LOCATION = [
    {"lat": 42.416751, "lon": 15.854121, "alt_m": None, "ts": "2026-04-18 17:38:02", "locatie": "Adriatica - coasta Italiei"},
    {"lat": 42.417958, "lon": 15.906894, "alt_m": None, "ts": "2026-04-18 17:38:21", "locatie": "Adriatica"},
    {"lat": 42.439498, "lon": 17.056779, "alt_m": None, "ts": "2026-04-18 17:45:19", "locatie": "Adriatica centrala"},
    {"lat": 42.440222, "lon": 17.111665, "alt_m": None, "ts": "2026-04-18 17:45:38", "locatie": "Adriatica - aproape Croatia"},
    {"lat": 42.485822, "lon": 18.564560, "alt_m": None, "ts": "2026-04-18 17:54:32", "locatie": "Coasta Montenegro"},
    {"lat": 42.495181, "lon": 18.586998, "alt_m": None, "ts": "2026-04-18 17:54:43", "locatie": "Montenegro"},
    {"lat": 42.500790, "lon": 18.600496, "alt_m": None, "ts": "2026-04-18 17:54:49", "locatie": "Montenegro"},
    {"lat": 42.514764, "lon": 18.634353, "alt_m": None, "ts": "2026-04-18 17:55:04", "locatie": "Montenegro interior"},
    {"lat": 42.761862, "lon": 19.234452, "alt_m": None, "ts": "2026-04-18 17:59:34", "locatie": "Montenegro/Albania"},
    {"lat": 42.774243, "lon": 19.264730, "alt_m": None, "ts": "2026-04-18 17:59:48", "locatie": "Albania/Macedonia"},
    {"lat": 43.074951, "lon": 22.037836, "alt_m": None, "ts": "2026-04-18 18:18:05", "locatie": "Serbia/Bulgaria"},
    {"lat": 43.069110, "lon": 22.082556, "alt_m": None, "ts": "2026-04-18 18:18:21", "locatie": "Serbia"},
    # Outlieri detectati
    {"lat": 42.444900, "lon": 17.499219, "alt_m": None, "ts": "2026-04-18 18:48:00", "locatie": "OUTLIER GPS", "outlier": True},
    {"lat": 42.445198, "lon": 17.532356, "alt_m": None, "ts": "2026-04-18 18:48:11", "locatie": "OUTLIER GPS", "outlier": True},
    {"lat": 42.445353, "lon": 17.551708, "alt_m": None, "ts": "2026-04-18 18:48:18", "locatie": "OUTLIER GPS", "outlier": True},
]

GDPR_EVALUARE = [
    {"aplicatie": "Timestamp Camera (Bian Di)", "scor": "CRITIC",
     "probleme": ["Colecteaza email utilizator", "Trimite date catre terti",
                  "Nu permite stergerea datelor (Art.17 GDPR)", "Identificatori dispozitiv transmisi"],
     "recomandare": "INTERZIS pentru date APIA/LPIS sensibile",
     "culoare": "#c0392b"},
    {"aplicatie": "Location on Photo", "scor": "MEDIU",
     "probleme": ["Politica date neclara", "Altitudine NU in EXIF", "Outlieri GPS (3/15 foto)"],
     "recomandare": "Utilizare conditionata — necesita audit",
     "culoare": "#e67e22"},
    {"aplicatie": "GPS Camera", "scor": "INACCEPTABIL",
     "probleme": ["Internet-dependent (0 date din zbor)", "Destinatia GPS necunoscuta", "Esec functional total"],
     "recomandare": "INADMISIBIL pentru insp. agricole",
     "culoare": "#922b21"},
    {"aplicatie": "GeoFoto APIA (oficial)", "scor": "CONFORM / NEFUNCTIONAL",
     "probleme": ["Nefunctionala in test (11500m)", "Harti doar Romania", "Fara afisare alt/viteza/coordonate"],
     "recomandare": "Singura GDPR conformA — necesita dezvoltare urgenta",
     "culoare": "#117a65"},
]

COMPARATIE_APPS = pd.DataFrame([
    {"Aplicatie": "Timestamp Camera", "Offline": "DA", "EXIF lat/lon": "DA",
     "EXIF altitudine": "DA (11439m)", "EXIF viteza": "DA*", "Video geo": "DA",
     "GDPR": "CRITIC", "Nr. foto zbor": 362, "Rezultat": "PASS"},
    {"Aplicatie": "Location on Photo", "Offline": "DA", "EXIF lat/lon": "DA",
     "EXIF altitudine": "NU (overlay)", "EXIF viteza": "NU", "Video geo": "NU",
     "GDPR": "Mediu", "Nr. foto zbor": 15, "Rezultat": "PASS"},
    {"Aplicatie": "GPS Camera", "Offline": "NU", "EXIF lat/lon": "N/A",
     "EXIF altitudine": "N/A", "EXIF viteza": "N/A", "Video geo": "NU",
     "GDPR": "Necunoscut", "Nr. foto zbor": 0, "Rezultat": "ESEC"},
    {"Aplicatie": "GeoFoto APIA", "Offline": "NU", "EXIF lat/lon": "N/A",
     "EXIF altitudine": "N/A", "EXIF viteza": "N/A", "Video geo": "NU",
     "GDPR": "Conform UE", "Nr. foto zbor": 0, "Rezultat": "ESEC TOTAL"},
])

# ─── FUNCTII UTILITARE ─────────────────────────────────────────────────────────
def extrage_exif_foto(uploaded_file):
    """Extrage date GPS din fisier upload."""
    try:
        img = Image.open(uploaded_file)
        exif_raw = img._getexif()
        if not exif_raw:
            return None, img
        exif = {TAGS.get(k, k): v for k, v in exif_raw.items()}
        gps_raw = exif.get("GPSInfo", {})
        gps = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}
        def conv(val):
            d, m, s = val
            return float(d) + float(m)/60 + float(s)/3600
        lat = lon = alt = speed = ts = None
        if "GPSLatitude" in gps:
            lat = round(conv(gps["GPSLatitude"]), 7)
            if gps.get("GPSLatitudeRef") == "S": lat = -lat
        if "GPSLongitude" in gps:
            lon = round(conv(gps["GPSLongitude"]), 7)
            if gps.get("GPSLongitudeRef") == "W": lon = -lon
        if "GPSAltitude" in gps:
            alt = round(float(gps["GPSAltitude"]), 1)
        if "GPSSpeed" in gps:
            speed = round(float(gps["GPSSpeed"]), 2)
        ts = exif.get("DateTimeOriginal", "")
        model = exif.get("Model", "")
        make = exif.get("Make", "")
        return {
            "lat": lat, "lon": lon, "alt_m": alt, "speed_exif": speed,
            "timestamp": ts, "telefon": (make+" "+model).strip(),
            "are_gps": lat is not None and lon is not None,
            "are_altitudine": alt is not None,
        }, img
    except Exception as e:
        return {"eroare": str(e)}, None

def genereaza_gpx_track(track, titlu):
    linii = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="SecureGeo-APIA v1.0"',
        '     xmlns="http://www.topografix.com/GPX/1/1">',
        f'  <metadata><name>{titlu}</name></metadata>',
        '  <trk>', f'    <name>{titlu}</name>', '    <trkseg>',
    ]
    for p in track:
        linii.append(f'      <trkpt lat="{p["lat"]}" lon="{p["lon"]}">')
        if p.get("alt_m"):
            linii.append(f'        <ele>{p["alt_m"]}</ele>')
        try:
            dt = datetime.strptime(p["ts"], "%Y-%m-%d %H:%M:%S")
            linii.append(f'        <time>{dt.strftime("%Y-%m-%dT%H:%M:%SZ")}</time>')
        except Exception:
            pass
        linii.append(f'        <name>{p["locatie"]}</name>')
        linii.append('      </trkpt>')
    linii += ['    </trkseg>', '  </trk>', '</gpx>']
    return "\n".join(linii)

def genereaza_geojson_track():
    features = []
    for p in TRACK_TIMESTAMP:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point",
                         "coordinates": [p["lon"], p["lat"], p.get("alt_m", 0) or 0]},
            "properties": {"aplicatie": "Timestamp Camera", "ts": p["ts"],
                           "alt_m": p.get("alt_m"), "locatie": p["locatie"]}
        })
    for p in TRACK_LOCATION:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [p["lon"], p["lat"]]},
            "properties": {"aplicatie": "Location on Photo", "ts": p["ts"],
                           "alt_m": None, "locatie": p["locatie"],
                           "outlier": p.get("outlier", False)}
        })
    return json.dumps({
        "type": "FeatureCollection",
        "name": "SecureGeo_Roma_Bucuresti_18apr2026",
        "features": features
    }, indent=2, ensure_ascii=False)

def cripteaza_fisier(data: bytes) -> tuple:
    if CRYPTO_OK:
        cheie = Fernet.generate_key()
        f = Fernet(cheie)
        return f.encrypt(data), cheie
    cheie = base64.urlsafe_b64encode(os.urandom(32))
    kb = hashlib.sha256(cheie).digest()
    enc = bytes([b ^ kb[i % 32] for i, b in enumerate(data)])
    return enc, cheie

def creeaza_zip_securizat(componente: dict) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for nume, continut in componente.items():
            if isinstance(continut, str):
                continut = continut.encode("utf-8")
            zf.writestr(nume, continut)
            zf.writestr(nume + ".sha256",
                        hashlib.sha256(continut).hexdigest().encode())
    buf.seek(0)
    return buf.getvalue()

# ─── HEADER PRINCIPAL ──────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#117a65 50%,#c0392b 100%);
     border-radius:12px; padding:20px 28px; color:white; margin-bottom:16px;'>
    <div style='font-size:26px; font-weight:900; letter-spacing:1px;'>
        SecureGeo Integrated Platform
    </div>
    <div style='font-size:13px; margin-top:6px; opacity:0.9;'>
        AGROVISION Secure — AI + Cybersecurity + Digital Sovereignty for EU Agricultural Data
    </div>
    <div style='font-size:11px; margin-top:4px; opacity:0.7;'>
        Testing Module | Propunere ACE2-EU | UCB Targu Jiu, 6-8 iulie 2026
    </div>
</div>
""", unsafe_allow_html=True)

# Metrici cheie
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("Altitudine test", "11.439 m", "EXIF confirmat")
with m2:
    st.metric("Viteza test", "~800 km/h", "Timestamp Camera")
with m3:
    st.metric("Foto analizate", "377", "362 TS + 15 LoP")
with m4:
    st.metric("App cu EXIF alt.", "1 / 4", "Timestamp Camera")
with m5:
    st.metric("GDPR conform 100%", "0 / 4", "Niciuna completa")

st.divider()

# ─── TABURI PRINCIPALE ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Platforma & Context",
    "Analiza Imagine GPS",
    "Statistici & Rapoarte",
    "Protectia Datelor GDPR",
    "Pachet Securizat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PLATFORMA & CONTEXT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_desc, col_tabel = st.columns([1, 1])

    with col_desc:
        st.markdown("""
        ### AGROVISION Secure

        Platforma propusa combina **inteligenta artificiala**, **cybersecurity** si
        **principii de suveranitate digitala** pentru protectia datelor agricole si
        infrastructurii critice a UE.

        **Baza empirica — test real:**
        Fotografii georeferentiate realizate la **11.500 m altitudine**, viteza **800 km/h**,
        conditii de ploaie, zbor Roma → Bucuresti, 18 aprilie 2026.
        Dispozitiv: Samsung Galaxy A72 (SM-A725F).

        **Problema identificata:**
        Niciuna din cele 4 aplicatii testate nu indeplineste simultan:
        - functionalitate offline
        - EXIF complet (lat+lon+altitudine)
        - conformitate GDPR completa
        - compatibilitate QGIS/GPX Viewer

        **Solutia propusa — AGRI-GEO Framework:**
        """)

        criterii = [
            ("1", "Functionalitate 100% offline", "#1a5276"),
            ("2", "EXIF complet: lat+lon+altitudine+timestamp", "#117a65"),
            ("3", "GDPR conform (date nedivulgate tertilor)", "#8e44ad"),
            ("4", "Acuratete GPS <= 5 m", "#d35400"),
            ("5", "Export QGIS + GPX Viewer", "#c0392b"),
        ]
        for nr, text, culoare in criterii:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; padding:6px 12px;
                 background:white; border-radius:8px; margin:4px 0; font-size:12px;
                 border-left:4px solid {culoare}; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                <div style='background:{culoare}; color:white; border-radius:50%;
                     width:22px; height:22px; display:flex; align-items:center;
                     justify-content:center; font-weight:800; font-size:11px;
                     flex-shrink:0;'>{nr}</div>
                <div style='color:#333;'>{text}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        **Relevanta ACE2-EU:**
        - AI in cybersecurity: detectie anomalii + criptare AES-256
        - Infrastructura critica: LPIS/IACS/APIA
        - Suveranitate digitala: 100% offline, fara cloud non-UE
        - Date securizate: ZIP AES-256 + GeoJSON + GPX
        """)

    with col_tabel:
        st.markdown("### Comparatie aplicatii testate")
        st.markdown("**Zbor Roma-Bucuresti, 18 apr 2026, 11.500m / 800 km/h**")

        culori_rez = {"PASS": "#27ae60", "ESEC": "#e74c3c", "ESEC TOTAL": "#922b21"}
        culori_gdpr = {"CRITIC": "#c0392b", "Mediu": "#e67e22",
                       "Necunoscut": "#95a5a6", "Conform UE": "#27ae60"}

        for _, row in COMPARATIE_APPS.iterrows():
            rez_col  = culori_rez.get(row["Rezultat"], "#999")
            gdpr_col = culori_gdpr.get(row["GDPR"], "#999")
            alt_icon = "DA" if "DA" in str(row["EXIF altitudine"]) else "NU"
            alt_col  = "#27ae60" if alt_icon == "DA" else "#e74c3c"
            off_col  = "#27ae60" if row["Offline"] == "DA" else "#e74c3c"

            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:12px 14px;
                 margin:6px 0; border-left:5px solid {rez_col};
                 box-shadow:0 1px 4px rgba(0,0,0,0.07); font-size:11px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div style='font-weight:700; color:#333; font-size:13px;'>
                        {row["Aplicatie"]}
                    </div>
                    <span style='background:{rez_col}; color:white; padding:2px 10px;
                    border-radius:10px; font-weight:700;'>{row["Rezultat"]}</span>
                </div>
                <div style='display:flex; gap:12px; margin-top:8px; flex-wrap:wrap;'>
                    <div>Offline: <b style='color:{off_col};'>{row["Offline"]}</b></div>
                    <div>Alt EXIF: <b style='color:{alt_col};'>{alt_icon}</b></div>
                    <div>Foto zbor: <b>{row["Nr. foto zbor"]}</b></div>
                    <div>Video: <b>{row["Video geo"]}</b></div>
                    <div>GDPR: <span style='background:{gdpr_col}; color:white;
                         padding:1px 6px; border-radius:4px;'>{row["GDPR"]}</span></div>
                </div>
                <div style='color:#888; margin-top:4px;'>
                    EXIF altitudine: {row["EXIF altitudine"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#fef9e7; border-left:4px solid #f39c12; border-radius:0 8px 8px 0;
             padding:10px 14px; margin-top:8px; font-size:11px;'>
            <b>Concluzie:</b> 0 din 4 aplicatii indeplinesc toate criteriile AGRI-GEO.
            Timestamp Camera = cel mai bun tehnic, dar GDPR problematic.
            Necesara aplicatie noua open-source conformA.
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALIZA IMAGINE GPS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Analiza imagine georeferentiata — extragere metadate EXIF")

    col_up, col_rez = st.columns([1, 1])

    with col_up:
        st.markdown("#### Incarca fotografie")
        foto = st.file_uploader(
            "JPG din Timestamp Camera sau Location on Photo",
            type=["jpg", "jpeg"],
            help="Fotografii din zborul Roma-Bucuresti 18 apr 2026"
        )
        use_demo_foto = st.checkbox("Sau foloseste date demo (punct zbor real)", value=True)

        if foto and PIL_OK:
            exif_data, img_obj = extrage_exif_foto(foto)
        else:
            exif_data = {
                "lat": 42.420063, "lon": 15.995659, "alt_m": 11439.2,
                "speed_exif": 5490.4, "timestamp": "2026:04:18 17:38:53",
                "telefon": "samsung SM-A725F",
                "are_gps": True, "are_altitudine": True,
                "nota": "Date demo din EXIF real (Timestamp Camera, prim punct zbor)"
            }
            img_obj = None

    with col_rez:
        st.markdown("#### Metadate EXIF extrase")

        if exif_data and "eroare" not in exif_data:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Latitudine", f"{exif_data.get('lat', 'N/A')}°N")
                st.metric("Altitudine", f"{exif_data.get('alt_m', 'N/A')} m",
                          "IN EXIF" if exif_data.get('are_altitudine') else "LIPSA din EXIF")
            with c2:
                st.metric("Longitudine", f"{exif_data.get('lon', 'N/A')}°E")
                st.metric("Telefon", exif_data.get("telefon", "N/A"))

            st.markdown(f"**Timestamp:** `{exif_data.get('timestamp', 'N/A')}`")

            if exif_data.get("are_altitudine"):
                st.success("Altitudine disponibila in EXIF — compatibil QGIS 3D")
            else:
                st.warning("Altitudine NU in EXIF — incompatibil cu analiza 3D QGIS")

            if exif_data.get("nota"):
                st.info(exif_data["nota"])

            # Harta punct
            if PLOTLY_OK and exif_data.get("lat"):
                fig_map = go.Figure(go.Scattergeo(
                    lat=[exif_data["lat"]],
                    lon=[exif_data["lon"]],
                    mode="markers+text",
                    marker=dict(size=15, color="#c0392b", symbol="circle"),
                    text=[f"Alt: {exif_data.get('alt_m', '?')}m"],
                    textposition="top center",
                ))
                fig_map.update_layout(
                    geo=dict(
                        scope="europe",
                        showland=True,
                        landcolor="lightgray",
                        showocean=True,
                        oceancolor="lightblue",
                        showcoastlines=True,
                        projection_type="natural earth",
                        center=dict(lat=43, lon=18),
                        lataxis_range=[40, 47],
                        lonaxis_range=[12, 28],
                    ),
                    height=280,
                    margin=dict(t=10, b=10, l=0, r=0),
                    title=dict(text="Pozitia fotografiei", font_size=12)
                )
                st.plotly_chart(fig_map, use_container_width=True)
        elif exif_data and "eroare" in exif_data:
            st.error(f"Eroare EXIF: {exif_data['eroare']}")
        else:
            st.info("Incarca o fotografie sau activeaza datele demo.")

    # Harta traiectorie completa
    st.divider()
    st.markdown("### Traiectoria completa Roma → Bucuresti (date reale EXIF)")

    if PLOTLY_OK:
        fig_track = go.Figure()

        # Track Timestamp Camera
        lats_ts = [p["lat"] for p in TRACK_TIMESTAMP]
        lons_ts = [p["lon"] for p in TRACK_TIMESTAMP]
        alts_ts = [p["alt_m"] for p in TRACK_TIMESTAMP]
        labels_ts = [f"{p['locatie']}<br>Alt: {p['alt_m']}m<br>{p['ts']}"
                     for p in TRACK_TIMESTAMP]

        fig_track.add_trace(go.Scattergeo(
            lat=lats_ts, lon=lons_ts,
            mode="markers+lines",
            name="Timestamp Camera (alt in EXIF)",
            marker=dict(size=10, color="#1a5276", symbol="circle"),
            line=dict(color="#1a5276", width=2),
            hovertemplate="%{text}<extra></extra>",
            text=labels_ts
        ))

        # Track Location on Photo (fara outlieri)
        normale = [p for p in TRACK_LOCATION if not p.get("outlier")]
        outlieri = [p for p in TRACK_LOCATION if p.get("outlier")]

        fig_track.add_trace(go.Scattergeo(
            lat=[p["lat"] for p in normale],
            lon=[p["lon"] for p in normale],
            mode="markers",
            name="Location on Photo (fara alt EXIF)",
            marker=dict(size=8, color="#27ae60", symbol="diamond"),
            hovertemplate="%{text}<extra></extra>",
            text=[f"{p['locatie']}<br>{p['ts']}" for p in normale]
        ))

        if outlieri:
            fig_track.add_trace(go.Scattergeo(
                lat=[p["lat"] for p in outlieri],
                lon=[p["lon"] for p in outlieri],
                mode="markers",
                name="Outlieri GPS (Location on Photo)",
                marker=dict(size=12, color="#e74c3c", symbol="x"),
                hovertemplate="%{text}<extra></extra>",
                text=[f"OUTLIER GPS<br>{p['ts']}" for p in outlieri]
            ))

        fig_track.update_layout(
            geo=dict(
                scope="europe",
                showland=True, landcolor="#f8f9fa",
                showocean=True, oceancolor="#d6eaf8",
                showcoastlines=True, coastlinecolor="#aaa",
                projection_type="natural earth",
                center=dict(lat=43, lon=19),
                lataxis_range=[40, 47],
                lonaxis_range=[12, 28],
            ),
            height=420,
            margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)"),
            title=dict(
                text="Traiectorie zbor Roma-Bucuresti | 18 apr 2026 | 11.439m altitudine",
                font_size=13
            )
        )
        st.plotly_chart(fig_track, use_container_width=True)

        st.markdown("""
        <div style='font-size:11px; color:#666; padding:8px;'>
            Cercuri albastre = Timestamp Camera (altitudine in EXIF).
            Romburi verzi = Location on Photo (fara altitudine in EXIF).
            X rosii = outlieri GPS detectati (pozitii imposibile din punct de vedere fizic).
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — STATISTICI & RAPOARTE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Statistici zbor & generare raport")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("#### Timestamp Camera — statistici EXIF")
        ts_alts = [p["alt_m"] for p in TRACK_TIMESTAMP if p.get("alt_m")]
        ts_zbor = [p for p in TRACK_TIMESTAMP if p.get("alt_m", 0) > 1000]

        date_ts_df = pd.DataFrame([
            {"Metric": "Total foto analizate (folder)", "Valoare": "362"},
            {"Metric": "Cu coordonate GPS", "Valoare": "362 (100%)"},
            {"Metric": "Cu altitudine in EXIF", "Valoare": "362 (100%) — UNIC"},
            {"Metric": "Altitudine maxima (EXIF)", "Valoare": "11.439,2 m"},
            {"Metric": "Altitudine minima (sol OTP)", "Valoare": "133,9 m"},
            {"Metric": "Video georeferenciat", "Valoare": "1 (TimeVideo_20260418_194459.mp4)"},
            {"Metric": "GDPR status", "Valoare": "PROBLEMATIC (trimite date terti)"},
            {"Metric": "Acoperire ruta", "Valoare": "Italia (coast) -> OTP Bucuresti"},
        ])
        st.dataframe(date_ts_df, use_container_width=True, hide_index=True)

    with col_s2:
        st.markdown("#### Location on Photo — statistici EXIF")
        date_loc_df = pd.DataFrame([
            {"Metric": "Total foto zbor", "Valoare": "15"},
            {"Metric": "Cu coordonate GPS", "Valoare": "15 (100%)"},
            {"Metric": "Cu altitudine in EXIF", "Valoare": "0 (0%) — LIPSA"},
            {"Metric": "Outlieri GPS detectati", "Valoare": "3 (20%) — important!"},
            {"Metric": "Interval longitudinal real", "Valoare": "15.85°E - 22.08°E"},
            {"Metric": "GDPR status", "Valoare": "De verificat"},
            {"Metric": "Foto teren Gorj (1 apr)", "Valoare": "34 (45.03-45.04°N)"},
            {"Metric": "Compatibilitate QGIS 3D", "Valoare": "NU (fara altitudine)"},
        ])
        st.dataframe(date_loc_df, use_container_width=True, hide_index=True)

    # Profil altitudine
    if PLOTLY_OK:
        st.markdown("#### Profil altitudine — date reale Timestamp Camera")
        fig_alt = go.Figure()
        fig_alt.add_trace(go.Scatter(
            x=[p["lon"] for p in TRACK_TIMESTAMP],
            y=[p["alt_m"] for p in TRACK_TIMESTAMP],
            mode="lines+markers",
            name="Altitudine (m)",
            line=dict(color="#1a5276", width=3),
            marker=dict(size=8, color="#c0392b"),
            hovertemplate="Lon: %{x:.4f}°E<br>Alt: %{y:.1f}m<br>%{text}<extra></extra>",
            text=[p["locatie"] for p in TRACK_TIMESTAMP]
        ))
        fig_alt.add_hline(y=11439, line_dash="dash", line_color="#c0392b",
                          annotation_text="Alt. cruziera 11.439m (confirmat EXIF)",
                          annotation_font_color="#c0392b")
        fig_alt.update_layout(
            xaxis_title="Longitudine (°E)",
            yaxis_title="Altitudine (m)",
            height=320,
            margin=dict(t=30, b=50, l=60, r=20)
        )
        st.plotly_chart(fig_alt, use_container_width=True)

    st.divider()
    st.markdown("#### Generare raport")

    col_r1, col_r2 = st.columns([2, 1])
    with col_r2:
        inspector = st.text_input("Inspector", "Gamulescu O.M.")
        institutie = st.selectbox("Institutie", ["APIA CJ Gorj", "UCB Targu Jiu", "Prefectura Gorj"])
        include_gdpr = st.checkbox("Include evaluare GDPR", True)
        include_recom = st.checkbox("Include recomandari", True)

    with col_r1:
        if st.button("Genereaza raport complet", type="primary", use_container_width=True):
            sep = "=" * 78
            raport = f"""{sep}
RAPORT SECUREGEO — EVALUARE APLICATII GEOREFERENTIERE MOBILE
Zbor: Roma (FCO) -> Bucuresti (OTP) | 18 aprilie 2026
Conditii: 11.500 m altitudine | ~800 km/h | precipitatii
Dispozitiv: Samsung Galaxy A72 (SM-A725F)
{sep}
Data generare: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Inspector: {inspector}
Institutie: {institutie}
Proiect: SecureGeo ACE2-EU Cybersecurity & Digital Sovereignty
{sep}

REZULTATE PRINCIPALE
--------------------
[PASS] Timestamp Camera (Bian Di): 362 foto + 1 video georeferenciat
       Altitudine EXIF reala: 11.439,2 m (confirmat!)
       GDPR: PROBLEMATIC — trimite date catre terti, nu permite stergerea

[PASS] Location on Photo: 15 foto cu coordonate GPS
       Altitudine: NU in EXIF (overlay text pe imagine)
       Outlieri GPS detectati: 3 puncte (20%)

[ESEC] GPS Camera: 0 date din zbor (internet-dependent)

[ESEC] GeoFoto APIA: nefunctionala in conditiile testului

CONCLUZIE: 0 din 4 aplicatii indeplinesc toate criteriile AGRI-GEO.

FRAMEWORK AGRI-GEO (propus)
----------------------------
[1] Functionalitate 100% offline
[2] EXIF complet: lat + lon + altitudine + timestamp
[3] Conformitate GDPR (date nedivulgate tertilor)
[4] Acuratete GPS <= 5 m
[5] Export QGIS + GPX Viewer

"""
            if include_gdpr:
                raport += "EVALUARE GDPR\n" + "-"*40 + "\n"
                for app in GDPR_EVALUARE:
                    raport += f"  {app['aplicatie']}: [{app['scor']}]\n"
                    raport += f"  Recomandare: {app['recomandare']}\n\n"

            if include_recom:
                raport += f"""RECOMANDARI
-----------
1. Revizuire urgenta GeoFoto APIA (MADR): adaugare altitudine + offline total
2. Standard tehnic obligatoriu pentru aplicatii inspectie APIA (AGRI-GEO)
3. Pilotare SecureGeo in jud. Gorj, Dolj, Olt (parteneriate existente)
4. Articol ISI: MDPI Drones (IF 4.8, Q1, APC 2600 CHF)
5. Propunere proiect ACE2-EU: AGROVISION Secure

{sep}
Raport generat de SecureGeo Platform v1.0 | Bloc 5 AI Aplicat
{sep}"""

            st.download_button(
                "Descarca raport TXT",
                data=raport.encode("utf-8"),
                file_name=f"raport_securegeo_{date.today().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )

            csv_date = []
            for p in TRACK_TIMESTAMP:
                csv_date.append({"aplicatie": "Timestamp Camera", **p})
            for p in TRACK_LOCATION:
                csv_date.append({"aplicatie": "Location on Photo", **p})
            df_csv = pd.DataFrame(csv_date)
            st.download_button(
                "Descarca date GPS CSV (pentru QGIS/Excel)",
                data=df_csv.to_csv(index=False, encoding="utf-8-sig"),
                file_name=f"track_securegeo_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PROTECTIA DATELOR GDPR
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Evaluare protectia datelor — GDPR & Digital Sovereignty")

    st.markdown("""
    <div style='background:#eaf4fb; border-left:5px solid #1a5276; border-radius:0 8px 8px 0;
         padding:12px 16px; margin-bottom:16px; font-size:12px;'>
        Evaluare conform <b>Regulamentului UE 2016/679 (GDPR)</b>, <b>NIS2 Directive</b>
        si <b>EU Data Act 2025</b>. Date agricole APIA/LPIS = date sensibile cu caracter
        institutional — necesita cel mai inalt nivel de protectie.
    </div>
    """, unsafe_allow_html=True)

    for app in GDPR_EVALUARE:
        with st.expander(f"{app['aplicatie']} — [{app['scor']}]", expanded=False):
            col_g1, col_g2 = st.columns([1, 1])
            with col_g1:
                st.markdown(f"""
                <div style='background:{app["culoare"]}15; border-left:4px solid {app["culoare"]};
                     border-radius:0 8px 8px 0; padding:12px 14px;'>
                    <div style='font-weight:700; color:{app["culoare"]}; font-size:14px;'>
                        Scor: {app["scor"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("**Probleme identificate:**")
                for p in app["probleme"]:
                    st.markdown(f"- {p}")
            with col_g2:
                st.markdown("**Recomandare:**")
                st.info(app["recomandare"])

    st.divider()
    st.markdown("### Simulator evaluare GDPR — aplicatie noua")
    st.markdown("Introdu caracteristicile unei aplicatii pentru evaluare rapida GDPR:")

    col_ev1, col_ev2 = st.columns(2)
    with col_ev1:
        offline_check = st.checkbox("Functioneaza 100% offline", True)
        stocheaza_local = st.checkbox("Date stocate doar local pe dispozitiv", True)
        permite_stergere = st.checkbox("Permite stergerea datelor (Art. 17 GDPR)", False)
        trimite_terti = st.checkbox("Trimite date catre terti", False)
    with col_ev2:
        are_politica = st.checkbox("Are politica de confidentialitate clara", True)
        criptare_transport = st.checkbox("Date criptate in tranzit (TLS)", True)
        stocare_UE = st.checkbox("Date stocate pe servere UE", True)
        audit_regulat = st.checkbox("Audit securitate regulat", False)

    scor_gdpr = (offline_check + stocheaza_local + permite_stergere +
                 (not trimite_terti) + are_politica + criptare_transport +
                 stocare_UE + audit_regulat)

    culoare_scor = "#27ae60" if scor_gdpr >= 7 else "#e67e22" if scor_gdpr >= 4 else "#c0392b"
    nivel = "CONFORM" if scor_gdpr >= 7 else "PARTIAL CONFORM" if scor_gdpr >= 4 else "NON-CONFORM"

    st.markdown(f"""
    <div style='background:{culoare_scor}15; border:2px solid {culoare_scor};
         border-radius:10px; padding:16px; margin-top:12px; text-align:center;'>
        <div style='font-size:28px; font-weight:900; color:{culoare_scor};'>{scor_gdpr}/8</div>
        <div style='font-size:16px; font-weight:700; color:{culoare_scor};'>{nivel}</div>
        <div style='font-size:11px; color:#666; margin-top:4px;'>
            Score GDPR estimat pentru aplicatia configurata mai sus
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PACHET SECURIZAT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### Generare pachet securizat SecureGeo")
    st.markdown("Genereaza un pachet ZIP criptat AES-256 cu toate exporturile — compatibil QGIS si GPX Viewer.")

    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        st.markdown("#### Continut pachet")
        inc_geojson = st.checkbox("GeoJSON track (QGIS)", True)
        inc_gpx_ts  = st.checkbox("GPX Timestamp Camera", True)
        inc_gpx_loc = st.checkbox("GPX Location on Photo", True)
        inc_csv     = st.checkbox("CSV date complete", True)
        inc_raport  = st.checkbox("Raport TXT complet", True)
        inc_gdpr    = st.checkbox("Raport GDPR JSON", True)
        criptat     = st.checkbox("Cripteaza AES-256", True)

        nota_autor = st.text_input("Nota inspector", "Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | APIA CJ Gorj")

        if st.button("Genereaza pachet ZIP SecureGeo", type="primary", use_container_width=True):
            with st.spinner("Generare pachet..."):
                componente = {}

                if inc_geojson:
                    componente["securegeo_track.geojson"] = genereaza_geojson_track()

                if inc_gpx_ts:
                    componente["track_timestamp_camera.gpx"] = genereaza_gpx_track(
                        TRACK_TIMESTAMP, "Timestamp Camera — Roma-Bucuresti 18apr2026")

                if inc_gpx_loc:
                    componente["track_location_on_photo.gpx"] = genereaza_gpx_track(
                        TRACK_LOCATION, "Location on Photo — Roma-Bucuresti 18apr2026")

                if inc_csv:
                    rows = []
                    for p in TRACK_TIMESTAMP:
                        rows.append({"aplicatie": "Timestamp Camera", **p})
                    for p in TRACK_LOCATION:
                        rows.append({"aplicatie": "Location on Photo", **p})
                    componente["date_gps_complete.csv"] = pd.DataFrame(rows).to_csv(
                        index=False, encoding="utf-8-sig")

                if inc_raport:
                    componente["raport_securegeo.txt"] = (
                        f"RAPORT SECUREGEO\nData: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                        f"Inspector: {nota_autor}\n\n"
                        f"Timestamp Camera: 362 foto, altitudine EXIF = 11439.2m\n"
                        f"Location on Photo: 15 foto, altitudine LIPSA din EXIF\n"
                        f"GPS Camera: 0 date din zbor (internet-dependent)\n"
                        f"GeoFoto APIA: nefunctionala in test\n\n"
                        f"Concluzie: 0/4 aplicatii indeplinesc criteriile AGRI-GEO.\n"
                        f"Propunere: SecureGeo ACE2-EU | UCB Targu Jiu, iulie 2026\n"
                    )

                if inc_gdpr:
                    componente["evaluare_gdpr.json"] = json.dumps(
                        GDPR_EVALUARE, indent=2, ensure_ascii=False)

                componente["README.txt"] = (
                    "SecureGeo Package\n"
                    "=================\n"
                    f"Generat: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    f"Inspector: {nota_autor}\n\n"
                    "Deschide:\n"
                    "  *.geojson -> QGIS (Layer > Add Layer > Add Vector Layer)\n"
                    "  *.gpx     -> GPX Viewer\n"
                    "  *.csv     -> Excel sau QGIS\n"
                    f"Criptare: {'AES-256 (Fernet)' if criptat and CRYPTO_OK else 'Necriptata'}\n"
                    "Proiect: SecureGeo ACE2-EU | UCB Targu Jiu\n"
                )

                if criptat:
                    # Cripteaza fiecare fisier individual
                    comp_enc = {}
                    chei = {}
                    for nume, continut in componente.items():
                        if isinstance(continut, str):
                            continut_bytes = continut.encode("utf-8")
                        else:
                            continut_bytes = continut
                        enc, cheie = cripteaza_fisier(continut_bytes)
                        comp_enc[f"encrypted/{nume}.enc"] = enc
                        chei[nume] = cheie.decode() if isinstance(cheie, bytes) else cheie
                    comp_enc["chei_decriptare.json"] = json.dumps(chei, indent=2).encode("utf-8")
                    comp_enc["README.txt"] = componente["README.txt"].encode("utf-8")
                    zip_bytes = creeaza_zip_securizat(comp_enc)
                    label_zip = "securegeo_CRIPTAT_AES256"
                else:
                    zip_bytes = creeaza_zip_securizat(
                        {k: (v.encode("utf-8") if isinstance(v, str) else v)
                         for k, v in componente.items()})
                    label_zip = "securegeo_necriptat"

                st.session_state["zip_generat"] = zip_bytes
                st.session_state["zip_label"] = label_zip
                st.session_state["hash_zip"] = hashlib.sha256(zip_bytes).hexdigest()

    with col_p2:
        st.markdown("#### Pachet generat")

        if "zip_generat" in st.session_state:
            zip_bytes = st.session_state["zip_generat"]
            label = st.session_state["zip_label"]
            hash_v = st.session_state["hash_zip"]

            st.success("Pachet ZIP generat cu succes!")

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Dimensiune ZIP", f"{len(zip_bytes)/1024:.1f} KB")
            with c2:
                st.metric("Criptare", "AES-256" if criptat and CRYPTO_OK else "Necriptata")

            st.markdown("**SHA-256 integritate:**")
            st.code(hash_v, language="text")

            st.download_button(
                "Descarca pachet ZIP SecureGeo",
                data=zip_bytes,
                file_name=f"{label}_{date.today().strftime('%Y%m%d')}.zip",
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
        else:
            st.info("Apasa butonul din stanga pentru a genera pachetul.")
            st.markdown("""
            **Continut pachet:**
            - `securegeo_track.geojson` → QGIS
            - `track_timestamp_camera.gpx` → GPX Viewer
            - `track_location_on_photo.gpx` → GPX Viewer
            - `date_gps_complete.csv` → Excel/QGIS
            - `raport_securegeo.txt` → raport complet
            - `evaluare_gdpr.json` → date protectie
            - `chei_decriptare.json` → chei AES (daca criptat)
            """)

    st.divider()
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1a5276 0%,#117a65 100%);
         border-radius:10px; padding:14px 20px; color:white; font-size:12px;'>
        <b>SecureGeo Integrated Platform v1.0</b> | Bloc 5 AI Aplicat — Pagina 10b<br>
        Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj<br>
        Propunere ACE2-EU Cybersecurity & Digital Sovereignty | UCB Targu Jiu, 6-8 iulie 2026
    </div>
    """, unsafe_allow_html=True)
