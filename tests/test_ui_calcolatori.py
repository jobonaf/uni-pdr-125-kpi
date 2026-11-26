# tests/test_ui_calcolatori.py
# Test di integrazione sull'interfaccia Streamlit (richiede streamlit installato).
import pathlib

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402


APP = pathlib.Path(__file__).resolve().parent.parent / "streamlit_app.py"


@pytest.fixture
def app():
    return AppTest.from_file(str(APP), default_timeout=60).run()


@pytest.mark.parametrize("kpi_id,inputs,valutazione,percentuale", [
    ("r1", {"retr_uomini": 30000.0, "retr_donne": 27000.0}, "Parziale", "10.0"),
    ("oc5", {"donne_responsabili": 5, "totale_responsabili": 10}, "Sì", "50.0"),
])
def test_pulsante_calcolatore_imposta_valutazione(app, kpi_id, inputs, valutazione, percentuale):
    """Regressione: il pulsante modificava un widget già istanziato (StreamlitAPIException)."""
    for nome, valore in inputs.items():
        app.number_input(key=f"calc_{kpi_id}_{nome}").set_value(valore)
    app.run()
    app.button(key=f"btn_calc_{kpi_id}").click().run()
    assert not app.exception
    assert app.selectbox(key=f"sel_{kpi_id}").value == valutazione
    assert app.text_input(key=f"perc_{kpi_id}").value == percentuale
    assert app.session_state.kpi_values[kpi_id]["valore"] == valutazione
