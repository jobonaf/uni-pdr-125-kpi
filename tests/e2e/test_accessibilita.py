# tests/e2e/test_accessibilita.py — scansione automatica WCAG 2.1 AA con axe-core (issue #9, #10, #12, #27)
# e controllo di responsività (nessuno scorrimento orizzontale) a larghezze di mobile, tablet e desktop.
import pathlib

import pytest

from .conftest import VISTE, vai

AXE = pathlib.Path(__file__).parent / "vendor" / "axe.min.js"
TAG = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]


def _prepara(p):
    """Stato con dati reali, perché alcune viste sono vuote senza storico."""
    p.fill("#nome", "ARPA FVG"); p.click("text=Fascia 1"); vai(p, "Compilazione")
    p.select_option("#v-c1", "Sì"); p.select_option("#v-r1", "Parziale")
    vai(p, "Confronto"); p.click("text=Salva l'anno")
    vai(p, "Compilazione"); p.select_option("#v-c1", "Parziale")


@pytest.mark.parametrize("vista", VISTE)
def test_nessuna_violazione_axe(pagina, vista):
    pagina.add_script_tag(path=str(AXE))
    _prepara(pagina); vai(pagina, vista)
    r = pagina.evaluate("tag => axe.run(document, { runOnly: { type: 'tag', values: tag } })", TAG)
    assert not r["violations"], "\n".join(
        f"[{v['impact']}] {v['id']}: {v['help']} — {[n['target'] for n in v['nodes']][:3]}" for v in r["violations"])


@pytest.mark.parametrize("larghezza", [360, 390, 768, 1280])
@pytest.mark.parametrize("vista", VISTE)
def test_nessuno_scorrimento_orizzontale(browser, url, vista, larghezza):
    ctx = browser.new_context(viewport={"width": larghezza, "height": 800}); p = ctx.new_page(); p.goto(url); p.wait_for_selector("h1")
    _prepara(p); vai(p, vista)
    assert not p.evaluate("document.documentElement.scrollWidth > innerWidth"), f"{vista} a {larghezza}px"
    ctx.close()
