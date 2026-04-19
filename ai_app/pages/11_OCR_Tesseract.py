"""
ZIUA 11 — OCR: Extragere Text din Imagini si Documente
Modul 2: Computer Vision
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import date
import io
import re

try:
    import cv2
    CV2_OK = True
except ImportError:
    CV2_OK = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import pytesseract
    # Cale implicita Tesseract pe Windows
    import os
    cai_tesseract = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\USER\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
    ]
    for cale in cai_tesseract:
        if os.path.exists(cale):
            pytesseract.pytesseract.tesseract_cmd = cale
            break
    # Test rapid
    pytesseract.get_tesseract_version()
    TESS_OK = True
except Exception:
    TESS_OK = False

try:
    import easyocr
    EASY_OK = True
except ImportError:
    EASY_OK = False

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 11 — OCR Tesseract",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>📄</div>
    <div style='font-size:16px; font-weight:700; color:#2471a3;'>ZIUA 11</div>
    <div style='font-size:11px; color:#666;'>OCR — Extragere Text din Imagini</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 2 — Computer Vision")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 11 / 30 zile")
st.sidebar.progress(11/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 11:**
- OCR — cum functioneaza
- Tesseract vs EasyOCR
- Preprocesare imagine pentru OCR
- Extragere structurata (regex)
- Limbaj / configurare Tesseract
- Aplicatii APIA practice
""")

st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>📄</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#2471a3; font-weight:800;'>
            Ziua 11 — OCR: Extragere Text din Imagini
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 2 — Computer Vision &nbsp;|&nbsp;
            Tesseract + EasyOCR — documente APIA, formulare, etichete parcele
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "📷 OCR pe Imagine", "🔬 Preprocesare & Extractie", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII UTILITARE
# ══════════════════════════════════════════════════════════════════════════════
def genereaza_document_demo():
    """Genereaza o imagine demo cu text de tip formular APIA."""
    if not PIL_OK:
        return None
    w, h  = 600, 400
    img   = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw  = ImageDraw.Draw(img)

    # Chenar
    draw.rectangle([10, 10, w-10, h-10], outline=(0, 0, 0), width=2)

    # Antet
    draw.rectangle([10, 10, w-10, 60], fill=(23, 86, 152))
    draw.text((20, 20), "AGENTIA DE PLATI SI INTERVENTIE PENTRU AGRICULTURA",
              fill=(255,255,255))
    draw.text((20, 38), "Centrul Judetean Gorj — Cerere Unica de Plata 2024",
              fill=(200,220,255))

    # Continut formular
    linii = [
        ("Fermier:",         "IONESCU GHEORGHE"),
        ("CNP / CUI:",       "1780415180023"),
        ("Nr. cerere:",      "GJ-2024-001847"),
        ("Data depunere:",   "15.03.2024"),
        ("Suprafata totala:","12.45 ha"),
        ("Judet:",           "GORJ"),
        ("Localitate:",      "Targu Jiu"),
        ("Cultura declarata:","Grau de toamna"),
        ("Bloc fizic LPIS:", "GORJ_BF_00234"),
        ("NDVI verificat:",  "0.67 (normal)"),
    ]

    y = 75
    for i, (eticheta, valoare) in enumerate(linii):
        bg = (245, 248, 255) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([12, y, w-12, y+26], fill=bg)
        draw.text((20, y+5),  eticheta, fill=(80, 80, 80))
        draw.text((220, y+5), valoare,  fill=(0, 0, 0))
        y += 28

    draw.text((20, y+8), "Semnatura inspector: _______________", fill=(120,120,120))
    draw.text((350, y+8), f"Data: {date.today().strftime('%d.%m.%Y')}", fill=(120,120,120))
    return img

def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if CV2_OK else img

