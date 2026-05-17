# c_PhantomGeo_Research.py
# Platforma de cercetare: Geolocalizare Fantoma si Integritatea Geodatelor
# Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, UCB Targu Jiu
# Copyright © 2026 Oliviu Mihnea Gamulescu. Toate drepturile rezervate.

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="PhantomGeo Research",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero-box {
    background: linear-gradient(135deg, #0D47A1 0%, #1565C0 40%, #1976D2 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    color: white;
}
.hero-box h1 { font-size: 1.55rem; font-weight: 800; margin: 0 0 0.4rem 0; line-height: 1.3; }
.hero-box p  { font-size: 0.92rem; margin: 0.2rem 0; opacity: 0.88; }
.hero-box .doi { font-size: 0.82rem; opacity: 0.75; margin-top: 0.7rem; }

.contrib-card {
    background: #E3F2FD;
    border-left: 5px solid #1565C0;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0;
    font-size: 0.93rem;
    line-height: 1.5;
}
.fm-card {
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin: 0.4rem 0;
    color: white;
    font-size: 0.88rem;
}
.layer-card {
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    color: white;
    font-size: 0.9rem;
}
.copyright-bar {
    background: #ECEFF1;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.8rem;
    color: #546E7A;
    text-align: center;
    margin-top: 2rem;
    border: 1px solid #CFD8DC;
}
.pgrs-trusted   { color: #2E7D32; font-weight: 700; font-size: 1.2rem; }
.pgrs-cond      { color: #E65100; font-weight: 700; font-size: 1.2rem; }
.pgrs-degraded  { color: #F57F17; font-weight: 700; font-size: 1.2rem; }
.pgrs-phantom   { color: #B71C1C; font-weight: 700; font-size: 1.2rem; }
.kw-chip {
    display: inline-block;
    background: #E3F2FD;
    border: 1px solid #90CAF9;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.8rem;
    margin: 0.2rem;
    color: #1565C0;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <h1>🛰️ Geolocalizare Fantomă și Integritatea Geodatelor de Încredere<br>
  în Ecosistemele Europene de Monitorizare Agricolă Bazate pe AI</h1>
  <p><strong>Phantom Geolocation and Geodata Integrity in European AI-Based Agricultural Monitoring Ecosystems</strong></p>
  <p>Anti-Spoofing · Anti-Tampering · Anti-Sniffing · AGRO-GEO TRUST Framework · PGRS</p>
  <p><strong>Autor:</strong> Prof. Asoc. Dr. Oliviu Mihnea Gămulescu
     &nbsp;|&nbsp; Universitatea „Constantin Brâncuși" din Târgu Jiu, România</p>
  <p class="doi">
    © 2026 Oliviu Mihnea Gămulescu. Toate drepturile rezervate.
    &nbsp;|&nbsp; Platformă: <a href="https://georeferencing-applications.streamlit.app" style="color:#90CAF9">georeferencing-applications.streamlit.app</a>
    &nbsp;|&nbsp; DOI platformă: <a href="https://doi.org/10.5281/zenodo.19829462" style="color:#90CAF9">10.5281/zenodo.19829462</a>
  </p>
</div>
""", unsafe_allow_html=True)

# ── TABS ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Articol & Contribuții",
    "🔬 Experimente GNSS",
    "🏗️ AGRO-GEO TRUST Framework",
    "📊 Calculator PGRS",
    "🔐 Securitate Geospațială",
])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — ARTICOL & CONTRIBUTII
# ════════════════════════════════════════════════════════════════════
with tab1:
    col_abs, col_kw = st.columns([2, 1])

    with col_abs:
        st.subheader("Rezumat")
        st.markdown("""
Integritatea datelor geospațiale reprezintă o condiție fundamentală pentru sistemele de inteligență
artificială fiabile, utilizate în ecosistemele europene moderne de monitorizare agricolă.
Cadrele contemporane care integrează imagini satelitare **Sentinel**, produsele programului **Copernicus**,
misiunile **UAV/drone** și colectarea mobilă **GNSS** se bazează tot mai mult pe coordonatele
încorporate în metadatele EXIF ca dovezi spațiale primare.

Prezentul studiu introduce și definește formal conceptul de **Geolocalizare Fantomă (GF)** — persistența
sau propagarea unor coordonate GNSS anterior valide în metadatele imaginilor după pierderea temporară
a semnalului, generând dovezi geospațiale aparent valide, dar contextual inconsistente.

Prin analiză experimentală independentă în **4 scenarii** geografic diverse (Dubai, Istanbul, Lisabona,
Târgu Jiu), sunt caracterizate **patru moduri de defectare (FM-1—FM-4)** și cuantificate ratele lor de
apariție pe două arhitecturi contrastante de dispozitive mobile.

Studiul propune **Framework-ul AGRO-GEO TRUST** și indicatorul compozit **Phantom Geolocation Risk Score
(PGRS)**. Ratele GF observate variază între **3,6% și 100%** în funcție de experiment și dispozitiv.
        """)

        st.subheader("Abstract (English — for ISI indexing)")
        with st.expander("View English Abstract"):
            st.markdown("""
The integrity of geospatial data constitutes a foundational prerequisite for reliable artificial
intelligence (AI) systems deployed in modern European agricultural monitoring ecosystems. This study
introduces and formally defines the concept of **Phantom Geolocation (PGL)** — the persistence or
propagation of previously valid GNSS coordinates within image metadata following temporary signal loss
or positioning unavailability, generating apparently valid yet contextually inconsistent geospatial
evidence.

Through independent experimental analysis across four geographically diverse scenarios (Dubai, Istanbul,
Lisbon, Târgu Jiu), four primary failure modes (FM-1 through FM-4) are characterised and quantified
across contrasting mobile device architectures (Samsung Galaxy A72 vs. OPPO Reno5 Lite).

The **AGRO-GEO TRUST Framework** (four layers: Geo-Integrity, Metadata Trust, Secure Transmission,
AI Validation) and the **Phantom Geolocation Risk Score (PGRS)** are proposed. Phantom geolocation
rates range from **3.6% to 100%** across experimental contexts. Findings demonstrate alignment
requirements with **EU AI Act Article 10(3)** data quality obligations.
            """)

    with col_kw:
        st.subheader("Cuvinte-cheie")
        keywords = [
            "geolocalizare fantomă", "integritate GNSS", "securitate cibernetică geospațială",
            "AI de încredere", "teledetecție", "UAV / drone", "Copernicus", "Sentinel",
            "anti-spoofing", "metadate EXIF", "agricultură de precizie", "AI Act UE",
            "suveranitate digitală", "PGRS", "AGRO-GEO TRUST",
        ]
        kw_html = "".join(f'<span class="kw-chip">{k}</span>' for k in keywords)
        st.markdown(kw_html, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Referințe cheie")
        st.markdown("""
- Reg. (UE) 2024/1689 — AI Act, Art. 10(3)
- Reg. (UE) 2022/1173 — GSAA / IACS
- Reg. (UE) 2021/2116 — PAC finanțare
- Directiva INSPIRE 2007/2/CE
- ISO 19157:2013 — Data Quality
- EUSPA SIS ICD v1.1 — OSNMA Galileo
- Humphreys et al. 2008 — GPS Spoofing
- Balafoutis et al. 2017 — Precision Agriculture
        """)

    st.divider()
    st.subheader("Definiția Formală a Geolocalizării Fantomă")
    st.markdown("""
<div style="background:linear-gradient(135deg,#0D47A1,#1565C0); color:white;
     border-radius:12px; padding:1.6rem 1.8rem; margin:0.5rem 0 1rem 0;">
  <p style="font-size:0.85rem; opacity:0.8; margin:0 0 0.6rem 0;">
    <strong>Definiție 1 (Geolocalizare Fantomă — GF)</strong> &nbsp;—&nbsp;
    contribuție originală, propusă în cadrul cercetării independente
  </p>
  <p style="font-size:1.0rem; line-height:1.7; margin:0 0 1rem 0;">
    Un eveniment de <strong>Geolocalizare Fantomă</strong> apare când coordonatele
    <strong>(φ, λ, h)</strong> încorporate în metadatele digitale ale imaginii la momentul
    achiziției <strong>t₁</strong> corespund unui fix GNSS obținut la un moment anterior
    <strong>t₀ &lt; t₁</strong>, din cauza pierderii sau indisponibilității semnalului în
    intervalul <strong>[t₀, t₁]</strong>, astfel încât coordonatele încorporate sunt
    inconsistente spațial cu poziția reală de achiziție <strong>(φ*, λ*, h*)</strong>,
    în limitele incertitudinii de măsurare.
  </p>
  <div style="background:rgba(255,255,255,0.15); border-radius:8px;
       padding:0.8rem 1.2rem; font-family:monospace; font-size:1.05rem; text-align:center;">
    <strong>GF(I) = ADEVĂRAT &nbsp; ⟺ &nbsp; ||P<sub>EXIF</sub>(I) − P<sub>actual</sub>(I)|| &gt; ε<sub>GNSS</sub></strong>
  </div>
  <p style="font-size:0.88rem; opacity:0.85; margin:0.8rem 0 0 0;">
    unde <strong>P</strong> desemnează vectorii de poziție și
    <strong>ε<sub>GNSS</sub></strong> reprezintă incertitudinea de poziționare așteptată
    (tipic <strong>3–5 m</strong> pentru receptoare civile L1).
  </p>
</div>
""", unsafe_allow_html=True)

    with st.expander("ℹ️ Interpretare și context"):
        col_def1, col_def2 = st.columns(2)
        with col_def1:
            st.markdown("""
**Variabile:**
- **(φ, λ, h)** — latitudine, longitudine, altitudine din EXIF
- **(φ*, λ*, h*)** — poziția reală la momentul achiziției
- **t₀** — momentul ultimului fix GNSS valid
- **t₁** — momentul achiziției imaginii (t₁ > t₀)
- **ε_GNSS** — incertitudinea standard a receptorului L1 (3–5 m)
- **[t₀, t₁]** — intervalul de pierdere a semnalului
            """)
        with col_def2:
            st.markdown("""
**Ce face GF diferit față de o eroare obișnuită:**
- Nu este o **degradare graduală** a preciziei
- Nu este o **absență** detectabilă a coordonatelor
- Este o coordonată **aparent validă** (trece orice filtru simplu)
- Dar este **contextual falsă** — encode-ează o poziție diferită
- Devine **invizibilă** pentru AI dacă nu se aplică PGRS sau STII

**Exemplu practic (EXP07 Istanbul):**
> Imaginile făcute pe Bosfor au coordonate EXIF = 44.57°N, 26.08°E
> (București) — cu STII max = 127,3 → viteza implicată: 1.273 km/h
            """)

    st.divider()
    st.subheader("1.3 Contribuții Originale")

    contributii = [
        ("FM-1—FM-4", "🔵", "#1565C0",
         "Definirea taxonomică formală a Geolocalizării Fantomă (GF) și a celor patru moduri principale "
         "de defectare: FM-1 (persistența ultimului fix), FM-2 (cluster înghețat), FM-3 (altitudine absentă), "
         "FM-4 (absență indusă de format HEIC/RAW)."),
        ("Experimente", "🟢", "#2E7D32",
         "Cuantificarea experimentală a ratelor GF în scenarii geografic diverse (Dubai, Istanbul, "
         "Lisabona, Târgu Jiu) și arhitecturi de dispozitive contrastante (Samsung Galaxy A72 vs. OPPO Reno5 Lite). "
         "Rate observate: 3,6% — 100%."),
        ("AGRO-GEO TRUST", "🟠", "#E65100",
         "Framework-ul AGRO-GEO TRUST — arhitectură conceptuală pe patru straturi pentru integritatea "
         "datelor geospațiale în sistemele AI agricole: Geo-Integrity Layer, Metadata Trust Layer, "
         "Secure Transmission Layer, AI Validation Layer."),
        ("PGRS", "🟣", "#6A1B9A",
         "Phantom Geolocation Risk Score (PGRS) — indicator compozit original [0–1] pentru evaluarea "
         "fiabilității geodatelor pe baza a 7 sub-indicatori: continuitate GNSS, consistență EXIF, "
         "coerență temporală, validitate altitudine, integritate semnal, model de întrerupere, coerență STII."),
        ("Securitate", "🔴", "#B71C1C",
         "Integrarea dimensiunilor anti-spoofing, anti-tampering și anti-sniffing în contextul monitorizării "
         "agricole, aliniată cerințelor Regulamentului UE 2024/1689 (AI Act), Art. 10(3): date de antrenament "
         "«lipsite de erori și complete, în măsura în care este posibil»."),
    ]

    for tag, emoji, color, text in contributii:
        st.markdown(f"""
<div class="contrib-card" style="border-left-color:{color}; background:{color}11;">
  <strong style="color:{color};">{emoji} [{tag}]</strong><br>
  {text}
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div class="copyright-bar">
  © 2026 <strong>Oliviu Mihnea Gămulescu</strong> — Universitatea „Constantin Brâncuși" din Târgu Jiu.
  Toate drepturile rezervate. Reproducerea parțială sau totală este permisă exclusiv cu citarea sursei.
  <br>Cercetare academică independentă. Nicio dată administrativă instituțională nu a fost utilizată.
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 2 — EXPERIMENTE GNSS
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🔬 Date Experimentale — EXP04, EXP07, EXP10, EXP11")

    df_exp = pd.DataFrame({
        "ID": ["EXP04", "EXP07", "EXP07", "EXP10", "EXP11"],
        "Locație": ["Dubai, EAU", "Istanbul, Turcia", "Istanbul, Turcia",
                    "Lisabona, Portugalia", "Târgu Jiu, România"],
        "Dispozitiv": ["OPPO Reno5 Lite", "OPPO Reno5 Lite", "Samsung A72",
                       "Samsung A72", "Samsung A72"],
        "PGR (%)": [100.0, 84.2, 3.6, 4.7, 15.0],
        "FM primar": ["FM-1, FM-2", "FM-1, FM-2", "FM-1", "FM-1", "FM-1, FM-3"],
        "STII max": [">200", "127,3", "4,2", "3,8", "18,7"],
        "PGRS": [0.11, 0.18, 0.79, 0.81, 0.71],
        "Clasificare PGRS": ["FANTOMĂ", "FANTOMĂ", "CONDIȚIONAT", "CONDIȚIONAT", "CONDIȚIONAT"],
        "Mediu": ["E-1 + E-3", "E-1 + E-2", "E-1 + E-2", "E-1 + E-3", "E-1"],
    })

    st.dataframe(
        df_exp.style.apply(
            lambda row: [
                "background:#FFCDD2" if row["PGR (%)"] > 50
                else "background:#FFF9C4" if row["PGR (%)"] > 10
                else "background:#C8E6C9"
            ] * len(row),
            axis=1
        ),
        use_container_width=True,
        hide_index=True,
    )

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("#### Figura 1 — Rata GF (PGR %) per experiment")
        colors_bar = ["#C62828" if d == "OPPO Reno5 Lite" else "#1565C0" for d in df_exp["Dispozitiv"]]
        labels_bar = [
            f"{row['ID']}<br>{row['Locație']}<br>({row['Dispozitiv'].split()[0]})"
            for _, row in df_exp.iterrows()
        ]
        fig_pgr = go.Figure()
        fig_pgr.add_trace(go.Bar(
            x=labels_bar,
            y=df_exp["PGR (%)"],
            marker_color=colors_bar,
            text=[f"{v}%" for v in df_exp["PGR (%)"]],
            textposition="outside",
            name="PGR (%)",
        ))
        fig_pgr.add_hline(y=50, line_dash="dash", line_color="#FF8F00",
                          annotation_text="Prag atenție 50%", annotation_position="right")
        fig_pgr.add_hline(y=10, line_dash="dot", line_color="#2E7D32",
                          annotation_text="Prag acceptabil 10%", annotation_position="right")
        fig_pgr.update_layout(
            yaxis_title="PGR (%)",
            yaxis_range=[0, 120],
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=20, b=10),
            font_family="Arial",
        )
        fig_pgr.update_xaxes(showgrid=False)
        fig_pgr.update_yaxes(showgrid=True, gridcolor="#EEEEEE")
        st.plotly_chart(fig_pgr, use_container_width=True)

        st.caption(
            "**Figura 1.** Rata geolocalizării fantomă (PGR %) per experiment și dispozitiv. "
            "Roșu = OPPO Reno5 Lite; Albastru = Samsung Galaxy A72. "
            "© 2026 Oliviu Mihnea Gămulescu"
        )

    with col_g2:
        st.markdown("#### Figura 2 — Scoruri PGRS cu zone de clasificare")
        fig_pgrs = go.Figure()
        fig_pgrs.add_hrect(y0=0.85, y1=1.05, fillcolor="#2E7D32", opacity=0.08, line_width=0)
        fig_pgrs.add_hrect(y0=0.65, y1=0.85, fillcolor="#F57F17", opacity=0.10, line_width=0)
        fig_pgrs.add_hrect(y0=0.40, y1=0.65, fillcolor="#FF8F00", opacity=0.08, line_width=0)
        fig_pgrs.add_hrect(y0=0.00, y1=0.40, fillcolor="#B71C1C", opacity=0.08, line_width=0)

        pgrs_colors = ["#B71C1C" if v < 0.40 else "#E65100" if v < 0.65
                       else "#F57F17" if v < 0.85 else "#2E7D32"
                       for v in df_exp["PGRS"]]
        fig_pgrs.add_trace(go.Bar(
            x=labels_bar,
            y=df_exp["PGRS"],
            marker_color=pgrs_colors,
            text=[f"{v:.2f}<br>[{c}]" for v, c in zip(df_exp["PGRS"], df_exp["Clasificare PGRS"])],
            textposition="outside",
        ))
        for y_line, color, label in [
            (0.85, "#2E7D32", "TRUSTED ≥ 0.85"),
            (0.65, "#F57F17", "CONDIȚIONAT ≥ 0.65"),
            (0.40, "#FF8F00", "DEGRADAT ≥ 0.40"),
        ]:
            fig_pgrs.add_hline(y=y_line, line_dash="dash", line_color=color,
                               annotation_text=label, annotation_position="right",
                               line_width=1.5)
        fig_pgrs.update_layout(
            yaxis_title="Scor PGRS [0–1]",
            yaxis_range=[0, 1.15],
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=20, b=10),
        )
        fig_pgrs.update_xaxes(showgrid=False)
        fig_pgrs.update_yaxes(showgrid=True, gridcolor="#EEEEEE")
        st.plotly_chart(fig_pgrs, use_container_width=True)

        st.caption(
            "**Figura 2.** Scoruri PGRS per experiment cu zone de clasificare (verde=TRUSTED, "
            "portocaliu=CONDIȚIONAT, roșu=FANTOMĂ). © 2026 Oliviu Mihnea Gămulescu"
        )

    st.markdown("#### Figura 3 — Corelația PGR vs. PGRS")
    fig_scatter = go.Figure()
    for idx, row in df_exp.iterrows():
        color = "#C62828" if "OPPO" in row["Dispozitiv"] else "#1565C0"
        fig_scatter.add_trace(go.Scatter(
            x=[row["PGR (%)"]],
            y=[row["PGRS"]],
            mode="markers+text",
            marker=dict(color=color, size=16, line=dict(color="white", width=2)),
            text=[f"{row['ID']}<br>({row['Dispozitiv'].split()[0]})"],
            textposition="top right",
            name=row["Dispozitiv"],
            showlegend=(idx <= 1),
        ))
    pgr_arr = np.array(df_exp["PGR (%)"])
    pgrs_arr = np.array(df_exp["PGRS"])
    z = np.polyfit(pgr_arr, pgrs_arr, 1)
    x_line = np.linspace(0, 105, 100)
    fig_scatter.add_trace(go.Scatter(
        x=x_line, y=np.poly1d(z)(x_line),
        mode="lines", line=dict(dash="dash", color="gray", width=1.5),
        name="Tendință liniară",
    ))
    fig_scatter.add_hline(y=0.85, line_dash="dot", line_color="#2E7D32",
                          annotation_text="Prag TRUSTED (0.85)", annotation_position="right")
    r = float(np.corrcoef(pgr_arr, pgrs_arr)[0, 1])
    fig_scatter.add_annotation(
        x=5, y=0.95, text=f"<b>r = {r:.3f}</b>",
        showarrow=False, font=dict(size=13, color="#212121"),
        bgcolor="white", bordercolor="#BDBDBD",
    )
    fig_scatter.update_layout(
        xaxis_title="Rata GF — PGR (%)",
        yaxis_title="Scor PGRS [0–1]",
        xaxis_range=[-5, 112],
        yaxis_range=[0, 1.05],
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(x=0.7, y=0.98),
        margin=dict(t=20, b=20),
        height=420,
    )
    fig_scatter.update_xaxes(showgrid=True, gridcolor="#EEEEEE")
    fig_scatter.update_yaxes(showgrid=True, gridcolor="#EEEEEE")
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption(
        "**Figura 3.** Corelația dintre PGR (%) și scorul PGRS per experiment (r = coeficient Pearson). "
        "© 2026 Oliviu Mihnea Gămulescu"
    )

    st.divider()
    st.subheader("Taxonomia modurilor de defectare (FM-1 — FM-4)")
    st.markdown("#### Figura 4 — Distribuția estimată FM")

    fig_pie = go.Figure(go.Pie(
        labels=["FM-1: Persistență ultim fix", "FM-2: Cluster înghețat",
                "FM-3: Altitudine absentă", "FM-4: Absență format HEIC"],
        values=[45, 30, 15, 10],
        marker_colors=["#1565C0", "#FF8F00", "#2E7D32", "#6A1B9A"],
        hole=0.35,
        textinfo="percent+label",
        pull=[0.04, 0.04, 0.04, 0.04],
    ))
    fig_pie.update_layout(
        margin=dict(t=10, b=10),
        paper_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="h", x=0, y=-0.1),
        height=360,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.caption(
        "**Figura 4.** Distribuția estimată a modurilor de defectare FM-1—FM-4 în setul de date experimental cumulat. "
        "© 2026 Oliviu Mihnea Gămulescu"
    )

    fm_data = [
        ("FM-1", "#1565C0", "Persistența ultimului fix",
         "Receptorul reține ultima poziție GNSS validă după pierderea semnalului. "
         "Coordonate identice apar în imagini temporal și spațial disparate.",
         "Medie — analiză traiectorie sau STII > 1"),
        ("FM-2", "#FF8F00", "Cluster de coordonate înghețate",
         "Imagini consecutive partajează coordonate identice sub-metrice. "
         "Varianța pozițională din secvență este zero.",
         "Ridicată — test varianță statistică"),
        ("FM-3", "#2E7D32", "Altitudine absentă / nivel mării implicit",
         "Câmpul h absent sau setat implicit la 0 m MSL în ciuda terenului variabil. "
         "Detectat în EXP11 (aeronave ușoară la 300—1.200 m AGL).",
         "Ridicată — verificare consistență altitudine față de DTM"),
        ("FM-4", "#6A1B9A", "Absență GPS indusă de format",
         "Formatul HEIC (Samsung A72) elimină metadatele GPS la codificare. "
         "Imagini fără câmpuri GPS la dispozitiv cu capacitate GNSS completă.",
         "Ridicată — audit câmpuri metadate per imagine"),
    ]
    cols_fm = st.columns(2)
    for i, (mode, color, title, desc, detect) in enumerate(fm_data):
        with cols_fm[i % 2]:
            st.markdown(f"""
<div class="fm-card" style="background:{color};">
  <strong>🔹 {mode} — {title}</strong><br><br>
  {desc}<br><br>
  <em>Detectabilitate: {detect}</em>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="copyright-bar">© 2026 Oliviu Mihnea Gămulescu — Date colectate independent, echipamente proprii. Nu se utilizează date instituționale.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 3 — AGRO-GEO TRUST FRAMEWORK
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🏗️ Framework-ul AGRO-GEO TRUST")
    st.markdown("""
Framework-ul AGRO-GEO TRUST este o arhitectură conceptuală pe **patru straturi** pentru asigurarea
integrității datelor geospațiale în sistemele AI de monitorizare agricolă. Este conceput independent
de implementare, aplicabil în sistemele Sentinel, fluxurile UAV și colectarea mobilă GNSS.
    """)

    layers = [
        {
            "nr": "4", "name": "AI VALIDATION LAYER", "color": "#4A148C",
            "icon": "🤖",
            "componente": [
                "Filtrare PGRS ≥ 0,85 pentru seturi de date de antrenament AI",
                "Audit de consistență spațială față de geometria parcelelor LPIS",
                "Reconstrucție traiectorie misiune; imagini inconsistente în carantină",
                "Validare încrucișată Sentinel-2: spectral vs. vizual la (φ, λ)",
                "Lanț de audit complet — conformitate AI Act Art. 12 (evidențe)",
            ],
            "reglementare": "AI Act (UE) 2024/1689, Art. 10(3) + Art. 12",
        },
        {
            "nr": "3", "name": "SECURE TRANSMISSION LAYER", "color": "#BF360C",
            "icon": "🔒",
            "componente": [
                "TLS 1.3 obligatoriu — toate transmisiile de date geospațiale",
                "DTLS 1.3 pentru fluxuri de telemetrie UAV în timp real",
                "Autentificare mutuală: certificate dispozitiv ↔ server",
                "Tunel VPN pentru date sensibile ale parcelelor agricole",
                "Monitorizare anomalii trafic — detectare man-in-the-middle",
                "Endpoint-uri cloud exclusiv în jurisdicția UE (GDPR rezidență date)",
            ],
            "reglementare": "GDPR (UE) 2016/679; NIS2 Directiva (UE) 2022/2555",
        },
        {
            "nr": "2", "name": "METADATA TRUST LAYER", "color": "#1B5E20",
            "icon": "🔏",
            "componente": [
                "Hash SHA-256 al blocului EXIF — calculat imediat post-achiziție",
                "Semnătură digitală eIDAS — cheie privată legată de dispozitiv",
                "Consistență temporală: GPSDateStamp vs. DateTimeOriginal",
                "Logging diferențial al secvențelor de coordonate",
                "Stocare chei în TPM hardware — rezistentă la extracție software",
            ],
            "reglementare": "Reg. eIDAS (UE) 910/2014; ISO 19157:2013",
        },
        {
            "nr": "1", "name": "GEO-INTEGRITY LAYER", "color": "#0D47A1",
            "icon": "🛰️",
            "componente": [
                "Validare multi-constelație: GPS + Galileo + GLONASS + BeiDou",
                "Fix currency check: coordonate > 30 s → semnalizate PHANTOM",
                "Comparare IMU vs. GNSS: detecție deplasări imposibile",
                "RAIM (Receiver Autonomous Integrity Monitoring) — protecție nivel L",
                "OSNMA Galileo: autentificare criptografică mesaje navigație (SIS ICD v1.1)",
            ],
            "reglementare": "EUSPA SIS ICD v1.1 (OSNMA); Reg. (UE) 2021/696 (Space Programme)",
        },
    ]

    for layer in layers:
        with st.expander(
            f"{'▲' if layer['nr']=='4' else '▲'} Stratul {layer['nr']} — {layer['name']} {layer['icon']}",
            expanded=True
        ):
            col_l, col_r = st.columns([2, 1])
            with col_l:
                st.markdown(f"""
<div class="layer-card" style="background:{layer['color']};">
  <strong style="font-size:1.05rem;">{layer['icon']} {layer['name']}</strong><br><br>
  {''.join(f"<div>✔ {c}</div>" for c in layer['componente'])}
</div>""", unsafe_allow_html=True)
            with col_r:
                st.markdown(f"""
**📋 Referință reglementară:**
> {layer['reglementare']}
                """)

    st.divider()
    st.subheader("Diagrama framework-ului (interactivă)")

    fig_fw = go.Figure()
    layer_defs = [
        (0, 1.5, "#0D47A1", "1. GEO-INTEGRITY LAYER",
         "GPS+Galileo+GLONASS+BeiDou | RAIM | OSNMA | IMU | Fix currency"),
        (1.5, 3.0, "#1B5E20", "2. METADATA TRUST LAYER",
         "SHA-256 EXIF | eIDAS semnătură | Consistență temporală | TPM"),
        (3.0, 4.5, "#BF360C", "3. SECURE TRANSMISSION LAYER",
         "TLS 1.3 | DTLS UAV | VPN | Autentificare mutuală | Anti-sniffing"),
        (4.5, 6.0, "#4A148C", "4. AI VALIDATION LAYER",
         "PGRS ≥ 0.85 | Audit LPIS | Sentinel-2 cross-val | Audit lanț AI Act"),
    ]
    for y0, y1, color, title, desc in layer_defs:
        fig_fw.add_shape(type="rect", x0=0, y0=y0, x1=10, y1=y1,
                         fillcolor=color, opacity=0.85, line=dict(color="white", width=3))
        fig_fw.add_annotation(x=5, y=(y0 + y1) / 2 + 0.25, text=f"<b>{title}</b>",
                              showarrow=False, font=dict(color="white", size=13),
                              xanchor="center")
        fig_fw.add_annotation(x=5, y=(y0 + y1) / 2 - 0.25, text=f"<i>{desc}</i>",
                              showarrow=False, font=dict(color="white", size=9.5),
                              xanchor="center")

    for y_arrow in [1.5, 3.0, 4.5]:
        fig_fw.add_annotation(
            x=5, y=y_arrow, ax=5, ay=y_arrow - 0.3,
            xref="x", yref="y", axref="x", ayref="y",
            arrowhead=2, arrowsize=1.5, arrowcolor="#455A64", arrowwidth=2.5,
        )

    fig_fw.update_layout(
        xaxis=dict(visible=False, range=[0, 10]),
        yaxis=dict(visible=False, range=[-0.1, 6.5]),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=430,
        margin=dict(t=10, b=10, l=10, r=10),
        title=dict(text="AGRO-GEO TRUST Framework — Arhitectura pe Patru Straturi",
                   x=0.5, font=dict(size=14)),
    )
    st.plotly_chart(fig_fw, use_container_width=True)
    st.caption("**Figura 5.** Framework-ul AGRO-GEO TRUST — arhitectura conceptuală pe patru straturi. © 2026 Oliviu Mihnea Gămulescu")

    st.markdown('<div class="copyright-bar">© 2026 Oliviu Mihnea Gămulescu — AGRO-GEO TRUST Framework este o contribuție originală protejată prin drept de autor.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 4 — CALCULATOR PGRS
# ════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📊 Calculator interactiv — Phantom Geolocation Risk Score (PGRS)")
    st.markdown("""
**PGRS** este un indicator compozit original [0–1] pentru evaluarea fiabilității geodatelor.
Ajustează cei **7 sub-indicatori** pentru a calcula scorul imaginii tale.

> **Formula:** `PGRS = 0.20·S_CONT + 0.18·S_EXIF + 0.18·S_TIME + 0.15·S_ALT + 0.12·S_SIG + 0.10·S_INT + 0.07·S_CONS`
    """)

    st.info("Fiecare sub-indicator Sᵢ ∈ {0 = absent | 0.5 = parțial | 1.0 = verificat}")

    col_c1, col_c2 = st.columns(2)

    sub_indicators = [
        ("S_CONT", "Continuitate GNSS", "Fix GNSS menținut fără întrerupere pe durata sesiunii", 0.20, "col_c1"),
        ("S_EXIF", "Consistență EXIF", "Toate câmpurile GPS EXIF obligatorii prezente și non-implicite", 0.18, "col_c1"),
        ("S_TIME", "Coerență marcaj temporal", "Marcajul GPS în T_max = 30 s față de marcajul imaginii", 0.18, "col_c1"),
        ("S_ALT", "Validitate altitudine", "GPSAltitude consistentă cu modelul de teren (DTM) ± 200 m", 0.15, "col_c2"),
        ("S_SIG", "Integritate semnal", "PDOP < 2,5 și cel puțin 5 sateliți la momentul achiziției", 0.12, "col_c2"),
        ("S_INT", "Model de întrerupere", "Fără evenimente documentate de pierdere a semnalului în sesiune", 0.10, "col_c2"),
        ("S_CONS", "Coerență spațio-temporală", "STII < 1,0 pentru toate perechile de imagini consecutive", 0.07, "col_c2"),
    ]

    scores = {}
    with col_c1:
        for sym, name, desc, weight, target in sub_indicators:
            if target == "col_c1":
                val = st.select_slider(
                    f"**{sym}** — {name} (w={weight})",
                    options=[0.0, 0.5, 1.0],
                    value=1.0,
                    help=desc,
                    key=f"slider_{sym}"
                )
                scores[sym] = (val, weight)
    with col_c2:
        for sym, name, desc, weight, target in sub_indicators:
            if target == "col_c2":
                val = st.select_slider(
                    f"**{sym}** — {name} (w={weight})",
                    options=[0.0, 0.5, 1.0],
                    value=1.0,
                    help=desc,
                    key=f"slider_{sym}"
                )
                scores[sym] = (val, weight)

    pgrs_total = sum(v * w for v, w in scores.values())

    st.divider()
    col_res1, col_res2, col_res3 = st.columns([1, 2, 1])

    with col_res2:
        st.markdown(f"<h2 style='text-align:center;'>PGRS = <strong>{pgrs_total:.3f}</strong></h2>",
                    unsafe_allow_html=True)

        if pgrs_total >= 0.85:
            cls, cls_color, cls_desc, cls_action = (
                "✅ TRUSTED (DE ÎNCREDERE)", "#2E7D32",
                "Geodatele sunt de încredere ridicată.",
                "Adecvat pentru antrenament AI și analiză automatizată."
            )
        elif pgrs_total >= 0.65:
            cls, cls_color, cls_desc, cls_action = (
                "⚠️ CONDITIONAL (CONDIȚIONAT)", "#E65100",
                "Geodatele necesită verificare suplimentară.",
                "Revizuire manuală recomandată; semnalizat în setul de date."
            )
        elif pgrs_total >= 0.40:
            cls, cls_color, cls_desc, cls_action = (
                "🔶 DEGRADED (DEGRADAT)", "#F57F17",
                "Coordonatele prezintă inconsistențe semnificative.",
                "Exclus din antrenamentul AI; utilizare documentară limitată."
            )
        else:
            cls, cls_color, cls_desc, cls_action = (
                "🚫 PHANTOM (FANTOMĂ)", "#B71C1C",
                "Coordonate false cu mare probabilitate.",
                "Pus în carantină. Nu se utilizează în sisteme AI."
            )

        st.markdown(f"""
<div style="background:{cls_color}; color:white; border-radius:10px;
            padding:1.2rem; text-align:center; margin:0.5rem 0;">
  <h3 style="margin:0;">{cls}</h3>
  <p style="margin:0.4rem 0; opacity:0.9;">{cls_desc}</p>
  <p style="margin:0; font-size:0.88rem; opacity:0.8;">{cls_action}</p>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Contribuția fiecărui sub-indicator la PGRS total")
    contrib_names = [sym for sym, *_ in sub_indicators]
    contrib_vals = [scores[sym][0] * scores[sym][1] for sym in contrib_names]
    contrib_colors = ["#1565C0", "#1976D2", "#1E88E5", "#2E7D32", "#388E3C", "#E65100", "#6A1B9A"]

    fig_contrib = go.Figure(go.Bar(
        x=contrib_names,
        y=contrib_vals,
        marker_color=contrib_colors,
        text=[f"{v:.3f}" for v in contrib_vals],
        textposition="outside",
    ))
    fig_contrib.add_hline(y=sum(contrib_vals), line_dash="dash", line_color="#B71C1C",
                          annotation_text=f"PGRS total = {pgrs_total:.3f}", annotation_position="right")
    fig_contrib.update_layout(
        yaxis_title="Contribuție ponderată la PGRS",
        yaxis_range=[0, max(max(contrib_vals) * 1.3, 0.25)],
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=300,
        margin=dict(t=20, b=10),
    )
    fig_contrib.update_xaxes(showgrid=False)
    fig_contrib.update_yaxes(showgrid=True, gridcolor="#EEEEEE")
    st.plotly_chart(fig_contrib, use_container_width=True)

    st.divider()
    st.markdown("#### Calibrare PGRS pe datele experimentale")
    df_calib = pd.DataFrame({
        "Experiment": ["EXP04 Dubai (OPPO)", "EXP07 Istanbul (OPPO)",
                       "EXP07 Istanbul (Samsung)", "EXP10 Lisabona (Samsung)",
                       "EXP11 Târgu Jiu (Samsung)"],
        "PGRS": [0.11, 0.18, 0.79, 0.81, 0.71],
        "Clasificare": ["FANTOMĂ", "FANTOMĂ", "CONDIȚIONAT", "CONDIȚIONAT", "CONDIȚIONAT"],
        "PGR (%)": [100.0, 84.2, 3.6, 4.7, 15.0],
    })
    st.dataframe(df_calib, use_container_width=True, hide_index=True)

    st.markdown('<div class="copyright-bar">© 2026 Oliviu Mihnea Gămulescu — PGRS este un indicator compozit original, propus în articolul de cercetare. Formula și ponderile sunt protejate prin drept de autor academic.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 5 — SECURITATE GEOSPATIALA
# ════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("🔐 Dimensiuni de Securitate Geospațială")

    sec_tab1, sec_tab2, sec_tab3 = st.tabs([
        "🛡️ GNSS / GPS Anti-Spoofing",
        "🔏 Anti-Tampering",
        "📡 Anti-Sniffing",
    ])

    with sec_tab1:
        st.markdown("""
### GNSS / GPS Anti-Spoofing

**Spoofing-ul GNSS** încearcă să substituie semnalele satelitare reale cu semnale false generate artificial,
mișcând virtual poziția înregistrată, falsificând traseul UAV și alterând coordonatele EXIF.

> *Context agricol:* obiectivul spoofing-ului agricol este falsificarea dovezilor spațiale în datele de
> monitorizare — denaturând utilizarea terenului, prezența culturilor sau limitele parcelelor în
> rezultatele procesate de AI.
        """)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### Mecanism de atac")
            st.markdown("""
1. Atacatorul transmite semnal GPS mai puternic decât sateliții reali
2. Receptorul acceptă semnalul fals (nu există autentificare în GPS L1 clasic)
3. Poziția raportată se mișcă virtual
4. Coordonatele EXIF reflectă poziția falsă
5. AI-ul antrenat pe aceste date moștenește bias-ul spațial
            """)

        with col_s2:
            st.markdown("#### Măsuri de detecție și prevenire")
            masuri = [
                ("Multi-constelație GPS+Galileo+GLONASS+BeiDou",
                 "Spoofing-ul unei singure constellații devine insuficient dacă celelalte rămân autentice"),
                ("OSNMA Galileo (SIS ICD v1.1)",
                 "Autentificare criptografică a mesajelor de navigație — ireproductibilă fără cheile private EUSPA"),
                ("Comparare IMU vs. GNSS",
                 "Salt de poziție > 50 m/s cu zero accelerație IMU = indicator spoofing"),
                ("Analiză STII (Spațio-Temporal Inconsistency Index)",
                 "STII > 1 = traiectorie fizic imposibilă"),
                ("RAIM (Receiver Autonomous Integrity Monitoring)",
                 "Identifică sateliți cu pseudodistanțe inconsistente — semnal substituit"),
                ("Monitorizare C/N₀ RF",
                 "Putere semnal anormal de ridicată față de cer deschis = sursă locală suspectă"),
            ]
            for titlu, desc in masuri:
                st.markdown(f"**✅ {titlu}**")
                st.caption(desc)

        st.divider()
        st.markdown("#### Demo interactiv — Detector salt de poziție imposibil (STII)")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            delta_d = st.number_input("Δd — deplasare coordonate (m)", 0.0, 100000.0, 5000.0, 100.0)
        with col_d2:
            v_max = st.number_input("v_max — viteză max. plauzibilă (km/h)", 1.0, 1000.0, 120.0, 10.0)
        with col_d3:
            delta_t = st.number_input("Δt — interval inter-imagine (s)", 0.1, 300.0, 2.0, 0.1)
        stii = delta_d / (v_max / 3.6 * delta_t) if delta_t > 0 and v_max > 0 else 0
        if stii > 1:
            st.error(f"🚨 STII = {stii:.2f} — TRAIECTORIE FIZIC IMPOSIBILĂ → posibil spoofing sau geolocalizare fantomă!")
        elif stii > 0.7:
            st.warning(f"⚠️ STII = {stii:.2f} — deplasare suspectă, revizuire manuală recomandată")
        else:
            st.success(f"✅ STII = {stii:.2f} — traiectorie plauzibilă")
        st.caption("Formula: STII = Δd / (v_max × Δt). STII > 1 → imposibil fizic la viteza declarată.")

    with sec_tab2:
        st.markdown("""
### Anti-Tampering

**Anti-tampering** în contextul geospațial abordează atât modificarea deliberată post-achiziție a
coordonatelor imaginilor, cât și detectarea defectărilor pasive (FM-1, FM-4) care produc metadate
intern inconsistente.

> *Exemplu:* dacă un fișier imagine este editat după captură (coordonate modificate, timestamp schimbat),
> sau dacă firmware-ul dispozitivului propagă coordonate fantomă, mecanismele anti-tampering
> detectează discrepanța.
        """)

        mecanisme = [
            ("1", "Sigilii de securitate fizice", "#1565C0",
             "Etichetare inviolabilă pe echipamentele de teren, documentând seria misiunii. Ruperea sigiliului = dovadă de acces neautorizat."),
            ("2", "Hash SHA-256 EXIF", "#1976D2",
             "Blocul EXIF este hashed imediat post-achiziție și stocat în fișier sidecar. Orice modificare ulterioară a metadatelor alterează hash-ul."),
            ("3", "Semnătură digitală eIDAS", "#1E88E5",
             "Fișierul imagine este semnat cu cheie privată legată de dispozitiv. Semnătura este verificabilă față de PKI fără a dezvălui cheia privată."),
            ("4", "Secure Boot + verificare software", "#2E7D32",
             "Codul aplicației cameră verificat față de hash-ul de încredere la fiecare lansare. Extensia lanțului Secure Boot."),
            ("5", "Monitorizare integritate firmware", "#388E3C",
             "Hash-ul firmware-ului dispozitivului comparat cu golden hash publicat de producător. Anomalie → potențiala manipulare."),
            ("6", "Anti-debugging / anti-reverse engineering", "#43A047",
             "Verificări de integritate la rulare detectând instrumente de analiză ce ar putea facilita injecția de coordonate."),
            ("7", "TPM hardware pentru chei private", "#E65100",
             "Cheile private pentru semnături digitale stocate în Trusted Platform Module. Rezistente la extracție software."),
            ("8", "Lanț de încredere temporal (hash secvențial)", "#6A1B9A",
             "Hash-ul fiecărei imagini incorporează hash-ul imaginii anterioare (blockchain-like). Inserarea retroactivă devine detectabilă."),
        ]

        cols_tm = st.columns(2)
        for i, (nr, titlu, color, desc) in enumerate(mecanisme):
            with cols_tm[i % 2]:
                st.markdown(f"""
<div style="background:{color}; color:white; border-radius:8px;
     padding:0.8rem 1rem; margin:0.4rem 0; font-size:0.88rem;">
  <strong>#{nr} {titlu}</strong><br>
  {desc}
</div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("#### Demo SHA-256 — Detecție modificare metadate GPS")
        import hashlib, json, datetime

        st.markdown("Completează coordonatele GPS originale:")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            lat_orig = st.number_input("Latitudine originală", value=45.0374823, format="%.7f")
        with col_t2:
            lon_orig = st.number_input("Longitudine originală", value=23.2719841, format="%.7f")
        with col_t3:
            alt_orig = st.number_input("Altitudine originală (m)", value=312.5, format="%.1f")

        meta_orig = {"lat": lat_orig, "lon": lon_orig, "alt": alt_orig,
                     "ts": "2026-03-24T12:14:12Z", "device": "Samsung A72"}
        hash_orig = hashlib.sha256(json.dumps(meta_orig, sort_keys=True).encode()).hexdigest()
        st.code(f"SHA-256 original: {hash_orig}", language=None)

        st.markdown("Simulează o modificare suspectă a coordonatelor:")
        col_t4, col_t5, col_t6 = st.columns(3)
        with col_t4:
            lat_mod = st.number_input("Latitudine modificată", value=lat_orig, format="%.7f", key="lat_mod")
        with col_t5:
            lon_mod = st.number_input("Longitudine modificată", value=lon_orig, format="%.7f", key="lon_mod")
        with col_t6:
            alt_mod = st.number_input("Altitudine modificată (m)", value=alt_orig, format="%.1f", key="alt_mod")

        meta_mod = {"lat": lat_mod, "lon": lon_mod, "alt": alt_mod,
                    "ts": "2026-03-24T12:14:12Z", "device": "Samsung A72"}
        hash_mod = hashlib.sha256(json.dumps(meta_mod, sort_keys=True).encode()).hexdigest()
        st.code(f"SHA-256 modificat: {hash_mod}", language=None)

        if hash_orig == hash_mod:
            st.success("✅ Hash identic — metadatele nu au fost modificate. Integritate confirmată.")
        else:
            st.error("🚨 Hash diferit — TAMPERING DETECTAT! Metadatele GPS au fost modificate.")

    with sec_tab3:
        st.markdown("""
### Anti-Sniffing

**Anti-sniffing** abordează interceptarea neautorizată a datelor geospațiale în cursul transmisiei
de la dispozitivul de achiziție la infrastructura cloud.

> *Context agricol:* coordonatele parcelelor, starea culturilor și traiectoriile UAV pot constitui
> informații comercial sensibile sau relevante pentru securitate națională.
        """)

        df_sniff = pd.DataFrame({
            "Clasă de date": [
                "Coordonate GPS în tranzit",
                "Fișiere imagine cu EXIF",
                "Fluxuri telemetrie UAV",
                "Jetoane de autentificare",
                "Rezultate AI (ieșiri procesare)",
                "Stocare cloud",
            ],
            "Sensibilitate": ["RIDICATĂ", "CRITICĂ", "RIDICATĂ", "CRITICĂ", "MEDIE", "RIDICATĂ"],
            "Risc interceptare": ["Mare", "Critic", "Mare", "Critic", "Mediu", "Ridicat"],
            "Măsură de protecție": [
                "TLS 1.3 + tunel VPN",
                "TLS mutual + criptare end-to-end",
                "DTLS 1.3",
                "JWT scurtă durată + certificate pinning",
                "HTTPS cu HSTS",
                "AES-256 server-side + criptare client-side",
            ],
        })

        def color_sensitivity(val):
            if val == "CRITICĂ":
                return "background-color:#FFCDD2; color:#B71C1C; font-weight:bold"
            elif val == "RIDICATĂ":
                return "background-color:#FFE0B2; color:#E65100; font-weight:bold"
            return "background-color:#FFF9C4; color:#F57F17"

        st.dataframe(
            df_sniff.style.applymap(color_sensitivity, subset=["Sensibilitate"]),
            use_container_width=True, hide_index=True,
        )

        st.divider()
        st.markdown("#### Demo — Comparație date în clar vs. criptate TLS 1.3")
        col_sn1, col_sn2 = st.columns(2)
        with col_sn1:
            st.markdown("**❌ Date în clar (fără criptare)**")
            st.code("""
GET /api/field-data HTTP/1.1
Host: agri-platform.eu

{
  "device_id": "SA72-GORJ-001",
  "lat": 45.0374823,
  "lon": 23.2719841,
  "alt": 312.5,
  "parcel_id": "RO002437918",
  "crop": "grau_toamna",
  "ndvi": 0.72,
  "timestamp": "2026-03-24T12:14:12Z"
}
            """, language="http")
            st.error("🚨 Interceptabil cu orice analizor de trafic (Wireshark, tcpdump)")
        with col_sn2:
            st.markdown("**✅ Date criptate TLS 1.3**")
            st.code("""
Handshake TLS 1.3:
  ClientHello (TLS_AES_256_GCM_SHA384)
  ServerHello + Certificate
  ← mutual authentication ←
  Encrypted Application Data:

[ENCRYPTED - AES-256-GCM]
a9f3c2b1e4d7890a1b2c3d4e5f6789012
3456789abcdef0123456789abcdef0123
[Conținut ilegibil fără cheile sesiunii]
            """, language="text")
            st.success("✅ Date complet opace pentru orice interceptor pe traseul de rețea")

        st.divider()
        st.markdown("#### Conformitate cu suveranitatea digitală europeană")
        col_leg1, col_leg2, col_leg3 = st.columns(3)
        with col_leg1:
            st.markdown("""
**🇪🇺 Directiva INSPIRE (2007/2/CE)**
Standardizare interoperabilitate date geospațiale europene.
Transmisia nesigură poate viola cerințele de rezidență a datelor.
            """)
        with col_leg2:
            st.markdown("""
**🔐 GDPR (UE) 2016/679**
Date de localizare = date personale dacă pot identifica indirect.
Criptarea în tranzit = obligație de securitate Art. 32.
            """)
        with col_leg3:
            st.markdown("""
**🛡️ NIS2 Directiva (UE) 2022/2555**
Platformele de monitorizare agricolă = infrastructură critică.
Măsuri de securitate cibernetică obligatorii pentru operatori.
            """)

    st.markdown('<div class="copyright-bar">© 2026 Oliviu Mihnea Gămulescu — Toate drepturile rezervate. Conținutul acestei platforme reprezintă cercetare academică independentă și este protejat prin drept de autor. Citarea se face cu indicarea sursei: Gămulescu, O.M. (2026). Phantom Geolocation and Geodata Integrity. UCB Târgu Jiu.</div>', unsafe_allow_html=True)
