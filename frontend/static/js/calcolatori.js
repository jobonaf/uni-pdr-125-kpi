// frontend/static/js/calcolatori.js
// Porting JavaScript di src/logic/calcolatori.py (logica pura, nessun accesso al DOM).
// La configurazione dichiarativa dei calcolatori sta in kpi-catalog.json ("calcolatori").
// Il comportamento è verificato contro tests/fixtures/calcolatori_golden.json.

export function calcolaValore(config, inputs) {
  const f = config.formula;
  switch (f.tipo) {
    case "differenza":
      return inputs[f.a] - inputs[f.b];
    case "percentuale":
      return (inputs[f.parte] / inputs[f.totale]) * 100;
    case "gap_percentuale": {
      const rif = inputs[f.riferimento];
      if (rif <= 0) return 0;
      return ((rif - inputs[f.confronto]) / rif) * 100;
    }
    default:
      throw new Error(`Tipo di formula sconosciuto: ${f.tipo}`);
  }
}

export function valuta(config, valore) {
  const v = config.valutazione;
  if (v.confronto === "maggiore_uguale") {
    if (valore >= v.soglia_si) return "Sì";
    return valore >= v.soglia_parziale ? "Parziale" : "No";
  }
  if (v.confronto === "minore") {
    if (valore < v.soglia_si) return "Sì";
    return valore < v.soglia_parziale ? "Parziale" : "No";
  }
  throw new Error(`Tipo di confronto sconosciuto: ${v.confronto}`);
}

function mancante(x) {
  return x === undefined || x === null || x === "" || Number.isNaN(x);
}

/**
 * Esegue il calcolatore di un KPI.
 * Restituisce { valore, valutazione }, oppure null se il KPI non ha un calcolatore,
 * se manca almeno un input o se il calcolo non è definito (es. divisione per zero).
 */
export function calcolaKpi(catalogo, kpiId, inputs) {
  const config = catalogo.calcolatori[kpiId];
  if (!config) return null;
  if (config.inputs.some((i) => mancante(inputs[i.name]))) return null;
  const valore = calcolaValore(config, inputs);
  if (!Number.isFinite(valore)) return null;
  return { valore, valutazione: valuta(config, valore) };
}
