# Architettura del sistema

## Panoramica

Lo strumento è strutturato in tre livelli separati:

- **Dati** (`src/data/`) — catalogo KPI, pesi delle aree, fasce dimensionali
- **Logica** (`src/logic/`) — calcolo score, validazione, gestione stato
- **Interfaccia** (`src/ui/`) — componenti di rendering (attualmente Streamlit)

Questa separazione consente di sostituire il layer UI (es. migrazione da
Streamlit a Bootstrap Italia) senza modificare la logica di calcolo.

## Struttura di `src/`

```
src/
├── __init__.py
├── data/
│   ├── __init__.py
│   └── kpi_catalog.py      # AREE, CLUSTER, KPI_DA_RENDICONTARE_PER_FASCIA
├── logic/
│   ├── __init__.py
│   └── scoring.py          # calcola_score_area(), calcola_score_globale(),
│                           # kpi_applicabile(), is_kpi_da_rendicontare(),
│                           # calcola_kpi_non_compilati()
└── ui/
    ├── __init__.py
    ├── anagrafica.py        # render_anagrafica()
    ├── compilazione.py      # render_compilazione()
    ├── confronto.py         # render_confronto()
    ├── dashboard.py         # render_dashboard()
    ├── import_export.py     # render_import_export()
    ├── report.py            # render_report()
    └── sidebar.py           # render_sidebar()
```

## Modello dati

### Struttura di un KPI

```python
{
    "id": "c1",                    # identificatore univoco
    "punti": 20,                   # punteggio massimo
    "tipo": "qualitativo",         # "qualitativo" | "quantitativo"
    "testo": "...",                # testo breve per UI
    "descrizione": "...",          # testo esteso normativo
    "fasceRichieste": [1, 2, 3, 4], # fasce dimensionali applicabili
    "soglia": "..."                # solo per KPI quantitativi
}
```

### Struttura di `kpi_values` (session state)

```python
{
    "c1": {
        "valore": "Sì",      # "Sì" | "No" | "Parziale" | "N/V"
        "note": "...",        # evidenze documentali
        "percentuale": "38.5" # solo per KPI quantitativi
    },
    ...
}
```

### Struttura del file JSON esportato

```json
{
    "version": "1.0",
    "compilazione_parziale": true,
    "kpi_compilati": 12,
    "kpi_totali": 19,
    "azienda": {
        "nome": "Esempio S.r.l.",
        "settore": "J",
        "fascia": 2,
        "anno": 2025
    },
    "kpi_values": { ... },
    "esportato": "2025-04-20T10:30:00"
}
```

## Logica di calcolo dello score

Lo score di ogni area è calcolato come:

```
score_area = (punti_ottenuti / punti_massimi) * 100
```

dove `punti_ottenuti` vale:
- `punti` del KPI se valore = `"Sì"`
- `punti * 0.5` se valore = `"Parziale"`
- `0` se valore = `"No"` o `"N/V"`

Lo score globale è la somma pesata degli score delle aree:

```
score_globale = Σ (score_area / 100) * peso_area
```

I pesi delle aree sono definiti nella norma (UNI/PdR 125:2022, §5.1):

| Area | Peso |
|---|---|
| Cultura e Strategia | 15% |
| Governance | 15% |
| Processi HR | 10% |
| Opportunità di Crescita | 20% |
| Equità Remunerativa | 20% |
| Tutela Genitorialità | 20% |

La soglia per accedere alla certificazione è **score globale ≥ 60%**.

## KPI "necessari" per fascia

Per fascia 1 e 2, la norma identifica un sottoinsieme di KPI che devono essere
obbligatoriamente misurati e rendicontati (UNI/PdR 125:2022, Prospetti 3-8).
Il termine "necessario" indica l'obbligo di rendicontazione, non di esito
positivo: un KPI con risposta "No" abbassa lo score ma non blocca la
certificazione, che dipende esclusivamente dallo score globale ≥ 60%.

Per fascia 3 e 4 si applicano tutti gli indicatori, senza ulteriori vincoli
individuali oltre alla soglia globale.

## Riferimenti normativi

- UNI/PdR 125:2022, §5.1 (Generalità — sistema di punteggio)
- UNI/PdR 125:2022, §5.2–§5.7 (Prospetti 3-8 — KPI per area)
- UNI/PdR 125:2022, Appendice B (benchmark ATECO)
- Decreto Min. Pari Opportunità 29 aprile 2022 (GU n. 152/2022)