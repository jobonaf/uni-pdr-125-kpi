import { test } from "node:test";
import assert from "node:assert/strict";
import { statoIniziale, creaExport, validaImport } from "../static/js/stato.js";
import { catalogo } from "./helpers.js";

test("export: stesse chiavi del formato 2.0 di Streamlit", () => {
  const s = statoIniziale(catalogo, 2026);
  const e = creaExport(catalogo, s, new Date("2026-01-01T00:00:00Z"));
  assert.deepEqual(Object.keys(e), ["version", "compilazione_parziale", "kpi_compilati", "kpi_totali", "azienda", "kpi_values", "calc_data", "esportato"]);
  assert.equal(e.version, "2.0");
  assert.equal(e.kpi_compilati, 0);
  assert.equal(e.compilazione_parziale, true);
});

test("round-trip: export → import restituisce lo stesso stato", () => {
  const s = statoIniziale(catalogo, 2026);
  s.azienda = { nome: "ARPA", settore: "Ambiente", fascia: 2, anno: 2026 };
  s.kpi_values.c1 = { valore: "Sì", note: "ok", percentuale: "" };
  const r = validaImport(catalogo, JSON.parse(JSON.stringify(creaExport(catalogo, s))));
  assert.equal(r.ok, true);
  assert.deepEqual(r.stato, s);
});

test("import: errori su fascia, valori e struttura non validi", () => {
  const base = () => creaExport(catalogo, statoIniziale(catalogo));
  let d = base(); d.azienda.fascia = 7;
  assert.equal(validaImport(catalogo, d).ok, false);
  d = base(); d.kpi_values.c1.valore = "Forse";
  assert.match(validaImport(catalogo, d).errori[0], /c1/);
  assert.equal(validaImport(catalogo, { azienda: {} }).ok, false);
  assert.equal(validaImport(catalogo, null).ok, false);
  assert.equal(validaImport(catalogo, []).ok, false);
});

test("import: KPI sconosciuti ignorati con avviso, KPI mancanti a N/V", () => {
  const d = creaExport(catalogo, statoIniziale(catalogo));
  d.kpi_values.zzz = { valore: "Sì" }; delete d.kpi_values.c1;
  const r = validaImport(catalogo, d);
  assert.equal(r.ok, true);
  assert.match(r.avvisi[0], /zzz/);
  assert.equal(r.stato.kpi_values.c1.valore, "N/V");
  assert.ok(!("zzz" in r.stato.kpi_values));
});

test("import: calc_data filtrato (calcolatori noti, solo input numerici) e round-trip", () => {
  const s = statoIniziale(catalogo, 2026);
  s.calc_data.r1 = { retr_uomini: 30000, retr_donne: 27000 };
  const d = JSON.parse(JSON.stringify(creaExport(catalogo, s)));
  assert.deepEqual(validaImport(catalogo, d).stato.calc_data, s.calc_data);
  d.calc_data = { r1: { retr_uomini: 1, retr_donne: "x", extra: 5 }, zzz: { a: 1 }, oc5: null };
  assert.deepEqual(validaImport(catalogo, d).stato.calc_data, { r1: { retr_uomini: 1 } });
});
