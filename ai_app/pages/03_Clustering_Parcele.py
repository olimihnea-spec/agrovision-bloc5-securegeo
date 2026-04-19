"""
ZIUA 3 — Clustering — Grupare Nesupervizata a Parcelelor Agricole
Modul 1: Machine Learning cu scikit-learn
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import date

try:
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score, adjusted_rand_score
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
    page_title="Ziua 3 — Clustering Parcele",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>🗂️</div>
    <div style='font-size:16px; font-weight:700; color:#8e44ad;'>ZIUA 3</div>
    <div style='font-size:11px; color:#666;'>Clustering — Grupare Nesupervizata</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 1 — Machine Learning")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 3 / 30 zile")
st.sidebar.progress(3/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 3:**
- Invatare nesupervizata
- K-Means — centroizi
- Metoda Cotului (Elbow)
- Silhouette Score
- DBSCAN — clustering bazat pe densitate
- PCA — reducere dimensionalitate
- Adjusted Rand Index
""")

if not SK_OK:
    st.error("scikit-learn nu este instalat. Ruleaza: `pip install scikit-learn`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>🗂️</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#8e44ad; font-weight:800;'>
            Ziua 3 — Clustering Parcele Agricole
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 1 — Machine Learning &nbsp;|&nbsp;
            K-Means si DBSCAN pe date NDVI — fara etichete
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "📊 Date & Vizualizare", "🤖 Clustering", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# GENERARE DATE (identic cu zilele anterioare)
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
    "Grau":             {"mai": (0.65,0.08), "iun": (0.55,0.10), "iul": (0.25,0.08), "aug": (0.15,0.05), "ha": (1.5,5.0)},
    "Floarea-soarelui": {"mai": (0.30,0.07), "iun": (0.55,0.09), "iul": (0.75,0.08), "aug": (0.50,0.10), "ha": (2.0,8.0)},
    "Porumb":           {"mai": (0.25,0.06), "iun": (0.60,0.09), "iul": (0.82,0.07), "aug": (0.70,0.09), "ha": (1.0,6.0)},
    "Lucerna":          {"mai": (0.60,0.08), "iun": (0.55,0.09), "iul": (0.65,0.08), "aug": (0.58,0.09), "ha": (1.0,4.0)},
    "Fanete":           {"mai": (0.48,0.08), "iun": (0.52,0.08), "iul": (0.48,0.07), "aug": (0.42,0.08), "ha": (0.5,3.0)},
}

rows = []
for cultura, cfg in CULTURI_CFG.items():
    for _ in range(N_PER_CLS):
        rows.append({
            "cultura":     cultura,
            "NDVI_mai":    round(float(np.clip(np.random.normal(cfg["mai"][0], cfg["mai"][1]), 0, 1)), 3),
            "NDVI_iunie":  round(float(np.clip(np.random.normal(cfg["iun"][0], cfg["iun"][1]), 0, 1)), 3),
            "NDVI_iulie":  round(float(np.clip(np.random.normal(cfg["iul"][0], cfg["iul"][1]), 0, 1)), 3),
            "NDVI_august": round(float(np.clip(np.random.normal(cfg["aug"][0], cfg["aug"][1]), 0, 1)), 3),
            "suprafata_ha": round(float(np.random.uniform(cfg["ha"][0], cfg["ha"][1])), 2),
        })

df = pd.DataFrame(rows)
FEATURES = ["NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august"]

scaler_global = StandardScaler()
X_scaled = scaler_global.fit_transform(df[FEATURES].to_numpy())

