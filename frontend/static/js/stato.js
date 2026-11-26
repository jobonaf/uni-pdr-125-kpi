// frontend/static/js/stato.js
// Stato dell'applicazione e formato di import/export, compatibile con il JSON "versione 2.0"
// prodotto dall'app Streamlit. Logica pura (nessun accesso al DOM).
import { initKpiValues, kpiApplicabile } from "./scoring.js";

export function statoIniziale(catalogo, anno = new Date().getFullYear()) {
  return {
    azienda: { nome: "", settore: "", fascia: 3, anno },
    kpi_values: initKpiValues(catalogo),
    calc_data: {},
  };
}

export function creaExport(catalogo, stato, adesso = new Date()) {
  const fascia = stato.azienda.fascia;
  const totali = catalogo.aree.flatMap((a) => a.kpi).filter((k) => kpiApplicabile(k, fascia)).length;
  const compilati = Object.values(stato.kpi_values).filter((v) => v.valore && v.valore !== "N/V").length;
  return {
    version: "2.0",
    compilazione_parziale: compilati < totali,
    kpi_compilati: compilati,
    kpi_totali: totali,
    azienda: stato.azienda,
    kpi_values: stato.kpi_values,
    calc_data: stato.calc_data,
    esportato: adesso.toISOString(),
  };
}

/**
 * Valida e normalizza un file importato (o lo stato salvato nel browser).
 * Restituisce { ok, errori, avvisi, stato }: gli errori bloccano l'import, gli avvisi no
 * (KPI sconosciuti ignorati, KPI mancanti impostati a N/V).
 */
export function validaImport(catalogo, dati) {
  const errori = [];
  const avvisi = [];
  const oggetto = (x) => x !== null && typeof x === "object" && !Array.isArray(x);
  if (!oggetto(dati)) return { ok: false, errori: ["Il file non contiene un oggetto JSON."], avvisi, stato: null };
  if (!oggetto(dati.azienda)) errori.push("Manca la sezione «azienda».");
  if (!oggetto(dati.kpi_values)) errori.push("Manca la sezione «kpi_values».");
  if (errori.length) return { ok: false, errori, avvisi, stato: null };

  const fascia = dati.azienda.fascia;
  if (![1, 2, 3, 4].includes(fascia)) errori.push(`Fascia non valida: ${JSON.stringify(fascia)} (attese 1–4).`);

  const stato = statoIniziale(catalogo);
  stato.azienda = {
    nome: String(dati.azienda.nome ?? ""),
    settore: String(dati.azienda.settore ?? ""),
    fascia: [1, 2, 3, 4].includes(fascia) ? fascia : 3,
    anno: Number.isInteger(dati.azienda.anno) ? dati.azienda.anno : new Date().getFullYear(),
  };
  const ammessi = catalogo.scoring.valutazioni;
  for (const [id, v] of Object.entries(dati.kpi_values)) {
    if (!(id in stato.kpi_values)) {
      avvisi.push(`KPI sconosciuto ignorato: ${id}`);
    } else if (!oggetto(v) || !ammessi.includes(v.valore)) {
      errori.push(`Valore non valido per ${id}: ${JSON.stringify(oggetto(v) ? v.valore : v)}.`);
    } else {
      stato.kpi_values[id] = { valore: v.valore, note: String(v.note ?? ""), percentuale: String(v.percentuale ?? "") };
    }
  }
  if (oggetto(dati.calc_data)) stato.calc_data = dati.calc_data;
  return { ok: errori.length === 0, errori, avvisi, stato: errori.length ? null : stato };
}
