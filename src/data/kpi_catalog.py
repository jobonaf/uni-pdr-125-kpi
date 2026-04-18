# src/data/kpi_catalog.py
# Dati strutturali: AREE, CLUSTER, KPI_DA_RENDICONTARE_PER_FASCIA, CALCOLATORI_KPI

# =============================================================================
# DATI STRUTTURALI — UNI/PdR 125:2022
# =============================================================================

AREE = [
    {
        "id": "cultura",
        "nome": "Cultura e Strategia",
        "peso": 15,
        "colore": "#1a5f7a",
        "icona": "🧭",
        "descrizione": "Misura la coerenza dei valori, della visione e degli obiettivi di inclusione dell'organizzazione con le politiche dichiarate e i comportamenti concreti.",
        "kpi": [
            {
                "id": "c1", "punti": 20, "tipo": "qualitativo",
                "testo": "Piano strategico formalizzato e implementato",
                "descrizione": "L'organizzazione ha adottato un piano strategico formale che favorisce e sostiene lo sviluppo di un ambiente di lavoro inclusivo, con valori aziendali esplicitamente coerenti con una cultura della parità.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "c2", "punti": 10, "tipo": "qualitativo",
                "testo": "Procedure interne per espressione anonima di opinioni",
                "descrizione": "Esistono strumenti concreti che consentono a tutto il personale di esprimere opinioni e suggerimenti in modo anonimo.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "c3", "punti": 20, "tipo": "qualitativo",
                "testo": "Comunicazione interna e sensibilizzazione sul linguaggio inclusivo",
                "descrizione": "Nell'ultimo anno sono state realizzate iniziative sistematiche di comunicazione interna che promuovono comportamenti e un linguaggio capace di garantire un ambiente di lavoro inclusivo.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "c4", "punti": 10, "tipo": "qualitativo",
                "testo": "Politiche per rappresentanza di genere in eventi e panel",
                "descrizione": "Esistono policy esplicite che garantiscono la rappresentanza equa dei generi tra i relatori di eventi aziendali.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "c5", "punti": 10, "tipo": "qualitativo",
                "testo": "Formazione su genere, stereotipi e unconscious bias (ultimo biennio)",
                "descrizione": "Nell'ultimo biennio sono stati realizzati interventi formativi specifici su differenza di genere, stereotipi e bias inconsci.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "c6", "punti": 20, "tipo": "qualitativo",
                "testo": "Survey sulla percezione delle pari opportunità (ultimo anno)",
                "descrizione": "Nell'ultimo anno è stata condotta almeno un'indagine strutturata per rilevare la percezione dei dipendenti sulle pari opportunità.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "c7", "punti": 10, "tipo": "qualitativo",
                "testo": "Promozione delle pari opportunità verso stakeholder esterni (ultimo biennio)",
                "descrizione": "Nell'ultimo biennio l'organizzazione ha realizzato iniziative verso l'esterno su temi di inclusione e parità.",
                "fasceRichieste": [3, 4]
            },
        ]
    },
    {
        "id": "governance",
        "nome": "Governance",
        "peso": 15,
        "colore": "#2d8a6e",
        "icona": "🏛️",
        "descrizione": "Verifica la presenza di presidi organizzativi formali, responsabilità assegnate e risorse allocate per la gestione delle tematiche di genere.",
        "kpi": [
            {
                "id": "g1", "punti": 25, "tipo": "qualitativo",
                "testo": "Presidio organizzativo dedicato all'inclusione e parità di genere",
                "descrizione": "Esiste nella struttura organizzativa un presidio specifico con mandato esplicito sulla gestione e il monitoraggio delle tematiche di inclusione e parità.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "g2", "punti": 25, "tipo": "qualitativo",
                "testo": "Processi per gestire episodi di non inclusività",
                "descrizione": "Sono definiti e operativi processi documentati per ricevere, istruire e risolvere segnalazioni di discriminazione.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "g3", "punti": 15, "tipo": "qualitativo",
                "testo": "Budget dedicato alle iniziative di inclusione e parità",
                "descrizione": "È presente una voce di bilancio dedicata esplicitamente a iniziative per l'inclusione e la parità di genere.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "g4", "punti": 15, "tipo": "qualitativo",
                "testo": "Obiettivi di parità di genere inseriti nella valutazione del management",
                "descrizione": "I vertici e il management hanno obiettivi specifici e misurabili legati alla parità di genere inseriti nel sistema di valutazione della performance.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "g5", "punti": 20, "tipo": "quantitativo",
                "testo": "Quota del genere meno rappresentato nel CdA/organo di controllo ≥ 1/3",
                "descrizione": "Il genere meno rappresentato deve costituire almeno 1/3 della composizione complessiva del consiglio di amministrazione.",
                "fasceRichieste": [2, 3, 4],
                "soglia": "≥ 1/3 composizione CdA"
            },
        ]
    },
    {
        "id": "hr",
        "nome": "Processi HR",
        "peso": 10,
        "colore": "#5b7fa6",
        "icona": "👥",
        "descrizione": "Valuta la neutralità rispetto al genere dei principali processi di gestione del personale lungo tutto il ciclo di vita lavorativo.",
        "kpi": [
            {
                "id": "h1", "punti": 25, "tipo": "qualitativo",
                "testo": "Processi HR neutrali rispetto al genere (selezione, contratto, on-boarding, valutazione)",
                "descrizione": "I processi chiave del ciclo HR sono documentati e prevedono esplicite misure anti-discriminatorie.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "h2", "punti": 15, "tipo": "qualitativo",
                "testo": "Analisi del turnover disaggregata per genere",
                "descrizione": "L'organizzazione raccoglie e analizza regolarmente i dati di turnover disaggregati per genere.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "h3", "punti": 15, "tipo": "qualitativo",
                "testo": "Accesso equo a formazione e percorsi di valorizzazione",
                "descrizione": "Esistono policy che garantiscono la partecipazione equa e paritaria di uomini e donne a tutti i percorsi formativi.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "h4", "punti": 20, "tipo": "qualitativo",
                "testo": "Politiche di mobilità interna e piani di successione inclusivi",
                "descrizione": "I processi di mobilità interna e i piani di successione sono strutturati in modo da garantire pari opportunità.",
                "fasceRichieste": [2, 3, 4]
            },
            {
                "id": "h5", "punti": 15, "tipo": "qualitativo",
                "testo": "Protezione del ruolo e della retribuzione nel post-maternità",
                "descrizione": "Esistono procedure documentate che garantiscono al dipendente che rientra da un congedo di maternità di ritrovare la stessa posizione o una equivalente.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "h6", "punti": 10, "tipo": "qualitativo",
                "testo": "Referente aziendale e prassi a tutela da molestie e mobbing",
                "descrizione": "È presente almeno una figura referente con mandato esplicito sulla tutela dei dipendenti da molestie e mobbing.",
                "fasceRichieste": [1, 2, 3, 4]
            },
        ]
    },
    {
        "id": "crescita",
        "nome": "Opportunità di Crescita",
        "peso": 20,
        "colore": "#7b5ea7",
        "icona": "📈",
        "descrizione": "Misura l'effettivo accesso neutrale rispetto al genere ai percorsi di carriera e di crescita professionale.",
        "kpi": [
            {
                "id": "oc1", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne sull'organico totale — fascia 1-2 (confronto biennale)",
                "descrizione": "La percentuale di donne sull'organico totale deve crescere di almeno +10 punti percentuali rispetto al biennio precedente.",
                "fasceRichieste": [1, 2],
                "soglia": "+10pp vs biennio precedente → parità"
            },
            {
                "id": "oc2", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne sull'organico totale vs benchmark industry — fascia 3-4",
                "descrizione": "La percentuale di donne sull'organico deve essere almeno +10 punti percentuali superiore alla media del settore di appartenenza.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs media ATECO industry"
            },
            {
                "id": "oc3", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne dirigenti — fascia 2 (confronto biennale)",
                "descrizione": "La percentuale di donne con qualifica dirigenziale deve crescere di almeno +10 punti percentuali rispetto al biennio precedente.",
                "fasceRichieste": [2],
                "soglia": "+10pp vs biennio precedente"
            },
            {
                "id": "oc4", "punti": 25, "tipo": "quantitativo",
                "testo": "% donne dirigenti vs benchmark industry — fascia 3-4",
                "descrizione": "La percentuale di donne con qualifica di dirigente deve essere almeno +10pp superiore alla media dell'industry.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs media ATECO industry"
            },
            {
                "id": "oc5", "punti": 20, "tipo": "quantitativo",
                "testo": "% donne responsabili di unità organizzative ≥ 40%",
                "descrizione": "La percentuale di donne tra i responsabili di unità organizzative deve essere almeno pari al 40%.",
                "fasceRichieste": [2, 3, 4],
                "soglia": "≥ 40% del totale responsabili"
            },
            {
                "id": "oc6", "punti": 20, "tipo": "quantitativo",
                "testo": "% donne nella prima linea di riporto al Vertice",
                "descrizione": "La percentuale di donne nei ruoli di riporto diretto al CEO deve essere almeno +10pp superiore alla percentuale media di dirigenti donne.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs % dirigenti femminili industry"
            },
            {
                "id": "oc7", "punti": 10, "tipo": "quantitativo",
                "testo": "% donne con delega su budget di spesa/investimento",
                "descrizione": "La percentuale di donne con delega formale su budget deve essere almeno +10pp superiore alla % media di dirigenti donne.",
                "fasceRichieste": [3, 4],
                "soglia": "+10pp vs % dirigenti femminili industry"
            },
        ]
    },
    {
        "id": "retribuzione",
        "nome": "Equità Remunerativa",
        "peso": 20,
        "colore": "#c4622d",
        "icona": "⚖️",
        "descrizione": "Misura il differenziale retributivo tra generi in logica di total reward.",
        "kpi": [
            {
                "id": "r1", "punti": 40, "tipo": "quantitativo",
                "testo": "Gap retributivo per stesso livello e mansione < 10%",
                "descrizione": "La differenza tra la retribuzione media lorda annua di uomini e donne a parità di livello deve essere inferiore al 10%.",
                "fasceRichieste": [1, 2, 3, 4],
                "soglia": "Gap < 10% e decrescente nel tempo"
            },
            {
                "id": "r2", "punti": 30, "tipo": "quantitativo",
                "testo": "Parità nel tasso di promozione annuale per genere",
                "descrizione": "La percentuale di donne promosse deve essere uguale alla percentuale di uomini promossi.",
                "fasceRichieste": [3, 4],
                "soglia": "Tasso promozione F = Tasso promozione M per livello"
            },
            {
                "id": "r3", "punti": 30, "tipo": "quantitativo",
                "testo": "Accesso paritario alla remunerazione variabile",
                "descrizione": "La percentuale di donne che ricevono remunerazione variabile deve essere uguale alla percentuale di uomini.",
                "fasceRichieste": [3, 4],
                "soglia": "% accesso variabile F = % accesso variabile M"
            },
        ]
    },
    {
        "id": "genitorialita",
        "nome": "Tutela Genitorialità",
        "peso": 20,
        "colore": "#b8873f",
        "icona": "🌱",
        "descrizione": "Valuta la presenza di politiche a sostegno della genitorialità in tutte le sue forme.",
        "kpi": [
            {
                "id": "ge1", "punti": 20, "tipo": "qualitativo",
                "testo": "Servizi dedicati al rientro post maternità/paternità",
                "descrizione": "Esistono servizi strutturati per il rientro al lavoro dopo un congedo di maternità o paternità.",
                "fasceRichieste": [3, 4]
            },
            {
                "id": "ge2", "punti": 35, "tipo": "qualitativo",
                "testo": "Policy oltre CCNL per maternità/paternità e conciliazione vita-lavoro",
                "descrizione": "L'organizzazione ha adottato policy che vanno oltre quanto previsto dal CCNL.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "ge3", "punti": 25, "tipo": "qualitativo",
                "testo": "Policy per valorizzare la genitorialità come acquisizione di competenze",
                "descrizione": "Esistono policy esplicite che riconoscono e valorizzano la genitorialità come momento di acquisizione di nuove competenze.",
                "fasceRichieste": [1, 2, 3, 4]
            },
            {
                "id": "ge4", "punti": 10, "tipo": "quantitativo",
                "testo": "Tasso di fruizione effettiva dei congedi di paternità obbligatori",
                "descrizione": "Rapporto tra il numero di padri che hanno fruito del congedo di paternità obbligatorio e il totale dei padri potenzialmente beneficiari.",
                "fasceRichieste": [3, 4],
                "soglia": "→ 100% fruizione"
            },
            {
                "id": "ge5", "punti": 10, "tipo": "quantitativo",
                "testo": "Tasso di fruizione dei giorni di congedo di paternità previsti dalla legge",
                "descrizione": "Rapporto tra i giorni medi di congedo di paternità effettivamente fruiti e il totale dei giorni potenziali.",
                "fasceRichieste": [3, 4],
                "soglia": "→ 100% giorni fruiti"
            },
        ]
    }
]

