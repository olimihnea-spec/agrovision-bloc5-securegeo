"""
ZIUA 7 — YOLOv8: Detectie Obiecte in Imagini Agricole
Modul 2: Computer Vision
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
Teza: Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone
"""

import streamlit as st
import numpy as np
from datetime import date
import io

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    from ultralytics import YOLO
    YOLO_OK = True
except ImportError:
    YOLO_OK = False

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 7 — YOLOv8",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>📷</div>
    <div style='font-size:16px; font-weight:700; color:#c0392b;'>ZIUA 7</div>
    <div style='font-size:11px; color:#666;'>YOLOv8 — Computer Vision</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 2 — Computer Vision")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 7 / 30 zile")
st.sidebar.progress(7/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 7:**
- Deep Learning vs ML clasic
- Retele neuronale convolutionale (CNN)
- YOLO — You Only Look Once
- Bounding Box, Confidence, NMS
- YOLOv8 arhitectura
- Transfer Learning
- Fine-tuning pe culturi agricole
""")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>📷</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#c0392b; font-weight:800;'>
            Ziua 7 — YOLOv8: Detectie Obiecte in Imagini
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 2 — Computer Vision &nbsp;|&nbsp;
            De la pixeli la cultura identificata — direct din imagini drone
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px; padding:10px 18px; color:white; margin-bottom:12px;
     font-size:12px;'>
    Legatura directa cu teza de doctorat:
    <b>"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"</b>
    &nbsp;|&nbsp; YOLOv8 = instrumentul principal de detectie din cercetare
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "⚙️ Setup & Model", "📷 Detectie Live", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### De ce YOLO in loc de KNN/SVM pe NDVI?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background:#f8f9fa; border-radius:10px; padding:14px;
             border-top:4px solid #3498db;'>
            <div style='font-weight:700; color:#3498db; font-size:14px;'>
                ML Clasic — Ziua 1 (KNN / SVM)
            </div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Input:</b> valori numerice extrase (NDVI_mai, NDVI_iulie...)<br>
                <b>Proces:</b> calcul distante sau hiperplane intre puncte<br>
                <b>Output:</b> o eticheta per randul din tabel<br><br>
                <b>Avantaje:</b> rapid, interpretabil, functioneaza cu putine date<br>
                <b>Dezavantaje:</b> trebuie sa extragi manual featurile din imagini;
                nu vede spatialitatea pixelilor
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#f8f9fa; border-radius:10px; padding:14px;
             border-top:4px solid #c0392b;'>
            <div style='font-weight:700; color:#c0392b; font-size:14px;'>
                Deep Learning — YOLO (Ziua 7)
            </div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Input:</b> imaginea bruta (pixeli, 640x640)<br>
                <b>Proces:</b> retea neuronala cu milioane de parametri
                invata automat ce featuri conteaza<br>
                <b>Output:</b> bounding boxes + clase + confidence per obiect<br><br>
                <b>Avantaje:</b> lucreaza direct pe imagine, detecteaza
                mai multe obiecte simultan, generalizeaza pe imagini noi<br>
                <b>Dezavantaje:</b> necesita mii de imagini etichetate,
                GPU recomandat pentru antrenare
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Cum functioneaza YOLO?")

    st.markdown("""
    **YOLO** = *You Only Look Once* — in loc sa scaneze imaginea de mai multe ori
    (cum fac algoritmii mai vechi), YOLO o analizeaza **o singura data** si returneaza
    toate detectiile simultan.
    """)

    pasi = [
        ("1", "Resize imagine",
         "Imaginea este redimensionata la 640x640 pixeli indiferent de dimensiunea originala",
         "#3498db"),
        ("2", "Backbone CNN",
         "O retea convolutionala (CSPDarknet) extrage featuri din imagine la mai multe rezolutii",
         "#8e44ad"),
        ("3", "Neck (FPN)",
         "Feature Pyramid Network combina featurile de la rezolutii diferite pentru a detecta obiecte mici si mari",
         "#27ae60"),
        ("4", "Head — predictii",
         "Pentru fiecare zona din imagine prezice: coordonate box (x,y,w,h), confidence, probabilitati clase",
         "#e74c3c"),
        ("5", "NMS",
         "Non-Maximum Suppression elimina box-urile duplicate — pastreaza doar cel mai bun per obiect",
         "#d35400"),
    ]

    for nr, etapa, desc, culoare in pasi:
        st.markdown(f"""
        <div style='display:flex; gap:12px; align-items:flex-start; margin:6px 0;
             background:white; border-radius:8px; padding:10px 14px;
             box-shadow:0 1px 3px rgba(0,0,0,0.06);'>
            <div style='background:{culoare}; color:white; border-radius:50%;
                 width:26px; height:26px; display:flex; align-items:center;
                 justify-content:center; font-weight:800; font-size:12px;
                 flex-shrink:0; margin-top:2px;'>{nr}</div>
            <div>
                <div style='font-weight:700; color:{culoare}; font-size:13px;'>{etapa}</div>
                <div style='font-size:12px; color:#555; margin-top:2px;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Versiunile YOLOv8")
        versiuni = [
            ("YOLOv8n", "nano",    "~6 MB",   "cea mai rapida, ideala demo",  "#27ae60"),
            ("YOLOv8s", "small",   "~22 MB",  "echilibru viteza/acuratete",   "#3498db"),
            ("YOLOv8m", "medium",  "~50 MB",  "acuratete buna, GPU recomandat","#8e44ad"),
            ("YOLOv8l", "large",   "~87 MB",  "acuratete inalta",             "#e67e22"),
            ("YOLOv8x", "extra",   "~136 MB", "cel mai precis, GPU necesar",  "#c0392b"),
        ]
        for model, dim, marime, desc, culoare in versiuni:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                 padding:7px 12px; margin:3px 0; border-radius:6px;
                 border-left:4px solid {culoare}; background:#fafafa;
                 font-size:12px;'>
                <span style='font-weight:700; color:{culoare};'>{model}</span>
                <span style='color:#777;'>{dim}</span>
                <span style='color:#888;'>{marime}</span>
                <span style='color:#555;'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Azi folosim **YOLOv8n** — descarca automat ~6 MB, ruleaza pe CPU.")

    with col2:
        st.markdown("### Transfer Learning — de ce e important")
        st.markdown("""
        <div style='background:#fef9e7; border-radius:10px; padding:14px;
             border-top:4px solid #f39c12;'>
            <div style='font-weight:700; color:#f39c12;'>Nu antrenam de la zero!</div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                YOLOv8n a fost deja antrenat pe <b>COCO</b> — un dataset cu
                120.000 de imagini si 80 de clase (masini, persoane, animale...).<br><br>
                <b>Transfer Learning</b> inseamna ca luam aceasta retea
                care <i>stie deja sa vada</i> si o <b>fine-tunam</b> pe
                imaginile noastre cu culturi agricole.<br><br>
                In loc de milioane de imagini si saptamani de antrenare,
                avem nevoie de cateva sute de imagini etichetate
                si cateva ore pe un GPU gratuit (Google Colab).<br><br>
                <b>Acesta este exact fluxul din teza de doctorat.</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Clasele COCO (pre-antrenat)")
        st.markdown("""
        Modelul YOLOv8n standard detecteaza 80 de clase generale.
        Pentru culturi agricole specifice (grau, porumb, floarea-soarelui)
        este nevoie de **fine-tuning** pe un dataset agricol etichetat.

        **Roboflow Universe** are sute de dataset-uri agricole publice
        cu imagini drone gata etichetate — cauta *"crop detection aerial"*
        sau *"wheat detection drone"*.
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SETUP & MODEL
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Instalare si configurare YOLOv8")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Pas 1 — Instalare")
        st.code("pip install ultralytics", language="bash")
        st.markdown("""
        Instaleaza automat: `ultralytics`, `torch`, `torchvision`,
        `opencv-python`, `Pillow`, `numpy`, `pandas`, `matplotlib`.

        Prima rulare descarca automat **YOLOv8n.pt** (~6 MB) din internet
        si il salveaza local. Rulari ulterioare folosesc versiunea locala.
        """)

        st.markdown("#### Pas 2 — Cod minim functional")
        st.code("""
from ultralytics import YOLO
from PIL import Image

# Incarca modelul (descarca automat la prima rulare)
model = YOLO("yolov8n.pt")

# Detectie pe o imagine
results = model("imagine.jpg", conf=0.25)

# Imagine cu bounding boxes desenate
annotated = results[0].plot()   # numpy array BGR
img = Image.fromarray(annotated[:, :, ::-1])   # BGR -> RGB

# Rezultate numerice
boxes = results[0].boxes
for box in boxes:
    cls_id = int(box.cls)
    conf   = float(box.conf)
    label  = model.names[cls_id]
    coords = box.xyxy[0].tolist()   # [x1, y1, x2, y2]
    print(f"{label}: {conf:.2f} — {coords}")
""", language="python")

    with col2:
        st.markdown("#### Pas 3 — Fine-tuning pe culturi agricole")
        st.code("""
from ultralytics import YOLO

# Pleaca de la modelul pre-antrenat pe COCO
model = YOLO("yolov8n.pt")

# Fine-tuning pe dataset-ul tau
model.train(
    data="dataset_culturi/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    project="culturi_gorj",
    name="yolov8n_culturi_v1",
)

# Cel mai bun model salvat automat in:
# culturi_gorj/yolov8n_culturi_v1/weights/best.pt
""", language="python")

        st.markdown("#### Format dataset (data.yaml)")
        st.code("""
# data.yaml — descris structura dataset-ului
path:  dataset_culturi/
train: images/train/
val:   images/val/

nc: 5   # numar clase
names:
  - Grau
  - Floarea-soarelui
  - Porumb
  - Lucerna
  - Fanete
""", language="yaml")

        st.markdown("#### Unde gasesti dataset-uri agricole gratuite")
        st.markdown("""
        <div style='background:#e8f4fd; border-radius:8px; padding:12px;
             border-left:4px solid #2980b9; font-size:12px;'>
            <b>Roboflow Universe</b> — cauta: <i>crop detection aerial</i>,
            <i>wheat detection drone</i>, <i>corn field detection</i><br><br>
            Filtreaza: <b>License = CC BY 4.0</b> (liber pentru cercetare)<br><br>
            Descarca in format <b>YOLOv8</b> — primesti direct structura
            de foldere si fisierul <code>data.yaml</code> gata de utilizat.<br><br>
            <b>Google Colab</b> ofera GPU gratuit pentru antrenare —
            ruleaza <code>model.train()</code> in cloud fara sa instalezi nimic local.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Status instalare pe acest sistem")

    c1, c2, c3 = st.columns(3)
    with c1:
        if YOLO_OK:
            try:
                import ultralytics
                st.success(f"ultralytics {ultralytics.__version__} instalat")
            except Exception:
                st.success("ultralytics instalat")
        else:
            st.error("ultralytics LIPSA — ruleaza: `pip install ultralytics`")
    with c2:
        if PIL_OK:
            from PIL import __version__ as pv
            st.success(f"Pillow {pv} instalat")
        else:
            st.error("Pillow LIPSA — ruleaza: `pip install Pillow`")
    with c3:
        try:
            import torch
            st.success(f"PyTorch {torch.__version__} instalat")
        except ImportError:
            st.warning("PyTorch absent — se instaleaza odata cu ultralytics")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DETECTIE LIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if not YOLO_OK:
        st.error("""
        **ultralytics nu este instalat.**

        Ruleaza in terminal:
        ```
        pip install ultralytics
        ```
        Apoi reporneste aplicatia Streamlit.
        """)
        st.stop()

    if not PIL_OK:
        st.error("Pillow nu este instalat. Ruleaza: `pip install Pillow`")
        st.stop()

    st.markdown("### Detectie pe imagini — YOLOv8n")

    col_cfg, col_rez = st.columns([1, 2])

    with col_cfg:
        st.markdown("#### Configurare")

        imagine_uploadata = st.file_uploader(
            "Incarca o imagine (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Imagini drone agricole, fotografii parcele, orice imagine cu obiecte"
        )

        conf_threshold = st.slider(
            "Prag confidence (conf)",
            min_value=0.05, max_value=0.95,
            value=0.25, step=0.05,
            help="Sub acest prag, detectiile sunt ignorate. Scade pentru mai multe detectii."
        )

        iou_threshold = st.slider(
            "Prag IOU (NMS)",
            min_value=0.1, max_value=0.9,
            value=0.45, step=0.05,
            help="Threshold pentru Non-Maximum Suppression. Valori mici = mai putine box-uri duplicate."
        )

        arata_labels  = st.checkbox("Arata etichete pe imagine", value=True)
        arata_conf    = st.checkbox("Arata confidence pe imagine", value=True)

        detecteaza = st.button("Detecteaza", type="primary",
                               use_container_width=True,
                               disabled=(imagine_uploadata is None))

        if imagine_uploadata is None:
            st.info("Incarca o imagine pentru a activa detectia.")

    with col_rez:
        if imagine_uploadata and detecteaza:
            with st.spinner("Incarcare model si detectie in curs..."):
                try:
                    @st.cache_resource(show_spinner=False)
                    def incarca_model():
                        return YOLO("yolov8n.pt")

                    model = incarca_model()

                    img_bytes = imagine_uploadata.read()
                    img_pil   = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                    img_np    = np.array(img_pil)

                    results = model(
                        img_np,
                        conf=conf_threshold,
                        iou=iou_threshold,
                        verbose=False
                    )
                    result = results[0]

                    # Imagine adnotata
                    annotated_bgr = result.plot(
                        labels=arata_labels,
                        conf=arata_conf
                    )
                    annotated_rgb = annotated_bgr[:, :, ::-1]
                    img_adnotata  = Image.fromarray(annotated_rgb)

                    col_orig, col_det = st.columns(2)
                    with col_orig:
                        st.markdown("**Original:**")
                        st.image(img_pil, use_container_width=True)
                    with col_det:
                        st.markdown("**Detectii YOLOv8n:**")
                        st.image(img_adnotata, use_container_width=True)

                    # Tabel detectii
                    boxes = result.boxes
                    if boxes is not None and len(boxes) > 0:
                        n_det = len(boxes)
                        st.markdown(f"#### {n_det} obiect(e) detectat(e)")

                        rows_det = []
                        for box in boxes:
                            cls_id = int(box.cls[0])
                            conf_v = float(box.conf[0])
                            label  = model.names[cls_id]
                            x1, y1, x2, y2 = [round(float(v), 1)
                                               for v in box.xyxy[0].tolist()]
                            w = round(x2 - x1, 1)
                            h = round(y2 - y1, 1)
                            rows_det.append({
                                "Obiect":      label,
                                "Confidence":  f"{conf_v*100:.1f}%",
                                "X1,Y1":       f"({x1}, {y1})",
                                "Latime x Inaltime": f"{w} x {h} px",
                            })

                        det_df = sorted(rows_det,
                                        key=lambda r: float(r["Confidence"].replace("%","")),
                                        reverse=True)
                        st.dataframe(det_df, use_container_width=True, hide_index=True)

                        # KPI-uri
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("Obiecte detectate", n_det)
                        with c2:
                            confs = [float(b.conf[0]) for b in boxes]
                            st.metric("Confidence medie", f"{np.mean(confs)*100:.1f}%")
                        with c3:
                            clase_det = list({model.names[int(b.cls[0])]
                                             for b in boxes})
                            st.metric("Clase unice", len(clase_det))

                        if PLOTLY_OK:
                            # Distributie clase detectate
                            cls_counts = {}
                            for box in boxes:
                                lbl = model.names[int(box.cls[0])]
                                cls_counts[lbl] = cls_counts.get(lbl, 0) + 1
                            fig_cls = go.Figure(go.Bar(
                                x=list(cls_counts.keys()),
                                y=list(cls_counts.values()),
                                marker_color="#c0392b",
                                text=list(cls_counts.values()),
                                textposition="outside",
                            ))
                            fig_cls.update_layout(
                                yaxis_title="Nr. detectii",
                                height=250,
                                margin=dict(t=10, b=40, l=40, r=20),
                            )
                            st.plotly_chart(fig_cls, use_container_width=True)

                        # Download imagine adnotata
                        buf_out = io.BytesIO()
                        img_adnotata.save(buf_out, format="JPEG", quality=90)
                        buf_out.seek(0)
                        st.download_button(
                            "Descarca imaginea cu detectii",
                            data=buf_out,
                            file_name=f"detectie_{imagine_uploadata.name}",
                            mime="image/jpeg"
                        )

                    else:
                        st.warning(
                            f"Nicio detectie cu confidence > {conf_threshold:.0%}. "
                            "Incearca sa scazi pragul de confidence."
                        )

                except Exception as e:
                    st.error(f"Eroare la detectie: {e}")
                    st.info(
                        "Daca eroarea este legata de download model, "
                        "verifica conexiunea la internet si reincearca."
                    )

        elif imagine_uploadata and not detecteaza:
            img_pil = Image.open(imagine_uploadata).convert("RGB")
            st.markdown("**Imaginea incarcata (apasa Detecteaza):**")
            st.image(img_pil, use_container_width=True)
            w, h = img_pil.size
            st.caption(f"Dimensiune: {w} x {h} px")

        else:
            st.markdown("""
            <div style='background:#f8f9fa; border-radius:12px; padding:40px;
                 text-align:center; color:#aaa; border:2px dashed #ddd;'>
                <div style='font-size:48px;'>📷</div>
                <div style='font-size:14px; margin-top:10px;'>
                    Incarca o imagine din coloana stanga
                </div>
                <div style='font-size:12px; margin-top:6px;'>
                    JPG sau PNG — fotografie drone, parcel agricola, orice imagine
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 7")

    col1, col2 = st.columns(2)
    concepte = [
        ("CNN",                  "Retea neuronala convolutionala — invata featuri spatiale din pixeli"),
        ("YOLO",                 "You Only Look Once — detectie completa intr-o singura trecere"),
        ("Bounding Box",         "Dreptunghi care incadreaza obiectul: [x1, y1, x2, y2] sau [x,y,w,h]"),
        ("Confidence",           "Cat de sigur este modelul ca exista un obiect in acea zona [0,1]"),
        ("IOU",                  "Intersection over Union — masura suprapunere intre doua bounding boxes"),
        ("NMS",                  "Non-Maximum Suppression — elimina detectiile duplicate per obiect"),
        ("Transfer Learning",    "Folosesti o retea preantrenata ca punct de start — economisesti timp si date"),
        ("Fine-tuning",          "Reantrenezi ultimele straturi pe datele tale specifice (culturi agricole)"),
        ("YOLOv8n",              "Versiunea nano — 6 MB, rapida pe CPU, buna pentru demo si prototipare"),
        ("model.names",          "Dictionarul claselor: {0: 'person', 1: 'car', ...} — specific fiecarui model"),
        ("result.plot()",        "Returneaza numpy array BGR cu bounding boxes desenate pe imagine"),
        ("data.yaml",            "Fisierul de configurare dataset — defineste caile si numele claselor"),
    ]
    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#fff5f5; border-left:3px solid #c0392b;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#c0392b; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
from ultralytics import YOLO
from PIL import Image
import numpy as np

# 1. Incarca model (descarca automat prima data)
model = YOLO("yolov8n.pt")          # pre-antrenat COCO
# model = YOLO("best.pt")           # modelul tau fine-tunat

# 2. Detectie pe imagine
results = model("fotografie_drone.jpg", conf=0.25, iou=0.45)
result  = results[0]

# 3. Imagine adnotata
img_adnotata = Image.fromarray(result.plot()[:, :, ::-1])   # BGR->RGB
img_adnotata.save("detectie_output.jpg")

# 4. Acces rezultate numerice
for box in result.boxes:
    label  = model.names[int(box.cls[0])]
    conf   = float(box.conf[0])
    x1,y1,x2,y2 = box.xyxy[0].tolist()
    print(f"{label}: {conf:.2f} la ({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f})")

# 5. Fine-tuning pe dataset propriu
model = YOLO("yolov8n.pt")
model.train(
    data="dataset_culturi/data.yaml",
    epochs=50,
    imgsz=640,
    project="culturi_gorj"
)
""", language="python")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Legatura cu teza de doctorat")
        st.markdown("""
        In teza **"Contributii privind recunoasterea automata a culturilor
        cu ajutorul unei Drone"** (Universitatea din Petrosani, 2024),
        fluxul de lucru este exact cel de mai sus:

        1. Zbor drona deasupra parcelelor din Gorj
        2. Imagini RGB/multispectrale colectate
        3. Etichetare manuala (Roboflow sau LabelImg)
        4. Antrenare YOLOv8 pe imaginile etichetate
        5. Validare pe parcele nevazute de model
        6. Rezultate comparate cu datele LPIS din APIA

        Aplicatia din aceasta zi reproduce **exact** acest flux,
        cu un model pre-antrenat ca punct de demonstratie.
        """)
    with col_b:
        st.markdown("#### Ziua 8 — ce urmeaza")
        st.markdown("""
        **OpenCV — bazele procesarii de imagini**

        Inainte de a folosi modele complexe ca YOLO, trebuie sa intelegem
        operatiile fundamentale pe imagini:

        - Citire, scriere, redimensionare imagini
        - Spatii de culoare (RGB, BGR, HSV, Grayscale)
        - Filtre si detectie muchii (Canny, Sobel)
        - Histograme si egalizare contrast
        - Operatii morfologice

        Aceste tehnici sunt folosite si ca preprocesare inainte de YOLO.
        """)

    st.success(
        "**Ziua 7 finalizata!** YOLOv8 pentru detectie obiecte in imagini — "
        "de la pixeli la bounding boxes in cateva linii de cod. "
        "Continua cu **Ziua 8 — OpenCV bazele**."
    )
