#!/usr/bin/env python3
"""Genera tests/fixtures/scoring_golden.json: scenari di riferimento per lo scoring.

Le fixture sono prodotte dall'implementazione Python (src/logic/scoring.py) e usate
dai test di entrambe le implementazioni (Python e JavaScript), così non possono divergere.
Rigenerare solo se la logica di scoring cambia volontariamente:

    python scripts/export_golden_scoring.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data.kpi_catalog import AREE  # noqa: E402
from src.logic.scoring import calcola_score_globale, calcola_kpi_non_compilati  # noqa: E402

OUTPUT = ROOT / "tests" / "fixtures" / "scoring_golden.json"
FASCE = [1, 2, 3, 4]
VALORI = ["N/V", "No", "Parziale", "Sì"]
N_CASUALI = 20


def tutti_i_kpi():
    return [k["id"] for a in AREE for k in a["kpi"]]


def generatore(seed):
    """LCG deterministico (indipendente dalla versione di Python)."""
    stato = seed
    while True:
        stato = (stato * 1103515245 + 12345) % (2 ** 31)
        yield stato >> 8


def scenari_valori():
    ids = tutti_i_kpi()
    yield "tutti N/V", {i: "N/V" for i in ids}
    for v in ("No", "Parziale", "Sì"):
        yield f"tutti {v}", {i: v for i in ids}
    for a in AREE:
        valori = {i: "N/V" for i in ids}
        valori.update({k["id"]: "Sì" for k in a["kpi"]})
        yield f"solo area {a['id']} = Sì", valori
    mancanti = {i: "Sì" for i in ids}
    mancanti.pop(ids[0])
    yield "KPI assente dal dizionario", mancanti
    rnd = generatore(125)
    for n in range(N_CASUALI):
        yield f"casuale {n + 1}", {i: VALORI[next(rnd) % 4] for i in ids}


def costruisci():
    casi = []
    for fascia in FASCE:
        for nome, valori in scenari_valori():
            kv = {i: {"valore": v, "note": "", "percentuale": ""} for i, v in valori.items()}
            g = calcola_score_globale(kv, fascia)
            casi.append({
                "nome": nome,
                "fascia": fascia,
                "valori": valori,
                "scoreGlobale": g["score_globale"],
                "aree": [
                    {k: d[k] for k in ("id", "score", "massimo", "ottenuti", "completati", "totale", "contributo")}
                    for d in g["aree_details"]
                ],
                "nonCompilati": [m["kpi"]["id"] for m in calcola_kpi_non_compilati(kv, fascia)],
            })
    return casi


if __name__ == "__main__":
    casi = costruisci()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(casi, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Scritti {len(casi)} scenari in {OUTPUT.relative_to(ROOT)}")
