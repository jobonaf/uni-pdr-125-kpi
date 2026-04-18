# src/ui/compilazione.py
import streamlit as st
from src.data.kpi_catalog import AREE, CALCOLATORI_KPI
from src.logic.scoring import kpi_applicabile, is_kpi_da_rendicontare, calcola_score_area
from src.logic.scoring import init_calculator_state, update_kpi_from_calculator

def render_compilazione():
    st.markdown("## ✏️ Compilazione KPI")
    fascia = st.session_state.azienda.get("fascia", 3)
    tabs = st.tabs([f"{area['icona']} {area['nome']}" for area in AREE])
    for tab, area in zip(tabs, AREE):
        with tab:
            kpi_applicabili = [k for k in area["kpi"] if kpi_applicabile(k, fascia)]
            if not kpi_applicabili:
                st.info("Nessun KPI applicabile per questa fascia dimensionale in quest'area.")
                continue
            res = calcola_score_area(area, st.session_state.kpi_values, fascia)
            col1, col2, col3 = st.columns(3)
            col1.metric("Punti ottenuti", f"{res['ottenuti']:.1f}/{res['massimo']}")
            col2.metric("KPI compilati", f"{res['completati']}/{res['totale']}")
            col3.metric("Score area", f"{res['score']:.1f}%")
            st.markdown(f"**{area['descrizione']}**")
            st.markdown("---")
            for kpi in kpi_applicabili:
                da_rendicontare = is_kpi_da_rendicontare(kpi["id"], fascia)
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        badge_text = f"{kpi['tipo'].upper()} | {kpi['punti']} PT"
                        if da_rendicontare:
                            badge_text += " | 📋 DA RENDICONTARE"
                        st.markdown(f"**{kpi['testo']}**")
                        st.caption(badge_text)
                        if kpi.get("soglia"):
                            st.caption(f"*Soglia: {kpi['soglia']}*")
                        with st.expander("📖 Descrizione estesa"):
                            st.markdown(kpi["descrizione"])
                    with col2:
                        current_val = st.session_state.kpi_values.get(kpi["id"], {}).get("valore", "N/V")
                        current_note = st.session_state.kpi_values.get(kpi["id"], {}).get("note", "")
                        current_perc = st.session_state.kpi_values.get(kpi["id"], {}).get("percentuale", "")
                        opzioni = ["N/V", "No", "Parziale", "Sì"]
                        def on_val_change(kpi_id):
                            st.session_state.kpi_values[kpi_id]["valore"] = st.session_state[f"sel_{kpi_id}"]
                        def on_note_change(kpi_id):
                            st.session_state.kpi_values[kpi_id]["note"] = st.session_state[f"note_{kpi_id}"]
                        def on_perc_change(kpi_id):
                            st.session_state.kpi_values[kpi_id]["percentuale"] = st.session_state[f"perc_{kpi_id}"]
                        st.selectbox(
                            "Valutazione", options=opzioni, key=f"sel_{kpi['id']}",
                            label_visibility="collapsed", on_change=on_val_change, args=(kpi["id"],)
                        )
                        st.text_area(
                            "Note", key=f"note_{kpi['id']}", placeholder="Note, evidenze documentali...",
                            label_visibility="collapsed", on_change=on_note_change, args=(kpi["id"],)
                        )
                        if kpi["tipo"] == "quantitativo":
                            st.text_input(
                                "Valore % rilevato", key=f"perc_{kpi['id']}", placeholder="Es. 38.5",
                                label_visibility="collapsed", on_change=on_perc_change, args=(kpi["id"],)
                            )
                            if kpi["id"] in CALCOLATORI_KPI:
                                with st.expander("🧮 Calcolatore automatico"):
                                    config = CALCOLATORI_KPI[kpi["id"]]
                                    # Inizializza stato calcolatore se necessario
                                    if f"calc_{kpi['id']}" not in st.session_state:
                                        st.session_state[f"calc_{kpi['id']}"] = {}
                                    for inp in config["inputs"]:
                                        key = f"calc_{kpi['id']}_{inp['name']}"
                                        current_calc_val = st.session_state.get(f"calc_{kpi['id']}", {}).get(inp["name"])
                                        if current_calc_val is None:
                                            if inp["type"] == "int":
                                                current_calc_val = inp.get("min", 0)
                                            else:
                                                current_calc_val = float(inp.get("min", 0.0))
                                            st.session_state[f"calc_{kpi['id']}"][inp["name"]] = current_calc_val
                                        if inp["type"] == "float":
                                            min_val = float(inp.get("min")) if inp.get("min") is not None else None
                                            max_val = float(inp.get("max")) if inp.get("max") is not None else None
                                            st.number_input(
                                                inp["label"], value=float(current_calc_val), key=key,
                                                step=0.1, format="%.2f", min_value=min_val, max_value=max_val
                                            )
                                        else:
                                            min_val = int(inp.get("min")) if inp.get("min") is not None else None
                                            max_val = int(inp.get("max")) if inp.get("max") is not None else None
                                            st.number_input(
                                                inp["label"], value=int(current_calc_val), key=key,
                                                step=1, min_value=min_val, max_value=max_val
                                            )
                                        st.session_state.setdefault(f"calc_{kpi['id']}", {})[inp["name"]] = st.session_state[key]
                                    if st.button(f"Calcola e imposta valutazione", key=f"btn_calc_{kpi['id']}"):
                                        # Aggiorna kpi_values in base ai valori del calcolatore
                                        calc_data = st.session_state.get(f"calc_{kpi['id']}", {})
                                        if calc_data:
                                            inputs = {inp["name"]: calc_data.get(inp["name"]) for inp in config["inputs"]}
                                            if all(v is not None for v in inputs.values()):
                                                valore_calcolato = config["formula"](inputs)
                                                valutazione = config["valutazione"](valore_calcolato)
                                                st.session_state[f"sel_{kpi['id']}"] = valutazione
                                                st.session_state[f"perc_{kpi['id']}"] = f"{valore_calcolato:.1f}"
                                                st.session_state.kpi_values[kpi["id"]] = {
                                                    "valore": valutazione,
                                                    "note": st.session_state.kpi_values.get(kpi["id"], {}).get("note", ""),
                                                    "percentuale": f"{valore_calcolato:.1f}"
                                                }
                                                st.rerun()
                        # Inizializza i widget principali
                        if f"sel_{kpi['id']}" not in st.session_state:
                            st.session_state[f"sel_{kpi['id']}"] = current_val
                        if f"note_{kpi['id']}" not in st.session_state:
                            st.session_state[f"note_{kpi['id']}"] = current_note
                        if f"perc_{kpi['id']}" not in st.session_state and kpi["tipo"] == "quantitativo":
                            st.session_state[f"perc_{kpi['id']}"] = current_perc