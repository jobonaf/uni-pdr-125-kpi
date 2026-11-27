# tests/test_documentazione_logica.py
# Impedisce che docs/logica-calcolo.md resti indietro: ogni funzione pubblica della logica
# (Python) e ogni export di scoring.js / calcolatori.js deve comparire nel documento.
import ast
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "logica-calcolo.md").read_text(encoding="utf-8")


def _funzioni_python():
    for f in sorted((ROOT / "src" / "logic").glob("*.py")):
        for nodo in ast.parse(f.read_text(encoding="utf-8")).body:
            if isinstance(nodo, ast.FunctionDef) and not nodo.name.startswith("_"):
                yield f.stem, nodo.name


def _export_js():
    for f in sorted((ROOT / "frontend" / "static" / "js").glob("*.js")):
        yield from re.findall(r"^export function (\w+)", f.read_text(encoding="utf-8"), re.M)


@pytest.mark.parametrize("modulo,nome", list(_funzioni_python()))
def test_funzione_python_documentata(modulo, nome):
    assert f"`{nome}(" in DOC, f"{modulo}.{nome} non documentata in docs/logica-calcolo.md"


@pytest.mark.parametrize("nome", list(_export_js()))
def test_export_js_documentato(nome):
    assert f"`{nome}(" in DOC, f"{nome} non documentata in docs/logica-calcolo.md"


def test_esempio_numerico_coerente_con_il_codice():
    from src.data.kpi_catalog import AREE
    from src.logic.scoring import calcola_score_area

    area = next(a for a in AREE if a["id"] == "retribuzione")
    kv = {"r1": {"valore": "Sì"}, "r2": {"valore": "Parziale"}, "r3": {"valore": "No"}}
    res = calcola_score_area(area, kv, 3)
    assert res["ottenuti"] == 55 and res["massimo"] == 100
    assert res["score"] / 100 * area["peso"] == pytest.approx(11.0)
