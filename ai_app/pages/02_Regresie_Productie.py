"""
ZIUA 2 — Regresie — Predictie Productie Agricola
Modul 1: Machine Learning cu scikit-learn
Autor: Prof. Asoc. Dr. Oliviu Mihnea Gamulescu | UCB Targu Jiu | APIA CJ Gorj
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import date

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
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
    page_title="Ziua 2 — Regresie Productie",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <div style='font-size:36px;'>📈</div>
    <div style='font-size:16px; font-weight:700; color:#2980b9;'>ZIUA 2</div>
    <div style='font-size:11px; color:#666;'>Regresie — Predictie Productie</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Modul 1 — Machine Learning")
st.sidebar.divider()
st.sidebar.markdown("**Progres:** 2 / 30 zile")
st.sidebar.progress(2/30)
st.sidebar.markdown(f"**Data:** {date.today().strftime('%d.%m.%Y')}")
st.sidebar.divider()
st.sidebar.markdown("""
**Concepte ziua 2:**
- Clasificare vs Regresie
- Linear Regression
- Random Forest Regressor
- MAE, RMSE, R²
- Feature Importance
- Overfitting si generalizare
""")

if not SK_OK:
    st.error("scikit-learn nu este instalat. Ruleaza: `pip install scikit-learn`")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div style='font-size:48px;'>📈</div>
    <div>
        <h1 style='margin:0; font-size:28px; color:#2980b9; font-weight:800;'>
            Ziua 2 — Predictie Productie Agricola
        </h1>
        <p style='margin:0; color:#546e7a; font-size:14px;'>
            Modul 1 — Machine Learning &nbsp;|&nbsp;
            Linear Regression si Random Forest pe date NDVI + meteo
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Teorie", "📊 Date & Explorare", "🤖 Antrenare Model", "📚 Ce am invatat"
])

# ══════════════════════════════════════════════════════════════════════════════
# GENERARE DATE SIMULATE
# ══════════════════════════════════════════════════════════════════════════════
np.random.seed(42)
N_PER_CLS = 80   # 80 parcele per cultura = 400 total

CULORI_CULTURA = {
    "Grau":              "#f39c12",
    "Floarea-soarelui":  "#e74c3c",
    "Porumb":            "#27ae60",
    "Lucerna":           "#16a085",
    "Fanete":            "#795548",
}

# Configuratie per cultura: profil NDVI + parametri productie
CULTURI_CFG = {
    "Grau": {
        "ndvi": {"mai": (0.65, 0.08), "iun": (0.55, 0.10), "iul": (0.25, 0.08), "aug": (0.15, 0.05)},
        "prod_base": 4200,  "prod_std": 600,  "ha": (1.5, 5.0),
        "coef_ndvi": 3500,  "ndvi_luna": "mai",   # NDVI mai important pentru grau
        "coef_prec": 6.0,   "coef_temp": 40.0,
    },
    "Floarea-soarelui": {
        "ndvi": {"mai": (0.30, 0.07), "iun": (0.55, 0.09), "iul": (0.75, 0.08), "aug": (0.50, 0.10)},
        "prod_base": 2500,  "prod_std": 400,  "ha": (2.0, 8.0),
        "coef_ndvi": 2200,  "ndvi_luna": "iul",
        "coef_prec": 4.5,   "coef_temp": 35.0,
    },
    "Porumb": {
        "ndvi": {"mai": (0.25, 0.06), "iun": (0.60, 0.09), "iul": (0.82, 0.07), "aug": (0.70, 0.09)},
        "prod_base": 7500,  "prod_std": 1200, "ha": (1.0, 6.0),
        "coef_ndvi": 5000,  "ndvi_luna": "iul",
        "coef_prec": 9.0,   "coef_temp": 60.0,
    },
    "Lucerna": {
        "ndvi": {"mai": (0.60, 0.08), "iun": (0.55, 0.09), "iul": (0.65, 0.08), "aug": (0.58, 0.09)},
        "prod_base": 9500,  "prod_std": 1400, "ha": (1.0, 4.0),
        "coef_ndvi": 6000,  "ndvi_luna": "iul",
        "coef_prec": 7.0,   "coef_temp": 50.0,
    },
    "Fanete": {
        "ndvi": {"mai": (0.48, 0.08), "iun": (0.52, 0.08), "iul": (0.48, 0.07), "aug": (0.42, 0.08)},
        "prod_base": 3000,  "prod_std": 500,  "ha": (0.5, 3.0),
        "coef_ndvi": 2800,  "ndvi_luna": "iun",
        "coef_prec": 8.0,   "coef_temp": 30.0,
    },
}

LUNA_KEY = {"mai": "NDVI_mai", "iun": "NDVI_iunie", "iul": "NDVI_iulie", "aug": "NDVI_august"}
PREC_MEDIE = 280.0   # mm precipitatii sezon (mai-aug), medie Gorj
TEMP_MEDIE = 20.0    # grade C temperatura medie

rows = []
for cultura, cfg in CULTURI_CFG.items():
    ndvi_cfg = cfg["ndvi"]
    for _ in range(N_PER_CLS):
        ndvi_mai = float(np.clip(np.random.normal(ndvi_cfg["mai"][0], ndvi_cfg["mai"][1]), 0.0, 1.0))
        ndvi_iun = float(np.clip(np.random.normal(ndvi_cfg["iun"][0], ndvi_cfg["iun"][1]), 0.0, 1.0))
        ndvi_iul = float(np.clip(np.random.normal(ndvi_cfg["iul"][0], ndvi_cfg["iul"][1]), 0.0, 1.0))
        ndvi_aug = float(np.clip(np.random.normal(ndvi_cfg["aug"][0], ndvi_cfg["aug"][1]), 0.0, 1.0))
        prec     = float(np.clip(np.random.normal(PREC_MEDIE, 55.0), 80.0, 500.0))
        temp     = float(np.clip(np.random.normal(TEMP_MEDIE, 2.5),  12.0, 32.0))
        ha       = round(float(np.random.uniform(cfg["ha"][0], cfg["ha"][1])), 2)

        ndvi_cheie = {"mai": ndvi_mai, "iun": ndvi_iun, "iul": ndvi_iul, "aug": ndvi_aug}
        ndvi_val   = ndvi_cheie[cfg["ndvi_luna"]]

        productie = (
            cfg["prod_base"]
            + cfg["coef_ndvi"] * (ndvi_val - 0.5)
            + cfg["coef_prec"] * (prec - PREC_MEDIE)
            + cfg["coef_temp"] * (temp - TEMP_MEDIE)
            + float(np.random.normal(0.0, cfg["prod_std"]))
        )
        productie = max(300.0, round(productie, 0))

        rows.append({
            "cultura":          cultura,
            "NDVI_mai":         round(ndvi_mai, 3),
            "NDVI_iunie":       round(ndvi_iun, 3),
            "NDVI_iulie":       round(ndvi_iul, 3),
            "NDVI_august":      round(ndvi_aug, 3),
            "precipitatii_mm":  round(prec, 1),
            "temperatura_C":    round(temp, 1),
            "suprafata_ha":     ha,
            "productie_kg_ha":  int(productie),
        })

df = pd.DataFrame(rows)

FEATURES_NDVI  = ["NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august"]
FEATURES_METEO = ["precipitatii_mm", "temperatura_C"]
FEATURES_ALL   = FEATURES_NDVI + FEATURES_METEO
TARGET         = "productie_kg_ha"

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEORIE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Clasificare vs Regresie — care e diferenta?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background:#fff3e0; border-radius:10px; padding:16px;
             border-top:4px solid #f39c12;'>
            <div style='font-weight:700; color:#f39c12; font-size:15px;'>
                Clasificare (Ziua 1)
            </div>
            <div style='font-size:13px; color:#555; margin-top:8px;'>
                Raspunde la intrebarea: <b>Care categorie?</b><br><br>
                Exemplu: <i>"Ce cultura are aceasta parcela?"</i><br>
                Raspuns posibil: Grau / Porumb / Lucerna / ...<br><br>
                Output: o <b>eticheta discreta</b> (clasa)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#e8f4fd; border-radius:10px; padding:16px;
             border-top:4px solid #2980b9;'>
            <div style='font-weight:700; color:#2980b9; font-size:15px;'>
                Regresie (Ziua 2)
            </div>
            <div style='font-size:13px; color:#555; margin-top:8px;'>
                Raspunde la intrebarea: <b>Cat de mult?</b><br><br>
                Exemplu: <i>"Cat produce aceasta parcela?"</i><br>
                Raspuns posibil: 6.240 kg/ha<br><br>
                Output: o <b>valoare numerica continua</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Algoritmii de azi")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background:#fafafa; border-radius:10px; padding:16px;
             border-top:4px solid #2980b9;'>
            <div style='font-weight:700; color:#2980b9; font-size:15px;'>
                Linear Regression
            </div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Idee:</b> gaseste o linie (sau hiperplan) care minimizeaza
                suma patratelor erorilor intre valorile prezise si cele reale.<br><br>
                <b>Formula:</b><br>
                <code>productie = a1*NDVI_iul + a2*prec + a3*temp + b</code><br><br>
                Modelul invata coeficientii a1, a2, a3 si interceptul b din date.<br><br>
                <b>Avantaje:</b> simplu, rapid, interpretabil (stii exact
                cu cat creste productia la +1mm ploaie)<br><br>
                <b>Dezavantaje:</b> presupune relatie liniara — nu poate
                surprinde interactiuni complexe
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#fafafa; border-radius:10px; padding:16px;
             border-top:4px solid #27ae60;'>
            <div style='font-weight:700; color:#27ae60; font-size:15px;'>
                Random Forest Regressor
            </div>
            <div style='font-size:12px; color:#555; margin-top:8px;'>
                <b>Idee:</b> construieste sute de arbori de decizie pe subseturi
                aleatorii din date si features, apoi face media predictiilor.<br><br>
                <b>Analogie:</b> intrebi 100 de experti (fiecare cu experienta
                diferita) si faci media estimarilor lor.<br><br>
                <b>Avantaje:</b> surprinde relatii neliniare, robust la outlieri,
                ofera Feature Importance (care variabila conteaza cel mai mult)<br><br>
                <b>Dezavantaje:</b> mai lent, mai greu de interpretat
                decat regresia liniara
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Metricile de evaluare pentru regresie")

    metrici = [
        ("MAE", "Mean Absolute Error",
         "Eroarea medie absoluta in unitatile targetului (kg/ha). "
         "MAE=300 inseamna ca modelul greseste in medie cu 300 kg/ha.",
         "#e74c3c"),
        ("RMSE", "Root Mean Square Error",
         "Radical din media patratelor erorilor. Penalizeaza mai mult erorile mari. "
         "RMSE > MAE intotdeauna — diferenta mare = sunt outlieri.",
         "#f39c12"),
        ("R²", "Coeficientul de determinare",
         "Cat % din variatia productiei este explicata de model. "
         "R²=0.85 = modelul explica 85% din variatie. R²=1.0 = perfect. R²=0 = inutil.",
         "#27ae60"),
    ]

    for simbol, nume, desc, culoare in metrici:
        st.markdown(f"""
        <div style='display:flex; gap:12px; align-items:flex-start; margin:8px 0;
             background:white; border-radius:10px; padding:12px;
             box-shadow:0 1px 4px rgba(0,0,0,0.07); border-left:4px solid {culoare};'>
            <div style='font-size:22px; font-weight:900; color:{culoare};
                 min-width:50px; text-align:center;'>{simbol}</div>
            <div>
                <div style='font-weight:700; color:#333; font-size:13px;'>{nume}</div>
                <div style='font-size:12px; color:#555; margin-top:4px;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATE & EXPLORARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Dataset — 400 parcele agricole Gorj (5 culturi x 80)")

    # KPI per cultura
    cols_kpi = st.columns(5)
    for col, (cultura, culoare) in zip(cols_kpi, CULORI_CULTURA.items()):
        subset = df[df["cultura"] == cultura]
        med    = int(subset[TARGET].mean())
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:10px;
                 text-align:center; border-top:3px solid {culoare};
                 box-shadow:0 1px 4px rgba(0,0,0,0.08);'>
                <div style='font-size:18px; font-weight:800; color:{culoare};'>{med}</div>
                <div style='font-size:10px; color:#777;'>kg/ha mediu</div>
                <div style='font-size:11px; font-weight:600; color:#333;'>{cultura}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    col_tabel, col_stat = st.columns([3, 2])
    with col_tabel:
        st.markdown("**Primele 10 randuri:**")
        st.dataframe(
            df[["cultura", "NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august",
                "precipitatii_mm", "temperatura_C", "productie_kg_ha"]]
            .head(10).round(3),
            use_container_width=True, hide_index=True
        )
    with col_stat:
        st.markdown("**Statistici productie (kg/ha):**")
        stats = df.groupby("cultura")[TARGET].agg(["mean","std","min","max"]).round(0).astype(int)
        stats.columns = ["Medie", "Std", "Min", "Max"]
        st.dataframe(stats, use_container_width=True)

    st.divider()

    if PLOTLY_OK:
        col_box, col_scatter = st.columns(2)

        with col_box:
            st.markdown("#### Distributia productiei per cultura")
            fig_box = go.Figure()
            for cultura, culoare in CULORI_CULTURA.items():
                subset = df[df["cultura"] == cultura]
                fig_box.add_trace(go.Box(
                    y=subset[TARGET],
                    name=cultura,
                    marker_color=culoare,
                    boxmean=True
                ))
            fig_box.update_layout(
                yaxis_title="Productie (kg/ha)",
                height=350,
                showlegend=False,
                margin=dict(t=20, b=30, l=50, r=20),
            )
            st.plotly_chart(fig_box, use_container_width=True)
            st.caption(
                "Lucerna are productia cea mai ridicata (masa verde totala, 3-4 cosiri/an). "
                "Porumbul are cea mai mare variabilitate. "
                "Fanetele au productia cea mai mica si mai stabila."
            )

        with col_scatter:
            st.markdown("#### NDVI iulie vs Productie")
            fig_sc = go.Figure()
            for cultura, culoare in CULORI_CULTURA.items():
                subset = df[df["cultura"] == cultura]
                fig_sc.add_trace(go.Scatter(
                    x=subset["NDVI_iulie"],
                    y=subset[TARGET],
                    mode="markers",
                    name=cultura,
                    marker=dict(color=culoare, size=5, opacity=0.6)
                ))
            fig_sc.update_layout(
                xaxis_title="NDVI Iulie",
                yaxis_title="Productie (kg/ha)",
                height=350,
                margin=dict(t=20, b=30, l=50, r=20),
            )
            st.plotly_chart(fig_sc, use_container_width=True)
            st.caption(
                "Se observa corelatie pozitiva intre NDVI iulie si productie — "
                "parcele cu vegetatie mai densa in iulie produc mai mult. "
                "Graul este o exceptie (matureaza mai devreme)."
            )

        st.markdown("#### Corelatii intre features si productie")
        corr = df[FEATURES_ALL + [TARGET]].corr()[[TARGET]].drop(TARGET).round(2)
        corr.columns = ["Corelatie cu productia"]

        if PLOTLY_OK:
            fig_corr = go.Figure(go.Bar(
                x=corr["Corelatie cu productia"],
                y=corr.index,
                orientation="h",
                marker_color=["#27ae60" if v > 0 else "#e74c3c"
                              for v in corr["Corelatie cu productia"]],
            ))
            fig_corr.update_layout(
                xaxis_title="Coeficient Pearson",
                height=250,
                margin=dict(t=10, b=30, l=120, r=20),
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            st.caption(
                "Corelatia Pearson masoara relatia liniara intre -1 si +1. "
                "Variabilele cu corelatie mai mare sunt mai utile pentru regresie."
            )
    else:
        st.info("Instaleaza plotly: `pip install plotly`")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANTRENARE MODEL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Antrenare si evaluare modele de regresie")

    col_params, col_rez = st.columns([1, 2])

    with col_params:
        st.markdown("#### Parametri antrenare")

        test_size = st.slider(
            "Proportie date de test (%)",
            min_value=10, max_value=40, value=20, step=5
        ) / 100

        model_ales = st.selectbox(
            "Algoritmul de regresie",
            ["Linear Regression", "Random Forest Regressor", "Ambii (comparatie)"]
        )

        if "Random Forest" in model_ales or "Ambii" in model_ales:
            n_trees = st.slider("Nr. arbori (Random Forest)", 50, 500, 100, step=50)
            max_depth = st.slider("Adancime maxima arbori", 2, 20, 8)
        else:
            n_trees, max_depth = 100, 8

        cultura_filtru = st.selectbox(
            "Antreneaza pe:",
            ["Toate culturile"] + list(CULORI_CULTURA.keys())
        )

        antreneaza = st.button("Antreneaza modelul", type="primary")

    with col_rez:
        if antreneaza:
            df_train_src = (
                df if cultura_filtru == "Toate culturile"
                else df[df["cultura"] == cultura_filtru]
            )

            X = df_train_src[FEATURES_ALL].values
            y = df_train_src[TARGET].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )

            scaler  = StandardScaler()
            X_train_sc = scaler.fit_transform(X_train)
            X_test_sc  = scaler.transform(X_test)

            modele = {}
            if model_ales in ("Linear Regression", "Ambii (comparatie)"):
                modele["Linear Regression"] = LinearRegression()
            if model_ales in ("Random Forest Regressor", "Ambii (comparatie)"):
                modele["Random Forest"] = RandomForestRegressor(
                    n_estimators=n_trees,
                    max_depth=max_depth,
                    random_state=42,
                    n_jobs=-1
                )

            rezultate = {}
            for nume, model in modele.items():
                # LR beneficiaza de scalare, RF nu are nevoie dar nu strica
                model.fit(X_train_sc, y_train)
                y_pred = model.predict(X_test_sc)
                mae    = mean_absolute_error(y_test, y_pred)
                rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
                r2     = r2_score(y_test, y_pred)
                rezultate[nume] = {
                    "model":  model,
                    "y_pred": y_pred,
                    "y_test": y_test,
                    "mae":    mae,
                    "rmse":   rmse,
                    "r2":     r2,
                }

            # ── Metrici ──────────────────────────────────────────────────────
            st.markdown("#### Rezultate")
            culori_model = {"Linear Regression": "#2980b9", "Random Forest": "#27ae60"}

            for nume, rez in rezultate.items():
                culoare_m = culori_model.get(nume, "#8e44ad")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"""
                    <div style='background:{culoare_m}18; border-top:3px solid {culoare_m};
                         border-radius:8px; padding:10px; text-align:center;'>
                        <div style='font-size:11px; color:#666; font-weight:600;'>{nume}</div>
                        <div style='font-size:11px; color:#999; margin-top:2px;'>MAE</div>
                        <div style='font-size:20px; font-weight:800; color:{culoare_m};'>
                            {rez["mae"]:.0f} kg/ha
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div style='background:{culoare_m}18; border-top:3px solid {culoare_m};
                         border-radius:8px; padding:10px; text-align:center;'>
                        <div style='font-size:11px; color:#666; font-weight:600;'>{nume}</div>
                        <div style='font-size:11px; color:#999; margin-top:2px;'>RMSE</div>
                        <div style='font-size:20px; font-weight:800; color:{culoare_m};'>
                            {rez["rmse"]:.0f} kg/ha
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c3:
                    r2_color = "#27ae60" if rez["r2"] > 0.7 else "#f39c12" if rez["r2"] > 0.4 else "#e74c3c"
                    st.markdown(f"""
                    <div style='background:{culoare_m}18; border-top:3px solid {culoare_m};
                         border-radius:8px; padding:10px; text-align:center;'>
                        <div style='font-size:11px; color:#666; font-weight:600;'>{nume}</div>
                        <div style='font-size:11px; color:#999; margin-top:2px;'>R²</div>
                        <div style='font-size:20px; font-weight:800; color:{r2_color};'>
                            {rez["r2"]:.3f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Grafic Actual vs Prezis ───────────────────────────────────────
            if PLOTLY_OK:
                st.markdown("#### Actual vs Prezis")
                fig_avp = go.Figure()

                for nume, rez in rezultate.items():
                    culoare_m = culori_model.get(nume, "#8e44ad")
                    fig_avp.add_trace(go.Scatter(
                        x=rez["y_test"],
                        y=rez["y_pred"],
                        mode="markers",
                        name=nume,
                        marker=dict(color=culoare_m, size=5, opacity=0.6)
                    ))

                val_min = int(min(df[TARGET]) * 0.9)
                val_max = int(max(df[TARGET]) * 1.05)
                fig_avp.add_trace(go.Scatter(
                    x=[val_min, val_max], y=[val_min, val_max],
                    mode="lines", name="Predictie perfecta",
                    line=dict(color="#999", dash="dash", width=1)
                ))
                fig_avp.update_layout(
                    xaxis_title="Productie reala (kg/ha)",
                    yaxis_title="Productie prezisa (kg/ha)",
                    height=320,
                    margin=dict(t=20, b=40, l=50, r=20),
                )
                st.plotly_chart(fig_avp, use_container_width=True)
                st.caption(
                    "Cu cat punctele sunt mai aproape de linia diagonala, "
                    "cu atat modelul prezice mai bine. "
                    "Devierea sistematica de la diagonala = bias."
                )

                # ── Feature Importance (RF) ───────────────────────────────────
                if "Random Forest" in rezultate:
                    st.markdown("#### Feature Importance — Random Forest")
                    rf_model = rezultate["Random Forest"]["model"]
                    importances = rf_model.feature_importances_
                    fi_df = pd.DataFrame({
                        "Feature":    FEATURES_ALL,
                        "Importanta": importances
                    }).sort_values("Importanta", ascending=True)

                    fig_fi = go.Figure(go.Bar(
                        x=fi_df["Importanta"],
                        y=fi_df["Feature"],
                        orientation="h",
                        marker_color="#27ae60",
                    ))
                    fig_fi.update_layout(
                        xaxis_title="Importanta relativa",
                        height=250,
                        margin=dict(t=10, b=30, l=120, r=20),
                    )
                    st.plotly_chart(fig_fi, use_container_width=True)
                    st.caption(
                        "Feature Importance arata cat de mult contribuie fiecare "
                        "variabila la predictia modelului Random Forest. "
                        "Suma importantelor = 1.0 (100%)."
                    )

                # ── Coeficienti LR ───────────────────────────────────────────
                if "Linear Regression" in rezultate:
                    st.markdown("#### Coeficienti — Linear Regression")
                    lr_model = rezultate["Linear Regression"]["model"]
                    coef_df = pd.DataFrame({
                        "Feature":    FEATURES_ALL,
                        "Coeficient": lr_model.coef_.round(1)
                    }).sort_values("Coeficient", key=abs, ascending=True)

                    fig_coef = go.Figure(go.Bar(
                        x=coef_df["Coeficient"],
                        y=coef_df["Feature"],
                        orientation="h",
                        marker_color=["#27ae60" if v > 0 else "#e74c3c"
                                      for v in coef_df["Coeficient"]],
                    ))
                    fig_coef.update_layout(
                        xaxis_title="Coeficient (kg/ha per unitate de feature)",
                        height=250,
                        margin=dict(t=10, b=30, l=120, r=20),
                    )
                    st.plotly_chart(fig_coef, use_container_width=True)
                    st.caption(
                        "Coeficient pozitiv = cresterea acelei variabile creste productia. "
                        "Marimea absoluta = cat de mult influenteaza (dupa scalare)."
                    )

            # ── Predictie parcela noua ────────────────────────────────────────
            st.divider()
            st.markdown("#### Prezice productia pentru o parcela noua")
            st.caption("Introdu valorile NDVI si datele meteo:")

            c1, c2, c3, c4 = st.columns(4)
            with c1: p_ndvi_mai = st.number_input("NDVI Mai",    0.0, 1.0, 0.62, 0.01, key="p_mai")
            with c2: p_ndvi_iun = st.number_input("NDVI Iunie",  0.0, 1.0, 0.57, 0.01, key="p_iun")
            with c3: p_ndvi_iul = st.number_input("NDVI Iulie",  0.0, 1.0, 0.65, 0.01, key="p_iul")
            with c4: p_ndvi_aug = st.number_input("NDVI August", 0.0, 1.0, 0.60, 0.01, key="p_aug")

            c5, c6 = st.columns(2)
            with c5: p_prec = st.number_input("Precipitatii sezon (mm)", 80.0, 500.0, 290.0, 10.0)
            with c6: p_temp = st.number_input("Temperatura medie (°C)",  12.0, 32.0,  20.0,  0.5)

            x_nou_raw = np.array([[p_ndvi_mai, p_ndvi_iun, p_ndvi_iul, p_ndvi_aug,
                                   p_prec, p_temp]])
            x_nou_sc  = scaler.transform(x_nou_raw)

            pred_cols = st.columns(len(rezultate))
            for (nume, rez), col_pred in zip(rezultate.items(), pred_cols):
                pred_val = int(rez["model"].predict(x_nou_sc)[0])
                culoare_m = culori_model.get(nume, "#8e44ad")
                with col_pred:
                    st.markdown(f"""
                    <div style='background:{culoare_m}18; border:2px solid {culoare_m};
                         border-radius:10px; padding:14px; text-align:center;'>
                        <div style='font-size:12px; color:#555;'>{nume}</div>
                        <div style='font-size:26px; font-weight:800; color:{culoare_m};'>
                            {pred_val:,} kg/ha
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        else:
            st.info("Apasa **Antreneaza modelul** pentru a vedea rezultatele.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CE AM INVATAT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ce am invatat — Ziua 2")

    col1, col2 = st.columns(2)

    concepte = [
        ("Regresie vs Clasificare",   "Regresia prezice o valoare numerica; clasificarea prezice o clasa"),
        ("Linear Regression",         "Gaseste coeficientii unei ecuatii liniare care minimizeaza erorile"),
        ("Random Forest Regressor",   "Ansamblu de arbori de decizie — media predictiilor lor individuale"),
        ("MAE",                       "Eroarea medie absoluta — cat greseste modelul in medie (kg/ha)"),
        ("RMSE",                      "Penalizeaza mai mult erorile mari decat MAE"),
        ("R²",                        "0.0 = model inutil, 1.0 = model perfect. >0.7 = bun"),
        ("Feature Importance",        "Cat contribuie fiecare variabila la predictia Random Forest"),
        ("Coeficienti LR",            "Interpretabili direct: +100 kg/ha per mm precipitatii extra"),
        ("train_test_split()",        "Separa datele: modelul nu 'vede' datele de test la antrenare"),
        ("StandardScaler()",          "Esential pentru LR — aduce featurile la aceeasi scara"),
        ("fit() pe X_train",          "NICIODATA fit pe X_test — altfel introduci data leakage"),
        ("n_jobs=-1",                 "Random Forest foloseste toate nucleele CPU in paralel"),
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
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

# 1. Pregatire date
X = df[["NDVI_mai", "NDVI_iunie", "NDVI_iulie", "NDVI_august",
        "precipitatii_mm", "temperatura_C"]].values
y = df["productie_kg_ha"].values

# 2. Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Scalare (fit NUMAI pe train!)
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# 4. Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
print(f"LR — MAE: {mean_absolute_error(y_test, y_pred_lr):.0f} kg/ha")
print(f"LR — R2:  {r2_score(y_test, y_pred_lr):.3f}")

# 5. Random Forest
rf = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print(f"RF — MAE: {mean_absolute_error(y_test, y_pred_rf):.0f} kg/ha")
print(f"RF — R2:  {r2_score(y_test, y_pred_rf):.3f}")

# 6. Feature Importance (RF)
for feat, imp in zip(["NDVI_mai","NDVI_iun","NDVI_iul","NDVI_aug","prec","temp"],
                     rf.feature_importances_):
    print(f"  {feat}: {imp:.3f}")

# 7. Predictie parcela noua
x_nou = scaler.transform([[0.62, 0.57, 0.65, 0.60, 290, 20]])
print(f"Productie prezisa (RF): {rf.predict(x_nou)[0]:.0f} kg/ha")
""", language="python")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Legatura cu munca ta la APIA")
        st.markdown("""
        La APIA, inspectorii verifica daca productia declarata de fermieri
        este realista fata de suprafata si cultura declarata.

        Un model de regresie antrenat pe date istorice NDVI + meteo ar putea:
        - Estima productia **asteptata** per parcela din judetul Gorj
        - Semnala declaratii **suspecte** (productie declarata mult peste estimat)
        - Automatiza o parte din **analiza de risc** inainte de controlul pe teren

        Aceasta este o aplicatie concreta pentru un articol ISI in domeniul
        **AI aplicat in controlul subventiilor agricole**.
        """)
    with col_b:
        st.markdown("#### Ziua 3 — ce urmeaza")
        st.markdown("""
        **Clustering** — grupare nesupervizata a parcelelor agricole.

        In loc sa prezici o clasa sau o valoare, descoperi **grupuri naturale**
        in date fara sa stii raspunsul corect dinainte.

        Algoritmi: **K-Means** si **DBSCAN**

        Aplicatie: gruparea parcelelor APIA din Gorj dupa profil vegetal NDVI
        — utila pentru harta de risc si planificarea controalelor pe teren.
        """)

    st.success(
        "**Ziua 2 finalizata!** Linear Regression si Random Forest Regressor "
        "pentru predictia productiei agricole din NDVI + date meteo. "
        "Continua cu **Ziua 3 — Clustering** pentru a descoperi grupuri naturale in parcele."
    )
