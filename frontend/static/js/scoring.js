// frontend/static/js/scoring.js
// Porting JavaScript di src/logic/scoring.py (logica pura, nessun accesso al DOM).
// Tutte le funzioni ricevono il catalogo (kpi-catalog.json) come primo argomento, così
// sono testabili con Node e riusabili nel browser. Il comportamento è verificato contro
// tests/fixtures/scoring_golden.json, generato dall'implementazione Python.
//
// kpiValues ha la stessa forma dell'app Streamlit: { [kpiId]: { valore, note, percentuale } }
// con valore in catalogo.scoring.valutazioni ("N/V", "No", "Parziale", "Sì").

export function kpiApplicabile(kpi, fascia) {
  return kpi.fasceRichieste.includes(fascia);
}

export function isKpiDaRendicontare(catalogo, kpiId, fascia) {
  if (!catalogo.scoring.fasceConKpiDaRendicontare.includes(fascia)) return false;
  const fasce = catalogo.kpiDaRendicontarePerFascia[kpiId];
  return Array.isArray(fasce) && fasce.includes(fascia);
}

export function calcolaScoreArea(catalogo, area, kpiValues, fascia) {
  const applicabili = area.kpi.filter((k) => kpiApplicabile(k, fascia));
  if (applicabili.length === 0) {
    return { score: 0, massimo: 0, ottenuti: 0, completati: 0, totale: 0 };
  }
  let ottenuti = 0;
  let massimo = 0;
  let completati = 0;
  for (const k of applicabili) {
    massimo += k.punti;
    const val = kpiValues[k.id]?.valore;
    if (val === "Sì") {
      ottenuti += k.punti;
      completati += 1;
    } else if (val === "Parziale") {
      ottenuti += k.punti * catalogo.scoring.fattoreParziale;
      completati += 1;
    } else if (val === "No") {
      completati += 1;
    }
  }
  const score = massimo > 0 ? (ottenuti / massimo) * 100 : 0;
  return { score, massimo, ottenuti, completati, totale: applicabili.length };
}

export function calcolaScoreGlobale(catalogo, kpiValues, fascia) {
  let scoreGlobale = 0;
  const areeDetails = [];
  for (const area of catalogo.aree) {
    const res = calcolaScoreArea(catalogo, area, kpiValues, fascia);
    const contributo = (res.score / 100) * area.peso;
    scoreGlobale += contributo;
    areeDetails.push({ ...area, ...res, contributo });
  }
  return { scoreGlobale, areeDetails };
}

export function calcolaKpiNonCompilati(catalogo, kpiValues, fascia) {
  const nonCompilati = [];
  for (const area of catalogo.aree) {
    for (const kpi of area.kpi) {
      if (!kpiApplicabile(kpi, fascia)) continue;
      if (!isKpiDaRendicontare(catalogo, kpi.id, fascia)) continue;
      const val = kpiValues[kpi.id]?.valore;
      if (val === undefined || val === null || val === "N/V") {
        nonCompilati.push({
          area: area.nome,
          icona: area.icona,
          colore: area.colore,
          kpi,
          valoreAttuale: val ?? null,
        });
      }
    }
  }
  return nonCompilati;
}

export function initKpiValues(catalogo) {
  const values = {};
  for (const area of catalogo.aree) {
    for (const kpi of area.kpi) {
      values[kpi.id] = { valore: "N/V", note: "", percentuale: "" };
    }
  }
  return values;
}

export function certificabile(catalogo, scoreGlobale) {
  return scoreGlobale >= catalogo.scoring.sogliaCertificazione;
}
