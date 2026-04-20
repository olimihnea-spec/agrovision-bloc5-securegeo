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

try:
    from skimage.segmentation import slic, watershed, find_boundaries
    from skimage.color import rgb2lab
    from skimage.feature import peak_local_max
    from scipy import ndimage as ndi
    SKIMAGE_OK = True
except ImportError:
    SKIMAGE_OK = False

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
    """Converteste aria in pixeli la hectare folosind GSD."""
    aria_m2 = aria_px * (scala_m_per_px ** 2)
    return aria_m2 / 10_000.0


def pixeli_la_metri(lungime_px: float, scala_m_per_px: float) -> float:
    return lungime_px * scala_m_per_px


def calculeaza_gsd(altitudine_m: float, focal_mm: float,
                   sensor_w_mm: float, img_w_px: int) -> float:
    """
    Calculeaza GSD (Ground Sampling Distance) = metri / pixel.

    Formula: GSD = (altitudine × sensor_w) / (focal × img_w)

    Parametri tipici:
    - Drone DJI Phantom 4: focal=8.8mm, sensor=13.2×8.8mm, 4000px → GSD@100m = 3.3 cm/px
    - Telefon (zbor avion ~11500m): focal_eq=26mm, sensor=6.17mm, 4032px → GSD ≈ 27 m/px
    - Satelit Sentinel-2: 10 m/px (direct)
    """
    if focal_mm <= 0 or sensor_w_mm <= 0 or img_w_px <= 0:
        return 0.0
    return (altitudine_m * sensor_w_mm) / (focal_mm * img_w_px)


