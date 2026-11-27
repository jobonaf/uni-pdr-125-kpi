# src/data/export_catalog.py
# Costruisce la rappresentazione JSON del catalogo per il frontend statico
# (Bootstrap Italia + GitHub Pages, issue #23). Nessuna dipendenza da Streamlit.
from src.data import kpi_catalog as cat

SCHEMA_VERSION = 1
NORMA = "UNI/PdR 125:2022"


def costruisci_catalogo_json():
    """Restituisce un dict serializzabile in JSON con tutti i dati del catalogo."""
    return {
        "schemaVersion": SCHEMA_VERSION,
        "norma": NORMA,
        "scoring": {
            "sogliaCertificazione": cat.SOGLIA_CERTIFICAZIONE,
            "fattoreParziale": cat.FATTORE_PARZIALE,
            "valutazioni": cat.VALUTAZIONI,
            "fasceConKpiDaRendicontare": cat.FASCE_CON_KPI_DA_RENDICONTARE,
        },
        "cluster": cat.CLUSTER,
        "aree": cat.AREE,
        "kpiDaRendicontarePerFascia": cat.KPI_DA_RENDICONTARE_PER_FASCIA,
        "calcolatori": cat.CALCOLATORI_KPI,
    }
