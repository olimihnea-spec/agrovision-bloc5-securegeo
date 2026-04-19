"""
Ziua 14 — Detectie Contururi: Masurare Suprafata Parcele Agricole
Modul 2 (extensie): Computer Vision
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import datetime

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 14 — Detectie Contururi",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🗺️</div>
    <div style='font-size:16px; font-weight:700; color:#1a5276;'>ZIUA 14</div>
    <div style='font-size:11px; color:#666;'>Detectie Contururi & Masurare Suprafata</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 2 — Computer Vision (extensie)")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 14 / 30 zile")
st.sidebar.progress(14 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 14:**
- `cv2.findContours` — detectie contururi
- `cv2.contourArea` — suprafata in pixeli
- `cv2.arcLength` — perimetru
- Conversie pixeli → hectare
- `cv2.putText` — text in interiorul parcelei
- Detectie cultura dupa culoare (HSV)
- Aplicatie APIA: masurare automatizata
""")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🗺️</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1a5276; font-weight:800;'>
            Ziua 14 — Detectie Contururi: Masurare Suprafata Parcele
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 2 — Computer Vision (extensie) &nbsp;|&nbsp;
            cv2.findContours + Arie + Perimetru + Cultura detectata inscrise pe parcela
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px;padding:12px 20px;margin-bottom:16px;'>
<span style='color:#f9e79f;font-size:13px;font-style:italic;'>
"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"<br>
<b style='color:white;'>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | Universitatea din Petrosani, 2024</b>
</span></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTE CULTURI (HSV ranges + metadata)
# ══════════════════════════════════════════════════════════════════════════════
CULTURI_CONFIG = {
    "Grau":             {"bgr": (40, 150, 210), "hsv_low": (15, 60, 100),  "hsv_high": (35, 255, 255), "id_prefix": "GJ-GR"},
    "Floarea-soarelui": {"bgr": (30, 220, 255), "hsv_low": (20, 100, 150), "hsv_high": (35, 255, 255), "id_prefix": "GJ-FS"},
    "Porumb":           {"bgr": (50, 180, 80),  "hsv_low": (40, 60, 80),   "hsv_high": (80, 255, 220), "id_prefix": "GJ-PO"},
    "Lucerna":          {"bgr": (30, 160, 30),  "hsv_low": (38, 80, 40),   "hsv_high": (75, 255, 160), "id_prefix": "GJ-LU"},
    "Fanete":           {"bgr": (60, 90, 130),  "hsv_low": (10, 30, 60),   "hsv_high": (30, 160, 180), "id_prefix": "GJ-FA"},
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCȚII
# ══════════════════════════════════════════════════════════════════════════════

def genereaza_harta_parcele_contur(w=800, h=600, seed=42) -> np.ndarray:
    """
    Genereaza o imagine sintetica cu 5 parcele distincte (culori diferite),
    borduri negre clare intre ele — ideala pentru detectia contururilor.
    """
    np.random.seed(seed)
    img = np.zeros((h, w, 3), dtype=np.uint8)

    parcele = [
        # (poligon_pts, culoare_BGR, cultura)
        (np.array([[10,10],[390,10],[390,290],[10,290]]),
         (40, 150, 210), "Grau"),
        (np.array([[410,10],[790,10],[790,290],[410,290]]),
         (30, 200, 255), "Floarea-soarelui"),
        (np.array([[10,310],[260,310],[260,590],[10,590]]),
         (50, 180, 80),  "Porumb"),
        (np.array([[280,310],[530,310],[530,590],[280,590]]),
         (30, 170, 40),  "Lucerna"),
        (np.array([[550,310],[790,310],[790,590],[550,590]]),
         (60, 90, 130),  "Fanete"),
    ]

    # Deseneaza fiecare parcela cu textura de zgomot natural
    for pts, culoare, _ in parcele:
        mask_tmp = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask_tmp, [pts], 255)
        roi_mask = mask_tmp > 0

        # Aplica culoarea de baza
        for c in range(3):
            img[:, :, c][roi_mask] = culoare[c]

        # Adauga zgomot pentru aspect natural
        noise = np.random.randint(-20, 20, (h, w)).astype(np.int16)
        for c in range(3):
            canal = img[:, :, c].astype(np.int16)
            canal[roi_mask] = np.clip(canal[roi_mask] + noise[roi_mask], 0, 255)
            img[:, :, c] = canal.astype(np.uint8)

    # Borduri negre clare (separator parcele)
    for pts, _, _ in parcele:
        cv2.polylines(img, [pts], True, (0, 0, 0), thickness=4)

    # Zona stresata in Lucerna (galben-brun — simuleaza seceta)
    cv2.ellipse(img, (405, 450), (50, 35), 0, 0, 360, (30, 100, 160), -1)

    return img, parcele