# PCA 2D pentru vizualizare
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
df["PCA1"] = X_pca[:, 0].round(3)
df["PCA2"] = X_pca[:, 1].round(3)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Ce este invatarea nesupervizata?")

    col1, col2, col3 = st.columns(3)
    for col, (tip, desc, culoare, ex) in zip(
        [col1, col2, col3],
        [
            ("Supervizat",    "Inveți din exemple cu etichete cunoscute",   "#27ae60",
             "Zilele 1-2: stiam cultura si productia"),
            ("Nesupervizat",  "Descoperi structuri in date fara etichete",  "#8e44ad",
             "Ziua 3: nu stim cultura, descoperim grupuri naturale"),
            ("Semi-supervizat","Putine etichete + multe date neetichetate", "#2980b9",
             "Caz frecvent in practica — putine date verificate"),
        ]
    ):
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:10px; padding:14px;
                 border-top:4px solid {culoare}; box-shadow:0 1px 4px rgba(0,0,0,0.07);
                 height:160px;'>
                <div style='font-weight:700; color:{culoare}; font-size:14px;'>{tip}</div>
                <div style='font-size:12px; color:#555; margin-top:6px;'>{desc}</div>
                <div style='font-size:11px; color:#888; margin-top:8px;
                     border-top:1px solid #eee; padding-top:6px;'>
                    <b>Exemplu:</b> {ex}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Algoritmii de azi")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background:#fafafa; border-radius:10px; padding:16px;
             border-top:4px solid #8e44ad;'>
            <div style='font-weight:700; color:#8e44ad; font-size:15px;'>K-Means</div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Idee:</b> imparte datele in K grupuri astfel incat fiecare
                punct sa fie cat mai aproape de centrul grupului sau.<br><br>
                <b>Algoritm:</b><br>
                1. Alege K centroizi aleatori<br>
                2. Atribuie fiecare punct celui mai apropiat centroid<br>
                3. Recalculeaza centroizii (media grupului)<br>
                4. Repeta pana la convergenta<br><br>
                <b>Parametru cheie:</b> K = numarul de clustere (trebuie ales!)<br><br>
                <b>Limitare:</b> presupune clustere sferice, sensibil la outlieri,
                trebuie sa stii K dinainte
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#fafafa; border-radius:10px; padding:16px;
             border-top:4px solid #2980b9;'>
            <div style='font-weight:700; color:#2980b9; font-size:15px;'>DBSCAN</div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Idee:</b> un cluster = zona densa de puncte.
                Punctele izolate = zgomot (noise), nu apartin niciunui cluster.<br><br>
                <b>Parametri:</b><br>
                — <b>eps</b>: raza de vecinatate (cat de apropiati trebuie sa fie vecinii)<br>
                — <b>min_samples</b>: cate puncte minime formeaza un cluster<br><br>
                <b>Avantaje:</b> nu trebuie sa stii K dinainte,
                detecteaza clustere de orice forma,
                identifica automat outlieri (puncte anomale)<br><br>
                <b>Aplicatie APIA:</b> parcele cu profil NDVI atipic
                sunt marcate ca noise = candidati pentru control
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Cum alegem K la K-Means? — Metoda Cotului (Elbow)")
    st.markdown("""
    Rulam K-Means pentru K = 2, 3, 4, ..., 10 si masuram **inertia**
    (suma distantelor patratice fata de centroid).
    Inertia scade pe masura ce K creste — cautam **cotul** graficului,
    punctul unde reducerea inertiei incetineste brusc.

    Completam cu **Silhouette Score**: masura cat de bine separat este fiecare punct
    de propriul cluster fata de clusterul vecin. Valori: **-1** (rau) → **+1** (perfect).
    """)

    st.markdown("### Cum masuram calitatea clusteringului?")
    metrici = [
        ("Inertia (WCSS)",    "Suma distantelor patratice intre fiecare punct si centroidul sau. Mai mica = mai buna. Folosita in metoda cotului.", "#8e44ad"),
        ("Silhouette Score",  "Cat de bine e separat fiecare punct: aproape de propriul cluster si departe de vecinii. [-1, +1], >0.5 = bun.", "#27ae60"),
        ("Adjusted Rand Index", "Compara clusterele gasite cu etichetele reale (daca le stim). 0 = aleator, 1 = perfect.", "#2980b9"),
    ]
    for simbol, desc, culoare in metrici:
        st.markdown(f"""
        <div style='border-left:4px solid {culoare}; background:white; border-radius:0 8px 8px 0;
             padding:10px 14px; margin:6px 0; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
            <span style='font-weight:700; color:{culoare};'>{simbol}</span>
            <span style='font-size:12px; color:#555; margin-left:8px;'>{desc}</span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATE & VIZUALIZARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Datele reale — culturi cunoscute (supervizat)")
    st.info(
        "In clustering **nu folosim** eticheta `cultura` pentru antrenare. "
        "O afisam doar pentru a vedea daca algoritmul o descopera singur."
    )

    # KPI per cultura
    cols_kpi = st.columns(5)
    for col, (cultura, culoare) in zip(cols_kpi, CULORI_CULTURA.items()):
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:10px;
                 text-align:center; border-top:3px solid {culoare};
                 box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
                <div style='font-size:20px; font-weight:800; color:{culoare};'>{N_PER_CLS}</div>
                <div style='font-size:11px; font-weight:600; color:#333;'>{cultura}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    if PLOTLY_OK:
        col_pca, col_ndvi = st.columns(2)

        with col_pca:
            st.markdown("#### PCA — date reale (culturi cunoscute)")
            st.caption(
                f"PCA reduce 4 dimensiuni NDVI la 2 axe vizualizabile. "
                f"Varianta explicata: PC1={pca.explained_variance_ratio_[0]*100:.1f}%, "
                f"PC2={pca.explained_variance_ratio_[1]*100:.1f}%"
            )
            fig_real = go.Figure()
            for cultura, culoare in CULORI_CULTURA.items():
                subset = df[df["cultura"] == cultura]
                fig_real.add_trace(go.Scatter(
                    x=subset["PCA1"], y=subset["PCA2"],
                    mode="markers", name=cultura,
                    marker=dict(color=culoare, size=5, opacity=0.7)
                ))
            fig_real.update_layout(
                xaxis_title="PC1", yaxis_title="PC2",
                height=350, margin=dict(t=10, b=30, l=40, r=20),
            )
            st.plotly_chart(fig_real, use_container_width=True)

        with col_ndvi:
            st.markdown("#### Profil NDVI mediu per cultura")
            luni = ["Mai", "Iunie", "Iulie", "August"]
            fig_ndvi = go.Figure()
            for cultura, culoare in CULORI_CULTURA.items():
                subset = df[df["cultura"] == cultura]
                medii = [subset[f].mean() for f in FEATURES]
                fig_ndvi.add_trace(go.Scatter(
                    x=luni, y=medii, name=cultura,
                    mode="lines+markers",
                    line=dict(color=culoare, width=2),
                    marker=dict(size=8)
                ))
            fig_ndvi.update_layout(
                yaxis_title="NDVI mediu", yaxis=dict(range=[0, 1]),
                height=350, margin=dict(t=10, b=30, l=40, r=20),
            )
            st.plotly_chart(fig_ndvi, use_container_width=True)

        st.markdown("#### Scatter NDVI Mai vs NDVI Iulie — cele mai discriminante luni")
        fig_sc = go.Figure()
        for cultura, culoare in CULORI_CULTURA.items():
            subset = df[df["cultura"] == cultura]
            fig_sc.add_trace(go.Scatter(
                x=subset["NDVI_mai"], y=subset["NDVI_iulie"],
                mode="markers", name=cultura,
                marker=dict(color=culoare, size=5, opacity=0.6)
            ))
        fig_sc.update_layout(
            xaxis_title="NDVI Mai", yaxis_title="NDVI Iulie",
            height=320, margin=dict(t=10, b=30, l=50, r=20),
        )
        st.plotly_chart(fig_sc, use_container_width=True)
        st.caption(
            "Graul are NDVI mai ridicat in mai si foarte scazut in iulie. "
            "Porumbul are maximul in iulie. "
            "Aceste doua luni separa bine culturile — algoritmul ar trebui sa le descopere."
        )
    else:
        st.info("Instaleaza plotly: `pip install plotly`")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CLUSTERING
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Clustering — fara etichete")

    subtab_km, subtab_db = st.tabs(["K-Means", "DBSCAN"])

    # ── K-MEANS ──────────────────────────────────────────────────────────────
    with subtab_km:
        col_p, col_r = st.columns([1, 2])

        with col_p:
            st.markdown("#### Parametri K-Means")

            arata_elbow = st.checkbox("Calculeaza curba Elbow + Silhouette", value=True)
            k_ales = st.slider("K — numarul de clustere", 2, 10, 5)
            km_init = st.selectbox("Metoda initializare", ["k-means++", "random"],
                                   help="k-means++ alege centroizi distantati initial — converge mai repede")
            ruleaza_km = st.button("Ruleaza K-Means", type="primary")

        with col_r:
            if arata_elbow:
                st.markdown("#### Curba Elbow + Silhouette")
                K_range   = range(2, 11)
                inertii   = []
                siluete   = []
                for k in K_range:
                    km_tmp = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
                    lbls   = km_tmp.fit_predict(X_scaled)
                    inertii.append(km_tmp.inertia_)
                    siluete.append(silhouette_score(X_scaled, lbls))

                if PLOTLY_OK:
                    fig_elbow = go.Figure()
                    fig_elbow.add_trace(go.Scatter(
                        x=list(K_range), y=inertii,
                        mode="lines+markers", name="Inertia",
                        line=dict(color="#8e44ad", width=2),
                        marker=dict(size=8),
                        yaxis="y1"
                    ))
                    fig_elbow.add_trace(go.Scatter(
                        x=list(K_range), y=siluete,
                        mode="lines+markers", name="Silhouette",
                        line=dict(color="#27ae60", width=2, dash="dash"),
                        marker=dict(size=8),
                        yaxis="y2"
                    ))
                    fig_elbow.add_vline(
                        x=k_ales, line_dash="dot", line_color="#e74c3c",
                        annotation_text=f"K ales={k_ales}", annotation_position="top right"
                    )
                    fig_elbow.update_layout(
                        xaxis=dict(title="K (numar clustere)", tickvals=list(K_range)),
                        yaxis=dict(title="Inertia", color="#8e44ad"),
                        yaxis2=dict(title="Silhouette Score", overlaying="y",
                                    side="right", color="#27ae60", range=[0, 1]),
                        height=300,
                        margin=dict(t=20, b=30, l=60, r=60),
                        legend=dict(x=0.5, y=1.1, orientation="h"),
                    )
                    st.plotly_chart(fig_elbow, use_container_width=True)
                    best_k = list(K_range)[siluete.index(max(siluete))]
                    st.caption(
                        f"Silhouette maxim la K={best_k}. "
                        "Cotul inertiei sugereaza acelasi K. "
                        "Ai ales K={k_ales}.".replace("{k_ales}", str(k_ales))
                    )

            if ruleaza_km:
                km = KMeans(n_clusters=k_ales, init=km_init, n_init=10, random_state=42)
                df["cluster_km"] = km.fit_predict(X_scaled)

                sil = silhouette_score(X_scaled, df["cluster_km"])
                ari = adjusted_rand_score(
                    df["cultura"].map({c: i for i, c in enumerate(CULORI_CULTURA)}),
                    df["cluster_km"]
                )

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Clustere gasite", k_ales)
                with c2:
                    st.metric("Silhouette Score", f"{sil:.3f}")
                with c3:
                    st.metric("Adjusted Rand Index", f"{ari:.3f}",
                              help="Compara cu etichetele reale: 1.0 = perfect")

                if PLOTLY_OK:
                    CULORI_CLUSTER = [
                        "#8e44ad","#e74c3c","#27ae60","#2980b9","#f39c12",
                        "#16a085","#795548","#c0392b","#1abc9c","#d35400"
                    ]

                    col_km1, col_km2 = st.columns(2)

                    with col_km1:
                        st.markdown("#### Clustere gasite (PCA 2D)")
                        fig_km = go.Figure()
                        for cl in sorted(df["cluster_km"].unique()):
                            subset = df[df["cluster_km"] == cl]
                            fig_km.add_trace(go.Scatter(
                                x=subset["PCA1"], y=subset["PCA2"],
                                mode="markers",
                                name=f"Cluster {cl}",
                                marker=dict(color=CULORI_CLUSTER[cl % len(CULORI_CLUSTER)],
                                            size=5, opacity=0.7)
                            ))
                        # centroizi in spatiul PCA
                        centroids_pca = pca.transform(km.cluster_centers_)
                        fig_km.add_trace(go.Scatter(
                            x=centroids_pca[:, 0], y=centroids_pca[:, 1],
                            mode="markers", name="Centroizi",
                            marker=dict(symbol="x", size=14, color="black",
                                        line=dict(width=2))
                        ))
                        fig_km.update_layout(
                            xaxis_title="PC1", yaxis_title="PC2",
                            height=320, margin=dict(t=10, b=30, l=40, r=20),
                        )
                        st.plotly_chart(fig_km, use_container_width=True)

                    with col_km2:
                        st.markdown("#### Compozitia clusterelor (culturi reale)")
                        compozitie = (
                            df.groupby(["cluster_km", "cultura"])
                            .size().reset_index(name="n")
                        )
                        pivot = compozitie.pivot(
                            index="cluster_km", columns="cultura", values="n"
                        ).fillna(0).astype(int)

                        fig_stacked = go.Figure()
                        for cultura, culoare in CULORI_CULTURA.items():
                            if cultura in pivot.columns:
                                fig_stacked.add_trace(go.Bar(
                                    x=[f"C{i}" for i in pivot.index],
                                    y=pivot[cultura],
                                    name=cultura,
                                    marker_color=culoare,
                                ))
                        fig_stacked.update_layout(
                            barmode="stack",
                            xaxis_title="Cluster K-Means",
                            yaxis_title="Nr. parcele",
                            height=320,
                            margin=dict(t=10, b=30, l=40, r=20),
                        )
                        st.plotly_chart(fig_stacked, use_container_width=True)
                        st.caption(
                            "Un cluster pur (o singura culoare) = algoritmul a descoperit "
                            "cultura respectiva fara sa stie etichetele. "
                            "Amestecul indica culturi greu de separat."
                        )

                    # Centroizi NDVI
                    st.markdown("#### Profilul NDVI al centroizilor")
                    centroids_orig = scaler_global.inverse_transform(km.cluster_centers_)
                    luni = ["Mai", "Iunie", "Iulie", "August"]
                    fig_cent = go.Figure()
                    for i, centroid in enumerate(centroids_orig):
                        fig_cent.add_trace(go.Scatter(
                            x=luni, y=centroid,
                            mode="lines+markers",
                            name=f"Cluster {i}",
                            line=dict(color=CULORI_CLUSTER[i % len(CULORI_CLUSTER)], width=2),
                            marker=dict(size=8)
                        ))
                    fig_cent.update_layout(
                        yaxis_title="NDVI", yaxis=dict(range=[0, 1]),
                        height=300, margin=dict(t=10, b=30, l=40, r=20),
                    )
                    st.plotly_chart(fig_cent, use_container_width=True)
                    st.caption(
                        "Fiecare centroid = profilul NDVI 'tipic' al clusterului. "
                        "Compara cu graficul de la Tab 2 pentru a identifica ce cultura reprezinta."
                    )
            else:
                if not arata_elbow:
                    st.info("Apasa **Ruleaza K-Means** pentru a vedea rezultatele.")

    # ── DBSCAN ───────────────────────────────────────────────────────────────
    with subtab_db:
        col_p2, col_r2 = st.columns([1, 2])

        with col_p2:
            st.markdown("#### Parametri DBSCAN")
            st.markdown("""
            <div style='background:#e8f4fd; border-radius:8px; padding:10px; font-size:12px;'>
            <b>eps</b> = raza de vecinatate<br>
            Valori mici → mai multe clustere mici + mai mult noise<br>
            Valori mari → clustere mari, putine<br><br>
            <b>min_samples</b> = puncte minime per cluster<br>
            Valori mici → mai putine puncte noise<br>
            Valori mari → mai strict, mai mult noise
            </div>
            """, unsafe_allow_html=True)

            eps_val      = st.slider("eps", 0.1, 2.0, 0.5, step=0.05)
            min_samp_val = st.slider("min_samples", 2, 20, 5)
            ruleaza_db   = st.button("Ruleaza DBSCAN", type="primary")

        with col_r2:
            if ruleaza_db:
                db = DBSCAN(eps=eps_val, min_samples=min_samp_val)
                df["cluster_db"] = db.fit_predict(X_scaled)

                n_clustere = len(set(df["cluster_db"])) - (1 if -1 in df["cluster_db"].to_numpy() else 0)
                n_noise    = int((df["cluster_db"] == -1).sum())
                pct_noise  = n_noise / len(df) * 100

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Clustere gasite", n_clustere)
                with c2:
                    st.metric("Puncte noise", n_noise,
                              help="Parcele atipice — candidati pentru control APIA")
                with c3:
                    st.metric("% noise", f"{pct_noise:.1f}%")

                if n_clustere < 2:
                    st.warning(
                        f"Cu eps={eps_val} si min_samples={min_samp_val} s-a gasit "
                        f"un singur cluster sau niciun cluster. "
                        "Mareste eps sau micsoreaza min_samples."
                    )
                else:
                    try:
                        sil_db = silhouette_score(
                            X_scaled[df["cluster_db"] != -1],
                            df.loc[df["cluster_db"] != -1, "cluster_db"]
                        )
                        st.metric("Silhouette (fara noise)", f"{sil_db:.3f}")
                    except Exception:
                        pass

                if PLOTLY_OK and n_clustere >= 1:
                    CULORI_CLUSTER_DB = [
                        "#8e44ad","#e74c3c","#27ae60","#2980b9","#f39c12",
                        "#16a085","#795548","#c0392b","#1abc9c","#d35400"
                    ]

                    col_db1, col_db2 = st.columns(2)

                    with col_db1:
                        st.markdown("#### Clustere DBSCAN (PCA 2D)")
                        fig_db = go.Figure()

                        # Noise in gri
                        noise_pts = df[df["cluster_db"] == -1]
                        if len(noise_pts) > 0:
                            fig_db.add_trace(go.Scatter(
                                x=noise_pts["PCA1"], y=noise_pts["PCA2"],
                                mode="markers", name="Noise (anomalii)",
                                marker=dict(color="#aaa", size=4, opacity=0.5,
                                            symbol="x")
                            ))

                        for cl in sorted(set(df["cluster_db"].unique()) - {-1}):
                            subset = df[df["cluster_db"] == cl]
                            fig_db.add_trace(go.Scatter(
                                x=subset["PCA1"], y=subset["PCA2"],
                                mode="markers",
                                name=f"Cluster {cl}",
                                marker=dict(
                                    color=CULORI_CLUSTER_DB[cl % len(CULORI_CLUSTER_DB)],
                                    size=5, opacity=0.7
                                )
                            ))
                        fig_db.update_layout(
                            xaxis_title="PC1", yaxis_title="PC2",
                            height=320, margin=dict(t=10, b=30, l=40, r=20),
                        )
                        st.plotly_chart(fig_db, use_container_width=True)

                    with col_db2:
                        st.markdown("#### Parcele noise — profil atipic")
                        noise_df = df[df["cluster_db"] == -1]
                        if len(noise_df) > 0:
                            st.markdown(f"""
                            <div style='background:#fff3cd; border-left:4px solid #f39c12;
                                 border-radius:0 8px 8px 0; padding:10px 14px;'>
                                <b>{len(noise_df)} parcele</b> au profil NDVI atipic
                                (nu se incadreaza in niciun cluster dens).<br><br>
                                La APIA, acestea ar fi <b>candidati prioritari
                                pentru control pe teren</b> — pot reprezenta:
                                <ul style='margin:6px 0; font-size:12px;'>
                                    <li>Culturi declarate incorect</li>
                                    <li>Parcele partial distruse (inundatii, seceta)</li>
                                    <li>Culturi mixte sau neidentificate</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

                            st.dataframe(
                                noise_df[["cultura","NDVI_mai","NDVI_iunie",
                                          "NDVI_iulie","NDVI_august"]]
                                .head(10).round(3),
                                use_container_width=True, hide_index=True
                            )
                        else:
                            st.success(
                                "Niciun punct noise cu parametrii alesi. "
                                "Micsoreaza eps pentru a detecta anomalii."
                            )
            else:
                st.info("Apasa **Ruleaza DBSCAN** pentru a vedea rezultatele.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 3")

    col1, col2 = st.columns(2)
    concepte = [
        ("Invatare nesupervizata",  "Nu avem etichete — descoperim structuri ascunse in date"),
        ("K-Means",                 "K centroizi, fiecare punct → cel mai apropiat centroid"),
        ("DBSCAN",                  "Clustere = zone dense; puncte izolate = noise (anomalii)"),
        ("Metoda Cotului",          "Grafic Inertie vs K — cautam cotul unde curba se aplatizeaza"),
        ("Silhouette Score",        "[-1, +1]: cat de bine separat e fiecare punct de cluster-ul sau"),
        ("Adjusted Rand Index",     "Compara clustering-ul cu etichetele reale: 0=aleator, 1=perfect"),
        ("PCA",                     "Reducere dimensionalitate: 4 dimensiuni NDVI → 2 axe vizualizabile"),
        ("eps (DBSCAN)",            "Raza de vecinatate — controleaza marimea si numarul clusterelor"),
        ("min_samples (DBSCAN)",    "Puncte minime pentru a forma un cluster dens"),
        ("Noise points",            "Puncte care nu apartin niciunui cluster = potentiale anomalii"),
        ("fit_predict()",           "Antreneaza si atribuie clustere simultan — specific clusteringului"),
        ("StandardScaler",          "Obligatoriu inainte de K-Means si DBSCAN — distantele trebuie comparabile"),
    ]

    for i, (concept, explicatie) in enumerate(concepte):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style='background:#f5f0ff; border-left:3px solid #8e44ad;
                 border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;'>
                <div style='font-weight:700; color:#8e44ad; font-size:13px;'>{concept}</div>
                <div style='font-size:12px; color:#555;'>{explicatie}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Cod esential — copy-paste ready")
    st.code("""
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, adjusted_rand_score

# 1. Scalare obligatorie
scaler = StandardScaler()
X_sc   = scaler.fit_transform(X)   # X = matrice NDVI (fara etichete)

# 2. K-Means
km     = KMeans(n_clusters=5, init="k-means++", n_init=10, random_state=42)
labels = km.fit_predict(X_sc)
print(f"Silhouette: {silhouette_score(X_sc, labels):.3f}")
print(f"Inertia:    {km.inertia_:.1f}")

# 3. Metoda cotului
for k in range(2, 11):
    km_tmp = KMeans(n_clusters=k, n_init=10, random_state=42)
    km_tmp.fit(X_sc)
    print(f"K={k}  Inertia={km_tmp.inertia_:.0f}  "
          f"Sil={silhouette_score(X_sc, km_tmp.labels_):.3f}")

# 4. DBSCAN
db     = DBSCAN(eps=0.5, min_samples=5)
labels = db.fit_predict(X_sc)
n_cls  = len(set(labels)) - (1 if -1 in labels else 0)
n_noi  = (labels == -1).sum()
print(f"Clustere: {n_cls}, Noise: {n_noi}")

# 5. PCA pentru vizualizare 2D
pca    = PCA(n_components=2, random_state=42)
X_2d   = pca.fit_transform(X_sc)
print(f"Varianta explicata: {pca.explained_variance_ratio_.sum()*100:.1f}%")

# 6. Compara cu etichete reale (daca le stim)
ari = adjusted_rand_score(y_real, labels)
print(f"Adjusted Rand Index: {ari:.3f}")
""", language="python")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Aplicatie directa APIA — Harta de risc")
        st.markdown("""
        DBSCAN aplicat pe datele NDVI din LPIS ar putea genera automat
        o **lista de parcele prioritare pentru control**:

        - Parcelele **noise** (atipice) → control fizic obligatoriu
        - Clustere cu **profil NDVI inconsistent** cu cultura declarata → verificare
        - Aceasta reduce timpul de selectie a parcelelor de la zile la **minute**

        O aplicatie operationala ar necesita date NDVI reale din **Sentinel-2**
        (gratuit, rezolutie 10m, disponibil pe Copernicus Open Access Hub).
        """)
    with col_b:
        st.markdown("#### Ziua 4 — ce urmeaza")
        st.markdown("""
        **Evaluare modele** — cum stim daca un model ML este cu adevarat bun?

        - **Confusion Matrix** aprofundata
        - **ROC Curve** si **AUC**
        - **Cross-Validation** (k-fold)
        - Overfitting vs Underfitting
        - Cum alegem cel mai bun model pentru o problema reala
        """)

    st.success(
        "**Ziua 3 finalizata!** K-Means si DBSCAN pentru gruparea nesupervizata "
        "a parcelelor agricole dupa profil NDVI. "
        "Continua cu **Ziua 4 — Evaluare Modele**."
    )
