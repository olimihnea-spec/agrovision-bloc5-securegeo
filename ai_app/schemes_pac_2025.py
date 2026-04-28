"""
Valorile de referinta PAC 2025 — Romania (PSN 2023-2027)
Fisier central: modifica DOAR AICI cand se schimba legislatia.

Surse:
- Regulamentul UE 2021/2115 (PAC Strategic Plans)
- Regulamentul UE 2021/2116 (finantare si monitorizare)
- Ordinele MADR privind schemele de sprijin 2025
- HG privind aprobarea PSN Romania 2023-2027

Ultima actualizare: 21 aprilie 2026
"""

# ══════════════════════════════════════════════════════════════════════════════
# PLATI DIRECTE (PD)
# ══════════════════════════════════════════════════════════════════════════════

BISS_EUR_HA = 130.0
"""Plata de baza (BISS — Basic Income Support for Sustainability)
Toate parcelele agricole eligibile. Valoare medie nationala 2025."""

REDISTRIBUTIV_EUR_HA = 50.0
REDISTRIBUTIV_MAX_HA = 30.0
"""Plata redistributiva: +50 EUR/ha pentru primele 30 ha."""

ECO1_EUR_HA = 45.0
"""Eco-schema 1 — Rotatie culturi si diversificare:
Conditii: min 3 culturi, max 75% cereale, min 10% leguminoase."""

ECO2_EUR_HA = 35.0
"""Eco-schema 2 — Practici agro-ecologice:
Conditii: fasii tampon min 3m, fara tratamente pe fasii, acoperire sol iarna."""

ECO3_EUR_HA = 60.0
"""Eco-schema 3 — Pajisti permanente si biodiversitate."""

TINERI_FERMIERI_EUR_HA = 25.0
TINERI_FERMIERI_MAX_HA = 90.0
TINERI_FERMIERI_MAX_ANI = 5
"""Plata suplimentara tineri fermieri: +25 EUR/ha, max 90 ha, max 5 ani
de la prima cerere PAC."""

# ══════════════════════════════════════════════════════════════════════════════
# PLATI CUPLATE — CULTURI (VCS — Voluntary Coupled Support)
# ══════════════════════════════════════════════════════════════════════════════

CULTURI_CUPLATE = {
    "Grau":                55.0,
    "Orz":                 50.0,
    "Porumb":              50.0,
    "Floarea-soarelui":    80.0,
    "Rapita":              65.0,
    "Soia":               120.0,
    "Sfecla de zahar":    180.0,
    "Orez":               200.0,
    "Mazare/Fasole":       90.0,
    "Lucerna":             40.0,
    "Hamei":              350.0,
    "Legume camp":         95.0,
    "Cartofi":             85.0,
    "Tutun":              350.0,
    "Vita de vie":        220.0,
    "Pomi fructiferi":    180.0,
}
"""EUR/ha per cultura. Valori estimate PAC 2025."""

# ══════════════════════════════════════════════════════════════════════════════
# PLATI CUPLATE — ANIMALE
# ══════════════════════════════════════════════════════════════════════════════

ANIMALE_CUPLATE = {
    "Vaci de lapte":       100.0,
    "Vaci suciase (SVCP)": 130.0,
    "Bivoli":              150.0,
    "Oi (UVM)":             20.0,
    "Capre":                18.0,
    "Scroafe":              40.0,
    "Viermi de matase":     50.0,
}
"""EUR/cap animal. Conditie: inscris in RNE (Registrul National al Exploatatiilor)."""

BUNASTARE_ANIMALE = {
    "Porcine":              80.0,
    "Pasari broiler":       55.0,
    "Pasari outoare":       50.0,
    "Bovine":               70.0,
}
"""EUR/cap — schema bunastare animale (conditii specifice adapost, spatiu etc.)."""

# ══════════════════════════════════════════════════════════════════════════════
# DEZVOLTARE RURALA (PSN 2023-2027 — Masuri relevante)
# ══════════════════════════════════════════════════════════════════════════════

