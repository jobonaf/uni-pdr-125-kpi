# Frontend statico (Bootstrap Italia)

Versione senza server dello strumento: tutta la logica gira nel browser e i dati restano nel `localStorage`.

```
python -m http.server -d frontend 8000   # poi aprire http://localhost:8000
cd frontend && node --test               # test della logica JavaScript
```

- `index.html` + `static/js/app.js`: interfaccia (Organizzazione, Compilazione, Dashboard, Confronto, Report, Salva/carica)
- `static/js/scoring.js`, `calcolatori.js`, `stato.js`, `confronto.js`: logica pura, testata contro il Python
- `static/data/kpi-catalog.json`: generato da `python scripts/export_catalog.py`
- `static/vendor/bootstrap-italia/`: Bootstrap Italia 2.18.3 incluso nel repository (solo CSS, icone, font Titillium Web) per funzionare anche dietro proxy o offline

Il file JSON scaricato è compatibile con quello dell'app Streamlit (versione 2.0). A differenza di Streamlit,
l'import viene validato: fascia 1–4, id dei KPI noti e valori ammessi; i KPI sconosciuti vengono ignorati con un avviso.

Calcolatori: disponibili per i 6 KPI quantitativi che li definiscono nel catalogo (oc1, oc3, oc5, r1, ge4, ge5).

Report e confronto tra anni sono disponibili; lo storico è una funzione in più del frontend (Streamlit non lo salva nel file).

Non ancora presenti: grafici interattivi e i calcolatori mancanti nel catalogo.
