# src/logic/scoring.py
from src.data.kpi_catalog import AREE, KPI_DA_RENDICONTARE_PER_FASCIA

def kpi_applicabile(kpi, fascia):
    return fascia in kpi["fasceRichieste"]

def is_kpi_da_rendicontare(kpi_id, fascia):
    if fascia >= 3:
        return False
    return kpi_id in KPI_DA_RENDICONTARE_PER_FASCIA and fascia in KPI_DA_RENDICONTARE_PER_FASCIA[kpi_id]

def calcola_score_area(area, kpi_values, fascia):
    kpi_appl = [k for k in area["kpi"] if kpi_applicabile(k, fascia)]
    if not kpi_appl:
        return {"score": 0, "massimo": 0, "ottenuti": 0, "completati": 0, "totale": 0}
    punti_ottenuti = 0
    punti_massimi = 0
    completati = 0
    for k in kpi_appl:
        punti_massimi += k["punti"]
        val = kpi_values.get(k["id"], {}).get("valore")
        if val == "Sì":
            punti_ottenuti += k["punti"]
            completati += 1
        elif val == "Parziale":
            punti_ottenuti += k["punti"] * 0.5
            completati += 1
        elif val == "No":
            completati += 1
    score = (punti_ottenuti / punti_massimi * 100) if punti_massimi > 0 else 0
    return {
        "score": score,
        "massimo": punti_massimi,
        "ottenuti": punti_ottenuti,
        "completati": completati,
        "totale": len(kpi_appl)
    }

def calcola_score_globale(kpi_values, fascia):
    score_globale = 0
    aree_details = []
    for area in AREE:
        res = calcola_score_area(area, kpi_values, fascia)
        contributo = (res["score"] / 100) * area["peso"]
        score_globale += contributo
        aree_details.append({
            **area,
            **res,
            "contributo": contributo
        })
    return {"score_globale": score_globale, "aree_details": aree_details}

def calcola_kpi_non_compilati(kpi_values, fascia):
    non_compilati = []
    for area in AREE:
        for kpi in area["kpi"]:
            if not kpi_applicabile(kpi, fascia):
                continue
            if not is_kpi_da_rendicontare(kpi["id"], fascia):
                continue
            val = kpi_values.get(kpi["id"], {}).get("valore")
            if val in [None, "N/V"]:
                non_compilati.append({
                    "area": area["nome"],
                    "icona": area["icona"],
                    "colore": area["colore"],
                    "kpi": kpi,
                    "valore_attuale": val
                })
    return non_compilati

def init_kpi_values():
    """Inizializza la struttura dati per i valori KPI."""
    values = {}
    for area in AREE:
        for kpi in area["kpi"]:
            values[kpi["id"]] = {"valore": "N/V", "note": "", "percentuale": ""}
    return values