DR_MASURI = {
    "Zone defavorizate montane (ZUM)":       100.0,
    "Zone defavorizate altele (ZUD)":         50.0,
    "Agromediu — pajisti traditionale":      130.0,
    "Agromediu — culturi verzi":              90.0,
    "Agricultura ecologica — conversie":     250.0,
    "Agricultura ecologica — mentinere":     180.0,
    "Ferme mici (sub 10 ha)":                500.0,  # plata forfetara anuala
    "Tineri fermieri DR":                   15000.0, # sprijin instalare (forfet)
}
"""EUR/ha/an sau EUR forfetar per angajament. Durata angajament: 5 ani."""

# ══════════════════════════════════════════════════════════════════════════════
# PRAGURI DE NECONFORMITATE
# ══════════════════════════════════════════════════════════════════════════════

PRAG_SUPRAFATA_AVERTISMENT_PCT = 3.0
"""Diferenta suprafata declarata vs masurata > 3% → avertisment inspector."""

PRAG_SUPRAFATA_PENALIZARE_PCT  = 5.0
"""Diferenta > 5% → reducere proportionala subventie parcela afectata."""

PRAG_SUPRAFATA_EXCLUDERE_PCT   = 20.0
"""Diferenta > 20% → excludere parcela + penalizare 1 an urmator."""

PRAG_SUPRAFATA_FRAUDA_PCT      = 50.0
"""Diferenta > 50% → sesizare control special + excludere 3 ani."""

NDVI_VEGETATIE_NORMALA         = 0.35
"""NDVI >= 0.35 → vegetatie activa (cultura prezenta)."""

NDVI_CULTURA_ABSENTA           = 0.20
"""NDVI < 0.20 → posibil teren necultivat sau cultura distrusa."""

# ══════════════════════════════════════════════════════════════════════════════
# LIMITE SI PLAFOANE
# ══════════════════════════════════════════════════════════════════════════════

SUPRAFATA_MINIMA_ELIGIBILA_HA  = 0.3
"""Suprafata minima per parcela pentru a fi eligibila la plati."""

SUPRAFATA_MINIMA_CERERE_HA     = 1.0
"""Suprafata totala minima pentru a depune cerere PAC."""

PLAFON_NATIONAL_REDUCERE_PCT   = 100.0
"""Reducere 100% daca discrepantele sunt intentionate (frauda constatata)."""

CAPPING_PLATI_DIRECTE_EUR      = 100000.0
"""Plafon maxim plati directe per fermier/an (capping EU). Deasupra: reducere."""

DEGRESSIVITATE_PRAG_EUR        = 60000.0
"""Peste 60.000 EUR/an plati directe: reducere progresiva (degressivitate)."""

DEGRESSIVITATE_REDUCERE_PCT    = 25.0
"""Procent reducere aplicat sumei care depaseste pragul."""

# ══════════════════════════════════════════════════════════════════════════════
# CULORI UI (pentru vizualizare Streamlit)
# ══════════════════════════════════════════════════════════════════════════════

CULORI_SCHEME = {
    "BISS":               "#1a5276",
    "Redistributiv":      "#117a65",
    "Eco-schema 1":       "#27ae60",
    "Eco-schema 2":       "#2ecc71",
    "Eco-schema 3":       "#1abc9c",
    "Tineri fermieri":    "#8e44ad",
    "Cuplate culturi":    "#d35400",
    "Cuplate animale":    "#c0392b",
    "Bunastare animale":  "#e74c3c",
    "DR":                 "#6c3483",
}

CULORI_NECONFORMITATE = {
    "ok":         "#27ae60",
    "avertisment":"#e67e22",
    "penalizare": "#e74c3c",
    "frauda":     "#922b21",
}

# ══════════════════════════════════════════════════════════════════════════════
# METADATA
# ══════════════════════════════════════════════════════════════════════════════

VERSIUNE = "2025.1"
DATA_ACTUALIZARE = "21.04.2026"
SURSA_LEGALA = [
    "Regulamentul UE 2021/2115 — PAC Strategic Plans",
    "Regulamentul UE 2021/2116 — finantare si monitorizare PAC",
    "PSN Romania 2023-2027 (aprobat CE, 2022)",
    "Ordinele MADR 2025 privind schemele de sprijin",
]
