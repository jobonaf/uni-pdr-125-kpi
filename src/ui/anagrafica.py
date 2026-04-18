# src/ui/anagrafica.py
import streamlit as st
from datetime import datetime
from src.data.kpi_catalog import CLUSTER

def render_anagrafica():
    st.markdown("## 🏢 Anagrafica Organizzazione")
    st.warning(
        "⚠️ **Questo strumento è un supporto alla autovalutazione e alla preparazione alla certificazione.**\n\n"
        "La certificazione di parità di genere ai sensi della UNI/PdR 125:2022, necessaria per accedere agli incentivi "
        "di legge (es. sgravi contributivi L. 162/2021), può essere rilasciata **esclusivamente** da un Organismo di "
        "Certificazione accreditato Accredia. Il punteggio calcolato da questa applicazione non costituisce certificazione ufficiale.\n\n"
        "Per l’elenco degli organismi abilitati: [certificazione.pariopportunita.gov.it](https://certificazione.pariopportunita.gov.it/public/organismi-di-certificazione)"
    )
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
    if settore:
        st.markdown("### 📊 Benchmark di settore")
        st.info("Per i dati aggiornati consultare ISTAT (Rilevazione Forze di Lavoro) e INPS (Rapporto Annuale)")