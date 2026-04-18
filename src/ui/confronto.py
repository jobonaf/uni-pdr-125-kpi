# src/ui/confronto.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.logic.scoring import calcola_score_globale, kpi_applicabile
from src.data.kpi_catalog import AREE

def render_confronto():
    st.markdown("## 📅 Confronto Annualità")
    if not st.session_state.anni:
        st.info("Nessun dato storico disponibile. Salva almeno un'annualità dalla sezione 💾 Dati per attivare il confronto.")
        return
    anni_disponibili = sorted([a["azienda"]["anno"] for a in st.session_state.anni])
    anno_riferimento = st.selectbox("Anno di riferimento", anni_disponibili, index=len(anni_disponibili)-1)
    entry_riferimento = next(a for a in st.session_state.anni if a["azienda"]["anno"] == anno_riferimento)
    score_corrente = calcola_score_globale(st.session_state.kpi_values, st.session_state.azienda.get("fascia", 3))
    score_riferimento = calcola_score_globale(entry_riferimento["kpi_values"], entry_riferimento["azienda"]["fascia"])
    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col1:
        st.metric(f"Anno {anno_riferimento}", f"{score_riferimento['score_globale']:.1f}%")
    with col2:
        delta = score_corrente["score_globale"] - score_riferimento["score_globale"]
        st.metric("Δ", f"{delta:+.1f}pp", delta_color="normal")
    with col3:
        st.metric(f"Anno corrente ({st.session_state.azienda.get('anno', '—')})", f"{score_corrente['score_globale']:.1f}%")
    st.markdown("### 📈 Andamento Score Globale")
    trend_data = []
    for entry in sorted(st.session_state.anni, key=lambda x: x["azienda"]["anno"]):
        score = calcola_score_globale(entry["kpi_values"], entry["azienda"]["fascia"])
        trend_data.append({"anno": entry["azienda"]["anno"], "score": score["score_globale"]})
    trend_data.append({"anno": st.session_state.azienda.get("anno", 0), "score": score_corrente["score_globale"]})
    trend_data = sorted(trend_data, key=lambda x: x["anno"])
    df_trend = pd.DataFrame(trend_data)
    fig = px.line(df_trend, x="anno", y="score", markers=True)
    fig.update_layout(yaxis_title="Score (%)", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### 📋 Confronto KPI")
    confronto_data = []
    for area in AREE:
        for kpi in area["kpi"]:
            fascia = st.session_state.azienda.get("fascia", 3)
            if kpi_applicabile(kpi, fascia):
                val_corr = st.session_state.kpi_values.get(kpi["id"], {}).get("valore", "N/V")
                val_rif = entry_riferimento["kpi_values"].get(kpi["id"], {}).get("valore", "N/V")
                confronto_data.append({
                    "Area": area["nome"], "KPI": kpi["testo"],
                    f"{anno_riferimento}": val_rif, "Anno corrente": val_corr,
                    "Variazione": "⬆️" if (val_corr == "Sì" and val_rif != "Sì") or (val_corr == "Parziale" and val_rif == "No") else "⬇️" if (val_corr == "No" and val_rif != "No") else "➡️"
                })
    df_confronto = pd.DataFrame(confronto_data)
    st.dataframe(df_confronto, use_container_width=True, hide_index=True)