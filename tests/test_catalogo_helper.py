# tests/test_catalogo_helper.py
import pytest

from src.logic.catalogo import formatta_fasce, nota_equivalente, trova_kpi


@pytest.mark.parametrize("fasce,atteso", [([2], "2"), ([1, 2], "1–2"), ([3, 4], "3–4"), ([1, 2, 3, 4], "1–4"), ([1, 3], "1, 3")])
def test_formatta_fasce(fasce, atteso):
    assert formatta_fasce(fasce) == atteso


def test_trova_kpi():
    assert trova_kpi("r1")["id"] == "r1"
    assert trova_kpi("inesistente") is None


@pytest.mark.parametrize("kpi_id,contiene", [
    ("oc1", ["fascia 1–2", "per fascia 3–4", "benchmark di settore"]),
    ("oc2", ["fascia 3–4", "per fascia 1–2", "biennio precedente"]),
    ("oc3", ["fascia 2", "per fascia 3–4", "benchmark di settore"]),
    ("oc4", ["fascia 3–4", "per fascia 2", "biennio precedente"]),
])
def test_nota_equivalente(kpi_id, contiene):
    nota = nota_equivalente(trova_kpi(kpi_id))
    for frammento in contiene:
        assert frammento in nota


def test_nessuna_nota_per_kpi_senza_equivalente():
    assert nota_equivalente(trova_kpi("c1")) is None
