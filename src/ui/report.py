# src/ui/report.py
import streamlit as st
from datetime import datetime
from src.logic.scoring import calcola_score_globale, kpi_applicabile
from src.data.kpi_catalog import AREE

def render_report():
    st.markdown("## 📄 Report PDF")
    fascia = st.session_state.azienda.get("fascia", 3)
    score_data = calcola_score_globale(st.session_state.kpi_values, fascia)
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
        score = score_data["score_globale"]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### Score Globale Ponderato: **{score:.1f}%**")
        with col2:
            if score >= 60:
                st.success("✅ Soglia di certificazione (60%) raggiunta")
            else:
                st.warning(f"⚠️ Gap alla certificazione: {60 - score:.1f} punti percentuali")
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
        st.markdown("### ⚠️ Avvertenza importante")
        st.markdown(
            "Il presente report deriva da un’autovalutazione effettuata tramite strumento informatico di supporto. "
            "Non costituisce certificazione ufficiale ai sensi della UNI/PdR 125:2022. "
            "La certificazione di parità di genere può essere rilasciata **esclusivamente** da Organismi di Certificazione accreditati Accredia.\n\n"
            "Per l’elenco degli organismi: [certificazione.pariopportunita.gov.it](https://certificazione.pariopportunita.gov.it/public/organismi-di-certificazione)"
        )
        st.caption("UNI/PdR 125:2022 — Parità di Genere nelle Organizzazioni")
        st.caption(f"Generato il {datetime.now().strftime('%d/%m/%Y %H:%M')}")