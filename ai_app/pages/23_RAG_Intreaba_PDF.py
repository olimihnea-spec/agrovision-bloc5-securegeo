"""
Ziua 23 — RAG Simplu: Intreaba un Document PDF
Modul 4: AI Generativ Local
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import datetime
import time
import re
import math
from collections import Counter

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from pypdf import PdfReader
    PYPDF_OK = True
except ImportError:
    try:
        from PyPDF2 import PdfReader
        PYPDF_OK = True
    except ImportError:
        PYPDF_OK = False

OLLAMA_URL = "http://localhost:11434"

# ══════════════════════════════════════════════════════════════════════════════
# TEXT DEMO (simulare document PAC — fara PDF real necesar)
# ══════════════════════════════════════════════════════════════════════════════

TEXT_DEMO_PAC = """
REGULAMENTUL (UE) 2021/2116 AL PARLAMENTULUI EUROPEAN SI AL CONSILIULUI
din 2 decembrie 2021
privind finantarea, gestionarea si monitorizarea politicii agricole comune

TITLUL I — DISPOZITII GENERALE

Articolul 1 — Obiect
Prezentul regulament stabileste norme privind finantarea cheltuielilor din domeniul politicii
agricole comune (PAC), inclusiv cheltuielile pentru dezvoltarea rurala.

Articolul 2 — Fonduri
PAC este finantata din Fondul European de Garantare Agricola (FEGA) si Fondul European
Agricol pentru Dezvoltare Rurala (FEADR).

TITLUL II — SISTEMUL INTEGRAT DE ADMINISTRARE SI CONTROL (IACS)

Articolul 65 — IACS
Statele membre instituie si exploateaza un sistem integrat de administrare si control (IACS).
IACS cuprinde: (a) un sistem de identificare a parcelelor agricole (LPIS);
(b) un sistem de identificare si inregistrare a drepturilor la plata;
(c) cereri de ajutor si cereri de plata; (d) un sistem integrat de control.

Articolul 66 — Sistemul de identificare a parcelelor agricole (LPIS)
LPIS se bazeaza pe harti sau documente cadastrale sau alte date cartografice.
Se utilizeaza tehnici de teledetectie prin satelit sau aeriene.
Statele membre actualizeaza LPIS cel putin o data pe an.

TITLUL III — CONTROALE SI PENALIZARI

Articolul 84 — Principii generale de control
Statele membre efectueaza controale administrative pentru toate cererile de ajutor.
Controalele la fata locului se efectueaza pentru cel putin 5% din solicitanti.
Se utilizeaza tehnici de teledetectie (drone, satelit) pentru verificarea suprafetelor.

Articolul 85 — Reduceri si excluderi
Daca suprafata declarata depaseste suprafata determinata cu mai mult de 3%,
ajutorul se reduce cu procentul de supradeclarare.
Daca diferenta depaseste 20%, ajutorul se reduce suplimentar.
Daca diferenta depaseste 50%, fermierii sunt exclusi de la plata.

Articolul 86 — Sanctiuni administrative
In caz de neconformitate intentionata, fermierii sunt exclusi de la schema de ajutor
pentru anul respectiv si pentru urmatorii doi ani.

TITLUL IV — ECO-SCHEME

Articolul 31 — Eco-scheme voluntare
Statele membre pot oferi plati pentru eco-scheme voluntare.
Eco-schemele pot include: rotatia culturilor, acoperirea solului iarna,
reducerea pesticidelor, gestionarea apei, biodiversitatea.
Romania a implementat 5 eco-scheme in PAC 2023-2027.

TITLUL V — PLATI DIRECTE

Articolul 17 — Plata de baza
Plata de baza se acorda pentru fiecare hectar eligibil declarat de fermier.
Suprafata minima pentru plata: 1 hectar per fermier (Romania).
Valoarea medie plata de baza Romania: 185 EUR/hectar (2025).

