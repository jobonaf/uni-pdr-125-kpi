// frontend/static/js/stato.js
// Stato dell'applicazione e formato di import/export, compatibile con il JSON "versione 2.0"
// prodotto dall'app Streamlit (la chiave opzionale "storico" è un'aggiunta del frontend, ignorata da Streamlit).
// Logica pura (nessun accesso al DOM).
import { initKpiValues, kpiApplicabile } from "./scoring.js";

const oggetto = (x) => x !== null && typeof x === "object" && !Array.isArray(x);

export function statoIniziale(catalogo, anno = new Date().getFullYear()) {
  return {
    azienda: { nome: "", settore: "", fascia: 3, anno },
    kpi_values: initKpiValues(catalogo),
    calc_data: {},
    storico: [],
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
    storico: stato.storico ?? [],
    esportato: adesso.toISOString(),
  };
}

// Valida e normalizza una coppia { azienda, kpi_values } (anno corrente o voce di storico).
function normalizza(catalogo, dati) {
  const errori = [];
  const avvisi = [];
  if (!oggetto(dati)) return { errori: ["Il file non contiene un oggetto JSON."], avvisi };
  if (!oggetto(dati.azienda)) errori.push("Manca la sezione «azienda».");
  if (!oggetto(dati.kpi_values)) errori.push("Manca la sezione «kpi_values».");
  if (errori.length) return { errori, avvisi };

  const fascia = dati.azienda.fascia;
  if (![1, 2, 3, 4].includes(fascia)) errori.push(`Fascia non valida: ${JSON.stringify(fascia)} (attese 1–4).`);
  const base = statoIniziale(catalogo);
  const azienda = {
    nome: String(dati.azienda.nome ?? ""),
    settore: String(dati.azienda.settore ?? ""),
    fascia: [1, 2, 3, 4].includes(fascia) ? fascia : 3,
    anno: Number.isInteger(dati.azienda.anno) ? dati.azienda.anno : base.azienda.anno,
  };
  const kpi_values = base.kpi_values;
  const ammessi = catalogo.scoring.valutazioni;
  for (const [id, v] of Object.entries(dati.kpi_values)) {
    if (!(id in kpi_values)) avvisi.push(`KPI sconosciuto ignorato: ${id}`);
    else if (!oggetto(v) || !ammessi.includes(v.valore)) errori.push(`Valore non valido per ${id}: ${JSON.stringify(oggetto(v) ? v.valore : v)}.`);
    else kpi_values[id] = { valore: v.valore, note: String(v.note ?? ""), percentuale: String(v.percentuale ?? "") };
  }
  return { errori, avvisi, azienda, kpi_values };
}

/**
 * Valida e normalizza un file importato (o lo stato salvato nel browser).
 * Restituisce { ok, errori, avvisi, stato }: gli errori bloccano l'import, gli avvisi no
 * (KPI sconosciuti ignorati, KPI mancanti a N/V, voci di storico non valide o duplicate scartate).
 */
export function validaImport(catalogo, dati) {
  const n = normalizza(catalogo, dati);
  if (n.errori.length) return { ok: false, errori: n.errori, avvisi: n.avvisi, stato: null };
  const stato = { azienda: n.azienda, kpi_values: n.kpi_values, calc_data: {}, storico: [] };
  const avvisi = [...n.avvisi];

  if (oggetto(dati.calc_data)) {   // solo calcolatori noti e solo input numerici
    for (const [id, inp] of Object.entries(dati.calc_data)) {
      if (!catalogo.calcolatori[id] || !oggetto(inp)) continue;
      const puliti = {};
      for (const i of catalogo.calcolatori[id].inputs) {
        if (typeof inp[i.name] === "number" && Number.isFinite(inp[i.name])) puliti[i.name] = inp[i.name];
      }
      stato.calc_data[id] = puliti;
    }
  }
  if (Array.isArray(dati.storico)) {
    const visti = new Set();
    dati.storico.forEach((voce, i) => {
      const m = normalizza(catalogo, voce);
      if (m.errori.length) avvisi.push(`Voce di storico ${i + 1} ignorata: ${m.errori[0]}`);
      else if (visti.has(m.azienda.anno)) avvisi.push(`Anno ${m.azienda.anno} duplicato nello storico: ignorato`);
      else { visti.add(m.azienda.anno); stato.storico.push({ azienda: m.azienda, kpi_values: m.kpi_values }); }
    });
    stato.storico.sort((a, b) => a.azienda.anno - b.azienda.anno);
  }
  return { ok: true, errori: [], avvisi, stato };
}
