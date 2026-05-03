"""
SECUREGEO GLOBAL FRAMEWORK — GNSS Behaviour Under Extreme Conditions
Cercetare empirica: +11.439 m (aviatie) la -30 m (submarin, Atlantic)
Implicatii GDPR + Regulamentul UE 2024/1689 (Actul AI)

Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu
       Facultatea de Inginerie, UCB Targu Jiu | APIA CJ Gorj
Publicatie: Zenodo Preprint 2026 | target MDPI Sensors (IF 3.4)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import io, math

try:
    from PIL import Image as PILImage
    from PIL.ExifTags import TAGS, GPSTAGS
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

# ─── HELPER FUNCTIONS TAB D ───────────────────────────────────────────────────

def _safe_f(val):
    try:
        if hasattr(val, 'numerator'):
            return float(val.numerator) / float(val.denominator)
        return float(val)
    except:
        return None

def _dms_dd(dms, ref):
    try:
        d = _safe_f(dms[0]) or 0
        m = _safe_f(dms[1]) or 0
        s = _safe_f(dms[2]) or 0
        dd = d + m/60 + s/3600
        if isinstance(ref, bytes):
            ref = ref.decode('ascii', errors='ignore').strip('\x00')
        if ref in ['S', 'W']:
            dd = -dd
        return round(dd, 7)
    except:
        return None

def _alt_m(gps_data):
    try:
        alt = gps_data.get('GPSAltitude')
        if alt is None:
            return None
        alt_m = _safe_f(alt)
        ref = gps_data.get('GPSAltitudeRef', 0)
        if ref == b'\x01' or ref == 1:
            alt_m = -alt_m
        return round(alt_m, 2) if alt_m is not None else None
    except:
        return None

def _approx_geoid(lat, lon):
    """Aproximare grosiera ondulare geoid EGM96 (eroare ±15m — doar pentru indicatie)."""
    if lat is None or lon is None:
        return 25.0
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    N = (25 * math.cos(lat_r)
         - 5 * math.cos(2 * lat_r)
         + 8 * math.cos(lon_r) * math.cos(lat_r)
         + 5)
    return round(N, 1)

def _eval_agri_geo_d(has_gps, lat_dd, lon_dd, alt_m, all_exif, phantom_score):
    results = []
    results.append(("AG-1", "Georef. Offline", "N/A",
        "Nu se poate determina offline capability dintr-o fotografie izolata.", "#6c757d"))
    if has_gps and alt_m is not None and all_exif.get('DateTimeOriginal'):
        ag2_s, ag2_c = "DA", "#27ae60"
        ag2_d = f"Lat + Lon + Alt ({alt_m}m) + DateTime prezente in EXIF"
    elif has_gps and alt_m is None:
        ag2_s, ag2_c = "PARTIAL", "#e67e22"
        ag2_d = "Lat + Lon prezente, ALTITUDINEA lipseste din EXIF"
    elif has_gps:
        ag2_s, ag2_c = "PARTIAL", "#e67e22"
        ag2_d = "GPS prezent dar EXIF incomplet (alt sau datetime absent)"
    else:
        ag2_s, ag2_c = "NU", "#c0392b"
        ag2_d = "GPS absent din EXIF"
    results.append(("AG-2", "EXIF Complet", ag2_s, ag2_d, ag2_c))
    results.append(("AG-3", "Conformitate GDPR", "N/A",
        "Conformitatea GDPR a aplicatiei nu se poate evalua dintr-o fotografie.", "#6c757d"))
    gps_dop = all_exif.get('GPSDOP')
    if gps_dop:
        dop_val = _safe_f(gps_dop)
        if dop_val and dop_val <= 2:
            results.append(("AG-4", "Acuratete GPS", "DA",
                f"PDOP = {dop_val:.1f} (excelent)", "#27ae60"))
        elif dop_val and dop_val <= 5:
            results.append(("AG-4", "Acuratete GPS", "PARTIAL",
                f"PDOP = {dop_val:.1f} (acceptabil)", "#e67e22"))
        else:
            results.append(("AG-4", "Acuratete GPS", "NU",
                f"PDOP = {dop_val:.1f} (slab, >5)", "#c0392b"))
    else:
        results.append(("AG-4", "Acuratete GPS", "N/A",
            "Tag GPSDOP absent — acuratete nedeterminabila din EXIF", "#6c757d"))
    results.append(("AG-5", "Interoperabilitate", "N/A",
        "Nu se evalueaza dintr-o fotografie izolata.", "#6c757d"))
    if not has_gps:
        results.append(("AG-6", "Divulg. GNSS", "N/A", "Fara GPS.", "#6c757d"))
    elif phantom_score >= 60:
        results.append(("AG-6", "Divulg. GNSS", "NU",
            "CRITIC: indicatori puternici phantom — pierdere semnal nedivulgata", "#c0392b"))
    elif phantom_score >= 35:
        results.append(("AG-6", "Divulg. GNSS", "NU",
            "ATENTIE: indicatori moderati phantom — verificare manuala necesara", "#e67e22"))
    elif alt_m is None:
        results.append(("AG-6", "Divulg. GNSS", "PARTIAL",
            "Altitudine absenta — AG-6 nu se poate confirma", "#e67e22"))
    else:
        results.append(("AG-6", "Divulg. GNSS", "DA",
            "Niciun indicator phantom detectat — date GPS aparent valide", "#27ae60"))
    return results

# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SecureGeo Global Framework",
    page_icon="G",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.sgf-header {
    background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
    padding: 28px 32px; border-radius: 14px; margin-bottom: 24px; color: white;
}
.sgf-header h1 { font-size: 2rem; font-weight: 900; margin: 0 0 6px 0; }
.sgf-header p  { font-size: 0.95rem; margin: 0; opacity: 0.9; }
.metric-card {
    background: #f8faff; border: 2px solid #e8eeff;
    border-radius: 10px; padding: 16px; text-align: center;
}
.metric-card .val { font-size: 2rem; font-weight: 900; color: #1a2980; }
.metric-card .lbl { font-size: 0.8rem; color: #555; margin-top: 4px; }
.phase-box {
    border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;
    border-left: 5px solid;
}
.agri-row {
    background: #f8faff; border-radius: 8px; padding: 12px 16px;
    margin-bottom: 6px; border-left: 4px solid #1a5276;
}
.agri-row.new { border-left-color: #c0392b; background: #fef9f9; }
.finding-box {
    background: #fff3cd; border: 1px solid #ffc107;
    border-radius: 8px; padding: 14px; margin: 10px 0;
}
.doi-box {
    background: #eafaf1; border: 1px solid #27ae60;
    border-radius: 8px; padding: 14px; text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:26px; font-weight:900; color:#1a2980;'>SecureGeo</div>
    <div style='font-size:10px; color:#117a65; font-weight:700;'>GLOBAL FRAMEWORK</div>
    <div style='font-size:10px; color:#666; margin-top:4px;'>GNSS Extreme Research</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("""
**Experimente empirice:**
- Zbor comercial +11.439 m (aviatie)
- Submarin turistic -30 m (Atlantic)

**Cadru propus:**
- AGRI-GEO Framework (6 criterii)
- AG-6: Divulgare pierdere GNSS

**Implicatii:**
- GDPR Art. 5(1)(d) — acuratete
- Actul AI Art. 10(2)(b) — date
""")
st.sidebar.divider()
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.markdown("**Bloc 5 AI Aplicat** | Pagina 10c")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#1a2980; border-radius:8px; padding:10px 12px; color:white; font-size:10px; line-height:1.7;'>
<div style='font-size:11px; font-weight:900; margin-bottom:6px;'>&copy; 2026 Proprietate intelectuala</div>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj<br>
<b>DOI:</b> 10.5281/zenodo.19829462<br>
<b>Lege:</b> Legea nr. 8/1996<br>
<div style='margin-top:6px; opacity:0.8; font-size:9px;'>
Citare obligatorie la orice utilizare a datelor sau metodologiei.
</div>
</div>
""", unsafe_allow_html=True)

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sgf-header">
    <h1>SecureGeo Global Framework</h1>
    <p>Comportamentul GNSS in conditii extreme: de la +11.439 m (aviatie comerciala)
    la -30 m (submarin turistic, Oceanul Atlantic, Tenerife)<br>
    Studiu tri-continental: Romania | Tenerife (Atlantic) | Dubai + Abu Dhabi (Golf Persic)<br>
    Implicatii pentru integritatea datelor in sisteme AI — GDPR + Regulamentul UE 2024/1689</p>
</div>
""", unsafe_allow_html=True)

# ─── METRICI CHEIE ─────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.markdown("""<div class="metric-card">
    <div class="val">11.469</div>
    <div class="lbl">m altitudine totala<br>range documentat</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="metric-card">
    <div class="val">1.406</div>
    <div class="lbl">fotografii EXIF<br>analizate total</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="metric-card">
    <div class="val" style="color:#c0392b;">326+</div>
    <div class="lbl">fotografii GPS<br>fantoma confirmate</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="metric-card">
    <div class="val">70 m</div>
    <div class="lbl">diferenta geoid<br>Tenerife vs Abu Dhabi</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown("""<div class="metric-card">
    <div class="val">3</div>
    <div class="lbl">continente<br>studiate</div>
    </div>""", unsafe_allow_html=True)
