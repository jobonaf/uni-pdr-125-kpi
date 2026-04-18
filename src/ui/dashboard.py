# src/ui/dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.logic.scoring import calcola_score_globale, calcola_kpi_non_compilati, kpi_applicabile
from src.data.kpi_catalog import AREE

def render_dashboard():
    st.markdown("## 📊 Dashboard")
    fascia = st.session_state.azienda.get("fascia", 3)
    score_data = calcola_score_globale(st.session_state.kpi_values, fascia)
    score_globale = score_data["score_globale"]
    aree_details = score_data["aree_details"]
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Score Globale: **{score_globale:.1f}%**")
        if score_globale >= 60:
            st.success("✅ Soglia di certificazione raggiunta")
        else:
            st.warning(f"⚠️ Mancano {60 - score_globale:.1f} punti percentuali alla certificazione")
    kpi_non_compilati = calcola_kpi_non_compilati(st.session_state.kpi_values, fascia)
    if kpi_non_compilati:
        with st.expander("📋 Indicatori da rendicontare non ancora compilati", expanded=True):
            st.warning(
                f"**{len(kpi_non_compilati)} indicatori chiave di prestazione (KPI) non ancora compilati** — "
                f"compilali per ottenere uno score accurato. "
                f"La certificazione dipende dal punteggio complessivo (soglia: 60%), "
                f"non dall'esito di singoli indicatori."
            )
            for m in kpi_non_compilati:
                st.markdown(f"- **{m['area']}**: {m['kpi']['testo']}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🕸️ Profilo radar per area")
        radar_data = [{"area": a["nome"], "score": round(a["score"], 1)} for a in aree_details]
        fig = go.Figure(data=go.Scatterpolar(
            r=[d["score"] for d in radar_data],
            theta=[d["area"] for d in radar_data],
            fill='toself', marker=dict(color='#1a5f7a'), line=dict(color='#1a5f7a', width=2)
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### 📊 Score per area (%)")
        bar_data = pd.DataFrame([{"area": a["nome"], "score": round(a["score"], 1), "colore": a["colore"]} for a in aree_details])
        fig = px.bar(bar_data, x="score", y="area", orientation='h', text="score", color="area",
                     color_discrete_map={a["nome"]: a["colore"] for a in aree_details})
        fig.update_layout(xaxis_title="Score (%)", yaxis_title="", height=400, showlegend=False)
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("### 📋 Riepilogo aree")
    df = pd.DataFrame([
        {"Area": f"{a['icona']} {a['nome']}", "Peso": f"{a['peso']}%", "KPI": a["totale"],
         "Compilati": a["completati"], "Score": f"{a['score']:.1f}%", "Contributo": f"{a['contributo']:.2f}pp"}
        for a in aree_details
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
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