# Changelog

Tutte le modifiche rilevanti a questo progetto sono documentate in questo file.

Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e il progetto adotta il [Versionamento Semantico](https://semver.org/lang/it/).

## [Non rilasciato]

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