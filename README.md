# Strumento KPI UNI/PdR 125:2022

## Descrizione

Applicazione per la compilazione, il monitoraggio e la reportistica dei KPI previsti dalla **Prassi di Riferimento UNI/PdR 125:2022** sulla **parità di genere nelle organizzazioni** pubbliche e private.

Lo strumento è sviluppato in conformità alle Linee Guida AGID sull'acquisizione e il riuso di software per le PA (art. 69 D.Lgs. 82/2005 — Codice dell'Amministrazione Digitale).

## ⚠️ Limiti e avvertenze

Questo strumento è fornito a scopo di **autovalutazione** e supporto alla preparazione per la certificazione UNI/PdR 125:2022.

La certificazione ufficiale di parità di genere, che consente l'accesso agli incentivi previsti dalla legge (es. sgravi contributivi L. 162/2021), **può essere rilasciata esclusivamente da un Organismo di Certificazione accreditato da Accredia**, ai sensi del Regolamento CE 765/2008 e del Decreto Ministeriale 29 aprile 2022 (GU n. 152 del 01/07/2022).

Il punteggio calcolato da questa applicazione non sostituisce in alcun modo il giudizio di un Organismo di Certificazione. Per l'elenco degli organismi abilitati, consultare il sito ufficiale del Dipartimento per le Pari Opportunità:
<https://certificazione.pariopportunita.gov.it/public/organismi-di-certificazione>

## Funzionalità principali

- **Compilazione guidata dei KPI** per fascia dimensionale (1–4)
- **Verifica automatica** dei KPI da rendicontare ("necessari") per fascia
- **Calcolo dello score globale ponderato** (soglia certificazione: 60%)
- **Dashboard** con radar chart e bar chart per area
- **Confronto storico** tra annualità
- **Export/import dati** in JSON
- **Report stampabile / esportabile** in PDF via browser

## Riferimenti normativi

- **UNI/PdR 125:2022** (pubblicata il 16 marzo 2022, ICS 03.100.01)
- **D.Lgs. 11 aprile 2006 n.198** — Codice delle pari opportunità
- **L. 162/2021** — Parità salariale
- **Agenda ONU 2030** — Goal 5 (uguaglianza di genere)

## Tecnologie

> ⚙️ **Nota:** l'interfaccia è attualmente basata su **Streamlit**. È in corso la migrazione verso **Bootstrap Italia** (Design System .italia) per conformità alle Linee Guida di Design AGID.

- **Python** ≥ 3.9
- **Streamlit** ≥ 1.28 — framework per l'interfaccia web
- **Pandas** ≥ 2.0 — elaborazione dati
- **Plotly** ≥ 5.17 — grafici interattivi (radar chart, bar chart)

## Struttura del repository

```
uni-pdr-125-kpi/
├── src/                         # codice sorgente Python
│   ├── data/
│   │   └── kpi_catalog.py       # AREE, CLUSTER, KPI_DA_RENDICONTARE_PER_FASCIA
│   ├── logic/
│   │   └── scoring.py           # calcolo score, validazione KPI
│   └── ui/                      # componenti dell'interfaccia Streamlit
│       ├── anagrafica.py
│       ├── compilazione.py
│       ├── confronto.py
│       ├── dashboard.py
│       ├── import_export.py
│       ├── report.py
│       └── sidebar.py
├── docs/                        # documentazione tecnica e utente
├── tests/                       # test automatizzati
├── AUTHORS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── publiccode.yml
├── streamlit_app.py             # app Streamlit
└── requirements.txt
```

## Installazione

### Requisiti di sistema

- Python ≥ 3.9 (verificare con `python --version` o `python3 --version`)
- pip (incluso nelle installazioni Python standard)

### Procedura

**1. Clona il repository**
```bash
git clone https://github.com/jobonaf/uni-pdr-125-kpi.git
cd uni-pdr-125-kpi
```

**2. Crea un ambiente virtuale** (raccomandato)
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**3. Installa le dipendenze**
```bash
pip install -r requirements.txt
```

**4. Avvia l'applicazione**
```bash
streamlit run streamlit_app.py
```

L'app si aprirà automaticamente nel browser su `http://localhost:8501`.

> **Windows — se `streamlit` non viene trovato nel PATH:**
> ```bash
> python -m streamlit run src/app.py
> # oppure, se l'eseguibile è in .venv:
> .venv\Scripts\python.exe -m streamlit run streamlit_app.py
> ```

## Utilizzo

1. Nella scheda **Anagrafica**, inserire il nome dell'organizzazione, selezionare il settore ATECO e la fascia dimensionale (1–4 in base al numero di addetti)
2. Nella scheda **KPI**, compilare gli indicatori per ciascuna delle 6 aree tematiche, scegliendo tra: `Sì`, `No`, `Parziale`, `N/V` (non ancora valutato)
3. Nella scheda **Dashboard**, verificare lo score globale ponderato e il dettaglio per area; lo score deve essere ≥ 60% per accedere alla certificazione
4. Nella scheda **Confronto**, confrontare i risultati con annualità precedenti salvate
5. Nella scheda **Report**, generare e stampare il report in PDF tramite la funzione di stampa del browser (Ctrl+P / Cmd+P)
6. Nella scheda **Dati**, esportare i dati in JSON per conservarli o importarli in sessioni successive

## Accessibilità

Lo strumento è sviluppato con attenzione alle **Linee Guida AGID sull'accessibilità** (WCAG 2.1 livello AA).

La dichiarazione di accessibilità sarà pubblicata a seguito della migrazione dell'interfaccia al Design System .italia (Bootstrap Italia), attualmente in corso.

Per segnalare problemi di accessibilità: <https://github.com/jobonaf/uni-pdr-125-kpi/issues>

## Licenza

**European Union Public Licence v1.2 (EUPL-1.2)**
<https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12>

Questo software è rilasciato sotto licenza EUPL-1.2 e può essere liberamente utilizzato, studiato, modificato e ridistribuito a condizione che le opere derivate siano distribuite con la stessa licenza e che venga mantenuta l'attribuzione all'autore.

## Autori

**Giovanni Bonafè**
ORCID: [0000-0002-7815-8866](https://orcid.org/0000-0002-7815-8866)

## Contribuzioni

Le contribuzioni sono benvenute! Per maggiori dettagli, si prega di consultare [CONTRIBUTING.md](CONTRIBUTING.md).

## Supporto

Per segnalare bug, suggerimenti o domande:

- **GitHub Issues**: <https://github.com/jobonaf/uni-pdr-125-kpi/issues>

---

**Versione:** 0.2.0
**Ultimo aggiornamento:** 2026-04-20
**Status:** In sviluppo