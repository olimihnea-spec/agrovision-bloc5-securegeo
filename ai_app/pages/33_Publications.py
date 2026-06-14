# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(
    page_title="Publications — Gămulescu O.-M.",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Publications")
    st.markdown("**Prof. Asoc. Dr. Oliviu Mihnea Gămulescu**")
    st.markdown("Universitatea Constantin Brâncuși din Târgu Jiu")
    st.markdown("---")
    st.markdown(f"**ORCID:** [0009-0002-3019-3790](https://orcid.org/0009-0002-3019-3790)")
    st.markdown("**Zenodo:** [olimihnea-spec](https://zenodo.org)")
    st.markdown("---")
    st.markdown("**Statistici**")
    st.metric("Articole ISI/BDI", "2")
    st.metric("Pre-înregistrări", "1")
    st.metric("DOI-uri active", "3")

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #0D47A1 0%, #1565C0 60%, #1976D2 100%);
            padding: 2rem 2.5rem; border-radius: 14px; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 2.2rem; font-weight: 800; margin: 0;">
        📚 Publications & Research Output
    </h1>
    <p style="color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 0.5rem;">
        Prof. Asoc. Dr. Oliviu Mihnea Gămulescu &nbsp;|&nbsp;
        Universitatea Constantin Brâncuși din Târgu Jiu &nbsp;|&nbsp;
        APIA Gorj
    </p>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; margin: 0;">
        ORCID: 0009-0002-3019-3790 &nbsp;·&nbsp; Cercetare: GNSS · UAV · Agricultură de precizie
    </p>
</div>
""", unsafe_allow_html=True)

# ── ARTICOL ISI Q1 ────────────────────────────────────────────────────────────
st.markdown("### 🏆 Articole ISI / BDI")
st.markdown("")

st.markdown("""
<div style="background: white; border: 1px solid #e3f2fd; border-left: 6px solid #0D47A1;
            border-radius: 10px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem;">
        <span style="background: #0D47A1; color: white; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem; font-weight: 700;">ISI Q1</span>
        <span style="background: #f3f4f6; color: #374151; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem;">In review</span>
        <span style="background: #fef3c7; color: #92400e; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem;">IF 4.8</span>
    </div>
    <h3 style="color: #0D47A1; font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem 0;">
        GNSS Metadata Integrity in Consumer Smartphones During Commercial Flights:
        GPS Spoofing Artifacts, JPEG Tampering Detection, and Implications for UAV Precision Agriculture
    </h3>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Autori:</strong> Gămulescu O.-M., et al.
    </p>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Revista:</strong> Drones (MDPI) &nbsp;·&nbsp; ISSN 2504-446X &nbsp;·&nbsp; Q1 &nbsp;·&nbsp; IF 4.8
    </p>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Preprint Zenodo:</strong>
        <a href="https://doi.org/10.5281/zenodo.19829463" target="_blank"
           style="color: #1976D2;">doi:10.5281/zenodo.19829463</a>
    </p>
    <p style="color: #546e7a; font-size: 0.88rem; margin-top: 0.8rem;">
        Studiu observațional pe Samsung Galaxy A72 (SM-A725F, Android 13) — 2 zboruri comerciale
        (Buc.–Roma n=377; Buc.–Lisabona n=78) + referință terestră (Cabo da Roca n=275).
        Anomalie EOI: 88% din fișiere (CI 95%: [85.8%–90.1%]). Velocity spikes: 1,560 km/h și 1,875 km/h.
        Phantom geolocation: 0/442 în zbor vs. 37.3% terestru.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: white; border: 1px solid #e8f5e9; border-left: 6px solid #2E7D32;
            border-radius: 10px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem;">
        <span style="background: #2E7D32; color: white; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem; font-weight: 700;">BDI</span>
        <span style="background: #e8f5e9; color: #1B5E20; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem;">Acceptat 25 mai 2026</span>
    </div>
    <h3 style="color: #2E7D32; font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem 0;">
        Agricultural Risk Assessment Using Drone Imagery and AI-Based Analysis
    </h3>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Autori:</strong> Gămulescu O.-M., et al.
    </p>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Revista:</strong> Scientific Papers Series Management, Economic Engineering in Agriculture and Rural Development
        &nbsp;·&nbsp; USAMVB București &nbsp;·&nbsp; PRINT ISSN 2284-7995
    </p>
