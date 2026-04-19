"""
ZIUA 4 — Evaluare Modele ML
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
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, learning_curve
    from sklearn.metrics import (
        confusion_matrix, classification_report,
        roc_curve, auc, accuracy_score
    )
    from sklearn.preprocessing import StandardScaler, label_binarize
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
    page_title="Ziua 4 — Evaluare Modele",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>📐</div>
    <div style='font-size:16px; font-weight:700; color:#e74c3c;'>ZIUA 4</div>
    <div style='font-size:11px; color:#666;'>Evaluare Modele ML</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 1 — Machine Learning")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 4 / 30 zile")
st.sidebar.progress(4/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 4:**
- Confusion Matrix aprofundata
- Precision, Recall, F1-score
- ROC Curve si AUC
- Cross-Validation (k-fold)
- Overfitting vs Underfitting
- Learning Curves
- Cum alegem cel mai bun model
""")

if not SK_OK:
    st.error("scikit-learn nu este instalat. Ruleaza: `pip install scikit-learn`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>📐</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#e74c3c; font-weight:800;'>
            Ziua 4 — Evaluare Corecta a Modelelor ML
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 1 — Machine Learning &nbsp;|&nbsp;
            Confusion Matrix, ROC, Cross-Validation, Overfitting
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "📊 Confusion Matrix", "📈 ROC & Cross-Validation", "📚 Overfitting & Rezumat"
])

# ══════════════════════════════════════════════════════════════════════════════
# DATE (identic cu zilele anterioare)
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
CLASE = list(CULORI_CULTURA.keys())

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

scaler = StandardScaler()
X_sc   = scaler.fit_transform(X_all)