Articolul 18 — Plata redistributiva
Romania acorda plata redistributiva pentru primele 30 de hectare.
Valoarea: 50 EUR/hectar suplimentar fata de plata de baza.

TITLUL VI — GDPR SI DATE PERSONALE

Articolul 98 — Protectia datelor cu caracter personal
Datele colectate prin IACS, inclusiv coordonatele GPS si fotografiile aeriene,
sunt date cu caracter personal conform RGPD.
Statele membre asigura securitatea si confidentialitatea acestor date.
Perioada de retentie: 7 ani dupa inchiderea dosarului.
"""

INTREBARI_DEMO = [
    "Care este pragul de penalizare pentru diferenta de suprafata?",
    "Ce este LPIS si ce contine?",
    "Ce procent din solicitanti sunt supusi controalelor la fata locului?",
    "Care este valoarea platii de baza in Romania?",
    "Ce sunt eco-schemele si sunt obligatorii?",
    "Care sunt consecintele neconformitatii intentionate?",
    "Cum se protejeaza datele GPS conform RGPD?",
]

STOPWORDS = {
    "si", "sau", "in", "la", "de", "cu", "pe", "din", "pentru", "care",
    "este", "sunt", "a", "al", "ale", "un", "o", "nu", "sa", "se", "ca",
    "mai", "prin", "fie", "daca", "dar", "iar", "fost", "fi", "au",
    "acest", "aceasta", "aceste", "acestor", "astfel", "urma",
    "privind", "conform", "poate", "trebuie", "pot", "cele",
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCTII RAG
# ══════════════════════════════════════════════════════════════════════════════

def extrage_text_pdf(fisier) -> str:
    if not PYPDF_OK:
        return ""
    try:
        reader = PdfReader(fisier)
        return "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
    except Exception as e:
        return f"[EROARE PDF] {e}"


def chunking(text: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    """Imparte textul in fragmente de ~chunk_size cuvinte cu suprapunere."""
    cuvinte = text.split()
    chunks, i = [], 0
    while i < len(cuvinte):
        chunk = " ".join(cuvinte[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def tokenizeaza(text: str) -> list[str]:
    tokens = re.findall(r'\b[a-zA-ZăâîșțĂÂÎȘȚ]{3,}\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def tfidf_retrieval(intrebare: str, chunks: list[str], top_k: int = 3) -> list[tuple]:
    """Returneaza top_k chunks cele mai relevante pentru intrebare."""
    q_tokens = set(tokenizeaza(intrebare))
    if not q_tokens:
        return [(0.0, c) for c in chunks[:top_k]]

    n = len(chunks)
    chunk_tokens = [tokenizeaza(c) for c in chunks]

    # IDF
    idf = {}
    for tok in q_tokens:
        df = sum(1 for ct in chunk_tokens if tok in ct)
        idf[tok] = math.log((n + 1) / (df + 1)) + 1

    # Scor per chunk
    scoruri = []
    for idx, (chunk, ct) in enumerate(zip(chunks, chunk_tokens)):
        freq = Counter(ct)
        total = max(len(ct), 1)
        scor = sum((freq.get(tok, 0) / total) * idf.get(tok, 0) for tok in q_tokens)
        scoruri.append((scor, chunk))

    scoruri.sort(reverse=True)
    return scoruri[:top_k]


def verifica_ollama():
    if not REQUESTS_OK:
        return False, []
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if r.status_code == 200:
            return True, [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return False, []


def raspunde_cu_context(model: str, intrebare: str, context: str) -> tuple:
    prompt = (
        f"Folosind EXCLUSIV informatiile din contextul de mai jos, "
        f"raspunde la intrebarea:\n\n"
        f"INTREBARE: {intrebare}\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"Raspunde concis, in romana. Daca raspunsul nu se gaseste in context, "
        f"spune clar: 'Informatia nu se gaseste in documentul furnizat.'"
    )
    system = (
        "Esti un asistent juridic specializat in legislatia PAC si APIA Romania. "
        "Raspunzi NUMAI pe baza documentului furnizat, fara a adauga informatii externe. "
        "Raspunsuri scurte, precise, cu referire la articolul relevant daca e posibil."
    )
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "system": system, "stream": False},
            timeout=120,
        )
        if r.status_code == 200:
            return True, r.json().get("response", "")
        return False, f"Eroare HTTP {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama nu ruleaza — porneste cu: ollama serve"
    except Exception as e:
        return False, str(e)


def raspuns_demo(intrebare: str, context: str) -> str:
    """Raspuns simplu bazat pe cautare de cuvinte cheie in context (fara LLM)."""
    q_tok = set(tokenizeaza(intrebare))
    propozitii = [p.strip() for p in re.split(r'[.\n]', context) if len(p.strip()) > 30]
    scoruri = []
    for prop in propozitii:
        p_tok = set(tokenizeaza(prop))
        scor = len(q_tok & p_tok)
        if scor > 0:
            scoruri.append((scor, prop))
    scoruri.sort(reverse=True)
    if scoruri:
        top = [p for _, p in scoruri[:3]]
        return (
            "Pe baza documentului:\n\n" +
            "\n".join(f"• {p}." for p in top) +
            "\n\n*[MOD DEMO — porneste Ollama pentru raspuns natural complet]*"
        )
    return "Informatia nu a fost gasita in documentul furnizat. [MOD DEMO]"

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ziua 23 — RAG PDF",
    page_icon="RAG",
    layout="wide",
    initial_sidebar_state="expanded"
)

ollama_ok, modele_disponibile = verifica_ollama()

# Initializare stare
if "rag_chunks"   not in st.session_state: st.session_state.rag_chunks   = []
if "rag_text"     not in st.session_state: st.session_state.rag_text     = ""
if "rag_sursa"    not in st.session_state: st.session_state.rag_sursa    = ""
if "rag_istoric"  not in st.session_state: st.session_state.rag_istoric  = []

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:26px; font-weight:900; color:#c0392b;'>RAG</div>
    <div style='font-size:16px; font-weight:700; color:#c0392b;'>ZIUA 23</div>
    <div style='font-size:11px; color:#666;'>Intreaba un Document PDF</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 4 — AI Generativ Local")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 23 / 30 zile")
st.sidebar.progress(23 / 30)
st.sidebar.markdown(f"**Data:** {datetime.date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()

if ollama_ok:
    st.sidebar.success(f"Ollama activ | {len(modele_disponibile)} modele")
    model_selectat = st.sidebar.selectbox("Model:", modele_disponibile or ["llama3.2:latest"])
else:
    st.sidebar.error("Ollama offline — mod demo")
    model_selectat = "llama3.2:latest"

if st.session_state.rag_chunks:
    st.sidebar.success(
        f"Document incarcat: **{st.session_state.rag_sursa}**\n"
        f"{len(st.session_state.rag_chunks)} fragmente indexate"
    )
    if st.sidebar.button("Schimba documentul", use_container_width=True):
        st.session_state.rag_chunks  = []
        st.session_state.rag_text    = ""
        st.session_state.rag_sursa   = ""
        st.session_state.rag_istoric = []
        st.rerun()

st.sidebar.divider()
st.sidebar.markdown("""
**Documente recomandate:**
- Regulamente UE PAC (PDF oficial)
- Proceduri APIA
- Ghiduri solicitant fonduri
- Suporturi de curs
- Teze doctorat
""")
st.sidebar.divider()
st.sidebar.markdown("""
<div style='background:#c0392b; border-radius:8px; padding:10px 12px;
     color:white; font-size:10px; line-height:1.7;'>
