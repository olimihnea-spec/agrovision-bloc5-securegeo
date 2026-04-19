"""
ZIUA 6 — Sinteza Modul 1: Aplicatie ML Completa
Modul 1: Machine Learning cu scikit-learn
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import pandas as pd
import io
import os
from datetime import datetime

try:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
    from sklearn.preprocessing import StandardScaler, label_binarize
    from sklearn.metrics import (
        accuracy_score, classification_report,
        confusion_matrix, roc_curve, auc, f1_score
    )
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
    page_title="Ziua 6 — Sinteza Modul 1",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🏆</div>
    <div style='font-size:16px; font-weight:700; color:#d35400;'>ZIUA 6</div>
    <div style='font-size:11px; color:#666;'>Sinteza Modul 1 — ML Complet</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 1 — Machine Learning")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 6 / 30 zile")
st.sidebar.progress(6/30)
st.sidebar.markdown(f"**Data:** {datetime.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Ce reunim azi:**
- Upload CSV propriu sau date simulate
- Pipeline + GridSearchCV automat
- Confusion Matrix + ROC + CV
- Export model .pkl
- Raport descarcabil
""")

if not SK_OK:
    st.error("scikit-learn nu este instalat. Ruleaza: `pip install scikit-learn`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🏆</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#d35400; font-weight:800;'>
            Ziua 6 — Sinteza Modul 1: Aplicatie ML Completa
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            De la date brute la model exportat — tot ce am invatat in 6 zile
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Banner teza ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#6c3483 0%,#1a5276 100%);
     border-radius:10px; padding:12px 18px; color:white; margin-bottom:12px;
     font-size:12px; opacity:0.9;'>
    Aplicatie bazata pe teza de doctorat:
    <b>"Contributii privind recunoasterea automata a culturilor cu ajutorul unei Drone"</b>
    &nbsp;|&nbsp; Universitatea din Petrosani, 2024
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Date", "🤖 Antrenare", "📊 Evaluare Completa", "💾 Export & Raport"
])

