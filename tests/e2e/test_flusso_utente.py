# tests/e2e/test_flusso_utente.py — interazione completa, persistenza, import/export (issue #25, #27).
import json

from .conftest import vai


def test_flusso_completo(pagina):
    p = pagina
    p.fill("#nome", "ARPA FVG"); p.fill("#anno", "2025"); p.click("text=Fascia 1")
    vai(p, "Compilazione")
    p.select_option("#v-c1", "Parziale"); p.select_option("#v-r1", "No")
    vai(p, "Dashboard")
    assert "Score globale: 7.5%" in p.inner_text(".alert")
    vai(p, "Confronto"); p.click("text=Salva l'anno 2025")
    assert "salvato nello storico" in p.inner_text(".alert")
    vai(p, "Organizzazione"); p.fill("#anno", "2026")
    vai(p, "Compilazione")
    p.select_option("#v-c1", "Sì"); p.select_option("#v-r1", "Parziale")
    p.fill("textarea[aria-label^='Note: ']", "Verbale CdA")
    vai(p, "Confronto")
    assert "(+17.5 pp)" in p.inner_text("p.fw-bold")
    assert p.locator("[aria-label=migliorato]").count() == 2
    vai(p, "Report")
    testo = p.inner_text("main")
    assert "ARPA FVG" in testo and "Verbale CdA" in testo and "fascia 1" in testo
    assert not p.errori


def test_calcolatore(pagina):
    p = pagina
    p.click("text=Fascia 1"); vai(p, "Compilazione")
    box = "details.mt-2:has(#c-r1-retr_uomini)"
    p.locator(box + " > summary").click()
    p.locator(box + " button").click()
    assert "Compila tutti i campi" in p.locator(box + " [role=status]").inner_text()
    p.fill("#c-r1-retr_uomini", "30000"); p.fill("#c-r1-retr_donne", "27000")
    p.locator(box + " button").click()
    assert p.input_value("#v-r1") == "Parziale"
    assert "10.0" in p.locator(box + " [role=status]").inner_text()


def test_persistenza_tra_sessioni(contesto, url, browser):
    p = contesto.new_page(); p.goto(url); p.wait_for_selector("h1")
    p.fill("#nome", "Ente di prova"); p.click("text=Fascia 2"); vai(p, "Compilazione")
    p.select_option("#v-c1", "Sì")
    p.close()
    p2 = contesto.new_page(); p2.goto(url); p2.wait_for_selector("h1")        # "nuova sessione", stesso browser
    assert p2.input_value("#nome") == "Ente di prova"
    vai(p2, "Compilazione"); assert p2.input_value("#v-c1") == "Sì"
    altro = browser.new_context(); p3 = altro.new_page(); p3.goto(url); p3.wait_for_selector("h1")
    assert p3.input_value("#nome") == ""                                    # un altro profilo parte vuoto
    altro.close()


def test_stato_salvato_corrotto_non_blocca_la_pagina(contesto, url):
    p = contesto.new_page(); p.goto(url)
    p.evaluate("localStorage.setItem('uni-pdr-125-kpi:stato', '{non json')")
    p.reload(); p.wait_for_selector("h1")
    assert p.input_value("#nome") == ""


def test_export_import(pagina, contesto, url, tmp_path):
    p = pagina
    p.fill("#nome", "ARPA"); p.click("text=Fascia 1"); vai(p, "Compilazione"); p.select_option("#v-c1", "Sì")
    vai(p, "Salva / carica")
    with p.expect_download() as d:
        p.click("text=Scarica JSON")
    dati = json.load(open(d.value.path(), encoding="utf-8"))
    assert dati["version"] == "2.0" and dati["kpi_values"]["c1"]["valore"] == "Sì"

    nuova = contesto.browser.new_context(); q = nuova.new_page(); q.goto(url); q.wait_for_selector("h1")
    vai(q, "Salva / carica")
    q.set_input_files("input[type=file]", d.value.path())
    q.wait_for_selector(".alert-success:has-text('File caricato')")
    vai(q, "Compilazione"); assert q.input_value("#v-c1") == "Sì"

    cattivo = tmp_path / "x.json"; cattivo.write_text(json.dumps({"azienda": {"fascia": 9}, "kpi_values": {}}))
    vai(q, "Salva / carica"); q.set_input_files("input[type=file]", str(cattivo))
    q.wait_for_selector(".alert-danger:has-text('Fascia non valida')")
    nonjson = tmp_path / "y.json"; nonjson.write_text("non è json")
    q.set_input_files("input[type=file]", str(nonjson))
    q.wait_for_selector(".alert-danger:has-text('non è un JSON valido')")
    nuova.close()


def test_navigazione_da_tastiera(pagina):
    """Tutto è raggiungibile e azionabile senza mouse (issue #9/#12): schede, fascia, valutazione."""
    p = pagina
    p.focus("button.nav-link:has-text('Organizzazione')")
    p.keyboard.press("Tab"); p.keyboard.press("Enter")                    # scheda successiva: Compilazione
    assert "Compilazione" in p.inner_text("h1")
    p.focus("button.nav-link:has-text('Organizzazione')"); p.keyboard.press("Enter")
    p.focus("button[role=radio]:has-text('Fascia 2')"); p.keyboard.press("Space")
    assert p.get_attribute("button[role=radio]:has-text('Fascia 2')", "aria-checked") == "true"
    p.focus("button.nav-link:has-text('Compilazione')"); p.keyboard.press("Enter")
    p.focus("select"); p.keyboard.press("ArrowDown")                      # cambia valutazione con la tastiera
    assert p.evaluate("document.querySelector('select').value") != "N/V"
    focus = p.evaluate("getComputedStyle(document.activeElement).outlineStyle + '|' + getComputedStyle(document.activeElement).boxShadow")
    assert focus.strip("|") not in ("", "none|none"), "indicatore di focus non visibile"
