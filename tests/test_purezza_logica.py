# tests/test_purezza_logica.py
# Issue #21: i livelli src/data e src/logic sono "puri": nessuna UI, nessuna chiamata di
# rete, nessun database, nessun accesso al file system (gli script in scripts/ sono
# l'unico punto in cui si legge/scrive su disco).
import ast
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULI_VIETATI = {
    "streamlit", "plotly", "pandas",                                   # interfaccia
    "requests", "urllib", "http", "socket", "httpx", "aiohttp",       # rete
    "sqlite3", "sqlalchemy", "psycopg2",                               # database
    "os", "pathlib", "shutil", "subprocess", "tempfile", "io", "glob",  # file system / processi
}
CHIAMATE_VIETATE = {"open", "input", "exec", "eval", "__import__"}


def _file_python():
    for pacchetto in ("data", "logic"):
        yield from sorted((ROOT / "src" / pacchetto).glob("*.py"))


@pytest.mark.parametrize("percorso", list(_file_python()), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_nessuna_dipendenza_da_ui_rete_db_o_filesystem(percorso):
    albero = ast.parse(percorso.read_text(encoding="utf-8"))
    for nodo in ast.walk(albero):
        nomi = []
        if isinstance(nodo, ast.Import):
            nomi = [a.name for a in nodo.names]
        elif isinstance(nodo, ast.ImportFrom):
            nomi = [nodo.module or ""]
        for nome in nomi:
            assert nome.split(".")[0] not in MODULI_VIETATI, f"{percorso.name} importa {nome}"
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
            assert nodo.func.id not in CHIAMATE_VIETATE, f"{percorso.name} chiama {nodo.func.id}()"
