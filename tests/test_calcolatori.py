# tests/test_calcolatori.py
import ast
import json
import pathlib

import pytest

from src.data.kpi_catalog import CALCOLATORI_KPI, AREE
from src.logic.calcolatori import calcola_valore, valuta, calcola_kpi

ROOT = pathlib.Path(__file__).resolve().parent.parent
GOLDEN = json.loads((ROOT / "tests" / "fixtures" / "calcolatori_golden.json").read_text(encoding="utf-8"))


def _casi():
    for kpi_id, casi in GOLDEN.items():
        for c in casi:
            yield pytest.param(kpi_id, c, id=f"{kpi_id}-{'-'.join(str(v) for v in c['inputs'].values())}")


@pytest.mark.parametrize("kpi_id,caso", list(_casi()))
def test_identico_al_comportamento_originale(kpi_id, caso):
    """Le fixture 'golden' sono state generate con le lambda originali (v0.2.0)."""
    config = CALCOLATORI_KPI[kpi_id]
    valore = calcola_valore(config, caso["inputs"])
    assert valore == pytest.approx(caso["valore"], rel=1e-12, abs=1e-12)
    assert valuta(config, valore) == caso["valutazione"]


def test_catalogo_calcolatori_serializzabile_json():
    """Prerequisito per la migrazione a JavaScript (issue #23)."""
    assert json.loads(json.dumps(CALCOLATORI_KPI)) == CALCOLATORI_KPI


def test_calcolatori_riferiscono_kpi_quantitativi_esistenti():
    quantitativi = {k["id"] for a in AREE for k in a["kpi"] if k["tipo"] == "quantitativo"}
    assert set(CALCOLATORI_KPI) <= quantitativi


def test_formule_usano_solo_input_dichiarati():
    for kpi_id, cfg in CALCOLATORI_KPI.items():
        nomi = {i["name"] for i in cfg["inputs"]}
        usati = {v for k, v in cfg["formula"].items() if k != "tipo"}
        assert usati <= nomi, kpi_id


def test_calcola_kpi_esempi():
    assert calcola_kpi("r1", {"retr_uomini": 30000.0, "retr_donne": 27000.0}) == (pytest.approx(10.0), "Parziale")
    assert calcola_kpi("oc5", {"donne_responsabili": 4, "totale_responsabili": 10}) == (pytest.approx(40.0), "Sì")


def test_calcola_kpi_input_mancanti_o_kpi_senza_calcolatore():
    assert calcola_kpi("oc5", {"donne_responsabili": 4}) is None
    assert calcola_kpi("oc5", {"donne_responsabili": 4, "totale_responsabili": ""}) is None
    assert calcola_kpi("c1", {}) is None


@pytest.mark.parametrize("pacchetto", ["data", "logic"])
def test_livelli_dati_e_logica_non_dipendono_da_streamlit(pacchetto):
    """Separazione dei livelli (issue #21): niente UI in src/data e src/logic."""
    for f in (ROOT / "src" / pacchetto).glob("*.py"):
        albero = ast.parse(f.read_text(encoding="utf-8"))
        for nodo in ast.walk(albero):
            nomi = []
            if isinstance(nodo, ast.Import):
                nomi = [a.name for a in nodo.names]
            elif isinstance(nodo, ast.ImportFrom):
                nomi = [nodo.module or ""]
            assert not any(n.split(".")[0] == "streamlit" for n in nomi), f"{f.name} importa streamlit"