def calculeaza_metrici_exacte(contur, gsd_m_per_px: float) -> dict:
    """
    Calculeaza aria si perimetrul EXACT folosind OpenCV si GSD cunoscut.

    - cv2.contourArea() returneaza aria EXACTA in pixeli (algoritm Shoelace/Green)
    - cv2.arcLength() returneaza perimetrul EXACT in pixeli (suma segmente)
    - Eroarea de conversie depinde exclusiv de acuratetea GSD-ului
    """
    aria_px2   = cv2.contourArea(contur)
    perim_px   = cv2.arcLength(contur, True)
    aria_m2    = aria_px2 * (gsd_m_per_px ** 2)
    aria_ha    = aria_m2 / 10_000.0
    perim_m    = perim_px * gsd_m_per_px
    # Compactitate: 1.0 = cerc perfect, 0 = forma foarte alungita
    compactitate = (4 * np.pi * aria_px2) / (perim_px ** 2) if perim_px > 0 else 0.0
    return {
        "aria_px2":     round(aria_px2, 1),
        "perim_px":     round(perim_px, 1),
        "aria_m2":      int(aria_m2),
        "aria_ha":      round(aria_ha, 4),
        "perim_m":      round(perim_m, 1),
        "compactitate": round(compactitate, 3),
    }


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
                          metoda: str = "hsv",
                          kmeans_k: int = 6,
                          alb_prag: int = 180,
                          culoare_contur_global=(255, 255, 255),
                          arata_cultura: bool = False,
                          masca_compas: bool = True,
                          masca_minimap: bool = True,
                          masca_text_ui: bool = True) -> tuple:
    """
    Pipeline complet detectie contururi.

    metoda="hsv"        — segmentare HSV vegetatie/sol/padure (RECOMANDAT imagini reale)
    metoda="linii_albe" — prag pixeli albi (Google Earth / QGIS cu linii trasate)
    metoda="canny"      — Canny edge detection
    metoda="kmeans"     — K-means color segmentation
    metoda="masca"      — masca non-negra (imagine sintetica, borduri negre)
    """
    h_img, w_img = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    if metoda == "hsv":
        # Segmentare HSV vegetatie/sol/padure — algoritm specializat imagini agricole
        thresh_clean = segmenteaza_hsv_agricol(
            img_bgr,
            masca_compas=masca_compas,
            masca_minimap=masca_minimap,
            masca_text=masca_text_ui,
        )

    elif metoda == "linii_albe":
        # Detecteaza pixeli albi/deschisi = liniile trasate (Google Earth, QGIS)
        # inRange: toti cei 3 canali BGR > alb_prag → linia este detectata
        lower = np.array([alb_prag, alb_prag, alb_prag], dtype=np.uint8)
        upper = np.array([255, 255, 255], dtype=np.uint8)
        white_mask = cv2.inRange(img_bgr, lower, upper)
        # Dilateaza liniile ca sa inchida micile intreruperi
        kernel_d = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated  = cv2.dilate(white_mask, kernel_d, iterations=2)
        # Inversam: interiorul parcelei devine alb
        filled   = cv2.bitwise_not(dilated)
        # Close: inchide gauri mici din interior
        # Open: elimina zgomot mic (text labels etc.)
        kc_sz = max(9, h_img // 80)
        ko_sz = max(5, h_img // 120)
        kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT, (kc_sz, kc_sz))
        kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT, (ko_sz, ko_sz))
        thresh_clean = cv2.morphologyEx(filled,       cv2.MORPH_CLOSE, kernel_c)
        thresh_clean = cv2.morphologyEx(thresh_clean, cv2.MORPH_OPEN,  kernel_o)

    elif metoda == "canny":
        blur   = cv2.GaussianBlur(gray, (5, 5), 0)
        edges  = cv2.Canny(blur, canny_low, canny_high)
        kernel_d = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated  = cv2.dilate(edges, kernel_d, iterations=3)
        filled   = cv2.bitwise_not(dilated)
        kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        thresh_clean = cv2.morphologyEx(filled,       cv2.MORPH_CLOSE, kernel_c)
        thresh_clean = cv2.morphologyEx(thresh_clean, cv2.MORPH_OPEN,  kernel_o)

    elif metoda == "kmeans":
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

    else:  # "masca" — imagine sintetica cu borduri negre
        mask = np.any(img_bgr > 25, axis=2).astype(np.uint8) * 255
        kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        thresh_clean = cv2.morphologyEx(mask,        cv2.MORPH_CLOSE, kernel_c)
        thresh_clean = cv2.morphologyEx(thresh_clean, cv2.MORPH_OPEN,  kernel_o)

    contururi, _ = cv2.findContours(thresh_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_rezultat = img_bgr.copy()
    parcele = []
    nr_parcela = 1
    aria_totala_img = h_img * w_img

    for contur in contururi:
        aria_px = cv2.contourArea(contur)
        # Ignora contururi mici (zgomot) si conturul intregii imagini
        if aria_px < aria_min_px:
            continue
        if aria_px > aria_totala_img * 0.90:
            continue  # conturul imaginii intregi — ignorat

        metrici = calculeaza_metrici_exacte(contur, scala_m_per_px)
        aria_ha  = metrici["aria_ha"]
        aria_m2  = metrici["aria_m2"]
        perim_m  = metrici["perim_m"]

        # Detectie cultura din culoarea ROI
        x_b, y_b, w_b, h_b = cv2.boundingRect(contur)
        roi = img_bgr[y_b:y_b+h_b, x_b:x_b+w_b]
        if mod_real or metoda in ("canny", "kmeans", "linii_albe"):
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
            "id":           id_parcela,
            "cultura":      cultura,
            "aria_ha":      metrici["aria_ha"],
            "aria_m2":      metrici["aria_m2"],
            "aria_px":      int(metrici["aria_px2"]),
            "perim_m":      metrici["perim_m"],
            "perim_px":     metrici["perim_px"],
            "compactitate": metrici["compactitate"],
            "centru":       centru_contur(contur),
            "nr":           nr_parcela,
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


def detecteaza_gradient_advanced(img_bgr: np.ndarray,
                                   scala_m_per_px: float,
                                   aria_min_px: int = 12000,
                                   id_fermier_prefix: str = "APIA-GJ",
                                   masca_compas: bool = True,
                                   masca_minimap: bool = True,
                                   masca_text_ui: bool = True,
                                   aspect_max: float = 12.0,
                                   culoare_contur=(255, 255, 255),
                                   arata_cultura: bool = False) -> tuple:
    """
    Algoritm avansat pentru imagini aeriene oblice (avion / Google Earth):
    1. Mascare UI (compas, mini-harta, telemetrie) — coordonate relative la dimensiunile imaginii
    2. pyrMeanShiftFiltering — simplificare coloristica
    3. CLAHE — contrast local
    4. Bariere = gradient morfologic + pixeli luminosi (drumuri)
    5. Regiuni = inversul barierelor + morfologie
    6. connectedComponentsWithStats — componente conexe
    7. Filtrare aspect ratio + pozitie y
    8. approxPolyDP — simplificare contur
    """
    h, w = img_bgr.shape[:2]

    # ── 1. Mascare UI overlay ──────────────────────────────────────────────────
    valid = np.ones((h, w), dtype=np.uint8) * 255
    if masca_compas:
        # compas: ~stanga-sus, ~28% lat x ~33% inaltime
        cv2.rectangle(valid, (0, int(h * 0.08)), (int(w * 0.28), int(h * 0.33)), 0, -1)
    if masca_minimap:
        # mini-harta: ~stanga-jos, ~37% lat x ~25% inaltime
        cv2.rectangle(valid, (0, int(h * 0.64)), (int(w * 0.37), h), 0, -1)
    if masca_text_ui:
        # telemetrie/text: ~dreapta-jos, ~30% lat x ~35% inaltime
        cv2.rectangle(valid, (int(w * 0.70), int(h * 0.66)), (w, h), 0, -1)

    masked = cv2.bitwise_and(img_bgr, img_bgr, mask=valid)

    # ── 2. Mean Shift + CLAHE ──────────────────────────────────────────────────
    smoothed  = cv2.pyrMeanShiftFiltering(masked, sp=18, sr=28)
    gray      = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)
    clahe     = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    gray_eq   = clahe.apply(gray)

    # ── 3. Bariere = gradient morfologic + pixeli luminosi ────────────────────
    grad = cv2.morphologyEx(
        gray_eq, cv2.MORPH_GRADIENT,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    _, edge_bin = cv2.threshold(grad, 18, 255, cv2.THRESH_BINARY)

    _, bright = cv2.threshold(gray_eq, 150, 255, cv2.THRESH_BINARY)
    bright    = cv2.morphologyEx(
        bright, cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1
    )

    barriers = cv2.bitwise_or(edge_bin, bright)
    barriers = cv2.bitwise_and(barriers, valid)
    barriers = cv2.dilate(
        barriers, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1
    )

    # ── 4. Regiuni candidate = inversul barierelor ────────────────────────────
    regions = cv2.bitwise_and(cv2.bitwise_not(barriers), valid)
    regions = cv2.morphologyEx(
        regions, cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=1
    )
    regions = cv2.morphologyEx(
        regions, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)), iterations=2
    )

    # ── 5. Connected components ───────────────────────────────────────────────
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(regions, connectivity=8)

    img_rezultat = img_bgr.copy()
    parcele = []
    nr_parcela = 1
    aria_totala = h * w

    for lbl in range(1, num_labels):
        area_px = int(stats[lbl, cv2.CC_STAT_AREA])
        if area_px < aria_min_px:
            continue

        comp_mask = np.uint8(labels == lbl) * 255
        contururi_c, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
        if not contururi_c:
            continue
        cnt = max(contururi_c, key=cv2.contourArea)
        cnt_area = cv2.contourArea(cnt)
        if cnt_area < aria_min_px:
            continue
        if cnt_area > aria_totala * 0.90:
            continue

        x_b, y_b, w_b, h_b = cv2.boundingRect(cnt)
        # Elimina fragmente de cer / orizont si noise alungit
        if y_b < int(h * 0.08):
            continue
        aspect = max(w_b / max(h_b, 1), h_b / max(w_b, 1))
        if aspect > aspect_max:
            continue

        # Simplificare contur
        epsilon = 0.003 * cv2.arcLength(cnt, True)
        approx  = cv2.approxPolyDP(cnt, epsilon, True)

        metrici = calculeaza_metrici_exacte(cnt, scala_m_per_px)
        roi     = img_bgr[y_b:y_b+h_b, x_b:x_b+w_b]
        cultura = detecteaza_cultura_hsv(roi)

        prefix_cultura = {
            "Grau": "GR", "Floarea-soarelui": "FS",
            "Porumb": "PO", "Lucerna": "LU",
            "Fanete": "FA", "Necunoscuta": "XX"
        }.get(cultura, "XX")
        id_parcela = f"{id_fermier_prefix}-{prefix_cultura}-{nr_parcela:03d}"

        info = {
            "id":           id_parcela,
            "cultura":      cultura,
            "aria_ha":      metrici["aria_ha"],
            "aria_m2":      metrici["aria_m2"],
            "aria_px":      int(metrici["aria_px2"]),
            "perim_m":      metrici["perim_m"],
            "perim_px":     metrici["perim_px"],
            "compactitate": metrici["compactitate"],
            "centru":       centru_contur(cnt),
            "nr":           nr_parcela,
            "approx_pts":   len(approx),
        }

        img_rezultat = inscrie_text_parcela(
            img_rezultat, approx, info,
            culoare_contur=culoare_contur,
            grosime_contur=3,
            arata_cultura=arata_cultura,
        )
        parcele.append(info)
        nr_parcela += 1

    return img_rezultat, parcele, regions


