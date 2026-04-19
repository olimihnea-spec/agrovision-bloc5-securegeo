"""
ZIUA 8 — OpenCV: Bazele Procesarii de Imagini
Modul 2: Computer Vision
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
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
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 8 — OpenCV Bazele",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🖼️</div>
    <div style='font-size:16px; font-weight:700; color:#16a085;'>ZIUA 8</div>
    <div style='font-size:11px; color:#666;'>OpenCV — Procesare Imagini</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 2 — Computer Vision")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 8 / 30 zile")
st.sidebar.progress(8/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 8:**
- OpenCV si BGR vs RGB
- Spatii de culoare
- Redimensionare si rotire
- Histograme
- Filtre (blur, Gaussian)
- Detectie muchii (Canny, Sobel)
- Operatii morfologice
- Threshold si segmentare
""")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🖼️</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#16a085; font-weight:800;'>
            Ziua 8 — OpenCV: Bazele Procesarii de Imagini
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 2 — Computer Vision &nbsp;|&nbsp;
            Operatii fundamentale pe imagini — preprocesare pentru YOLO si analiza drone
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Verificare dependente ──────────────────────────────────────────────────────
if not CV2_OK:
    st.error("OpenCV nu este instalat. Ruleaza: `pip install opencv-python`")
    st.stop()
if not PIL_OK:
    st.error("Pillow nu este instalat. Ruleaza: `pip install Pillow`")
    st.stop()

# ── Upload imagine globala (sus, vizibila in toate tab-urile) ──────────────────
st.markdown("**Incarca o imagine pentru a lucra cu ea in toate tab-urile:**")
uploaded = st.file_uploader("", type=["jpg","jpeg","png"], label_visibility="collapsed")

def imagine_demo():
    """Genereaza o imagine sintetica de 300x300 cu forme colorate (fallback)."""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [34, 139, 34]                              # fond verde (camp)
    cv2.rectangle(img, (20,20),  (130,130), (218,165,32), -1)   # galben (grau)
    cv2.rectangle(img, (150,20), (280,130), (255,140,0),  -1)   # portocaliu (floarea-soarelui)
    cv2.circle(img,   (80,220),   60,       (50,205,50),  -1)   # verde deschis (porumb)
    cv2.circle(img,   (220,220),  60,       (139,69,19),  -1)   # maro (fanete)
    img = cv2.GaussianBlur(img, (5,5), 0)
    return img   # BGR

if uploaded:
    file_bytes = np.frombuffer(uploaded.read(), np.uint8)
    img_bgr    = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img_bgr is None:
        st.error("Imaginea nu a putut fi citita. Incearca alt fisier.")
        img_bgr = imagine_demo()
    st.session_state["img_bgr"] = img_bgr
    h, w = img_bgr.shape[:2]
    st.caption(f"Imagine incarcata: {w} x {h} px, {uploaded.name}")
else:
    if "img_bgr" not in st.session_state:
        st.session_state["img_bgr"] = imagine_demo()
    st.caption("Imaginea demo este generata automat (verde=camp, galben=grau, portocaliu=floarea-soarelui).")

