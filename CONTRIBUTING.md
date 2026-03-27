# Guida alla Contribuzione

Grazie per l'interesse nel contribuire a questo progetto! Questo documento fornisce le linee guida per partecipare allo sviluppo dello **Strumento KPI UNI/PdR 125:2022**.

## Come contribuire

Le contribuzioni possono assumere diverse forme:

- **Bug report** — Segnalazione di problemi riscontrati
- **Bug fix** — Risoluzione di difetti nel codice
- **Miglioramenti** — Nuove funzionalità o ottimizzazioni
- **Traduzioni** — Localizzazione in altre lingue
- **Documentazione** — Miglioramento della documentazione

## Processo di contribuzione

### 1. Preparazione

1. **Fork il repository** su GitHub
2. **Clona il fork** localmente:
   ```bash
   git clone https://github.com/TUO_UTENTE/uni-pdr-125-kpi.git
   cd uni-pdr-125-kpi
   ```
3. **Configura il remote upstream**:
   ```bash
   git remote add upstream https://github.com/jobonaf/uni-pdr-125-kpi.git
   ```

### 2. Creazione del branch

Crea un branch descrittivo per la tua contribuzione:

```bash
# Per bugfix
git checkout -b fix/descrizione-bug

# Per nuove funzionalità
git checkout -b feature/descrizione-feature

# Per documentazione
git checkout -b docs/descrizione-doc
```

### 3. Sviluppo

### 4. Testing

### 5. Commit

Scrivi messaggi di commit chiari e descrittivi in italiano:

```bash
# ✓ Buono
git commit -m "fix: correggi calcolo dello score ponderato"
git commit -m "feat: aggiungi export in CSV"
git commit -m "docs: aggiorna README con istruzioni installazione"

# ✗ Evita
git commit -m "aggiustamenti"
git commit -m "fix vari"
```

### 6. Push e Pull Request

```bash
# Sincronizza con upstream
git fetch upstream
git rebase upstream/main

# Push al tuo fork
git push origin TUO_BRANCH

# Crea Pull Request su GitHub
```

**Nel PR includi:**
- Descrizione chiara della modifica
- Riferimento a issue correlate (es. `Closes #123`)
- Screenshot o GIF per cambiamenti visivi
- Checklist di verifica

## Standard di codice

### Naming conventions

### Struttura del progetto

### Commenti

Documenta il codice in italiano:

## Licenza

Contribuendo a questo progetto, accetti che le tue contribuzioni siano distribuite sotto licenza **EUPL-1.2**. Vedi [LICENSE](LICENSE) per dettagli.

## Linee guida per la segnalazione di bug

### Prima di segnalare

1. Verifica che il bug non sia già stato segnalato
2. Assicurati di aver utilizzato l'ultima versione
3. Raccogli informazioni di sistema (browser, versione)

### Contenuto della segnalazione

```markdown
## Titolo
[Descrizione breve del bug]

## Descrizione
[Descrizione dettagliata del problema]

## Passi per riprodurre
1. [Primo passo]
2. [Secondo passo]
...

## Risultato osservato
[Cosa succede attualmente]

## Risultato atteso
[Cosa dovrebbe succedere]

## Informazioni di sistema
- Browser: [es. Chrome 120]
- SO: [es. Windows 11, macOS 14]
- Versione app: [es. 2.0.0]
```

## Richieste di funzionalità

Proposte per nuove funzionalità sono benvenute! Per segnalare:

1. Apri una Issue su GitHub
2. Descrivi il caso d'uso
3. Spiega come la funzionalità aiuterebbe gli utenti
4. Indica la priorità (bassa, media, alta)

## Comunicazione

- **Dubbi sulla contribuzione?** → Apri una Issue per discutere
- **Discussioni generali** → Usa GitHub Discussions
- **Contatti diretti** → giovanni.bonafe@arpa.fvg.it

## Riconoscimenti

I contributori saranno riconosciuti nel file [AUTHORS.md](AUTHORS.md) e nei release notes.

---

Grazie per il tuo contributo! 🎉
