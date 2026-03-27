import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime
import io

st.set_page_config(
    page_title="UNI/PdR 125:2022 - Gestione KPI Parità di Genere",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# DATI STRUTTURALI — UNI/PdR 125:2022
# =============================================================================

AREE = [
    {
        "id": "cultura",
        "nome": "Cultura e Strategia",
        "peso": 15,
        "colore": "#1a5f7a",
        "icona": "🧭",
        "descrizione": "Misura la coerenza dei valori, della visione e degli obiettivi di inclusione dell'organizzazione con le politiche dichiarate e i comportamenti concreti.",
        "kpi": [
            {
                "id": "c1", "punti": 20, "tipo": "qualitativo",
                "testo": "Piano strategico formalizzato e implementato",
                "descrizione": "L'organizzazione ha adottato un piano strategico formale che favorisce e sostiene lo sviluppo di un ambiente di lavoro inclusivo, con valori aziendali esplicitamente coerenti con una cultura della parità.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "c2", "punti": 10, "tipo": "qualitativo",
                "testo": "Procedure interne per espressione anonima di opinioni",
                "descrizione": "Esistono strumenti concreti che consentono a tutto il personale di esprimere opinioni e suggerimenti in modo anonimo.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "c3", "punti": 20, "tipo": "qualitativo",
                "testo": "Comunicazione interna e sensibilizzazione sul linguaggio inclusivo",
                "descrizione": "Nell'ultimo anno sono state realizzate iniziative sistematiche di comunicazione interna che promuovono comportamenti e un linguaggio capace di garantire un ambiente di lavoro inclusivo.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "c4", "punti": 10, "tipo": "qualitativo",
                "testo": "Politiche per rappresentanza di genere in eventi e panel",
                "descrizione": "Esistono policy esplicite che garantiscono la rappresentanza equa dei generi tra i relatori di eventi aziendali.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "c5", "punti": 10, "tipo": "qualitativo",
                "testo": "Formazione su genere, stereotipi e unconscious bias (ultimo biennio)",
                "descrizione": "Nell'ultimo biennio sono stati realizzati interventi formativi specifici su differenza di genere, stereotipi e bias inconsci.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "c6", "punti": 20, "tipo": "qualitativo",
                "testo": "Survey sulla percezione delle pari opportunità (ultimo anno)",
                "descrizione": "Nell'ultimo anno è stata condotta almeno un'indagine strutturata per rilevare la percezione dei dipendenti sulle pari opportunità.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "c7", "punti": 10, "tipo": "qualitativo",
                "testo": "Promozione delle pari opportunità verso stakeholder esterni (ultimo biennio)",
                "descrizione": "Nell'ultimo biennio l'organizzazione ha realizzato iniziative verso l'esterno su temi di inclusione e parità.",
                "fasceRichieste": [3, 4]
            },
        ]
    },
    {
        "id": "governance",
        "nome": "Governance",
        "peso": 15,
        "colore": "#2d8a6e",
        "icona": "🏛️",
        "descrizione": "Verifica la presenza di presidi organizzativi formali, responsabilità assegnate e risorse allocate per la gestione delle tematiche di genere.",
        "kpi": [
            {
                "id": "g1", "punti": 25, "tipo": "qualitativo",
                "testo": "Presidio organizzativo dedicato all'inclusione e parità di genere",
                "descrizione": "Esiste nella struttura organizzativa un presidio specifico con mandato esplicito sulla gestione e il monitoraggio delle tematiche di inclusione e parità.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "g2", "punti": 25, "tipo": "qualitativo",
                "testo": "Processi per gestire episodi di non inclusività",
                "descrizione": "Sono definiti e operativi processi documentati per ricevere, istruire e risolvere segnalazioni di discriminazione.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "g3", "punti": 15, "tipo": "qualitativo",
                "testo": "Budget dedicato alle iniziative di inclusione e parità",
                "descrizione": "È presente una voce di bilancio dedicata esplicitamente a iniziative per l'inclusione e la parità di genere.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "g4", "punti": 15, "tipo": "qualitativo",
                "testo": "Obiettivi di parità di genere inseriti nella valutazione del management",
                "descrizione": "I vertici e il management hanno obiettivi specifici e misurabili legati alla parità di genere inseriti nel sistema di valutazione della performance.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "g5", "punti": 20, "tipo": "quantitativo",
                "testo": "Quota del genere meno rappresentato nel CdA/organo di controllo ≥ 1/3",
                "descrizione": "Il genere meno rappresentato deve costituire almeno 1/3 della composizione complessiva del consiglio di amministrazione.",
                "fasceRichieste": [2, 3, 4],
                "soglia": "≥ 1/3 composizione CdA"
            },
        ]
    },
    {
        "id": "hr",
        "nome": "Processi HR",
        "peso": 10,
        "colore": "#5b7fa6",
        "icona": "👥",
        "descrizione": "Valuta la neutralità rispetto al genere dei principali processi di gestione del personale lungo tutto il ciclo di vita lavorativo.",
        "kpi": [
            {
                "id": "h1", "punti": 25, "tipo": "qualitativo",
                "testo": "Processi HR neutrali rispetto al genere (selezione, contratto, on-boarding, valutazione)",
                "descrizione": "I processi chiave del ciclo HR sono documentati e prevedono esplicite misure anti-discriminatorie.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "h2", "punti": 15, "tipo": "qualitativo",
                "testo": "Analisi del turnover disaggregata per genere",
                "descrizione": "L'organizzazione raccoglie e analizza regolarmente i dati di turnover disaggregati per genere.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "h3", "punti": 15, "tipo": "qualitativo",
                "testo": "Accesso equo a formazione e percorsi di valorizzazione",
                "descrizione": "Esistono policy che garantiscono la partecipazione equa e paritaria di uomini e donne a tutti i percorsi formativi.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "h4", "punti": 20, "tipo": "qualitativo",
                "testo": "Politiche di mobilità interna e piani di successione inclusivi",
                "descrizione": "I processi di mobilità interna e i piani di successione sono strutturati in modo da garantire pari opportunità.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "h5", "punti": 15, "tipo": "qualitativo",
                "testo": "Protezione del ruolo e della retribuzione nel post-maternità",
                "descrizione": "Esistono procedure documentate che garantiscono al dipendente che rientra da un congedo di maternità di ritrovare la stessa posizione o una equivalente.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "h6", "punti": 10, "tipo": "qualitativo",
                "testo": "Referente aziendale e prassi a tutela da molestie e mobbing",
                "descrizione": "È presente almeno una figura referente con mandato esplicito sulla tutela dei dipendenti da molestie e mobbing.",
                "fasceRichieste": [1, 2, 3, 4]
            },
        ]
    },
    {
        "id": "crescita",
        "nome": "Opportunità di Crescita",
        "peso": 20,
        "colore": "#7b5ea7",
        "icona": "📈",
        "descrizione": "Misura l'effettivo accesso neutrale rispetto al genere ai percorsi di carriera e di crescita professionale.",
        "kpi": [
            {
                "id": "oc1", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne sull'organico totale — fascia 1-2 (confronto biennale)",
                "descrizione": "La percentuale di donne sull'organico totale deve crescere di almeno +10 punti percentuali rispetto al biennio precedente.",
                "fasceRichieste": [1, 2],
                "soglia": "+10pp vs biennio precedente → parità"
            },
            {
                "id": "oc2", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne sull'organico totale vs benchmark industry — fascia 3-4",
                "descrizione": "La percentuale di donne sull'organico deve essere almeno +10 punti percentuali superiore alla media del settore di appartenenza.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs media ATECO industry"
            },
            {
                "id": "oc3", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne dirigenti — fascia 2 (confronto biennale)",
                "descrizione": "La percentuale di donne con qualifica dirigenziale deve crescere di almeno +10 punti percentuali rispetto al biennio precedente.",
                "fasceRichieste": [2],
                "soglia": "+10pp vs biennio precedente"
            },
            {
                "id": "oc4", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne dirigenti vs benchmark industry — fascia 3-4",
                "descrizione": "La percentuale di donne con qualifica di dirigente deve essere almeno +10pp superiore alla media dell'industry.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs media ATECO industry"
            },
            {
                "id": "oc5", "punti": 20, "tipo": "quantitativo",
                "testo": "% donne responsabili di unità organizzative ≥ 40%",
                "descrizione": "La percentuale di donne tra i responsabili di unità organizzative deve essere almeno pari al 40%.",
                "fasceRichieste": [2, 3, 4],
                "soglia": "≥ 40% del totale responsabili"
            },
            {
                "id": "oc6", "punti": 20, "tipo": "quantitativo",
                "testo": "% donne nella prima linea di riporto al Vertice",
                "descrizione": "La percentuale di donne nei ruoli di riporto diretto al CEO deve essere almeno +10pp superiore alla percentuale media di dirigenti donne.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs % dirigenti femminili industry"
            },
            {
                "id": "oc7", "punti": 10, "tipo": "quantitativo",
                "testo": "% donne con delega su budget di spesa/investimento",
                "descrizione": "La percentuale di donne con delega formale su budget deve essere almeno +10pp superiore alla % media di dirigenti donne.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs % dirigenti femminili industry"
            },
        ]
    },
    {
        "id": "retribuzione",
        "nome": "Equità Remunerativa",
        "peso": 20,
        "colore": "#c4622d",
        "icona": "⚖️",
        "descrizione": "Misura il differenziale retributivo tra generi in logica di total reward.",
        "kpi": [
            {
                "id": "r1", "punti": 40, "tipo": "quantitativo",
                "testo": "Gap retributivo per stesso livello e mansione < 10%",
                "descrizione": "La differenza tra la retribuzione media lorda annua di uomini e donne a parità di livello deve essere inferiore al 10%.",
                "fasceRichieste": [1, 2, 3, 4],
                "soglia": "Gap < 10% e decrescente nel tempo"
            },
            {
                "id": "r2", "punti": 30, "tipo": "quantitativo",
                "testo": "Parità nel tasso di promozione annuale per genere",
                "descrizione": "La percentuale di donne promosse deve essere uguale alla percentuale di uomini promossi.",
                "fasceRichieste": [3, 4],
                "soglia": "Tasso promozione F = Tasso promozione M per livello"
            },
            {
                "id": "r3", "punti": 30, "tipo": "quantitativo",
                "testo": "Accesso paritario alla remunerazione variabile",
                "descrizione": "La percentuale di donne che ricevono remunerazione variabile deve essere uguale alla percentuale di uomini.",
                "fasceRichieste": [3, 4],
                "soglia": "% accesso variabile F = % accesso variabile M"
            },
        ]
    },
    {
        "id": "genitorialita",
        "nome": "Tutela Genitorialità",
        "peso": 20,
        "colore": "#b8873f",
        "icona": "🌱",
        "descrizione": "Valuta la presenza di politiche a sostegno della genitorialità in tutte le sue forme.",
        "kpi": [
            {
                "id": "ge1", "punti": 20, "tipo": "qualitativo",
                "testo": "Servizi dedicati al rientro post maternità/paternità",
                "descrizione": "Esistono servizi strutturati per il rientro al lavoro dopo un congedo di maternità o paternità.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "ge2", "punti": 35, "tipo": "qualitativo",
                "testo": "Policy oltre CCNL per maternità/paternità e conciliazione vita-lavoro",
                "descrizione": "L'organizzazione ha adottato policy che vanno oltre quanto previsto dal CCNL.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "ge3", "punti": 25, "tipo": "qualitativo",
                "testo": "Policy per valorizzare la genitorialità come acquisizione di competenze",
                "descrizione": "Esistono policy esplicite che riconoscono e valorizzano la genitorialità come momento di acquisizione di nuove competenze.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "ge4", "punti": 10, "tipo": "quantitativo",
                "testo": "Tasso di fruizione effettiva dei congedi di paternità obbligatori",
                "descrizione": "Rapporto tra il numero di padri che hanno fruito del congedo di paternità obbligatorio e il totale dei padri potenzialmente beneficiari.",
                "fasceRichieste": [3, 4],
                "soglia": "→ 100% fruizione"
            },
            {
                "id": "ge5", "punti": 10, "tipo": "quantitativo",
                "testo": "Tasso di fruizione dei giorni di congedo di paternità previsti dalla legge",
                "descrizione": "Rapporto tra i giorni medi di congedo di paternità effettivamente fruiti e il totale dei giorni potenziali.",
                "fasceRichieste": [3, 4],
                "soglia": "→ 100% giorni fruiti"
            },
        ]
    }
]

CLUSTER = [
    {"id": 1, "nome": "Micro", "range": "1–9 addetti", "emoji": "🔹"},
    {"id": 2, "nome": "Piccola", "range": "10–49 addetti", "emoji": "🔷"},
    {"id": 3, "nome": "Media", "range": "50–249 addetti", "emoji": "🔶"},
    {"id": 4, "nome": "Grande", "range": "≥ 250 addetti", "emoji": "🟠"},
]

KPI_OBBLIGATORI_PER_FASCIA = {
    "c1": [1, 2], "c3": [2], "c5": [2],
    "g1": [1, 2], "g2": [2],
    "h1": [1, 2], "h4": [2], "h6": [1, 2],
    "oc1": [1, 2], "oc3": [2],
    "r1": [1, 2],
    "ge2": [1, 2], "ge3": [1, 2],
}


# =============================================================================
# FUNZIONI DI SUPPORTO
# =============================================================================

def kpi_applicabile(kpi, fascia):
    """Verifica se un KPI è applicabile per la fascia dimensionale"""
    return fascia in kpi["fasceRichieste"]


def is_kpi_obbligatorio(kpi_id, fascia):
    """Verifica se un KPI è obbligatorio per la fascia"""
    if fascia >= 3:
        return True
    return kpi_id in KPI_OBBLIGATORI_PER_FASCIA and fascia in KPI_OBBLIGATORI_PER_FASCIA[kpi_id]


def calcola_score_area(area, kpi_values, fascia):
    """Calcola lo score percentuale di una singola area"""
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
    """Calcola lo score globale ponderato"""
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


def calcola_obbligatori_mancanti(kpi_values, fascia):
    """Calcola i KPI obbligatori non soddisfatti"""
    mancanti = []
    for area in AREE:
        for kpi in area["kpi"]:
            if not kpi_applicabile(kpi, fascia):
                continue
            if not is_kpi_obbligatorio(kpi["id"], fascia):
                continue
            val = kpi_values.get(kpi["id"], {}).get("valore")
            if val not in ["Sì", "Parziale"]:
                mancanti.append({
                    "area": area["nome"],
                    "icona": area["icona"],
                    "colore": area["colore"],
                    "kpi": kpi,
                    "valore_attuale": val
                })
    return mancanti


def init_kpi_values():
    """Inizializza la struttura dati per i valori KPI"""
    values = {}
    for area in AREE:
        for kpi in area["kpi"]:
            values[kpi["id"]] = {"valore": None, "note": "", "percentuale": ""}
    return values


# =============================================================================
# COMPONENTI UI
# =============================================================================

def render_sidebar(azienda, kpi_values):
    """Renderizza la sidebar con informazioni di sintesi"""
    with st.sidebar:
        st.markdown("## ⚖️ UNI/PdR 125:2022")
        st.markdown("### Parità di Genere")
        
        if azienda.get("nome"):
            st.markdown(f"**{azienda['nome']}**")
            st.markdown(f"Anno: {azienda.get('anno', '—')}")
            st.markdown(f"Fascia: {azienda.get('fascia', '—')}")
        
        st.markdown("---")
        
        # Score attuale
        score_data = calcola_score_globale(kpi_values, azienda.get("fascia", 3))
        score = score_data["score_globale"]
        
        col1, col2 = st.columns(2)
        col1.metric("Score", f"{score:.1f}%")
        
        if score >= 60:
            col2.markdown("✅ **CERTIFICABILE**")
        elif score >= 40:
            col2.markdown("⚠️ **IN PROGRESS**")
        else:
            col2.markdown("🔴 **GAP ELEVATO**")
        
        st.markdown("---")
        
        # Progresso per area
        st.markdown("### Progresso per Area")
        for area in AREE:
            res = calcola_score_area(area, kpi_values, azienda.get("fascia", 3))
            if res["totale"] > 0:
                st.markdown(f"{area['icona']} {area['nome']}")
                st.progress(res["completati"] / res["totale"], text=f"{res['completati']}/{res['totale']} KPI")
        
        st.markdown("---")
        st.caption("© Giovanni Bonafè · EUPL v1.2")


def render_anagrafica():
    """Renderizza la sezione anagrafica"""
    st.markdown("## 🏢 Anagrafica Organizzazione")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome organizzazione", value=st.session_state.azienda.get("nome", ""))
        settore = st.selectbox(
            "Settore ATECO",
            options=["", "A", "B-E", "F", "G", "H", "I", "J", "K", "L-N", "O", "P-Q", "R-U"],
            format_func=lambda x: {
                "": "— Seleziona —",
                "A": "A — Agricoltura, silvicoltura e pesca",
                "B-E": "B-E — Industria in senso stretto",
                "F": "F — Costruzioni",
                "G": "G — Commercio",
                "H": "H — Trasporto e magazzinaggio",
                "I": "I — Alberghi e ristoranti",
                "J": "J — Servizi di informazione e comunicazione",
                "K": "K — Attività finanziarie e assicurative",
                "L-N": "L-N — Attività immobiliari, servizi alle imprese",
                "O": "O — Amministrazione pubblica e difesa",
                "P-Q": "P-Q — Istruzione, sanità e altri servizi sociali",
                "R-U": "R-U — Altri servizi collettivi e personali",
            }.get(x, x),
            index=0 if not st.session_state.azienda.get("settore") else 
                  ["", "A", "B-E", "F", "G", "H", "I", "J", "K", "L-N", "O", "P-Q", "R-U"].index(st.session_state.azienda.get("settore", ""))
        )
    
    with col2:
        anno = st.number_input("Anno di riferimento", value=st.session_state.azienda.get("anno", datetime.now().year), min_value=2020, max_value=2040, step=1)
        
        st.markdown("**Fascia dimensionale**")
        fascia_cols = st.columns(4)
        for i, c in enumerate(CLUSTER):
            with fascia_cols[i]:
                if st.button(
                    f"{c['emoji']}\n{c['nome']}\n{c['range']}",
                    key=f"fascia_{c['id']}",
                    use_container_width=True,
                    type="primary" if st.session_state.azienda.get("fascia") == c["id"] else "secondary"
                ):
                    st.session_state.azienda["fascia"] = c["id"]
                    st.rerun()
    
    st.session_state.azienda.update({
        "nome": nome,
        "settore": settore,
        "anno": anno
    })
    
    # Benchmark info
    if settore:
        st.markdown("### 📊 Benchmark di settore")
        st.info("Per i dati aggiornati consultare ISTAT (Rilevazione Forze di Lavoro) e INPS (Rapporto Annuale)")


def render_compilazione():
    """Renderizza la sezione di compilazione KPI"""
    st.markdown("## ✏️ Compilazione KPI")
    
    fascia = st.session_state.azienda.get("fascia", 3)
    
    # Tabs per le aree
    tabs = st.tabs([f"{area['icona']} {area['nome']}" for area in AREE])
    
    for tab, area in zip(tabs, AREE):
        with tab:
            res = calcola_score_area(area, st.session_state.kpi_values, fascia)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Punti ottenuti", f"{res['ottenuti']:.0f}/{res['massimo']}")
            col2.metric("KPI compilati", f"{res['completati']}/{res['totale']}")
            col3.metric("Score area", f"{res['score']:.1f}%")
            
            st.markdown(f"**{area['descrizione']}**")
            st.markdown("---")
            
            for kpi in area["kpi"]:
                applicabile = kpi_applicabile(kpi, fascia)
                obbligatorio = is_kpi_obbligatorio(kpi["id"], fascia)
                
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Titolo KPI con badge
                        badge_text = f"{kpi['tipo'].upper()} | {kpi['punti']} PT"
                        if obbligatorio:
                            badge_text += " | ⚠️ OBBLIGATORIO"
                        if not applicabile:
                            badge_text += " | NON APPLICABILE"
                        
                        st.markdown(f"**{kpi['testo']}**")
                        st.caption(badge_text)
                        
                        if kpi.get("soglia"):
                            st.caption(f"*Soglia: {kpi['soglia']}*")
                        
                        with st.expander("📖 Descrizione estesa"):
                            st.markdown(kpi["descrizione"])
                    
                    with col2:
                        if applicabile:
                            current_val = st.session_state.kpi_values.get(kpi["id"], {}).get("valore", "N/V")
                            value = st.selectbox(
                                "Valutazione",
                                options=["N/V", "No", "Parziale", "Sì"],
                                index=["N/V", "No", "Parziale", "Sì"].index(current_val) if current_val in ["N/V", "No", "Parziale", "Sì"] else 0,
                                key=f"kpi_{kpi['id']}",
                                label_visibility="collapsed"
                            )
                            
                            note = st.text_area(
                                "Note",
                                value=st.session_state.kpi_values.get(kpi["id"], {}).get("note", ""),
                                key=f"note_{kpi['id']}",
                                placeholder="Note, evidenze documentali...",
                                label_visibility="collapsed"
                            )
                            
                            percentuale = ""
                            if kpi["tipo"] == "quantitativo":
                                percentuale = st.text_input(
                                    "Valore % rilevato",
                                    value=st.session_state.kpi_values.get(kpi["id"], {}).get("percentuale", ""),
                                    key=f"perc_{kpi['id']}",
                                    placeholder="Es. 38.5",
                                    label_visibility="collapsed"
                                )
                            
                            st.session_state.kpi_values[kpi["id"]] = {
                                "valore": value,
                                "note": note,
                                "percentuale": percentuale
                            }
                        else:
                            st.info("KPI non applicabile per questa fascia dimensionale")


def render_dashboard():
    """Renderizza la dashboard con grafici"""
    st.markdown("## 📊 Dashboard")
    
    fascia = st.session_state.azienda.get("fascia", 3)
    score_data = calcola_score_globale(st.session_state.kpi_values, fascia)
    score_globale = score_data["score_globale"]
    aree_details = score_data["aree_details"]
    
    # Header con score
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Score Globale: **{score_globale:.1f}%**")
        if score_globale >= 60:
            st.success("✅ Soglia di certificazione raggiunta")
        else:
            st.warning(f"⚠️ Mancano {60 - score_globale:.1f} punti percentuali alla certificazione")
    
    # Verifica KPI obbligatori
    obbligatori_mancanti = calcola_obbligatori_mancanti(st.session_state.kpi_values, fascia)
    
    if obbligatori_mancanti:
        with st.expander("⚠️ KPI obbligatori non soddisfatti", expanded=True):
            st.error(f"**{len(obbligatori_mancanti)} KPI obbligatori non soddisfatti** — bloccanti per la certificazione")
            for m in obbligatori_mancanti:
                st.markdown(f"- **{m['area']}**: {m['kpi']['testo']} → {m['valore_attuale'] or 'N/V'}")
    
    # Grafici
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🕸️ Profilo radar per area")
        radar_data = [{"area": a["nome"], "score": round(a["score"], 1)} for a in aree_details]
        fig = go.Figure(data=go.Scatterpolar(
            r=[d["score"] for d in radar_data],
            theta=[d["area"] for d in radar_data],
            fill='toself',
            marker=dict(color='#1a5f7a'),
            line=dict(color='#1a5f7a', width=2)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Score per area (%)")
        bar_data = pd.DataFrame([{"area": a["nome"], "score": round(a["score"], 1), "colore": a["colore"]} for a in aree_details])
        fig = px.bar(bar_data, x="score", y="area", orientation='h', text="score", color="area", color_discrete_map={a["nome"]: a["colore"] for a in aree_details})
        fig.update_layout(xaxis_title="Score (%)", yaxis_title="", height=400, showlegend=False)
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabella riepilogo
    st.markdown("### 📋 Riepilogo aree")
    df = pd.DataFrame([
        {
            "Area": f"{a['icona']} {a['nome']}",
            "Peso": f"{a['peso']}%",
            "KPI": a["totale"],
            "Compilati": a["completati"],
            "Score": f"{a['score']:.1f}%",
            "Contributo": f"{a['contributo']:.2f}pp"
        }
        for a in aree_details
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Distribuzione KPI
    st.markdown("### 📊 Distribuzione valutazioni KPI")
    distribuzione = {"Sì": 0, "Parziale": 0, "No": 0, "N/V": 0}
    for area in AREE:
        for kpi in area["kpi"]:
            if kpi_applicabile(kpi, fascia):
                val = st.session_state.kpi_values.get(kpi["id"], {}).get("valore", "N/V")
                distribuzione[val] = distribuzione.get(val, 0) + 1
    
    total = sum(distribuzione.values())
    df_dist = pd.DataFrame([
        {"Valutazione": k, "Conteggio": v, "Percentuale": v/total*100 if total > 0 else 0}
        for k, v in distribuzione.items()
    ])
    fig = px.pie(df_dist, values="Conteggio", names="Valutazione", color="Valutazione",
                 color_discrete_map={"Sì": "#2d8a6e", "Parziale": "#b8873f", "No": "#c4622d", "N/V": "#aaa"})
    st.plotly_chart(fig, use_container_width=True)


def render_confronto():
    """Renderizza la sezione di confronto storico"""
    st.markdown("## 📅 Confronto Annualità")
    
    if not st.session_state.anni:
        st.info("Nessun dato storico disponibile. Salva almeno un'annualità dalla sezione 💾 Dati per attivare il confronto.")
        return
    
    # Selezione anno di riferimento
    anni_disponibili = sorted([a["azienda"]["anno"] for a in st.session_state.anni])
    anno_riferimento = st.selectbox("Anno di riferimento", anni_disponibili, index=len(anni_disponibili)-1)
    
    entry_riferimento = next(a for a in st.session_state.anni if a["azienda"]["anno"] == anno_riferimento)
    
    # Calcolo score
    score_corrente = calcola_score_globale(st.session_state.kpi_values, st.session_state.azienda.get("fascia", 3))
    score_riferimento = calcola_score_globale(entry_riferimento["kpi_values"], entry_riferimento["azienda"]["fascia"])
    
    # Confronto score
    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col1:
        st.metric(f"Anno {anno_riferimento}", f"{score_riferimento['score_globale']:.1f}%")
    with col2:
        delta = score_corrente["score_globale"] - score_riferimento["score_globale"]
        st.metric("Δ", f"{delta:+.1f}pp", delta_color="normal")
    with col3:
        st.metric(f"Anno corrente ({st.session_state.azienda.get('anno', '—')})", f"{score_corrente['score_globale']:.1f}%")
    
    # Andamento nel tempo
    st.markdown("### 📈 Andamento Score Globale")
    trend_data = []
    for entry in sorted(st.session_state.anni, key=lambda x: x["azienda"]["anno"]):
        score = calcola_score_globale(entry["kpi_values"], entry["azienda"]["fascia"])
        trend_data.append({"anno": entry["azienda"]["anno"], "score": score["score_globale"]})
    
    # Aggiungi anno corrente
    trend_data.append({"anno": st.session_state.azienda.get("anno", 0), "score": score_corrente["score_globale"]})
    trend_data = sorted(trend_data, key=lambda x: x["anno"])
    
    df_trend = pd.DataFrame(trend_data)
    fig = px.line(df_trend, x="anno", y="score", markers=True)
    fig.update_layout(yaxis_title="Score (%)", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    # Confronto KPI per KPI
    st.markdown("### 📋 Confronto KPI")
    
    confronto_data = []
    for area in AREE:
        for kpi in area["kpi"]:
            fascia = st.session_state.azienda.get("fascia", 3)
            if kpi_applicabile(kpi, fascia):
                val_corr = st.session_state.kpi_values.get(kpi["id"], {}).get("valore", "N/V")
                val_rif = entry_riferimento["kpi_values"].get(kpi["id"], {}).get("valore", "N/V")
                
                confronto_data.append({
                    "Area": area["nome"],
                    "KPI": kpi["testo"],
                    f"{anno_riferimento}": val_rif,
                    "Anno corrente": val_corr,
                    "Variazione": "⬆️" if (val_corr == "Sì" and val_rif != "Sì") or (val_corr == "Parziale" and val_rif == "No") else "⬇️" if (val_corr == "No" and val_rif != "No") else "➡️"
                })
    
    df_confronto = pd.DataFrame(confronto_data)
    st.dataframe(df_confronto, use_container_width=True, hide_index=True)


def render_report():
    """Renderizza il report stampabile"""
    st.markdown("## 📄 Report PDF")
    
    fascia = st.session_state.azienda.get("fascia", 3)
    score_data = calcola_score_globale(st.session_state.kpi_values, fascia)
    
    # Pulsante per stampa/PDF
    st.markdown("""
    <style>
    @media print {
        .stApp { margin: 0; padding: 0; }
        .stMarkdown, .stDataFrame, .stPlotlyChart { break-inside: avoid; }
        button, .stButton, .stSelectbox { display: none !important; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("🖨️ Stampa / Salva PDF", use_container_width=True):
        st.write("Premi Ctrl+P (Cmd+P su Mac) per stampare o salvare come PDF")
    
    st.markdown("---")
    
    # Contenuto report
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"# UNI/PdR 125:2022")
            st.markdown(f"## Report di Valutazione")
            st.markdown(f"### Parità di Genere nelle Organizzazioni")
        with col2:
            st.markdown(f"**{st.session_state.azienda.get('nome', '—')}**")
            st.markdown(f"ATECO: {st.session_state.azienda.get('settore', '—')}")
            st.markdown(f"Fascia: {st.session_state.azienda.get('fascia', '—')}")
            st.markdown(f"Anno: {st.session_state.azienda.get('anno', '—')}")
            st.markdown(f"Generato: {datetime.now().strftime('%d/%m/%Y')}")
        
        st.markdown("---")
        
        # Score
        score = score_data["score_globale"]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### Score Globale Ponderato: **{score:.1f}%**")
        with col2:
            if score >= 60:
                st.success("✅ Soglia di certificazione (60%) raggiunta")
            else:
                st.warning(f"⚠️ Gap alla certificazione: {60 - score:.1f} punti percentuali")
        
        # Dettaglio per area
        for area in score_data["aree_details"]:
            st.markdown(f"### {area['icona']} {area['nome']} — peso {area['peso']}%")
            st.markdown(f"**Score: {area['score']:.1f}%** | **Contributo: {area['contributo']:.2f}pp**")
            
            kpi_area = [k for k in area["kpi"] if kpi_applicabile(k, fascia)]
            for kpi in kpi_area:
                val = st.session_state.kpi_values.get(kpi["id"], {}).get("valore", "N/V")
                icon = "✓" if val == "Sì" else "~" if val == "Parziale" else "✗" if val == "No" else "—"
                punti_ott = kpi["punti"] if val == "Sì" else kpi["punti"] * 0.5 if val == "Parziale" else 0
                st.markdown(f"- **{icon}** {kpi['testo']} — {punti_ott:.0f}/{kpi['punti']} pt")
            
            st.markdown("---")
        
        # Footer
        st.caption("UNI/PdR 125:2022 — Parità di Genere nelle Organizzazioni")
        st.caption(f"Generato il {datetime.now().strftime('%d/%m/%Y %H:%M')}")


def render_import_export():
    """Renderizza la sezione di import/export dati"""
    st.markdown("## 💾 Importa / Esporta Dati")
    
    # Statistiche compilazione
    fascia = st.session_state.azienda.get("fascia", 3)
    kpi_totali = sum(1 for area in AREE for k in area["kpi"] if kpi_applicabile(k, fascia))
    kpi_compilati = sum(1 for v in st.session_state.kpi_values.values() if v.get("valore") not in [None, "N/V"])
    
    col1, col2 = st.columns(2)
    with col1:
        if kpi_compilati < kpi_totali:
            st.info(f"📝 **Compilazione parziale**: {kpi_compilati}/{kpi_totali} KPI compilati")
        else:
            st.success(f"✅ **Compilazione completa**: {kpi_compilati}/{kpi_totali} KPI compilati")
    
    # Esporta
    with col2:
        if st.button("📤 Esporta JSON", use_container_width=True):
            payload = {
                "version": "1.0",
                "compilazione_parziale": kpi_compilati < kpi_totali,
                "kpi_compilati": kpi_compilati,
                "kpi_totali": kpi_totali,
                "azienda": st.session_state.azienda,
                "kpi_values": st.session_state.kpi_values,
                "esportato": datetime.now().isoformat()
            }
            json_str = json.dumps(payload, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Scarica file JSON",
                data=json_str,
                file_name=f"uni-pdr-125_{st.session_state.azienda.get('nome', 'org')}_{st.session_state.azienda.get('anno', '')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Importa
    st.markdown("### 📥 Importa JSON")
    uploaded_file = st.file_uploader("Seleziona un file JSON esportato in precedenza", type=["json"])
    
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            if "azienda" in data and "kpi_values" in data:
                st.session_state.azienda = data["azienda"]
                st.session_state.kpi_values = data["kpi_values"]
                
                # Aggiungi allo storico se non esiste già
                if not any(a["azienda"]["anno"] == data["azienda"]["anno"] for a in st.session_state.anni):
                    st.session_state.anni.append({
                        "azienda": data["azienda"],
                        "kpi_values": data["kpi_values"]
                    })
                    st.session_state.anni.sort(key=lambda x: x["azienda"]["anno"])
                
                st.success(f"✅ Caricato: {data['azienda'].get('nome', '—')} ({data['azienda'].get('anno', '—')})")
                st.rerun()
            else:
                st.error("Formato file non valido")
        except Exception as e:
            st.error(f"Errore durante l'importazione: {e}")
    
    # Storico annualità
    st.markdown("### 📅 Storico Annualità")
    
    if st.button("➕ Salva anno corrente nello storico", use_container_width=True):
        anno_corrente = st.session_state.azienda.get("anno")
        if not any(a["azienda"]["anno"] == anno_corrente for a in st.session_state.anni):
            st.session_state.anni.append({
                "azienda": st.session_state.azienda.copy(),
                "kpi_values": {k: v.copy() if isinstance(v, dict) else v for k, v in st.session_state.kpi_values.items()}
            })
            st.session_state.anni.sort(key=lambda x: x["azienda"]["anno"])
            st.success(f"✅ Anno {anno_corrente} salvato nello storico")
            st.rerun()
        else:
            st.warning(f"L'anno {anno_corrente} è già presente nello storico")
    
    if st.session_state.anni:
        st.markdown("#### Storico salvato:")
        for entry in sorted(st.session_state.anni, key=lambda x: x["azienda"]["anno"], reverse=True):
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                st.markdown(f"**{entry['azienda']['anno']}**")
            with col2:
                st.markdown(entry['azienda'].get('nome', '—'))
            with col3:
                score = calcola_score_globale(entry["kpi_values"], entry["azienda"]["fascia"])
                st.markdown(f"Score: {score['score_globale']:.1f}%")
            with col4:
                if st.button("📂 Carica", key=f"load_{entry['azienda']['anno']}"):
                    st.session_state.azienda = entry["azienda"]
                    st.session_state.kpi_values = entry["kpi_values"]
                    st.success(f"✅ Caricato anno {entry['azienda']['anno']}")
                    st.rerun()
                if st.button("🗑️ Rimuovi", key=f"del_{entry['azienda']['anno']}"):
                    st.session_state.anni = [a for a in st.session_state.anni if a["azienda"]["anno"] != entry["azienda"]["anno"]]
                    st.rerun()


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Inizializza session state
    if "azienda" not in st.session_state:
        st.session_state.azienda = {
            "nome": "",
            "settore": "",
            "fascia": 3,
            "anno": datetime.now().year
        }
    
    if "kpi_values" not in st.session_state:
        st.session_state.kpi_values = init_kpi_values()
    
    if "anni" not in st.session_state:
        st.session_state.anni = []
    
    # Sidebar
    render_sidebar(st.session_state.azienda, st.session_state.kpi_values)
    
    # Main content
    st.title("Strumento di Gestione KPI — UNI/PdR 125:2022")
    st.markdown("### Parità di Genere nelle Organizzazioni")
    
    # Tabs principali
    tabs = st.tabs([
        "🏢 Anagrafica",
        "✏️ KPI",
        "📊 Dashboard",
        "📅 Confronto",
        "📄 Report",
        "💾 Dati"
    ])
    
    with tabs[0]:
        render_anagrafica()
    
    with tabs[1]:
        render_compilazione()
    
    with tabs[2]:
        render_dashboard()
    
    with tabs[3]:
        render_confronto()
    
    with tabs[4]:
        render_report()
    
    with tabs[5]:
        render_import_export()
    
    # Footer
    st.markdown("---")
    st.caption("""
    **UNI/PdR 125:2022 — Parità di Genere nelle Organizzazioni**  
    Autore: Giovanni Bonafè · ORCID: 0000-0002-7815-8866 · Licenza: EUPL v1.2  
    GitHub: https://github.com/jobonaf
    """)


if __name__ == "__main__":
    main()