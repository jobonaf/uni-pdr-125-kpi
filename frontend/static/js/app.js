// frontend/static/js/app.js — interfaccia (DOM). La logica è in scoring.js e stato.js.
import { calcolaScoreGlobale, calcolaKpiNonCompilati, kpiApplicabile, certificabile } from "./scoring.js";
import { calcolaKpi } from "./calcolatori.js";
import { statoIniziale, creaExport, validaImport } from "./stato.js";

const CHIAVE = "uni-pdr-125-kpi:stato";
const VISTE = { org: "Organizzazione", comp: "Compilazione", dash: "Dashboard", dati: "Salva / carica" };
let catalogo, stato, vista = "org", messaggio = null;

const el = (tag, attrs = {}, ...figli) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) e.setAttribute(k, v);
  }
  e.append(...figli.flat().filter((f) => f != null));   // append(testo) = textContent: nessun HTML dai dati
  return e;
};

function salva() { try { localStorage.setItem(CHIAVE, JSON.stringify(stato)); } catch { /* storage non disponibile */ } }
function ripristina() {
  try {
    const grezzo = localStorage.getItem(CHIAVE);
    const r = grezzo && validaImport(catalogo, JSON.parse(grezzo));
    return r && r.ok ? r.stato : null;
  } catch { return null; }
}

function renderTabs() {
  const ul = document.getElementById("tabs");
  ul.replaceChildren(...Object.entries(VISTE).map(([id, nome]) => el("li", { class: "nav-item" },
    el("button", { class: "nav-link" + (id === vista ? " active" : ""), type: "button",
      "aria-current": id === vista ? "page" : false, onclick: () => { vista = id; messaggio = null; render(); } }, nome))));
}

function vistaOrg() {
  const a = stato.azienda;
  const campo = (id, etichetta, tipo, chiave) => el("div", { class: "col-md-4 mb-3" },
    el("label", { for: id, class: "form-label" }, etichetta),
    el("input", { id, type: tipo, class: "form-control", value: a[chiave],
      oninput: (e) => { a[chiave] = tipo === "number" ? Number(e.target.value) : e.target.value; salva(); } }));
  return el("section", {},
    el("h1", { class: "h3" }, "Organizzazione"),
    el("div", { class: "row" }, campo("nome", "Nome", "text", "nome"), campo("settore", "Settore", "text", "settore"), campo("anno", "Anno", "number", "anno")),
    el("h2", { class: "h5 mt-3" }, "Fascia dimensionale"),
    el("div", { class: "row", role: "radiogroup", "aria-label": "Fascia dimensionale" }, catalogo.cluster.map((c) =>
      el("div", { class: "col-6 col-lg-3 mb-3" },
        el("button", { type: "button", role: "radio", "aria-checked": String(a.fascia === c.id),
          class: "card card-body w-100 text-start fascia-card" + (a.fascia === c.id ? " selected" : ""),
          onclick: () => { a.fascia = c.id; salva(); render(); } },
          el("strong", {}, `${c.emoji} Fascia ${c.id} — ${c.nome}`), el("span", {}, c.range)))))
  );
}

function calcolatore(k, v) {
  const cfg = catalogo.calcolatori[k.id];
  if (!cfg) return null;
  const dati = () => stato.calc_data[k.id] ?? {};   // la voce si crea solo quando l'utente scrive
  const esito = el("div", { class: "small mt-2", role: "status" });
  const campi = cfg.inputs.map((i) => el("div", { class: "mb-2" },
    el("label", { for: `c-${k.id}-${i.name}`, class: "form-label small" }, i.label),
    el("input", { id: `c-${k.id}-${i.name}`, type: "number", class: "form-control w-auto", value: dati()[i.name] ?? "",
      step: i.type === "int" ? "1" : "any", min: i.min, max: i.max,
      oninput: (e) => {
        const d = (stato.calc_data[k.id] ??= {});
        if (e.target.value === "") delete d[i.name]; else d[i.name] = Number(e.target.value);
        if (!Object.keys(d).length) delete stato.calc_data[k.id];
        salva();
      } })));
  const applica = () => {
    const r = calcolaKpi(catalogo, k.id, dati());
    if (!r) { esito.textContent = "Compila tutti i campi con valori validi (i totali devono essere maggiori di zero)."; return; }
    v.valore = r.valutazione; v.percentuale = r.valore.toFixed(1); salva();
    document.getElementById(`v-${k.id}`).value = r.valutazione;
    esito.textContent = `Valore calcolato: ${v.percentuale} → ${r.valutazione}`;
  };
  return el("details", { class: "mt-2" }, el("summary", { class: "small" }, "Calcolatore"),
    el("p", { class: "small fw-bold mt-2 mb-2" }, cfg.label), campi,
    el("button", { class: "btn btn-sm btn-outline-primary", type: "button", onclick: applica }, "Calcola e imposta valutazione"), esito);
}

