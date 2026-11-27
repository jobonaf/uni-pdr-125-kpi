// frontend/static/js/confronto.js — confronto tra annualità (logica pura).
import { calcolaScoreGlobale, kpiApplicabile } from "./scoring.js";

const RANGO = { No: 0, Parziale: 1, "Sì": 2 };

/** Variazione tra due valutazioni: "su", "giu", "uguale" o "nd" (se una delle due è N/V o sconosciuta). */
export function variazioneKpi(da, a) {
  if (!(da in RANGO) || !(a in RANGO)) return "nd";
  return RANGO[a] > RANGO[da] ? "su" : RANGO[a] < RANGO[da] ? "giu" : "uguale";
}

/**
 * Confronta due annualità { azienda, kpi_values } (ciascuna con la propria fascia).
 * I KPI confrontati sono quelli applicabili alla fascia dell'annualità corrente.
 */
export function confrontaAnni(catalogo, corrente, riferimento) {
  const c = calcolaScoreGlobale(catalogo, corrente.kpi_values, corrente.azienda.fascia);
  const r = calcolaScoreGlobale(catalogo, riferimento.kpi_values, riferimento.azienda.fascia);
  const aree = c.areeDetails.map((a, i) => ({
    id: a.id, nome: a.nome, totale: a.totale,
    corrente: a.score, riferimento: r.areeDetails[i].score, delta: a.score - r.areeDetails[i].score,
  })).filter((a) => a.totale > 0);
  const kpi = catalogo.aree.flatMap((area) => area.kpi
    .filter((k) => kpiApplicabile(k, corrente.azienda.fascia))
    .map((k) => {
      const rif = riferimento.kpi_values[k.id]?.valore ?? "N/V";
      const cor = corrente.kpi_values[k.id]?.valore ?? "N/V";
      return { area: area.nome, id: k.id, testo: k.testo, riferimento: rif, corrente: cor, variazione: variazioneKpi(rif, cor) };
    }));
  return { scoreCorrente: c.scoreGlobale, scoreRiferimento: r.scoreGlobale, delta: c.scoreGlobale - r.scoreGlobale, aree, kpi };
}
