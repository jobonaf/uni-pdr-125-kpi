# Frontend statico (Bootstrap Italia)

Versione senza server dello strumento: tutta la logica gira nel browser e i dati restano nel `localStorage`.

```
python -m http.server -d frontend 8000   # poi aprire http://localhost:8000
cd frontend && node --test               # test della logica JavaScript
```

- `index.html` + `static/js/app.js`: interfaccia (Organizzazione, Compilazione, Dashboard, Salva/carica)
- `static/js/scoring.js`, `calcolatori.js`, `stato.js`: logica pura, testata contro il Python
- `static/data/kpi-catalog.json`: generato da `python scripts/export_catalog.py`
- `static/vendor/bootstrap-italia/`: Bootstrap Italia 2.18.3 incluso nel repository (solo CSS, icone, font Titillium Web) per funzionare anche dietro proxy o offline

Il file JSON scaricato è compatibile con quello dell'app Streamlit (versione 2.0). A differenza di Streamlit,
l'import viene validato: fascia 1–4, id dei KPI noti e valori ammessi; i KPI sconosciuti vengono ignorati con un avviso.

Non ancora presenti: calcolatori dei KPI quantitativi, report stampabile dedicato, storico e confronto tra anni.