function vistaComp() {
  const fascia = stato.azienda.fascia;
  return el("section", {}, el("h1", { class: "h3" }, `Compilazione KPI — fascia ${fascia}`),
    catalogo.aree.map((area) => {
      const kpi = area.kpi.filter((k) => kpiApplicabile(k, fascia));
      if (!kpi.length) return null;
      return el("details", { class: "mb-3", open: "" },
        el("summary", { class: "h5" }, `${area.icona} ${area.nome} (peso ${area.peso}%)`),
        el("p", { class: "text-muted" }, area.descrizione),
        kpi.map((k) => {
          const v = stato.kpi_values[k.id];
          return el("div", { class: "kpi" },
            el("label", { for: `v-${k.id}`, class: "fw-bold d-block" }, k.testo),
            el("div", { class: "small text-muted" }, `${k.tipo} · ${k.punti} pt` + (k.soglia ? ` · soglia: ${k.soglia}` : "")),
            el("select", { id: `v-${k.id}`, class: "form-select w-auto mt-2",
              onchange: (e) => { v.valore = e.target.value; salva(); } },
              catalogo.scoring.valutazioni.map((o) => el("option", { value: o, selected: o === v.valore }, o))),
            calcolatore(k, v),
            el("details", { class: "mt-2" }, el("summary", { class: "small" }, "Descrizione estesa"), el("p", {}, k.descrizione)));
        }));
    }));
}

function vistaDash() {
  const { scoreGlobale, areeDetails } = calcolaScoreGlobale(catalogo, stato.kpi_values, stato.azienda.fascia);
  const ok = certificabile(catalogo, scoreGlobale);
  const nc = calcolaKpiNonCompilati(catalogo, stato.kpi_values, stato.azienda.fascia).length;
  return el("section", {}, el("h1", { class: "h3" }, "Dashboard"),
    el("div", { class: "alert " + (ok ? "alert-success" : "alert-warning"), role: "status" },
      `Score globale: ${scoreGlobale.toFixed(1)}% — ` + (ok
        ? `soglia di certificazione (${catalogo.scoring.sogliaCertificazione}%) raggiunta`
        : `mancano ${(catalogo.scoring.sogliaCertificazione - scoreGlobale).toFixed(1)} punti alla soglia del ${catalogo.scoring.sogliaCertificazione}%`)),
    nc ? el("p", {}, `📋 ${nc} KPI da rendicontare non ancora compilati.`) : null,
    areeDetails.filter((a) => a.totale > 0).map((a) => el("div", { class: "mb-3" },
      el("div", {}, `${a.icona} ${a.nome}: ${a.score.toFixed(1)}% (${a.completati}/${a.totale} KPI compilati, contributo ${a.contributo.toFixed(1)} su ${a.peso})`),
      el("div", { class: "barra", role: "img", "aria-label": `${a.nome} ${a.score.toFixed(0)}%` },
        el("span", { style: `width:${a.score}%;background:${a.colore}` })))),
    el("button", { class: "btn btn-outline-primary no-print", type: "button", onclick: () => window.print() }, "Stampa"));
}

function vistaDati() {
  const scarica = () => {
    const blob = new Blob([JSON.stringify(creaExport(catalogo, stato), null, 2)], { type: "application/json" });
    const a = el("a", { href: URL.createObjectURL(blob), download: `uni-pdr-125_${stato.azienda.nome || "org"}_${stato.azienda.anno}.json` });
    a.click(); URL.revokeObjectURL(a.href);
  };
  const carica = async (e) => {
    const file = e.target.files[0]; if (!file) return;
    try {
      const r = validaImport(catalogo, JSON.parse(await file.text()));
      if (r.ok) { stato = r.stato; salva(); }
      messaggio = r.ok ? { tipo: "success", testo: "File caricato." + (r.avvisi.length ? " " + r.avvisi.join(" ") : "") } : { tipo: "danger", testo: r.errori.join(" ") };
    } catch { messaggio = { tipo: "danger", testo: "Il file non è un JSON valido." }; }
    render();
  };
  return el("section", {}, el("h1", { class: "h3" }, "Salva / carica"),
    el("p", {}, "I dati restano nel tuo browser. Il file JSON è compatibile con quello dell'app Streamlit."),
    messaggio ? el("div", { class: `alert alert-${messaggio.tipo}`, role: "alert" }, messaggio.testo) : null,
    el("button", { class: "btn btn-primary me-2", type: "button", onclick: scarica }, "Scarica JSON"),
    el("label", { class: "btn btn-outline-primary mb-0" }, "Carica JSON", el("input", { type: "file", accept: "application/json", hidden: "", onchange: carica })),
    el("button", { class: "btn btn-outline-danger ms-2", type: "button",
      onclick: () => { if (confirm("Azzerare tutti i dati?")) { stato = statoIniziale(catalogo); salva(); render(); } } }, "Azzera"));
}

function render() {
  renderTabs();
  document.getElementById("main").replaceChildren({ org: vistaOrg, comp: vistaComp, dash: vistaDash, dati: vistaDati }[vista]());
}

try {
  catalogo = await (await fetch("static/data/kpi-catalog.json")).json();
  stato = ripristina() ?? statoIniziale(catalogo);
  render();
} catch (e) {
  document.getElementById("main").textContent = "Impossibile caricare il catalogo. Se apri il file direttamente, avvia un server locale: python -m http.server -d frontend";
}
