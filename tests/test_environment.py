# tests/test_environment.py
# requirements.txt (pip, usato dalla CI) ed environment.yml (conda) devono dichiarare le stesse dipendenze.
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _nomi_requirements():
    righe = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    return {re.split(r"[<>=!~ ]", r.strip(), maxsplit=1)[0].lower() for r in righe if r.strip() and not r.startswith("#")}


def _dipendenze_conda():
    nomi = {}
    for riga in (ROOT / "environment.yml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s+- ([A-Za-z0-9_.\-]+)\s*(.*)$", riga)
        if m:
            nomi[m.group(1).lower()] = m.group(2).strip()
    return nomi


def test_dipendenze_dell_app_presenti_in_environment_yml():
    conda = _dipendenze_conda()
    mancanti = _nomi_requirements() - set(conda)
    assert not mancanti, f"in requirements.txt ma non in environment.yml: {sorted(mancanti)}"


def test_versioni_minime_allineate():
    versioni = {}
    for riga in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z0-9_.\-]+)>=([\d.]+)", riga.strip())
        if m:
            versioni[m.group(1).lower()] = m.group(2)
    conda = _dipendenze_conda()
    for nome, v in versioni.items():
        assert conda[nome] == f">={v}", f"{nome}: requirements {v} ≠ environment.yml {conda[nome]!r}"


def test_strumenti_di_test_in_environment_yml():
    conda = _dipendenze_conda()
    # playwright su conda-forge è il pacchetto Node: i binding Python si chiamano playwright-python
    assert {"pytest", "playwright-python", "nodejs"} <= set(conda)
    assert "playwright" not in conda