</div>
""", unsafe_allow_html=True)

# ── PRE-INREGISTRARE ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🔬 Pre-înregistrări (OSF/Zenodo)")
st.markdown("")

st.markdown("""
<div style="background: white; border: 1px solid #ede7f6; border-left: 6px solid #6A1B9A;
            border-radius: 10px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem;">
        <span style="background: #6A1B9A; color: white; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem; font-weight: 700;">Preregistration</span>
        <span style="background: #f3e5f5; color: #4A148C; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem;">Publicat 14 iunie 2026</span>
        <span style="background: #f3f4f6; color: #374151; padding: 0.2rem 0.8rem;
                     border-radius: 20px; font-size: 0.85rem;">CC BY 4.0</span>
    </div>
    <h3 style="color: #6A1B9A; font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem 0;">
        Pre-Registration: GNSS Metadata Integrity in Consumer Smartphones —
        Madeira Field Campaign (June 24–July 1, 2026)
    </h3>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Autor:</strong> Gămulescu, Oliviu-Mihnea
        &nbsp;·&nbsp; Universitatea Constantin Brâncuși din Târgu Jiu
    </p>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>DOI:</strong>
        <a href="https://doi.org/10.5281/zenodo.20687660" target="_blank"
           style="color: #7B1FA2;">doi:10.5281/zenodo.20687660</a>
    </p>
    <p style="color: #374151; font-size: 0.95rem; margin: 0.3rem 0;">
        <strong>Platformă:</strong> Zenodo (CERN) &nbsp;·&nbsp; Version v1
    </p>
    <p style="color: #546e7a; font-size: 0.88rem; margin-top: 0.8rem;">
        Protocol pre-înregistrat pentru campania de teren Madeira: 7 seturi de date planificate
        (zboruri comerciale OTP–FNC–OTP, referință open-sky, profil altitudinal PR1 la 1,818 m,
        obstrucție canopeu Laurisilva, tranziție verticală Cabo Girão). Ipotezele H1–H4
        declarate anterior colectării datelor.
    </p>
</div>
""", unsafe_allow_html=True)

# ── CERCETARE IN DESFASURARE ───────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🚀 Cercetare în desfășurare")
st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #e3f2fd; border-radius: 10px; padding: 1.2rem; text-align: center;">
        <div style="font-size: 2rem;">✈️</div>
        <h4 style="color: #0D47A1; margin: 0.5rem 0 0.3rem 0;">Madeira 2026</h4>
        <p style="color: #374151; font-size: 0.9rem; margin: 0;">
            Campanie teren 24 iun – 1 iul 2026<br>
            EXP-MAD-F1, EXP-ALT, EXP-CANOPY<br>
            <strong>7 experimente planificate</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #e8f5e9; border-radius: 10px; padding: 1.2rem; text-align: center;">
        <div style="font-size: 2rem;">🛰️</div>
        <h4 style="color: #2E7D32; margin: 0.5rem 0 0.3rem 0;">Articol extins</h4>
        <p style="color: #374151; font-size: 0.9rem; margin: 0;">
            Target: GPS Solutions (IF 4.2)<br>
            sau Remote Sensing (IF 5.0+)<br>
            <strong>Multi-zbor, multi-mediu</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #f3e5f5; border-radius: 10px; padding: 1.2rem; text-align: center;">
        <div style="font-size: 2rem;">🌿</div>
        <h4 style="color: #6A1B9A; margin: 0.5rem 0 0.3rem 0;">Laurisilva GPS</h4>
        <p style="color: #374151; font-size: 0.9rem; margin: 0;">
            Phantom geolocation sub canopeu<br>
            Pădure UNESCO Madeira<br>
            <strong>H3: &gt;20% așteptat</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── CITARE APA ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📋 Citare APA")

st.code("""Gămulescu, O.-M. (2026). Pre-Registration: GNSS Metadata Integrity in Consumer
Smartphones — Madeira Field Campaign (June 24–July 1, 2026). Zenodo.
https://doi.org/10.5281/zenodo.20687660""", language="text")

st.markdown("""
<div style="background: #f8f9fa; border-radius: 8px; padding: 1rem 1.5rem; margin-top: 1rem;">
    <p style="color: #546e7a; font-size: 0.88rem; margin: 0;">
        © 2026 Gămulescu, Oliviu-Mihnea &nbsp;·&nbsp;
        Universitatea Constantin Brâncuși din Târgu Jiu &nbsp;·&nbsp;
        ORCID: <a href="https://orcid.org/0009-0002-3019-3790" target="_blank"
        style="color: #1976D2;">0009-0002-3019-3790</a>
    </p>
</div>
""", unsafe_allow_html=True)
