"""
Ziua 12 — Sinteza Modul 2: Computer Vision Complet
Pipeline integrat: OpenCV + NDVI + YOLO + OCR + Detectie Anomalii
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import io
import re
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Ziua 12 — Sinteza Modul 2", page_icon="🔭", layout="wide")

# ─── Culori culturi ────────────────────────────────────────────────────────────
CULTURI = ["Grau", "Floarea-soarelui", "Porumb", "Lucerna", "Fanete"]
CULORI  = ["#f39c12", "#f1c40f", "#27ae60", "#16a085", "#795548"]

# ══════════════════════════════════════════════════════════════════════════════
# FUNCȚII UTILITARE
# ══════════════════════════════════════════════════════════════════════════════

def ndvi_la_culoare(ndvi: np.ndarray) -> np.ndarray:
    """Converteste array NDVI [-1,1] in imagine BGR (RdYlGn manual)."""
    t = np.clip((ndvi + 1.0) / 2.0, 0.0, 1.0).astype(np.float32)
    r, g, b = np.zeros_like(t), np.zeros_like(t), np.zeros_like(t)
    m1 = t < 0.5
    r[m1] = 1.0;        g[m1] = t[m1] * 2.0
    r[~m1] = 1.0 - (t[~m1] - 0.5) * 2.0;  g[~m1] = 1.0
    return np.stack([(b * 255).astype(np.uint8),
                     (g * 255).astype(np.uint8),
                     (r * 255).astype(np.uint8)], axis=-1)


def genereaza_harta_parcele(w=640, h=480):
    """Genereaza o imagine sintetica cu 5 parcele agricole colorate."""
    img = np.ones((h, w, 3), dtype=np.uint8) * 30  # fundal inchis

    zone = [
        (0,   0,   w//2, h//2,  (40,120,40),  "Grau"),
        (w//2,0,   w,    h//2,  (30,180,180), "Floarea-soarelui"),
        (0,   h//2,w//3, h,     (20,160,80),  "Porumb"),
        (w//3,h//2,2*w//3, h,   (80,200,120), "Lucerna"),
        (2*w//3,h//2, w, h,     (100,80,60),  "Fanete"),
    ]

    np.random.seed(42)
    for (x1,y1,x2,y2,culoare,_) in zone:
        roi = img[y1:y2, x1:x2]
        noise = np.random.randint(-15, 15, roi.shape).astype(np.int16)
        roi_f = roi.astype(np.int16) + noise
        img[y1:y2, x1:x2] = np.clip(roi_f, 0, 255).astype(np.uint8)
        # contur parcel
        cv2.rectangle(img, (x1, y1), (x2-1, y2-1), (200,200,200), 2)

    # zona stresata in Lucerna
    cx, cy = (w//3 + 2*w//3)//2, (h//2 + h)//2
    cv2.ellipse(img, (cx, cy), (50, 35), 0, 0, 360, (20, 40, 150), -1)

    return img, zone


def calcul_ndvi_rgb(img_bgr: np.ndarray):
    """Aproximare NDVI din imagine RGB folosind ExG (Excess Green)."""
    img_f = img_bgr.astype(np.float32) / 255.0
    R = img_f[:, :, 2]
    G = img_f[:, :, 1]
    B = img_f[:, :, 0]
    denom = R + G + B + 1e-6
    exg = (2*G - R - B)
    ndvi_approx = np.clip(exg, -1.0, 1.0)
    return ndvi_approx


def detectie_anomalii_rapida(ndvi_map: np.ndarray, zone: list):
    """Detecteaza anomalii NDVI per zona/parcel."""
    rezultate = []
    for (x1,y1,x2,y2,_,cultura) in zone:
        roi = ndvi_map[y1:y2, x1:x2]
        medie = float(np.mean(roi))
        procent_stress = float(np.mean(roi < 0.1) * 100)
        status = "Normal" if medie > 0.2 else ("Stress moderat" if medie > 0.0 else "Stress sever")
        rezultate.append({
            "Cultura": cultura,
            "NDVI_mediu": round(medie, 3),
            "Stress_%": round(procent_stress, 1),
            "Status": status
        })
    return rezultate


def preprocesare_ocr(img_bgr: np.ndarray) -> np.ndarray:
    """Pipeline preprocesare standard pentru OCR."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return cleaned


