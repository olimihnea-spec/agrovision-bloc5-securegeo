# CalcPAC-APIA — Design Document
**Data:** 21 aprilie 2026  
**Autor:** Prof. Asoc. Dr. Oliviu Mihnea Gamulescu  
**Consilier Superior APIA CJ Gorj | UCB Târgu Jiu | Centrul Suport SU Prefectura Gorj**

---

## 1. Problema rezolvată

Procedurile operationale APIA depasesc 700 de pagini. Legislatia PAC se modifica de 2-3 ori pe an.
Un inspector trebuie sa calculeze manual subventiile aplicabile per fermier, sa verifice neconformitatile
si sa tina pasul cu fiecare act normativ nou.

**CalcPAC-APIA** automatizeaza acest proces:
- Calcul instant al tuturor schemelor de sprijin aplicabile unui fermier
- Semnalizare automata a potentialelor neconformitati
- Monitorizare legislatie si actualizare ghidata a valorilor

---

## 2. Utilizator tinta

**Inspector APIA** — introduce datele fermierului si primeste in secunde:
- Suma totala estimata per schema
- Lista neconformitatilor potentiale cu pragul depasit
- Recomandari de control suplimentar

---

## 3. Scheme acoperite (PAC 2023–2027 / PSN Romania)

### 3.1 Plati directe (PD)
| Schema | Valoare referinta | Conditii |
|---|---|---|
| BISS — Plata de baza | ~130 EUR/ha | Toate parcelele eligibile |
| Plata redistributiva | +50 EUR/ha | Primele 30 ha |
| Eco-schema 1 (rotatie) | +45 EUR/ha | Min. 3 culturi, max 75% cereale |
| Eco-schema 2 (agro-eco) | +35 EUR/ha | Fasii tampon, fara tratamente |
| Tineri fermieri | +25 EUR/ha | Max 90 ha, max 5 ani de la prima cerere |

### 3.2 Plati cuplate — culturi
| Cultura | Valoare referinta |
|---|---|
| Grau | ~55 EUR/ha |
| Porumb | ~50 EUR/ha |
| Floarea-soarelui | ~80 EUR/ha |
| Soia | ~120 EUR/ha |
| Sfecla de zahar | ~180 EUR/ha |
| Rapita | ~65 EUR/ha |
| Orez | ~200 EUR/ha |

### 3.3 Plati cuplate — animale
| Specie | Valoare referinta |
|---|---|
| Vaci de lapte | ~100 EUR/cap |
| Vaci sucisare (SVCP) | ~130 EUR/cap |
| Oi/capre | ~20 EUR/cap |
| Bivolitele | ~150 EUR/cap |

### 3.4 Dezvoltare Rurala (PSN 2023–2027)
| Masura | Valoare referinta |
|---|---|
| Zone defavorizate (ZUD) | 50–100 EUR/ha |
| Agromediu (pajisti) | ~130 EUR/ha |
| Agricultura ecologica — conversie | ~250 EUR/ha |
| Agricultura ecologica — mentinere | ~180 EUR/ha |
| Bunastare animale | 40–80 EUR/cap |

> **Nota:** Toate valorile sunt estimate PAC 2025 si se actualizeaza prin Modulul C.

---

## 4. Arhitectura tehnica

```
schemes_pac_2025.py          ← toate valorile EUR + praguri (un singur fisier)
        ↓
pages/XX_Calculator_PAC.py   ← interfata Streamlit
    ├── Tab 1: Formular fermier
    │       ├── Date generale (CNP, judet, varsta)
    │       ├── Parcele (LPIS, ha, cultura, eco-schema aplicata)
    │       └── Animale (specie, capete, angajamente DR)
    ├── Tab 2: Rezultate calcul
    │       ├── Tabel scheme + EUR per schema
    │       ├── Total estimat
    │       └── Flag-uri neconformitate
    ├── Tab 3: Analiza neconformitati
    │       ├── Suprafata masurata (integrat Z14 Contururi)
    │       ├── Cultura identificata (integrat Z10 Anomalii NDVI)
    │       └── Comparatie declarata vs. masurata
    └── Tab 4: Monitor legislatie
            ├── RSS Monitorul Oficial (cuvinte cheie APIA/PAC)
            ├── Legis.ro — versiuni consolidate
            └── NLP extragere valori noi + propunere actualizare
```

---

## 5. Modulul A — Calculator scheme

### Input formular inspector
```
Fermier:
  - Nume, CNP (optional)
  - Judet, varsta (pentru bonus tineri fermieri)
  - Este tanar fermier? (prima cerere PAC)

Parcele (list dinamica, max 50):
  - Cod LPIS
  - Suprafata declarata [ha]
  - Cultura principala
  - Aplica eco-schema 1 (rotatie)?
  - Aplica eco-schema 2 (agro-eco)?
  - Angajament DR activ? (agromediu / bio / ZUD)

Animale (optional):
  - Vaci de lapte: X capete
  - Vaci suciase: X capete
  - Oi/capre: X capete
  - Angajament bunastare animale?
```

