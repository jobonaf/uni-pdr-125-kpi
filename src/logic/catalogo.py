# src/logic/catalogo.py
# Utilità pure di lettura del catalogo (nessuna dipendenza da Streamlit).
from src.data.kpi_catalog import AREE


def trova_kpi(kpi_id):
    """Restituisce il dizionario del KPI con l'id dato, o None se non esiste."""
    for area in AREE:
        for kpi in area["kpi"]:
            if kpi["id"] == kpi_id:
                return kpi
    return None


def formatta_fasce(fasce):
    """Formatta un elenco di fasce: [2] -> '2', [1, 2] -> '1–2', [3, 4] -> '3–4', [1, 3] -> '1, 3'."""
    f = sorted(fasce)
    if len(f) == 1:
        return str(f[0])
    if f == list(range(f[0], f[-1] + 1)):
        return f"{f[0]}–{f[-1]}"
    return ", ".join(str(x) for x in f)


def nota_equivalente(kpi):
    """Nota esplicativa per i KPI che fanno parte di una coppia mutuamente esclusiva.

    Esempio (oc1): "Applicabile alle organizzazioni di fascia 1–2 — per fascia 3–4 vedi
    l'indicatore equivalente con benchmark di settore". Restituisce None se il KPI non ha
    un indicatore equivalente.
    """
    altro = trova_kpi(kpi["equivalente"]) if kpi.get("equivalente") else None
    if altro is None:
        return None
    confronto = "benchmark di settore" if min(altro["fasceRichieste"]) >= 3 else "confronto sul biennio precedente"
    return (
        f"Applicabile alle organizzazioni di fascia {formatta_fasce(kpi['fasceRichieste'])} — "
        f"per fascia {formatta_fasce(altro['fasceRichieste'])} vedi l'indicatore equivalente con {confronto}"
    )