def detecteaza_cultura_din_culoare(roi_bgr: np.ndarray) -> str:
    """Detecteaza cultura dominanta dintr-un ROI pe baza culorii medii (imagini sintetice)."""
    if roi_bgr.size == 0:
        return "Necunoscuta"
    medie_bgr = roi_bgr.mean(axis=(0, 1))
    B, G, R = medie_bgr[0], medie_bgr[1], medie_bgr[2]

    if R > 150 and G > 130 and B < 80:
        return "Floarea-soarelui"
    if G > 140 and R < 120 and B < 100:
        return "Porumb"
    if G > 120 and R > 120 and B < 80:
        return "Grau"
    if G > 100 and R < 80 and B < 80:
        return "Lucerna"
    if R > 80 and G > 70 and B > 40 and R < 160:
        return "Fanete"
    return "Necunoscuta"


def detecteaza_cultura_hsv(roi_bgr: np.ndarray) -> str:
    """
    Detecteaza cultura dominanta din ROI folosind spatiul HSV.
    Potrivit pentru imagini reale (drone / avion / satelit).
    """
    if roi_bgr.size == 0:
        return "Necunoscuta"
    if roi_bgr.ndim == 2:
        return "Necunoscuta"

    roi_hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)
    H = roi_hsv[:, :, 0].mean()   # 0-180 in OpenCV
    S = roi_hsv[:, :, 1].mean()   # 0-255
    V = roi_hsv[:, :, 2].mean()   # 0-255

    # Verde intens, saturat → Porumb / Lucerna
    if 35 <= H <= 85 and S > 60:
        if V > 110:
            return "Porumb"
        return "Lucerna"

    # Galben-verde → Grau (maturizare) / Floarea-soarelui
    if 20 <= H < 40 and S > 40:
        if V > 130:
            return "Floarea-soarelui"
        return "Grau"

    # Verde pal sau albastru-verde → Fanete / pasuni
    if 85 < H <= 130 and S > 25:
        return "Fanete"

    # Brun sau rosiatic → sol / mirisite
    if H < 20 or H > 150:
        if S > 30:
            return "Grau"    # sol deschis / miriste
        return "Fanete"

    # Saturat scazut → sol gol sau teren arid
    if S < 30:
        return "Necunoscuta"

    return "Necunoscuta"


def pixeli_la_hectare(aria_px: float, scala_m_per_px: float) -> float:
    """Converteste aria in pixeli la hectare folosind scala."""
    aria_m2 = aria_px * (scala_m_per_px ** 2)
    return aria_m2 / 10_000.0


def pixeli_la_metri(lungime_px: float, scala_m_per_px: float) -> float:
    return lungime_px * scala_m_per_px


def centru_contur(contur) -> tuple[int, int]:
    """Calculeaza centrul unui contur cu Momente."""
    M = cv2.moments(contur)
    if M["m00"] == 0:
        return (0, 0)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy)


def inscrie_text_parcela(img: np.ndarray, contur, info: dict,
                          culoare_contur=(255, 255, 255),
                          grosime_contur=3,
                          arata_cultura: bool = False) -> np.ndarray:
    """
    Stil Google Earth:
    - Contur alb (sau culoarea aleasa), gros
    - Text alb cu outline negru, fara fundal opac
    - Format: "79,407 sq m\\n1,206 m"
    """
    rezultat = img.copy()
    cv2.drawContours(rezultat, [contur], -1, culoare_contur, grosime_contur)

    cx, cy = centru_contur(contur)
    h_img, w_img = rezultat.shape[:2]

    # Format Google Earth: "79,407 sq m" + "1,206 m"
    aria_m2 = info.get("aria_m2", int(info["aria_ha"] * 10_000))
    perim_m = int(info["perim_m"])
    linii = [
        f"{aria_m2:,} sq m",
        f"{perim_m:,} m",
    ]
    if arata_cultura and info.get("cultura", "Necunoscuta") != "Necunoscuta":
        linii.append(info["cultura"])

    font       = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    grosime    = 1
    line_h     = 22

    # Calculeaza latimea maxima pentru centrare
    largimi = [cv2.getTextSize(l, font, font_scale, grosime)[0][0] for l in linii]
    total_h = line_h * len(linii)

    # Pozitie centrata pe centrul conturului
    y_start = cy - total_h // 2

    for i, linie in enumerate(linii):
        tx = cx - largimi[i] // 2
        ty = y_start + (i + 1) * line_h
        # Clipeaza la marginile imaginii
        tx = max(4, min(tx, w_img - largimi[i] - 4))
        ty = max(line_h, min(ty, h_img - 4))
        # Outline negru (stroke gros)
        cv2.putText(rezultat, linie, (tx, ty),
                    font, font_scale, (0, 0, 0), grosime + 2, cv2.LINE_AA)
        # Text alb deasupra
        cv2.putText(rezultat, linie, (tx, ty),
                    font, font_scale, (255, 255, 255), grosime, cv2.LINE_AA)

    return rezultat