<b>Autor:</b> Prof. Asoc. Dr. Oliviu Mihnea Gamulescu<br>
<b>UCB</b> Targu Jiu | <b>APIA</b> CJ Gorj
</div>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:36px; font-weight:900; color:#c0392b;'>RAG</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#c0392b; font-weight:800;'>
            Ziua 23 — RAG: Intreaba un Document PDF
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Retrieval-Augmented Generation · Incarca orice PDF · Intreaba in limba naturala
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

if not ollama_ok:
    st.warning("Ollama offline — raspunsuri prin cautare de cuvinte cheie (fara AI generativ). Porneste `ollama serve` pentru AI complet.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# TABURI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Incarca document",
    "Intreaba documentul",
    "Cum functioneaza RAG",
    "Ce am invatat",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INCARCARE DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Incarca documentul pe care vrei sa il interoghezi")

    sursa = st.radio(
        "Sursa document:",
        ["Document demo (Reg. UE 2021/2116 PAC — extras)",
         "Incarca PDF propriu"],
        key="sursa_doc",
        horizontal=True,
    )

    col_inc, col_prev = st.columns([1, 1])

    with col_inc:
        if sursa.startswith("Document demo"):
            if st.button("Incarca documentul demo PAC", type="primary",
                         use_container_width=True, key="btn_demo_rag"):
                with st.spinner("Procesez documentul..."):
                    text = TEXT_DEMO_PAC
                    chunks = chunking(text, chunk_size=300, overlap=60)
                    st.session_state.rag_text   = text
                    st.session_state.rag_chunks = chunks
                    st.session_state.rag_sursa  = "Reg. UE 2021/2116 PAC (extras demo)"
                st.success(f"Document incarcat: {len(chunks)} fragmente indexate.")
                st.rerun()
        else:
            if not PYPDF_OK:
                st.error(
                    "pypdf nu este instalat. Adauga in requirements.txt:\n"
                    "```\npypdf>=4.0.0\n```\nSau: `pip install pypdf`"
                )
            else:
                pdf_file = st.file_uploader(
                    "Incarca fisier PDF (max 50 MB):",
                    type=["pdf"],
                    key="pdf_upload"
                )
                if pdf_file:
                    chunk_size = st.slider("Dimensiune fragment (cuvinte):", 100, 600, 300, 50)
                    if st.button("Proceseaza PDF", type="primary",
                                 use_container_width=True, key="btn_pdf_proc"):
                        with st.spinner("Extrag textul si indexez..."):
                            text = extrage_text_pdf(pdf_file)
                            if text.startswith("[EROARE"):
                                st.error(text)
                            else:
                                chunks = chunking(text, chunk_size=chunk_size, overlap=60)
                                st.session_state.rag_text   = text
                                st.session_state.rag_chunks = chunks
                                st.session_state.rag_sursa  = pdf_file.name
                                st.success(
                                    f"PDF procesat: {len(text.split())} cuvinte → "
                                    f"{len(chunks)} fragmente indexate."
                                )
                                st.rerun()

        if st.session_state.rag_chunks:
            st.markdown("---")
            st.success(f"**{st.session_state.rag_sursa}** — gata de interogare")
            c1, c2, c3 = st.columns(3)
            c1.metric("Cuvinte total", len(st.session_state.rag_text.split()))
            c2.metric("Fragmente indexate", len(st.session_state.rag_chunks))
            c3.metric("Marime medie fragment", f"{int(sum(len(c.split()) for c in st.session_state.rag_chunks)/max(len(st.session_state.rag_chunks),1))} cuv.")

    with col_prev:
        if st.session_state.rag_text:
            st.markdown("**Previzualizare document (primele 1000 caractere):**")
            st.markdown(
                f"<div style='background:#f8f9fa; border-radius:8px; padding:12px; "
                f"font-size:11px; line-height:1.7; height:320px; overflow-y:auto; "
                f"border:1px solid #ddd; white-space:pre-wrap;'>"
                f"{st.session_state.rag_text[:1200]}...</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
<div style='background:#fef9e7; border-radius:8px; padding:20px; text-align:center;
     color:#888; font-size:13px; margin-top:20px; border:2px dashed #f39c12;'>
Niciun document incarcat.<br>
Selecteaza sursa si apasa <b>Incarca</b>.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — INTEROGARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.rag_chunks:
        st.info("Incarca un document in tab-ul 'Incarca document' pentru a incepe interogarea.")
    else:
        st.subheader(f"Intreaba documentul: {st.session_state.rag_sursa}")

        col_q, col_opt = st.columns([3, 1])

        with col_opt:
            top_k = st.slider("Fragmente folosite ca context:", 1, 5, 3, key="topk_rag")
            arata_context = st.checkbox("Arata contextul gasit", value=False, key="show_ctx")
            st.markdown("**Intrebari rapide:**")
            for intrebare_r in INTREBARI_DEMO:
                if st.button(
                    intrebare_r[:42] + "…" if len(intrebare_r) > 42 else intrebare_r,
                    use_container_width=True,
                    key=f"qr_{intrebare_r[:12]}"
                ):
                    st.session_state["intrebare_rapida"] = intrebare_r

        with col_q:
            # Afiseaza istoricul
            for item in st.session_state.rag_istoric:
                with st.chat_message("user"):
                    st.markdown(item["intrebare"])
                with st.chat_message("assistant"):
                    st.markdown(item["raspuns"])
                    if item.get("context") and arata_context:
                        with st.expander("Context folosit"):
                            for i, (scor, chunk) in enumerate(item["context"], 1):
                                st.markdown(
                                    f"<div style='font-size:10px; background:#f5f5f5; "
                                    f"padding:8px; border-radius:4px; margin:4px 0; "
                                    f"border-left:3px solid #c0392b;'>"
                                    f"<b>Fragment {i} (relevanta: {scor:.4f})</b><br>"
                                    f"{chunk[:300]}...</div>",
                                    unsafe_allow_html=True
                                )

            # Input
            val_rapida = st.session_state.pop("intrebare_rapida", "")
            intrebare_user = st.chat_input(
                "Introdu intrebarea despre document...",
                key="chat_rag_input"
            )
            if val_rapida and not intrebare_user:
                intrebare_user = val_rapida

            if intrebare_user:
                with st.chat_message("user"):
                    st.markdown(intrebare_user)

                with st.chat_message("assistant"):
                    with st.spinner("Caut in document si generez raspuns..."):
                        # Retrieval
                        top_chunks = tfidf_retrieval(
                            intrebare_user,
                            st.session_state.rag_chunks,
                            top_k=top_k
                        )
                        context_text = "\n\n---\n\n".join(chunk for _, chunk in top_chunks)

                        # Generation
                        if ollama_ok:
                            ok, raspuns = raspunde_cu_context(
                                model_selectat, intrebare_user, context_text
                            )
                            if not ok:
                                raspuns = f"Eroare: {raspuns}"
                        else:
                            raspuns = raspuns_demo(intrebare_user, context_text)

                    st.markdown(raspuns)

                    if arata_context:
                        with st.expander("Context folosit pentru acest raspuns"):
                            for i, (scor, chunk) in enumerate(top_chunks, 1):
                                st.markdown(
                                    f"<div style='font-size:10px; background:#f5f5f5; "
                                    f"padding:8px; border-radius:4px; margin:4px 0; "
                                    f"border-left:3px solid #c0392b;'>"
                                    f"<b>Fragment {i} (relevanta: {scor:.4f})</b><br>"
                                    f"{chunk[:300]}...</div>",
                                    unsafe_allow_html=True
                                )

                st.session_state.rag_istoric.append({
                    "intrebare": intrebare_user,
                    "raspuns":   raspuns,
                    "context":   top_chunks,
                })
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUM FUNCTIONEAZA RAG
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Cum functioneaza RAG (Retrieval-Augmented Generation)?")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**RAG = Retrieval + Generation**

Problema pe care o rezolva: LLM-urile nu stiu ce e in documentele tale specifice.
RAG ii "arata" documentul relevant inainte sa raspunda.

**Pasii algoritmului RAG simplu (implementat azi):**

```
1. INGESTIE (o singura data per document)
   PDF → text brut → chunking (fragmente ~300 cuvinte)
   Fiecare fragment = o "bucata" din document

2. RETRIEVAL (la fiecare intrebare)
   Intrebare utilizator
       ↓
   TF-IDF: calculeaza relevanta fiecarui fragment
       ↓
   Selecteaza top-3 fragmente cele mai relevante

3. AUGMENTATION
   Prompt = "Raspunde la [intrebare] folosind [context]"
   Context = top-3 fragmente concatenate

4. GENERATION
   LLM (Ollama) primeste prompt + context
       ↓
   Raspunde NUMAI pe baza contextului furnizat
```

**De ce nu dai direct tot documentul la LLM?**
- Un PDF de 100 pagini = ~50.000 tokens
- Llama 3.2 accepta max 128K tokens (unele modele mai putin)
- RAG selecteaza doar ce e relevant → mai rapid + mai precis
""")

        st.markdown("---")
        st.markdown("**Cod complet RAG simplu:**")
        st.code("""
import requests
from pypdf import PdfReader
import math
from collections import Counter
import re

def chunking(text, size=300, overlap=60):
    cuvinte = text.split()
    chunks, i = [], 0
    while i < len(cuvinte):
        chunks.append(" ".join(cuvinte[i:i+size]))
        i += size - overlap
    return chunks

def retrieval_tfidf(intrebare, chunks, top_k=3):
    q_tok = set(intrebare.lower().split())
    scoruri = []
    for chunk in chunks:
        c_tok = chunk.lower().split()
        freq = Counter(c_tok)
        scor = sum(freq.get(t,0) for t in q_tok) / max(len(c_tok),1)
        scoruri.append((scor, chunk))
    return sorted(scoruri, reverse=True)[:top_k]

# Ingestie
reader = PdfReader("regulament_pac.pdf")
text = "\\n".join(p.extract_text() for p in reader.pages)
chunks = chunking(text)

# Retrieval + Generation
intrebare = "Care este pragul de penalizare?"
context = "\\n---\\n".join(c for _,c in retrieval_tfidf(intrebare, chunks))

prompt = f"Context:\\n{context}\\n\\nIntrebare: {intrebare}"
r = requests.post("http://localhost:11434/api/generate",
    json={"model":"llama3.2","prompt":prompt,"stream":False})
print(r.json()["response"])
""", language="python")

    with col2:
        st.markdown("""
<div style='background:#fdf2f8; border-radius:10px; padding:14px;
     border-top:4px solid #c0392b;'>
<div style='font-weight:700; color:#c0392b;'>RAG vs. Fine-tuning</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.8;'>

<b>RAG (ce folosim azi):</b><br>
✓ Documente noi fara reantrenare<br>
✓ Raspunsuri cu sursa verificabila<br>
✓ Functioneaza pe orice LLM<br>
✓ Gratuit, offline<br>
✗ Calitate depinde de chunking<br><br>

<b>Fine-tuning:</b><br>
✓ LLM "stie" domeniul in profunzime<br>
✗ Necesita date de antrenare<br>
✗ Cost ridicat (GPU + timp)<br>
✗ Nu se actualizeaza usor<br><br>

<b>Concluzie: pentru documente APIA<br>
→ RAG este alegerea corecta.</b>
</div></div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style='background:#e8f4fd; border-radius:10px; padding:14px; margin-top:12px;
     border-top:4px solid #1a5276;'>
<div style='font-weight:700; color:#1a5276;'>Aplicatii APIA concrete</div>
<div style='font-size:11px; color:#333; margin-top:8px; line-height:1.8;'>

<b>1. Asistent reglementari</b><br>
Incarca Reg. UE 2021/2116 +<br>
Ordinele MADR + Ghiduri APIA<br>
→ Raspunde la intrebari instantaneu<br><br>

<b>2. Verificare dosar</b><br>
Incarca cererea fermierului<br>
→ "Ce suprafete declara?"<br>
→ "Exista parcele neeligibile?"<br><br>

<b>3. Asistent student UCB</b><br>
Incarca suportul de curs<br>
→ Studentii intreaba direct<br>
→ Raspuns din cursul tau<br>
</div></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Ziua 23 — Ce am invatat")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
#### RAG — Concepte cheie

**Retrieval-Augmented Generation:**
- Retrieval = cauta fragmentele relevante
- Augmentation = adauga context la prompt
- Generation = LLM raspunde cu context

**Chunking:**
```python
# Fragment de 300 cuvinte cu 60 cuvinte suprapunere
chunking(text, chunk_size=300, overlap=60)
# Suprapunerea evita pierderea informatiei
# la granita dintre fragmente
```

**TF-IDF pentru retrieval:**
- TF = frecventa cuvant in fragment
- IDF = raritatea cuvantului in tot documentul
- Score = TF × IDF → fragmentele cu cuvinte
  rare dar frecvente local primesc scor mare

**Prompt cu context:**
```python
prompt = f\"\"\"
Folosind EXCLUSIV contextul de mai jos,
raspunde la: {intrebare}

CONTEXT:
{context}
\"\"\"
```

**Hallucination prevention:**
- Instructiunea "EXCLUSIV din context"
- Modelul spune "nu se gaseste" daca lipseste
- Poti verifica sursa (fragmentul afisat)
""")

    with col2:
        st.markdown("""
#### Pipeline RAG complet M1-M4

```
Document PAC (PDF)
    ↓ Z23 RAG: extragere text
    ↓ chunking 300 cuv/fragment
    ↓ TF-IDF retrieval
    ↓ LLM generare raspuns
    → "Art. 85: diferenta > 3% = penalizare"

Imagine aeriana drone
    ↓ Z14 CV: suprafata masurata = 4.31 ha
    ↓ Z10 NDVI: anomalii detectate
    ↓ Z18 NLP: suprafata declarata = 4.52 ha
    ↓ Z22 LLM: genereaza raport
    ↓ Z23 RAG: verifica baza legala
    → Raport complet + articol legal citat
```
""")
        st.markdown("""
<div style='background:#fdedec; border-radius:8px; padding:14px; margin-top:10px;
     border-top:3px solid #c0392b;'>
<div style='font-weight:700; color:#922b21;'>Concluzie Ziua 23</div>
<div style='font-size:11px; color:#333; margin-top:6px; line-height:1.7;'>
RAG transforma orice PDF in baza de cunostinte interogabila.
Fara antrenare, fara cost, offline complet.<br><br>
Inspector APIA poate intreba direct regulamentul PAC
fara sa caute manual in 200 de pagini.<br><br>
Urmatoarea: <b>Ziua 24 — Sinteza Modul 4</b> (finalizarea M4).
</div></div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
<div style='background:linear-gradient(135deg,#c0392b 0%,#8e44ad 100%);
     border-radius:10px; padding:16px 24px; color:white;'>
<div style='font-size:15px; font-weight:800;'>Ziua 23 — FINALIZATA</div>
<div style='font-size:12px; margin-top:6px; opacity:0.9;'>
RAG · Chunking · TF-IDF Retrieval · LLM Generation · PDF incarcare · Chat cu document
</div>
<div style='font-size:11px; margin-top:8px; opacity:0.7;'>
Urmatoarea: Ziua 24 — Sinteza Modul 4 AI Generativ
</div>
</div>
""", unsafe_allow_html=True)
