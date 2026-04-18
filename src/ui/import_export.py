# src/ui/import_export.py
import streamlit as st
import json
from datetime import datetime
from src.logic.scoring import calcola_score_globale, kpi_applicabile, init_kpi_values
from src.data.kpi_catalog import AREE, CALCOLATORI_KPI

def render_import_export():
    st.markdown("## 💾 Importa / Esporta Dati")
    fascia = st.session_state.azienda.get("fascia", 3)
    kpi_totali = sum(1 for area in AREE for k in area["kpi"] if kpi_applicabile(k, fascia))
    kpi_compilati = sum(1 for v in st.session_state.kpi_values.values() if v.get("valore") not in [None, "N/V"])
    col1, col2 = st.columns(2)
    with col1:
        if kpi_compilati < kpi_totali:
            st.info(f"📝 **Compilazione parziale**: {kpi_compilati}/{kpi_totali} KPI compilati")
        else:
            st.success(f"✅ **Compilazione completa**: {kpi_compilati}/{kpi_totali} KPI compilati")
    with col2:
        if st.button("📤 Esporta JSON", use_container_width=True):
            calc_data = {}
            for kpi_id in CALCOLATORI_KPI.keys():
                if f"calc_{kpi_id}" in st.session_state:
                    calc_data[kpi_id] = st.session_state[f"calc_{kpi_id}"]
            payload = {
                "version": "2.0",
                "compilazione_parziale": kpi_compilati < kpi_totali,
                "kpi_compilati": kpi_compilati,
                "kpi_totali": kpi_totali,
                "azienda": st.session_state.azienda,
                "kpi_values": st.session_state.kpi_values,
                "calc_data": calc_data,
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
    st.markdown("### 📥 Importa JSON")
    uploaded_file = st.file_uploader("Seleziona un file JSON esportato in precedenza", type=["json"])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            if "azienda" in data and "kpi_values" in data:
                st.session_state.azienda = data["azienda"]
                st.session_state.kpi_values = data["kpi_values"]
                if "calc_data" in data:
                    for kpi_id, calc_values in data["calc_data"].items():
                        st.session_state[f"calc_{kpi_id}"] = calc_values
                for k in list(st.session_state.keys()):
                    if k.startswith("sel_") or k.startswith("note_") or k.startswith("perc_") or k.startswith("calc_"):
                        del st.session_state[k]
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
                    for k in list(st.session_state.keys()):
                        if k.startswith("sel_") or k.startswith("note_") or k.startswith("perc_") or k.startswith("calc_"):
                            del st.session_state[k]
                    st.success(f"✅ Caricato anno {entry['azienda']['anno']}")
                    st.rerun()
                if st.button("🗑️ Rimuovi", key=f"del_{entry['azienda']['anno']}"):
                    st.session_state.anni = [a for a in st.session_state.anni if a["azienda"]["anno"] != entry["azienda"]["anno"]]
                    st.rerun()