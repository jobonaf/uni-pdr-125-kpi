# tests/test_export_catalog.py
import json
import pathlib
import subprocess
import sys

from src.data.export_catalog import costruisci_catalogo_json
from src.data.kpi_catalog import AREE

ROOT = pathlib.Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "frontend" / "static" / "data" / "kpi-catalog.json"


def _json_committato():
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_json_committato_aggiornato():
    """Se fallisce: python scripts/export_catalog.py (poi commit del JSON)."""
    assert _json_committato() == json.loads(json.dumps(costruisci_catalogo_json()))


def test_script_check_ok():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "export_catalog.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_struttura_json():
    c = _json_committato()
    assert c["schemaVersion"] == 1
    assert c["scoring"]["sogliaCertificazione"] == 60
    assert c["scoring"]["fattoreParziale"] == 0.5
    assert c["scoring"]["valutazioni"] == ["N/V", "No", "Parziale", "Sì"]
    assert [a["id"] for a in c["aree"]] == [a["id"] for a in AREE]
    assert [x["id"] for x in c["cluster"]] == [1, 2, 3, 4]


def test_riferimenti_interni_coerenti():
    c = _json_committato()
    kpi = {k["id"]: k for a in c["aree"] for k in a["kpi"]}
    assert set(c["kpiDaRendicontarePerFascia"]) <= set(kpi)
    assert set(c["calcolatori"]) <= set(kpi)
    fasce = {x["id"] for x in c["cluster"]}
    for fasce_kpi in c["kpiDaRendicontarePerFascia"].values():
        assert set(fasce_kpi) <= fasce
        assert set(fasce_kpi) <= set(c["scoring"]["fasceConKpiDaRendicontare"])