def segmenteaza_kmeans(img_bgr: np.ndarray, k: int = 6) -> np.ndarray:
    """
    Segmenteaza imaginea in k regiuni de culoare similara (K-means).
    Returneaza imaginea segmentata BGR.
    """
    h, w = img_bgr.shape[:2]
    pixels = img_bgr.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, k, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS
    )
    segmentat = centers[labels.flatten()].reshape(h, w, 3).astype(np.uint8)
    return segmentat


def analizeaza_contururi(img_bgr: np.ndarray,
                          scala_m_per_px: float,
                          aria_min_px: int = 2000,
                          id_fermier_prefix: str = "APIA-GJ",
                          mod_real: bool = False,
                          canny_low: int = 30,
                          canny_high: int = 150,
                          metoda: str = "canny",
                          kmeans_k: int = 6,
                          culoare_contur_global=(255, 255, 255),
                          arata_cultura: bool = False) -> tuple:
    """
    Pipeline complet detectie contururi.

    metoda="masca"  — masca non-negra (imagine sintetica, borduri negre)
    metoda="canny"  — Canny edge detection (imagini reale cu linii vizibile)
    metoda="kmeans" — K-means color segmentation (imagini reale fara linii)
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    if metoda == "canny":
        blur   = cv2.GaussianBlur(gray, (5, 5), 0)
        edges  = cv2.Canny(blur, canny_low, canny_high)
        kernel_d = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated  = cv2.dilate(edges, kernel_d, iterations=3)
        # Inversam: interiorul parcelei devine alb
        filled   = cv2.bitwise_not(dilated)
        kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        thresh_clean = cv2.morphologyEx(filled,       cv2.MORPH_CLOSE, kernel_c)
        thresh_clean = cv2.morphologyEx(thresh_clean, cv2.MORPH_OPEN,  kernel_o)

    elif metoda == "kmeans":
        # Segmenteaza in k culori, aplica Canny pe imaginea segmentata
        segm = segmenteaza_kmeans(img_bgr, k=kmeans_k)
        gray_s = cv2.cvtColor(segm, cv2.COLOR_BGR2GRAY)
        edges  = cv2.Canny(gray_s, 10, 50)
        kernel_d = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated  = cv2.dilate(edges, kernel_d, iterations=2)
        filled   = cv2.bitwise_not(dilated)
        kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
        kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        thresh_clean = cv2.morphologyEx(filled,       cv2.MORPH_CLOSE, kernel_c)
        thresh_clean = cv2.morphologyEx(thresh_clean, cv2.MORPH_OPEN,  kernel_o)

    else:  # "masca" — imagine sintetica
        mask = np.any(img_bgr > 25, axis=2).astype(np.uint8) * 255
        kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        thresh_clean = cv2.morphologyEx(mask,        cv2.MORPH_CLOSE, kernel_c)
        thresh_clean = cv2.morphologyEx(thresh_clean, cv2.MORPH_OPEN,  kernel_o)

    contururi, _ = cv2.findContours(thresh_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_rezultat = img_bgr.copy()
    parcele = []
    nr_parcela = 1

    for contur in contururi:
        aria_px = cv2.contourArea(contur)
        if aria_px < aria_min_px:
            continue

        perim_px = cv2.arcLength(contur, True)
        aria_ha  = pixeli_la_hectare(aria_px, scala_m_per_px)
        aria_m2  = int(aria_px * (scala_m_per_px ** 2))
        perim_m  = pixeli_la_metri(perim_px, scala_m_per_px)

        # Detectie cultura din culoarea ROI
        x_b, y_b, w_b, h_b = cv2.boundingRect(contur)
        roi = img_bgr[y_b:y_b+h_b, x_b:x_b+w_b]
        if mod_real or metoda in ("canny", "kmeans"):
            cultura = detecteaza_cultura_hsv(roi)
        else:
            cultura = detecteaza_cultura_din_culoare(roi)

        # ID fermier
        prefix_cultura = {
            "Grau": "GR", "Floarea-soarelui": "FS",
            "Porumb": "PO", "Lucerna": "LU",
            "Fanete": "FA", "Necunoscuta": "XX"
        }.get(cultura, "XX")
        id_parcela = f"{id_fermier_prefix}-{prefix_cultura}-{nr_parcela:03d}"

        info = {
            "id":       id_parcela,
            "cultura":  cultura,
            "aria_ha":  round(aria_ha, 4),
            "aria_m2":  aria_m2,
            "aria_px":  int(aria_px),
            "perim_m":  round(perim_m, 2),
            "perim_px": round(perim_px, 1),
            "centru":   centru_contur(contur),
            "nr":       nr_parcela,
        }

        img_rezultat = inscrie_text_parcela(
            img_rezultat, contur, info,
            culoare_contur=culoare_contur_global,
            grosime_contur=3,
            arata_cultura=arata_cultura,
        )
        parcele.append(info)
        nr_parcela += 1

    return img_rezultat, parcele


# ══════════════════════════════════════════════════════════════════════════════
# INTERFATA
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie",
    "🗺️ Detectie & Masurare",
    "📊 Rezultate & Raport",
    "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Detectia contururilor in imagini agricole")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**Conturul** = curba care uneste punctele cu acelasi nivel de intensitate la marginea
unui obiect dintr-o imagine.

#### Pipeline detectie contururi parcele
```
Imagine drone (color BGR)
    ↓
[1] Grayscale — cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ↓
[2] Blur — cv2.GaussianBlur(gray, (5,5), 0)
    (elimina zgomotul care ar crea contururi false)
    ↓
[3] Threshold — cv2.threshold(blur, 0, 255, THRESH_BINARY_INV + THRESH_OTSU)
    (separa parcela de fundal)
    ↓
[4] Morfologie — cv2.morphologyEx(thresh, MORPH_CLOSE, kernel)
    (inchide gaurile mici din interior)
    ↓
[5] cv2.findContours(thresh, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    (gaseste lista de contururi externe)
    ↓
[6] Filtreaza dupa arie minima (elimina zgomot rezidual)
    ↓
[7] Pentru fiecare contur:
    • cv2.contourArea(contur)   → arie in pixeli
    • cv2.arcLength(contur, True) → perimetru in pixeli
    • arie_ha = arie_px × (m/px)² / 10.000
    • cv2.putText() → inscrie pe imagine
```

#### Conversie pixeli → hectare
Cheia este **scala** imaginii, care depinde de:
- **Altitudinea de zbor** a dronei (ex: 100 m)
- **Rezolutia senzorului** (ex: 4000×3000 px)
- **Field of View** (unghiul obiectivului)

Formula: `1 pixel = (2 × altitudine × tan(FOV/2)) / latime_px`

Exemplu tipic drone agricola la 100m altitudine:
`1 pixel ≈ 0.05 m → 1 px² = 0.0025 m² → 1 ha = 4.000.000 px²`
""")

    with col2:
        st.markdown("""
<div style='background:#e8f4fd; border-radius:10px; padding:14px;
     border-top:4px solid #1a5276;'>
<div style='font-weight:700; color:#1a5276;'>Functii OpenCV cheie</div>
<div style='font-size:11px; color:#333; margin-top:10px; line-height:1.9;'>

<b>cv2.findContours()</b><br>
Parametri RETR:<br>
• RETR_EXTERNAL — doar contururi exterioare<br>
• RETR_TREE — ierarhie completa<br><br>

Parametri CHAIN:<br>
• CHAIN_APPROX_SIMPLE — comprima segm. drepte<br>
• CHAIN_APPROX_NONE — toate punctele<br><br>

<b>cv2.contourArea(cnt)</b><br>
→ arie in pixeli²<br><br>

<b>cv2.arcLength(cnt, closed=True)</b><br>
→ perimetru in pixeli<br><br>

<b>cv2.moments(cnt)</b><br>
→ centru de greutate (cx, cy)<br><br>

<b>cv2.boundingRect(cnt)</b><br>
→ dreptunghi (x, y, w, h)<br><br>

<b>cv2.putText(img, text, org, font, scale, color, thickness)</b><br>
→ scrie text pe imagine
</div></div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f8f5; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #27ae60;'>
<div style='font-weight:700; color:#1e8449;'>Aplicatie APIA</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.6;'>
Imaginile drone → detectie automata contururi →
calcul suprafata per parcela →
comparare cu suprafata declarata in cerere PAC →
<b>flag automat neconformitati</b><br><br>
Aceasta este esenta tezei de doctorat:
automatizarea controlului pe teren prin CV.
</div></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DETECTIE & MASURARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Detectie contururi + Masurare suprafata parcele")

    col_stanga, col_dreapta = st.columns([1, 2])

    with col_stanga:
        st.markdown("**Sursa imagine:**")
        sursa = st.radio(
            "Alege sursa:",
            ["Imagine demo (sintetica)", "Upload imagine proprie"],
            key="sursa_img"
        )

        uploaded = None
        if sursa == "Upload imagine proprie":
            uploaded = st.file_uploader(
                "Incarca imagine parcela (JPG/PNG):",
                type=["jpg", "jpeg", "png", "bmp", "tiff"],
                key="upload_contur"
            )

        st.divider()
        st.markdown("**Parametri scala:**")

        scala_optiune = st.selectbox(
            "Tipul scalei:",
            ["Drone 100m altitudine (0.05 m/px)",
             "Drone 50m altitudine (0.025 m/px)",
             "Drone 200m altitudine (0.10 m/px)",
             "Satelit (10 m/px)",
             "Manual (introdu valoarea)"],
            key="scala_opt"
        )

        scala_map = {
            "Drone 100m altitudine (0.05 m/px)": 0.05,
            "Drone 50m altitudine (0.025 m/px)": 0.025,
            "Drone 200m altitudine (0.10 m/px)": 0.10,
            "Satelit (10 m/px)": 10.0,
        }

        if "Manual" in scala_optiune:
            scala_m_per_px = st.number_input(
                "Scala (metri per pixel):", min_value=0.001, max_value=100.0,
                value=0.05, step=0.005, key="scala_manual"
            )
        else:
            scala_m_per_px = scala_map.get(scala_optiune, 0.05)
            st.metric("Scala activa", f"{scala_m_per_px} m/px")

        st.divider()
        st.markdown("**Metoda detectie:**")
        # Auto-selecteaza metoda
        metoda_default = "Canny (imagine cu linii vizibile)" if uploaded is not None else "Masca non-negru (imagine sintetica)"
        metoda_aleasa = st.selectbox(
            "Algoritm segmentare:",
            [
                "Canny (imagine cu linii vizibile)",
                "K-means (imagine fara linii — segmentare culori)",
                "Masca non-negru (imagine sintetica)",
            ],
            index=0 if uploaded is not None else 2,
            key="metoda_seg"
        )
        metoda_map = {
            "Canny (imagine cu linii vizibile)": "canny",
            "K-means (imagine fara linii — segmentare culori)": "kmeans",
            "Masca non-negru (imagine sintetica)": "masca",
        }
        metoda = metoda_map[metoda_aleasa]
        mod_real = metoda != "masca"

        if metoda == "canny":
            st.markdown("**Parametri Canny:**")
            canny_low  = st.slider("Prag minim:", 5, 100,  30, 5,  key="canny_low")
            canny_high = st.slider("Prag maxim:", 30, 300, 150, 10, key="canny_high")
        else:
            canny_low, canny_high = 30, 150

        kmeans_k = 6
        if metoda == "kmeans":
            kmeans_k = st.slider("Nr. culori K-means:", 3, 12, 6, 1, key="kmeans_k")

        st.divider()
        st.markdown("**Afisare contururi:**")
        culoare_contur_hex = st.color_picker(
            "Culoare contur:", "#FFFFFF", key="culoare_contur"
        )
        # Converteste hex → BGR
        h_col = culoare_contur_hex.lstrip("#")
        r, g, b = int(h_col[0:2], 16), int(h_col[2:4], 16), int(h_col[4:6], 16)
        culoare_contur_bgr = (b, g, r)

        arata_cultura = st.checkbox("Afiseaza cultura pe parcela", value=False, key="arata_cult")

        st.divider()
        st.markdown("**Filtrare contururi:**")
        aria_min_px = st.slider(
            "Arie minima (pixeli):",
            min_value=100, max_value=50000, value=3000, step=500,
            help="Contururi mai mici sunt ignorate (zgomot)",
            key="aria_min"
        )

        id_prefix = st.text_input(
            "Prefix ID fermier:",
            value="APIA-GJ",
            key="id_prefix"
        )

        st.divider()
        ruleaza = st.button("Detecteaza Contururi", type="primary",
                            use_container_width=True, key="btn_detect")

    with col_dreapta:
        if sursa == "Imagine demo (sintetica)":
            img_src, _ = genereaza_harta_parcele_contur()
            st.markdown("**Imagine originala (sintetica — 5 parcele agricole):**")
        elif uploaded is not None:
            file_bytes = np.frombuffer(uploaded.read(), np.uint8)
            img_src = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            st.markdown("**Imagine incarcata:**")
        else:
            img_src, _ = genereaza_harta_parcele_contur()
            st.markdown("**Imagine demo (nicio imagine incarcata):**")

        st.image(img_src[:, :, ::-1], use_container_width=True,
                 caption=f"Dimensiune: {img_src.shape[1]}×{img_src.shape[0]} px")

        if ruleaza:
            with st.spinner("Detectez contururi..."):
                img_rez, parcele_detectate = analizeaza_contururi(
                    img_src, scala_m_per_px, aria_min_px, id_prefix,
                    mod_real=mod_real,
                    canny_low=canny_low,
                    canny_high=canny_high,
                    metoda=metoda,
                    kmeans_k=kmeans_k,
                    culoare_contur_global=culoare_contur_bgr,
                    arata_cultura=arata_cultura,
                )
            st.session_state["img_rezultat"]       = img_rez
            st.session_state["parcele_detectate"]  = parcele_detectate
            st.session_state["scala_m_per_px"]     = scala_m_per_px
            st.session_state["mod_real_folosit"]   = mod_real
            st.session_state["metoda_folosita"]    = metoda
            st.session_state["canny_low"]          = canny_low
            st.session_state["canny_high"]         = canny_high

    # Afiseaza rezultatul sub cele doua coloane
    if ruleaza and "img_rezultat" in st.session_state:
        st.divider()
        st.markdown("### Rezultat — contururi detectate cu informatii inscrise:")

        img_rez    = st.session_state["img_rezultat"]
        parcele_d  = st.session_state["parcele_detectate"]

        st.image(img_rez[:, :, ::-1], use_container_width=True,
                 caption=f"{len(parcele_d)} parcele detectate")

        # Download imagine rezultat
        img_pil = Image.fromarray(img_rez[:, :, ::-1])
        buf = io.BytesIO()
        img_pil.save(buf, format="PNG")
        st.download_button(
            "Descarca imagine cu contururi (PNG)",
            data=buf.getvalue(),
            file_name=f"contururi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )

        # Intermediare diagnostice
        _metoda_f = st.session_state.get("metoda_folosita", "masca")
        with st.expander("Imagini intermediare pipeline"):
            gray_d = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
            c_low  = st.session_state.get("canny_low",  30)
            c_high = st.session_state.get("canny_high", 150)

            if _metoda_f == "canny":
                blur_d  = cv2.GaussianBlur(gray_d, (5, 5), 0)
                edges_d = cv2.Canny(blur_d, c_low, c_high)
                kd_ = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                dil_d  = cv2.dilate(edges_d, kd_, iterations=3)
                fill_d = cv2.bitwise_not(dil_d)
                k_c_   = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
                k_o_   = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
                close_ = cv2.morphologyEx(fill_d, cv2.MORPH_CLOSE, k_c_)
                open_  = cv2.morphologyEx(close_, cv2.MORPH_OPEN,  k_o_)
                viz_cnt = np.ones_like(img_src) * 255
                cnts_viz, _ = cv2.findContours(open_, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(viz_cnt, cnts_viz, -1, (0, 0, 255), 2)
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.image(edges_d, caption="Canny edges", use_container_width=True)
                with c2:
                    st.image(dil_d,   caption="Dilatare + Invert", use_container_width=True)
                with c3:
                    st.image(open_,   caption="Close+Open", use_container_width=True)
                with c4:
                    st.image(viz_cnt, caption="Contururi gasite", use_container_width=True)

            elif _metoda_f == "kmeans":
                segm_d = segmenteaza_kmeans(img_src, k=6)
                gray_s = cv2.cvtColor(segm_d, cv2.COLOR_BGR2GRAY)
                edges_s = cv2.Canny(gray_s, 10, 50)
                kd_ = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                dil_s  = cv2.dilate(edges_s, kd_, iterations=2)
                fill_s = cv2.bitwise_not(dil_s)
                k_c_   = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
                k_o_   = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
                open_s = cv2.morphologyEx(
                    cv2.morphologyEx(fill_s, cv2.MORPH_CLOSE, k_c_),
                    cv2.MORPH_OPEN, k_o_
                )
                viz_cnt = np.ones_like(img_src) * 255
                cnts_viz, _ = cv2.findContours(open_s, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(viz_cnt, cnts_viz, -1, (0, 0, 255), 2)
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.image(segm_d[:,:,::-1], caption="K-means segmentat",
                             use_container_width=True)
                with c2:
                    st.image(edges_s, caption="Canny pe segmentat",
                             use_container_width=True)
                with c3:
                    st.image(open_s,  caption="Close+Open", use_container_width=True)
                with c4:
                    st.image(viz_cnt, caption="Contururi gasite", use_container_width=True)

            else:
                mask_   = np.any(img_src > 25, axis=2).astype(np.uint8) * 255
                k_c_ = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
                close_ = cv2.morphologyEx(mask_, cv2.MORPH_CLOSE, k_c_)
                k_o_ = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                open_  = cv2.morphologyEx(close_, cv2.MORPH_OPEN,  k_o_)
                viz_cnt = np.ones_like(img_src) * 255
                cnts_viz, _ = cv2.findContours(open_, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(viz_cnt, cnts_viz, -1, (0, 0, 255), 2)
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.image(mask_,   caption="Masca non-negra", use_container_width=True)
                with c2:
                    st.image(close_,  caption="Morfologie Close", use_container_width=True)
                with c3:
                    st.image(open_,   caption="Morfologie Open", use_container_width=True)
                with c4:
                    st.image(viz_cnt, caption="Contururi gasite", use_container_width=True)

    elif not ruleaza:
        st.info("Configureaza parametrii si apasa **Detecteaza Contururi**.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REZULTATE & RAPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Tabel rezultate + Raport APIA")

    if "parcele_detectate" not in st.session_state or not st.session_state["parcele_detectate"]:
        st.info("Mergi la tab **Detectie & Masurare** si apasa **Detecteaza Contururi** mai intai.")
    else:
        parcele = st.session_state["parcele_detectate"]
        scala   = st.session_state.get("scala_m_per_px", 0.05)

        import pandas as pd
        df = pd.DataFrame([{
            "Nr.":         p["nr"],
            "ID Parcela":  p["id"],
            "Cultura":     p["cultura"],
            "Aria (sq m)": f"{p.get('aria_m2', int(p['aria_ha']*10000)):,}",
            "Aria (ha)":   p["aria_ha"],
            "Perim. (m)":  f"{int(p['perim_m']):,}",
            "Aria (px²)":  p["aria_px"],
            "Centru":      f"({p['centru'][0]}, {p['centru'][1]})",
        } for p in parcele])

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Metrici sumar
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Parcele detectate", len(parcele))
        with col2:
            st.metric("Suprafata totala", f"{sum(p['aria_ha'] for p in parcele):.3f} ha")
        with col3:
            st.metric("Perimetru total", f"{sum(p['perim_m'] for p in parcele):.1f} m")
        with col4:
            culturi_unice = len(set(p["cultura"] for p in parcele))
            st.metric("Culturi distincte", culturi_unice)

        # Grafic arie per parcela
        if PLOTLY_OK:
            culori_bar = ["#f39c12", "#f1c40f", "#27ae60", "#16a085", "#795548",
                          "#8e44ad", "#2471a3", "#e74c3c"]
            fig_bar = go.Figure(go.Bar(
                x=[p["id"] for p in parcele],
                y=[p["aria_ha"] for p in parcele],
                marker_color=[culori_bar[i % len(culori_bar)] for i in range(len(parcele))],
                text=[f"{p['aria_ha']:.3f} ha<br>{p['cultura']}" for p in parcele],
                textposition="outside",
            ))
            fig_bar.update_layout(
                title="Suprafata per parcela detectata",
                yaxis_title="Suprafata (ha)",
                height=320,
                margin=dict(t=40, b=60),
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Generare raport
        st.divider()
        st.subheader("Raport APIA — detectie automata contururi")

        data_raport = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        linii_raport = [
            "=" * 65,
            "RAPORT DETECTIE AUTOMATA CONTURURI PARCELE AGRICOLE",
            "AGENTIA DE PLATI SI INTERVENTIE PENTRU AGRICULTURA",
            "Centrul Judetean Gorj — Serviciul Control pe Teren",
            "=" * 65,
            f"Data generare:     {data_raport}",
            f"Scala imagine:     {scala} m/pixel",
            f"Parcele detectate: {len(parcele)}",
            f"Suprafata totala:  {sum(p['aria_ha'] for p in parcele):.4f} ha",
            "",
            "-" * 65,
            f"{'Nr.':<5} {'ID Parcela':<22} {'Cultura':<20} {'Aria (ha)':<12} {'Perim.(m)'}",
            "-" * 65,
        ]
        for p in parcele:
            linii_raport.append(
                f"{p['nr']:<5} {p['id']:<22} {p['cultura']:<20} "
                f"{p['aria_ha']:<12.4f} {p['perim_m']:.2f}"
            )
        linii_raport += [
            "-" * 65,
            f"{'TOTAL':<5} {'':<22} {'':<20} "
            f"{sum(p['aria_ha'] for p in parcele):<12.4f}",
            "",
            "=" * 65,
            "REFERINTA ACADEMICA:",
            "  'Contributii privind recunoasterea automata a culturilor",
            "   cu ajutorul unei Drone'",
            "  Prof. Asoc. Dr. Oliviu Mihnea Gamulescu",
            "  Universitatea din Petrosani, 2024",
            "",
            "Inspector: ____________________  Semnatura: ______________",
            "=" * 65,
        ]
        raport_txt = "\n".join(linii_raport)

        col_prev, col_dl = st.columns([3, 1])
        with col_prev:
            st.text_area("Previzualizare raport:", raport_txt, height=320)
        with col_dl:
            st.download_button(
                "Descarca Raport TXT",
                data=raport_txt.encode("utf-8"),
                file_name=f"raport_contururi_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Descarca CSV",
                data=csv_data,
                file_name=f"parcele_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Ce am invatat azi — Ziua 14")

    concepte = [
        ("cv2.findContours()", "Detecteaza contururi externe intr-o imagine binarizata"),
        ("cv2.contourArea()", "Calculeaza aria unui contur in pixeli patrati"),
        ("cv2.arcLength()", "Calculeaza perimetrul unui contur in pixeli"),
        ("cv2.moments()", "Calculeaza centrul de greutate (cx, cy) al unui contur"),
        ("Scala m/px", "Factorul de conversie pixeli → metri, dependent de altitudinea dronei"),
        ("Hectar", "Arie = aria_px × scala² / 10.000 (1 ha = 10.000 m²)"),
        ("cv2.putText()", "Inscrie text direct pe imagine cu font, culoare, grosime"),
        ("cv2.addWeighted()", "Suprapunere semi-transparenta (fundal text lizibil)"),
        ("THRESH_OTSU", "Binarizare automata — gaseste pragul optim fara parametri manuali"),
        ("MORPH_CLOSE", "Inchide gaurile mici din interiorul parcelelor dupa threshold"),
    ]

    for concept, descriere in concepte:
        st.markdown(f"""
<div style='display:flex; gap:12px; padding:8px 14px; margin:4px 0;
     background:#f8f9fa; border-radius:8px; font-size:13px;
     border-left:4px solid #1a5276;'>
<b style='color:#1a5276; min-width:180px; font-family:monospace;'>{concept}</b>
<span style='color:#333;'>{descriere}</span>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Cod minimal — detectie contururi si masurare")
    st.code("""
import cv2
import numpy as np

# Citeste imaginea
img = cv2.imread("parcela_drone.jpg")

# Pipeline preprocesare
gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur  = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blur, 0, 255,
             cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Detectie contururi
contururi, _ = cv2.findContours(thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

# Scala: 1 pixel = 0.05 metri (drone la 100m)
SCALA = 0.05  # m/px

for i, cnt in enumerate(contururi):
    aria_px   = cv2.contourArea(cnt)
    perim_px  = cv2.arcLength(cnt, True)
    aria_ha   = aria_px * (SCALA**2) / 10_000
    perim_m   = perim_px * SCALA

    # Centru de greutate
    M  = cv2.moments(cnt)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Deseneaza conturul
    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)

    # Inscrie informatii
    cv2.putText(img, f"ID: APIA-{i+1:03d}",
                (cx-60, cy-20), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1)
    cv2.putText(img, f"{aria_ha:.3f} ha | {perim_m:.1f} m",
                (cx-60, cy+5), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (100, 255, 100), 1)

cv2.imwrite("rezultat_contururi.jpg", img)
print(f"Total: {len(contururi)} parcele detectate")
""", language="python")

    st.markdown("### Aplicatie in teza de doctorat")
    st.success("""
Aceasta tehnica este direct aplicabila in contextul tezei:
- Imaginea drone este procesat automat
- Fiecare parcela este delimitata si masurata
- Suprafata calculata este comparata cu cea declarata in LPIS/IACS
- Neconformitatile (diferente > 5%) sunt flagate pentru control fizic

Automatizarea acestui proces reduce timpul de inspectie APIA
de la ore la minute per ferma.
""")

    st.markdown("""
---
*Referinta: "Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"
— Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, Universitatea din Petrosani, 2024*
""")
