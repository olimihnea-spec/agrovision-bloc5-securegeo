"""
ZIUA 1 — Clasificare culturi din date NDVI
Modul 1: Machine Learning cu scikit-learn
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import date

try:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        accuracy_score, classification_report,
        confusion_matrix, ConfusionMatrixDisplay
    )
    from sklearn.preprocessing import StandardScaler
    SK_OK = True
except ImportError:
    SK_OK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 1 — Clasificare NDVI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🌿</div>
    <div style='font-size:16px; font-weight:700; color:#27ae60;'>ZIUA 1</div>
    <div style='font-size:11px; color:#666;'>Clasificare Culturi NDVI</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 1 — Machine Learning")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 1 / 30 zile")
st.sidebar.progress(1/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 1:**
- Ce este Machine Learning?
- Clasificare supervizata
- KNN — K Nearest Neighbors
- SVM — Support Vector Machine
- Train/Test split
- Acuratete si confusion matrix
""")

if not SK_OK:
    st.error("scikit-learn nu este instalat. Ruleaza: `pip install scikit-learn`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🌿</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#27ae60; font-weight:800;'>
            Ziua 1 — Clasificare Culturi din Date NDVI
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 1 — Machine Learning &nbsp;|&nbsp;
            KNN si SVM pe date reale din parcele agricole
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "📊 Date & Explorare", "🤖 Antrenare Model", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# GENERARE DATE SIMULATE (realiste pentru Gorj)
# ══════════════════════════════════════════════════════════════════════════════
np.random.seed(42)
N = 300

# Fiecare cultura are un profil NDVI diferit pe parcursul sezonului
# Coloane: NDVI_mai, NDVI_iunie, NDVI_iulie, NDVI_august, suprafata_ha
date_culturi = {
    "Grau":        {"mai": (0.65, 0.08), "iun": (0.55, 0.10), "iul": (0.25, 0.08), "aug": (0.15, 0.05), "ha": (1.5, 5.0)},
    "Floarea-soarelui": {"mai": (0.30, 0.07), "iun": (0.55, 0.09), "iul": (0.75, 0.08), "aug": (0.50, 0.10), "ha": (2.0, 8.0)},
    "Porumb":      {"mai": (0.25, 0.06), "iun": (0.60, 0.09), "iul": (0.82, 0.07), "aug": (0.70, 0.09), "ha": (1.0, 6.0)},
    "Lucerna":     {"mai": (0.60, 0.08), "iun": (0.55, 0.09), "iul": (0.65, 0.08), "aug": (0.58, 0.09), "ha": (1.0, 4.0)},
    "Fanete":      {"mai": (0.48, 0.08), "iun": (0.52, 0.08), "iul": (0.48, 0.07), "aug": (0.42, 0.08), "ha": (0.5, 3.0)},
}

rows = []
etichete = []
n_per_cls = N // len(date_culturi)

for cultura, params in date_culturi.items():
    for _ in range(n_per_cls):
        rows.append({
            "NDVI_mai":    np.clip(np.random.normal(params["mai"][0], params["mai"][1]), 0, 1),
            "NDVI_iunie":  np.clip(np.random.normal(params["iun"][0], params["iun"][1]), 0, 1),
            "NDVI_iulie":  np.clip(np.random.normal(params["iul"][0], params["iul"][1]), 0, 1),
            "NDVI_august": np.clip(np.random.normal(params["aug"][0], params["aug"][1]), 0, 1),
            "suprafata_ha": round(np.random.uniform(params["ha"][0], params["ha"][1]), 2),
        })
        etichete.append(cultura)

df = pd.DataFrame(rows)
df["cultura"] = etichete

FEATURES = ["NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august"]
CULORI_CULTURA = {
    "Grau":              "#f39c12",
    "Floarea-soarelui":  "#e74c3c",
    "Porumb":            "#27ae60",
    "Lucerna":           "#16a085",
    "Fanete":            "#795548",
}

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Ce este Machine Learning?")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        **Machine Learning (ML)** este o ramura a inteligentei artificiale in care
        calculatorul **invata din exemple** — fara sa fie programat explicit cu reguli.

        In loc sa scriem: *"daca NDVI_iulie > 0.8 atunci porumb"*,
        ii dam calculatorului **300 de exemple** de parcele cu valorile NDVI cunoscute
        si el **descopera singur** tiparele care diferentiaza culturile.
        """)

        st.markdown("#### Tipuri de ML")
        tipuri = [
            ("Supervizat", "Inveti din exemple etichetate (stii raspunsul corect)", "#27ae60",
             "Clasificare culturi, predictie productie"),
            ("Nesupervizat", "Gasesti structuri in date fara etichete", "#2980b9",
             "Grupare parcele similare (clustering)"),
            ("Prin recompensa", "Agentul invata prin incercare-eroare", "#8e44ad",
             "Jocuri, robotica, optimizare rute"),
        ]
        for tip, desc, culoare, ex in tipuri:
            st.markdown(f"""
            <div style='border-left:4px solid {culoare}; padding:8px 14px;
                 background:#fafafa; border-radius:0 8px 8px 0; margin:6px 0;'>
                <div style='font-weight:700; color:{culoare};'>{tip}</div>
                <div style='font-size:12px; color:#333;'>{desc}</div>
                <div style='font-size:11px; color:#888; margin-top:2px;'>Exemplu: {ex}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Azi folosim: Clasificare Supervizata")
        st.markdown("""
        **Problema:** Avem 300 de parcele agricole din Gorj.
        Pentru fiecare parcel stim valorile NDVI in mai, iunie, iulie si august.
        Stim si ce cultura are fiecare parcela (grau, floarea-soarelui, porumb, legume).

        **Intrebarea:** Daca vine o parcel noua cu valorile NDVI:
        `mai=0.30, iunie=0.58, iulie=0.80, august=0.68` — **ce cultura are?**

        Algoritmul ML invata din cele 300 de exemple si clasifica parcel necunoscuta.
        """)

    with col2:
        st.markdown("#### Algoritmii de azi")

        st.markdown("""
        <div style='background:#fff3e0; border-radius:10px; padding:14px;
             border-top:4px solid #f39c12; margin-bottom:12px;'>
            <div style='font-weight:700; color:#f39c12; font-size:15px;'>
                KNN — K Nearest Neighbors
            </div>
            <div style='font-size:12px; color:#555; margin-top:6px;'>
                <b>Idee:</b> o parcela noua apartine aceleiasi culturi
                ca cele mai apropiate K parcele cunoscute.<br><br>
                <b>Analogie:</b> esti ceea ce sunt vecinii tai.
                Daca 4 din 5 vecini cei mai apropiati sunt porumb,
                probabil esti si tu porumb.<br><br>
                <b>Parametru cheie:</b> K = numarul de vecini (implicit 5)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#f0f0ff; border-radius:10px; padding:14px;
             border-top:4px solid #8e44ad;'>
            <div style='font-weight:700; color:#8e44ad; font-size:15px;'>
                SVM — Support Vector Machine
            </div>
            <div style='font-size:12px; color:#555; margin-top:6px;'>
                <b>Idee:</b> gaseste linia (sau suprafata) care
                separa cel mai bine clasele, cu marginea maxima.<br><br>
                <b>Analogie:</b> tragi o granita intre grau si porumb
                astfel incat sa fie cat mai departe de ambele grupuri.<br><br>
                <b>Avantaj:</b> functioneaza bine si cu putine date
                si in spatii cu multe dimensiuni
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Fluxul ML")
        pasi_ml = [
            ("1", "Date",        "300 parcele cu NDVI + eticheta cultura"),
            ("2", "Split",       "80% antrenare / 20% testare"),
            ("3", "Antrenare",   "Modelul invata din datele de train"),
            ("4", "Evaluare",    "Testam pe date nevazute"),
            ("5", "Predictie",   "Parcel noua → cultura prezisa"),
        ]
        for nr, etapa, desc in pasi_ml:
            st.markdown(f"""
            <div style='display:flex; gap:8px; align-items:center; margin:4px 0;'>
                <div style='background:#27ae60; color:white; border-radius:50%;
                     width:22px; height:22px; display:flex; align-items:center;
                     justify-content:center; font-size:11px; font-weight:700;
                     flex-shrink:0;'>{nr}</div>
                <div style='font-size:12px;'>
                    <b>{etapa}:</b> {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATE & EXPLORARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Datasetul — 300 parcele agricole Gorj")

    col1, col2, col3, col4, col5 = st.columns(5)
    for col, (cultura, culoare) in zip(
        [col1, col2, col3, col4, col5], CULORI_CULTURA.items()
    ):
        n_cls = len(df[df["cultura"] == cultura])
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:12px;
                 text-align:center; border-top:3px solid {culoare};
                 box-shadow:0 1px 4px rgba(0,0,0,0.08);'>
                <div style='font-size:22px; font-weight:800; color:{culoare};'>{n_cls}</div>
                <div style='font-size:12px; color:#555;'>{cultura}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    col_tabel, col_stat = st.columns([3, 2])
    with col_tabel:
        st.markdown("**Primele 10 randuri:**")
        st.dataframe(
            df[["NDVI_mai","NDVI_iunie","NDVI_iulie","NDVI_august","suprafata_ha","cultura"]]
            .head(10).round(3),
            use_container_width=True, hide_index=True
        )
    with col_stat:
        st.markdown("**Statistici descriptive (NDVI):**")
        st.dataframe(
            df[FEATURES].describe().round(3),
            use_container_width=True
        )

    st.divider()
    st.markdown("#### Profil NDVI per cultura — de ce sunt clasificabile?")

    if PLOTLY_OK:
        # Grafic linii NDVI mediu per cultura
        luni = ["Mai", "Iunie", "Iulie", "August"]
        fig = go.Figure()
        for cultura, culoare in CULORI_CULTURA.items():
            subset = df[df["cultura"] == cultura]
            medii = [
                subset["NDVI_mai"].mean(),
                subset["NDVI_iunie"].mean(),
                subset["NDVI_iulie"].mean(),
                subset["NDVI_august"].mean(),
            ]
            fig.add_trace(go.Scatter(
                x=luni, y=medii, name=cultura,
                mode="lines+markers",
                line=dict(color=culoare, width=3),
                marker=dict(size=10)
            ))
        fig.update_layout(
            title="Profil NDVI mediu per cultura (mai-august)",
            xaxis_title="Luna",
            yaxis_title="NDVI mediu",
            yaxis=dict(range=[0, 1]),
            height=350,
            margin=dict(t=40, b=30, l=30, r=30),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Graul atinge peak NDVI in mai-iunie (cereala de toamna) si scade rapid la maturare. "
            "Porumbul si floarea-soarelui ating maximul in iulie. "
            "Aceasta diferenta temporala permite clasificarea automata."
        )
    else:
        st.info("Instaleaza plotly: `pip install plotly`")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANTRENARE MODEL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Antrenare si evaluare modele ML")

    col_params, col_rez = st.columns([1, 2])

    with col_params:
        st.markdown("#### Parametri antrenare")

        test_size = st.slider(
            "Proportie date de test (%)",
            min_value=10, max_value=40, value=20, step=5
        ) / 100

        model_ales = st.selectbox(
            "Algoritmul ML",
            ["KNN — K Nearest Neighbors", "SVM — Support Vector Machine", "Ambii (comparatie)"]
        )

        if "KNN" in model_ales:
            k_vecini = st.slider("K — numarul de vecini (KNN)", 1, 15, 5)
        else:
            k_vecini = 5

        normalizeaza = st.checkbox(
            "Normalizeaza datele (StandardScaler)",
            value=True,
            help="Recomandat pentru SVM si KNN — aduce toate valorile la aceeasi scara"
        )

        antreneaza = st.button("Antreneaza modelul", type="primary")

    with col_rez:
        if antreneaza:
            X = df[FEATURES].values
            y = df["cultura"].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )

            if normalizeaza:
                scaler  = StandardScaler()
                X_train = scaler.fit_transform(X_train)
                X_test  = scaler.transform(X_test)

            rezultate = {}

            if "Ambii" in model_ales:
                modele = {
                    "KNN": KNeighborsClassifier(n_neighbors=k_vecini),
                    "SVM": SVC(kernel="rbf", C=1.0, random_state=42)
                }
            elif "KNN" in model_ales:
                modele = {"KNN": KNeighborsClassifier(n_neighbors=k_vecini)}
            else:
                modele = {"SVM": SVC(kernel="rbf", C=1.0, random_state=42)}

            for nume_model, model in modele.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc    = accuracy_score(y_test, y_pred)
                rezultate[nume_model] = {
                    "model":  model,
                    "y_pred": y_pred,
                    "y_test": y_test,
                    "acc":    acc,
                    "report": classification_report(y_test, y_pred, output_dict=True)
                }

            # ── Afisare rezultate ────────────────────────────────────────────
            st.markdown("#### Rezultate")

            for nume_model, rez in rezultate.items():
                culoare_model = "#f39c12" if "KNN" in nume_model else "#8e44ad"
                st.markdown(f"""
                <div style='background:{culoare_model}22; border-left:4px solid {culoare_model};
                     border-radius:0 8px 8px 0; padding:10px 14px; margin:8px 0;'>
                    <span style='font-weight:700; color:{culoare_model}; font-size:15px;'>
                        {nume_model}
                    </span>
                    <span style='font-size:20px; font-weight:800; color:{culoare_model};
                    margin-left:16px;'>
                        {rez["acc"]*100:.1f}% acuratete
                    </span>
                    <span style='font-size:12px; color:#666; margin-left:8px;'>
                        ({int(test_size*300)} parcele de test)
                    </span>
                </div>
                """, unsafe_allow_html=True)

            # ── Classification report ────────────────────────────────────────
            if rezultate:
                primul = list(rezultate.values())[0]
                report = primul["report"]
                clase  = [c for c in report if c not in ("accuracy","macro avg","weighted avg")]
                rows_r = []
                for cls in clase:
                    rows_r.append({
                        "Cultura":    cls,
                        "Precizie":   f"{report[cls]['precision']:.2f}",
                        "Recall":     f"{report[cls]['recall']:.2f}",
                        "F1-score":   f"{report[cls]['f1-score']:.2f}",
                        "Suport":     int(report[cls]['support']),
                    })
                st.dataframe(pd.DataFrame(rows_r), use_container_width=True, hide_index=True)

            # ── Confusion matrix ─────────────────────────────────────────────
            if PLOTLY_OK and rezultate:
                st.markdown("#### Confusion Matrix")
                primul_key = list(rezultate.keys())[0]
                rez0   = rezultate[primul_key]
                clase  = sorted(set(rez0["y_test"]))
                cm     = confusion_matrix(rez0["y_test"], rez0["y_pred"], labels=clase)

                fig_cm = go.Figure(go.Heatmap(
                    z=cm,
                    x=clase, y=clase,
                    colorscale="Greens",
                    text=cm, texttemplate="%{text}",
                    showscale=False
                ))
                fig_cm.update_layout(
                    xaxis_title="Prezis",
                    yaxis_title="Real",
                    height=300,
                    margin=dict(t=20, b=40, l=60, r=20),
                )
                st.plotly_chart(fig_cm, use_container_width=True)
                st.caption(
                    "Diagonala principala = clasificari corecte. "
                    "Valorile din afara diagonalei = erori (ex: porumb clasificat ca floarea-soarelui)."
                )

            # ── Predictie pe parcel noua ─────────────────────────────────────
            st.divider()
            st.markdown("#### Testeaza pe o parcel noua")
            st.caption("Introdu valorile NDVI si afla ce cultura are parcela:")

            c1, c2, c3, c4 = st.columns(4)
            with c1: ndvi_mai  = st.number_input("NDVI Mai",    0.0, 1.0, 0.30, 0.01)
            with c2: ndvi_iun  = st.number_input("NDVI Iunie",  0.0, 1.0, 0.58, 0.01)
            with c3: ndvi_iul  = st.number_input("NDVI Iulie",  0.0, 1.0, 0.80, 0.01)
            with c4: ndvi_aug  = st.number_input("NDVI August", 0.0, 1.0, 0.68, 0.01)

            x_nou = np.array([[ndvi_mai, ndvi_iun, ndvi_iul, ndvi_aug]])
            if normalizeaza:
                x_nou = scaler.transform(x_nou)

            primul_model = list(rezultate.values())[0]
            pred = primul_model["model"].predict(x_nou)[0]
            culoare_pred = CULORI_CULTURA.get(pred, "#333")

            st.markdown(f"""
            <div style='background:{culoare_pred}22; border:2px solid {culoare_pred};
                 border-radius:10px; padding:16px; text-align:center; margin-top:8px;'>
                <div style='font-size:13px; color:#555;'>Parcela prezisa ca:</div>
                <div style='font-size:28px; font-weight:800; color:{culoare_pred};'>{pred}</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("Apasa **Antreneaza modelul** pentru a vedea rezultatele.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 1")

    col1, col2 = st.columns(2)

    concepte = [
        ("Machine Learning",         "Calculatorul invata din exemple, nu din reguli scrise manual"),
        ("Clasificare supervizata",  "Invatam un model din date etichetate pentru a prezice clase noi"),
        ("KNN",                      "Clasifica dupa cele mai apropiate K exemple din datele de antrenare"),
        ("SVM",                      "Gaseste granita optima intre clase cu margine maxima"),
        ("train_test_split()",       "Imparte datele: 80% antrenare, 20% testare — evaluare corecta"),
        ("StandardScaler()",         "Normalizeaza datele: medie 0, deviatie standard 1"),
        ("accuracy_score()",         "Proportia predictiilor corecte din total"),
        ("confusion_matrix()",       "Tabel care arata ce clase au fost confundate cu ce"),
        ("classification_report()",  "Precizie, Recall si F1-score per clasa"),
        ("fit() / predict()",        "fit() = antrenare; predict() = prezicere pe date noi"),
        ("stratify=y",               "Asigura proportii egale de clase in train si test"),
        ("numpy random seed",        "np.random.seed(42) — reproductibilitate rezultate"),
    ]

    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f0f7ff; border-left:3px solid #2980b9;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#2980b9; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")

    st.code("""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. Pregatire date
X = df[["NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august"]].values
y = df["cultura"].values

# 2. Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Normalizare (important pentru KNN si SVM)
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)   # fit DOAR pe train
X_test  = scaler.transform(X_test)        # transform pe test

# 4. KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
print(f"KNN acuratete: {accuracy_score(y_test, knn.predict(X_test)):.2%}")

# 5. SVM
svm = SVC(kernel="rbf", C=1.0, random_state=42)
svm.fit(X_train, y_train)
print(f"SVM acuratete: {accuracy_score(y_test, svm.predict(X_test)):.2%}")

# 6. Predictie parcel noua
x_nou = scaler.transform([[0.30, 0.58, 0.80, 0.68]])
print(f"Cultura prezisa: {knn.predict(x_nou)[0]}")
""", language="python")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Legatura cu munca ta la APIA")
        st.markdown("""
        Datele NDVI pe care le-ai folosit in **AgroVision** (Bloc 3) pot fi
        folosite direct ca input pentru un model ML de clasificare culturi.

        - **APIA** foloseste deja LPIS + teledetectie pentru verificare culturi
        - Un model KNN/SVM antrenat pe date reale Gorj ar putea detecta
          **declaratii incorecte** in cererile PAC
        - Aceasta este o aplicatie directa pentru articolul tau urmator
        """)
    with col_b:
        st.markdown("#### Ziua 2 — ce urmeaza")
        st.markdown("""
        **Regresie** — in loc sa prezici *ce cultura*, prezici *cat produce*.

        Vom construi un model care estimeaza **productia in kg/ha**
        in functie de:
        - valorile NDVI din sezon
        - precipitatii lunare
        - temperatura medie

        Algoritmi: **Linear Regression** si **Random Forest Regressor**
        """)

    st.success(
        "**Ziua 1 finalizata!** Primul model ML functional — KNN si SVM pe date NDVI. "
        "Continua cu **Ziua 2 — Regresie** pentru a prezice productia agricola."
    )