def genereaza_document_demo_pil(w=600, h=380) -> np.ndarray:
    """Genereaza document APIA demo cu PIL."""
    img_pil = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img_pil)

    try:
        font_title = ImageFont.truetype("arial.ttf", 16)
        font_body  = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_body  = ImageFont.load_default()

    draw.rectangle([10, 10, w-10, h-10], outline=(0,0,0), width=2)
    draw.rectangle([10, 10, w-10, 50], fill=(0,51,102), outline=(0,0,0), width=1)
    draw.text((20, 18), "APIA — RAPORT ANALIZA PARCELA AGRICOLA", fill=(255,255,255), font=font_title)

    linii = [
        ("Nr. cerere:", "2024-GJ-007823"),
        ("CNP beneficiar:", "1760412180032"),
        ("Suprafata totala:", "42.75 ha"),
        ("Judet:", "Gorj"),
        ("Bloc LPIS:", "GORJ-MU-0045"),
        ("Cultura declarata:", "Grau de toamna"),
        ("NDVI mediu masurat:", "0.612"),
        ("Data controlului:", "15.04.2024"),
        ("Inspector:", "Gam. O.M."),
    ]

    y = 70
    for eticheta, valoare in linii:
        draw.text((25, y), eticheta, fill=(0,0,0), font=font_body)
        draw.text((220, y), valoare, fill=(0,60,120), font=font_body)
        y += 28

    draw.text((25, y + 10),
              "Teza: 'Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone'",
              fill=(80,80,80), font=font_body)

    img_np = np.array(img_pil)
    return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)


def extrage_campuri_ocr(text: str) -> dict:
    """Extrage campuri APIA din text OCR cu regex."""
    campuri = {}
    patterns = {
        "Nr. cerere":       r'(?:Nr\.?\s*cerere[:\s]+)([\w\-]+)',
        "CNP":              r'(?:CNP[:\s]+)(\d{13})',
        "Suprafata (ha)":   r'(?:Suprafata[^:]*:[:\s]+)([\d.,]+)\s*ha',
        "Judet":            r'(?:Judet[:\s]+)([A-Za-z\-]+)',
        "Bloc LPIS":        r'(?:Bloc LPIS[:\s]+)([\w\-]+)',
        "NDVI":             r'(?:NDVI[^:]*:[:\s]+)([\d.,]+)',
        "Data":             r'(\d{2}[./]\d{2}[./]\d{4})',
    }
    for camp, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        campuri[camp] = m.group(1).strip() if m else "—"
    return campuri


def genereaza_raport_final(anomalii: list, campuri_ocr: dict) -> str:
    """Genereaza raport complet de sinteza."""
    data = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    linii = [
        "=" * 60,
        "RAPORT SINTEZA MODUL 2 — COMPUTER VISION APLICAT",
        "=" * 60,
        f"Data generare: {data}",
        f"Aplicatie: Bloc 5 AI Aplicat | Ziua 12",
        "",
        "REFERINTA ACADEMICA:",
        "  'Contributii privind recunoasterea automata a culturilor",
        "   cu ajutorul unei Drone'",
        "  Prof. Asoc. Dr. Oliviu Mihnea Gamulescu",
        "  Universitatea din Petrosani, 2024",
        "",
        "-" * 60,
        "SECTIUNEA 1: ANALIZA NDVI PARCELE",
        "-" * 60,
    ]
    for a in anomalii:
        linii.append(f"  {a['Cultura']:<20} NDVI={a['NDVI_mediu']:>6}  "
                     f"Stress={a['Stress_%']:>5}%  [{a['Status']}]")

    linii += [
        "",
        "-" * 60,
        "SECTIUNEA 2: CAMPURI EXTRASE PRIN OCR",
        "-" * 60,
    ]
    for camp, val in campuri_ocr.items():
        linii.append(f"  {camp:<20}: {val}")

    linii += [
        "",
        "-" * 60,
        "INSTRUMENTE FOLOSITE IN MODUL 2",
        "-" * 60,
        "  Z07 — YOLOv8: Detectie obiecte pe imagini drone",
        "  Z08 — OpenCV: Filtre, margini, morfologie",
        "  Z09 — NDVI: Indici vegetatie multispectral",
        "  Z10 — Detectie anomalii: Scoring risc parcele",
        "  Z11 — OCR Tesseract: Extragere date documente",
        "  Z12 — Sinteza: Pipeline complet CV",
        "",
        "=" * 60,
        "Inspector: ________________   Semnatura: ____________",
        "=" * 60,
    ]
    return "\n".join(linii)


