import { test } from "node:test";
import assert from "node:assert/strict";
import { calcolaValore, valuta, calcolaKpi } from "../static/js/calcolatori.js";
import { catalogo, caricaJson } from "./helpers.js";

const golden = caricaJson("tests", "fixtures", "calcolatori_golden.json");

test("calcolatori: stesso risultato dell'implementazione originale (fixture golden)", () => {
  let n = 0;
  for (const [kpiId, casi] of Object.entries(golden)) {
    const config = catalogo.calcolatori[kpiId];
    assert.ok(config, `calcolatore ${kpiId} assente dal catalogo`);
    for (const c of casi) {
      const valore = calcolaValore(config, c.inputs);
      assert.ok(
        Math.abs(valore - c.valore) <= 1e-9,
        `${kpiId} ${JSON.stringify(c.inputs)}: atteso ${c.valore}, ottenuto ${valore}`
      );
      assert.equal(valuta(config, valore), c.valutazione, `${kpiId} ${JSON.stringify(c.inputs)}`);
      n += 1;
    }
  }
  assert.ok(n > 600);
});

test("calcolaKpi: esempi", () => {
  const r1 = calcolaKpi(catalogo, "r1", { retr_uomini: 30000, retr_donne: 27000 });
  assert.ok(Math.abs(r1.valore - 10) < 1e-9);
  assert.equal(r1.valutazione, "Parziale");
  const oc5 = calcolaKpi(catalogo, "oc5", { donne_responsabili: 4, totale_responsabili: 10 });
  assert.equal(oc5.valutazione, "Sì");
});

test("calcolaKpi: null con input mancanti, KPI senza calcolatore o divisione per zero", () => {
  assert.equal(calcolaKpi(catalogo, "oc5", { donne_responsabili: 4 }), null);
  assert.equal(calcolaKpi(catalogo, "oc5", { donne_responsabili: 4, totale_responsabili: "" }), null);
  assert.equal(calcolaKpi(catalogo, "oc5", { donne_responsabili: 4, totale_responsabili: NaN }), null);
  assert.equal(calcolaKpi(catalogo, "oc5", { donne_responsabili: 4, totale_responsabili: 0 }), null);
  assert.equal(calcolaKpi(catalogo, "c1", {}), null);
});
