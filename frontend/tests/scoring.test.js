import { test } from "node:test";
import assert from "node:assert/strict";
import {
  calcolaScoreGlobale,
  calcolaKpiNonCompilati,
  initKpiValues,
  certificabile,
} from "../static/js/scoring.js";
import { catalogo, caricaJson } from "./helpers.js";

const golden = caricaJson("tests", "fixtures", "scoring_golden.json");
const vicino = (a, b) => Math.abs(a - b) <= 1e-9;

function kpiValuesDa(valori) {
  return Object.fromEntries(Object.entries(valori).map(([id, v]) => [id, { valore: v, note: "", percentuale: "" }]));
}

test("scoring: stesso risultato dell'implementazione Python su tutti gli scenari golden", () => {
  assert.ok(golden.length >= 100);
  for (const c of golden) {
    const etichetta = `fascia ${c.fascia} — ${c.nome}`;
    const kv = kpiValuesDa(c.valori);

    const g = calcolaScoreGlobale(catalogo, kv, c.fascia);
    assert.ok(vicino(g.scoreGlobale, c.scoreGlobale), `${etichetta}: score globale ${g.scoreGlobale} ≠ ${c.scoreGlobale}`);
    assert.equal(g.areeDetails.length, c.aree.length, etichetta);

    c.aree.forEach((atteso, i) => {
      const a = g.areeDetails[i];
      assert.equal(a.id, atteso.id, etichetta);
      for (const chiave of ["score", "massimo", "ottenuti", "contributo"]) {
        assert.ok(vicino(a[chiave], atteso[chiave]), `${etichetta} ${a.id}.${chiave}: ${a[chiave]} ≠ ${atteso[chiave]}`);
      }
      assert.equal(a.completati, atteso.completati, `${etichetta} ${a.id}.completati`);
      assert.equal(a.totale, atteso.totale, `${etichetta} ${a.id}.totale`);
    });

    const nonCompilati = calcolaKpiNonCompilati(catalogo, kv, c.fascia).map((m) => m.kpi.id);
    assert.deepEqual(nonCompilati, c.nonCompilati, `${etichetta}: KPI non compilati`);
  }
});

test("initKpiValues: un valore N/V per ogni KPI del catalogo", () => {
  const values = initKpiValues(catalogo);
  const ids = catalogo.aree.flatMap((a) => a.kpi.map((k) => k.id));
  assert.deepEqual(Object.keys(values), ids);
  assert.ok(Object.values(values).every((v) => v.valore === "N/V"));
});

test("certificabile: soglia al 60% inclusa", () => {
  assert.equal(certificabile(catalogo, 60), true);
  assert.equal(certificabile(catalogo, 59.99), false);
});
