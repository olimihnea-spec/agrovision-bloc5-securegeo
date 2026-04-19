"""
ZIUA 5 — Pipeline scikit-learn + Export Model
Modul 1: Machine Learning cu scikit-learn
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import pandas as pd
import io
import os
from datetime import date

try:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, classification_report
    import joblib
    SK_OK = True
except ImportError:
    SK_OK = False

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(
    page_title="Ziua 5 — Pipeline & Export",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>⚙️</div>
    <div style='font-size:16px; font-weight:700; color:#1abc9c;'>ZIUA 5</div>
    <div style='font-size:11px; color:#666;'>Pipeline & Export Model</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 1 — Machine Learning")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 5 / 30 zile")
st.sidebar.progress(5/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 5:**
- Pipeline scikit-learn
- GridSearchCV — tuning automat
- Salveaza model cu joblib
- Incarca model salvat
- Predictie fara reanrenare
- Model productie-ready
""")

if not SK_OK:
    st.error("scikit-learn nu este instalat. Ruleaza: `pip install scikit-learn`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>⚙️</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#1abc9c; font-weight:800;'>
            Ziua 5 — Pipeline scikit-learn + Export Model
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 1 — Machine Learning &nbsp;|&nbsp;
            Pipeline, GridSearchCV, joblib — model gata de productie
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "⚙️ Pipeline & GridSearch", "💾 Export & Incarcare", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# DATE
# ══════════════════════════════════════════════════════════════════════════════
np.random.seed(42)
N_PER_CLS = 80

CULORI_CULTURA = {
    "Grau":              "#f39c12",
    "Floarea-soarelui":  "#e74c3c",
    "Porumb":            "#27ae60",
    "Lucerna":           "#16a085",
    "Fanete":            "#795548",
}

CULTURI_CFG = {
    "Grau":             {"mai": (0.65,0.08), "iun": (0.55,0.10), "iul": (0.25,0.08), "aug": (0.15,0.05)},
    "Floarea-soarelui": {"mai": (0.30,0.07), "iun": (0.55,0.09), "iul": (0.75,0.08), "aug": (0.50,0.10)},
    "Porumb":           {"mai": (0.25,0.06), "iun": (0.60,0.09), "iul": (0.82,0.07), "aug": (0.70,0.09)},
    "Lucerna":          {"mai": (0.60,0.08), "iun": (0.55,0.09), "iul": (0.65,0.08), "aug": (0.58,0.09)},
    "Fanete":           {"mai": (0.48,0.08), "iun": (0.52,0.08), "iul": (0.48,0.07), "aug": (0.42,0.08)},
}

rows = []
for cultura, cfg in CULTURI_CFG.items():
    for _ in range(N_PER_CLS):
        rows.append({
            "cultura":     cultura,
            "NDVI_mai":    float(np.clip(np.random.normal(cfg["mai"][0], cfg["mai"][1]), 0, 1)),
            "NDVI_iunie":  float(np.clip(np.random.normal(cfg["iun"][0], cfg["iun"][1]), 0, 1)),
            "NDVI_iulie":  float(np.clip(np.random.normal(cfg["iul"][0], cfg["iul"][1]), 0, 1)),
            "NDVI_august": float(np.clip(np.random.normal(cfg["aug"][0], cfg["aug"][1]), 0, 1)),
        })

df = pd.DataFrame(rows)
FEATURES = ["NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august"]
X_all = df[FEATURES].values
y_all = df["cultura"].values

X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all, test_size=0.2, random_state=42, stratify=y_all
)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "modele_salvate")
os.makedirs(MODEL_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Problema cu codul de pana acum")

    st.warning("""
    In Zilele 1-4 am facut mereu:
    `scaler.fit_transform(X_train)` → `model.fit(X_train_sc)` → `scaler.transform(X_test)` → `model.predict(X_test_sc)`

    **Riscuri:**
    - Uiti sa aplici scalerul pe datele noi
    - Aplici `fit_transform` si pe datele de test (data leakage!)
    - Codul devine greu de reutilizat si de partajat
    """)

    st.markdown("### Solutia: Pipeline")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        Un **Pipeline** impacheteaza toti pasii (preprocesare + model)
        intr-un singur obiect care se comporta exact ca un model normal.

        Un singur `fit()` face totul in ordine:
        1. Scaler: `fit_transform` pe train
        2. Model: `fit` pe datele scalate

        Un singur `predict()` aplica automat:
        1. Scaler: `transform` (nu `fit`!) pe date noi
        2. Model: `predict` pe rezultat
        """)

        st.code("""
# Fara Pipeline — risc de erori
scaler  = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)       # NU fit_transform!
model.fit(X_train_sc, y_train)
y_pred = model.predict(X_test_sc)