X_train, X_test, y_train, y_test = train_test_split(
    X_sc, y_all, test_size=0.2, random_state=42, stratify=y_all
)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### De ce acuratetea singura nu e suficienta?")

    st.warning("""
    **Problema:** Un model cu 95% acuratete poate totusi sa fie prost.

    Exemplu extrem: daca 95% din parcelele APIA sunt grau si modelul prezice
    intotdeauna \"Grau\", are 95% acuratete — dar nu invata nimic util.
    Avem nevoie de metrici mai nuantate.
    """)

    st.divider()
    st.markdown("### Confusion Matrix — tabloul de bord al clasificarii")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        O Confusion Matrix arata **cate predictii** au fost corecte si unde
        a gresit modelul, pentru **fiecare clasa**.

        Linie = clasa **reala** | Coloana = clasa **prezisa**

        - **Diagonala principala** = predictii corecte (TP per clasa)
        - **In afara diagonalei** = erori (confuzii intre clase)
        """)

        st.markdown("#### Din Confusion Matrix derivam:")
        metrici = [
            ("Precision",
             "Din toate parcelele prezise ca Grau, cate sunt cu adevarat Grau?",
             "TP / (TP + FP)", "#2980b9",
             "Important cand costul unui fals pozitiv e mare"),
            ("Recall (Sensitivity)",
             "Din toate parcelele reale de Grau, cate a detectat modelul?",
             "TP / (TP + FN)", "#27ae60",
             "Important cand costul unui fals negativ e mare"),
            ("F1-score",
             "Media armonica intre Precision si Recall — echilibru intre ele",
             "2 * P*R / (P+R)", "#8e44ad",
             "Cel mai util cand clasele sunt dezechilibrate"),
        ]
        for nume, desc, formula, culoare, cand in metrici:
            st.markdown(f"""
            <div style='border-left:4px solid {culoare}; background:white;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;
                 box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                <div style='font-weight:700; color:{culoare};'>{nume}
                    <span style='font-size:11px; background:{culoare}22;
                    padding:2px 6px; border-radius:4px; margin-left:8px;'>{formula}</span>
                </div>
                <div style='font-size:12px; color:#333; margin-top:4px;'>{desc}</div>
                <div style='font-size:11px; color:#888; margin-top:2px;'>{cand}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Analogie APIA")
        st.markdown("""
        <div style='background:#fff3e0; border-radius:10px; padding:14px;
             border-top:4px solid #f39c12;'>
            <div style='font-weight:700; color:#f39c12;'>Inspector control parcele</div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>TP</b> = parcel frauduloasa detectata corect<br><br>
                <b>FP</b> = parcel corecta marcata gresit (fermier nevinovat deranjat)<br><br>
                <b>FN</b> = parcel frauduloasa nedetectata (frauda netaxata)<br><br>
                <b>TN</b> = parcel corecta, lasata in pace<br><br>
                <hr style='margin:8px 0; border-color:#eee;'>
                La APIA vrei <b>Recall mare</b> (prindeti cat mai multe fraude),
                dar si <b>Precision rezonabila</b> (sa nu deranjati fermierii corecti).
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### ROC Curve si AUC")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **ROC** (Receiver Operating Characteristic) arata trade-off-ul dintre:
        - **TPR** (True Positive Rate = Recall) — cat din pozitivele reale sunt detectate
        - **FPR** (False Positive Rate) — cat din negativele reale sunt gresit clasificate ca pozitive

        Curba e trasata pentru **toate pragurile posibile de decizie** (0.0 → 1.0).

        **AUC** (Area Under Curve):
        - AUC = 1.0 → model perfect
        - AUC = 0.5 → model aleator (linia diagonala)
        - AUC < 0.5 → model mai prost decat aruncatul cu banul
        """)
    with col2:
        st.markdown("""
        <div style='background:#e8f4fd; border-radius:10px; padding:14px;
             border-top:4px solid #2980b9;'>
            <div style='font-weight:700; color:#2980b9;'>Cross-Validation (k-fold)</div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Problema:</b> un singur train/test split poate da rezultate
                norocoase sau ghinioniste.<br><br>
                <b>Solutia:</b> imparte datele in K parti (folds),
                antreneaza de K ori — de fiecare data un fold diferit e testul.<br><br>
                <b>Rezultat:</b> K scoruri → media si deviatia standard
                = estimare mai robusta a performantei reale.<br><br>
                <b>Tipic:</b> k=5 sau k=10
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CONFUSION MATRIX
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Confusion Matrix interactiva")

    col_p, col_r = st.columns([1, 2])
    with col_p:
        st.markdown("#### Parametri")
        model_cm = st.selectbox(
            "Model",
            ["KNN (k=5)", "KNN (k=1) — overfitting", "SVM", "Random Forest"],
            key="model_cm"
        )
        normalizeaza_cm = st.checkbox("Normalizeaza (proportii)", value=False,
                                      help="Arata procentele in loc de numarul de parcele")
        ruleaza_cm = st.button("Calculeaza Confusion Matrix", type="primary")

    with col_r:
        if ruleaza_cm:
            if model_cm == "KNN (k=5)":
                clf = KNeighborsClassifier(n_neighbors=5)
            elif model_cm == "KNN (k=1) — overfitting":
                clf = KNeighborsClassifier(n_neighbors=1)
            elif model_cm == "SVM":
                clf = SVC(kernel="rbf", C=1.0, random_state=42, probability=True)
            else:
                clf = RandomForestClassifier(n_estimators=100, random_state=42)

            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            acc    = accuracy_score(y_test, y_pred)

            cm = confusion_matrix(y_test, y_pred, labels=CLASE)
            if normalizeaza_cm:
                cm_plot = cm.astype(float) / cm.sum(axis=1, keepdims=True)
                fmt_cm  = ".2f"
            else:
                cm_plot = cm
                fmt_cm  = "d"

            # Raport per clasa
            report = classification_report(y_test, y_pred, output_dict=True)
            rows_r = []
            for cls in CLASE:
                if cls in report:
                    rows_r.append({
                        "Cultura":   cls,
                        "Precision": f"{report[cls]['precision']:.3f}",
                        "Recall":    f"{report[cls]['recall']:.3f}",
                        "F1-score":  f"{report[cls]['f1-score']:.3f}",
                        "Suport":    int(report[cls]['support']),
                    })

            st.metric("Acuratete generala", f"{acc*100:.1f}%")

            if PLOTLY_OK:
                col_cm, col_rep = st.columns([3, 2])

                with col_cm:
                    text_matrix = [[f"{cm_plot[i][j]:{fmt_cm}}" for j in range(len(CLASE))]
                                   for i in range(len(CLASE))]
                    fig_cm = go.Figure(go.Heatmap(
                        z=cm_plot,
                        x=CLASE, y=CLASE,
                        colorscale="Blues",
                        text=text_matrix,
                        texttemplate="%{text}",
                        showscale=True,
                    ))
                    fig_cm.update_layout(
                        xaxis_title="Prezis",
                        yaxis_title="Real",
                        height=380,
                        margin=dict(t=20, b=60, l=80, r=20),
                    )
                    st.plotly_chart(fig_cm, use_container_width=True)
                    st.caption(
                        "Diagonala = clasificari corecte. "
                        "Valori in afara diagonalei = confuzii. "
                        "Ex: randul 'Lucerna', coloana 'Fanete' = parcele de Lucerna "
                        "clasificate gresit ca Fanete."
                    )

                with col_rep:
                    st.markdown("**Metrici per cultura:**")
                    st.dataframe(pd.DataFrame(rows_r),
                                 use_container_width=True, hide_index=True)

                    # Erori cele mai frecvente
                    erori = []
                    for i, cls_real in enumerate(CLASE):
                        for j, cls_prez in enumerate(CLASE):
                            if i != j and cm[i][j] > 0:
                                erori.append({
                                    "Real": cls_real,
                                    "Prezis ca": cls_prez,
                                    "Nr. greseli": int(cm[i][j])
                                })
                    if erori:
                        erori_df = pd.DataFrame(erori).sort_values("Nr. greseli", ascending=False)
                        st.markdown("**Cele mai frecvente confuzii:**")
                        st.dataframe(erori_df.head(5), use_container_width=True, hide_index=True)
                        top = erori_df.iloc[0]
                        st.caption(
                            f"Confuzia principala: {top['Real']} clasificata ca "
                            f"{top['Prezis ca']} ({top['Nr. greseli']} cazuri) — "
                            "probabil profile NDVI similare intre aceste doua culturi."
                        )
        else:
            st.info("Apasa **Calculeaza Confusion Matrix** pentru a vedea rezultatele.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ROC & CROSS-VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col_left, col_right = st.columns(2)

    # ── ROC ──────────────────────────────────────────────────────────────────
    with col_left:
        st.markdown("### ROC Curve (One-vs-Rest)")
        st.caption("Fiecare curba = o cultura vs toate celelalte")

        model_roc = st.selectbox(
            "Model pentru ROC",
            ["SVM", "KNN (k=5)", "Random Forest"],
            key="model_roc"
        )
        ruleaza_roc = st.button("Calculeaza ROC", type="primary")

        if ruleaza_roc:
            if model_roc == "SVM":
                clf_roc = SVC(kernel="rbf", C=1.0, random_state=42, probability=True)
            elif model_roc == "KNN (k=5)":
                clf_roc = KNeighborsClassifier(n_neighbors=5)
            else:
                clf_roc = RandomForestClassifier(n_estimators=100, random_state=42)

            clf_roc.fit(X_train, y_train)

            # Binarizare pentru ROC multiclasa
            y_test_bin  = label_binarize(y_test, classes=CLASE)
            y_score     = (clf_roc.predict_proba(X_test)
                           if hasattr(clf_roc, "predict_proba")
                           else None)

            if y_score is not None and PLOTLY_OK:
                fig_roc = go.Figure()
                # Linia de referinta (model aleator)
                fig_roc.add_trace(go.Scatter(
                    x=[0, 1], y=[0, 1],
                    mode="lines", name="Aleator (AUC=0.50)",
                    line=dict(color="#ccc", dash="dash", width=1)
                ))

                for i, (cultura, culoare) in enumerate(CULORI_CULTURA.items()):
                    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
                    auc_val     = auc(fpr, tpr)
                    fig_roc.add_trace(go.Scatter(
                        x=fpr, y=tpr,
                        mode="lines",
                        name=f"{cultura} (AUC={auc_val:.3f})",
                        line=dict(color=culoare, width=2)
                    ))

                fig_roc.update_layout(
                    xaxis_title="False Positive Rate",
                    yaxis_title="True Positive Rate (Recall)",
                    xaxis=dict(range=[0, 1]),
                    yaxis=dict(range=[0, 1.02]),
                    height=380,
                    margin=dict(t=20, b=40, l=50, r=20),
                )
                st.plotly_chart(fig_roc, use_container_width=True)
                st.caption(
                    "Curba mai aproape de coltul stanga-sus = model mai bun. "
                    "AUC aproape de 1.0 = cultura usor de clasificat. "
                    "AUC aproape de 0.5 = cultura greu de separat de celelalte."
                )
            else:
                st.info("Modelul ales nu suporta probabilitati. Alege SVM sau Random Forest.")
        else:
            st.info("Apasa **Calculeaza ROC** pentru a vedea curbele.")

    # ── CROSS-VALIDATION ─────────────────────────────────────────────────────
    with col_right:
        st.markdown("### Cross-Validation (k-fold)")

        model_cv = st.selectbox(
            "Model pentru CV",
            ["KNN (k=5)", "SVM", "Random Forest"],
            key="model_cv"
        )
        k_folds = st.slider("Numar folduri (k)", 3, 10, 5)
        ruleaza_cv = st.button("Ruleaza Cross-Validation", type="primary")

        if ruleaza_cv:
            if model_cv == "KNN (k=5)":
                clf_cv = KNeighborsClassifier(n_neighbors=5)
            elif model_cv == "SVM":
                clf_cv = SVC(kernel="rbf", C=1.0, random_state=42)
            else:
                clf_cv = RandomForestClassifier(n_estimators=100, random_state=42)

            skf    = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)
            scoruri = cross_val_score(clf_cv, X_sc, y_all, cv=skf, scoring="accuracy")

            st.markdown(f"**Rezultate {k_folds}-fold CV:**")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Medie", f"{scoruri.mean()*100:.2f}%")
            with c2:
                st.metric("Std Dev", f"{scoruri.std()*100:.2f}%")
            with c3:
                st.metric("Min / Max",
                          f"{scoruri.min()*100:.1f}% / {scoruri.max()*100:.1f}%")

            if PLOTLY_OK:
                fig_cv = go.Figure()
                fig_cv.add_trace(go.Bar(
                    x=[f"Fold {i+1}" for i in range(k_folds)],
                    y=scoruri * 100,
                    marker_color=["#27ae60" if s >= scoruri.mean() else "#e74c3c"
                                  for s in scoruri],
                    text=[f"{s*100:.1f}%" for s in scoruri],
                    textposition="outside",
                ))
                fig_cv.add_hline(
                    y=scoruri.mean() * 100,
                    line_dash="dash", line_color="#2980b9",
                    annotation_text=f"Medie: {scoruri.mean()*100:.2f}%",
                    annotation_position="right"
                )
                fig_cv.update_layout(
                    yaxis_title="Acuratete (%)",
                    yaxis=dict(range=[max(0, scoruri.min()*100 - 5), 101]),
                    height=320,
                    margin=dict(t=20, b=30, l=50, r=80),
                )
                st.plotly_chart(fig_cv, use_container_width=True)

            st.markdown(f"""
            <div style='background:#e8f4fd; border-left:4px solid #2980b9;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin-top:8px;'>
                <b>Interpretare:</b> Modelul are
                <b>{scoruri.mean()*100:.1f}% ± {scoruri.std()*100:.1f}%</b> acuratete
                in medie pe {k_folds} evaluari independente.<br>
                Deviatia mica ({scoruri.std()*100:.2f}%) indica un model
                <b>stabil</b> — nu depinde de cum sunt impartite datele.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Apasa **Ruleaza Cross-Validation** pentru a vedea rezultatele.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — OVERFITTING & REZUMAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Overfitting vs Underfitting — cel mai important concept in ML")

    col1, col2, col3 = st.columns(3)
    for col, (tip, culoare, desc, semne, solutie) in zip(
        [col1, col2, col3],
        [
            ("Underfitting", "#3498db",
             "Modelul este prea simplu — nu invata nici macar datele de antrenare.",
             "Acuratete mica pe train SI pe test",
             "Model mai complex, mai multe features, mai multi arbori"),
            ("Just right", "#27ae60",
             "Modelul generalizeaza bine — invata tiparele, nu zgomotul.",
             "Acuratete buna pe train, similara pe test",
             "Acesta e obiectivul — mentine-l cu regularizare si CV"),
            ("Overfitting", "#e74c3c",
             "Modelul memoreaza datele de antrenare — esueaza pe date noi.",
             "Acuratete foarte mare pe train, mica pe test",
             "Regularizare, mai multe date, cross-validation, dropout"),
        ]
    ):
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:14px;
                 border-top:4px solid {culoare}; box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
                <div style='font-weight:700; color:{culoare}; font-size:15px;'>{tip}</div>
                <div style='font-size:12px; color:#555; margin-top:6px;'>{desc}</div>
                <div style='margin-top:10px; font-size:11px;'>
                    <b style='color:#333;'>Semne:</b><br>
                    <span style='color:#666;'>{semne}</span>
                </div>
                <div style='margin-top:6px; font-size:11px;'>
                    <b style='color:#333;'>Solutii:</b><br>
                    <span style='color:#666;'>{solutie}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Demonstratie Overfitting — KNN cu K diferit")
    st.caption("K mic = model complex (overfitting), K mare = model simplu (underfitting)")

    ruleaza_ov = st.button("Arata demonstratia Overfitting vs Underfitting", type="primary")

    if ruleaza_ov:
        k_values    = list(range(1, 31))
        acc_train   = []
        acc_test    = []

        for k in k_values:
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X_train, y_train)
            acc_train.append(accuracy_score(y_train, knn.predict(X_train)))
            acc_test.append(accuracy_score(y_test,  knn.predict(X_test)))

        if PLOTLY_OK:
            fig_ov = go.Figure()
            fig_ov.add_trace(go.Scatter(
                x=k_values, y=[a*100 for a in acc_train],
                mode="lines+markers", name="Acuratete TRAIN",
                line=dict(color="#e74c3c", width=2),
                marker=dict(size=5)
            ))
            fig_ov.add_trace(go.Scatter(
                x=k_values, y=[a*100 for a in acc_test],
                mode="lines+markers", name="Acuratete TEST",
                line=dict(color="#27ae60", width=2),
                marker=dict(size=5)
            ))

            best_k    = k_values[acc_test.index(max(acc_test))]
            fig_ov.add_vline(
                x=best_k, line_dash="dot", line_color="#2980b9",
                annotation_text=f"K optim={best_k}",
                annotation_position="top right"
            )
            fig_ov.add_vrect(
                x0=1, x1=3, fillcolor="#e74c3c", opacity=0.05,
                annotation_text="Overfitting", annotation_position="top left"
            )
            fig_ov.add_vrect(
                x0=20, x1=30, fillcolor="#3498db", opacity=0.05,
                annotation_text="Underfitting", annotation_position="top right"
            )
            fig_ov.update_layout(
                xaxis_title="K (numar vecini)",
                yaxis_title="Acuratete (%)",
                xaxis=dict(tickvals=k_values),
                height=360,
                margin=dict(t=20, b=40, l=50, r=20),
            )
            st.plotly_chart(fig_ov, use_container_width=True)
            st.caption(
                f"K=1: acuratete 100% pe train (memoreaza totul!), scazuta pe test = overfitting. "
                f"K={best_k}: cel mai bun echilibru train/test. "
                f"K=30: ambele acuratete scad = underfitting."
            )

    st.divider()
    st.markdown("### Ce am invatat — Ziua 4")

    col1, col2 = st.columns(2)
    concepte = [
        ("Confusion Matrix",         "Tabel NN cu clasificari corecte pe diagonala si erori in rest"),
        ("Precision",                "TP/(TP+FP) — din cate prezise pozitive, cate chiar sunt pozitive"),
        ("Recall",                   "TP/(TP+FN) — din toate pozitivele reale, cate am detectat"),
        ("F1-score",                 "Media armonica Precision-Recall — util la clase dezechilibrate"),
        ("ROC Curve",                "Grafic TPR vs FPR pentru toate pragurile posibile"),
        ("AUC",                      "Aria sub curba ROC: 1.0=perfect, 0.5=aleator"),
        ("Cross-Validation",         "K evaluari independente — estimare robusta a performantei reale"),
        ("StratifiedKFold",          "CV care pastreaza proportia claselor in fiecare fold"),
        ("Overfitting",              "Model prea complex: acuratete mare pe train, mica pe test"),
        ("Underfitting",             "Model prea simplu: acuratete mica pe amandoua"),
        ("Learning Curve",           "Grafic acuratete vs dimensiune dataset — diagnostica over/underfitting"),
        ("K optim (KNN)",            "K mic = overfitting, K mare = underfitting; CV gaseste K-ul corect"),
    ]
    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#fff5f5; border-left:3px solid #e74c3c;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#e74c3c; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import label_binarize