# ══════════════════════════════════════════════════════════════════════════════
# INTERFATA STREAMLIT
# ══════════════════════════════════════════════════════════════════════════════

st.title("Ziua 12 — Sinteza Modul 2: Computer Vision Complet")
st.markdown("""
**Modulul 2 (Zilele 7-12) finalizat.** Aceasta pagina integreaza toate instrumentele
Computer Vision intr-un singur pipeline: preprocesare imagine → NDVI → detectie anomalii → OCR → raport.
""")

# Banner teza
st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px;padding:14px 20px;margin-bottom:16px;'>
<span style='color:#f9e79f;font-size:14px;font-style:italic;'>
"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"<br>
<b style='color:white;'>Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | Universitatea din Petrosani, 2024</b>
</span>
</div>""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teorie",
    "1. Imagine & OpenCV",
    "2. NDVI & Anomalii",
    "3. OCR & Extragere",
    "Raport Final & Recapitulare"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Ce este un pipeline Computer Vision?")
    st.markdown("""
Un **pipeline CV** inlantuie mai multe instrumente astfel incat output-ul unui pas devine input-ul urmatorului:

```
Imagine bruta
    ↓
[OpenCV] Preprocesare (filtru, resize, contrast)
    ↓
[NDVI] Calcul indice vegetatie → harta culori
    ↓
[Detectie anomalii] Identificare zone stresate
    ↓
[OCR] Extragere text din documente asociate
    ↓
[Raport] PDF / TXT pentru inspector APIA
```

### De ce integram toate instrumentele?
| Instrument | Ce rezolva |
|---|---|
| **OpenCV** | Curata imaginea, elimina zgomot, detecteaza margini |
| **NDVI** | Masoara sanatatea vegetatiei per pixel |
| **Anomalii** | Identifica parcele cu risc APIA pentru control |
| **OCR** | Digitalizeaza documente fizice (cereri, rapoarte teren) |
| **Raport** | Documentatie formala pentru inspectori |

### Contextul tezei de doctorat
Acesta este exact fluxul descris in teza *"Contributii privind recunoasterea automata a culturilor
cu ajutorul unei Drone"*: imaginile drone → procesare CV → decizie APIA.
""")

    st.info("""
**Recapitulare Modul 2 (6 zile):**
- Z7: YOLOv8 — detectie obiecte in timp real
- Z8: OpenCV — filtre, culori, morfologie, Canny/Sobel
- Z9: NDVI multispectral — indici vegetatie, harta culori
- Z10: Detectie anomalii — scoring risc parcele APIA
- Z11: OCR Tesseract — digitalizare documente
- Z12: Sinteza — pipeline complet integrat ← *esti aici*
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — IMAGINE & OPENCV
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Pasul 1: Imagine agricola + Preprocesare OpenCV")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Parametri preprocesare:**")
        blur_k   = st.slider("Gaussian blur (kernel)", 1, 15, 3, step=2, key="blur")
        contrast = st.slider("Contrast (alpha)", 0.5, 3.0, 1.2, step=0.1, key="contrast")
        canny_t1 = st.slider("Canny threshold 1", 10, 100, 30, key="c1")
        canny_t2 = st.slider("Canny threshold 2", 50, 300, 100, key="c2")

    # Genereaza imaginea
    img_orig, zone_parcele = genereaza_harta_parcele()

    # Aplicare preprocesare
    img_blur  = cv2.GaussianBlur(img_orig, (blur_k, blur_k), 0)
    img_contr = cv2.convertScaleAbs(img_blur, alpha=contrast, beta=0)
    img_gray  = cv2.cvtColor(img_contr, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, canny_t1, canny_t2)

    with col2:
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown("**Original**")
            st.image(img_orig[:, :, ::-1], use_container_width=True)
        with r2:
            st.markdown("**Blur + Contrast**")
            st.image(img_contr[:, :, ::-1], use_container_width=True)
        with r3:
            st.markdown("**Grayscale**")
            st.image(img_gray, use_container_width=True)
        with r4:
            st.markdown("**Canny (margini)**")
            st.image(img_canny, use_container_width=True)

    # Salveaza in session state pentru pasii urmatori
    st.session_state["img_procesat"] = img_contr
    st.session_state["zone_parcele"] = zone_parcele

    st.success("Imaginea este pregatita pentru analiza NDVI.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — NDVI & ANOMALII
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Pasul 2: Calcul NDVI + Detectie Anomalii")

    img_src = st.session_state.get("img_procesat", genereaza_harta_parcele()[0])
    zone_src = st.session_state.get("zone_parcele", genereaza_harta_parcele()[1])

    ndvi_map = calcul_ndvi_rgb(img_src)
    ndvi_img = ndvi_la_culoare(ndvi_map)
    anomalii = detectie_anomalii_rapida(ndvi_map, zone_src)

    st.session_state["anomalii"] = anomalii

    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Harta NDVI (aproximare RGB)**")
        st.image(ndvi_img[:, :, ::-1], use_container_width=True)
        st.caption("Rosu = stress, Galben = moderat, Verde = vegetatie sanatoasa")

    with colB:
        st.markdown("**Tabel anomalii per parcel:**")
        import pandas as pd
        df_anom = pd.DataFrame(anomalii)

        def coloreaza_status(val):
            if val == "Normal":
                return "background-color: #d5f5e3"
            elif val == "Stress moderat":
                return "background-color: #fef9e7"
            else:
                return "background-color: #fadbd8"

        st.dataframe(
            df_anom.style.applymap(coloreaza_status, subset=["Status"]),
            use_container_width=True,
            hide_index=True
        )

    # Grafic NDVI per cultura
    st.markdown("**Grafic NDVI mediu per cultura:**")
    fig_ndvi = go.Figure()
    culori_bar = [CULORI[CULTURI.index(a["Cultura"])] if a["Cultura"] in CULTURI else "#888"
                  for a in anomalii]
    fig_ndvi.add_trace(go.Bar(
        x=[a["Cultura"] for a in anomalii],
        y=[a["NDVI_mediu"] for a in anomalii],
        marker_color=culori_bar,
        text=[a["Status"] for a in anomalii],
        textposition="outside"
    ))
    fig_ndvi.add_hline(y=0.2, line_dash="dash", line_color="red",
                       annotation_text="Prag stress")
    fig_ndvi.update_layout(
        height=300,
        yaxis_title="NDVI mediu",
        showlegend=False,
        margin=dict(t=30, b=40)
    )
    st.plotly_chart(fig_ndvi, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — OCR & EXTRAGERE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Pasul 3: Document APIA → OCR → Campuri extrase")

    colX, colY = st.columns(2)

    with colX:
        st.markdown("**Document demo generat (PIL):**")
        doc_img = genereaza_document_demo_pil()
        st.image(doc_img[:, :, ::-1], use_container_width=True)

    with colY:
        st.markdown("**Preprocesare pentru OCR:**")
        doc_prep = preprocesare_ocr(doc_img)
        st.image(doc_prep, use_container_width=True)
        st.caption("Imagine binarizata Otsu — text mai clar pentru OCR")

    # OCR demo text (fallback fara Tesseract instalat)
    text_demo = """APIA - RAPORT ANALIZA PARCELA AGRICOLA
Nr. cerere: 2024-GJ-007823
CNP beneficiar: 1760412180032
Suprafata totala: 42.75 ha
Judet: Gorj
Bloc LPIS: GORJ-MU-0045
Cultura declarata: Grau de toamna
NDVI mediu masurat: 0.612
Data controlului: 15.04.2024
Inspector: Gam. O.M."""

    # Incearca Tesseract real
    ocr_text = text_demo
    sursa_ocr = "Demo (text predefinit)"

    try:
        import pytesseract
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for p in tesseract_paths:
            import os
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                break
        ocr_text = pytesseract.image_to_string(doc_prep, config="--psm 6")
        sursa_ocr = "Tesseract OCR (real)"
    except Exception:
        pass

    campuri = extrage_campuri_ocr(ocr_text)
    st.session_state["campuri_ocr"] = campuri

    st.markdown(f"**Sursa OCR:** `{sursa_ocr}`")
    st.markdown("**Campuri extrase cu regex:**")

    col1, col2 = st.columns(2)
    campuri_lista = list(campuri.items())
    jumatate = len(campuri_lista) // 2
    with col1:
        for k, v in campuri_lista[:jumatate]:
            st.metric(k, v)
    with col2:
        for k, v in campuri_lista[jumatate:]:
            st.metric(k, v)

    with st.expander("Text brut OCR"):
        st.code(ocr_text, language="text")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — RAPORT FINAL & RECAPITULARE
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Raport Final + Recapitulare Modul 2")

    anomalii_final = st.session_state.get("anomalii", detectie_anomalii_rapida(
        calcul_ndvi_rgb(genereaza_harta_parcele()[0]), genereaza_harta_parcele()[1]
    ))
    campuri_final = st.session_state.get("campuri_ocr", {
        "Nr. cerere": "2024-GJ-007823",
        "CNP": "1760412180032",
        "Suprafata (ha)": "42.75",
        "Judet": "Gorj",
        "Bloc LPIS": "GORJ-MU-0045",
        "NDVI": "0.612",
        "Data": "15.04.2024",
    })

    raport_txt = genereaza_raport_final(anomalii_final, campuri_final)

    colR1, colR2 = st.columns([2, 1])
    with colR1:
        st.text_area("Previzualizare raport:", raport_txt, height=380)
    with colR2:
        st.markdown("**Actiuni:**")
        st.download_button(
            label="Descarca Raport TXT",
            data=raport_txt.encode("utf-8"),
            file_name=f"sinteza_modul2_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

        st.markdown("---")
        st.markdown("**Sumar pipeline:**")
        st.success("Pas 1: Imagine preprocesata cu OpenCV")
        st.success("Pas 2: NDVI calculat + anomalii detectate")
        st.success("Pas 3: Document OCR-izat + campuri extrase")
        st.success("Pas 4: Raport generat")

    # ─── Recapitulare Modul 2 ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Recapitulare Modul 2 — Computer Vision (Zilele 7-12)")

    zile_m2 = [
        ("Z7", "YOLOv8 Detectie Culturi",
         "Detectie obiecte in timp real, bounding boxes, fine-tuning pe drone",
         "ultralytics", "#2ecc71"),
        ("Z8", "OpenCV Bazele",
         "Filtre spatiale, spatii culori, Canny/Sobel, morfologie, thresholding",
         "cv2", "#3498db"),
        ("Z9", "NDVI Multispectral",
         "Indici vegetatie, harta RdYlGn, detectie stress, ExG/VARI/GLI",
         "numpy + cv2", "#27ae60"),
        ("Z10", "Detectie Anomalii",
         "Scoring risc parcele, raport inspector APIA, scatter NDVI",
         "plotly", "#e74c3c"),
        ("Z11", "OCR Tesseract",
         "Extragere text din documente, regex campuri APIA, preprocesare",
         "pytesseract / easyocr", "#9b59b6"),
        ("Z12", "Sinteza Modul 2",
         "Pipeline integrat CV complet: imagine → NDVI → anomalii → OCR → raport",
         "toate", "#f39c12"),
    ]

    for ziua, titlu, descriere, lib, culoare in zile_m2:
        with st.container():
            st.markdown(f"""
<div style='border-left:4px solid {culoare};padding:8px 16px;margin:6px 0;
     background:rgba(0,0,0,0.03);border-radius:0 8px 8px 0;'>
<b style='color:{culoare};'>{ziua}</b> — <b>{titlu}</b><br>
<span style='font-size:13px;color:#555;'>{descriere}</span><br>
<code style='font-size:11px;'>{lib}</code>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.info("""
**Urmatorul modul: M3 — NLP Aplicat (Zilele 13-18)**

- Z13: Hugging Face Transformers — introducere
- Z14: Analiza sentimentului
- Z15: Clasificare texte agricole / APIA
- Z16: Rezumare automata documente
- Z17: Named Entity Recognition (NER)
- Z18: Sinteza Modul 3
""")

    st.markdown("""
---
*Referinta: 'Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone'
— Prof. Asoc. Dr. Oliviu Mihnea Gamulescu, Universitatea din Petrosani, 2024*
""")