def detecteaza_slic_watershed(img_bgr: np.ndarray,
                               scala_m_per_px: float,
                               aria_min_px: int = 15000,
                               id_fermier_prefix: str = "APIA-GJ",
                               masca_compas: bool = True,
                               masca_minimap: bool = True,
                               masca_text_ui: bool = True,
                               n_segments: int = 320,
                               aspect_max: float = 16.0,
                               culoare_contur=(255, 255, 255),
                               arata_cultura: bool = False) -> tuple:
    """
    Algoritm SLIC superpixeli + Watershed pentru imagini agricole aeriene.
    Pipeline:
    1. Mascare UI relativa la dimensiunile imaginii
    2. pyrMeanShiftFiltering + SLIC in spatiu LAB
    3. Harta elevatie = gradient morfologic + frontiere SLIC + zone luminoase
    4. Masca teren HSV (verde/sol/padure)
    5. Distance transform + peak_local_max -> markeri watershed
    6. Watershed segmentation -> regiuni parcele
    7. Filtrare + approxPolyDP + inscriere text stil Google Earth
    """
    if not SKIMAGE_OK:
        return img_bgr.copy(), [], None

    h, w = img_bgr.shape[:2]

    # ── 1. Mascare UI (coordonate absolute calibrate pe imaginea reala) ───────
    valid = np.ones((h, w), dtype=np.uint8)
    if masca_compas:
        # compas: stanga-sus (0,90)→(420,470)
        cv2.rectangle(valid, (0, 90), (min(420, w), min(470, h)), 0, -1)
    if masca_minimap:
        # mini-harta: stanga-jos (0,930)→(560,h)
        cv2.rectangle(valid, (0, min(930, h)), (min(560, w), h), 0, -1)
    if masca_text_ui:
        # telemetrie/logo: dreapta-jos (1070,890)→(w,h)
        cv2.rectangle(valid, (min(1070, w), min(890, h)), (w, h), 0, -1)
    valid_bool = valid.astype(bool)

    # ── 2. Mean Shift + SLIC in LAB ───────────────────────────────────────────
    smoothed_bgr = cv2.pyrMeanShiftFiltering(img_bgr, sp=18, sr=26)
    smoothed_rgb = cv2.cvtColor(smoothed_bgr, cv2.COLOR_BGR2RGB)
    lab = rgb2lab(smoothed_rgb)

    segments = slic(
        lab,
        n_segments=n_segments,
        compactness=12,
        sigma=1.2,
        start_label=1,
        mask=valid_bool,
        channel_axis=-1,
    )

    # ── 3. Harta elevatie pentru watershed ───────────────────────────────────
    gray = cv2.cvtColor(smoothed_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    grad = cv2.morphologyEx(
        gray, cv2.MORPH_GRADIENT,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    slic_bounds = find_boundaries(segments, mode="outer").astype(np.uint8) * 255

    _, bright = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    bright = cv2.morphologyEx(
        bright, cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1
    )

    elevation = cv2.normalize(grad, None, 0, 255, cv2.NORM_MINMAX)
    elevation = cv2.addWeighted(elevation, 0.8, slic_bounds, 0.7, 0)
    elevation = cv2.addWeighted(elevation, 1.0, bright, 0.45, 0)
    elevation = np.where(valid_bool, elevation, 255).astype(np.uint8)

    # ── 4. Masca teren HSV ────────────────────────────────────────────────────
    hsv = cv2.cvtColor(smoothed_bgr, cv2.COLOR_BGR2HSV)
    mask_green   = cv2.inRange(hsv, np.array([25, 18, 25]),  np.array([95, 255, 255]))
    mask_brown   = cv2.inRange(hsv, np.array([5,  18, 20]),  np.array([28, 255, 220]))
    mask_darkveg = cv2.inRange(hsv, np.array([20, 8,  10]),  np.array([85, 180, 125]))

    land = cv2.bitwise_or(mask_green, mask_brown)
    land = cv2.bitwise_or(land, mask_darkveg)
    land = cv2.bitwise_and(land, valid)
    land = cv2.morphologyEx(land, cv2.MORPH_CLOSE,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),
                             iterations=2)
    land = cv2.morphologyEx(land, cv2.MORPH_OPEN,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
                             iterations=1)

    # ── 5. Distance transform + markeri ──────────────────────────────────────
    dist      = cv2.distanceTransform(land, cv2.DIST_L2, 5)
    dist_norm = cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)

    coords = peak_local_max(
        dist_norm,
        min_distance=40,
        threshold_abs=0.13,
        labels=(land > 0),
    )
    markers = np.zeros_like(gray, dtype=np.int32)
    for i, (r, c) in enumerate(coords, start=1):
        markers[r, c] = i
    markers = ndi.label(markers > 0)[0]

    # ── 6. Watershed ─────────────────────────────────────────────────────────
    labels_ws = watershed(elevation, markers=markers, mask=(land > 0))

    # ── 7. Extrage parcele ────────────────────────────────────────────────────
    img_rezultat = img_bgr.copy()
    parcele      = []
    nr_parcela   = 1
    aria_totala  = h * w

    for lbl in np.unique(labels_ws):
        if lbl == 0:
            continue
        reg      = np.uint8(labels_ws == lbl) * 255
        area_reg = int(cv2.countNonZero(reg))
        if area_reg < aria_min_px:
            continue

        contururi_c, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contururi_c:
            continue
        cnt      = max(contururi_c, key=cv2.contourArea)
        cnt_area = cv2.contourArea(cnt)
        if cnt_area < aria_min_px or cnt_area > aria_totala * 0.90:
            continue

        x_b, y_b, w_b, h_b = cv2.boundingRect(cnt)
        if y_b < 110:   # elimina cer / orizont (absolut px)
            continue
        aspect = max(w_b / max(h_b, 1), h_b / max(w_b, 1))
        if aspect > aspect_max:
            continue

        perim  = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.0035 * perim, True)

        metrici = calculeaza_metrici_exacte(cnt, scala_m_per_px)
        roi     = img_bgr[y_b:y_b+h_b, x_b:x_b+w_b]
        cultura = detecteaza_cultura_hsv(roi)

        prefix_cultura = {
            "Grau": "GR", "Floarea-soarelui": "FS",
            "Porumb": "PO", "Lucerna": "LU",
            "Fanete": "FA", "Necunoscuta": "XX"
        }.get(cultura, "XX")
        id_parcela = f"{id_fermier_prefix}-{prefix_cultura}-{nr_parcela:03d}"

        info = {
            "id":           id_parcela,
            "cultura":      cultura,
            "aria_ha":      metrici["aria_ha"],
            "aria_m2":      metrici["aria_m2"],
            "aria_px":      int(metrici["aria_px2"]),
            "perim_m":      metrici["perim_m"],
            "perim_px":     metrici["perim_px"],
            "compactitate": metrici["compactitate"],
            "centru":       centru_contur(cnt),
            "nr":           nr_parcela,
        }

        # Deseneaza conturul
        cv2.drawContours(img_rezultat, [approx], -1, culoare_contur, 3)

        # Text stil Google Earth: 3 linii cu marimi diferite
        cx, cy = centru_contur(cnt)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Linia 1: ID parcela (mai mare)
        linie1 = f"P{nr_parcela}"
        scale1, th1 = 0.7, 2
        (tw1, _), _ = cv2.getTextSize(linie1, font, scale1, th1)
        tx1 = max(4, min(cx - tw1 // 2, w - tw1 - 4))
        ty1 = max(20, min(cy - 22, h - 50))
        cv2.putText(img_rezultat, linie1, (tx1, ty1), font, scale1, (0, 0, 0), th1 + 2, cv2.LINE_AA)
        cv2.putText(img_rezultat, linie1, (tx1, ty1), font, scale1, (255, 255, 255), th1, cv2.LINE_AA)

        # Linia 2: Arie (sq m)
        linie2 = f"{metrici['aria_m2']:,} sq m"
        scale2, th2 = 0.55, 1
        (tw2, _), _ = cv2.getTextSize(linie2, font, scale2, th2)
        tx2 = max(4, min(cx - tw2 // 2, w - tw2 - 4))
        ty2 = max(20, min(cy + 2, h - 30))
        cv2.putText(img_rezultat, linie2, (tx2, ty2), font, scale2, (0, 0, 0), th2 + 2, cv2.LINE_AA)
        cv2.putText(img_rezultat, linie2, (tx2, ty2), font, scale2, (255, 255, 255), th2, cv2.LINE_AA)

        # Linia 3: Perimetru (m)
        linie3 = f"{int(metrici['perim_m']):,} m"
        scale3, th3 = 0.55, 1
        (tw3, _), _ = cv2.getTextSize(linie3, font, scale3, th3)
        tx3 = max(4, min(cx - tw3 // 2, w - tw3 - 4))
        ty3 = max(20, min(cy + 24, h - 10))
        cv2.putText(img_rezultat, linie3, (tx3, ty3), font, scale3, (0, 0, 0), th3 + 2, cv2.LINE_AA)
        cv2.putText(img_rezultat, linie3, (tx3, ty3), font, scale3, (255, 255, 255), th3, cv2.LINE_AA)

        parcele.append(info)
        nr_parcela += 1

    return img_rezultat, parcele, land


def segmenteaza_hsv_agricol(img_bgr: np.ndarray,
                              masca_compas: bool = True,
                              masca_minimap: bool = True,
                              masca_text: bool = True) -> np.ndarray:
    """
    Segmentare HSV pentru imagini agricole aeriene (Google Earth / avion / satelit).
    Detecteaza: vegetatie verde, sol/brun, padure, exclude drumuri deschise.
    Mascheaza zonele UI: compas stg-sus, mini-harta stg-jos, text alb.
    Returneaza masca binara 0/255 cu zonele agricole.
    """
    h, w = img_bgr.shape[:2]

    # Masca valida: 1 = zone de analizat, 0 = UI overlay de ignorat
    mask_valid = np.ones((h, w), dtype=np.uint8) * 255
    if masca_compas:
        cx_sz = int(w * 0.22)
        cy_sz = int(h * 0.30)
        cv2.rectangle(mask_valid, (0, 0), (cx_sz, cy_sz), 0, -1)
    if masca_minimap:
        mx_sz = int(w * 0.32)
        my_sz = int(h * 0.35)
        cv2.rectangle(mask_valid, (0, h - my_sz), (mx_sz, h), 0, -1)
    if masca_text:
        tx_sz = int(w * 0.55)
        ty_sz = int(h * 0.45)
        cv2.rectangle(mask_valid, (w - tx_sz, h - ty_sz), (w, h), 0, -1)

    # Aplica masca
    img_m = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_valid)

    # Blur + HSV
    blur = cv2.GaussianBlur(img_m, (7, 7), 0)
    hsv  = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Vegetatie verde
    mask_verde  = cv2.inRange(hsv, np.array([30, 20, 30]),   np.array([95, 255, 255]))
    # Sol / brun
    mask_sol    = cv2.inRange(hsv, np.array([5,  20, 20]),   np.array([25, 255, 220]))
    # Padure / vegetatie inchisa
    mask_padure = cv2.inRange(hsv, np.array([20, 10, 10]),   np.array([80, 180, 120]))
    # Drumuri / zone deschise luminoase — de EXCLUS
    mask_drum   = cv2.inRange(hsv, np.array([0,   0, 120]),  np.array([180, 80, 255]))

    # Combina zone agricole si exclude drumuri
    mask_agricol = cv2.bitwise_or(mask_verde, mask_sol)
    mask_agricol = cv2.bitwise_or(mask_agricol, mask_padure)
    mask_agricol = cv2.bitwise_and(mask_agricol, cv2.bitwise_not(mask_drum))
    mask_agricol = cv2.bitwise_and(mask_agricol, mask_valid)

    # Morfologie: Close (umple gauri), Open (elimina zgomot)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    mask_agricol = cv2.morphologyEx(mask_agricol, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask_agricol = cv2.morphologyEx(mask_agricol, cv2.MORPH_OPEN,  kernel, iterations=1)

    return mask_agricol


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
        st.markdown("**Parametri scala (GSD):**")

        metoda_scala = st.radio(
            "Cum stabilesti scala:",
            ["Preset", "Calculator GSD", "Manual"],
            horizontal=True, key="metoda_scala"
        )

        if metoda_scala == "Preset":
            scala_optiune = st.selectbox(
                "Tipul scalei:",
                ["Drone 100m altitudine (0.05 m/px)",
                 "Drone 50m altitudine (0.025 m/px)",
                 "Drone 200m altitudine (0.10 m/px)",
                 "Avion 1000m (0.5 m/px)",
                 "Avion 3000m (1.5 m/px)",
                 "Avion 11500m (27 m/px)",
                 "Satelit Sentinel-2 (10 m/px)"],
                key="scala_opt"
            )
            scala_map = {
                "Drone 100m altitudine (0.05 m/px)":  0.05,
                "Drone 50m altitudine (0.025 m/px)":  0.025,
                "Drone 200m altitudine (0.10 m/px)":  0.10,
                "Avion 1000m (0.5 m/px)":             0.5,
                "Avion 3000m (1.5 m/px)":             1.5,
                "Avion 11500m (27 m/px)":             27.0,
                "Satelit Sentinel-2 (10 m/px)":       10.0,
            }
            scala_m_per_px = scala_map.get(scala_optiune, 0.05)
            st.metric("GSD activ", f"{scala_m_per_px} m/px")

        elif metoda_scala == "Calculator GSD":
            st.markdown("""
            <div style='font-size:11px; color:#555; background:#f0f4ff;
                 padding:8px; border-radius:6px; margin-bottom:6px;'>
            <b>Formula GSD:</b> (altitudine × sensor_latime) / (focal × img_latime_px)
            </div>""", unsafe_allow_html=True)
            alt_m   = st.number_input("Altitudine (m):", 10.0, 15000.0, 100.0, 10.0, key="gsd_alt")
            focal   = st.number_input("Focal length (mm):", 1.0, 200.0, 8.8, 0.5, key="gsd_focal")
            sensor  = st.number_input("Latime senzor (mm):", 1.0, 50.0, 13.2, 0.1, key="gsd_sensor")
            img_w_px = st.number_input("Latime imagine (px):", 100, 20000, 4000, 100, key="gsd_imgw",
                                        format="%d")
            scala_m_per_px = calculeaza_gsd(alt_m, focal, sensor, int(img_w_px))
            st.metric("GSD calculat", f"{scala_m_per_px:.4f} m/px",
                      help="1 pixel in imagine = aceasta distanta in realitate")
            # Exemple rapide
            st.caption("Exemple: DJI Phantom 4 la 100m → 0.033 m/px | "
                        "Telefon Samsung (zbor avion 11500m) → ~27 m/px")

        else:  # Manual
            scala_m_per_px = st.number_input(
                "GSD manual (m/px):", 0.001, 500.0, 0.05, 0.005, key="scala_manual"
            )

        st.divider()
        st.markdown("**Metoda detectie:**")
        slic_label = ("SLIC + Watershed (recomandat imagini reale)"
                      if SKIMAGE_OK else
                      "SLIC + Watershed [lipseste scikit-image]")
        metoda_aleasa = st.selectbox(
            "Algoritm segmentare:",
            [
                slic_label,
                "Gradient Avansat (Mean Shift + CLAHE)",
                "HSV Vegetatie/Sol",
                "Linii albe (Google Earth / QGIS)",
                "K-means (segmentare culori)",
                "Canny (contraste puternice)",
                "Masca non-negru (imagine sintetica)",
            ],
            index=0 if uploaded is not None else 6,
            key="metoda_seg"
        )
        metoda_map = {
            slic_label:                                             "slic",
            "Gradient Avansat (Mean Shift + CLAHE)":               "gradient",
            "HSV Vegetatie/Sol":                                    "hsv",
            "Linii albe (Google Earth / QGIS)":                    "linii_albe",
            "K-means (segmentare culori)":                         "kmeans",
            "Canny (contraste puternice)":                         "canny",
            "Masca non-negru (imagine sintetica)":                 "masca",
        }
        metoda   = metoda_map[metoda_aleasa]
        mod_real = metoda != "masca"

        # Parametri specifici metodei
        canny_low, canny_high, kmeans_k, alb_prag = 30, 150, 6, 180
        masca_compas = masca_minimap = masca_text_ui = False
        aspect_max = 12.0
        n_segments = 350

        if metoda in ("slic", "gradient", "hsv"):
            st.markdown("**Mascheaza UI Google Earth:**")
            masca_compas  = st.checkbox("Compas (stanga sus)",      value=True, key="m_compas")
            masca_minimap = st.checkbox("Mini-harta (stanga jos)",   value=True, key="m_mini")
            masca_text_ui = st.checkbox("Text / logo (dreapta jos)", value=True, key="m_text")
            if metoda == "slic":
                n_segments = st.slider("Superpixeli SLIC:", 150, 600, 320, 50, key="n_seg",
                                       help="Mai multi = granularitate mai fina, mai lent")
                aspect_max = st.slider("Aspect ratio maxim:", 3.0, 20.0, 16.0, 0.5,
                                       key="aspect_max_slic")
                if not SKIMAGE_OK:
                    st.error("scikit-image si scipy nu sunt instalate. "
                             "Ruleaza: `pip install scikit-image scipy`")
            elif metoda == "gradient":
                n_segments = 350
                aspect_max = st.slider("Aspect ratio maxim:", 3.0, 20.0, 12.0, 0.5,
                                       help="Parcele mai alungite sunt ignorate",
                                       key="aspect_max")
        elif metoda == "linii_albe":
            alb_prag = st.slider("Prag alb (pixeli ≥):", 140, 240, 180, 5, key="alb_prag")
        elif metoda == "canny":
            canny_low  = st.slider("Prag Canny minim:", 5, 100,  30, 5,  key="canny_low")
            canny_high = st.slider("Prag Canny maxim:", 30, 300, 150, 10, key="canny_high")
        elif metoda == "kmeans":
            kmeans_k = st.slider("Nr. culori K-means:", 3, 12, 6, 1, key="kmeans_k")

        st.divider()
        st.markdown("**Afisare contururi:**")
        culoare_contur_hex = st.color_picker("Culoare contur:", "#FFFFFF", key="culoare_contur")
        h_col = culoare_contur_hex.lstrip("#")
        r_, g_, b_ = int(h_col[0:2], 16), int(h_col[2:4], 16), int(h_col[4:6], 16)
        culoare_contur_bgr = (b_, g_, r_)
        arata_cultura = st.checkbox("Afiseaza cultura pe parcela", value=False, key="arata_cult")

        st.divider()
        st.markdown("**Filtrare contururi:**")
        aria_min_px = st.slider(
            "Arie minima (pixeli²):",
            min_value=100, max_value=50000, value=1000, step=100,
            help="Contururi mai mici sunt ignorate. Scade daca gaseste 0 parcele.",
            key="aria_min"
        )
        id_prefix = st.text_input("Prefix ID fermier:", value="APIA-GJ", key="id_prefix")

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
            # Fallback automat: daca SLIC ales dar scikit-image lipseste
            metoda_efectiva = metoda
            if metoda == "slic" and not SKIMAGE_OK:
                st.warning(
                    "scikit-image nu este instalat — folosesc Gradient Avansat ca fallback. "
                    "Instaleaza cu: `pip install scikit-image scipy` si reporneste Streamlit."
                )
                metoda_efectiva = "gradient"

            with st.spinner("Detectez contururi... poate dura 10-30s"):
                mask_grad = None

                if metoda_efectiva == "slic":
                    img_rez, parcele_detectate, mask_grad = detecteaza_slic_watershed(
                        img_src, scala_m_per_px,
                        aria_min_px=aria_min_px,
                        id_fermier_prefix=id_prefix,
                        masca_compas=masca_compas,
                        masca_minimap=masca_minimap,
                        masca_text_ui=masca_text_ui,
                        n_segments=n_segments,
                        aspect_max=aspect_max,
                        culoare_contur=culoare_contur_bgr,
                        arata_cultura=arata_cultura,
                    )

                elif metoda_efectiva == "gradient":
                    img_rez, parcele_detectate, mask_grad = detecteaza_gradient_advanced(
                        img_src, scala_m_per_px,
                        aria_min_px=aria_min_px,
                        id_fermier_prefix=id_prefix,
                        masca_compas=masca_compas,
                        masca_minimap=masca_minimap,
                        masca_text_ui=masca_text_ui,
                        aspect_max=aspect_max,
                        culoare_contur=culoare_contur_bgr,
                        arata_cultura=arata_cultura,
                    )

                else:
                    img_rez, parcele_detectate = analizeaza_contururi(
                        img_src, scala_m_per_px, aria_min_px, id_prefix,
                        mod_real=mod_real,
                        canny_low=canny_low,
                        canny_high=canny_high,
                        metoda=metoda_efectiva,
                        kmeans_k=kmeans_k,
                        alb_prag=alb_prag,
                        culoare_contur_global=culoare_contur_bgr,
                        arata_cultura=arata_cultura,
                        masca_compas=masca_compas,
                        masca_minimap=masca_minimap,
                        masca_text_ui=masca_text_ui,
                    )

                if mask_grad is not None:
                    st.session_state["mask_gradient"] = mask_grad

                n_detectate = len(parcele_detectate)
                if n_detectate == 0:
                    st.warning(
                        f"0 parcele detectate cu metoda **{metoda_efectiva}**. "
                        "Incearca: scade **Arie minima** la 500-1000 px, "
                        "debifeza mastile UI, sau schimba metoda."
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
        _metoda_f = st.session_state.get("metoda_folosita", "gradient")
        with st.expander("Imagini intermediare pipeline"):
            gray_d = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
            c_low  = st.session_state.get("canny_low",  30)
            c_high = st.session_state.get("canny_high", 150)

            if _metoda_f == "gradient":
                mask_g = st.session_state.get("mask_gradient")
                if mask_g is not None:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.image(img_src[:,:,::-1], caption="Original",
                                 use_container_width=True)
                    with c2:
                        st.image(mask_g, caption="Regiuni detectate (alb = parcela)",
                                 use_container_width=True)
                else:
                    st.info("Ruleaza detectia mai intai.")

            elif _metoda_f == "canny":
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
            "Nr.":             p["nr"],
            "ID Parcela":      p["id"],
            "Cultura":         p["cultura"],
            "Aria (sq m)":     f"{p.get('aria_m2', int(p['aria_ha']*10000)):,}",
            "Aria (ha)":       p["aria_ha"],
            "Perim. (m)":      f"{int(p['perim_m']):,}",
            "Compactitate":    p.get("compactitate", "—"),
            "Aria (px²)":      p["aria_px"],
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