# 1. Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=clase)

# 2. Raport complet per clasa
print(classification_report(y_test, y_pred))

# 3. Cross-Validation (k=5)
skf    = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoruri = cross_val_score(model, X_scaled, y, cv=skf, scoring="accuracy")
print(f"CV: {scoruri.mean():.3f} +/- {scoruri.std():.3f}")

# 4. ROC multiclasa (One-vs-Rest)
y_bin  = label_binarize(y_test, classes=clase)
y_prob = model.predict_proba(X_test)   # necesita probability=True la SVC
for i, cls in enumerate(clase):
    fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob[:, i])
    print(f"{cls}: AUC = {auc(fpr, tpr):.3f}")

# 5. Detectie overfitting
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc  = accuracy_score(y_test,  model.predict(X_test))
gap       = train_acc - test_acc
if gap > 0.10:
    print(f"ATENTIE: gap {gap:.2f} — posibil overfitting")
""", language="python")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Ghid rapid: ce metrica alegi?")
        st.markdown("""
        | Situatie | Metrica recomandata |
        |----------|-------------------|
        | Clase echilibrate | Acuratete sau F1 macro |
        | Clase dezechilibrate | F1 weighted sau AUC |
        | Vrei putine false alarme | Precision |
        | Vrei sa prinzi tot | Recall |
        | Compara mai multe modele | AUC-ROC |
        | Validare robusta | Cross-Validation |
        """)
    with col_b:
        st.markdown("#### Ziua 5 — ce urmeaza")
        st.markdown("""
        **Pipeline scikit-learn** — incapsuleaza preprocesare + model
        intr-un singur obiect reproductibil.

        - `Pipeline([scaler, model])` — un singur `fit()` si `predict()`
        - `GridSearchCV` — gaseste automat cei mai buni hiperparametri
        - Export model (`joblib`) — salveaza modelul antrenat pe disc
        - Incarcare model salvat — reutilizeaza fara reanrenare
        """)

    st.success(
        "**Ziua 4 finalizata!** Confusion Matrix, ROC, Cross-Validation si "
        "diagnosticarea Overfitting/Underfitting. "
        "Continua cu **Ziua 5 — Pipeline scikit-learn**."
    )