def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def afiseaza_pereche(col1, col2, img1, label1, img2, label2, caption=""):
    with col1:
        st.markdown(f"**{label1}**")
        st.image(bgr2rgb(img1) if img1.ndim == 3 and img1.shape[2] == 3
                 else img1, use_container_width=True)
    with col2:
        st.markdown(f"**{label2}**")
        st.image(bgr2rgb(img2) if img2.ndim == 3 and img2.shape[2] == 3
                 else img2, use_container_width=True)
    if caption:
        st.caption(caption)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "🎨 Culori & Transformari", "🔍 Filtre & Muchii", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Ce este OpenCV?")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **OpenCV** (Open Source Computer Vision Library) este cea mai utilizata
        librarie de procesare a imaginilor — folosita in robotica, medicina,
        automotive, agricultura de precizie si drone.

        - Scrisa in C++ cu binding-uri Python
        - Peste 2500 de algoritmi optimizati
        - Ruleaza pe CPU, GPU (CUDA), ARM (Raspberry Pi, Jetson)
        - Instalare: `pip install opencv-python`

        In contextul **dronelor agricole**, OpenCV este folosit pentru:
        - Preprocesarea imaginilor inainte de YOLO
        - Calculul indicilor de vegetatie (NDVI din benzi multispectrale)
        - Detectia granitelor parcelelor
        - Eliminarea zgomotului din imagini
        """)

    with col2:
        st.markdown("""
        <div style='background:#e8f8f5; border-radius:10px; padding:14px;
             border-top:4px solid #16a085;'>
            <div style='font-weight:700; color:#16a085;'>Atentie: BGR nu RGB!</div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                OpenCV citeste imaginile in format <b>BGR</b>
                (Blue-Green-Red), nu RGB.<br><br>
                Matplotlib si Streamlit asteapta <b>RGB</b>.<br><br>
                Conversia obligatorie:<br>
                <code>img_rgb = cv2.cvtColor(img_bgr,<br>
                &nbsp;&nbsp;cv2.COLOR_BGR2RGB)</code><br><br>
                Aceasta este <b>cea mai frecventa eroare</b>
                a incepatorilor cu OpenCV — imaginile apar
                cu nuante ciudate (rosu apare albastru).
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Spatii de culoare")

    spatii = [
        ("BGR",       "Format implicit OpenCV. Fiecare pixel = (B, G, R), valori 0-255.",
         "#3498db", "cv2.imread() returneaza BGR"),
        ("RGB",       "Format standard (Pillow, Streamlit, Matplotlib). R=rosu, G=verde, B=albastru.",
         "#e74c3c", "cv2.cvtColor(img, cv2.COLOR_BGR2RGB)"),
        ("Grayscale", "O singura canal — intensitate 0 (negru) la 255 (alb). Reduce datele 3x.",
         "#7f8c8d", "cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)"),
        ("HSV",       "Hue (tenta), Saturation (saturatie), Value (luminozitate). Util pentru filtrare culori.",
         "#8e44ad", "cv2.cvtColor(img, cv2.COLOR_BGR2HSV)"),
        ("LAB",       "Perceptual — L=luminozitate, A si B=componente culoare. Uniform pentru ochi uman.",
         "#d35400", "cv2.cvtColor(img, cv2.COLOR_BGR2LAB)"),
    ]

    cols_sp = st.columns(5)
    for col, (nume, desc, culoare, cod) in zip(cols_sp, spatii):
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:12px;
                 border-top:3px solid {culoare}; box-shadow:0 1px 4px rgba(0,0,0,0.06);
                 height:160px; font-size:11px;'>
                <div style='font-weight:700; color:{culoare}; font-size:13px;
                     margin-bottom:4px;'>{nume}</div>
                <div style='color:#555;'>{desc}</div>
                <div style='background:#f8f8f8; border-radius:4px; padding:4px 6px;
                     margin-top:8px; font-family:monospace; font-size:10px;
                     color:#333;'>{cod}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Operatii fundamentale")

    ops = [
        ("Citire imagine",     "cv2.imread('foto.jpg')",
         "Returneaza numpy array BGR sau None daca fisierul nu exista"),
        ("Scriere imagine",    "cv2.imwrite('output.jpg', img)",
         "Salveaza pe disc. Calitate JPEG: cv2.imwrite('f.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])"),
        ("Dimensiune",         "img.shape",
         "Returneaza (inaltime, latime, canale) — atentie: H inainte de W!"),
        ("Redimensionare",     "cv2.resize(img, (latime, inaltime))",
         "Atentie: ordinea e (W, H) in resize, opus lui shape care e (H, W)"),
        ("Rotire 90 grade",    "cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)",
         "Variante: ROTATE_90_COUNTERCLOCKWISE, ROTATE_180"),
        ("Flip",               "cv2.flip(img, 1)",
         "0=vertical, 1=orizontal, -1=ambele — util pentru augmentare dataset"),
        ("Decupare (crop)",    "img[y1:y2, x1:x2]",
         "Slicing numpy direct — img[100:200, 50:150] = zona din imagine"),
        ("Desenare box",       "cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)",
         "Parametri: imagine, colt stanga-sus, colt dreapta-jos, culoare BGR, grosime"),
    ]

    col1, col2 = st.columns(2)
    for i, (op, cod, desc) in enumerate(ops):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f0fdf9; border-left:3px solid #16a085;
                 border-radius:0 8px 8px 0; padding:8px 12px; margin:5px 0;'>
                <div style='font-weight:700; color:#16a085; font-size:12px;'>{op}</div>
                <div style='font-family:monospace; font-size:11px; color:#2c3e50;
                     background:#e8f8f5; padding:3px 6px; border-radius:3px;
                     margin:3px 0;'>{cod}</div>
                <div style='font-size:11px; color:#666;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CULORI & TRANSFORMARI
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    img_bgr = st.session_state["img_bgr"]
    h, w    = img_bgr.shape[:2]

    st.markdown("### Spatii de culoare — comparatie vizuala")

    c1, c2, c3, c4, c5 = st.columns(5)
    spatii_viz = [
        ("BGR (original)",  img_bgr,  True),
        ("Grayscale",       cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY), False),
        ("Canal R",         cv2.split(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))[0], False),
        ("Canal G",         cv2.split(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))[1], False),
        ("Canal B",         cv2.split(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))[2], False),
    ]
    for col, (label, img_s, is_color) in zip([c1,c2,c3,c4,c5], spatii_viz):
        with col:
            st.markdown(f"<div style='text-align:center;font-size:12px;font-weight:600;"
                        f"color:#16a085;'>{label}</div>", unsafe_allow_html=True)
            if is_color:
                st.image(bgr2rgb(img_s), use_container_width=True)
            else:
                st.image(img_s, use_container_width=True)

    st.caption(
        "Canalul G (verde) are cea mai mare valoare pe vegetatie sanatoasa. "
        "Canalul R este util pentru calculul NDVI (reflectanta in rosu). "
        "Grayscale reduce datele de 3x si accelereaza procesarea."
    )

    st.divider()
    st.markdown("### Spatiul HSV — filtrare culori")
    st.markdown("""
    HSV separa **culoarea** (Hue) de **luminozitate** (Value),
    ceea ce il face ideal pentru a izola o culoare indiferent de iluminare.
    Util la detectia vegetatiei (verde) sau a solului expus (maro).
    """)

    col_hsv, col_mask = st.columns(2)
    with col_hsv:
        st.markdown("#### Parametri filtru HSV")
        h_min = st.slider("Hue min (0=rosu, 60=galben, 120=verde)",  0,  179,  35, key="h_min")
        h_max = st.slider("Hue max",                                  0,  179,  85, key="h_max")
        s_min = st.slider("Saturation min",                           0,  255,  40, key="s_min")
        v_min = st.slider("Value (luminozitate) min",                 0,  255,  40, key="v_min")

    with col_mask:
        img_hsv  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        lower    = np.array([h_min, s_min, v_min])
        upper    = np.array([h_max, 255,   255])
        mask     = cv2.inRange(img_hsv, lower, upper)
        rezultat = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)

        c1_, c2_ = st.columns(2)
        with c1_:
            st.markdown("**Masca (alb = selectat)**")
            st.image(mask, use_container_width=True)
        with c2_:
            st.markdown("**Zona selectata**")
            st.image(bgr2rgb(rezultat), use_container_width=True)

    st.caption(
        "Hue 35-85 corespunde culorilor galben-verde — aproximativ vegetatia. "
        "Ajusteaza pragurile pentru a izola o anumita cultura dupa culoare."
    )

    st.divider()
    st.markdown("### Transformari geometrice")

    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        scala_proc = st.slider("Scalare (%)", 25, 200, 100, 25)
        rotire_gr  = st.slider("Rotire (grade)", -180, 180, 0, 15)
        flip_opt   = st.selectbox("Flip", ["Niciunul", "Orizontal", "Vertical", "Ambele"])

    with col_t2:
        img_t = img_bgr.copy()
        if scala_proc != 100:
            nw = max(1, int(w * scala_proc / 100))
            nh = max(1, int(h * scala_proc / 100))
            img_t = cv2.resize(img_t, (nw, nh))

        if rotire_gr != 0:
            ht, wt = img_t.shape[:2]
            M    = cv2.getRotationMatrix2D((wt//2, ht//2), rotire_gr, 1.0)
            img_t = cv2.warpAffine(img_t, M, (wt, ht))

        flip_map = {"Orizontal": 1, "Vertical": 0, "Ambele": -1}
        if flip_opt in flip_map:
            img_t = cv2.flip(img_t, flip_map[flip_opt])

        col_o, col_r = st.columns(2)
        with col_o:
            st.markdown("**Original**")
            st.image(bgr2rgb(img_bgr), use_container_width=True)
            st.caption(f"{w}x{h} px")
        with col_r:
            st.markdown("**Rezultat**")
            st.image(bgr2rgb(img_t), use_container_width=True)
            ht2, wt2 = img_t.shape[:2]
            st.caption(f"{wt2}x{ht2} px")

    st.divider()
    st.markdown("### Histograma — distributia intensitatilor")

    if PLOTLY_OK:
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([img_gray], [0], None, [256], [0,256]).flatten()

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(
            x=list(range(256)), y=hist_gray,
            mode="lines", fill="tozeroy",
            name="Grayscale",
            line=dict(color="#16a085", width=1),
            fillcolor="rgba(22,160,133,0.3)"
        ))

        img_rgb_show = bgr2rgb(img_bgr)
        for canal, culoare, label in [(0,"#e74c3c","R"), (1,"#27ae60","G"), (2,"#3498db","B")]:
            hist_c = cv2.calcHist([img_rgb_show], [canal], None, [256], [0,256]).flatten()
            fig_hist.add_trace(go.Scatter(
                x=list(range(256)), y=hist_c,
                mode="lines", name=label,
                line=dict(color=culoare, width=1.5),
                opacity=0.6
            ))

        fig_hist.update_layout(
            xaxis_title="Intensitate pixel (0-255)",
            yaxis_title="Nr. pixeli",
            height=280,
            margin=dict(t=10, b=40, l=50, r=20),
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption(
            "O histograma concentrata spre stanga = imagine intunecata. "
            "Concentrata spre dreapta = supraexpusa. "
            "Distribuita uniform = contrast bun."
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FILTRE & MUCHII
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    img_bgr = st.session_state["img_bgr"]

    st.markdown("### Filtre de netezire (blur)")

    col_blur_p, col_blur_r = st.columns([1, 2])
    with col_blur_p:
        tip_blur  = st.selectbox("Tip filtru",
                                  ["Gaussian Blur", "Median Blur", "Bilateral Filter"])
        kernel_sz = st.slider("Marime kernel", 1, 31, 5, 2,
                              help="Trebuie sa fie impar. Mai mare = mai mult blur.")
        if tip_blur == "Bilateral Filter":
            sigma_color = st.slider("Sigma Color", 10, 150, 75)
            sigma_space = st.slider("Sigma Space", 10, 150, 75)

    with col_blur_r:
        if tip_blur == "Gaussian Blur":
            k = kernel_sz if kernel_sz % 2 == 1 else kernel_sz + 1
            img_blur = cv2.GaussianBlur(img_bgr, (k, k), 0)
            caption_b = f"Gaussian Blur kernel={k}x{k} — elimina zgomot Gaussian"
        elif tip_blur == "Median Blur":
            k = kernel_sz if kernel_sz % 2 == 1 else kernel_sz + 1
            img_blur = cv2.medianBlur(img_bgr, k)
            caption_b = f"Median Blur kernel={k} — excelent pentru zgomot salt-and-pepper"
        else:
            img_blur = cv2.bilateralFilter(img_bgr, 9, sigma_color, sigma_space)
            caption_b = "Bilateral Filter — netezeste pastrind muchiile clare"

        afiseaza_pereche(
            *st.columns(2),
            img_bgr, "Original",
            img_blur, "Blur aplicat",
            caption_b
        )

    st.divider()
    st.markdown("### Detectie muchii")

    subtab_canny, subtab_sobel = st.tabs(["Canny Edge Detection", "Sobel Gradient"])

    with subtab_canny:
        col_cp, col_cr = st.columns([1, 2])
        with col_cp:
            st.markdown("""
            **Canny** este cel mai popular algoritm de detectie muchii.
            Functioneaza in 4 pasi:
            1. Gaussian blur (reduce zgomot)
            2. Gradient Sobel (intensitate + directie)
            3. Non-maximum suppression
            4. Hysteresis thresholding (2 praguri)
            """)
            canny_t1 = st.slider("Threshold 1 (minim)", 0,  300,  50)
            canny_t2 = st.slider("Threshold 2 (maxim)", 0,  300, 150)
            blur_inainte = st.checkbox("Aplica Gaussian Blur inainte", value=True)

        with col_cr:
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            if blur_inainte:
                img_gray = cv2.GaussianBlur(img_gray, (5,5), 0)
            edges_canny = cv2.Canny(img_gray, canny_t1, canny_t2)

            afiseaza_pereche(
                *st.columns(2),
                img_bgr, "Original",
                edges_canny, "Muchii Canny",
                f"Threshold: {canny_t1} - {canny_t2}. Alb = muchii detectate."
            )

    with subtab_sobel:
        col_sp, col_sr = st.columns([1, 2])
        with col_sp:
            st.markdown("""
            **Sobel** calculeaza gradientul imaginii pe directia X si Y.
            Utila pentru:
            - Detectia granitelor parcelelor (linii orizontale/verticale)
            - Analiza texturii culturilor din imagini drone
            """)
            sobel_ksize = st.select_slider("Kernel Sobel", [1, 3, 5, 7], value=3)
            directie    = st.radio("Directie gradient",
                                   ["X (vertical)", "Y (orizontal)", "Combinat"], horizontal=True)

        with col_sr:
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            img_gray = cv2.GaussianBlur(img_gray, (3,3), 0)

            sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
            sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=sobel_ksize)

            if directie == "X (vertical)":
                rezultat_s = cv2.convertScaleAbs(sobel_x)
                cap_s = "Gradient X — detecteaza muchii verticale"
            elif directie == "Y (orizontal)":
                rezultat_s = cv2.convertScaleAbs(sobel_y)
                cap_s = "Gradient Y — detecteaza muchii orizontale"
            else:
                sx = cv2.convertScaleAbs(sobel_x)
                sy = cv2.convertScaleAbs(sobel_y)
                rezultat_s = cv2.addWeighted(sx, 0.5, sy, 0.5, 0)
                cap_s = "Gradient combinat X+Y — toate muchiile"

            afiseaza_pereche(
                *st.columns(2),
                img_bgr, "Original",
                rezultat_s, f"Sobel {directie}",
                cap_s
            )

    st.divider()
    st.markdown("### Threshold si Segmentare")

    col_th_p, col_th_r = st.columns([1, 2])
    with col_th_p:
        tip_thresh = st.selectbox("Tip threshold",
                                   ["Binary", "Otsu (automat)", "Adaptive (local)"])
        if tip_thresh == "Binary":
            thresh_val = st.slider("Valoare prag", 0, 255, 127)

    with col_th_r:
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        if tip_thresh == "Binary":
            _, img_thresh = cv2.threshold(img_gray, thresh_val, 255,
                                           cv2.THRESH_BINARY)
            cap_t = f"Binary threshold = {thresh_val} — pixeli > {thresh_val} devin albi"
        elif tip_thresh == "Otsu (automat)":
            blur_g = cv2.GaussianBlur(img_gray, (5,5), 0)
            otsu_t, img_thresh = cv2.threshold(
                blur_g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            cap_t = f"Otsu calculeaza automat pragul optim = {otsu_t:.0f}"
        else:
            img_thresh = cv2.adaptiveThreshold(
                img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            cap_t = "Adaptive threshold — prag diferit per zona locala (util la iluminare neuniforma)"

        afiseaza_pereche(
            *st.columns(2),
            img_bgr, "Original",
            img_thresh, f"Threshold: {tip_thresh}",
            cap_t
        )

    st.divider()
    st.markdown("### Operatii morfologice")
    st.caption("Utile pentru curatarea mascelor dupa threshold sau segmentare NDVI")

    col_mp, col_mr = st.columns([1, 2])
    with col_mp:
        op_morf = st.selectbox("Operatie",
                                ["Erosion", "Dilation", "Opening", "Closing"])
        kernel_m = st.slider("Kernel morfologic", 3, 21, 5, 2)
        st.markdown(f"""
        <div style='background:#fef9e7; border-radius:8px; padding:10px;
             border-left:3px solid #f39c12; font-size:11px;'>
            <b>Erosion:</b> erodeaza margini — elimina zgomot mic<br>
            <b>Dilation:</b> umfla obiecte — umple gauri mici<br>
            <b>Opening:</b> Erosion + Dilation — elimina zgomot pastrind forma<br>
            <b>Closing:</b> Dilation + Erosion — umple goluri mici in obiecte
        </div>
        """, unsafe_allow_html=True)

    with col_mr:
        _, img_bin = cv2.threshold(
            cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY), 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        km   = cv2.getStructuringElement(cv2.MORPH_RECT,
                                          (kernel_m, kernel_m))
        ops_map = {
            "Erosion":  cv2.MORPH_ERODE,
            "Dilation": cv2.MORPH_DILATE,
            "Opening":  cv2.MORPH_OPEN,
            "Closing":  cv2.MORPH_CLOSE,
        }
        img_morf = cv2.morphologyEx(img_bin, ops_map[op_morf], km)

        afiseaza_pereche(
            *st.columns(2),
            img_bin, "Binar (Otsu)",
            img_morf, f"Dupa {op_morf}",
            f"Kernel {kernel_m}x{kernel_m}. Alb = obiect, Negru = fundal."
        )

    st.divider()
    st.markdown("### Pipeline complet — preprocesare pentru YOLO")
    if st.button("Aplica pipeline preprocesare completa", type="primary"):
        st.markdown("**Pasii aplicati:**")
        pas_imgs = []

        img1 = img_bgr.copy()
        pas_imgs.append(("1. Original", bgr2rgb(img1)))

        img2 = cv2.GaussianBlur(img1, (5,5), 0)
        pas_imgs.append(("2. Gaussian Blur", bgr2rgb(img2)))

        img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        pas_imgs.append(("3. Grayscale", img3))

        _, img4 = cv2.threshold(img3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        pas_imgs.append(("4. Otsu Threshold", img4))

        km   = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        img5 = cv2.morphologyEx(img4, cv2.MORPH_OPEN, km)
        pas_imgs.append(("5. Morphological Opening", img5))

        img6 = cv2.Canny(img3, 50, 150)
        pas_imgs.append(("6. Canny Edges", img6))

        cols_pipe = st.columns(6)
        for col, (label, img_p) in zip(cols_pipe, pas_imgs):
            with col:
                st.markdown(f"<div style='font-size:10px;font-weight:600;"
                            f"color:#16a085;text-align:center;'>{label}</div>",
                            unsafe_allow_html=True)
                st.image(img_p, use_container_width=True)
        st.success(
            "Pipeline complet aplicat. Imaginea procesata (pasul 5) poate fi "
            "folosita ca masca pentru a ghida YOLO spre zonele de interes."
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 8")

    col1, col2 = st.columns(2)
    concepte = [
        ("BGR vs RGB",            "OpenCV = BGR; Streamlit/Matplotlib = RGB. Converteste intotdeauna cu cvtColor"),
        ("img.shape",             "Returneaza (H, W, C) — inaltime, latime, canale. H inainte de W!"),
        ("cv2.resize()",          "Parametru (W, H) — inversul lui shape. Greseala clasica"),
        ("Spatiu HSV",            "Separa culoarea de luminozitate — ideal pentru filtrare vegetatie"),
        ("cv2.inRange()",         "Creeaza masca binara pentru o gama de culori HSV"),
        ("cv2.GaussianBlur()",    "Filtru de netezire — reduce zgomot inainte de detectia muchiilor"),
        ("cv2.medianBlur()",      "Excelent pentru zgomot salt-and-pepper din imagini drone"),
        ("cv2.Canny()",           "Detectie muchii in 4 pasi: blur, gradient, NMS, hysteresis"),
        ("cv2.Sobel()",           "Gradientul imaginii pe X sau Y — detecteaza muchii directionale"),
        ("cv2.threshold()",       "Segmentare binara — pixeli peste prag = alb, sub prag = negru"),
        ("THRESH_OTSU",           "Calculeaza automat pragul optim din histograma imaginii"),
        ("Morphological ops",     "Erosion/Dilation/Opening/Closing — curata mascele dupa segmentare"),
    ]
    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f0fdf9; border-left:3px solid #16a085;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#16a085; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
import cv2
import numpy as np

# 1. Citire si afisare (Streamlit)
img_bgr = cv2.imread("fotografie.jpg")
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
st.image(img_rgb)

# 2. Spatiu HSV — izoleaza vegetatia verde
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
lower_verde = np.array([35,  40,  40])
upper_verde = np.array([85, 255, 255])
masca_verde = cv2.inRange(img_hsv, lower_verde, upper_verde)
vegetatie   = cv2.bitwise_and(img_bgr, img_bgr, mask=masca_verde)

# 3. Preprocesare pentru YOLO
img_blur  = cv2.GaussianBlur(img_bgr, (5, 5), 0)
img_gray  = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
edges     = cv2.Canny(img_gray, 50, 150)

# 4. Segmentare Otsu
_, img_bin = cv2.threshold(img_gray, 0, 255,
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 5. Curatare morfologica
kernel   = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_curat = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)

# 6. Salvare rezultat
cv2.imwrite("output.jpg", img_bgr)
""", language="python")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Aplicatie in analiza drone agricole")
        st.markdown("""
        In fluxul de lucru al tezei de doctorat, OpenCV este folosit
        **inainte** de YOLO pentru:

        - **Calibrarea** imaginilor din camera drone
        - **Corectia** distorsiunilor optice (undistort)
        - **Normalizarea** luminozitatii intre zboruri diferite
        - **Segmentarea** aproximativa a parcelelor (threshold + morfologie)
        - **Calculul NDVI** din benzile rosu si NIR (infrarosu apropiat)

        Ziua 9 aprofundeaza exact calculul NDVI din imagini multispectrale.
        """)
    with col_b:
        st.markdown("#### Ziua 9 — ce urmeaza")
        st.markdown("""
        **Calcul NDVI din imagini multispectrale**

        - Ce este NDVI si de ce conteaza la APIA
        - Imagini multispectrale (bande NIR, Red, Green)
        - Formula: NDVI = (NIR - Red) / (NIR + Red)
        - Calculul pixelul cu pixelul cu numpy
        - Harta de culori NDVI (verde=sanatoas, rosu=stress)
        - Detectia anomaliilor din harta NDVI
        """)

    st.success(
        "**Ziua 8 finalizata!** OpenCV bazele — spatii de culoare, filtre, "
        "detectie muchii, threshold si operatii morfologice. "
        "Continua cu **Ziua 9 — Calcul NDVI din imagini multispectrale**."
    )
