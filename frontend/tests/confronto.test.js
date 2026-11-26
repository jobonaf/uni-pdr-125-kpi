import { test } from "node:test";
import assert from "node:assert/strict";
import { confrontaAnni, variazioneKpi } from "../static/js/confronto.js";
import { statoIniziale, creaExport, validaImport } from "../static/js/stato.js";
import { catalogo } from "./helpers.js";

const con = (valore, anno, fascia = 3) => {
  const s = statoIniziale(catalogo, anno); s.azienda.fascia = fascia;
  for (const id of Object.keys(s.kpi_values)) s.kpi_values[id].valore = valore;
  return s;
};

test("variazioneKpi", () => {
  assert.equal(variazioneKpi("No", "Parziale"), "su");
  assert.equal(variazioneKpi("Sì", "Parziale"), "giu");
  assert.equal(variazioneKpi("Sì", "Sì"), "uguale");
  assert.equal(variazioneKpi("N/V", "Sì"), "nd");
  assert.equal(variazioneKpi("No", "N/V"), "nd");
});

test("confrontaAnni: tutti Sì contro tutti Parziale → +50 punti", () => {
  const r = confrontaAnni(catalogo, con("Sì", 2026), con("Parziale", 2025));
  assert.ok(Math.abs(r.scoreCorrente - 100) < 1e-9 && Math.abs(r.scoreRiferimento - 50) < 1e-9 && Math.abs(r.delta - 50) < 1e-9);
  assert.equal(r.aree.length, catalogo.aree.length);
  assert.ok(r.aree.every((a) => Math.abs(a.delta - 50) < 1e-9));
  assert.ok(r.kpi.length > 0 && r.kpi.every((k) => k.variazione === "su"));
});

test("confrontaAnni: fasce diverse, KPI della fascia corrente", () => {
  const r = confrontaAnni(catalogo, con("Sì", 2026, 1), con("No", 2025, 4));
  assert.ok(r.kpi.length < 20 && r.kpi.every((k) => k.variazione === "su"));
});

test("storico: round-trip, voci non valide e anni duplicati scartati con avviso", () => {
  const s = con("Sì", 2026); s.storico = [con("No", 2024), con("Parziale", 2025)].map(({ azienda, kpi_values }) => ({ azienda, kpi_values }));
  const d = JSON.parse(JSON.stringify(creaExport(catalogo, s)));
  assert.deepEqual(validaImport(catalogo, d).stato.storico, s.storico);
  d.storico.push({ azienda: { fascia: 9, anno: 2020 }, kpi_values: {} }, JSON.parse(JSON.stringify(s.storico[0])), "x");
  const r = validaImport(catalogo, d);
  assert.equal(r.ok, true);
  assert.equal(r.stato.storico.length, 2);
  assert.equal(r.avvisi.length, 3);
});

test("import senza storico (file di Streamlit) → storico vuoto", () => {
  const d = creaExport(catalogo, statoIniziale(catalogo)); delete d.storico;
  assert.deepEqual(validaImport(catalogo, d).stato.storico, []);
});
