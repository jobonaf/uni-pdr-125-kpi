# Changelog

Tutte le modifiche rilevanti a questo progetto sono documentate in questo file.

Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e il progetto adotta il [Versionamento Semantico](https://semver.org/lang/it/).

## [Non rilasciato]

### Aggiunto (calcolatori nel frontend, issue #15)

- Calcolatore nella pagina Compilazione per i KPI quantitativi che ne hanno uno nel catalogo (oc1, oc3, oc5, r1, ge4, ge5): inserisce gli input, calcola con `calcolaKpi`, imposta valutazione e valore percentuale
- Gli input dei calcolatori vengono salvati nel browser e nell'export (`calc_data`, come in Streamlit); all'import vengono filtrati (calcolatori noti, solo valori numerici) e coperti da test

### Aggiunto (frontend statico, prima versione, issue #24)

- `frontend/index.html` e `static/js/app.js`: pagine Organizzazione (fascia con card), Compilazione KPI per area, Dashboard (score globale, soglia, barre per area, stampa) e Salva/carica; dati nel `localStorage`
- `static/js/stato.js`: export compatibile con il JSON versione 2.0 di Streamlit e **validazione dell'import** (fascia, id e valori dei KPI)
- Bootstrap Italia 2.18.3 incluso in `frontend/static/vendor/` (CSS, icone, font), senza dipendere da CDN
- Non ancora presenti: calcolatori dei KPI quantitativi, report dedicato, storico e confronto

### Aggiunto (documentazione della logica e note sui KPI equivalenti, issue #21 e #14)

- `docs/logica-calcolo.md`: input/output di ogni funzione critica, perimetro della logica "pura", stato della validazione, tre diagrammi di flusso (Mermaid), esempio numerico e tabella di equivalenza Python ↔ JavaScript
- `src/logic/catalogo.py` (`trova_kpi`, `formatta_fasce`, `nota_equivalente`) e campo `equivalente` sui KPI oc1–oc4: l'interfaccia mostra accanto al badge una nota sulle fasce di applicabilità e sull'indicatore equivalente
- Test: purezza di `src/data` e `src/logic` (niente UI, rete, database, file system), copertura della documentazione (ogni funzione pubblica Python e ogni export JavaScript deve essere documentata), nota visibile nell'interfaccia, coppie di KPI ricavate dai dati

### Aggiunto (logica di scoring in JavaScript, issue #22)

- `frontend/static/js/scoring.js` e `calcolatori.js`: porting dei moduli Python `scoring.py` e `calcolatori.py` (funzioni pure che ricevono il catalogo JSON, nessun accesso al DOM)
- Test JavaScript con il runner integrato di Node (`cd frontend && node --test`), eseguiti contro fixture condivise con il Python: `tests/fixtures/calcolatori_golden.json` e `tests/fixtures/scoring_golden.json` (124 scenari su 4 fasce, generati da `scripts/export_golden_scoring.py`)
- `tests/test_scoring_golden.py`: il Python rispetta le stesse fixture

### Modificato (calcolatori)

- `calcola_kpi()` restituisce `None` anche in caso di divisione per zero (prima sollevava `ZeroDivisionError`), come la versione JavaScript

### Aggiunto (esportazione catalogo, issue #23)

- `scripts/export_catalog.py` genera `frontend/static/data/kpi-catalog.json` (aree, KPI, cluster, KPI da rendicontare, calcolatori, parametri di scoring); con `--check` verifica che il file sia aggiornato
- `src/data/export_catalog.py`: costruzione del dizionario JSON, senza dipendenze da Streamlit
- Test `tests/test_export_catalog.py`: falliscono se `kpi_catalog.py` cambia senza rigenerare il JSON

### Modificato

- Parametri di scoring centralizzati in `kpi_catalog.py` (`SOGLIA_CERTIFICAZIONE`, `FATTORE_PARZIALE`, `VALUTAZIONI`, `FASCE_CON_KPI_DA_RENDICONTARE`): la soglia del 60% era scritta a mano in quattro file della UI

- Calcolatori KPI (`CALCOLATORI_KPI`) resi **dichiarativi**: formule e soglie sono dati (serializzabili in JSON) invece di funzioni lambda; l'interpretazione è nel nuovo modulo puro `src/logic/calcolatori.py` (prerequisito per #22 e #23)
- `src/logic/scoring.py` non importa più Streamlit; rimossa la doppia definizione di `init_calculator_state` e la funzione `update_kpi_from_calculator`, ora sostituite da `calcola_kpi()` e dalla callback `applica_calcolatore` in `src/ui/compilazione.py` (issue #21)
- Commento inline sulle coppie KPI mutuamente esclusive oc1/oc2 e oc3/oc4 (issue #14)

### Corretto

- Il pulsante "Calcola e imposta valutazione" sollevava `StreamlitAPIException` (modifica di un widget già istanziato): ora usa una callback `on_click`
- README: comando di avvio su Windows puntava a `src/app.py` anziché a `streamlit_app.py`

### Aggiunto

- Test di equivalenza dei calcolatori con fixture generate dalle funzioni originali (`tests/fixtures/calcolatori_golden.json`), test di serializzabilità JSON, di separazione dei livelli e di integrazione UI (`AppTest`)
- `.gitignore`

### Rimosso

- `issues/epic-migrazione-bootstrap-italia-github-pages.md`: bozza generica con riferimenti a issue inesistenti; l'epic di riferimento è la #20 su GitHub

### In corso
- Migrazione dell'interfaccia da Streamlit a Bootstrap Italia (Design System .italia)
- Calcolatore inline per i KPI quantitativi
- Precompilazione dei benchmark ATECO da Appendice B della norma

---

## [0.2.0] - 2026-04-18

### Aggiunto
- Sezione `⚠️ Limiti e avvertenze` nel README con riferimento agli organismi
  di certificazione accreditati Accredia (issue #5)
- Struttura del repository reorganizzata: cartelle `src/`, `docs/`, `tests/`
  in conformità alle Linee Guida AGID su acquisizione e riuso (issue #13)

### Modificato
- Logica dei KPI "necessari": rinominato `KPI_OBBLIGATORI_PER_FASCIA` in
  `KPI_DA_RENDICONTARE_PER_FASCIA`; il termine "necessario" nella norma
  indica obbligo di rendicontazione, non di esito positivo (issue #2)
- `is_kpi_obbligatorio()` rinominata `is_kpi_da_rendicontare()`: per fascia
  3-4 restituisce ora `False` — nessun KPI individuale è bloccante per la
  certificazione, che dipende solo dallo score globale ≥ 60% (issue #1)
- `calcola_obbligatori_mancanti()` rinominata `calcola_kpi_non_compilati()`:
  segnala i KPI non ancora compilati (N/V) per fascia 1-2, non quelli con
  risposta negativa (issue #2, #3)
- Il messaggio "bloccanti per la certificazione" sostituito con un avviso
  informativo che spiega la logica dello score globale (issue #4)
- Aggiunti commenti normativi inline al dizionario `KPI_DA_RENDICONTARE_PER_FASCIA`
  con riferimento ai Prospetti 3-8 della norma (issue #3)
- Valore iniziale dei KPI impostato a `"N/V"` (invece di `None`) per coerenza
  con le opzioni del selectbox e corretto funzionamento del calcolo score
- Gestione dello stato Streamlit (`st.session_state`) per i widget di
  compilazione KPI riscritta per eliminare il disallineamento tra key dei
  widget e `kpi_values`

### Corretto
- Bug: il calcolo dello score assegnava punti errati a causa del conflitto
  tra il parametro `index=` del selectbox e la key in `st.session_state`
- Bug: `is_kpi_obbligatorio()` con `fascia >= 3: return True` causava la
  segnalazione di tutti i KPI di fascia 3-4 come "bloccanti" anche con
  score ≥ 60% (issue #1)

---

## [0.1.0] - 2026-03-27

### Aggiunto
- Prima versione funzionante dell'applicazione Streamlit
- Compilazione guidata dei KPI per le 6 aree UNI/PdR 125:2022
- Supporto alle 4 fasce dimensionali (micro, piccola, media, grande)
- Calcolo dello score globale ponderato con soglia di certificazione al 60%
- Dashboard con radar chart e bar chart per area (Plotly)
- Confronto storico tra annualità
- Export/import dati in JSON
- Report stampabile in PDF via browser
- `publiccode.yml` per il catalogo Developers Italia
- Licenza EUPL-1.2

[Non rilasciato]: https://github.com/jobonaf/uni-pdr-125-kpi/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jobonaf/uni-pdr-125-kpi/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jobonaf/uni-pdr-125-kpi/releases/tag/v0.1.0