# -*- coding: utf-8 -*-
"""
SecureGeo Defense Platform
GNSS/GPS Anti-Spoofing | Anti-Sniffing | Anti-Tampering
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu
"""

import streamlit as st
import hashlib
import json
import io
import os
import math
import zipfile
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
    page_title="SecureGeo Defense",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
  <div style='font-size:22px; font-weight:900; color:#1a5276;'>SecureGeo</div>
  <div style='font-size:11px; color:#c0392b; font-weight:700;'>DEFENSE PLATFORM</div>
  <div style='font-size:10px; color:#666; margin-top:4px;'>GNSS Security & Data Integrity</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("""
**Module disponibile:**
- GNSS / GPS Anti-Spoofing
- Anti-Sniffing
- Anti-Tampering
- Analiza fotografii teren
""")
st.sidebar.divider()
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.markdown("**Referinta:** [9] Gamulescu, O.-M. (2026). Zenodo DOI 10.5281/zenodo.19829463")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#1a5276; border-radius:8px; padding:10px 12px; color:white;
     font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj<br>
<b>Lege:</b> Legea nr. 8/1996<br>
<div style='margin-top:4px; opacity:0.8; font-size:9px;'>
Citare obligatorie la orice utilizare.
</div>
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#1a5276 0%,#922b21 50%,#145a32 100%);
     border-radius:12px; padding:20px 28px; color:white; margin-bottom:16px;'>
  <div style='font-size:24px; font-weight:900; letter-spacing:1px;'>
    SecureGeo Defense Platform
  </div>
  <div style='font-size:13px; margin-top:6px; opacity:0.9;'>
    GNSS / GPS Anti-Spoofing &nbsp;|&nbsp; Anti-Sniffing &nbsp;|&nbsp; Anti-Tampering
  </div>
  <div style='font-size:11px; margin-top:4px; opacity:0.7;'>
    Sisteme de securitate pentru date geospatiale agricole | UAV | LPIS | APIA
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Constelatii verificate", "4", "GPS+Galileo+GLONASS+BeiDou")
with c2:
    st.metric("Algoritm hash", "SHA-256", "Anti-Tampering")
with c3:
    st.metric("Criptare transport", "TLS 1.3", "Anti-Sniffing")
with c4:
    st.metric("Autentificare", "OSNMA", "Galileo SIS ICD v1.1")

st.divider()

