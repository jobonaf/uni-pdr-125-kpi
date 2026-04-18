# src/ui/sidebar.py
import streamlit as st
from src.logic.scoring import calcola_score_globale, calcola_score_area
from src.data.kpi_catalog import AREE

def render_sidebar(azienda, kpi_values):
    with st.sidebar:
        st.markdown("## ⚖️ UNI/PdR 125:2022")
        st.markdown("### Parità di Genere")
        if azienda.get("nome"):
            st.markdown(f"**{azienda['nome']}**")
            st.markdown(f"Anno: {azienda.get('anno', '—')}")
            st.markdown(f"Fascia: {azienda.get('fascia', '—')}")
        st.markdown("---")
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
        st.markdown("### Progresso per Area")
        for area in AREE:
            res = calcola_score_area(area, kpi_values, azienda.get("fascia", 3))
            if res["totale"] > 0:
                st.markdown(f"{area['icona']} {area['nome']}")
                st.progress(res["completati"] / res["totale"], text=f"{res['completati']}/{res['totale']} KPI")
        st.markdown("---")
        st.caption("© Giovanni Bonafè · EUPL v1.2")