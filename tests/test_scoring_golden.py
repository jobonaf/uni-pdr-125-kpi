# tests/test_scoring_golden.py
# Le fixture tests/fixtures/scoring_golden.json sono condivise con i test JavaScript
# (frontend/tests/scoring.test.js): qui si verifica che il Python le rispetti ancora.
# Se la logica di scoring cambia volontariamente: python scripts/export_golden_scoring.py
import importlib.util
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "scoring_golden.json").read_text(encoding="utf-8"))

_spec = importlib.util.spec_from_file_location("export_golden_scoring", ROOT / "scripts" / "export_golden_scoring.py")
_gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen)


def test_fixture_golden_aggiornate():
    assert json.loads(json.dumps(_gen.costruisci())) == FIXTURE


def test_golden_copre_tutte_le_fasce_e_gli_stati():
    assert {c["fascia"] for c in FIXTURE} == {1, 2, 3, 4}
    stati = {v for c in FIXTURE for v in c["valori"].values()}
    assert stati == {"N/V", "No", "Parziale", "Sì"}


@pytest.mark.parametrize("fascia", [1, 2])
def test_non_compilati_solo_per_fasce_semplificate(fascia):
    tutti_nv = next(c for c in FIXTURE if c["fascia"] == fascia and c["nome"] == "tutti N/V")
    assert tutti_nv["nonCompilati"]


@pytest.mark.parametrize("fascia", [3, 4])
def test_nessun_non_compilato_per_fasce_complete(fascia):
    assert all(c["nonCompilati"] == [] for c in FIXTURE if c["fascia"] == fascia)