# Cu Pipeline — simplu si sigur
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  KNeighborsClassifier(n_neighbors=5))
])
pipe.fit(X_train, y_train)                  # face totul automat
y_pred = pipe.predict(X_test)               # aplica scaler + predict
""", language="python")

    with col2:
        st.markdown("### GridSearchCV — tuning automat")
        st.markdown("""
        Pana acum am ales manual K=5 pentru KNN sau C=1.0 pentru SVM.
        **GridSearchCV** testeaza automat toate combinatiile posibile
        si returneaza cei mai buni hiperparametri.
        """)

        st.code("""
param_grid = {
    "model__n_neighbors": [3, 5, 7, 10],
    "model__weights":     ["uniform", "distance"],
}
# Testeaza 4 x 2 = 8 combinatii cu 5-fold CV
# = 40 antrenari totale
grid = GridSearchCV(pipe, param_grid, cv=5,
                    scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

print(grid.best_params_)
print(grid.best_score_)
y_pred = grid.predict(X_test)
""", language="python")

        st.markdown("### joblib — salveaza modelul")
        st.markdown("""
        Dupa ce ai antrenat un model bun, nu vrei sa-l reantrenezi
        de fiecare data cand pornesti aplicatia.
        `joblib` salveaza modelul (inclusiv Pipeline) pe disc.
        """)
        st.code("""
import joblib

# Salveaza
joblib.dump(pipe, "model_ndvi.pkl")

# Incarca (alta sesiune, alt calculator)
pipe_incarcat = joblib.load("model_ndvi.pkl")
y_pred = pipe_incarcat.predict(X_nou)
""", language="python")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PIPELINE & GRIDSEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Construieste si optimizeaza un Pipeline")

    col_p, col_r = st.columns([1, 2])

    with col_p:
        st.markdown("#### Configurare Pipeline")

        tip_model = st.selectbox(
            "Algoritmul",
            ["KNN", "SVM", "Random Forest"],
            key="tip_model_pipe"
        )

        foloseste_grid = st.checkbox("Optimizeaza cu GridSearchCV", value=True)

        if foloseste_grid:
            k_folds_gs = st.slider("Folduri CV in GridSearch", 3, 7, 5)
            st.markdown("**Grila de parametri:**")
            if tip_model == "KNN":
                st.code("n_neighbors: [3, 5, 7, 10, 15]\nweights: [uniform, distance]")
            elif tip_model == "SVM":
                st.code("C: [0.1, 1, 10]\nkernel: [rbf, linear]")
            else:
                st.code("n_estimators: [50, 100, 200]\nmax_depth: [5, 10, None]")

        antreneaza_pipe = st.button("Construieste Pipeline", type="primary")

    with col_r:
        if antreneaza_pipe:
            with st.spinner("Antrenare in curs..."):
                if tip_model == "KNN":
                    model_pipe = KNeighborsClassifier()
                    param_grid = {
                        "model__n_neighbors": [3, 5, 7, 10, 15],
                        "model__weights":     ["uniform", "distance"],
                    }
                elif tip_model == "SVM":
                    model_pipe = SVC(probability=True, random_state=42)
                    param_grid = {
                        "model__C":      [0.1, 1.0, 10.0],
                        "model__kernel": ["rbf", "linear"],
                    }
                else:
                    model_pipe = RandomForestClassifier(random_state=42)
                    param_grid = {
                        "model__n_estimators": [50, 100, 200],
                        "model__max_depth":    [5, 10, None],
                    }

                pipe = Pipeline([
                    ("scaler", StandardScaler()),
                    ("model",  model_pipe),
                ])

                if foloseste_grid:
                    skf  = StratifiedKFold(n_splits=k_folds_gs, shuffle=True, random_state=42)
                    grid = GridSearchCV(pipe, param_grid, cv=skf,
                                        scoring="accuracy", n_jobs=-1)
                    grid.fit(X_train, y_train)
                    best_pipe   = grid.best_estimator_
                    best_params = grid.best_params_
                    best_cv     = grid.best_score_
                else:
                    pipe.fit(X_train, y_train)
                    best_pipe   = pipe
                    best_params = {}
                    best_cv     = cross_val_score(pipe, X_train, y_train, cv=5).mean()

                y_pred  = best_pipe.predict(X_test)
                acc     = accuracy_score(y_test, y_pred)

                st.session_state["best_pipe"]   = best_pipe
                st.session_state["pipe_label"]  = tip_model

            # Rezultate
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Acuratete test", f"{acc*100:.2f}%")
            with c2:
                st.metric("CV score (train)", f"{best_cv*100:.2f}%")
            with c3:
                gap = best_cv - acc
                st.metric("Gap train-test", f"{abs(gap)*100:.2f}%",
                           delta=f"{'overfitting' if gap > 0.05 else 'OK'}",
                           delta_color="inverse" if gap > 0.05 else "normal")

            if foloseste_grid and best_params:
                st.markdown("**Cei mai buni parametri gasiti de GridSearchCV:**")
                params_clean = {k.replace("model__", ""): v for k, v in best_params.items()}
                params_df = pd.DataFrame(
                    [{"Parametru": k, "Valoare optima": str(v)}
                     for k, v in params_clean.items()]
                )
                st.dataframe(params_df, use_container_width=True, hide_index=True)

                if PLOTLY_OK:
                    st.markdown("**Toate combinatiile testate:**")
                    results_df = pd.DataFrame(grid.cv_results_)
                    results_df = results_df[["params","mean_test_score","std_test_score"]].copy()
                    results_df["params_str"]  = results_df["params"].apply(
                        lambda p: ", ".join(f"{k.replace('model__','')}={v}"
                                            for k, v in p.items())
                    )
                    results_df = results_df.sort_values("mean_test_score", ascending=True)

                    fig_gs = go.Figure(go.Bar(
                        x=results_df["mean_test_score"] * 100,
                        y=results_df["params_str"],
                        orientation="h",
                        error_x=dict(array=results_df["std_test_score"] * 100),
                        marker_color=["#1abc9c" if s == results_df["mean_test_score"].max()
                                      else "#bdc3c7"
                                      for s in results_df["mean_test_score"]],
                    ))
                    fig_gs.update_layout(
                        xaxis_title="Acuratete CV (%)",
                        height=max(250, len(results_df) * 28),
                        margin=dict(t=10, b=40, l=260, r=20),
                    )
                    st.plotly_chart(fig_gs, use_container_width=True)

            # Raport clasificare
            st.markdown("**Raport per cultura:**")
            report = classification_report(y_test, y_pred, output_dict=True)
            rows_r = [
                {"Cultura": cls,
                 "Precision": f"{report[cls]['precision']:.3f}",
                 "Recall":    f"{report[cls]['recall']:.3f}",
                 "F1-score":  f"{report[cls]['f1-score']:.3f}"}
                for cls in list(CULORI_CULTURA.keys()) if cls in report
            ]
            st.dataframe(pd.DataFrame(rows_r), use_container_width=True, hide_index=True)

        else:
            st.info("Configureaza Pipeline-ul si apasa **Construieste Pipeline**.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EXPORT & INCARCARE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Salveaza si reutilizeaza modelul antrenat")

    col_save, col_load = st.columns(2)

    with col_save:
        st.markdown("#### Salveaza modelul pe disc")

        if "best_pipe" not in st.session_state:
            st.info("Mergi la Tab-ul **Pipeline & GridSearch** si antreneaza un model mai intai.")
        else:
            pipe_de_salvat = st.session_state["best_pipe"]
            label_model    = st.session_state.get("pipe_label", "model")
            nume_fisier    = st.text_input(
                "Nume fisier",
                value=f"model_ndvi_{label_model.lower().replace(' ','_')}.pkl"
            )
            cale_salvare = os.path.join(MODEL_DIR, nume_fisier)

            if st.button("Salveaza model (.pkl)", type="primary"):
                joblib.dump(pipe_de_salvat, cale_salvare)
                st.success(f"Model salvat: `{cale_salvare}`")

                # Descarca si in browser
                buf = io.BytesIO()
                joblib.dump(pipe_de_salvat, buf)
                buf.seek(0)
                st.download_button(
                    label="Descarca .pkl (pentru transfer)",
                    data=buf,
                    file_name=nume_fisier,
                    mime="application/octet-stream"
                )

            st.markdown("**Modele salvate anterior:**")
            fisiere_pkl = [f for f in os.listdir(MODEL_DIR) if f.endswith(".pkl")]
            if fisiere_pkl:
                for f in fisiere_pkl:
                    cale_f   = os.path.join(MODEL_DIR, f)
                    marime   = os.path.getsize(cale_f) / 1024
                    st.markdown(f"""
                    <div style='background:#f8f9fa; border-radius:6px; padding:8px 12px;
                         margin:4px 0; font-size:12px; border-left:3px solid #1abc9c;'>
                        <b>{f}</b> &nbsp;
                        <span style='color:#888;'>{marime:.1f} KB</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Niciun model salvat inca.")

    with col_load:
        st.markdown("#### Incarca model si fa predictii")

        fisiere_disponibile = [f for f in os.listdir(MODEL_DIR) if f.endswith(".pkl")]

        if not fisiere_disponibile:
            st.info("Salveaza un model mai intai (coloana stanga).")
        else:
            fisier_ales = st.selectbox("Alege modelul", fisiere_disponibile)
            cale_de_incarcat = os.path.join(MODEL_DIR, fisier_ales)

            if st.button("Incarca modelul", type="primary"):
                try:
                    pipe_incarcat = joblib.load(cale_de_incarcat)
                    st.session_state["pipe_incarcat"] = pipe_incarcat
                    st.success(f"Model incarcat: `{fisier_ales}`")
                    acc_test = accuracy_score(y_test, pipe_incarcat.predict(X_test))
                    st.metric("Acuratete pe datele de test", f"{acc_test*100:.2f}%")
                except Exception as e:
                    st.error(f"Eroare la incarcare: {e}")

            if "pipe_incarcat" in st.session_state:
                st.divider()
                st.markdown("#### Predictie pe parcela noua (model incarcat)")
                st.caption("Modelul incarcat nu necesita reanrenare sau scaler separat:")

                c1, c2 = st.columns(2)
                with c1:
                    p_mai = st.number_input("NDVI Mai",    0.0, 1.0, 0.65, 0.01, key="l_mai")
                    p_iun = st.number_input("NDVI Iunie",  0.0, 1.0, 0.55, 0.01, key="l_iun")
                with c2:
                    p_iul = st.number_input("NDVI Iulie",  0.0, 1.0, 0.25, 0.01, key="l_iul")
                    p_aug = st.number_input("NDVI August", 0.0, 1.0, 0.15, 0.01, key="l_aug")

                x_nou = np.array([[p_mai, p_iun, p_iul, p_aug]])
                pipe_inc = st.session_state["pipe_incarcat"]
                pred     = pipe_inc.predict(x_nou)[0]
                culoare_pred = CULORI_CULTURA.get(pred, "#333")

                prob_str = ""
                if hasattr(pipe_inc.named_steps["model"], "predict_proba"):
                    proba    = pipe_inc.predict_proba(x_nou)[0]
                    clase_p  = pipe_inc.classes_
                    prob_str = " | ".join(
                        f"{c}: {p*100:.0f}%"
                        for c, p in sorted(zip(clase_p, proba),
                                           key=lambda x: -x[1])[:3]
                    )

                st.markdown(f"""
                <div style='background:{culoare_pred}18; border:2px solid {culoare_pred};
                     border-radius:10px; padding:14px; text-align:center; margin-top:8px;'>
                    <div style='font-size:12px; color:#555;'>Cultura prezisa (model incarcat)</div>
                    <div style='font-size:28px; font-weight:800; color:{culoare_pred};'>{pred}</div>
                    {f"<div style='font-size:11px; color:#777; margin-top:4px;'>{prob_str}</div>"
                     if prob_str else ""}
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 5")

    col1, col2 = st.columns(2)
    concepte = [
        ("Pipeline",               "Inlantuieste pasi (scaler + model) intr-un singur obiect"),
        ("Pipeline.fit()",         "Aplica fit_transform pe scaler, apoi fit pe model — o singura linie"),
        ("Pipeline.predict()",     "Aplica transform (nu fit!) pe scaler, apoi predict — sigur si corect"),
        ("Data Leakage",           "Eroarea de a aplica fit_transform si pe test — Pipeline o previne automat"),
        ("GridSearchCV",           "Testeaza toate combinatiile de hiperparametri cu CV si returneaza cel mai bun"),
        ("param_grid",             "Dictionar {'model__param': [val1, val2]} — notatia dublu underscore"),
        ("best_params_",           "Cei mai buni parametri gasiti: grid.best_params_"),
        ("best_score_",            "Scorul CV al celui mai bun model: grid.best_score_"),
        ("joblib.dump()",          "Salveaza orice obiect Python (Pipeline, model, scaler) pe disc"),
        ("joblib.load()",          "Incarca modelul salvat — gata de predictii fara reanrenare"),
        (".pkl",                   "Formatul fisierului joblib — Pickle binar, portabil intre sesiuni"),
        ("n_jobs=-1",              "GridSearchCV foloseste toate nucleele CPU in paralel — mai rapid"),
    ]

    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f0fff8; border-left:3px solid #1abc9c;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#1abc9c; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib

# 1. Construieste Pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  KNeighborsClassifier()),
])

# 2. GridSearchCV — gaseste parametrii optimi
param_grid = {
    "model__n_neighbors": [3, 5, 7, 10],
    "model__weights":     ["uniform", "distance"],
}
skf  = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = GridSearchCV(pipe, param_grid, cv=skf, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

print(f"Cei mai buni parametri: {grid.best_params_}")
print(f"CV score: {grid.best_score_:.3f}")
print(f"Test score: {grid.score(X_test, y_test):.3f}")

# 3. Salveaza cel mai bun Pipeline
joblib.dump(grid.best_estimator_, "model_ndvi.pkl")

# 4. Incarca si foloseste (alta sesiune)
pipe = joblib.load("model_ndvi.pkl")
pred = pipe.predict([[0.65, 0.55, 0.25, 0.15]])   # nu mai ai nevoie de scaler!
print(f"Cultura: {pred[0]}")
""", language="python")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### De ce conteaza la APIA")
        st.markdown("""
        Un Pipeline + model `.pkl` inseamna ca poti construi
        **o data** modelul de clasificare a culturilor si
        il **redistribui** tuturor inspectorilor APIA:

        - Inspector A incarca `model_ndvi.pkl` pe calculatorul sau
        - Introduce valorile NDVI din LPIS pentru o parcela suspecta
        - Primeste instant clasificarea prezisa
        - Fara Python avansat, fara reanrenare, fara scaler separat

        Acesta este primul pas catre un **instrument operational** pentru
        detectia automata a declaratiilor incorecte.
        """)
    with col_b:
        st.markdown("#### Ziua 6 — Sinteza Modul 1")
        st.markdown("""
        Ultima zi din **Modulul 1 — Machine Learning** va fi o
        **aplicatie integrata** care reuneste tot ce am invatat:

        - Dataset real (CSV uploadat de utilizator)
        - Alegere algoritm + Pipeline + GridSearchCV
        - Evaluare completa: Confusion Matrix, ROC, CV
        - Export model `.pkl`
        - Raport PDF generat automat

        O aplicatie completa, de la date brute la model exportat —
        **tot in Streamlit, tot gratuit**.
        """)

    st.success(
        "**Ziua 5 finalizata!** Pipeline scikit-learn, GridSearchCV si export joblib — "
        "modelul tau ML este acum reproductibil, optimizat si portabil. "
        "Continua cu **Ziua 6 — Sinteza Modul 1**."
    )