CLUSTER = [
    {"id": 1, "nome": "Micro", "range": "1–9 addetti", "emoji": "🔹"},
    {"id": 2, "nome": "Piccola", "range": "10–49 addetti", "emoji": "🔷"},
    {"id": 3, "nome": "Media", "range": "50–249 addetti", "emoji": "🔶"},
    {"id": 4, "nome": "Grande", "range": "≥ 250 addetti", "emoji": "🟠"},
]

# KPI che le organizzazioni di fascia 1 e 2 devono obbligatoriamente
# misurare e rendicontare (non necessariamente con esito positivo).
# Fonte: UNI/PdR 125:2022, Prospetti 3-8, clausole "è considerato necessario".
# NB: per fascia 3 e 4 si applicano tutti gli indicatori (nessuna
# semplificazione), ma non esiste alcun KPI il cui esito negativo blocchi
# individualmente la certificazione: conta solo lo score globale >= 60%.
# Cfr. UNI/PdR 125:2022, §5.1.
KPI_DA_RENDICONTARE_PER_FASCIA = {
    # Area Cultura e Strategia (Prospetto 3)
    "c1": [1, 2],   # Piano strategico formalizzato
    "c3": [2],      # Comunicazione interna e linguaggio inclusivo
    "c5": [2],      # Formazione su genere e bias

    # Area Governance (Prospetto 4)
    "g1": [1, 2],   # Presidio organizzativo dedicato
    "g2": [2],      # Processi per gestire episodi di non inclusività

    # Area Processi HR (Prospetto 5)
    "h1": [1, 2],   # Processi HR neutrali rispetto al genere
    "h4": [2],      # Mobilità interna e piani di successione inclusivi
    "h6": [1, 2],   # Referente aziendale per molestie e mobbing

    # Area Opportunità di Crescita (Prospetto 6)
    "oc1": [1, 2],  # % donne sull’organico totale (confronto biennale)
    "oc3": [2],     # % donne dirigenti (confronto biennale)

    # Area Equità Remunerativa (Prospetto 7)
    "r1": [1, 2],   # Gap retributivo < 10%

    # Area Tutela Genitorialità (Prospetto 8)
    "ge2": [1, 2],  # Policy oltre CCNL per genitorialità e conciliazione
    "ge3": [1, 2],  # Valorizzazione genitorialità come acquisizione competenze
}

