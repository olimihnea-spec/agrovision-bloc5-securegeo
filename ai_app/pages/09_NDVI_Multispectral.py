"""
ZIUA 9 — Calcul NDVI din Imagini Multispectrale
Modul 2: Computer Vision
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
Teza: Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone
"""

import streamlit as st
import numpy as np
from datetime import date
import io

try:
    import cv2
    CV2_OK = True
except ImportError:
    CV2_OK = False

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 9 — NDVI Multispectral",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🌱</div>
    <div style='font-size:16px; font-weight:700; color:#27ae60;'>ZIUA 9</div>
    <div style='font-size:11px; color:#666;'>NDVI din Imagini Multispectrale</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 2 — Computer Vision")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 9 / 30 zile")
st.sidebar.progress(9/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 9:**
- Benzi spectrale (NIR, Red, Green)
- Formula NDVI
- Calcul pixel cu pixel (numpy)
- Harta de culori NDVI
- Interpretare valori NDVI
- Detectie anomalii / parcele stresate
- NDVI sezonier
""")

if not CV2_OK:
    st.error("OpenCV nu este instalat. Ruleaza: `pip install opencv-python`")
    st.stop()
if not PIL_OK:
    st.error("Pillow nu este instalat. Ruleaza: `pip install Pillow`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🌱</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#27ae60; font-weight:800;'>
            Ziua 9 — Calcul NDVI din Imagini Multispectrale
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 2 — Computer Vision &nbsp;|&nbsp;
            De la benzi NIR + Red la harta de vegetatie si detectia anomaliilor
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#1e8449 0%,#1a5276 100%);
     border-radius:10px; padding:10px 18px; color:white; margin-bottom:12px;
     font-size:12px;'>
    Aceasta este tehnica centrala din teza de doctorat:
    <b>"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"</b>
    &nbsp;|&nbsp; NDVI calculat din imagini multispectrale Parrot Sequoia / Micasense
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "🗺️ Harta NDVI Simulata", "📷 NDVI din Imagine Proprie", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII UTILITARE
# ══════════════════════════════════════════════════════════════════════════════
def calculeaza_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """NDVI = (NIR - Red) / (NIR + Red). Rezultat in [-1, 1]."""
    nir_f = nir.astype(np.float32)
    red_f = red.astype(np.float32)
    suma  = nir_f + red_f
    ndvi  = np.where(suma > 0, (nir_f - red_f) / suma, 0.0)
    return np.clip(ndvi, -1.0, 1.0)

def ndvi_la_culoare(ndvi: np.ndarray) -> np.ndarray:
    """Aplica paleta RdYlGn pe valorile NDVI [-1, 1] → BGR pentru OpenCV.
    Paleta manuala: rosu(seceta) → galben(moderat) → verde(sanatoas).
    Compatibila cu orice versiune OpenCV.
    """
    # Normalizeaza [-1, 1] → [0, 1]
    t = ((ndvi + 1.0) / 2.0).astype(np.float32)
    t = np.clip(t, 0.0, 1.0)

    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)

    # Jumatatea inferioara [0, 0.5]: rosu → galben  (R=255, G creste 0→255, B=0)
    m1 = t < 0.5
    r[m1] = 1.0
    g[m1] = t[m1] * 2.0

    # Jumatatea superioara [0.5, 1]: galben → verde  (R scade 255→0, G=255, B=0)
    m2 = ~m1
    r[m2] = 1.0 - (t[m2] - 0.5) * 2.0
    g[m2] = 1.0

    # Construim BGR (OpenCV)
    bgr = np.stack([
        (b * 255).astype(np.uint8),
        (g * 255).astype(np.uint8),
        (r * 255).astype(np.uint8),
    ], axis=-1)
    return bgr

def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Ce este NDVI?")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **NDVI** (Normalized Difference Vegetation Index) este cel mai utilizat
        indice de vegetatie din teledetectie — calculat din doua benzi spectrale:
        """)

        st.markdown("""
        <div style='background:white; border-radius:12px; padding:20px;
             text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.08);
             margin:12px 0;'>
            <div style='font-size:26px; font-weight:800; color:#27ae60; font-family:serif;'>
                NDVI = (NIR &minus; Red) / (NIR + Red)
            </div>
            <div style='font-size:13px; color:#777; margin-top:8px;'>
                NIR = banda infrarosu apropiat (700-900 nm) &nbsp;|&nbsp;
                Red = banda rosie (620-700 nm)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **De ce functioneaza?**

        Clorofila din plantele sanatoase **absoarbe** lumina rosie (pentru fotosinteza)
        si **reflecta** infrarosul apropiat (structura celulara).
        Plantele stresate sau solul reflecta altfel.

        - Vegetatie sanatoasa: NIR mare, Red mic → NDVI aproape de +1
        - Sol expus: NIR ≈ Red → NDVI ≈ 0
        - Apa: NIR < Red → NDVI negativ
        """)

    with col2:
        st.markdown("### Interpretare valori")
        interpretari = [
            (-1.0, -0.1, "Apa, zapada, nori",          "#1a5276"),
            (-0.1,  0.1, "Sol expus, roca, nisip",      "#d35400"),
            ( 0.1,  0.2, "Sol cu vegetatie rara",       "#e67e22"),
            ( 0.2,  0.35,"Vegetatie stresata, uscata",  "#f39c12"),
            ( 0.35, 0.5, "Pasuni, culturi tinere",      "#f9e79f"),
            ( 0.5,  0.7, "Vegetatie moderata sanatoasa","#abebc6"),
            ( 0.7,  1.0, "Vegetatie densa sanatoasa",   "#1e8449"),
        ]
        for vmin, vmax, label, culoare in interpretari:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:8px; margin:3px 0;
                 font-size:11px;'>
                <div style='background:{culoare}; width:36px; height:18px;
                     border-radius:3px; flex-shrink:0;'></div>
                <div>
                    <b style='color:#333;'>{vmin:+.1f} → {vmax:+.1f}</b>
                    <span style='color:#666;'> {label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Benzi spectrale — ce masoara camera drone")

    benzi = [
        ("Blue",  "450-490 nm", "#3498db",
         "Rar folosita pentru NDVI. Utila pentru indicele de apa (NDWI)"),
        ("Green", "520-600 nm", "#27ae60",
         "GNDVI = (NIR-Green)/(NIR+Green) — mai sensibil la concentratia de clorofila"),
        ("Red",   "620-700 nm", "#e74c3c",
         "Banda principala pentru NDVI. Vegetatia sanatoasa absoarbe fortele"),
        ("Red Edge","705-745 nm","#8e44ad",
         "Banda specifica camerei multispectrale — foarte sensibila la stresul plantelor"),
        ("NIR",   "700-900 nm", "#1a5276",
         "Banda principala pentru NDVI. Vegetatia reflecta mult NIR — structura celulara"),
    ]

    cols_b = st.columns(5)
    for col, (banda, nm, culoare, desc) in zip(cols_b, benzi):
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:12px;
                 border-top:4px solid {culoare}; text-align:center;
                 box-shadow:0 1px 4px rgba(0,0,0,0.07); height:140px;'>
                <div style='font-weight:700; color:{culoare}; font-size:13px;'>{banda}</div>
                <div style='font-size:11px; color:#888; margin:3px 0;'>{nm}</div>
                <div style='font-size:11px; color:#555; margin-top:6px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### NDVI in context APIA")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Utilizari operationale la APIA:**
        - Verificarea culturii declarate (NDVI in iulie identifica porumbul vs grau)
        - Detectia parcelelor neutilizate (NDVI < 0.15 pe o parcela declarata arabil)
        - Estimarea daunelor (seceta, inundatii) — scaderea brusca a NDVI
        - Verificarea suprafetei cultivate vs suprafata declarata

        **Limite importante:**
        - Camera RGB standard nu are banda NIR — necesita camera multispectral
        - Parrot Sequoia, Micasense RedEdge, DJI Zenmuse P1 Multispectral
        - Costul echipamentului: 3.000-15.000 EUR
        - Alternativa gratuita: **Sentinel-2** (rezolutie 10m, la fiecare 5 zile)
        """)
    with col2:
        st.markdown("""
        **De unde obtii benzi multispectrale gratuit:**

        **Sentinel-2** (ESA Copernicus):
        - Banda B04 = Red
        - Banda B08 = NIR
        - Rezolutie 10m/pixel
        - Arhiva gratuita din 2015
        - Descarca prin: Copernicus Data Space, Google Earth Engine

        **Landsat 8/9** (NASA/USGS):
        - Banda B4 = Red
        - Banda B5 = NIR
        - Rezolutie 30m/pixel
        - Descarca din: USGS Earth Explorer (gratuit)
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HARTA NDVI SIMULATA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Harta NDVI simulata — parcele agricole Gorj")
    st.info(
        "Simulam benzile NIR si Red pentru o parcela cu 5 zone de cultura diferite. "
        "Valorile sunt realiste pentru o imagine drone din iulie."
    )

    col_cfg, col_harta = st.columns([1, 2])

    with col_cfg:
        st.markdown("#### Configurare parcele")

        np.random.seed(42)
        SIZE = 400

        ndvi_grau     = st.slider("NDVI Grau (iulie — maturare)",       0.0, 1.0, 0.25, 0.05)
        ndvi_porumb   = st.slider("NDVI Porumb (iulie — maxim)",         0.0, 1.0, 0.82, 0.05)
        ndvi_lucerna  = st.slider("NDVI Lucerna (iulie — cosit recent)", 0.0, 1.0, 0.55, 0.05)
        ndvi_fanete   = st.slider("NDVI Fanete",                         0.0, 1.0, 0.48, 0.05)
        ndvi_sol      = st.slider("NDVI Sol expus / drum",               -0.2, 0.2, 0.05, 0.05)
        zgomot_sigma  = st.slider("Zgomot spatial (sigma)",              0.0, 0.1, 0.03, 0.01)
        prag_anomalie = st.slider("Prag detectie anomalie (NDVI <)",     0.1, 0.5, 0.25, 0.05)

    with col_harta:
        # Construim harta NDVI sintetica
        ndvi_map = np.zeros((SIZE, SIZE), dtype=np.float32)

        # Zone: grau stanga-sus, porumb dreapta-sus,
        #        lucerna stanga-jos, fanete dreapta-jos, sol = banda centrala
        ndvi_map[:180, :180]  = ndvi_grau
        ndvi_map[:180, 220:]  = ndvi_porumb
        ndvi_map[220:, :180]  = ndvi_lucerna
        ndvi_map[220:, 220:]  = ndvi_fanete
        ndvi_map[180:220, :]  = ndvi_sol       # drum / canal

        # Adaugam zgomot gaussian realist
        zgomot = np.random.normal(0, zgomot_sigma, (SIZE, SIZE)).astype(np.float32)
        ndvi_map = np.clip(ndvi_map + zgomot, -1.0, 1.0)

        # Simulam o zona stresata (seceta locala) in parcela de lucerna
        ndvi_map[260:310, 40:120] = np.clip(ndvi_lucerna * 0.4 + zgomot[260:310, 40:120], -1, 1)

        # Simulam un bazin de apa mic
        cv2.circle(
            ndvi_map.view(np.uint8).reshape(SIZE, SIZE) if False else ndvi_map,
            (310, 80), 25, -0.3
        )
        ndvi_map = np.clip(ndvi_map, -1.0, 1.0)

        # Masca anomalii
        masca_anomalie = (ndvi_map < prag_anomalie).astype(np.uint8) * 255

        # Vizualizare
        ndvi_color_bgr = ndvi_la_culoare(ndvi_map)

        # Marcam anomaliile cu contururi rosii
        ndvi_color_marcat = ndvi_color_bgr.copy()
        contours, _ = cv2.findContours(masca_anomalie, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(ndvi_color_marcat, contours, -1, (0, 0, 255), 2)

        # Adaugam etichete zone
        etichete = [
            ((40,  80),  "GRAU"),
            ((240, 80),  "PORUMB"),
            ((40,  300), "LUCERNA"),
            ((240, 300), "FANETE"),
            ((160, 195), "DRUM"),
        ]
        for (x, y), text in etichete:
            cv2.putText(ndvi_color_marcat, text, (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2,
                        cv2.LINE_AA)

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("**Harta NDVI (paleta RdYlGn)**")
            st.image(bgr2rgb(ndvi_color_bgr), use_container_width=True)
        with col_h2:
            st.markdown(f"**Anomalii detectate (NDVI < {prag_anomalie})**")
            st.image(bgr2rgb(ndvi_color_marcat), use_container_width=True)

        st.caption(
            "Verde inchis = vegetatie sanatoasa | Galben = moderata | Rosu = stresata/sol. "
            "Contururile rosii din dreapta = zone sub pragul de anomalie (candidati control APIA)."
        )

        # Statistici NDVI per zona
        st.divider()
        st.markdown("#### Statistici NDVI per zona")
        zone = {
            "Grau":    ndvi_map[:180, :180].flatten(),
            "Porumb":  ndvi_map[:180, 220:].flatten(),
            "Lucerna": ndvi_map[220:, :180].flatten(),
            "Fanete":  ndvi_map[220:, 220:].flatten(),
            "Drum":    ndvi_map[180:220, :].flatten(),
        }
        stat_rows = []
        for zona, vals in zone.items():
            stat_rows.append({
                "Zona":      zona,
                "NDVI mediu": f"{vals.mean():.3f}",
                "NDVI min":   f"{vals.min():.3f}",
                "NDVI max":   f"{vals.max():.3f}",
                "Std Dev":    f"{vals.std():.3f}",
                "% anomalie": f"{(vals < prag_anomalie).mean()*100:.1f}%",
            })
        st.dataframe(stat_rows, use_container_width=True, hide_index=True)

    if PLOTLY_OK:
        st.divider()
        st.markdown("#### Distributia NDVI pe intreaga parcela")
        ndvi_flat = ndvi_map.flatten()

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=ndvi_flat,
            nbinsx=80,
            marker_color="#27ae60",
            name="Distributie NDVI",
            opacity=0.7
        ))
        fig_hist.add_vline(x=prag_anomalie, line_dash="dash", line_color="#e74c3c",
                           annotation_text=f"Prag anomalie={prag_anomalie}",
                           annotation_position="top right")
        fig_hist.update_layout(
            xaxis_title="Valoare NDVI",
            yaxis_title="Nr. pixeli",
            xaxis=dict(range=[-1, 1]),
            height=260,
            margin=dict(t=20, b=40, l=50, r=20),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        n_anomalie = int((ndvi_flat < prag_anomalie).sum())
        pct        = n_anomalie / len(ndvi_flat) * 100
        st.info(
            f"**{n_anomalie:,} pixeli ({pct:.1f}%)** au NDVI sub pragul {prag_anomalie} — "
            f"echivalentul a aproximativ **{n_anomalie * 100 / 1e6:.2f} ha** "
            f"(presupunand rezolutie 10 cm/pixel)."
        )

    # Download harta
    buf_harta = io.BytesIO()
    Image.fromarray(bgr2rgb(ndvi_color_marcat)).save(buf_harta, format="PNG")
    buf_harta.seek(0)
    st.download_button(
        "Descarca harta NDVI cu anomalii (.png)",
        data=buf_harta,
        file_name="harta_ndvi_gorj.png",
        mime="image/png"
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — NDVI DIN IMAGINE PROPRIE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### NDVI aproximativ din imagine RGB")

    st.warning("""
    **Nota importanta:** NDVI real necesita banda NIR (infrarosu apropiat) care nu exista
    pe camerele RGB standard. Din imagine RGB putem calcula un **indice de vegetatie aproximativ**
    folosind canalele vizibile. Rezultatul nu este NDVI real dar este util pentru demonstratie.
    """)

    col_info, col_formule = st.columns(2)
    with col_info:
        st.markdown("""
        **Indici calculabili din RGB:**

        - **ExG** (Excess Green): `2*G - R - B` — cel mai simplu
        - **VARI**: `(G - R) / (G + R - B)` — compensat atmosferic
        - **GLI**: `(2*G - R - B) / (2*G + R + B)` — normalizat
        """)
    with col_formule:
        st.markdown("""
        **Pentru NDVI real din imagini drone ai nevoie de:**
        - Camera multispectral (Parrot Sequoia, Micasense RedEdge)
        - Sau imagini Sentinel-2 descarcate (gratis)
        - Benzile: B04 (Red) + B08 (NIR) din Sentinel-2
        """)

    uploaded_ndvi = st.file_uploader(
        "Incarca o imagine RGB (fotografie teren agricol, parcel, vegetatie)",
        type=["jpg","jpeg","png"], key="uploader_ndvi"
    )

    indice_ales = st.selectbox(
        "Indice de vegetatie",
        ["ExG — Excess Green", "VARI", "GLI", "Canal Verde pur (G)"]
    )
    prag_rgb = st.slider("Prag detectie vegetatie", -1.0, 1.0, 0.1, 0.05,
                         key="prag_rgb")

    if uploaded_ndvi:
        file_bytes = np.frombuffer(uploaded_ndvi.read(), np.uint8)
        img_bgr    = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img_bgr is not None:
            # Redimensionam daca prea mare
            h, w = img_bgr.shape[:2]
            if max(h, w) > 800:
                scala = 800 / max(h, w)
                img_bgr = cv2.resize(img_bgr, (int(w*scala), int(h*scala)))

            img_rgb_arr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
            R = img_rgb_arr[:,:,0] / 255.0
            G = img_rgb_arr[:,:,1] / 255.0
            B = img_rgb_arr[:,:,2] / 255.0

            eps = 1e-6
            if indice_ales.startswith("ExG"):
                indice_map = 2*G - R - B
                indice_map = (indice_map - indice_map.min()) / (indice_map.max() - indice_map.min() + eps) * 2 - 1
            elif indice_ales.startswith("VARI"):
                denom      = G + R - B + eps
                indice_map = np.where(np.abs(denom) > eps, (G - R) / denom, 0.0)
                indice_map = np.clip(indice_map, -1, 1)
            elif indice_ales.startswith("GLI"):
                denom      = 2*G + R + B + eps
                indice_map = (2*G - R - B) / denom
                indice_map = np.clip(indice_map, -1, 1)
            else:
                indice_map = G * 2 - 1   # canal verde normalizat la [-1, 1]

            indice_color_bgr = ndvi_la_culoare(indice_map.astype(np.float32))
            masca_veg        = (indice_map > prag_rgb).astype(np.uint8) * 255
            vegetatie_izolata = cv2.bitwise_and(img_bgr, img_bgr, mask=masca_veg)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("**Original**")
                st.image(bgr2rgb(img_bgr), use_container_width=True)
            with col_b:
                st.markdown(f"**{indice_ales.split('—')[0].strip()} (paleta RdYlGn)**")
                st.image(bgr2rgb(indice_color_bgr), use_container_width=True)
            with col_c:
                st.markdown(f"**Vegetatie izolata (indice > {prag_rgb})**")
                st.image(bgr2rgb(vegetatie_izolata), use_container_width=True)

            # Statistici
            pct_vegetatie = float((indice_map > prag_rgb).mean() * 100)
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Indice mediu",  f"{float(indice_map.mean()):.3f}")
            with c2: st.metric("% vegetatie",   f"{pct_vegetatie:.1f}%")
            with c3: st.metric("Pixeli totali", f"{indice_map.size:,}")

            if PLOTLY_OK:
                fig_h = go.Figure()
                fig_h.add_trace(go.Histogram(
                    x=indice_map.flatten(),
                    nbinsx=60,
                    marker_color="#27ae60",
                    opacity=0.75
                ))
                fig_h.add_vline(x=prag_rgb, line_dash="dash", line_color="#e74c3c",
                                annotation_text=f"Prag={prag_rgb}",
                                annotation_position="top right")
                fig_h.update_layout(
                    xaxis_title=f"Valoare {indice_ales.split('—')[0].strip()}",
                    yaxis_title="Nr. pixeli",
                    height=220,
                    margin=dict(t=10, b=40, l=50, r=20),
                )
                st.plotly_chart(fig_h, use_container_width=True)

            # Download
            buf_out = io.BytesIO()
            Image.fromarray(bgr2rgb(indice_color_bgr)).save(buf_out, format="PNG")
            buf_out.seek(0)
            st.download_button(
                f"Descarca harta {indice_ales.split('—')[0].strip()}",
                data=buf_out,
                file_name="harta_vegetatie.png",
                mime="image/png"
            )
        else:
            st.error("Imaginea nu a putut fi citita.")
    else:
        st.info("Incarca o imagine (fotografie teren, parcel agricola, imagine satelit) pentru a calcula indicele de vegetatie.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 9")

    col1, col2 = st.columns(2)
    concepte = [
        ("NDVI",                  "Normalized Difference Vegetation Index = (NIR-Red)/(NIR+Red)"),
        ("Banda NIR",             "Infrarosu apropiat 700-900nm — vegetatia sanatoasa reflecta mult NIR"),
        ("Banda Red",             "620-700nm — clorofila absoarbe lumina rosie pentru fotosinteza"),
        ("Valori NDVI",           "> 0.5 = vegetatie sanatoasa | ~0 = sol | < 0 = apa"),
        ("numpy vectorizat",      "Calcul NDVI pe intreaga imagine dintr-o data — nu pixel cu pixel in loop"),
        ("np.clip()",             "Limiteaza valorile la intervalul dat: clip(ndvi, -1, 1)"),
        ("cv2.applyColorMap()",   "Aplica paleta de culori pe o imagine grayscale: COLORMAP_RdYlGn"),
        ("cv2.findContours()",    "Detecteaza contururi in imagini binare — folosita pentru anomalii NDVI"),
        ("cv2.inRange()",         "Creeaza masca pentru o gama de valori — selecteaza pixelii anomali"),
        ("ExG / VARI / GLI",      "Indici de vegetatie calculabili din RGB — aproximatii fara NIR"),
        ("Sentinel-2",            "Satelit ESA gratuit — benzile B04+B08 permit NDVI real la 10m/pixel"),
        ("Rezolutie spatiala",    "10 cm/pixel (drona) vs 10 m/pixel (Sentinel-2) — detaliu mult mai mare"),
    ]
    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f0fdf4; border-left:3px solid #27ae60;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#27ae60; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
import numpy as np
import cv2

# 1. Calcul NDVI din doua benzi numpy
# nir, red = array 2D float, valori 0-1 sau 0-255
def calculeaza_ndvi(nir, red):
    nir = nir.astype(np.float32)
    red = red.astype(np.float32)
    suma = nir + red
    ndvi = np.where(suma > 0, (nir - red) / suma, 0.0)
    return np.clip(ndvi, -1.0, 1.0)

# 2. Citire benzi din imagini separate (format GeoTIFF sau PNG)
nir_img = cv2.imread("banda_NIR.png", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
red_img = cv2.imread("banda_Red.png", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
ndvi    = calculeaza_ndvi(nir_img, red_img)

# 3. Vizualizare cu paleta de culori
ndvi_norm  = ((ndvi + 1.0) / 2.0 * 255).astype(np.uint8)
ndvi_color = cv2.applyColorMap(ndvi_norm, cv2.COLORMAP_RdYlGn)
cv2.imwrite("harta_ndvi.png", ndvi_color)

# 4. Detectie anomalii (NDVI < prag)
prag         = 0.25
masca_anomal = (ndvi < prag).astype(np.uint8) * 255
contours, _  = cv2.findContours(masca_anomal, cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(ndvi_color, contours, -1, (0, 0, 255), 2)

# 5. Statistici per zona
print(f"NDVI mediu: {ndvi.mean():.3f}")
print(f"Zone stresate: {(ndvi < prag).mean()*100:.1f}%")
print(f"Zone sanatoase: {(ndvi > 0.5).mean()*100:.1f}%")

# 6. Calcul din Sentinel-2 (band B04 = Red, B08 = NIR)
# Fisierele GeoTIFF se citesc cu rasterio:
# import rasterio
# with rasterio.open("B04.tif") as f: red = f.read(1).astype(float)
# with rasterio.open("B08.tif") as f: nir = f.read(1).astype(float)
""", language="python")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Legatura cu teza de doctorat")
        st.markdown("""
        Calculul NDVI din imagini drone este **contributia centrala**
        din teza: *"Contributii privind recunoasterea automata a culturilor
        cu ajutorul unei Drone"*.

        Fluxul complet implementat in teza:
        1. Zbor drone cu camera Parrot Sequoia (5 benzi)
        2. Generare ortomozaic cu Agisoft Metashape
        3. Calcul NDVI banda cu banda in QGIS sau Python
        4. Clasificare automata culturi din harta NDVI
        5. Validare cu datele LPIS din APIA Gorj

        Aceasta zi reuneste **tot ce ai invatat** pana acum:
        numpy (Ziua 2), OpenCV (Ziua 8), clasificare (Ziua 1).
        """)
    with col_b:
        st.markdown("#### Ziua 10 — ce urmeaza")
        st.markdown("""
        **Detectia anomaliilor in parcele agricole**

        Combinam tot ce am invatat in Modulul 2:
        - NDVI din ziua 9 + OpenCV din ziua 8 + YOLO din ziua 7
        - Detectam automat:
            - Zone cu seceta (NDVI scazut brusc)
            - Zone inundate (NDVI negativ)
            - Culturi declarate incorect
            - Parcele neutilizate (sol expus)
        - Generam un **raport automat** cu zonele suspecte
        - Aplicatie directa pentru **inspectorii APIA**
        """)

    st.success(
        "**Ziua 9 finalizata!** Calcul NDVI pixel cu pixel din benzi multispectrale, "
        "harta de culori, detectia anomaliilor si indici de vegetatie din RGB. "
        "Continua cu **Ziua 10 — Detectia anomaliilor in parcele**."
    )
