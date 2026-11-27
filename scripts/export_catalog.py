#!/usr/bin/env python3
"""Genera frontend/static/data/kpi-catalog.json a partire da src/data/kpi_catalog.py.

Uso (dalla radice del repository):
    python scripts/export_catalog.py            # scrive il file
    python scripts/export_catalog.py --check    # esce con 1 se il file non è aggiornato
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data.export_catalog import costruisci_catalogo_json  # noqa: E402

OUTPUT = ROOT / "frontend" / "static" / "data" / "kpi-catalog.json"


def serializza(catalogo):
    return json.dumps(catalogo, ensure_ascii=False, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="verifica che il JSON committato sia aggiornato")
    args = parser.parse_args()

    catalogo = costruisci_catalogo_json()
    if args.check:
        if not OUTPUT.exists() or json.loads(OUTPUT.read_text(encoding="utf-8")) != catalogo:
            print(f"{OUTPUT.relative_to(ROOT)} non è aggiornato: eseguire 'python scripts/export_catalog.py'")
            return 1
        print(f"{OUTPUT.relative_to(ROOT)} aggiornato")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serializza(catalogo), encoding="utf-8", newline="\n")
    print(f"Scritto {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
