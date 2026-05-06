"""
Ziua 21 — Generare Imagini AI: Teorie si Instrumente (fara modele locale)
Modul 4: AI Generativ Local
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""
import streamlit as st
import datetime

st.set_page_config(page_title="Ziua 21 — Generare Imagini AI", page_icon="IMG", layout="wide")

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:28px; font-weight:900; color:#8e44ad;'>IMG</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 21</div>
    <div style='font-size:11px; color:#666;'>Generare Imagini AI — Teorie</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI Generativ Local")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 21 / 30 zile")
st.sidebar.progress(21 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#8e44ad; border-radius:8px; padding:10px 12px; color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:40px; font-weight:900; color:#8e44ad;'>IMG</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 21 — Generare Imagini AI: Teorie si Instrumente
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Stable Diffusion · DALL-E · Midjourney · Aplicatii agricole
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.info(
    "Aceasta zi acopera teoria generarii de imagini cu AI. "
    "Stable Diffusion local necesita GPU dedicat (4+ GB VRAM) — "
    "pentru calculatoare fara GPU folosim instrumente online gratuite."
)
st.divider()

tab1, tab2, tab3 = st.tabs(["Cum functioneaza", "Instrumente gratuite", "Aplicatii agricole"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cum genereaza AI o imagine?")
        st.markdown("""
**Modelele de tip Diffusion (Stable Diffusion, DALL-E, Midjourney):**

1. **Antrenare** — modelul invata dintr-un miliard de perechi imagine+text
2. **Encoding** — textul tau (prompt) e transformat in vector numeric
3. **Noise → Imagine** — modelul porneste de la zgomot aleator si il
   "curata" pas cu pas pana obtine imaginea dorita
4. **Denoising** — 20-50 de pasi de rafinare progresiva

**Arhitecturi principale:**
| Model | Creator | Acces |
|---|---|---|
| Stable Diffusion | Stability AI | Open-source, local |
| DALL-E 3 | OpenAI | API platit |
| Midjourney | Midjourney | Abonament $10/luna |
| Flux | Black Forest Labs | Open-source |
| Ideogram | Ideogram AI | Gratuit online |

**De ce nu il rulam local azi?**
- Stable Diffusion = minim 4 GB VRAM GPU dedicat
- Pe CPU = 5-20 minute per imagine
- Alternativa: instrumente online gratuite (tab urmator)
""")
    with col2:
        st.subheader("Prompt engineering pentru imagini")
        st.markdown("""
**Structura unui prompt bun:**
```
[subiect principal], [stil], [calitate], [iluminare], [unghi]
```

**Exemple agricole:**
```
aerial view of wheat field in Romania,
drone photography, golden hour,
high resolution, professional

agricultural parcel map, satellite view,
NDVI color scale, green to red,
scientific visualization, high detail

Romanian farmer inspecting crops,
professional photography, natural light,
documentary style
```

**Negative prompt** (ce sa evite):
```
blurry, low quality, distorted,
watermark, text, ugly
```

**Parametri importanti:**
- **Steps**: 20 = rapid, 50 = calitate
- **CFG Scale**: 7 = echilibru prompt/creativitate
- **Sampler**: DPM++ 2M Karras (recomandat)
""")

with tab2:
    st.subheader("Instrumente online gratuite — fara GPU necesar")

    instrumente = [
        {
            "nume": "Ideogram AI",
            "url": "ideogram.ai",
            "gratuit": "10 imagini/zi gratuit",
            "calitate": "Excelenta, text in imagini",
            "utilizare": "Diagrame, infografice, prezentari UCB",
            "culoare": "#1a5276",
        },
        {
            "nume": "Adobe Firefly",
            "url": "firefly.adobe.com",
            "gratuit": "25 credite/luna gratuit",
            "calitate": "Profesionala, sigura comercial",
            "utilizare": "Materiale didactice, brosuri APIA",
            "culoare": "#e74c3c",
        },
        {
            "nume": "Bing Image Creator",
            "url": "bing.com/images/create",
            "gratuit": "100% gratuit cu cont Microsoft",
            "calitate": "Buna (DALL-E 3)",
            "utilizare": "Ilustratii rapide pentru cursuri",
            "culoare": "#2980b9",
        },
        {
            "nume": "Leonardo AI",
            "url": "leonardo.ai",
            "gratuit": "150 credite/zi gratuit",
            "calitate": "Foarte buna, multe modele",
            "utilizare": "Harti agricole stilizate, diagrame",
            "culoare": "#8e44ad",
        },
    ]

    for inst in instrumente:
        st.markdown(f"""
<div style='background:white; border-radius:8px; padding:12px 16px; margin:6px 0;
     box-shadow:0 2px 6px rgba(0,0,0,0.07); border-left:4px solid {inst["culoare"]};
     display:flex; gap:20px; align-items:center;'>
    <div style='min-width:150px;'>
        <div style='font-weight:700; color:{inst["culoare"]}; font-size:14px;'>{inst["nume"]}</div>
        <div style='font-size:10px; color:#888; font-family:monospace;'>{inst["url"]}</div>
    </div>
    <div style='flex:1; font-size:11px; line-height:1.7;'>
        <b>Gratuit:</b> {inst["gratuit"]}<br>
        <b>Calitate:</b> {inst["calitate"]}<br>
        <b>Util pentru:</b> {inst["utilizare"]}
    </div>
</div>
""", unsafe_allow_html=True)

with tab3:
    st.subheader("Aplicatii concrete in agricultura si academia")
    st.markdown("""
| Utilizare | Prompt exemplu | Instrument recomandat |
|---|---|---|
| Ilustratie curs UCB | `wheat field Romania, aerial view, educational diagram` | Bing Creator (gratuit) |
| Infografic PAC | `EU agricultural subsidies infographic, clean design, blue` | Ideogram (text precis) |
| Cover articol ISI | `GNSS satellite signal visualization, scientific illustration` | Adobe Firefly |
| Harta stilizata | `Romania agricultural map, regions colored by crop type` | Leonardo AI |
| Foto prezentare | `drone flying over corn field, professional photography` | Bing Creator |

**Integrare in Streamlit** — afisarea imaginilor generate:
```python
import streamlit as st
import requests
from PIL import Image
import io

# Daca ai API (ex. Stability AI $10/luna):
response = requests.post(
    "https://api.stability.ai/v1/generation/...",
    headers={"Authorization": "Bearer API_KEY"},
    json={"text_prompts": [{"text": "wheat field Romania"}]}
)
img = Image.open(io.BytesIO(response.content))
st.image(img, caption="Generat de AI")

# Sau afisezi direct imaginea descarcata manual:
st.image("imagine_generata.png", caption="Parcel agricol generat AI")
```
""")

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#8e44ad 0%,#1a5276 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 21 — FINALIZATA (Teorie)</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
Stable Diffusion · DALL-E · Midjourney · Instrumente gratuite online · Prompt engineering imagini
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 22 — Generator Continut Academic cu LLM
</div>
</div>
""", unsafe_allow_html=True)