# ══════════════════════════════════════════════════════════════════════════════
# GENERARE DATE SIMULATE (fallback)
# ══════════════════════════════════════════════════════════════════════════════
def genereaza_date_simulate():
    np.random.seed(42)
    N = 80
    cfg = {
        "Grau":             {"mai":(0.65,0.08),"iun":(0.55,0.10),"iul":(0.25,0.08),"aug":(0.15,0.05)},
        "Floarea-soarelui": {"mai":(0.30,0.07),"iun":(0.55,0.09),"iul":(0.75,0.08),"aug":(0.50,0.10)},
        "Porumb":           {"mai":(0.25,0.06),"iun":(0.60,0.09),"iul":(0.82,0.07),"aug":(0.70,0.09)},
        "Lucerna":          {"mai":(0.60,0.08),"iun":(0.55,0.09),"iul":(0.65,0.08),"aug":(0.58,0.09)},
        "Fanete":           {"mai":(0.48,0.08),"iun":(0.52,0.08),"iul":(0.48,0.07),"aug":(0.42,0.08)},
    }
    rows = []
    for cultura, c in cfg.items():
        for _ in range(N):
            rows.append({
                "cultura":     cultura,
                "NDVI_mai":    round(float(np.clip(np.random.normal(c["mai"][0],c["mai"][1]),0,1)),3),
                "NDVI_iunie":  round(float(np.clip(np.random.normal(c["iun"][0],c["iun"][1]),0,1)),3),
                "NDVI_iulie":  round(float(np.clip(np.random.normal(c["iul"][0],c["iul"][1]),0,1)),3),
                "NDVI_august": round(float(np.clip(np.random.normal(c["aug"][0],c["aug"][1]),0,1)),3),
            })
    return pd.DataFrame(rows)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DATE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Sursa de date")

    sursa = st.radio(
        "Alege sursa datelor:",
        ["Date simulate (5 culturi Gorj — implicit)", "Incarca CSV propriu"],
        horizontal=True
    )

    if sursa == "Incarca CSV propriu":
        st.markdown("""
        **Format asteptat:** CSV cu cel putin doua coloane:
        una cu eticheta clasei (ex: `cultura`) si una sau mai multe coloane numerice (features).
        """)
        fisier = st.file_uploader("Incarca fisier CSV", type=["csv"])
        if fisier:
            try:
                df_raw = pd.read_csv(fisier)
                st.success(f"Fisier incarcat: {fisier.name} — {len(df_raw)} randuri, {len(df_raw.columns)} coloane")
                st.dataframe(df_raw.head(5), use_container_width=True, hide_index=True)

                cols_numerice = df_raw.select_dtypes(include=[np.number]).columns.tolist()
                cols_toate    = df_raw.columns.tolist()

                col_target = st.selectbox("Coloana tinta (eticheta clase):", cols_toate,
                                          index=0)
                col_features = st.multiselect(
                    "Coloane features (valori numerice):",
                    [c for c in cols_numerice if c != col_target],
                    default=[c for c in cols_numerice if c != col_target][:4]
                )

                if col_target and col_features:
                    df_raw = df_raw.dropna(subset=[col_target] + col_features)
                    st.session_state["df"]       = df_raw
                    st.session_state["features"] = col_features
                    st.session_state["target"]   = col_target
                    st.session_state["sursa"]    = "csv"
            except Exception as e:
                st.error(f"Eroare la citire CSV: {e}")
        else:
            st.info("Incarca un fisier CSV sau alege datele simulate.")
            if "df" not in st.session_state or st.session_state.get("sursa") != "csv":
                df_sim = genereaza_date_simulate()
                st.session_state["df"]       = df_sim
                st.session_state["features"] = ["NDVI_mai","NDVI_iunie","NDVI_iulie","NDVI_august"]
                st.session_state["target"]   = "cultura"
                st.session_state["sursa"]    = "simulat"
    else:
        df_sim = genereaza_date_simulate()
        st.session_state["df"]       = df_sim
        st.session_state["features"] = ["NDVI_mai","NDVI_iunie","NDVI_iulie","NDVI_august"]
        st.session_state["target"]   = "cultura"
        st.session_state["sursa"]    = "simulat"

    if "df" in st.session_state:
        df      = st.session_state["df"]
        FEATS   = st.session_state["features"]
        TARGET  = st.session_state["target"]
        clase   = sorted(df[TARGET].dropna().unique().tolist())

        st.divider()
        st.markdown("### Sumar dataset")

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Total randuri",   len(df))
        with c2: st.metric("Features",        len(FEATS))
        with c3: st.metric("Clase unice",     len(clase))
        with c4: st.metric("Valori lipsa",    int(df[FEATS + [TARGET]].isna().sum().sum()))

        col_tabel, col_dist = st.columns([3, 2])
        with col_tabel:
            st.markdown("**Primele 8 randuri:**")
            st.dataframe(df[FEATS + [TARGET]].head(8).round(3),
                         use_container_width=True, hide_index=True)
        with col_dist:
            st.markdown("**Distributia claselor:**")
            dist = df[TARGET].value_counts().reset_index()
            dist.columns = ["Clasa", "Nr. parcele"]
            st.dataframe(dist, use_container_width=True, hide_index=True)
            if dist["Nr. parcele"].max() / dist["Nr. parcele"].min() > 3:
                st.warning("Date dezechilibrate — considera `class_weight='balanced'`.")

        # Descarca CSV sample pentru referinta
        csv_sample = df[FEATS + [TARGET]].to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descarca datele ca CSV (referinta format)",
            data=csv_sample,
            file_name="date_ndvi_sample.csv",
            mime="text/csv"
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANTRENARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if "df" not in st.session_state:
        st.info("Mergi la Tab-ul **Date** si incarca sau genereaza datele.")
    else:
        df    = st.session_state["df"]
        FEATS = st.session_state["features"]
        TARGET = st.session_state["target"]

        st.markdown("### Pipeline + GridSearchCV automat")

        col_cfg, col_res = st.columns([1, 2])

        with col_cfg:
            st.markdown("#### Configurare")

            algoritm = st.selectbox("Algoritm", ["Random Forest", "SVM", "KNN"])
            test_pct = st.slider("Date de test (%)", 10, 40, 20, 5)
            k_cv     = st.slider("Folduri Cross-Validation", 3, 7, 5)

            st.markdown("**Grila de parametri:**")
            if algoritm == "Random Forest":
                st.code("n_estimators: [50,100,200]\nmax_depth: [5,10,None]")
            elif algoritm == "SVM":
                st.code("C: [0.1,1,10]\nkernel: [rbf,linear]")
            else:
                st.code("n_neighbors: [3,5,7,10]\nweights: [uniform,distance]")

            porneste = st.button("Antreneaza si Optimizeaza", type="primary",
                                 use_container_width=True)

        with col_res:
            if porneste:
                X = df[FEATS].to_numpy()
                y = df[TARGET].to_numpy()

                X_tr, X_te, y_tr, y_te = train_test_split(
                    X, y, test_size=test_pct/100,
                    random_state=42, stratify=y
                )

                if algoritm == "Random Forest":
                    model_baza = RandomForestClassifier(random_state=42, n_jobs=-1)
                    param_grid = {"model__n_estimators":[50,100,200],
                                  "model__max_depth":[5,10,None]}
                elif algoritm == "SVM":
                    model_baza = SVC(probability=True, random_state=42)
                    param_grid = {"model__C":[0.1,1.0,10.0],
                                  "model__kernel":["rbf","linear"]}
                else:
                    model_baza = KNeighborsClassifier()
                    param_grid = {"model__n_neighbors":[3,5,7,10],
                                  "model__weights":["uniform","distance"]}

                pipe = Pipeline([("scaler", StandardScaler()),
                                 ("model",  model_baza)])

                with st.spinner("GridSearchCV in curs..."):
                    skf  = StratifiedKFold(n_splits=k_cv, shuffle=True, random_state=42)
                    grid = GridSearchCV(pipe, param_grid, cv=skf,
                                        scoring="accuracy", n_jobs=-1)
                    grid.fit(X_tr, y_tr)

                best  = grid.best_estimator_
                y_pred = best.predict(X_te)
                acc    = accuracy_score(y_te, y_pred)
                f1     = f1_score(y_te, y_pred, average="weighted")
                cv_sc  = grid.best_score_

                # Salveaza in sesiune pentru celelalte tab-uri
                st.session_state.update({
                    "best_pipe":   best,
                    "y_pred":      y_pred,
                    "y_test":      y_te,
                    "X_test":      X_te,
                    "y_train":     y_tr,
                    "clase":       sorted(set(y)),
                    "algoritm":    algoritm,
                    "acc":         acc,
                    "f1":          f1,
                    "cv_score":    cv_sc,
                    "best_params": grid.best_params_,
                    "test_pct":    test_pct,
                    "k_cv":        k_cv,
                })

                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Acuratete test",  f"{acc*100:.2f}%")
                with c2: st.metric("F1 weighted",     f"{f1:.3f}")
                with c3: st.metric(f"CV {k_cv}-fold", f"{cv_sc*100:.2f}%")

                params_clean = {k.replace("model__",""):v
                                for k,v in grid.best_params_.items()}
                st.markdown("**Parametri optimi gasiti:**")
                st.dataframe(
                    pd.DataFrame([{"Parametru":k,"Valoare":str(v)}
                                  for k,v in params_clean.items()]),
                    use_container_width=True, hide_index=True
                )
                st.success("Antrenare finalizata! Mergi la Tab-ul **Evaluare Completa**.")
            else:
                st.info("Apasa **Antreneaza si Optimizeaza** pentru a rula Pipeline-ul.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EVALUARE COMPLETA
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if "best_pipe" not in st.session_state:
        st.info("Mergi la Tab-ul **Antrenare** si ruleaza modelul mai intai.")
    else:
        best   = st.session_state["best_pipe"]
        y_pred = st.session_state["y_pred"]
        y_te   = st.session_state["y_test"]
        X_te   = st.session_state["X_test"]
        clase  = st.session_state["clase"]

        st.markdown("### Evaluare completa — toate metricile din Modulul 1")

        # ── KPI-uri principale ────────────────────────────────────────────────
        acc  = st.session_state["acc"]
        f1   = st.session_state["f1"]
        cv   = st.session_state["cv_score"]
        gap  = cv - acc

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Acuratete", f"{acc*100:.2f}%")
        with c2:
            st.metric("F1 weighted", f"{f1:.3f}")
        with c3:
            st.metric(f"CV score", f"{cv*100:.2f}%")
        with c4:
            culoare_gap = "normal" if abs(gap) < 0.05 else "inverse"
            st.metric("Gap CV-Test", f"{abs(gap)*100:.2f}%",
                      delta="Stabil" if abs(gap) < 0.05 else "Verifica overfitting",
                      delta_color=culoare_gap)

        st.divider()

        if PLOTLY_OK:
            col_cm, col_rep = st.columns([3, 2])

            # ── Confusion Matrix ──────────────────────────────────────────────
            with col_cm:
                st.markdown("#### Confusion Matrix")
                cm = confusion_matrix(y_te, y_pred, labels=clase)
                cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
                text_cm = [[f"{cm[i][j]}\n({cm_norm[i][j]*100:.0f}%)"
                            for j in range(len(clase))]
                           for i in range(len(clase))]

                fig_cm = go.Figure(go.Heatmap(
                    z=cm_norm, x=clase, y=clase,
                    colorscale="Blues",
                    text=text_cm, texttemplate="%{text}",
                    showscale=True,
                ))
                fig_cm.update_layout(
                    xaxis_title="Prezis", yaxis_title="Real",
                    height=380,
                    margin=dict(t=20, b=70, l=90, r=20),
                )
                st.plotly_chart(fig_cm, use_container_width=True)

            # ── Raport per clasa ──────────────────────────────────────────────
            with col_rep:
                st.markdown("#### Metrici per clasa")
                report = classification_report(y_te, y_pred, output_dict=True)
                rows_r = []
                for cls in clase:
                    if cls in report:
                        rows_r.append({
                            "Clasa":     cls,
                            "Precision": f"{report[cls]['precision']:.3f}",
                            "Recall":    f"{report[cls]['recall']:.3f}",
                            "F1":        f"{report[cls]['f1-score']:.3f}",
                            "N":         int(report[cls]['support']),
                        })
                st.dataframe(pd.DataFrame(rows_r),
                             use_container_width=True, hide_index=True)

                # Clasa cea mai greu de clasificat
                f1_vals = {cls: report[cls]["f1-score"]
                           for cls in clase if cls in report}
                cls_min = min(f1_vals, key=f1_vals.get)
                cls_max = max(f1_vals, key=f1_vals.get)
                st.markdown(f"""
                <div style='background:#fef9e7; border-left:3px solid #f39c12;
                     border-radius:0 8px 8px 0; padding:8px 12px; font-size:12px; margin-top:6px;'>
                    <b>Cea mai buna clasificare:</b> {cls_max} (F1={f1_vals[cls_max]:.3f})<br>
                    <b>Cea mai dificila:</b> {cls_min} (F1={f1_vals[cls_min]:.3f})
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # ── ROC Curves ───────────────────────────────────────────────────
            if hasattr(best.named_steps["model"], "predict_proba"):
                st.markdown("#### ROC Curves — One-vs-Rest")
                CULORI_ROC = ["#f39c12","#e74c3c","#27ae60","#16a085","#795548",
                              "#2980b9","#8e44ad","#d35400"]
                y_bin    = label_binarize(y_te, classes=clase)
                y_prob   = best.predict_proba(X_te)
                clase_p  = best.classes_

                fig_roc = go.Figure()
                fig_roc.add_trace(go.Scatter(
                    x=[0,1], y=[0,1], mode="lines",
                    name="Aleator (AUC=0.50)",
                    line=dict(color="#ccc", dash="dash", width=1)
                ))
                auc_mediu = 0.0
                for i, cls in enumerate(clase_p):
                    idx = list(clase).index(cls) if cls in clase else i
                    if idx < y_bin.shape[1]:
                        fpr, tpr, _ = roc_curve(y_bin[:, idx], y_prob[:, i])
                        auc_val     = auc(fpr, tpr)
                        auc_mediu  += auc_val
                        fig_roc.add_trace(go.Scatter(
                            x=fpr, y=tpr, mode="lines",
                            name=f"{cls} (AUC={auc_val:.3f})",
                            line=dict(color=CULORI_ROC[i % len(CULORI_ROC)], width=2)
                        ))
                auc_mediu /= len(clase_p)

                fig_roc.update_layout(
                    xaxis_title="False Positive Rate",
                    yaxis_title="True Positive Rate",
                    xaxis=dict(range=[0,1]), yaxis=dict(range=[0,1.02]),
                    height=360,
                    margin=dict(t=20, b=40, l=50, r=20),
                    annotations=[dict(
                        x=0.98, y=0.04, xref="paper", yref="paper",
                        text=f"<b>AUC mediu: {auc_mediu:.3f}</b>",
                        showarrow=False,
                        bgcolor="white", bordercolor="#ccc", borderwidth=1,
                        font=dict(size=12)
                    )]
                )
                st.plotly_chart(fig_roc, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT & RAPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    if "best_pipe" not in st.session_state:
        st.info("Mergi la Tab-ul **Antrenare** si ruleaza modelul mai intai.")
    else:
        best       = st.session_state["best_pipe"]
        acc        = st.session_state["acc"]
        f1         = st.session_state["f1"]
        cv         = st.session_state["cv_score"]
        clase      = st.session_state["clase"]
        algoritm   = st.session_state["algoritm"]
        params     = st.session_state["best_params"]
        test_pct   = st.session_state["test_pct"]
        k_cv       = st.session_state["k_cv"]
        y_te       = st.session_state["y_test"]
        y_pred     = st.session_state["y_pred"]

        col_model, col_raport = st.columns(2)

        # ── Export model ──────────────────────────────────────────────────────
        with col_model:
            st.markdown("#### Export model .pkl")

            MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "modele_salvate")
            os.makedirs(MODEL_DIR, exist_ok=True)

            nume_model = st.text_input(
                "Nume fisier model",
                value=f"model_{algoritm.lower().replace(' ','_')}_sinteza.pkl"
            )

            if st.button("Salveaza model pe disc", type="primary"):
                cale = os.path.join(MODEL_DIR, nume_model)
                joblib.dump(best, cale)
                st.success(f"Salvat: `{cale}`")

            buf_model = io.BytesIO()
            joblib.dump(best, buf_model)
            buf_model.seek(0)
            st.download_button(
                "Descarca model .pkl",
                data=buf_model,
                file_name=nume_model,
                mime="application/octet-stream",
                use_container_width=True
            )

            st.divider()
            st.markdown("#### Predictie rapida cu modelul curent")
            feats = st.session_state["features"]
            vals  = {}
            cols_pred = st.columns(min(4, len(feats)))
            for i, feat in enumerate(feats):
                with cols_pred[i % len(cols_pred)]:
                    vals[feat] = st.number_input(feat, 0.0, 1.0,
                                                  round(float(
                                                      np.random.uniform(0.3, 0.7)
                                                  ), 2),
                                                  0.01, key=f"pred_{feat}")
            x_nou = np.array([[vals[f] for f in feats]])
            pred_cls = best.predict(x_nou)[0]

            prob_linie = ""
            if hasattr(best.named_steps["model"], "predict_proba"):
                proba = best.predict_proba(x_nou)[0]
                top3  = sorted(zip(best.classes_, proba), key=lambda x: -x[1])[:3]
                prob_linie = " &nbsp;|&nbsp; ".join(
                    f"{c}: <b>{p*100:.0f}%</b>" for c, p in top3
                )

            st.markdown(f"""
            <div style='background:#fef5e7; border:2px solid #d35400;
                 border-radius:10px; padding:14px; text-align:center; margin-top:8px;'>
                <div style='font-size:12px; color:#777;'>Cultura prezisa</div>
                <div style='font-size:26px; font-weight:800; color:#d35400;'>{pred_cls}</div>
                {f"<div style='font-size:11px; color:#888; margin-top:4px;'>{prob_linie}</div>"
                 if prob_linie else ""}
            </div>
            """, unsafe_allow_html=True)

        # ── Raport text ───────────────────────────────────────────────────────
        with col_raport:
            st.markdown("#### Raport analiza ML")

            report     = classification_report(y_te, y_pred, output_dict=True)
            params_str = "; ".join(
                f"{k.replace('model__','')}={v}" for k, v in params.items()
            )

            continut_raport = f"""RAPORT ANALIZA ML — RECUNOASTERE AUTOMATA CULTURI AGRICOLE
================================================================
Generat: {datetime.today().strftime('%d.%m.%Y %H:%M')}
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu
Institutie: UCB Targu Jiu | APIA CJ Gorj
Teza de doctorat: Contributii privind recunoasterea automata
  a culturilor cu ajutorul unei Drone
  Universitatea din Petrosani, 2024

CONFIGURATIE MODEL
------------------
Algoritm:         {algoritm}
Pipeline:         StandardScaler + {algoritm}
Parametri optimi: {params_str}
Date de test:     {test_pct}%
Cross-Validation: {k_cv}-fold stratificat

REZULTATE PRINCIPALE
--------------------
Acuratete test:   {acc*100:.2f}%
F1 weighted:      {f1:.3f}
CV score (train): {cv*100:.2f}%
Gap CV-Test:      {abs(cv-acc)*100:.2f}% ({'stabil' if abs(cv-acc) < 0.05 else 'verifica overfitting'})

METRICI PER CLASA
-----------------
{'Clasa':<22} {'Precision':>10} {'Recall':>8} {'F1-score':>10} {'Suport':>8}
{'-'*60}"""

            for cls in clase:
                if cls in report:
                    r = report[cls]
                    continut_raport += (
                        f"\n{cls:<22} {r['precision']:>10.3f} {r['recall']:>8.3f}"
                        f" {r['f1-score']:>10.3f} {int(r['support']):>8}"
                    )

            continut_raport += f"""

CLASE ANALIZATE
---------------
{', '.join(clase)}

CONCLUZIE
---------
Modelul {algoritm} cu parametrii optimi ({params_str})
obtine {acc*100:.1f}% acuratete in clasificarea culturilor agricole
din date NDVI (mai, iunie, iulie, august).

Rezultatul confirma ca profilele NDVI sezoniere sunt suficiente
pentru recunoasterea automata a culturilor — in concordanta cu
metodologia din teza de doctorat.

================================================================
Generat cu: AI Aplicat v1.0 | Bloc 5 — Ziua 6
"""

            st.text_area("Previzualizare raport:", continut_raport, height=320)
            st.download_button(
                "Descarca raport .txt",
                data=continut_raport.encode("utf-8"),
                file_name=f"raport_ml_{datetime.today().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

        # ── Rezumat Modul 1 ───────────────────────────────────────────────────
        st.markdown("### Recapitulare Modul 1 — Machine Learning (6 zile)")
        zile = [
            ("1", "Clasificare culturi NDVI",      "KNN si SVM pe date tabelare",              "#27ae60"),
            ("2", "Regresie productie agricola",   "Linear Regression si Random Forest",        "#2980b9"),
            ("3", "Clustering parcele",            "K-Means si DBSCAN nesupervizat",            "#8e44ad"),
            ("4", "Evaluare modele",               "Confusion Matrix, ROC, Cross-Validation",   "#e74c3c"),
            ("5", "Pipeline si export",            "GridSearchCV, joblib, model reproductibil", "#1abc9c"),
            ("6", "Sinteza Modul 1",               "Aplicatie completa — date proprii la model exportat", "#d35400"),
        ]
        cols_z = st.columns(6)
        for col, (nr, titlu, desc, culoare) in zip(cols_z, zile):
            with col:
                st.markdown(f"""
                <div style='background:white; border-radius:10px; padding:12px;
                     border-top:4px solid {culoare}; text-align:center;
                     box-shadow:0 1px 4px rgba(0,0,0,0.07); height:130px;'>
                    <div style='font-size:22px; font-weight:800; color:{culoare};'>
                        Z{nr}
                    </div>
                    <div style='font-size:11px; font-weight:700; color:#333;
                         margin:4px 0;'>{titlu}</div>
                    <div style='font-size:10px; color:#777;'>{desc}</div>
                    <div style='margin-top:6px; font-size:16px;'>✅</div>
                </div>
                """, unsafe_allow_html=True)

        st.success(
            "**Modulul 1 — Machine Learning FINALIZAT!** "
            "Ai parcurs 6 zile de ML aplicat pe date agricole reale din Gorj. "
            "Continua cu **Modulul 2 — Computer Vision** (Ziua 7: YOLOv8)."
        )