# =============================================================================
# CALCOLATORI PER KPI QUANTITATIVI
# =============================================================================

CALCOLATORI_KPI = {
    "oc1": {
        "label": "Calcola Δ percentuale donne sull'organico (biennale)",
        "inputs": [
            {"name": "perc_donne_corrente", "label": "% donne anno corrente", "type": "float", "min": 0.0, "max": 100.0},
            {"name": "perc_donne_precedente", "label": "% donne biennio precedente", "type": "float", "min": 0.0, "max": 100.0}
        ],
        "formula": lambda inputs: inputs["perc_donne_corrente"] - inputs["perc_donne_precedente"],
        "soglia": 10,
        "valutazione": lambda val: "Sì" if val >= 10 else "Parziale" if val >= 5 else "No"
    },
    "oc3": {
        "label": "Calcola Δ percentuale donne dirigenti (biennale)",
        "inputs": [
            {"name": "perc_dir_corrente", "label": "% donne dirigenti anno corrente", "type": "float", "min": 0.0, "max": 100.0},
            {"name": "perc_dir_precedente", "label": "% donne dirigenti biennio precedente", "type": "float", "min": 0.0, "max": 100.0}
        ],
        "formula": lambda inputs: inputs["perc_dir_corrente"] - inputs["perc_dir_precedente"],
        "soglia": 10,
        "valutazione": lambda val: "Sì" if val >= 10 else "Parziale" if val >= 5 else "No"
    },
    "oc5": {
        "label": "Calcola % donne responsabili di unità organizzative",
        "inputs": [
            {"name": "donne_responsabili", "label": "Numero donne responsabili", "type": "int", "min": 0},
            {"name": "totale_responsabili", "label": "Numero totale responsabili", "type": "int", "min": 1}
        ],
        "formula": lambda inputs: (inputs["donne_responsabili"] / inputs["totale_responsabili"]) * 100,
        "soglia": 40,
        "valutazione": lambda val: "Sì" if val >= 40 else "Parziale" if val >= 30 else "No"
    },
    "r1": {
        "label": "Calcola gap retributivo per stesso livello/mansione",
        "inputs": [
            {"name": "retr_uomini", "label": "Retribuzione media annua lorda uomini (€)", "type": "float", "min": 0.0},
            {"name": "retr_donne", "label": "Retribuzione media annua lorda donne (€)", "type": "float", "min": 0.0}
        ],
        "formula": lambda inputs: (inputs["retr_uomini"] - inputs["retr_donne"]) / inputs["retr_uomini"] * 100 if inputs["retr_uomini"] > 0 else 0,
        "soglia": 10,
        "valutazione": lambda val: "Sì" if val < 10 else "Parziale" if val < 15 else "No"
    },
    "ge4": {
        "label": "Calcola tasso di fruizione congedi di paternità obbligatori",
        "inputs": [
            {"name": "padri_fruitori", "label": "Numero padri che hanno fruito del congedo", "type": "int", "min": 0},
            {"name": "padri_potenziali", "label": "Numero totale padri potenziali", "type": "int", "min": 1}
        ],
        "formula": lambda inputs: (inputs["padri_fruitori"] / inputs["padri_potenziali"]) * 100,
        "soglia": 100,
        "valutazione": lambda val: "Sì" if val >= 100 else "Parziale" if val >= 80 else "No"
    },
    "ge5": {
        "label": "Calcola tasso di fruizione giorni di congedo di paternità",
        "inputs": [
            {"name": "giorni_fruiti", "label": "Giorni medi fruiti per padre", "type": "float", "min": 0.0},
            {"name": "giorni_legge", "label": "Giorni previsti dalla legge", "type": "float", "min": 1.0}
        ],
        "formula": lambda inputs: (inputs["giorni_fruiti"] / inputs["giorni_legge"]) * 100,
        "soglia": 100,
        "valutazione": lambda val: "Sì" if val >= 100 else "Parziale" if val >= 80 else "No"
    },
}
