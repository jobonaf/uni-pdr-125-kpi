# tests/test_catalogo.py
import pytest
from src.data.kpi_catalog import AREE

KPI = {k["id"]: k for a in AREE for k in a["kpi"]}


@pytest.mark.parametrize("a,b", [("oc1", "oc2"), ("oc3", "oc4")])
def test_coppie_kpi_mutuamente_esclusive(a, b):
    """Issue #14: stessa metrica con benchmark diverso -> mai nella stessa fascia."""
    assert not set(KPI[a]["fasceRichieste"]) & set(KPI[b]["fasceRichieste"])


def test_id_kpi_univoci():
    ids = [k["id"] for a in AREE for k in a["kpi"]]
    assert len(ids) == len(set(ids))


def test_pesi_aree_sommano_a_100():
    assert sum(a["peso"] for a in AREE) == 100


@pytest.mark.parametrize("fascia", [3, 4])
def test_punti_per_area_fasce_alte_sommano_a_100(fascia):
    for a in AREE:
        assert sum(k["punti"] for k in a["kpi"] if fascia in k["fasceRichieste"]) == 100, a["id"]