def ruleaza_ocr(img_pil, motor="auto", limba="ron+eng"):
    """Ruleaza OCR si returneaza (text, motor_folosit)."""
    if motor == "auto":
        motor = "tesseract" if TESS_OK else ("easyocr" if EASY_OK else None)

    if motor == "tesseract" and TESS_OK:
        try:
            config = f"--oem 3 --psm 6 -l {limba}"
            text   = pytesseract.image_to_string(img_pil, config=config)
            return text.strip(), "Tesseract"
        except Exception as e:
            return f"[Eroare Tesseract: {e}]", "Tesseract"

    if motor == "easyocr" and EASY_OK:
        try:
            @st.cache_resource(show_spinner=False)
            def incarca_reader(lb):
                return easyocr.Reader(lb, gpu=False, verbose=False)
            lb_list = ["ro","en"] if "ron" in limba else ["en"]
            reader  = incarca_reader(tuple(lb_list))
            img_np  = np.array(img_pil)
            results = reader.readtext(img_np)
            text    = "\n".join([r[1] for r in results])
            return text.strip(), "EasyOCR"
        except Exception as e:
            return f"[Eroare EasyOCR: {e}]", "EasyOCR"

    return "[Niciun motor OCR disponibil]", "—"

def extrage_campuri(text):
    """Extrage campuri structurate din textul OCR cu regex."""
    campuri = {}
    pattern_map = {
        "Nr. cerere":    r"Nr\.?\s*cerere[:\s]+([A-Z]{2}-\d{4}-\d+)",
        "CNP/CUI":       r"CNP\s*/?\s*CUI[:\s]+([\d]{10,13})",
        "Suprafata":     r"Suprafata[^:]*:\s*([\d]+[.,][\d]+)\s*ha",
        "Data":          r"Data\s*depunere[:\s]+(\d{2}\.\d{2}\.\d{4})",
        "Judet":         r"Judet[:\s]+([A-Z]{2,}(?:\s[A-Z]+)?)",
        "Bloc LPIS":     r"Bloc\s*fizic[^:]*:\s*([A-Z_0-9]+)",
        "NDVI":          r"NDVI[^:]*:\s*([\d]+[.,][\d]+)",
    }
    for camp, pattern in pattern_map.items():
        m = re.search(pattern, text, re.IGNORECASE)
        campuri[camp] = m.group(1).strip() if m else "—"
    return campuri

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Ce este OCR?")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **OCR** (Optical Character Recognition) converteste imaginile cu text
        in text digital editabil si procesabil.

        Fluxul de baza:
        1. Imagine (scan, fotografie, screenshot)
        2. Preprocesare (binarizare, denoising, deskew)
        3. Segmentare (linii → cuvinte → caractere)
        4. Recunoastere caracter cu caracter (model ML antrenat)
        5. Text brut → postprocesare (corectie, structurare)

        **La APIA, OCR permite:**
        - Digitalizarea cererilor PAC depuse pe hartie
        - Extragerea automata a ID-urilor de parcela din fotografii
        - Procesarea facturilor si documentelor justificative
        - Citirea etichetelor de identificare din teren
        - Arhivarea si cautarea documentelor vechi scanate
        """)

    with col2:
        st.markdown("""
        <div style='background:#eaf2ff; border-radius:10px; padding:14px;
             border-top:4px solid #2471a3;'>
            <div style='font-weight:700; color:#2471a3;'>Tesseract vs EasyOCR</div>
            <div style='font-size:11px; color:#555; margin-top:8px;'>
                <b>Tesseract</b> (Google, open-source):<br>
                + Matur, precis pe documente clare<br>
                + Suporta 100+ limbi inclusiv romana<br>
                + pip install pytesseract<br>
                - Necesita si binar separat instalat<br><br>
                <b>EasyOCR</b> (JaidedAI):<br>
                + Instalare simpla: pip install easyocr<br>
                + Bun pe imagini complexe / inclinate<br>
                + Model deep learning (CRAFT + CRNN)<br>
                - Mai lent, ~300 MB download modele
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Instalare")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Tesseract (recomandat pentru documente)")
        st.markdown("**Pasul 1 — Binar Tesseract (Windows):**")
        st.code(
            "# Descarca installerul de la:\n"
            "# github.com/UB-Mannheim/tesseract/wiki\n"
            "# Alege: tesseract-ocr-w64-setup-5.x.x.exe\n"
            "# Instaleaza in C:\\Program Files\\Tesseract-OCR\\\n"
            "# Bifeaza limba Romana la instalare!",
            language="bash"
        )
        st.markdown("**Pasul 2 — Pachet Python:**")
        st.code("pip install pytesseract", language="bash")
        st.code("""
import pytesseract
from PIL import Image

# Seteaza calea (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

img  = Image.open("document.jpg")
text = pytesseract.image_to_string(img, lang="ron+eng")
print(text)
""", language="python")

    with col2:
        st.markdown("#### EasyOCR (mai simplu de instalat)")
        st.code("pip install easyocr", language="bash")
        st.code("""
import easyocr
from PIL import Image
import numpy as np

# Prima rulare descarca modele (~300 MB)
reader = easyocr.Reader(["ro", "en"], gpu=False)

img    = np.array(Image.open("document.jpg"))
result = reader.readtext(img)

for (bbox, text, confidence) in result:
    print(f"{text!r:30} conf={confidence:.2f}")
""", language="python")

        st.markdown("#### Status instalare pe acest sistem:")
        c1, c2 = st.columns(2)
        with c1:
            if TESS_OK:
                try:
                    ver = pytesseract.get_tesseract_version()
                    st.success(f"Tesseract {ver} — OK")
                except Exception:
                    st.success("Tesseract instalat")
            else:
                st.error("Tesseract LIPSA")
        with c2:
            if EASY_OK:
                st.success("EasyOCR instalat")
            else:
                st.warning("EasyOCR absent")

        if not TESS_OK and not EASY_OK:
            st.info(
                "Fara motor OCR, aplicatia ruleaza in **mod demo** "
                "cu text pre-generat. Instaleaza unul din motoarele de mai sus."
            )

    st.divider()
    st.markdown("### Configuratii utile Tesseract (`--psm`)")
    psm_cfg = [
        ("--psm 3",  "Auto — detectie automata layout (implicit)"),
        ("--psm 6",  "Block de text uniform — cel mai bun pentru formulare"),
        ("--psm 7",  "O singura linie de text — ID parcela, numar cerere"),
        ("--psm 11", "Text sparse — etichete, stampile, text neordonat"),
        ("--psm 13", "Linie bruta — ignora Tesseract layout analysis"),
    ]
    for cfg, desc in psm_cfg:
        st.markdown(f"""
        <div style='display:flex; gap:12px; padding:6px 12px; margin:3px 0;
             background:#f8faff; border-radius:6px; font-size:12px;
             border-left:3px solid #2471a3;'>
            <code style='color:#2471a3; font-weight:700; min-width:80px;'>{cfg}</code>
            <span style='color:#555;'>{desc}</span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — OCR PE IMAGINE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### OCR pe imagine — upload sau document demo")

    col_up, col_cfg = st.columns([2, 1])

    with col_up:
        uploaded_ocr = st.file_uploader(
            "Incarca imagine cu text (formular, document, fotografie)",
            type=["jpg","jpeg","png","bmp","tiff"],
            key="uploader_ocr"
        )

        if uploaded_ocr:
            img_pil = Image.open(uploaded_ocr).convert("RGB")
            st.markdown("**Imagine incarcata:**")
            st.image(img_pil, use_container_width=True)
        else:
            img_pil = genereaza_document_demo()
            if img_pil:
                st.markdown("**Document demo generat (formular APIA simulat):**")
                st.image(img_pil, use_container_width=True)

    with col_cfg:
        st.markdown("#### Configurare OCR")

        motor_ales = st.selectbox(
            "Motor OCR",
            (["Auto (primul disponibil)"] +
             (["Tesseract"] if TESS_OK else []) +
             (["EasyOCR"]   if EASY_OK else []) +
             (["Demo (fara motor)"] if not TESS_OK and not EASY_OK else []))
        )
        limba_ocr  = st.selectbox("Limba", ["ron+eng", "eng", "ron"],
                                   help="ron = romana, eng = engleza")
        ruleaza_ocr_btn = st.button("Ruleaza OCR", type="primary",
                                     use_container_width=True)

        st.divider()
        st.markdown("**Sfat:** Pentru rezultate mai bune:")
        st.markdown("""
        - Imagine clara, fara blur
        - Text negru pe fundal alb
        - Rezolutie minima 150 DPI
        - Fara rotire / inclinare
        """)

    if ruleaza_ocr_btn and img_pil:
        st.divider()
        # Daca utilizatorul a uploadat o imagine reala si nu e niciun motor → eroare clara
        imagine_reala = uploaded_ocr is not None
        fara_motor    = not TESS_OK and not EASY_OK
        mod_demo_ales = "Demo" in motor_ales

        if mod_demo_ales or (fara_motor and not imagine_reala):
            # Text demo hardcodat — DOAR pentru documentul demo generat
            text_ocr   = """AGENTIA DE PLATI SI INTERVENTIE PENTRU AGRICULTURA
Centrul Judetean Gorj - Cerere Unica de Plata 2024

Fermier:           IONESCU GHEORGHE
CNP / CUI:         1780415180023
Nr. cerere:        GJ-2024-001847
Data depunere:     15.03.2024
Suprafata totala:  12.45 ha
Judet:             GORJ
Localitate:        Targu Jiu
Cultura declarata: Grau de toamna
Bloc fizic LPIS:   GORJ_BF_00234
NDVI verificat:    0.67 (normal)

Semnatura inspector: _______________   Data: 13.04.2026"""
            motor_folosit = "Demo"
        elif fara_motor and imagine_reala:
            # Imagine reala uploadata, dar niciun motor OCR instalat
            st.error("""
**Niciun motor OCR nu este instalat pe acest sistem.**

Imaginea ta a fost incarcata corect, dar pentru a citi textul din ea ai nevoie de:

**Optiunea 1 — Tesseract (recomandat):**
1. Descarca de la: github.com/UB-Mannheim/tesseract/wiki
2. Instaleaza `tesseract-ocr-w64-setup-5.x.x.exe`
3. Bifeaza **limba Romana** la instalare
4. Reporneste aplicatia Streamlit

**Optiunea 2 — EasyOCR (mai simplu):**
```
pip install easyocr
```
Reporneste aplicatia. Prima rulare descarca ~300 MB modele.
""")
            st.stop()
        else:
            with st.spinner("OCR in curs..."):
                motor_map = {
                    "Auto (primul disponibil)": "auto",
                    "Tesseract": "tesseract",
                    "EasyOCR":   "easyocr",
                }
                text_ocr, motor_folosit = ruleaza_ocr(
                    img_pil,
                    motor=motor_map.get(motor_ales, "auto"),
                    limba=limba_ocr
                )

        col_text, col_camp = st.columns([3, 2])
        with col_text:
            st.markdown(f"#### Text extras (motor: {motor_folosit})")
            st.text_area("", text_ocr, height=300, key="ocr_result")
            st.metric("Caractere extrase", len(text_ocr))

            buf_txt = text_ocr.encode("utf-8")
            st.download_button(
                "Descarca text extras (.txt)",
                data=buf_txt,
                file_name="text_ocr.txt",
                mime="text/plain"
            )

        with col_camp:
            st.markdown("#### Campuri extrase automat (regex)")
            campuri = extrage_campuri(text_ocr)
            for camp, val in campuri.items():
                gasit = val != "—"
                culoare = "#27ae60" if gasit else "#bdc3c7"
                icon    = "✅" if gasit else "—"
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between;
                     padding:6px 10px; margin:3px 0; border-radius:6px;
                     background:{"#f0fdf4" if gasit else "#f8f9fa"};
                     border-left:3px solid {culoare}; font-size:12px;'>
                    <span style='color:#555;'>{icon} {camp}</span>
                    <b style='color:#333;'>{val}</b>
                </div>
                """, unsafe_allow_html=True)

            n_gasit = sum(1 for v in campuri.values() if v != "—")
            st.metric("Campuri identificate", f"{n_gasit} / {len(campuri)}")

            if campuri:
                csv_campuri = pd.DataFrame(
                    [{"Camp": k, "Valoare": v} for k, v in campuri.items()]
                ).to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Descarca campuri CSV",
                    data=csv_campuri,
                    file_name="campuri_ocr.csv",
                    mime="text/csv"
                )
    elif not ruleaza_ocr_btn:
        st.info("Incarca o imagine sau foloseste documentul demo, apoi apasa **Ruleaza OCR**.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PREPROCESARE & EXTRACTIE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Preprocesare imagine pentru OCR mai precis")
    st.markdown("""
    Calitatea OCR depinde critic de calitatea imaginii.
    Aceste tehnici (din **Ziua 8 — OpenCV**) imbunatatesc dramatic acuratetea.
    """)

    if not CV2_OK:
        st.error("OpenCV necesar pentru preprocesare. Ruleaza: `pip install opencv-python`")
    else:
        # Generam o imagine cu text degradat pentru demo
        img_demo_pil = genereaza_document_demo()
        if img_demo_pil:
            img_bgr = cv2.cvtColor(np.array(img_demo_pil), cv2.COLOR_RGB2BGR)

            col_pp, col_rez_pp = st.columns([1, 2])
            with col_pp:
                st.markdown("#### Pasi de preprocesare")

                aplica_gray    = st.checkbox("1. Conversie Grayscale",   value=True)
                aplica_resize  = st.checkbox("2. Marire 2x (upscale)",   value=True)
                aplica_blur    = st.checkbox("3. Gaussian Blur (denoising)", value=False)
                aplica_thresh  = st.checkbox("4. Threshold Otsu (binarizare)", value=True)
                aplica_deskew  = st.checkbox("5. Corectie inclinare (deskew)",  value=False)
                aplica_morph   = st.checkbox("6. Morphological Opening", value=False)

            with col_rez_pp:
                img_pp = img_bgr.copy()
                pasi_aplicati = ["Original"]

                if aplica_resize:
                    h_pp, w_pp = img_pp.shape[:2]
                    img_pp = cv2.resize(img_pp, (w_pp*2, h_pp*2),
                                        interpolation=cv2.INTER_CUBIC)
                    pasi_aplicati.append("Resize 2x")

                if aplica_gray:
                    img_pp = cv2.cvtColor(img_pp, cv2.COLOR_BGR2GRAY)
                    pasi_aplicati.append("Grayscale")

                if aplica_blur:
                    img_pp = cv2.GaussianBlur(
                        img_pp if img_pp.ndim == 2 else
                        cv2.cvtColor(img_pp, cv2.COLOR_BGR2GRAY),
                        (3, 3), 0
                    )
                    pasi_aplicati.append("Gaussian Blur")

                if aplica_thresh:
                    gray_for_thresh = (img_pp if img_pp.ndim == 2
                                       else cv2.cvtColor(img_pp, cv2.COLOR_BGR2GRAY))
                    _, img_pp = cv2.threshold(
                        gray_for_thresh, 0, 255,
                        cv2.THRESH_BINARY + cv2.THRESH_OTSU
                    )
                    pasi_aplicati.append("Otsu Threshold")

                if aplica_deskew and img_pp.ndim == 2:
                    coords = np.column_stack(np.where(img_pp < 128))
                    if len(coords) > 10:
                        angle = cv2.minAreaRect(coords.astype(np.float32))[-1]
                        if angle < -45:
                            angle = 90 + angle
                        if abs(angle) > 0.5:
                            h_d, w_d = img_pp.shape
                            M = cv2.getRotationMatrix2D(
                                (w_d//2, h_d//2), angle, 1.0
                            )
                            img_pp = cv2.warpAffine(
                                img_pp, M, (w_d, h_d),
                                flags=cv2.INTER_CUBIC,
                                borderMode=cv2.BORDER_REPLICATE
                            )
                    pasi_aplicati.append(f"Deskew")

                if aplica_morph and img_pp.ndim == 2:
                    k_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
                    img_pp  = cv2.morphologyEx(img_pp, cv2.MORPH_OPEN, k_morph)
                    pasi_aplicati.append("Morphological Open")

                c_orig, c_proc = st.columns(2)
                with c_orig:
                    st.markdown("**Original**")
                    st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB),
                             use_container_width=True)
                with c_proc:
                    st.markdown("**Preprocesata**")
                    st.image(img_pp, use_container_width=True)

                st.caption(
                    "Pasi aplicati: " + " → ".join(pasi_aplicati) + ". "
                    "Imaginea preprocesata este mai clara pentru OCR — "
                    "text alb/negru, fara zgomot, contrast maxim."
                )

                # OCR pe imaginea preprocesata vs originala
                if st.button("Compara OCR: original vs preprocesata", type="primary"):
                    with st.spinner("Rulare OCR comparativa..."):
                        img_orig_pil = img_demo_pil
                        img_proc_pil = Image.fromarray(img_pp)

                        text_orig, m1 = ruleaza_ocr(img_orig_pil)
                        text_proc, m2 = ruleaza_ocr(img_proc_pil)

                    st.markdown("#### Comparatie rezultate OCR")
                    ca, cb = st.columns(2)
                    with ca:
                        st.markdown(f"**Original ({m1}):**")
                        st.text_area("", text_orig, height=200, key="ocr_orig")
                        st.metric("Caractere", len(text_orig))
                    with cb:
                        st.markdown(f"**Preprocesata ({m2}):**")
                        st.text_area("", text_proc, height=200, key="ocr_proc")
                        st.metric("Caractere", len(text_proc))

    st.divider()
    st.markdown("### Extragere structurata cu Regex — retete APIA")
    st.markdown("Regex pentru campurile cel mai des intalnite in documentele APIA:")

    retete = [
        ("ID cerere PAC",      r"[A-Z]{2}-\d{4}-\d{5,7}",        "GJ-2024-001847"),
        ("CNP fermier",        r"\b[1-9]\d{12}\b",                "1780415180023"),
        ("Suprafata (ha)",     r"(\d{1,4}[.,]\d{1,4})\s*ha",      "12.45 ha"),
        ("Data (zz.ll.aaaa)", r"\d{2}\.\d{2}\.\d{4}",            "15.03.2024"),
        ("Bloc LPIS",          r"[A-Z]{2,6}_BF_\d{3,6}",          "GORJ_BF_00234"),
        ("NDVI valoare",       r"NDVI[^:]*:\s*(0\.\d{2,3})",      "NDVI: 0.67"),
        ("Cod judet",          r"\b(AB|AR|AG|BC|BH|BN|BT|BV|BR|B|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)\b",
         "GORJ → GJ"),
    ]

    col1, col2 = st.columns(2)
    for i, (camp, pattern, exemplu) in enumerate(retete):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f8faff; border-left:3px solid #2471a3;
                 border-radius:0 8px 8px 0; padding:8px 12px; margin:5px 0;
                 font-size:11px;'>
                <div style='font-weight:700; color:#2471a3;'>{camp}</div>
                <code style='background:#eaf2ff; padding:2px 5px; border-radius:3px;
                     font-size:10px;'>{pattern}</code>
                <div style='color:#777; margin-top:2px;'>Ex: {exemplu}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 11")

    col1, col2 = st.columns(2)
    concepte = [
        ("OCR",                  "Optical Character Recognition — text din imagine → text digital"),
        ("Tesseract",            "Motor OCR Google open-source, 100+ limbi, precis pe documente curate"),
        ("EasyOCR",              "Motor OCR deep learning — mai simplu de instalat, bun pe imagini complexe"),
        ("pytesseract",          "Wrapper Python pentru Tesseract: image_to_string(), image_to_data()"),
        ("--psm 6",              "Page Segmentation Mode — bloc de text uniform, ideal pentru formulare"),
        ("lang='ron+eng'",       "Detectie text roman + englez simultan in Tesseract"),
        ("Preprocesare OCR",     "Resize 2x + Grayscale + Otsu threshold = crestere dramatica acuratete"),
        ("Deskew",               "Corectia inclinarii imaginii (rotire mica) — esential pentru documente scanate"),
        ("regex extragere",      "re.search(pattern, text) — extrage campuri structurate din text brut OCR"),
        ("image_to_data()",      "Tesseract returneaza si coordonatele fiecarui cuvant — pentru highlighting"),
        ("Digitalizare APIA",    "OCR transforma documentele scanate in date procesabile automat"),
        ("Pipeline complet",     "Imagine → Preprocesare OpenCV → OCR → Regex → DataFrame → Export CSV"),
    ]
    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#eaf2ff; border-left:3px solid #2471a3;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#2471a3; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
