# src/logic/calcolatori.py
# Logica pura dei calcolatori per i KPI quantitativi (nessuna dipendenza da Streamlit).
# La configurazione dichiarativa è in src.data.kpi_catalog.CALCOLATORI_KPI.
from src.data.kpi_catalog import CALCOLATORI_KPI


def calcola_valore(config, inputs):
    """Calcola il valore dell'indicatore a partire dagli input del calcolatore."""
    f = config["formula"]
    tipo = f["tipo"]
    if tipo == "differenza":
        return inputs[f["a"]] - inputs[f["b"]]
    if tipo == "percentuale":
        return inputs[f["parte"]] / inputs[f["totale"]] * 100
    if tipo == "gap_percentuale":
        rif = inputs[f["riferimento"]]
        if rif <= 0:
            return 0
        return (rif - inputs[f["confronto"]]) / rif * 100
    raise ValueError(f"Tipo di formula sconosciuto: {tipo}")


def valuta(config, valore):
    """Converte il valore calcolato in valutazione: 'Sì', 'Parziale' o 'No'."""
    v = config["valutazione"]
    if v["confronto"] == "maggiore_uguale":
        if valore >= v["soglia_si"]:
            return "Sì"
        return "Parziale" if valore >= v["soglia_parziale"] else "No"
    if v["confronto"] == "minore":
        if valore < v["soglia_si"]:
            return "Sì"
        return "Parziale" if valore < v["soglia_parziale"] else "No"
    raise ValueError(f"Tipo di confronto sconosciuto: {v['confronto']}")


def calcola_kpi(kpi_id, inputs):
    """Esegue il calcolatore di un KPI.

    Restituisce (valore, valutazione), oppure None se il KPI non ha un
    calcolatore o se manca almeno un input.
    """
    config = CALCOLATORI_KPI.get(kpi_id)
    if not config:
        return None
    nomi = [i["name"] for i in config["inputs"]]
    if any(inputs.get(n) in (None, "") for n in nomi):
        return None
    valore = calcola_valore(config, inputs)
    return valore, valuta(config, valore)