# ── 4 taburi ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "GNSS / GPS Anti-Spoofing",
    "Anti-Sniffing",
    "Anti-Tampering",
    "Analiza Fotografii Teren"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: GNSS / GPS ANTI-SPOOFING
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### GNSS / GPS Anti-Spoofing")
    st.markdown("""
    <div style='background:#fdebd0; border-left:5px solid #e67e22;
         border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:16px; font-size:12px;'>
        <b>Ce este spoofing-ul GNSS?</b><br>
        Un atacator transmite un semnal radio mai puternic decat semnalele reale ale
        satelitilor GNSS. Receptorul GPS al dronei primeste semnalul fals si crede ca
        se afla intr-o alta pozitie. Rezultat: coordonate EXIF false in fotografiile
        de drona, harta de prescriptie NDVI georeferentiata gresit, date APIA/LPIS eronate.
    </div>
    """, unsafe_allow_html=True)

    col_atac, col_aparare = st.columns([1, 1])

    with col_atac:
        st.markdown("#### Scenariu atac spoofing pe drona agricola")
        st.markdown("""
        <div style='background:white; border-radius:10px; padding:14px;
             box-shadow:0 2px 6px rgba(0,0,0,0.08);'>
        <b>Pas 1:</b> Atacatorul plaseaza un emitator GPS la marginea parcelei.<br><br>
        <b>Pas 2:</b> Emite semnale GPS cu putere superioara satelitilor reali (+10 dB).<br><br>
        <b>Pas 3:</b> Receptorul dronei pierde fixul real si blocheaza semnalul fals.<br><br>
        <b>Pas 4:</b> Drona isi <i>crede</i> pozitia deplasata cu 500m spre nord.<br><br>
        <b>Pas 5:</b> Fotografiile inregistreaza coordonate false in EXIF.<br><br>
        <b>Pas 6:</b> Ortomozaicul generat este deplasat sistematic &mdash; incapabil
        pentru verificarea conformitatii PAC/LPIS.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Efecte detectabile")
        efecte = [
            ("Deplasare pozitie", "500 m - 10 km", "#c0392b"),
            ("Falsificare traseu zbor", "Ruta inexistenta in realitate", "#c0392b"),
            ("Coordonate EXIF alterate", "Lat/Lon false in toate fotografiile", "#c0392b"),
            ("Erori georeferentiere", "Ortomozaic deplasat sistematic", "#e67e22"),
            ("Date LPIS invalide", "Verificare PAC imposibila", "#922b21"),
        ]
        for efect, descriere, culoare in efecte:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; padding:6px 10px;
                 background:white; border-radius:6px; margin:3px 0; font-size:11px;
                 border-left:4px solid {culoare};'>
                <div style='flex:1; font-weight:600; color:#333;'>{efect}</div>
                <div style='color:#666;'>{descriere}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_aparare:
        st.markdown("#### Masuri Anti-Spoofing")

        masuri = [
            {
                "nr": "1",
                "titlu": "Verificare multi-constelatie",
                "desc": "GPS + Galileo + GLONASS + BeiDou simultan. Un atacator trebuie sa"
                        " simuleze 4 sisteme independente cu frecvente si geometrii diferite."
                        " Dificultate tehnica extrem de ridicata.",
                "culoare": "#1a5276",
                "eficienta": "95%",
            },
            {
                "nr": "2",
                "titlu": "Comparare IMU vs GNSS",
                "desc": "Modulul inertial (IMU) calculeaza pozitia independent de sateliti."
                        " Daca IMU spune: pozitia actuala este A, dar GNSS spune B"
                        " (diferenta >10m), este semnal de alarma de spoofing.",
                "culoare": "#117a65",
                "eficienta": "88%",
            },
            {
                "nr": "3",
                "titlu": "Detectie salturi imposibile de pozitie",
                "desc": "O drona la 500m/h nu poate sari 1000m intr-o secunda. Verificarea"
                        " consecutiva a coordonatelor EXIF detecteaza astfel de anomalii."
                        " Metoda RAIM (Receiver Autonomous Integrity Monitoring).",
                "culoare": "#6c3483",
                "eficienta": "92%",
            },
            {
                "nr": "4",
                "titlu": "Verificare semnal RF",
                "desc": "Analiza puterii semnalului receptionat. Semnalele GNSS reale ajung"
                        " la -130 dBm (foarte slabe). Un semnal artificial este mai puternic"
                        " &mdash; detectabil prin monitorizarea raportului semnal/zgomot (SNR).",
                "culoare": "#d35400",
                "eficienta": "80%",
            },
            {
                "nr": "5",
                "titlu": "Galileo OSNMA",
                "desc": "Open Service Navigation Message Authentication (SIS ICD v1.1)."
                        " Autentificare criptografica a mesajelor Galileo &mdash; imposibil"
                        " de falsificat fara cheia privata ESA/EUSPA.",
                "culoare": "#c0392b",
                "eficienta": "99%",
            },
            {
                "nr": "6",
                "titlu": "RAIM — Receiver Autonomous Integrity Monitoring",
                "desc": "Compara redundant pseudodistantele de la minim 5 sateliti vizibili."
                        " Izoleaza semnalele inconsistente. Standard in aviatia certificata,"
                        " recomandat pentru drone agricole cu misiuni critice.",
                "culoare": "#1a5276",
                "eficienta": "91%",
            },
        ]

        for m in masuri:
            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:12px 14px;
                 margin:6px 0; border-left:5px solid {m["culoare"]};
                 box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div style='display:flex; align-items:center; gap:10px;'>
                        <div style='background:{m["culoare"]}; color:white; border-radius:50%;
                             width:22px; height:22px; display:flex; align-items:center;
                             justify-content:center; font-weight:900; font-size:11px;
                             flex-shrink:0;'>{m["nr"]}</div>
                        <b style='font-size:12px; color:#333;'>{m["titlu"]}</b>
                    </div>
                    <div style='background:{m["culoare"]}15; color:{m["culoare"]};
                         padding:2px 8px; border-radius:10px; font-weight:700;
                         font-size:11px;'>Eficienta {m["eficienta"]}</div>
                </div>
                <div style='font-size:11px; color:#555; margin-top:8px;
                     line-height:1.6;'>{m["desc"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Simulator spoofing interactiv
    st.divider()
    st.markdown("### Simulator atac spoofing — traiectorie drona agricola")

    col_sim1, col_sim2, col_sim3 = st.columns(3)
    with col_sim1:
        lat_baza = st.number_input("Latitudine parcela (grad N)", value=45.037, step=0.001, format="%.4f")
        lon_baza = st.number_input("Longitudine parcela (grad E)", value=23.272, step=0.001, format="%.4f")
    with col_sim2:
        deplasare_lat = st.slider("Deplasare spoofing latitudine (grade)", -0.05, 0.05, 0.02, 0.001)
        deplasare_lon = st.slider("Deplasare spoofing longitudine (grade)", -0.05, 0.05, -0.015, 0.001)
    with col_sim3:
        pct_afectate = st.slider("% fotografii afectate de spoofing", 0, 100, 60, 5)
        st.markdown(f"""
        <div style='background:#fdebd0; border-radius:8px; padding:10px; font-size:11px;'>
            <b>Eroare pozitionala estimata:</b><br>
            {abs(deplasare_lat)*111000:.0f} m N/S<br>
            {abs(deplasare_lon)*111000*math.cos(math.radians(lat_baza)):.0f} m E/W<br>
            <b>Total:</b> {math.sqrt((deplasare_lat*111000)**2 +
                (deplasare_lon*111000*math.cos(math.radians(lat_baza)))**2):.0f} m
        </div>
        """, unsafe_allow_html=True)

    if PLOTLY_OK:
        # Traiectorie reala (grila de drona pe parcela)
        track_real = []
        n_linii = 6
        for i in range(n_linii):
            lat_linie = lat_baza + (i * 0.002)
            lon_start = lon_baza
            lon_stop = lon_baza + 0.008
            for j in range(8):
                track_real.append({
                    "lat": lat_linie,
                    "lon": lon_start + j * (lon_stop - lon_start) / 7,
                    "nr": i * 8 + j
                })

        # Traiectorie falsificata prin spoofing (partial)
        track_spoof = []
        for p in track_real:
            if p["nr"] / (n_linii * 8) * 100 < pct_afectate:
                track_spoof.append({
                    "lat": p["lat"] + deplasare_lat,
                    "lon": p["lon"] + deplasare_lon,
                    "nr": p["nr"], "spoof": True
                })
            else:
                track_spoof.append({**p, "spoof": False})

        fig_spoof = go.Figure()

        fig_spoof.add_trace(go.Scattermapbox(
            lat=[p["lat"] for p in track_real],
            lon=[p["lon"] for p in track_real],
            mode="markers+lines",
            name="Traiectorie REALA",
            marker=dict(size=6, color="#1a5276"),
            line=dict(color="#1a5276", width=2),
            hovertemplate="REAL: %.5f N, %.5f E<extra></extra>" % (0, 0),
        ))

        spoof_pts = [p for p in track_spoof if p["spoof"]]
        real_pts  = [p for p in track_spoof if not p["spoof"]]

        if spoof_pts:
            fig_spoof.add_trace(go.Scattermapbox(
                lat=[p["lat"] for p in spoof_pts],
                lon=[p["lon"] for p in spoof_pts],
                mode="markers",
                name=f"Coordonate FALSIFICATE ({pct_afectate}%)",
                marker=dict(size=8, color="#c0392b"),
                hovertemplate="SPOOF: %.5f N, %.5f E<extra></extra>" % (0, 0),
            ))
        if real_pts:
            fig_spoof.add_trace(go.Scattermapbox(
                lat=[p["lat"] for p in real_pts],
                lon=[p["lon"] for p in real_pts],
                mode="markers",
                name="Coordonate neafectate",
                marker=dict(size=6, color="#27ae60"),
            ))

        fig_spoof.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(
                    lat=lat_baza + deplasare_lat / 2,
                    lon=lon_baza + deplasare_lon / 2
                ),
                zoom=13,
            ),
            height=380,
            margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)"),
        )
        st.plotly_chart(fig_spoof, use_container_width=True)

        st.markdown(f"""
        <div style='font-size:11px; color:#666; padding:6px;'>
            Cercuri rosii = coordonate GPS false inregistrate in EXIF ca urmare a spoofing-ului.
            Cercuri verzi = fotografii neatinse. {pct_afectate}% din misiune compromis.
        </div>
        """, unsafe_allow_html=True)

    # Tabel constelatii
    st.divider()
    st.markdown("### Comparatie sisteme GNSS — rezistenta la spoofing")

    import pandas as pd
    df_gnss = pd.DataFrame([
        {"Sistem": "GPS (SUA)", "Frecvente": "L1 (1575 MHz), L2, L5",
         "Autentif. civila": "Nu (L1 C/A fara)", "Sateliti activi": "31",
         "Precizie (civil)": "3-5 m", "Anti-spoofing": "Medie"},
        {"Sistem": "Galileo (UE)", "Frecvente": "E1, E5a, E5b, E6",
         "Autentif. civila": "DA — OSNMA pe E1", "Sateliti activi": "28",
         "Precizie (civil)": "1-4 m", "Anti-spoofing": "Ridicata (OSNMA)"},
        {"Sistem": "GLONASS (RUS)", "Frecvente": "L1 (1598-1606 MHz), L2",
         "Autentif. civila": "Nu", "Sateliti activi": "24",
         "Precizie (civil)": "5-7 m", "Anti-spoofing": "Scazuta"},
        {"Sistem": "BeiDou (CHN)", "Frecvente": "B1, B2, B3",
         "Autentif. civila": "Partial (BDS-3)", "Sateliti activi": "45",
         "Precizie (civil)": "3-5 m", "Anti-spoofing": "Medie"},
    ])
    st.dataframe(df_gnss, use_container_width=True, hide_index=True)
    st.markdown("""
    <div style='background:#eaf4fb; border-left:4px solid #1a5276;
         border-radius:0 8px 8px 0; padding:10px 14px; font-size:11px;'>
        <b>Recomandare:</b> Utilizarea simultana GPS + Galileo ofera cel mai bun echilibru
        acoperire globala + autentificare OSNMA. Adaugarea GLONASS/BeiDou creste redundanta
        dar nu imbunatateste semnificativ securitatea anti-spoofing.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: ANTI-SNIFFING
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Anti-Sniffing — Protectia impotriva interceptarii datelor")
    st.markdown("""
    <div style='background:#e8f8f5; border-left:5px solid #117a65;
         border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:16px; font-size:12px;'>
        <b>Ce este sniffing-ul?</b><br>
        Capturarea traficului de date in tranzit intre componentele sistemului agricol:
        drona &harr; statie control (GCS) &harr; server cloud &harr; platforma AI de decizie.
        Datele interceptate pot include coordonate GPS, imagini multispectrale, date LPIS/IACS.
    </div>
    """, unsafe_allow_html=True)

    col_sn1, col_sn2 = st.columns([1, 1])

    with col_sn1:
        st.markdown("#### Ce poate intercepta un sniffer intr-o misiune UAV")

        date_interceptabile = [
            {"Date": "Coordonate GPS (lat/lon/alt)", "Sensibilitate": "CRITICA",
             "Culoare": "#c0392b", "Impact": "Divulga locatia exacta a parcelei"},
            {"Date": "Imagini multispectrale NDVI", "Sensibilitate": "CRITICA",
             "Culoare": "#c0392b", "Impact": "Informa concurenti despre culturile dvs."},
            {"Date": "Metadata misiune (data/ora/ruta)", "Sensibilitate": "RIDICATA",
             "Culoare": "#e67e22", "Impact": "Dezvaluie programul de inspectie"},
            {"Date": "Identitate operator (EXIF Make/Model)", "Sensibilitate": "MEDIE",
             "Culoare": "#d4ac0d", "Impact": "Profilare comportament inspector"},
            {"Date": "Date LPIS/IACS (numar parcela)", "Sensibilitate": "CRITICA",
             "Culoare": "#c0392b", "Impact": "Date confidentiale PAC/subventii"},
            {"Date": "Video georeferentiat", "Sensibilitate": "RIDICATA",
             "Culoare": "#e67e22", "Impact": "Reconstructie 3D teren"},
        ]

        for d in date_interceptabile:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:10px 12px;
                 margin:4px 0; border-left:4px solid {d["Culoare"]}; font-size:11px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <b style='color:#333;'>{d["Date"]}</b>
                    <span style='background:{d["Culoare"]}; color:white; padding:1px 8px;
                         border-radius:8px; font-size:10px;'>{d["Sensibilitate"]}</span>
                </div>
                <div style='color:#666; margin-top:4px;'>{d["Impact"]}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_sn2:
        st.markdown("#### Masuri de protectie Anti-Sniffing")

        protectii = [
            {
                "titlu": "TLS 1.3 / DTLS pentru MAVLink",
                "desc": "Criptarea end-to-end a canalului de comunicatie drona-GCS."
                        " TLS 1.3 elimina vulnerabilitatile versiunilor anterioare."
                        " DTLS (Datagram TLS) pentru protocoale UDP (MAVLink, RTP video).",
                "culoare": "#1a5276",
            },
            {
                "titlu": "VPN pentru transmisie cloud",
                "desc": "Toate datele GPS si imagini transmise exclusiv prin tunel VPN"
                        " criptat catre serverul de procesare. Certificate digitale validate"
                        " de autoritate de certificare recunoscuta (eIDAS).",
                "culoare": "#117a65",
            },
            {
                "titlu": "Autentificare mutuala (mTLS)",
                "desc": "Drona, GCS si serverul de procesare se autentifica reciproc"
                        " prin certificate X.509. Previne atacurile man-in-the-middle:"
                        " niciun nod intermediar neautorizat nu poate intra in lant.",
                "culoare": "#6c3483",
            },
            {
                "titlu": "Retea wi-fi dedicata (WPA3)",
                "desc": "Reteaua de date a misiunii de drona pe frecventa dedicata,"
                        " protejata WPA3-SAE. Izolata de reteaua institutionala/publica."
                        " Masca SSID + filtrare MAC.",
                "culoare": "#d35400",
            },
            {
                "titlu": "Monitorizare anomalii trafic (IDS)",
                "desc": "Sistem de detectie intruziuni (IDS) care monitorizeaza traficul"
                        " de date al misiunii. Alerta automata la: captare pachete,"
                        " sesiuni neautorizate, volume anormale de trafic.",
                "culoare": "#c0392b",
            },
        ]

        for p in protectii:
            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:12px 14px;
                 margin:6px 0; border-left:5px solid {p["culoare"]};
                 box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
                <b style='font-size:12px; color:#333;'>{p["titlu"]}</b>
                <div style='font-size:11px; color:#555; margin-top:6px;
                     line-height:1.6;'>{p["desc"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Demo: date necriptate vs criptate
    st.divider()
    st.markdown("### Demo: Ce vede un sniffer — date necriptate vs criptate")

    col_raw, col_enc = st.columns(2)

    with col_raw:
        st.markdown("#### Date necriptate (HTTP/UDP plain)")
        st.markdown("""
        <div style='background:#fce4e4; border-radius:8px; padding:10px 12px; font-family:monospace;
             font-size:11px; line-height:1.8; border:1px solid #e74c3c;'>
            POST /api/mission HTTP/1.1<br>
            Host: agro-platform.ro<br>
            Content-Type: application/json<br><br>
            {<br>
            &nbsp;&nbsp;"lat": 45.0374823,<br>
            &nbsp;&nbsp;"lon": 23.2719841,<br>
            &nbsp;&nbsp;"alt_m": 87.3,<br>
            &nbsp;&nbsp;"parcela_id": "RO002437918",<br>
            &nbsp;&nbsp;"ndvi_value": 0.742,<br>
            &nbsp;&nbsp;"operator": "Gamulescu O.M.",<br>
            &nbsp;&nbsp;"data": "2025-04-23"<br>
            }<br><br>
            <span style='color:#c0392b; font-weight:bold;'>Orice sniffer in retea vede totul!</span>
        </div>
        """, unsafe_allow_html=True)

    with col_enc:
        st.markdown("#### Date criptate TLS 1.3 (HTTPS)")

        # Genereaza text "criptat" demo
        demo_plaintext = '{"lat":45.0374823,"lon":23.2719841,"parcela_id":"RO002437918"}'
        demo_hash = hashlib.sha256(demo_plaintext.encode()).hexdigest()[:32]
        demo_enc_fake = base64.b64encode(hashlib.sha512(demo_plaintext.encode()).digest()).decode()[:60]

        st.markdown(f"""
        <div style='background:#d5f5e3; border-radius:8px; padding:10px 12px; font-family:monospace;
             font-size:11px; line-height:1.8; border:1px solid #27ae60;'>
            TLSv1.3 Record Layer: Application Data<br>
            Content Type: Application Data (23)<br>
            Version: TLS 1.2 (0x0303)<br>
            Length: 512<br><br>
            Encrypted Application Data:<br>
            {demo_enc_fake}<br>
            ...[continut complet indescifrabil]<br><br>
            <span style='color:#27ae60; font-weight:bold;'>Sniffer-ul nu poate decripta!</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#eaf4fb; border-left:4px solid #1a5276;
         border-radius:0 8px 8px 0; padding:10px 14px; margin-top:12px; font-size:11px;'>
        <b>Concluzie practica:</b> Activarea HTTPS + TLS 1.3 pentru toate API-urile de
        transmisie date agricole este obligatorie pentru protectia datelor LPIS/IACS.
        Cost implementare: minim (free cu Let's Encrypt). Beneficiu: protectie totala
        impotriva sniffing-ului pasiv.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: ANTI-TAMPERING
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Anti-Tampering — Protectia impotriva modificarii datelor sau sistemului")
    st.markdown("""
    <div style='background:#f4ecf7; border-left:5px solid #6c3483;
         border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:16px; font-size:12px;'>
        <b>Ce este tampering-ul?</b><br>
        Modificarea neautorizata a datelor, imaginilor, coordonatelor GPS sau
        software-ului sistemului, dupa capturare si inainte/in timpul procesarii.
        Impactul direct: coordonate EXIF false in fotografii UAV, georeferentiere alterata,
        date invalide pentru verificarile PAC/LPIS.
    </div>
    """, unsafe_allow_html=True)

    col_tp1, col_tp2 = st.columns([1, 1])

    with col_tp1:
        st.markdown("#### Cele 8 mecanisme de protectie Anti-Tampering")

        mecanisme = [
            {
                "nr": "1",
                "titlu": "Sigilii de securitate pe echipamente",
                "desc": "Sigilii fizice (holografice, evidente la deteriorare) pe"
                        " corpul dronei, baterie si card SD. Orice deschidere fizica"
                        " neautorizata este imediat vizibila. Standard: ISO/IEC 18000.",
                "culoare": "#1a5276",
                "icon": "FIZIC",
            },
            {
                "nr": "2",
                "titlu": "Criptare + semnatura digitala fisiere",
                "desc": "Fiecare fisier imagine (JPG/HEIC) este semnat digital cu"
                        " certificatul operatorului (eIDAS). Semnatura acopera inclusiv"
                        " metadatele EXIF cu coordonatele GPS.",
                "culoare": "#117a65",
                "icon": "CRIPTO",
            },
            {
                "nr": "3",
                "titlu": "Checksum / Hash SHA-256",
                "desc": "La capturare, se calculeaza automat SHA-256 al fiecarui fisier."
                        " Jurnalul de hashuri este stocat separat si semnat. Orice"
                        " modificare a fisierului (inclusiv 1 bit din EXIF GPS)"
                        " produce un hash complet diferit.",
                "culoare": "#6c3483",
                "icon": "HASH",
            },
            {
                "nr": "4",
                "titlu": "Verificare integritate software",
                "desc": "La pornire, sistemul calculeaza hash-ul tuturor modulelor"
                        " software si le compara cu valorile certificate de producator."
                        " Orice modificare a codului = refuz executie.",
                "culoare": "#d35400",
                "icon": "SW",
            },
            {
                "nr": "5",
                "titlu": "Secure Boot",
                "desc": "Procesul de bootare verifica semnatura digitala a fiecarui"
                        " strat software: UEFI → Bootloader → OS → Aplicatie drona."
                        " Firmware necertificat nu poate fi executat niciodata.",
                "culoare": "#c0392b",
                "icon": "BOOT",
            },
            {
                "nr": "6",
                "titlu": "Detectie modificari firmware",
                "desc": "Comparare continua a hash-ului firmware-ului activ cu"
                        " valoarea de referinta stocata in TPM. Orice inject de"
                        " malware in firmware = alarma imediata + blocare sistem.",
                "culoare": "#1a5276",
                "icon": "FW",
            },
            {
                "nr": "7",
                "titlu": "Anti-debugging / Anti-reverse-engineering",
                "desc": "Codul de procesare GPS este protejat impotriva analizei"
                        " prin: obfuscare cod, detectie debugger activ, verificare"
                        " mediu de executie (VM/sandbox). Previne intelegerea si"
                        " modificarea algoritmilor de achizitie coordonate.",
                "culoare": "#117a65",
                "icon": "ANTI-DBG",
            },
            {
                "nr": "8",
                "titlu": "TPM (Trusted Platform Module)",
                "desc": "Chip hardware dedicat care stocheaza chei criptografice"
                        " intr-un mediu izolat fizic. Cheile nu pot fi extrase"
                        " software. Garanteaza autenticitatea certificatelor"
                        " folosite la semnarea datelor de misiune.",
                "culoare": "#6c3483",
                "icon": "TPM",
            },
        ]

        for m in mecanisme:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:10px 12px;
                 margin:4px 0; border-left:4px solid {m["culoare"]}; font-size:11px;
                 box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                <div style='display:flex; align-items:center; gap:8px;'>
                    <div style='background:{m["culoare"]}; color:white; border-radius:4px;
                         padding:2px 6px; font-size:9px; font-weight:700;
                         flex-shrink:0;'>{m["icon"]}</div>
                    <b style='color:#333;'>{m["nr"]}. {m["titlu"]}</b>
                </div>
                <div style='color:#555; margin-top:6px; line-height:1.5;'>{m["desc"]}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_tp2:
        st.markdown("#### Ce poate detecta un sistem anti-tampering")

        detectii = [
            {
                "caz": "Cineva a modificat codul aplicatiei",
                "metoda": "Hash SHA-256 al binarului ≠ valoare certificata",
                "rezultat": "Executie blocata + alarma", "status": "DETECTAT"
            },
            {
                "caz": "Executabil injectat cu malware",
                "metoda": "Secure Boot / verificare semnatura binara",
                "rezultat": "Boot refuzat", "status": "DETECTAT"
            },
            {
                "caz": "Date GPS alterate in EXIF",
                "metoda": "Hash fisier imagine ≠ valoarea originala din jurnal",
                "rezultat": "Fisier marcat invalid", "status": "DETECTAT"
            },
            {
                "caz": "Imagini UAV editate dupa capturare",
                "metoda": "Hash SHA-256 imagine ≠ hash din jurnal misiune",
                "rezultat": "Proba invalida in contestatie", "status": "DETECTAT"
            },
            {
                "caz": "Firmware drona modificat",
                "metoda": "TPM: hash firmware activ ≠ referinta",
                "rezultat": "Drona blocata la pornire", "status": "DETECTAT"
            },
            {
                "caz": "Chei criptografice extrase",
                "metoda": "TPM izolat fizic — imposibil software",
                "rezultat": "Imposibil fara distrugere fizica chip", "status": "PROTEJAT"
            },
        ]

        for d in detectii:
            culoare = "#27ae60" if d["status"] == "DETECTAT" else "#1a5276"
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:10px 12px;
                 margin:4px 0; border-left:4px solid {culoare}; font-size:11px;'>
                <div style='display:flex; justify-content:space-between;'>
                    <b style='color:#333;'>{d["caz"]}</b>
                    <span style='background:{culoare}; color:white; padding:1px 8px;
                         border-radius:8px; font-size:10px; white-space:nowrap;
                         margin-left:8px;'>{d["status"]}</span>
                </div>
                <div style='color:#666; margin-top:4px;'><i>Metoda:</i> {d["metoda"]}</div>
                <div style='color:{culoare}; margin-top:2px; font-weight:600;'>
                    Rezultat: {d["rezultat"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # Demo live hash
        st.divider()
        st.markdown("#### Demo live: Verificare integritate SHA-256")
        st.markdown("Introduce text sau date GPS — simuleaza modificarea si detectia:")

        text_original = st.text_area(
            "Date GPS originale (EXIF simulat)",
            value='{"lat":45.0374823,"lon":23.2719841,"alt_m":87.3,"timestamp":"2025:04:23 11:34:20"}',
            height=80
        )
        hash_original = hashlib.sha256(text_original.encode()).hexdigest()
        st.code(f"SHA-256 original:\n{hash_original}", language="text")

        text_modificat = st.text_area(
            "Date GPS modificate (simuleaza tampering — schimba un caracter)",
            value=text_original.replace("45.037", "45.139"),
            height=80
        )
        hash_modificat = hashlib.sha256(text_modificat.encode()).hexdigest()
        st.code(f"SHA-256 dupa modificare:\n{hash_modificat}", language="text")

        if hash_original != hash_modificat:
            st.error("TAMPERING DETECTAT! Hashurile sunt diferite. Datele GPS au fost modificate.")
        else:
            st.success("Integritate confirmata. Datele nu au fost modificate.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: ANALIZA FOTOGRAFII TEREN
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Analiza fotografii teren — Securitate EXIF + Integritate")
    st.markdown("""
    <div style='background:#fef9e7; border-left:5px solid #f39c12;
         border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:16px; font-size:12px;'>
        Incarca fotografii din folderul tau <b>G:\\2025 PROPRIETATE OLIVIU\\TERENURI</b>
        pentru analiza EXIF GPS + calculul hashului SHA-256 de integritate.
        Sistemul verifica prezenta coordonatelor GPS, altitudinii si calculeaza
        amprenta digitala a fisierului pentru anti-tampering.
    </div>
    """, unsafe_allow_html=True)

    col_up, col_rez = st.columns([1, 1])

    with col_up:
        st.markdown("#### Incarca fotografie teren")
        fisiere = st.file_uploader(
            "JPG din folderul TERENURI (2025 aprilie / 2026 martie)",
            type=["jpg", "jpeg"],
            accept_multiple_files=True,
            help="G:\\2025 PROPRIETATE OLIVIU\\TERENURI"
        )

        use_demo = st.checkbox("Sau foloseste date demo (teren Gorj, 2025)", value=not bool(fisiere))

        # Date demo — fotografii reale de teren din zona Gorj
        DEMO_TERENURI = [
            {
                "fisier": "20250331_112921.jpg",
                "lat": 45.0374823, "lon": 23.2719841,
                "alt_m": None, "ts": "2025:03:31 11:29:21",
                "telefon": "Samsung SM-A725F",
                "are_gps": True, "are_alt": False,
                "locatie": "Teren agricol Gorj — parcela 1"
            },
            {
                "fisier": "20250331_114314.jpg",
                "lat": 45.0382156, "lon": 23.2724833,
                "alt_m": None, "ts": "2025:03:31 11:43:14",
                "telefon": "Samsung SM-A725F",
                "are_gps": True, "are_alt": False,
                "locatie": "Teren agricol Gorj — parcela 2"
            },
            {
                "fisier": "20260324_121412.jpg",
                "lat": 44.5631248, "lon": 23.5824891,
                "alt_m": 285.3, "ts": "2026:03:24 12:14:12",
                "telefon": "Samsung SM-A725F",
                "are_gps": True, "are_alt": True,
                "locatie": "Teren agricol Gorj — parcela 3 (2026)"
            },
        ]

    def analizeaza_fisier_upload(f):
        if not PIL_OK:
            return {"eroare": "PIL nedisponibil"}, None
        try:
            img = Image.open(f)
            exif_raw = img._getexif()
            if not exif_raw:
                try:
                    exif_data = img.getexif()
                    if exif_data:
                        exif_raw = {k: v for k, v in exif_data.items()}
                except Exception:
                    pass
            if not exif_raw:
                return {"eroare": "Fara EXIF"}, img

            exif = {TAGS.get(k, k): v for k, v in exif_raw.items()}
            gps_raw = exif.get("GPSInfo", {})
            gps = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}

            def conv(val):
                def r2f(r):
                    try:
                        if hasattr(r, 'numerator'):
                            return float(r.numerator) / float(r.denominator) if r.denominator else 0.0
                        return float(r[0]) / float(r[1]) if r[1] else 0.0
                    except Exception:
                        return 0.0
                d, m, s = val
                return r2f(d) + r2f(m) / 60 + r2f(s) / 3600

            lat = lon = alt_m = None
            if "GPSLatitude" in gps:
                lat = round(conv(gps["GPSLatitude"]), 7)
                if gps.get("GPSLatitudeRef") == "S":
                    lat = -lat
            if "GPSLongitude" in gps:
                lon = round(conv(gps["GPSLongitude"]), 7)
                if gps.get("GPSLongitudeRef") == "W":
                    lon = -lon
            if "GPSAltitude" in gps:
                try:
                    a = gps["GPSAltitude"]
                    alt_m = round(float(a.numerator) / float(a.denominator) if hasattr(a, 'numerator') else float(a[0]) / float(a[1]), 1)
                except Exception:
                    alt_m = None

            f.seek(0)
            hash_val = hashlib.sha256(f.read()).hexdigest()
            f.seek(0)

            return {
                "fisier": f.name,
                "lat": lat, "lon": lon, "alt_m": alt_m,
                "ts": exif.get("DateTimeOriginal", exif.get("DateTime", "N/A")),
                "telefon": (str(exif.get("Make", "")) + " " + str(exif.get("Model", ""))).strip(),
                "are_gps": lat is not None and lon is not None,
                "are_alt": alt_m is not None,
                "sha256": hash_val,
            }, img
        except Exception as e:
            return {"eroare": str(e)[:80]}, None

    with col_rez:
        st.markdown("#### Rezultate analiza EXIF + Integritate")

        if fisiere and PIL_OK:
            for f in fisiere[:5]:
                rez, img_obj = analizeaza_fisier_upload(f)
                if "eroare" in rez:
                    st.error(f"{f.name}: {rez['eroare']}")
                    continue

                culoare_gps = "#27ae60" if rez["are_gps"] else "#c0392b"
                culoare_alt = "#27ae60" if rez["are_alt"] else "#e67e22"

                st.markdown(f"""
                <div style='background:white; border-radius:10px; padding:12px 14px;
                     margin:6px 0; border-left:5px solid {culoare_gps};
                     box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
                    <b style='font-size:12px;'>{rez["fisier"]}</b><br>
                    <div style='display:flex; flex-wrap:wrap; gap:10px; margin-top:6px; font-size:11px;'>
                        <span>GPS: <b style='color:{culoare_gps};'>
                            {"%.5f N, %.5f E" % (rez["lat"], rez["lon"]) if rez["are_gps"] else "LIPSA"}</b>
                        </span>
                        <span>Alt: <b style='color:{culoare_alt};'>
                            {"%.1f m" % rez["alt_m"] if rez["are_alt"] else "NU in EXIF"}</b>
                        </span>
                        <span>Device: <b>{rez["telefon"]}</b></span>
                    </div>
                    <div style='font-size:10px; color:#888; margin-top:6px; font-family:monospace;'>
                        SHA-256: {rez["sha256"][:48]}...</div>
                </div>
                """, unsafe_allow_html=True)

                if img_obj:
                    st.image(img_obj, caption=rez["fisier"], use_container_width=True)

        elif use_demo:
            st.markdown("**Date demo — fotografii teren proprietate Gorj:**")
            for demo in DEMO_TERENURI:
                c_gps = "#27ae60" if demo["are_gps"] else "#c0392b"
                c_alt = "#27ae60" if demo["are_alt"] else "#e67e22"
                demo_hash = hashlib.sha256(
                    f'{demo["lat"]}{demo["lon"]}{demo["ts"]}'.encode()
                ).hexdigest()
                st.markdown(f"""
                <div style='background:white; border-radius:10px; padding:12px 14px;
                     margin:6px 0; border-left:5px solid {c_gps};
                     box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
                    <b style='font-size:12px;'>{demo["fisier"]}</b>
                    <div style='font-size:11px; color:#555;'>{demo["locatie"]}</div>
                    <div style='display:flex; flex-wrap:wrap; gap:10px; margin-top:6px; font-size:11px;'>
                        <span>GPS: <b style='color:{c_gps};'>
                            {"%.5f N, %.5f E" % (demo["lat"], demo["lon"])}</b></span>
                        <span>Alt: <b style='color:{c_alt};'>
                            {"%.1f m" % demo["alt_m"] if demo["are_alt"] else "LIPSA din EXIF (FM-4)"}</b></span>
                        <span>Device: <b>{demo["telefon"]}</b></span>
                    </div>
                    <div style='font-size:10px; color:#888; margin-top:6px; font-family:monospace;'>
                        SHA-256 (demo): {demo_hash[:48]}...</div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("Incarca fotografii JPG din folderul TERENURI sau activeaza datele demo.")

    # Harta terenuri
    if PLOTLY_OK and use_demo:
        st.divider()
        st.markdown("### Harta parcele — cu verificare anti-tampering status")

        fig_teren = go.Figure()

        for demo in DEMO_TERENURI:
            demo_hash = hashlib.sha256(
                f'{demo["lat"]}{demo["lon"]}{demo["ts"]}'.encode()
            ).hexdigest()
            culoare = "#27ae60" if demo["are_alt"] else "#e67e22"
            fig_teren.add_trace(go.Scattermapbox(
                lat=[demo["lat"]],
                lon=[demo["lon"]],
                mode="markers+text",
                name=demo["fisier"],
                marker=dict(size=14, color=culoare),
                text=[demo["fisier"][:16]],
                textposition="top right",
                hovertemplate=(
                    f"<b>{demo['fisier']}</b><br>"
                    f"Lat: {demo['lat']:.5f}<br>"
                    f"Lon: {demo['lon']:.5f}<br>"
                    f"Alt: {demo['alt_m'] if demo['are_alt'] else 'LIPSA'}<br>"
                    f"GPS: {'OK' if demo['are_gps'] else 'LIPSA'}<br>"
                    f"SHA-256: {demo_hash[:20]}...<extra></extra>"
                ),
            ))

        fig_teren.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=45.0378, lon=23.272),
                zoom=13,
            ),
            height=380,
            margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)"),
        )
        st.plotly_chart(fig_teren, use_container_width=True)

    # Generare raport securitate
    st.divider()
    st.markdown("### Generare raport securitate geospatiala")

    col_rp1, col_rp2 = st.columns([2, 1])

    with col_rp2:
        proprietar = st.text_input("Proprietar teren", "Gamulescu Oliviu-Mihnea")
        locatie = st.text_input("Locatie", "Gorj, Romania")
        include_spoofing = st.checkbox("Include analiza anti-spoofing", True)
        include_tampering = st.checkbox("Include analiza anti-tampering", True)
        include_sniffing = st.checkbox("Include analiza anti-sniffing", True)

    with col_rp1:
        if st.button("Genereaza Raport Securitate", type="primary", use_container_width=True):
            sep = "=" * 72
            raport = f"""{sep}
RAPORT SECURITATE GEOSPATIALA — SecureGeo Defense Platform
Data: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Proprietar: {proprietar}
Locatie: {locatie}
Referinta: Gamulescu, O.-M. (2026). DOI: 10.5281/zenodo.19829463
{sep}

REZUMAT EVALUARE SECURITATE GNSS/GPS
--------------------------------------
"""
            if include_spoofing:
                raport += """
[1] GNSS / GPS ANTI-SPOOFING
    Risc identificat: Semnale GPS false pot deplasa virtual pozitia dronei
    Masuri implementate:
    - Verificare multi-constelatie: GPS + Galileo (OSNMA) recomandata
    - Comparare IMU vs GNSS: salturi imposibile detectate automat
    - RAIM: monitorizare autonoma integritate receptor
    - Galileo OSNMA SIS ICD v1.1: autentificare criptografica mesaje
    Status: NECESITA IMPLEMENTARE pe drona agricola curenta
"""
            if include_sniffing:
                raport += """
[2] ANTI-SNIFFING (protectie interceptare date)
    Date vulnerabile: coordonate GPS, imagini NDVI, date LPIS/IACS
    Masuri implementate:
    - Activati TLS 1.3 pentru toate API-urile de transmisie
    - VPN criptat pentru transmisie date misiune catre cloud
    - Autentificare mutuala mTLS drona-GCS-server
    Status: PARTIAL IMPLEMENTAT (necesita audit complet)
"""
            if include_tampering:
                raport += """
[3] ANTI-TAMPERING (protectie modificare date/sistem)
    Risc: Modificare coordonate GPS in EXIF sau injectie malware firmware
    Masuri implementate:
    - Hash SHA-256 pentru fiecare fisier imagine la capturare
    - Semnatura digitala pachet misiune (eIDAS)
    - Secure Boot activat pe echipamente
    - TPM: chei criptografice izolate hardware
    Status: RECOMANDAT pentru misiuni cu date LPIS/PAC
"""
            raport += f"""
CONCLUZIE
---------
Datele geospatiale agricole necesita protectie pe 3 niveluri:
spoofing (semnal fals), sniffing (interceptare) si tampering (falsificare).
Implementarea completa SecureGeo Defense asigura conformitate cu:
- Regulamentul (UE) 2024/1689 (Legea AI), art. 10(3)
- GDPR art. 5(1)(d) — principiul acuratetii datelor
- ISO 19157:2013 — calitatea datelor geografice
- Galileo OSNMA SIS ICD v1.1 — autentificare GNSS

{sep}
Generat de SecureGeo Defense Platform | UCB Targu Jiu
Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | APIA CJ Gorj
{sep}"""

            st.download_button(
                "Descarca Raport Securitate TXT",
                data=raport.encode("utf-8"),
                file_name=f"raport_securitate_{date.today().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )

    st.divider()
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1a5276 0%,#117a65 100%);
         border-radius:10px; padding:14px 20px; color:white; font-size:11px;'>
        <b>SecureGeo Defense Platform</b> | Bloc 5 AI Aplicat<br>
        &copy; 2026 Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj<br>
        Baza: [9] Gamulescu, O.-M. (2026). DOI 10.5281/zenodo.19829463 |
        Galileo OSNMA SIS ICD v1.1 (EUSPA, 2023)<br>
        <span style='font-size:10px; opacity:0.8;'>
            Legea nr. 8/1996 — citare obligatorie la orice utilizare a datelor sau metodologiei.
        </span>
    </div>
    """, unsafe_allow_html=True)
