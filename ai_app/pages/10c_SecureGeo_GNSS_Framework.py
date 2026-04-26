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

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

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

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sgf-header">
    <h1>SecureGeo Global Framework</h1>
    <p>Comportamentul GNSS in conditii extreme: de la +11.439 m (aviatie comerciala)
    la -30 m (submarin turistic, Oceanul Atlantic, Tenerife)<br>
    Implicatii pentru integritatea datelor in sisteme AI — GDPR + Regulamentul UE 2024/1689</p>
</div>
""", unsafe_allow_html=True)

# ─── METRICI CHEIE ─────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown("""<div class="metric-card">
    <div class="val">11.469</div>
    <div class="lbl">m altitudine totala<br>range documentat</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="metric-card">
    <div class="val">924</div>
    <div class="lbl">fotografii EXIF<br>analizate (2 experimente)</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="metric-card">
    <div class="val" style="color:#c0392b;">243</div>
    <div class="lbl">fotografii cu GPS<br>fantoma (49 min)</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="metric-card">
    <div class="val">48,5 m</div>
    <div class="lbl">valoare fantoma<br>inghetata WGS84</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown("""<div class="metric-card">
    <div class="val">6</div>
    <div class="lbl">criterii AGRI-GEO<br>Framework propuse</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Zbor Aviatie (+11.439 m)",
    "Submarin Tenerife (-30 m)",
    "GPS Fantoma — Descoperire",
    "AGRI-GEO Framework (6 criterii)",
    "Implicatii GDPR + Actul AI"
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
<b>Zenodo Preprint.</b> doi: <code>[DOI disponibil dupa upload Zenodo]</code><br>
Target: MDPI Sensors (IF 3.4, Q1) | MDPI Drones (IF 4.8, Q1)
</div>
""", unsafe_allow_html=True)

    st.caption(
        "Pagina 10c — SecureGeo Global Framework | "
        "Bloc 5 AI Aplicat | UCB Targu Jiu | "
        f"Actualizat: {date.today().strftime('%d.%m.%Y')} | "
        "Prof. Asoc. Dr. Oliviu Mihnea Gamulescu"
    )