### Logica calcul (pseudocod)
```python
def calculeaza_pac(fermier, parcele, animale):
    rezultate = {}

    # BISS per parcela
    for p in parcele:
        rezultate["BISS"] += p.ha * BISS_EUR_HA

    # Redistributiva: primele 30 ha
    ha_redistributiv = min(total_ha, 30)
    rezultate["Redistributiv"] = ha_redistributiv * REDIST_EUR_HA

    # Eco-scheme
    ha_eco1 = sum(p.ha for p in parcele if p.eco1)
    rezultate["Eco1"] = ha_eco1 * ECO1_EUR_HA

    # Plati cuplate culturi
    for p in parcele:
        if p.cultura in CULTURI_CUPLATE:
            rezultate[f"Cuplat_{p.cultura}"] += p.ha * CULTURI_CUPLATE[p.cultura]

    # Animale
    rezultate["Vaci_lapte"] = animale.vaci_lapte * VACA_LAPTE_EUR
    ...

    return rezultate
```

---

## 6. Modulul B — Neconformitati

### Reguli de verificare
| Regula | Prag avertisment | Prag penalizare | Sursa date |
|---|---|---|---|
| Suprafata declarata vs. masurata | >3% diferenta | >5% diferenta | Z14 Contururi |
| Cultura declarata vs. identificata | Nepotrivire | Nepotrivire confirmata | Z10 NDVI |
| Eco-schema: conditii nerespectate | - | Pierdere eco-plata | Inspector |
| Tanar fermier: depasit 5 ani | - | Pierdere bonus | Data prima cerere |
| Angajament DR: cultura gresita | - | Recuperare plata | Inspector |

### Output neconformitate
```
[ROSU]   Suprafata GJ-001-A: declarata 4.52 ha, masurata 4.31 ha
         Diferenta: 4.6% < 5% — sub prag penalizare
         Actiune: nota in dosar, monitorizare

[ROSU]   Eco-schema 1 — Parcela GJ-002-B: cultura repetata (grau 2 ani consecutiv)
         Conditie nerespectata — pierdere eco-plata parcela: 45 EUR/ha x 3.8 ha = 171 EUR

[GALBEN] Angajament DR agromediu — confirmare documentatie necesara
```

---

## 7. Modulul C — Monitor legislatie

### Surse monitorizate
1. **Monitorul Oficial al Romaniei** — RSS feed zilnic  
   - Filtru: titluri cu "APIA", "scheme de sprijin", "plati directe", "PAC", "MADR"
   - Actiune: download text + analiza NLP

2. **Legis.ro** — versiuni consolidate  
   - Monitorizare: Ord. MADR, HG Guvern, Regulamente UE transpuse
   - Actiune: comparare cu versiunea salvata anterior

### Pipeline NLP extragere valori
```
Text act normativ
    ↓
NLP: cauta pattern-uri "X EUR/ha", "X lei/cap", "prag de X%"
    ↓
Propunere actualizare: "BISS: 130 → 135 EUR/ha (art. 7, alin. 2)"
    ↓
Inspector confirma → schemes_pac_2025.py actualizat automat
    ↓
Log: "Actualizat 21.04.2026 conform HG 312/2026, art. 7"
```

---

## 8. Integrare cu modulele existente

| Modul existent | Cum se integreaza |
|---|---|
| Z14 — Detectie Contururi | Suprafata masurata din imagini → comparata cu declarata |
| Z10 — Detectie Anomalii | NDVI → cultura identificata → comparata cu cultura declarata |
| Z10b — SecureGeo | Coordonate GPS → verificare ca parcela e in judetul declarat |
| Z18 — NLP | Extragere date din textul cererii PAC + extragere valori din lege |

---

## 9. Fisiere de creat

```
ai_app/
├── pages/
│   └── 19_Calculator_PAC.py       ← pagina principala
├── schemes_pac_2025.py             ← toate valorile EUR + praguri
└── utils/
    └── monitor_legislatie.py       ← RSS + scraping + NLP extragere
```

---

## 10. Plan de implementare (etape)

1. `schemes_pac_2025.py` — constante PAC 2025 pentru toate schemele
2. Formular inspector (Tab 1) — input parcele + animale
3. Motor calcul (Tab 2) — toate schemele, EUR total
4. Neconformitati (Tab 3) — reguli + flag-uri + integrare Z14/Z10
5. Monitor legislatie (Tab 4) — RSS Monitorul Oficial + NLP
6. Legis.ro scraping (Tab 4) — versiuni consolidate

---

*Vrei mai multe materiale ca acestea? Alătură-te comunității AI Wizard: [ai-wizard.tech/comunitate](https://ai-wizard.tech/comunitate)*
