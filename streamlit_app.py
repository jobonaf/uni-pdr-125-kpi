# streamlit_app.py
import streamlit as st
from datetime import datetime
from src.logic.scoring import init_kpi_values
from src.ui.sidebar import render_sidebar
from src.ui.anagrafica import render_anagrafica
from src.ui.compilazione import render_compilazione
from src.ui.dashboard import render_dashboard
from src.ui.confronto import render_confronto
from src.ui.report import render_report
from src.ui.import_export import render_import_export

st.set_page_config(
    page_title="UNI/PdR 125:2022 - Gestione KPI Parità di Genere",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
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

    render_sidebar(st.session_state.azienda, st.session_state.kpi_values)

    st.title("Strumento di Gestione KPI — UNI/PdR 125:2022")
    st.markdown("### Parità di Genere nelle Organizzazioni")

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

    st.markdown("---")
    st.caption("""
    **UNI/PdR 125:2022 — Parità di Genere nelle Organizzazioni**  
    Autore: Giovanni Bonafè · ORCID: 0000-0002-7815-8866 · Licenza: EUPL v1.2  
    GitHub: https://github.com/jobonaf
    """)

if __name__ == "__main__":
    main()