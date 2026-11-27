# tests/test_frontend_assets.py
# Il sito pubblicato su GitHub Pages è statico: ogni risorsa referenziata deve esistere nel repository.
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"


def test_font_face_puntano_a_file_esistenti():
    css = FRONTEND / "static" / "css" / "app.css"
    urls = re.findall(r"url\('([^']+\.woff2)'\)", css.read_text(encoding="utf-8"))
    assert len(urls) >= 4, "Bootstrap Italia non dichiara gli @font-face: vanno nel nostro CSS"
    for u in urls:
        assert (css.parent / u).resolve().exists(), f"font mancante: {u}"


def test_index_html_referenzia_file_esistenti():
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    percorsi = re.findall(r'(?:href|src)="(static/[^"]+)"', html)
    assert percorsi
    for p in percorsi:
        assert (FRONTEND / p).exists(), f"risorsa mancante: {p}"


def test_percorsi_relativi_per_il_deploy_in_sottocartella():
    """Su GitHub Pages il sito vive in /uni-pdr-125-kpi/: niente percorsi assoluti."""
    for f in [FRONTEND / "index.html", *(FRONTEND / "static" / "js").glob("*.js"), FRONTEND / "static" / "css" / "app.css"]:
        testo = f.read_text(encoding="utf-8")
        assert not re.search(r"""(?:href|src)=["']/(?!/)|fetch\(["']/|url\(["']?/(?!/)""", testo), f"percorso assoluto in {f.name}"


def test_workflow_ci_pubblica_solo_da_main():
    w = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "refs/heads/main" in w and "deploy-pages" in w and "pages: write" in w
