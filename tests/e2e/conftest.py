# tests/e2e/conftest.py — test end-to-end del frontend statico in un browser reale (Chromium).
# Richiedono: pip install playwright && python -m playwright install chromium
# Se Playwright o il browser mancano i test vengono saltati (in CI girano sempre).
import functools
import http.server
import pathlib
import threading

import os

import pytest

# In CI (E2E_OBBLIGATORI=1) l'assenza di Playwright o del browser è un errore, non un "skip".
OBBLIGATORI = bool(os.environ.get("E2E_OBBLIGATORI"))
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    if OBBLIGATORI:
        raise
    pytest.skip("Playwright non installato", allow_module_level=True)

FRONTEND = pathlib.Path(__file__).resolve().parents[2] / "frontend"
VISTE = ["Organizzazione", "Compilazione", "Dashboard", "Confronto", "Report", "Salva / carica"]


@pytest.fixture(scope="session")
def url():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(FRONTEND))
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}/index.html"
    server.shutdown()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as e:  # browser non installato
            if OBBLIGATORI:
                raise
            pytest.skip(f"Chromium non disponibile: {str(e)[:80]}")
        yield b
        b.close()


@pytest.fixture
def contesto(browser):
    c = browser.new_context(viewport={"width": 1024, "height": 800}, accept_downloads=True)
    yield c
    c.close()


@pytest.fixture
def pagina(contesto, url):
    p = contesto.new_page()
    p.errori = []
    p.on("pageerror", lambda e: p.errori.append(str(e)))
    p.on("console", lambda m: m.type == "error" and p.errori.append(m.text))
    p.on("response", lambda r: r.status >= 400 and p.errori.append(f"{r.status} {r.url}"))
    p.goto(url)
    p.wait_for_selector("h1")
    return p


def vai(pagina, nome):
    pagina.click(f"button.nav-link:has-text('{nome}')")
    pagina.wait_for_selector("h1")