with c6:
    st.markdown("""<div class="metric-card">
    <div class="val">6</div>
    <div class="lbl">criterii AGRI-GEO<br>Framework propuse</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Zbor Aviatie (+11.439 m)",
    "Submarin Tenerife (-30 m)",
    "GPS Fantoma — Descoperire",
    "AGRI-GEO Framework (6 criterii)",
    "Implicatii GDPR + Actul AI",
    "D — Analizator Fotografie",
    "E — Dubai + Abu Dhabi Global"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ZBOR AVIATIE
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Experimentul 1: Zbor Comercial Roma FCO — Bucuresti OTP")
    st.caption("18 aprilie 2026 | Samsung Galaxy A72 (SM-A725F) | Timestamp Camera (Bian Di) | 362 fotografii")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        if PLOTLY_OK:
            track = [
                {"lat": 42.420063, "lon": 15.995659, "alt_m": 11439.2, "locatie": "Adriatica - Pescara"},
                {"lat": 42.420675, "lon": 16.023374, "alt_m": 11438.0, "locatie": "Adriatica"},
                {"lat": 42.421897, "lon": 16.081579, "alt_m": 11435.8, "locatie": "Adriatica"},
                {"lat": 42.428667, "lon": 16.399334, "alt_m": 11430.0, "locatie": "Adriatica centrala"},
                {"lat": 42.485822, "lon": 18.564560, "alt_m": 11380.0, "locatie": "Coasta Montenegro"},
                {"lat": 42.761862, "lon": 19.234452, "alt_m": 11200.0, "locatie": "Montenegro/Albania"},
                {"lat": 43.074951, "lon": 22.037836, "alt_m": 10800.0, "locatie": "Serbia/Bulgaria"},
                {"lat": 44.000000, "lon": 24.500000, "alt_m": 3500.0,  "locatie": "Coborare Bucuresti"},
                {"lat": 44.575667, "lon": 26.094084, "alt_m": 135.1,   "locatie": "Aterizare OTP"},
                {"lat": 44.575544, "lon": 26.092700, "alt_m": 133.9,   "locatie": "OTP sol"},
            ]
            df_track = pd.DataFrame(track)

            fig_map = go.Figure()
            fig_map.add_trace(go.Scattergeo(
                lat=df_track["lat"], lon=df_track["lon"],
                mode="lines+markers",
                line=dict(width=3, color="#1a2980"),
                marker=dict(
                    size=10,
                    color=df_track["alt_m"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Altitudine (m)")
                ),
                text=df_track.apply(lambda r: f"{r['locatie']}<br>{r['alt_m']:.0f} m WGS84", axis=1),
                hoverinfo="text",
                name="Traiect zbor"
            ))
            fig_map.update_layout(
                geo=dict(
                    scope="europe", showland=True, landcolor="#f0f0f0",
                    showocean=True, oceancolor="#d0e8ff",
                    showcoastlines=True, coastlinecolor="#999",
                    center=dict(lat=43.5, lon=21), projection_scale=4
                ),
                height=350, margin=dict(l=0, r=0, t=0, b=0),
                title="Traiect zbor FCO-OTP cu altitudine EXIF (18 apr 2026)"
            )
            st.plotly_chart(fig_map, use_container_width=True)

    with col_b:
        st.markdown("**Date confirmate din EXIF:**")
        st.markdown("""
| Parametru | Valoare |
|-----------|---------|
| Altitudine max | **11.439,2 m** WGS84 |
| Viteza max | **823,5 km/h** |
| Nr. fotografii | **362** cu EXIF complet |
| Aplicatie | Timestamp Camera |
| Telefon | Samsung Galaxy A72 |
| Offline GPS | **DA** — fara internet |
| GDPR | **PROBLEMATIC** |
""")
        st.markdown("""
<div class="finding-box">
<b>Concluzie cheie:</b> Timestamp Camera inregistreaza corect altitudinea de 11.439 m,
viteza si coordonatele GPS fara conexiune la internet. Este singura aplicatie testata
cu EXIF complet la altitudini extreme.
</div>
""", unsafe_allow_html=True)

    st.info("Datele din acest experiment sunt unice in literatura de specialitate — EXIF georeferentiat la 11.439 m altitudine, vol comercial, fara precedent pentru aplicatii mobile agricole.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SUBMARIN TENERIFE
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Experimentul 2: Submarin Turistic — Oceanul Atlantic, Tenerife")
    st.caption("9 august 2025 | Samsung Galaxy A72 (camera standard) | 562 fotografii JPG")

    faze = [
        {"faza": "Faza 1", "descriere": "Suprafata doc", "interval": "10:47–10:50",
         "altitudine": "43–46 m WGS84", "nr_foto": 18,   "status": "GPS VALID",
         "culoare": "#27ae60", "comentariu": "GPS functional, semnal stabil la suprafata"},
        {"faza": "Faza 2", "descriere": "Coborare (tranzitie)", "interval": "10:55–10:56",
         "altitudine": "31,7 m WGS84 = −16 m ortometric", "nr_foto": 3, "status": "GPS PARTIAL",
         "culoare": "#e67e22", "comentariu": "CEL MAI JOS GPS — semnal partial, inca inregistreaza"},
        {"faza": "Faza 3", "descriere": "Subacvatic −30 m (GPS INGHETAT)", "interval": "11:04–11:53",
         "altitudine": "48,5 m WGS84 FANTOMA", "nr_foto": 243, "status": "GPS FANTOMA",
         "culoare": "#c0392b", "comentariu": "GEOLOCALIZARE FANTOMA: 49 minute, 43% din fotografii — indistinguibil de date valide"},
        {"faza": "Faza 4", "descriere": "Recuperare GPS", "interval": "11:56–12:00",
         "altitudine": "0,0 m WGS84", "nr_foto": 16, "status": "GPS RECUPERARE",
         "culoare": "#8e44ad", "comentariu": "GPS-ul reia semnalul fara blocare altitudine — 0,0 m neexplicat"},
        {"faza": "Faza 5", "descriere": "Suprafata recuperata", "interval": "12:01+",
         "altitudine": "46–48 m WGS84", "nr_foto": 282, "status": "GPS VALID",
         "culoare": "#27ae60", "comentariu": "GPS complet functional, valori consistente cu Faza 1"},
    ]

    for f in faze:
        border = f["culoare"]
        bg = "#fff0f0" if "FANTOMA" in f["status"] else ("#f0fff4" if "VALID" in f["status"] else "#fafafa")
        st.markdown(f"""
<div class="phase-box" style="border-left-color:{border}; background:{bg};">
<b style="color:{border};">{f['faza']}: {f['descriere']}</b>
&nbsp;|&nbsp; <code>{f['interval']}</code>
&nbsp;|&nbsp; {f['nr_foto']} fotografii
&nbsp;|&nbsp; <b>{f['altitudine']}</b>
&nbsp;|&nbsp; <span style="color:{border}; font-weight:700;">{f['status']}</span><br>
<small style="color:#555;">{f['comentariu']}</small>
</div>
""", unsafe_allow_html=True)

    st.divider()
    if PLOTLY_OK:
        st.markdown("**Seria de timp GPSAltitude EXIF — toate cele 562 fotografii (simulata din date reale):**")

        np.random.seed(42)
        t_surface1  = np.linspace(0, 3, 18)
        a_surface1  = np.random.normal(44.5, 0.8, 18)
        t_descent   = np.linspace(8, 9, 3)
        a_descent   = np.array([38.0, 34.5, 31.7])
        t_phantom   = np.linspace(17, 66, 243)
        a_phantom   = np.random.normal(48.5, 0.05, 243)
        t_recovery  = np.linspace(69, 73, 16)
        a_recovery  = np.zeros(16) + np.random.normal(0, 0.1, 16)
        t_surface2  = np.linspace(74, 97, 282)
        a_surface2  = np.random.normal(47.0, 1.0, 282)

        t_all = np.concatenate([t_surface1, t_descent, t_phantom, t_recovery, t_surface2])
        a_all = np.concatenate([a_surface1, a_descent, a_phantom, a_recovery, a_surface2])

        def min_to_hhmm(m):
            from datetime import timedelta
            t0 = datetime(2025, 8, 9, 10, 47, 0)
            return (t0 + timedelta(minutes=float(m))).strftime("%H:%M")

        colors = (
            ["#27ae60"] * 18 +
            ["#e67e22"] * 3 +
            ["#c0392b"] * 243 +
            ["#8e44ad"] * 16 +
            ["#27ae60"] * 282
        )

        fig_ts = go.Figure()

        for faza_data in [
            (t_surface1,  a_surface1,  "#27ae60", "Faza 1+5: GPS valid suprafata"),
            (t_descent,   a_descent,   "#e67e22", "Faza 2: Coborare (31,7 m WGS84)"),
            (t_phantom,   a_phantom,   "#c0392b", "Faza 3: GPS FANTOMA 48,5 m (243 foto, 49 min)"),
            (t_recovery,  a_recovery,  "#8e44ad", "Faza 4: Recuperare GPS (0,0 m)"),
            (t_surface2,  a_surface2,  "#27ae60", None),
        ]:
            t_, a_, col_, name_ = faza_data
            fig_ts.add_trace(go.Scatter(
                x=t_, y=a_,
                mode="markers",
                marker=dict(size=4, color=col_, opacity=0.7),
                name=name_ if name_ else "Faza 5: GPS valid suprafata",
                showlegend=name_ is not None
            ))

        fig_ts.add_hline(y=48.5, line_dash="dash", line_color="#c0392b", line_width=1.5,
                         annotation_text="Valoare fantoma: 48,5 m WGS84 (nivel marii Tenerife)")
        fig_ts.add_hline(y=-30,  line_dash="dashdot", line_color="#1a5276", line_width=1.2,
                         annotation_text="Adancime reala estimata: -30 m")
        fig_ts.add_hline(y=0.0,  line_dash="dot", line_color="#8e44ad", line_width=1.0)

        fig_ts.add_vrect(x0=17, x1=66, fillcolor="#c0392b", opacity=0.08, line_width=0)

        fig_ts.add_annotation(x=40, y=60, text="GEOLOCALIZARE FANTOMA<br>48,5 m inghetat<br>243 foto, 49 min",
                               showarrow=True, arrowhead=2, ax=0, ay=-40,
                               font=dict(color="#c0392b", size=11, family="Arial Black"),
                               bgcolor="#fadbd8", bordercolor="#c0392b")

        x_ticks_vals = list(range(0, 101, 10))
        x_ticks_text = [min_to_hhmm(m) for m in x_ticks_vals]
        fig_ts.update_layout(
            xaxis=dict(tickvals=x_ticks_vals, ticktext=x_ticks_text,
                       title="Ora locala (Tenerife, 9 august 2025)"),
            yaxis=dict(title="GPSAltitude EXIF (m WGS84 elipsoidal)", range=[-45, 75]),
            height=420,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="#f8f9fa",
            title="Seria de timp GPSAltitude — Excursie submarin turistic, Atlantic, Tenerife"
        )
        st.plotly_chart(fig_ts, use_container_width=True)
        st.caption("Date simulate din profilul real EXIF (562 fotografii, Samsung Galaxy A72, 9 aug 2025). Valorile exacte provin din extragere Python Pillow 10.x pe datele originale.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GPS FANTOMA
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Geolocalizarea Fantoma — Descoperire Noua")

    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown("""
### Ce este geolocalizarea fantoma?

Cand Samsung Galaxy A72 pierde semnalul GPS (ex. sub apa),
camera **standard** NU inregistreaza pierderea semnalului.
In schimb, **ingheata ultimul fix GPS valid** in metadata EXIF
al tuturor fotografiilor urmatoare.

**Problema critica:** aceste date sunt **indistinguibile** de date GPS valide:
- `GPSAltitudeRef = 0x00` (deasupra marii) pe tot parcursul
- Nicio eticheta EXIF de pierdere semnal (JEITA EXIF 2.32 nu prevede una)
- Valoarea inghepata: **48,5 m WGS84** = nivelul marii la Tenerife
""")

        st.markdown("""
### De ce 48,5 m = nivelul marii?

Formula: `h_elipsoidal = H_ortometric + N_geoid`

La Tenerife (Insulele Canare):
- Ondulatie geoida N ≈ 48 m (EGM96/EGM2008)
- Nivel marii (H=0) → h_WGS84 = 0 + 48 ≈ **48 m**
- Valoarea fantoma masurabilita: **48,5 m** ✓

Aceasta este **dovada geofizica** ca Samsung a inghetat
exact valoarea din momentul pierderii semnalului GPS
la suprafata marii.
""")

    with col_y:
        st.markdown("### Cronologia evenimentului")
        timeline_data = {
            "Moment": ["10:47", "10:55", "11:04", "11:53", "11:56", "12:01"],
            "Eveniment": [
                "GPS valid la doc — 43-46 m",
                "Coborare — 31,7 m WGS84 (-16 m ortometric)",
                "GPS INGHETAT — 48,5 m FANTOMA incepe",
                "GPS INGHETAT — 48,5 m FANTOMA sfarsit",
                "Recuperare GPS — 0,0 m",
                "GPS valid la suprafata — 46-48 m"
            ],
            "Foto": [18, 3, "→", 243, 16, 282],
            "Status": ["VALID", "PARTIAL", "FANTOMA", "FANTOMA", "RECUPERARE", "VALID"]
        }
        df_tl = pd.DataFrame(timeline_data)
        st.dataframe(df_tl, hide_index=True, use_container_width=True)

        st.markdown("""
<div class="finding-box">
<b>Impact pentru sisteme AI:</b><br>
Un sistem AI care foloseste aceste date EXIF pentru geolocalizare
va plasa 243 fotografii (43% din total) la <b>nivelul marii Tenerife (48,5 m)</b>
in loc de <b>adancimea reala de -30 m</b>.
Eroarea de altitudine = <b>78,5 m</b>. Nicio avertizare in date.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
### Samsung vs. alte dispozitive

| Comportament | Samsung std | Timestamp Camera |
|---|---|---|
| Inregistrare pierdere GPS | NU | NU |
| Ingheata ultimul fix | DA | DA |
| GPSAltitudeRef sub apa | 0x00 (gresit) | N/A |
| Detectabil automat | **NU** | **NU** |
""")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — AGRI-GEO FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("AGRI-GEO Framework — 6 Criterii de Conformitate")
    st.markdown("Cadru propus pentru cerinte minime de conformitate in aplicatii de georeferentiere folosite in sisteme AI de inspectie agricola.")

    criterii = [
        {
            "cod": "AG-1", "titlu": "Georeferentiere offline",
            "descriere": "Aplicatia trebuie sa functioneze fara conexiune la internet. GPS-ul nu depinde de server extern.",
            "testare": "Activare mod avion → fotografiere → verificare EXIF lat/lon",
            "rezultat_aviatie": "Timestamp Camera: DA | Location on Photo: DA | GPS Camera: NU",
            "nou": False
        },
        {
            "cod": "AG-2", "titlu": "Altitudine in EXIF",
            "descriere": "Altitudinea (GPSAltitude) trebuie inregistrata in metadate EXIF, nu doar ca overlay text.",
            "testare": "Extragere Python Pillow: exif[34853][6] != None",
            "rezultat_aviatie": "Timestamp Camera: DA (11.439 m) | Location on Photo: NU (overlay) | GPS Camera: NU",
            "nou": False
        },
        {
            "cod": "AG-3", "titlu": "Timestamp sincronizat",
            "descriere": "Ora fotografiei trebuie sincronizata cu GPS (nu ceasul telefonului). Toleranta: ±2 secunde.",
            "testare": "Comparare DateTimeOriginal cu GPSDateStamp/GPSTimeStamp",
            "rezultat_aviatie": "Timestamp Camera: DA | Location on Photo: Partial | GPS Camera: N/A",
            "nou": False
        },
        {
            "cod": "AG-4", "titlu": "Politica GDPR transparenta",
            "descriere": "Aplicatia trebuie sa aiba politica de confidentialitate accesibila, fara transmitere date catre terti fara consimtamant.",
            "testare": "Verificare politica + analiza trafic retea",
            "rezultat_aviatie": "Timestamp Camera: PROBLEMATIC | Location on Photo: De verificat | GPS Camera: Necunoscut",
            "nou": False
        },
        {
            "cod": "AG-5", "titlu": "Acuratete pozitionala",
            "descriere": "Eroarea GPS trebuie < 3 m in conditii normale. Outlieri detectabili si raportabili.",
            "testare": "Comparare cu coordonate de referinta cunoscute (puncte GNSS permanente)",
            "rezultat_aviatie": "Location on Photo: 3 outlieri la 17,5°E (imposibil pe ruta reala)",
            "nou": False
        },
        {
            "cod": "AG-6", "titlu": "Divulgare pierdere semnal GNSS",
            "descriere": "CRITERIU NOU: Aplicatia trebuie sa marcheze explicit fotografiile realizate fara semnal GPS valid. Inghetarea silentioasa a ultimului fix este o violare GDPR (Art. 5(1)(d)) si un risc Art. 10 Actul AI.",
            "testare": "Verificare tag EXIF dedicat sau flag metadata la pierdere semnal",
            "rezultat_aviatie": "NICIO aplicatie testata nu implementeaza AG-6. Standard JEITA EXIF 2.32 nu prevede tag dedicat.",
            "nou": True
        },
    ]

    for c in criterii:
        extra_style = "agri-row new" if c["nou"] else "agri-row"
        nou_badge = '<span style="background:#c0392b;color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700;margin-left:8px;">NOU din cercetarea GNSS Extrem</span>' if c["nou"] else ""
        st.markdown(f"""
<div class="{extra_style}">
<b style="font-size:1.1rem;">{c['cod']} — {c['titlu']}</b>{nou_badge}<br>
<small>{c['descriere']}</small><br>
<small><b>Testare:</b> {c['testare']}</small><br>
<small><b>Rezultat:</b> {c['rezultat_aviatie']}</small>
</div>
""", unsafe_allow_html=True)

    st.divider()

    if PLOTLY_OK:
        st.markdown("**Evaluare comparativa aplicatii (criterii AGRI-GEO):**")
        apps = ["Timestamp Camera", "Location on Photo", "GPS Camera", "GeoFoto APIA"]
        scoruri = {
            "AG-1 Offline":     [5, 5, 1, 1],
            "AG-2 Altitudine":  [5, 1, 1, 1],
            "AG-3 Timestamp":   [5, 3, 1, 2],
            "AG-4 GDPR":        [1, 3, 2, 5],
            "AG-5 Acuratete":   [5, 3, 2, 4],
            "AG-6 Divulgare":   [1, 1, 1, 1],
        }

        fig_radar = go.Figure()
        culori_app = ["#1a5276", "#117a65", "#b7950b", "#6c3483"]
        for i, app in enumerate(apps):
            vals = [scoruri[k][i] for k in scoruri.keys()]
            vals_closed = vals + [vals[0]]
            cats = list(scoruri.keys()) + [list(scoruri.keys())[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_closed, theta=cats, fill="toself",
                name=app, line_color=culori_app[i], opacity=0.7
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True, height=450,
            title="Radar AGRI-GEO 6 criterii (1=slab, 5=excelent)"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("AG-6 (Divulgare pierdere GNSS): scor 1 pentru toate aplicatiile — nicio aplicatie testata nu implementeaza aceasta cerinta.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — IMPLICATII GDPR + ACTUL AI
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Implicatii Reglementare — GDPR + Regulamentul UE 2024/1689")

    col_g, col_ai = st.columns(2)

    with col_g:
        st.markdown("""
### GDPR — Regulamentul UE 2016/679

**Art. 5(1)(d) — Principiul acuratesei:**
> *"Datele cu caracter personal trebuie sa fie exacte si, in cazul in care este necesar, sa fie actualizate"*

**Incalcare detectata:**
- 243 fotografii contin coordonate GPS **inexacte** (48,5 m in loc de -30 m)
- Utilizatorul nu este informat ca GPS-ul a pierdut semnalul
- Datele inexacte sunt procesate **silentios** ca date valide

**Art. 17 — Dreptul la stergere:**
- Timestamp Camera nu permite stergerea datelor trimise catre terti
- Identificatori dispozitiv transmisi fara consimtamant explicit

**Concluzie GDPR:**
Geolocalizarea fantoma constituie o **violare silentioasa** a Art. 5(1)(d):
date personale inexacte sunt procesate fara notificarea utilizatorului.
""")

    with col_ai:
        st.markdown("""
### Actul AI — Regulamentul UE 2024/1689

**Art. 10(2)(b) — Cerinte privind datele:**
> *"Seturile de date trebuie sa fie lipsite de erori si complete"*

**Sistem AI de inalta risc — inspectie agricola APIA:**
- Sistemele IACS/LPIS = AI de inalta risc (Anexa III, pct. 8)
- Datele de antrenament/validare trebuie sa fie lipsite de erori
- GPS fantoma = **eroare sistematica nedetectata** in date

**Art. 13 — Transparenta:**
- Utilizatorul/inspectorul trebuie informat despre limitarile sistemului
- Pierderea GPS nu este notificata = incalcare transparenta

**Art. 14 — Supraveghere umana:**
- Inspectorul APIA nu poate detecta manual GPS fantoma
- Necesita mecanisme tehnice de detectie (AG-6)

**Cerinta noua propusa (AG-6):**
Tag EXIF explicit sau flag metadata la pierdere semnal GPS.
""")

    st.divider()
    st.markdown("### Sinteza — Riscuri si Recomandari")

    riscuri = pd.DataFrame({
        "Scenariu": [
            "Fotografie subacvatica cu GPS fantoma",
            "Fotografie in tunel/subsol cu GPS inghetat",
            "Fotografie in zona fara semnal (padure densa)",
            "Fotografie la altitudine extreme (aviatie)"
        ],
        "Risc AI": ["CRITIC", "RIDICAT", "RIDICAT", "SCAZUT"],
        "Risc GDPR": ["RIDICAT", "MEDIU", "MEDIU", "SCAZUT"],
        "Detectabil automat": ["NU", "NU", "NU", "DA (altitudine > 500m)"],
        "Solutie AG-6": [
            "Tag EXIF GPS_SIGNAL_LOST",
            "Tag EXIF GPS_SIGNAL_LOST",
            "Threshold DOP / SNR",
            "Validare altitudine vs altimetru baric"
        ]
    })
    st.dataframe(riscuri, hide_index=True, use_container_width=True)

    st.divider()

    st.markdown("""
<div class="doi-box">
<b>Referinta stiintifica:</b><br>
Gamulescu, O.M. (2026). <i>GNSS Behaviour Under Extreme Altitude Conditions:
From +11,439 m (Commercial Aviation) to -30 m (Tourist Submarine, Atlantic Ocean) —
Implications for AI System Data Integrity under GDPR and EU AI Act (Regulation 2024/1689).</i><br>
<b>Zenodo Preprint.</b> DOI: <a href="https://doi.org/10.5281/zenodo.19829462" target="_blank">10.5281/zenodo.19829462</a><br>
Target: MDPI Sensors (IF 3.4, Q1) | MDPI Drones (IF 4.8, Q1)
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style='background:linear-gradient(135deg,#1a2980 0%,#26d0ce 100%);
     border-radius:12px; padding:18px 24px; color:white; margin-top:16px;'>
<div style='font-size:13px; font-weight:900; letter-spacing:1px; margin-bottom:8px;'>
    &copy; 2026 — PROPRIETATE INTELECTUALA PROTEJATA
</div>
<div style='font-size:12px; line-height:1.8;'>
    <b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
    <b>Afiliere:</b> Facultatea de Inginerie, Universitatea Constantin Brancusi Targu Jiu &nbsp;|&nbsp; APIA CJ Gorj<br>
    <b>Publicatie:</b> Zenodo Preprint 2026 &nbsp;|&nbsp;
    DOI: <code style='background:rgba(255,255,255,0.2); padding:2px 6px; border-radius:4px;'>10.5281/zenodo.19829462</code><br>
    <b>Target jurnal:</b> MDPI Sensors (IF 3.4, Q1) &nbsp;|&nbsp; MDPI Drones (IF 4.8, Q1)<br>
    <b>Date empirice:</b> Zbor Roma (FCO) &rarr; Bucuresti (OTP), 18 aprilie 2026 &nbsp;|&nbsp; Submarin turistic, Atlantic, 6 august 2025<br>
    <b>Cadru legal:</b> RGPD Art. 5(1)(d) &nbsp;|&nbsp; Regulamentul (UE) 2024/1689 Art. 10(2)(b)
</div>
<div style='font-size:10px; margin-top:10px; opacity:0.8;'>
    Orice utilizare a datelor, metodologiei sau rezultatelor prezentate necesita citarea sursei.
    Reproducerea fara acordul autorului constituie incalcarea drepturilor de autor conform Legii nr. 8/1996.
</div>
</div>
""", unsafe_allow_html=True)

    st.caption(
        "Pagina 10c — SecureGeo Global Framework | "
        "Bloc 5 AI Aplicat | UCB Targu Jiu | "
        f"Actualizat: {date.today().strftime('%d.%m.%Y')} | "
        "Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | "
        "DOI: 10.5281/zenodo.19829462"
    )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — PUNCT D: ANALIZATOR FOTOGRAFIE GEOREFERENTIATA
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("Punct D — Analizator Fotografie Georeferentiata")
    st.caption(
        "Incarca orice fotografie georeferentiata: analiza EXIF completa, "
        "detectie phantom geolocation, conformitate GDPR + Actul AI, evaluare AGRI-GEO AG-1...AG-6"
    )

    if not PIL_OK:
        st.error("Libraria Pillow nu este disponibila. Instalare: pip install Pillow>=10.0.0")
    else:
        up_file = st.file_uploader(
            "Incarca fotografie georeferentiata (JPG / JPEG / PNG)",
            type=["jpg", "jpeg", "png"],
            help="Fotografii realizate cu: Timestamp Camera, GPS Camera, Note Cam, GeoFoto, Angle Cam, camera standard."
        )

        if up_file is None:
            st.info("Incarca o fotografie pentru analiza completa EXIF.")
            st.markdown("""
**Ce detecteaza analizatorul:**
- Coordonate GPS (lat, lon, altitudine WGS84) din EXIF
- **Phantom geolocation** — geolocalizare fantoma (risc AG-6)
- Conformitate **GDPR Art. 5(1)(d)** — exactitate date de localizare
- Conformitate **Actul AI Art. 10(2)(b)** — calitate date pentru sisteme AI
- Evaluare **AGRI-GEO** (AG-1...AG-6)
- Comparare coordonate **vizibile pe fotografie** vs. **EXIF invizibil**

**Cum functioneaza detectia phantom:**
1. Extrage altitudinea WGS84 din EXIF
2. Compara cu nivelul marii estimat la acea locatie (geoid EGM96 aproximat)
3. Verifica consistenta timestamp imagine vs. GPS timestamp
4. Calculeaza scor de risc (0-100)
""")
        else:
            try:
                img_bytes = up_file.read()
                pil_img = PILImage.open(io.BytesIO(img_bytes))

                # ── EXTRACTIE EXIF ─────────────────────────────────────────────
                exif_raw = pil_img.getexif()
                all_exif = {}
                for tag_id, val in exif_raw.items():
                    tag_name = TAGS.get(tag_id, str(tag_id))
                    all_exif[tag_name] = val

                gps_block = exif_raw.get_ifd(0x8825)
                gps_data = {}
                if gps_block:
                    for k, v in gps_block.items():
                        gps_data[GPSTAGS.get(k, k)] = v

                lat_dd = lon_dd = alt_m = None
                gps_ts_str = "—"
                gps_date_str = str(gps_data.get("GPSDateStamp", "—"))
                img_dt_str = str(all_exif.get("DateTimeOriginal", all_exif.get("DateTime", "—")))
                alt_ref_val = gps_data.get("GPSAltitudeRef", None)

                if gps_data.get("GPSLatitude") and gps_data.get("GPSLatitudeRef"):
                    lat_dd = _dms_dd(gps_data["GPSLatitude"], gps_data["GPSLatitudeRef"])
                if gps_data.get("GPSLongitude") and gps_data.get("GPSLongitudeRef"):
                    lon_dd = _dms_dd(gps_data["GPSLongitude"], gps_data["GPSLongitudeRef"])
                if gps_data.get("GPSAltitude") is not None:
                    alt_m = _alt_m(gps_data)

                if gps_data.get("GPSTimeStamp"):
                    ts = gps_data["GPSTimeStamp"]
                    try:
                        h = int(_safe_f(ts[0]) or 0)
                        mn = int(_safe_f(ts[1]) or 0)
                        sc = _safe_f(ts[2]) or 0.0
                        gps_ts_str = f"{h:02d}:{mn:02d}:{sc:05.2f} UTC"
                    except:
                        gps_ts_str = str(ts)

                has_gps = (lat_dd is not None and lon_dd is not None)

                # ── ROW 1: IMAGINE + DATE GPS ────────────────────────────────
                col_img, col_gps = st.columns([1, 1])
                with col_img:
                    st.markdown("**Fotografie incarcata:**")
                    st.image(img_bytes, use_column_width=True)
                    st.caption(f"{pil_img.width} x {pil_img.height} px | {up_file.name}")

                with col_gps:
                    st.markdown("**Date GPS din EXIF (invizibile omului):**")
                    if has_gps:
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Latitudine", f"{lat_dd:.5f}°")
                        m2.metric("Longitudine", f"{lon_dd:.5f}°")
                        if alt_m is not None:
                            m3.metric("Altitudine", f"{alt_m:.1f} m")
                        else:
                            m3.metric("Altitudine", "ABSENT")

                        alt_ref_label = "0x00 (deasupra marii)"
                        if alt_ref_val == b'\x01' or alt_ref_val == 1:
                            alt_ref_label = "0x01 (sub nivelul marii)"

                        st.markdown(f"""
| Camp EXIF | Valoare |
|-----------|---------|
| GPSLatitude | `{lat_dd:.7f}°` |
| GPSLongitude | `{lon_dd:.7f}°` |
| GPSAltitude | `{f"{alt_m:.2f} m WGS84" if alt_m is not None else "ABSENT"}` |
| GPSAltitudeRef | `{alt_ref_label}` |
| GPSTimeStamp | `{gps_ts_str}` |
| GPSDateStamp | `{gps_date_str}` |
| DateTimeOriginal | `{img_dt_str}` |
""")
                    else:
                        st.error("GPS absent din EXIF — fotografia nu contine coordonate GPS")
                        st.markdown("**Implicatii:** AG-2: NU | GDPR: N/A | AG-6: N/A")

                # ── HARTA GPS ─────────────────────────────────────────────────
                if has_gps and PLOTLY_OK:
                    st.divider()
                    st.markdown("**Harta — locatia GPS din EXIF:**")
                    fig_map = go.Figure()
                    fig_map.add_trace(go.Scattergeo(
                        lat=[lat_dd], lon=[lon_dd],
                        mode="markers",
                        marker=dict(size=18, color="#c0392b",
                                    line=dict(width=2, color="white")),
                        text=[f"EXIF GPS<br>{lat_dd:.6f}°N<br>{lon_dd:.6f}°E<br>Alt: {alt_m}m"],
                        hoverinfo="text", name="Locatie EXIF"
                    ))
                    fig_map.update_layout(
                        geo=dict(
                            showland=True, landcolor="#f5f5f0",
                            showocean=True, oceancolor="#d0e8ff",
                            showcoastlines=True, coastlinecolor="#aaa",
                            center=dict(lat=lat_dd, lon=lon_dd),
                            projection_scale=10
                        ),
                        height=280, margin=dict(l=0, r=0, t=0, b=0),
                        title=f"Coordonate GPS EXIF: {lat_dd:.4f}°N, {lon_dd:.4f}°E"
                    )
                    st.plotly_chart(fig_map, use_container_width=True)

                # ── TABEL EXIF COMPLET ─────────────────────────────────────────
                st.divider()
                with st.expander("Tabel EXIF complet (toate tagurile detectate)", expanded=False):
                    exif_rows = []
                    for k, v in sorted(all_exif.items()):
                        if k in ("MakerNote", "UserComment"):
                            continue
                        try:
                            vs = str(v)[:250]
                        except:
                            vs = "—"
                        exif_rows.append({"Tag EXIF": k, "Valoare": vs})
                    for k, v in sorted(gps_data.items()):
                        try:
                            vs = str(v)[:250]
                        except:
                            vs = "—"
                        exif_rows.append({"Tag EXIF": f"GPS.{k}", "Valoare": vs})
                    if exif_rows:
                        st.dataframe(pd.DataFrame(exif_rows),
                                     hide_index=True, use_container_width=True)
                    else:
                        st.warning("Nu au fost detectate taguri EXIF in aceasta fotografie.")

                # ── DETECTIE PHANTOM GEOLOCATION ──────────────────────────────
                st.divider()
                st.markdown("### Detectie Phantom Geolocation (AG-6)")
                st.caption("Analiza bazata pe altitudine WGS84, consistenta timestamp si precizie GPS.")

                phantom_risks = []
                phantom_score = 0

                if not has_gps:
                    phantom_risks.append(("INFO", "Fara date GPS — phantom geolocation nu se aplica"))
                else:
                    if alt_m is None:
                        phantom_risks.append(("ATENTIE",
                            "Altitudinea lipseste din EXIF — nu se poate verifica phantom (AG-2: NU)"))
                        phantom_score += 20
                    elif alt_m == 0.0:
                        phantom_risks.append(("RIDICAT",
                            "Altitudine = 0,0 m exacta — posibil Faza 4 (recuperare GPS dupa pierdere semnal, "
                            "documentata in cercetarea SecureGeo)"))
                        phantom_score += 65
                    elif 25.0 <= alt_m <= 70.0:
                        N_est = _approx_geoid(lat_dd, lon_dd)
                        diff = abs(alt_m - N_est)
                        if diff < 12:
                            phantom_risks.append(("ATENTIE",
                                f"Altitudine {alt_m}m WGS84 ≈ nivel marii estimat la aceasta locatie "
                                f"(~{N_est:.0f}m geoid EGM96 aproximat, eroare ±15m). "
                                "Daca fotografia a fost realizata in mediu subacvatic sau in zona fara semnal GPS, "
                                "poate fi phantom geolocation (similar Faza 3 — experiment Tenerife)."))
                            phantom_score += 40
                        else:
                            phantom_risks.append(("OK",
                                f"Altitudine {alt_m}m WGS84. Geoid estimat: {N_est:.0f}m. "
                                "Diferenta: {diff:.0f}m — nu corespunde tiparului phantom.".format(diff=diff)))
                    elif alt_m > 5000:
                        phantom_risks.append(("ATENTIE",
                            f"Altitudine {alt_m:.0f}m — domeniu aviatie. "
                            "Daca fotografia nu a fost realizata in avion, poate fi phantom geolocation."))
                        phantom_score += 35
                    elif alt_m < -5:
                        phantom_risks.append(("INFO",
                            f"Altitudine negativa {alt_m:.1f}m WGS84 (GPSAltitudeRef=0x01). "
                            "Posibila fotografie subacvatica cu semnal GPS partial."))
                        phantom_score += 20
                    else:
                        phantom_risks.append(("OK",
                            f"Altitudine {alt_m:.1f}m WGS84 — in domeniu normal terestru"))

                    # Verificare timestamp
                    if img_dt_str != "—" and gps_date_str != "—" and gps_ts_str != "—":
                        try:
                            img_dt = datetime.strptime(img_dt_str[:19], "%Y:%m:%d %H:%M:%S")
                            gps_full = f"{gps_date_str} {gps_ts_str[:8]}"
                            gps_dt = datetime.strptime(gps_full, "%Y:%m:%d %H:%M:%S")
                            diff_s = abs((img_dt - gps_dt).total_seconds())
                            if diff_s > 120:
                                phantom_risks.append(("ATENTIE",
                                    f"Diferenta timestamp imagine vs GPS: {diff_s:.0f} secunde "
                                    "(normal < 30s). Posibila inconsistenta sau fus orar incorect."))
                                phantom_score += 25
                            elif diff_s > 30:
                                phantom_risks.append(("INFO",
                                    f"Diferenta timestamp: {diff_s:.0f}s "
                                    "(acceptabil dar verifica fusul orar)"))
                            else:
                                phantom_risks.append(("OK",
                                    f"Timestamp imagine vs GPS: diferenta {diff_s:.0f}s — consistent"))
                        except:
                            phantom_risks.append(("INFO",
                                "Timestamp-urile nu au putut fi comparate (format neasteptat)"))

                    # Verificare precizie GPS
                    if lat_dd is not None:
                        lat_str = f"{abs(lat_dd):.10f}".rstrip('0')
                        decimals = len(lat_str.split('.')[-1]) if '.' in lat_str else 0
                        if decimals < 3:
                            phantom_risks.append(("ATENTIE",
                                f"Precizie GPS scazuta: {decimals} zecimale semnificative "
                                "(normal 6-7). Posibil coordonate cache sau interpolare."))
                            phantom_score += 15
                        else:
                            phantom_risks.append(("OK",
                                f"Precizie GPS: {decimals} zecimale semnificative — normal"))

                # Scor -> nivel
                if phantom_score >= 60:
                    risk_label, risk_color, risk_bg = "CRITIC", "#c0392b", "#fadbd8"
                elif phantom_score >= 40:
                    risk_label, risk_color, risk_bg = "RIDICAT", "#e67e22", "#fdebd0"
                elif phantom_score >= 15:
                    risk_label, risk_color, risk_bg = "MEDIU", "#f39c12", "#fef9e7"
                else:
                    risk_label, risk_color, risk_bg = "SCAZUT", "#27ae60", "#eafaf1"

                col_r, col_ind = st.columns([1, 2])
                with col_r:
                    st.markdown(f"""
<div style="background:{risk_bg};border:2px solid {risk_color};border-radius:12px;
     padding:20px;text-align:center;">
<div style="font-size:2.4rem;font-weight:900;color:{risk_color};">{risk_label}</div>
<div style="font-size:0.85rem;color:#555;margin-top:6px;">
Risc Phantom Geolocation<br>Scor intern: {phantom_score}/100
</div>
</div>
""", unsafe_allow_html=True)
                    st.markdown("""
**Legende scoruri:**
- **SCAZUT (0-14)**: Date GPS consistente
- **MEDIU (15-39)**: Un indicator suspect
- **RIDICAT (40-59)**: Indicatori multipli
- **CRITIC (60+)**: Phantom confirmat sau probabil
""")

                with col_ind:
                    st.markdown("**Indicatori detectati:**")
                    icon_map = {
                        "OK": ("#27ae60", "#eafaf1", "OK"),
                        "ATENTIE": ("#e67e22", "#fef9e7", "ATENTIE"),
                        "RIDICAT": ("#c0392b", "#fadbd8", "RIDICAT"),
                        "INFO": ("#6c757d", "#f8f9fa", "INFO"),
                    }
                    for status, msg in phantom_risks:
                        c_, bg_, lbl_ = icon_map.get(status, ("#6c757d", "#f8f9fa", status))
                        st.markdown(
                            f"<div style='background:{bg_};border-left:4px solid {c_};"
                            f"padding:8px 12px;margin:4px 0;border-radius:4px;'>"
                            f"<b style='color:{c_};'>{lbl_}</b> — {msg}</div>",
                            unsafe_allow_html=True
                        )

                # ── COMPARARE COORDONATE VIZIBILE vs EXIF ─────────────────────
                st.divider()
                st.markdown("### Comparare Coordonate Vizibile pe Fotografie vs. EXIF Invizibil")
                st.caption(
                    "Multe aplicatii (Timestamp Camera, Note Cam, Location on Photo) suprapun "
                    "coordonatele GPS ca TEXT pe imagine. Introdu valorile pe care le citesti "
                    "vizual pentru comparatie cu EXIF-ul invizibil."
                )

                col_photo2, col_cmp = st.columns([1, 1])
                with col_photo2:
                    st.markdown("**Fotografia ta (zoom pentru text suprapus):**")
                    st.image(img_bytes, use_column_width=True)

                with col_cmp:
                    st.markdown("**Coordonatele vizibile pe fotografie:**")
                    vis_lat = st.text_input(
                        "Latitudine citita vizual (ex: 44.575667)", key="vl_d")
                    vis_lon = st.text_input(
                        "Longitudine citita vizual (ex: 26.094084)", key="vln_d")
                    vis_alt = st.text_input(
                        "Altitudine citita vizual (ex: 135.1)", key="va_d")

                    if vis_lat and vis_lon:
                        try:
                            vl = float(vis_lat)
                            vln = float(vis_lon)
                            va = float(vis_alt) if vis_alt else None

                            rows_c = []
                            if lat_dd is not None:
                                d_lat = abs(vl - lat_dd)
                                rows_c.append({
                                    "Camp": "Latitudine",
                                    "EXIF (invizibil)": f"{lat_dd:.6f}°",
                                    "Vizibil pe foto": f"{vl:.6f}°",
                                    "Delta": f"{d_lat * 111320:.1f} m",
                                    "Status": "OK" if d_lat < 0.0002 else "DIFERENTA!"
                                })
                            if lon_dd is not None:
                                d_lon = abs(vln - lon_dd)
                                cos_lat = math.cos(math.radians(lat_dd or 0))
                                rows_c.append({
                                    "Camp": "Longitudine",
                                    "EXIF (invizibil)": f"{lon_dd:.6f}°",
                                    "Vizibil pe foto": f"{vln:.6f}°",
                                    "Delta": f"{d_lon * 111320 * cos_lat:.1f} m",
                                    "Status": "OK" if d_lon < 0.0002 else "DIFERENTA!"
                                })
                            if va is not None and alt_m is not None:
                                d_alt = abs(va - alt_m)
                                rows_c.append({
                                    "Camp": "Altitudine",
                                    "EXIF (invizibil)": f"{alt_m:.1f} m",
                                    "Vizibil pe foto": f"{va:.1f} m",
                                    "Delta": f"{d_alt:.1f} m",
                                    "Status": "OK" if d_alt < 10 else "DIFERENTA!"
                                })

                            if rows_c:
                                df_cmp = pd.DataFrame(rows_c)
                                st.dataframe(df_cmp, hide_index=True,
                                             use_container_width=True)
                                if all(r["Status"] == "OK" for r in rows_c):
                                    st.success(
                                        "Coordonatele vizibile si EXIF sunt consistente. "
                                        "NOTA: Consistenta nu exclude phantom geolocation daca "
                                        "AMBELE surse sunt afectate simultan (pattern Faza 3).")
                                else:
                                    st.error(
                                        "DIFERENTA intre coordonatele vizibile si EXIF! "
                                        "Posibila eroare de scriere EXIF sau manipulare metadata.")
                        except ValueError:
                            st.warning("Introdu valori numerice valide.")

                # ── EVALUARE AGRI-GEO ────────────────────────────────────────
                st.divider()
                st.markdown("### Evaluare AGRI-GEO Framework (AG-1...AG-6)")
                ag_results = _eval_agri_geo_d(has_gps, lat_dd, lon_dd, alt_m,
                                               all_exif, phantom_score)
                cols_ag = st.columns(3)
                for idx, (ag_cod, ag_titlu, ag_status, ag_det, ag_col) in enumerate(ag_results):
                    bg_ag = ("#eafaf1" if ag_status == "DA" else
                             "#fef9e7" if ag_status == "PARTIAL" else
                             "#fadbd8" if ag_status == "NU" else "#f8f9fa")
                    with cols_ag[idx % 3]:
                        st.markdown(f"""
<div style="background:{bg_ag};border:2px solid {ag_col};border-radius:10px;
     padding:12px;margin-bottom:10px;">
<div style="font-size:1rem;font-weight:900;color:{ag_col};">{ag_cod}</div>
<div style="font-size:0.8rem;font-weight:700;">{ag_titlu}</div>
<div style="font-size:1.2rem;font-weight:900;color:{ag_col};margin:4px 0;">
{ag_status}</div>
<div style="font-size:0.72rem;color:#555;">{ag_det}</div>
</div>
""", unsafe_allow_html=True)

                # ── GDPR + ACTUL AI ──────────────────────────────────────────
                st.divider()
                col_gdpr, col_ai = st.columns(2)
                with col_gdpr:
                    st.markdown("### GDPR — Art. 5(1)(d)")
                    if not has_gps:
                        st.info("Fara GPS — Art. 5(1)(d) nu se aplica.")
                    elif phantom_score >= 40:
                        st.error(
                            "**Risc de incalcare Art. 5(1)(d)**\n\n"
                            "Datele GPS prezinta indicatori de inexactitate (phantom geolocation). "
                            "Operatorul are obligatia de a verifica si rectifica datele inainte de "
                            "utilizare in procese administrative sau juridice.")
                    elif phantom_score >= 15:
                        st.warning(
                            "**Risc mediu Art. 5(1)(d)**\n\n"
                            "Indicatori moderati de inexactitate. Se recomanda validare independenta.")
                    else:
                        st.success(
                            "**Fara indicatori de incalcare Art. 5(1)(d)**\n\n"
                            "Date GPS aparent exacte. Se recomanda validare independenta pentru "
                            "procese cu relevanta juridica.")

                with col_ai:
                    st.markdown("### Actul AI — Art. 10(2)(b)")
                    if alt_m is None and has_gps:
                        st.warning(
                            "**Date incomplete — Art. 10(2)(b)**\n\n"
                            "Altitudinea lipseste din EXIF. Date GPS incomplete pot "
                            "afecta calitatea seturilor de date pentru sisteme AI de risc ridicat "
                            "(Anexa III pct. 5(a), obligatoriu aug. 2026).")
                    elif phantom_score >= 40:
                        st.error(
                            "**Risc la calitatea datelor — Art. 10(2)(b)**\n\n"
                            "Indicatori phantom geolocation detectati. Aceste date introduse "
                            "in sisteme AI pot genera clasificari eronate — cerinta 'fara erori' "
                            "nu este satisfacuta.")
                    elif not has_gps:
                        st.warning(
                            "**GPS absent — Art. 10(2)(b)**\n\n"
                            "Fara coordonate GPS, datele sunt incomplete pentru sisteme AI "
                            "de inspectie teren.")
                    else:
                        st.success(
                            "**Date consistente — Art. 10(2)(b)**\n\n"
                            "GPS complet si consistent. Date aparent utilizabile in "
                            "sisteme AI de inspectie teren.")

                # ── RAPORT COMPLET ───────────────────────────────────────────
                st.divider()
                st.markdown("### Raport Complet de Analiza")

                report_lines = [
                    "=" * 60,
                    "RAPORT ANALIZA EXIF — SecureGeo AGRI-GEO Framework",
                    "Cadru: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu",
                    "DOI cercetare: 10.5281/zenodo.19829462",
                    f"Data analiza: {date.today().strftime('%d.%m.%Y')}",
                    "=" * 60,
                    f"Fisier: {up_file.name}",
                    f"Dimensiune: {pil_img.width}x{pil_img.height} px",
                    "-" * 40,
                    "DATE GPS EXIF:",
                    f"  Latitudine:       {f'{lat_dd:.7f} deg' if lat_dd else 'ABSENT'}",
                    f"  Longitudine:      {f'{lon_dd:.7f} deg' if lon_dd else 'ABSENT'}",
                    f"  Altitudine WGS84: {f'{alt_m:.2f} m' if alt_m is not None else 'ABSENT'}",
                    f"  GPS Timestamp:    {gps_ts_str}",
                    f"  GPS DateStamp:    {gps_date_str}",
                    f"  DateTimeOriginal: {img_dt_str}",
                    "-" * 40,
                    f"RISC PHANTOM GEOLOCATION: {risk_label} (scor: {phantom_score}/100)",
                    "Indicatori:",
                ]
                for status, msg in phantom_risks:
                    report_lines.append(f"  [{status}] {msg}")
                report_lines.extend([
                    "-" * 40,
                    "EVALUARE AGRI-GEO:",
                ])
                for ag_cod, ag_titlu, ag_status, ag_det, _ in ag_results:
                    report_lines.append(f"  {ag_cod} - {ag_titlu}: {ag_status}")
                    report_lines.append(f"    {ag_det}")
                report_lines.extend([
                    "-" * 40,
                    "CONFORMITATE NORMATIVA:",
                    f"  GDPR Art. 5(1)(d): {'RISC' if phantom_score >= 40 else 'OK'}",
                    f"  Actul AI Art. 10(2)(b): {'RISC' if (phantom_score >= 40 or (has_gps and alt_m is None)) else 'OK'}",
                    "=" * 60,
                    "NOTA: Raport generat automat din metadata EXIF.",
                    "Concluziile definitive necesita validare umana.",
                    "Referinta: Gamulescu O.M. (2026), doi:10.5281/zenodo.19829462",
                    "=" * 60,
                ])

                report_text = "\n".join(report_lines)
                with st.expander("Vizualizeaza raportul complet", expanded=True):
                    st.code(report_text, language="")

                st.download_button(
                    label="Descarca Raport TXT",
                    data=report_text.encode("utf-8"),
                    file_name=f"raport_exif_{up_file.name.replace('.', '_')}.txt",
                    mime="text/plain"
                )

            except Exception as exc:
                st.error(f"Eroare la procesarea fotografiei: {exc}")
                st.info("Asigura-te ca fisierul este o fotografie JPG/JPEG/PNG valida cu date EXIF.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7 — DUBAI + ABU DHABI GLOBAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.subheader("Studiu Tri-Continental — Dubai + Abu Dhabi, Decembrie 2025")
    st.caption("Samsung Galaxy A72 (SM-A725F) | 482 fotografii JPG analizate | Golf Persic, EAU")

    st.markdown("""
<div class="finding-box">
<b>Descoperire noua (3 mai 2026):</b> Fenomenul GPS Fantoma a fost confirmat si in Golful Persic (Abu Dhabi,
Dubai) — demonstrand ca fenomenul este <b>global, nu local</b>. Geoidul EGM96 are valori <b>negative</b>
in zona Golfului Persic (N ≈ −27 m la Abu Dhabi, N ≈ −33 m la Dubai), in contrast cu
valoarea <b>pozitiva</b> de la Tenerife (N ≈ +48 m). Diferenta maxima confirmata empiric: <b>70 m</b>
intre cele doua zone — acelasi nivel al marii, valori WGS84 radical diferite.
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ─── METRICI TAB 7 ───────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""<div class="metric-card">
        <div class="val">482</div>
        <div class="lbl">JPG analizate<br>Dubai + Abu Dhabi</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="metric-card">
        <div class="val" style="color:#c0392b;">8</div>
        <div class="lbl">secvente GPS Fantoma<br>Abu Dhabi (max 24 foto)</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="metric-card">
        <div class="val">433,9 m</div>
        <div class="lbl">altitudine max WGS84<br>Burj Khalifa etaj 124</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown("""<div class="metric-card">
        <div class="val" style="color:#e67e22;">−67,7 m</div>
        <div class="lbl">altitudine min WGS84<br>subsol Dubai Mall</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ─── SECTIUNI ────────────────────────────────────────────────────────────────
    sec1, sec2, sec3 = st.tabs([
        "Abu Dhabi — GPS Fantoma confirmat",
        "Burj Khalifa — Profil Altitudine",
        "Comparatie Geoid Tri-Continental"
    ])

    # ── ABU DHABI ────────────────────────────────────────────────────────────────
    with sec1:
        st.markdown("### Abu Dhabi, EAU — 10 decembrie 2025")
        st.markdown("""
**264 fotografii JPG analizate** cu Camera Standard Samsung Galaxy A72 in zona Abu Dhabi
(lat medie 24.412°N, lon medie 54.475°E). Altitudine medie: **−22,0 m WGS84** — confirmand
direct modelul EGM96: la Abu Dhabi, **nivelul marii corespunde cu −22 m WGS84** (N_geoid ≈ −27 m).
        """)

        if PLOTLY_OK:
            # Secventele GPS Fantoma Abu Dhabi
            seq_data = {
                "Secventa": ["Seq 1", "Seq 2", "Seq 3", "Seq 4", "Seq 5", "Seq 6-8"],
                "Nr. foto": [7, 14, 5, 24, 3, "~30 total"],
                "Alt. WGS84 (m)": [-20.8, -9.33, -11.56, -11.51, -28.73, "var."],
                "GPS Timestamp": ["07:16:21 UTC (inghetat)", "07:21:02 UTC (inghetat)",
                                   "07:21:56 UTC (inghetat)", "07:23:58 UTC (inghetat)",
                                   "07:29:58 UTC (inghetat)", "diverse (inghetate)"],
                "Status": ["FANTOMA", "FANTOMA", "FANTOMA", "FANTOMA", "FANTOMA", "FANTOMA"]
            }
            df_seq = pd.DataFrame(seq_data)
            st.dataframe(df_seq, use_container_width=True)

            st.markdown("""
<div class="finding-box">
<b>Mecanism identificat:</b> In interiorul unui mall sau suk acoperit din Abu Dhabi,
receptorul GNSS al Samsung Galaxy A72 a pierdut semnalul satelitar si a retinut
ultimele coordonate valide. Secventa cea mai lunga: <b>24 fotografii consecutive</b>
(~2,5 minute) cu lat/lon/alt/GPS_timestamp IDENTICE. Structurial, datele sunt
indistinguibile de coordonate GPS valide.
</div>
""", unsafe_allow_html=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("**Distributia altitudinilor WGS84 — Abu Dhabi:**")
            if PLOTLY_OK:
                alt_bins = [-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15]
                alt_counts = [3, 8, 25, 48, 62, 55, 35, 15, 8, 3, 2, 0]
                fig_hist = go.Figure(go.Bar(
                    x=[f"{alt_bins[i]} la {alt_bins[i+1]}m" for i in range(len(alt_bins)-1)],
                    y=alt_counts[:len(alt_bins)-1],
                    marker_color=["#1a5276" if v > -10 else "#c0392b" for v in alt_bins[:-1]],
                    text=alt_counts[:len(alt_bins)-1],
                    textposition="outside"
                ))
                fig_hist.update_layout(
                    title="Distributie altitudini WGS84 (Abu Dhabi, 264 JPG)",
                    xaxis_title="Interval altitudine WGS84",
                    yaxis_title="Nr. fotografii",
                    height=350, showlegend=False
                )
                st.plotly_chart(fig_hist, use_container_width=True)

        with col_r:
            st.markdown("**Interpretare geodezica:**")
            st.markdown("""
| Altitudine WGS84 | H ortometric* | Interpretare |
|---|---|---|
| −38,4 m (min) | −11,4 m | Parcare subterana? |
| −22,0 m (medie) | **≈ 0 m** | **Nivelul marii Abu Dhabi** |
| −11,5 m | ≈ +10,5 m | Strada/cladire joasa |
| +13,1 m (max) | ≈ +36 m | Etaj superior |

*H = h_WGS84 − N_geoid; N ≈ −27 m la Abu Dhabi (EGM96)
            """)
            st.info("**Confirmare empirica EGM96:** Media altitudinilor WGS84 (−22m) "
                    "corespunde exact nivelului marii la Abu Dhabi conform modelului geoidal.")

    # ── BURJ KHALIFA ─────────────────────────────────────────────────────────────
    with sec2:
        st.markdown("### Burj Khalifa, Dubai — 9 decembrie 2025")
        st.markdown("""
**194 fotografii JPG** capturate in si in jurul Burj Khalifa (828 m, cea mai inalta cladire din lume).
Analiza EXIF a relevat un **profil complet de altitudine** si doua tipuri de comportament GPS.
        """)

        if PLOTLY_OK:
            # Profil altitudine Burj Khalifa
            faze = [
                ("Sosire exterior\n15:43-15:47 UTC", -30, 8, "#27ae60", "GPS OK"),
                ("Interior intrare\n16:47-16:54 UTC", None, 29, "#e74c3c", "GPS ABSENT"),
                ("Platforma obs.\n16:56-18:01 UTC", 427, 52, "#1a5276", "GPS OK — Etaj 124"),
                ("Interior seara\n18:45-18:50 UTC", None, 24, "#e67e22", "GPS PARTIAL"),
                ("Subsol\n18:50 UTC", -67.7, 2, "#8e44ad", "GPS OK — Subteran"),
                ("Noapte 21:11\n21:11-22:14 UTC", 252, 79, "#2980b9", "GPS OK — Etaj ~45"),
            ]

            fig_burj = go.Figure()
            culori = [f[3] for f in faze]
            for i, (faza, alt, n, col, status) in enumerate(faze):
                if alt is not None:
                    fig_burj.add_trace(go.Scatter(
                        x=[i], y=[alt],
                        mode="markers+text",
                        marker=dict(size=max(12, n//3), color=col, symbol="circle",
                                    line=dict(color="white", width=2)),
                        text=[f"{alt}m<br>{n} foto"],
                        textposition="top center",
                        name=status,
                        hovertemplate=f"<b>{faza}</b><br>Alt: {alt}m WGS84<br>Foto: {n}<br>{status}<extra></extra>"
                    ))
                else:
                    fig_burj.add_trace(go.Scatter(
                        x=[i], y=[0],
                        mode="markers+text",
                        marker=dict(size=max(12, n//3), color=col, symbol="x",
                                    line=dict(color="white", width=2)),
                        text=[f"GPS ABSENT<br>{n} foto"],
                        textposition="top center",
                        name=status,
                        hovertemplate=f"<b>{faza}</b><br>GPS ABSENT<br>Foto: {n}<br>{status}<extra></extra>"
                    ))

            # Linia nivelului marii WGS84 la Dubai
            fig_burj.add_hline(y=-33, line_dash="dash", line_color="#e74c3c",
                               annotation_text="Nivelul marii WGS84 Dubai (N≈−33m)")
            fig_burj.add_hline(y=452-33, line_dash="dot", line_color="#1a5276",
                               annotation_text="Etaj 124 At the Top (452m ortometric = 419m WGS84)")

            fig_burj.update_layout(
                title="Profil altitudine EXIF WGS84 — Burj Khalifa, 9 dec 2025",
                xaxis=dict(ticktext=[f[0] for f in faze], tickvals=list(range(len(faze)))),
                yaxis_title="Altitudine WGS84 (m)",
                height=500, showlegend=True,
                xaxis_title="Faza / Ora"
            )
            st.plotly_chart(fig_burj, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
**Tabel faze Burj Khalifa:**

| Faza | Alt. WGS84 | H ortometric | Locatie |
|---|---|---|---|
| Exterior sosire | −28 la −35 m | 0–5 m | Strada Dubai |
| **Interior intrare** | **GPS ABSENT** | — | **Lobby Burj Khalifa** |
| **Platforma obs.** | **424–433 m** | **≈ 460 m** | **Etaj 124 "At the Top"** |
| Subsol | **−67,7 m** | −34,7 m | Parcare/Metro subteran |
| Noapte (ext.) | 240–265 m | ≈ 275 m | Zona exterioara Burj |
            """)
        with col_b:
            st.markdown("""
**Validare geodezica:**

Altitudine medie platforma: **427 m WGS84**
N_geoid Dubai (din masuratori): **≈ −33 m**
H ortometric calculat: **427 − (−33) = 460 m**
Etaj 124 "At the Top" (oficial): **452 m**
**Diferenta: 8 m → CONFIRMAT!** ✓

---

**Comportament GPS in Burj Khalifa:**
- **TIP 1 — GPS ABSENT:** 29 foto fara niciun camp GPS in EXIF (lobby/interior)
- **TIP 2 — GPS VALID:** 142 foto cu altitudine corecta (exterior/platforma)
- **TIP 3 — GPS NEGATIV:** −67,7 m WGS84 = subsol confirmat
            """)
            st.success("Burj Khalifa (828m) confirma functionarea GPS la altitudini "
                       "extreme urbane cand exista vizibilitate satelitara.")

    # ── COMPARATIE GEOID TRI-CONTINENTAL ─────────────────────────────────────────
    with sec3:
        st.markdown("### Comparatie Geoid EGM96 — Trei Continente")
        st.markdown("""
Datele reale din cele trei locatii documentate confirma in mod empiric modelul geoidal EGM96
(Lemoine et al., 1998; Pavlis et al., 2012) — **primul studiu care valideaza N_geoid din
metadate EXIF ale fotografiilor de consum.**
        """)

        # Tabel geoid
        geoid_data = {
            "Locatie": ["Tenerife, Insulele Canare (Atlantic)", "Abu Dhabi, EAU (Golf Persic)", "Dubai, EAU (Golf Persic)"],
            "Coordonate": ["28.019°N, 16.614°V", "24.412°N, 54.475°E", "25.205°N, 55.276°E"],
            "Data": ["9 aug 2025", "10 dec 2025", "9 dec 2025"],
            "Alt. medie WGS84": ["+48.54 m (fantoma)", "−22.0 m (medie)", "−30 m (sol)"],
            "N_geoid EGM96 (empiric)": ["+48 m", "−27 m", "−33 m"],
            "Nivel mare = WGS84": ["+48 m", "−22 m", "−33 m"],
            "Fenomen documentat": ["GPS Fantoma 243 foto / 49 min", "GPS Fantoma 8 secv. / max 24 foto", "GPS Absent lobby / Altit. obs. deck confirmata"]
        }
        df_geoid = pd.DataFrame(geoid_data)
        st.dataframe(df_geoid, use_container_width=True)

        if PLOTLY_OK:
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                # Bar chart geoid comparison
                locatii = ["Tenerife\n(Atlantic)", "Abu Dhabi\n(Golf Persic)", "Dubai\n(Golf Persic)"]
                n_vals = [48, -27, -33]
                culori_g = ["#1a5276" if v > 0 else "#c0392b" for v in n_vals]

                fig_geoid = go.Figure(go.Bar(
                    x=locatii, y=n_vals,
                    marker_color=culori_g,
                    text=[f"N = {v} m" for v in n_vals],
                    textposition="outside"
                ))
                fig_geoid.add_hline(y=0, line_color="black", line_width=2,
                                    annotation_text="Nivelul mediu al marii (H=0 m ortometric)")
                fig_geoid.update_layout(
                    title="N_geoid EGM96 confirmat empiric din EXIF fotografii",
                    yaxis_title="Ondulatie geoid N (m WGS84)",
                    height=380,
                    yaxis=dict(range=[-60, 70])
                )
                st.plotly_chart(fig_geoid, use_container_width=True)

            with col_g2:
                # Scatter: WGS84 vs ortometric
                fig_comp = go.Figure()
                # Tenerife sea level
                fig_comp.add_trace(go.Scatter(
                    x=[1], y=[48.54],
                    mode="markers+text",
                    name="Tenerife — GPS Fantoma (nivelul marii)",
                    marker=dict(size=20, color="#c0392b", symbol="star"),
                    text=["Tenerife\n+48.54m WGS84\n= 0m ortometric"],
                    textposition="top right"
                ))
                fig_comp.add_trace(go.Scatter(
                    x=[2], y=[-22.0],
                    mode="markers+text",
                    name="Abu Dhabi — medie altitudini",
                    marker=dict(size=20, color="#e67e22", symbol="star"),
                    text=["Abu Dhabi\n−22m WGS84\n≈ 0m ortometric"],
                    textposition="top right"
                ))
                fig_comp.add_trace(go.Scatter(
                    x=[3], y=[-33.0],
                    mode="markers+text",
                    name="Dubai — nivel sol",
                    marker=dict(size=20, color="#8e44ad", symbol="star"),
                    text=["Dubai\n−33m WGS84\n≈ 0m ortometric"],
                    textposition="top right"
                ))
                fig_comp.add_hline(y=0, line_dash="dash", line_color="blue",
                                   annotation_text="H=0 ortometric (nivelul marii real)")
                fig_comp.update_layout(
                    title="Nivelul marii WGS84 — 3 locatii, 3 valori complet diferite",
                    yaxis_title="Altitudine WGS84 (m)",
                    xaxis=dict(tickvals=[1,2,3], ticktext=["Tenerife", "Abu Dhabi", "Dubai"]),
                    height=380, showlegend=False
                )
                st.plotly_chart(fig_comp, use_container_width=True)

        st.divider()
        st.markdown("### Cele Doua Tipuri de Esec GPS — Clasificare Noua")

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("""
<div style='background:#eafaf1; border:2px solid #27ae60; border-radius:10px; padding:16px;'>
<h4 style='color:#1e8449;'>TIP 1 — GPS ABSENT</h4>
<b>Definitie:</b> Receptorul GNSS nu inregistreaza niciun camp GPS in EXIF.<br><br>
<b>Observat:</b> 29 fotografii in lobby-ul Burj Khalifa (interior cladire)<br><br>
<b>Detectabilitate:</b> ✅ IMEDIAT — campurile GPS lipsesc din EXIF<br><br>
<b>Pericol pentru AI:</b> SCAZUT — sistemele de validare refuza datele fara GPS<br><br>
<b>Conform JEITA EXIF 2.32:</b> Comportament <i>conform</i> — absenta campului = lipsa date
</div>
""", unsafe_allow_html=True)

        with col_t2:
            st.markdown("""
<div style='background:#fef9f9; border:2px solid #c0392b; border-radius:10px; padding:16px;'>
<h4 style='color:#c0392b;'>TIP 2 — GPS FANTOMA ⚠️</h4>
<b>Definitie:</b> Receptorul GNSS retine ultima coordonata valida si o inscrie in EXIF-ul tuturor
fotografiilor ulterioare, fara niciun indicator de pierdere a semnalului.<br><br>
<b>Observat:</b> 243 foto Tenerife (49 min) + 8 secvente Abu Dhabi (max 24 foto)<br><br>
<b>Detectabilitate:</b> ❌ INVIZIBIL — EXIF are structura identica cu date valide<br><br>
<b>Pericol pentru AI:</b> CRITIC — sistemele AI accepta coordonatele ca valide<br><br>
<b>Indicator cheie:</b> GPS Timestamp ingheat vs Camera DateTime (delta >120s = ALERT)
</div>
""", unsafe_allow_html=True)

        st.divider()
        st.markdown("""
<div class="doi-box">
<b>Referinta stiintifica:</b> Gamulescu, O.M. (2026). GPS Fantoma: Primul Studiu Experimental
Privind Inghetarea Silentioasa a Coordonatelor GNSS in 6 Aplicatii Georeferentiale Mobile
— Cadrul AGRI-GEO si Implicatii pentru Managementul Riscului Agricol.<br>
<b>DOI articol anterior:</b> 10.5281/zenodo.19829462<br>
Platforma: https://georeferencing-applications.streamlit.app/c_SecureGeo_GNSS_Framework
</div>
""", unsafe_allow_html=True)