import pytesseract
import cv2
import numpy as np
import re
from PIL import Image

# 1. Configurare Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

# 2. Preprocesare imagine pentru OCR maxim
def preprocesare_ocr(img_bgr):
    # Marire 2x
    h, w = img_bgr.shape[:2]
    img  = cv2.resize(img_bgr, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
    # Grayscale + Otsu threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binar = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binar

# 3. OCR cu Tesseract
img_bgr  = cv2.imread("formular_apia.jpg")
img_pp   = preprocesare_ocr(img_bgr)
img_pil  = Image.fromarray(img_pp)
text     = pytesseract.image_to_string(img_pil,
                                        config="--oem 3 --psm 6 -l ron+eng")

# 4. Extragere campuri cu regex
nr_cerere = re.search(r"[A-Z]{2}-\\d{4}-\\d+", text)
suprafata = re.search(r"([\\d]+[.,][\\d]+)\\s*ha", text)
data_dep  = re.search(r"\\d{2}\\.\\d{2}\\.\\d{4}", text)

print(f"Cerere:    {nr_cerere.group() if nr_cerere else 'negasit'}")
print(f"Suprafata: {suprafata.group(1) if suprafata else 'negasit'} ha")
print(f"Data:      {data_dep.group() if data_dep else 'negasit'}")

# 5. EasyOCR (alternativa fara binar separat)
import easyocr
reader = easyocr.Reader(["ro", "en"], gpu=False)
result = reader.readtext(np.array(img_pil))
for (bbox, text_cuvant, conf) in result:
    if conf > 0.5:
        print(f"{text_cuvant}  (conf={conf:.2f})")
""", language="python")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Aplicatie APIA — digitalizare cereri PAC")
        st.markdown("""
        Un sistem OCR operational la APIA ar putea:

        1. **Scana** cererile PAC depuse pe hartie
        2. **Extrage automat** datele: CNP, suprafata, culturi, blocuri LPIS
        3. **Valida** datele extrase contra bazei de date LPIS
        4. **Marca** automat discrepantele pentru verificare manuala
        5. **Popula** sistemul IACS fara introducere manuala

        Estimare economii: **60-80% reducere** a timpului de introducere date
        pentru 1000+ cereri/an la nivelul unui CJ.
        """)
    with col_b:
        st.markdown("#### Ziua 12 — Sinteza Modul 2")
        st.markdown("""
        Ultima zi din **Modulul 2 — Computer Vision** reuneste:

        - Upload imagine drone
        - **YOLO** — detectie obiecte
        - **NDVI** — calcul si harta
        - **OpenCV** — preprocesare si muchii
        - **OCR** — extragere text din etichete
        - **Detectie anomalii** — raport prioritizare
        - Export complet (imagini + CSV + raport)

        O aplicatie completa de analiza imagini agricole —
        **tot ce am invatat in Modulul 2, intr-o singura interfata**.
        """)

    st.success(
        "**Ziua 11 finalizata!** OCR cu Tesseract si EasyOCR — "
        "extragere text din documente APIA, preprocesare OpenCV si structurare regex. "
        "Continua cu **Ziua 12 — Sinteza Modul 2**."
    )
