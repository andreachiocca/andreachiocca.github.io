# Roadmap: andreachiocca.github.io

Data: 4 novembre 2026. Deriva da `docs/site-audit.md` (codici Q/M/R) e dalle scelte dell'autore:

- **mantenere lo stile attuale** (registro tecnico: FIG. NN, indici `01 /`, figure su griglia) e unirlo a un **minimalismo caldo**: carta avorio, inchiostro quasi nero, un solo accento caldo, titoli serif, molto spazio bianco;
- **molti visual, minimal, con animazioni leggere**;
- **preferire figure generate dai codici originali** (`multiaxial-fatigue`, `sharCP`, `SeAn-CP`, ...) rispetto alle illustrazioni;
- `sharCP` **va aggiunto** al catalogo, `FatPy` **resta escluso**.

Regole valide per ogni step:

- una PR per step, con screenshot prima/dopo (390 e 1440 px, chiaro e scuro), build e verificatori verdi e test aggiunti per ciò che cambia;
- nessuna modifica a URL, contenuti scientifici o dati pubblicati senza conferma;
- ogni figura generata dal codice riporta in didascalia la **provenienza**: repository@commit, funzione e caso di carico. I dati sperimentali e le illustrazioni restano distinti;
- animazioni solo con `transform`/`opacity`, durata ≤ 400 ms per gli ingressi, sempre disattivate con `prefers-reduced-motion`. Nessuna animazione è necessaria per capire il contenuto.

---

## Step 0: sbloccare la CI (fatto in questa PR)

Le PR aperte falliscono il check *Generated site verification* per una causa comune: `bundle-audit` ha iniziato a segnalare advisory nuovi su `addressable 2.9.0`, e da oggi anche su `activesupport`, `loofah` e `nokogiri`. Le modifiche delle singole PR non c'entrano, e **anche `master` fallirebbe al prossimo push**.

- [x] Aggiornamento conservativo del `Gemfile.lock` (`addressable 2.9.2`, `activesupport 8.1.4.1`, `loofah 2.25.3`, `nokogiri 1.19.7`). In locale: `bundle-audit` senza vulnerabilità, build OK, 54 test e tutti i verificatori OK.
- [ ] Dopo il merge: commentare `@dependabot rebase` sulle PR da #39 a #44. Le patch/minor (#41, #42, #43, #44) si possono unire. Le major di Actions (#39 `checkout` 4→7, #40 `upload-artifact` 4→7) vanno controllate sul changelog prima del merge.
- [ ] Chiudere la #31 (*Phase 4 Publications Atlas*, draft): il suo lavoro è già entrato in `master` con la #32.

## Step 1: catalogo software corretto

- Aggiungere **sharCP** (`andreachiocca/sharCP`, Python, MIT, con `CITATION.cff`): ECP per intagli acuti in giunti saldati. Collegarlo ai paper pertinenti e, se corrisponde, al dataset Zenodo Mode I/III già in catalogo (da verificare).
- I repository risultano trasferiti da `achiocca1/` ad `andreachiocca/`. Aggiornare `github_url`, `catalogue_status.json` e `sync_research_outputs.py`: i redirect di GitHub funzionano, ma vanno resi canonici.
- Correggere i metadati cambiati: `SeAn-CP` ora è **Python** (prima MATLAB) con licenza **GPL-3.0**.
- `FatPy` resta in `catalogue_exclusions.json`, invariato.
- Effort: M. Test: verificatore del catalogo aggiornato (sharCP presente, FatPy assente).

## Step 2: quick win dell'audit

Q1 immagine Open Graph · Q2 icone social · Q3 footer · Q4 testo duplicato in Publications · Q5 figura e ritratto nel primo schermo su mobile · Q6 varianti WebP · Q8 favicon personale · Q9 resti del template (notebook, plotly demo, `papers.bib`, PDF di esempio) · Q10 duplicati in Repositories.
Effort: M in totale; nessun cambiamento di stile.

## Step 3: design system "technical warm minimal"

Si evolve l'attuale, senza rifarlo.

- **Token CSS** in un solo file: `--paper #FAF8F3`, `--ink #1F1E1B`, `--muted #6B6760`, `--rule #E6E1D6`, `--accent #C4623E` (terracotta: link e focus), `--sigma #2A8C82` (teal, componenti normali), `--tau #D08A2E` (ambra, componenti di taglio). La dark mode usa le stesse tinte su `#16150F`. I colori σ/τ dell'hero diventano il codice cromatico di **tutte** le figure.
- **Font** self-hosted con subset latino + greco: *Newsreader* o *Source Serif 4* per i titoli, *Inter* per il testo, *JetBrains Mono* per etichette FIG. e numeri. Si elimina Google Fonts.
- **Griglia unica** a 1200 px con colonna di testo a circa 70 caratteri (M1). Le figure e le note a margine usano la colonna larga.
- **Motion kit** (~2 kB JS): comparsa a dissolvenza delle sezioni, *line drawing* degli SVG (`stroke-dashoffset`) all'ingresso nel viewport, contatori numerici nelle statistiche.
- Effort: L. Una PR per famiglia di pagine (home → research → publications/repositories → resto).

## Step 4: matematica visibile

- KaTeX self-hosted al posto di MathJax (M2). Le formule si renderizzano al build quando possibile (nessun flash).
- 1–2 equazioni chiave per area di ricerca, numerate e con il riferimento al paper.
- Effort: M.

## Step 5: figure generate dai codici originali (il cuore)

Pipeline: `scripts/generate_code_figures.py` installa ciascun pacchetto **a un commit fissato** e calcola i casi. Scrive JSON compatti in `assets/data/figures/` con un `manifest.json` (repo, commit, funzione, parametri, hash). Il sito si limita a disegnare: nessun calcolo scientifico è reimplementato in JS. Un test confronta i JSON con valori di riferimento ricalcolati, per intercettare derive.

| Figura | Sorgente | Cosa mostra | Interazione |
|---|---|---|---|
| **5a Sfera del danno** | `multifat` (`_findley_plane_value`, `_fatemi_socie_plane_value`, griglia piani da `multifat.planes`) | Parametro di danno $D(\theta,\varphi)$ sulla semisfera delle normali, per carico assiale-torsionale con $\lambda=\tau_a/\sigma_a$ e sfasamento $\Delta\varphi$; marcatore del piano critico $\mathbf{n}^\ast$. | Slider $\lambda$ e $\Delta\varphi$ su una griglia precalcolata (es. 5×7 casi). Rotazione della sfera trascinando. Transizioni morbide tra casi. |
| **5b Confronto criteri** | `multifat` (`Results/current`) | Errore di vita per criterio e materiale (dot plot ordinato), dai risultati già pubblicati del repo. | Hover per i dettagli; filtro per materiale. |
| **5c ECP su intagli acuti** | `sharCP` (`data/validation/*`) | Vita predetta vs sperimentale, con banda di dispersione, per le geometrie di validazione. | Hover per geometria e modo (I/III). |
| **5d Convergenza SeAn-CP** | `SeAn-CP` (`results/phase3_reference`) | Convergenza del metodo semi-analitico contro la scansione dei piani. | Statica con *line drawing*. |
| **5e Hero** | stesso motore di 5a | La FIG. 01 attuale resta. In seconda fase le onde $\sigma$/$\tau$ possono venire da un caso reale di 5a, con stessi valori e stessa didascalia. | Invariata. |

- Effort: 5a L, poi M per ciascuna delle altre.
- Da confermare con l'autore prima di pubblicare: quali materiali e casi mostrare, e che i risultati del repo siano quelli "ufficiali" (non *pre-audit*).

## Step 6: card software di nuova generazione

Linguaggio, licenza, release, DOI Zenodo (attivare l'integrazione GitHub→Zenodo sui repo, operazione dell'autore), pulsante **Cite** da `CITATION.cff`, snippet d'uso di 3 righe e la mini-figura dello Step 5 come anteprima della card (M3). Effort: M.

## Step 7: Technical notes

Ripubblicare le note ritirate (soluzione in forma chiusa del piano critico, metodo semi-analitico, ECP) con layout da quaderno: KaTeX, figure dello Step 5, note a margine e link a codice e paper (M4). **Richiede la revisione dei testi da parte dell'autore.** Effort: M per nota.

## Step 8: pubblicazioni

Pulsanti Cite / Code / Data collegati agli output, badge OA, thumbnail per le `selected`, conteggio citazioni statico da OpenAlex aggiornato in CI (M5). Verifica delle licenze dei PDF editoriali (M6): **serve una decisione dell'autore** per ogni PDF non OA. Effort: M.

## Step 9: talks, service e timeline

Pagina Talks & service da YAML, più una timeline della ricerca (R3) con un'animazione leggera di scorrimento. Effort: M.

---

## Ordine e dipendenze

```
0 ─▶ 1 ─▶ 2 ─▶ 3 ─┬─▶ 4 ─▶ 7
                  ├─▶ 5 ─▶ 6
                  └─▶ 8 ─▶ 9
```

Lo Step 5a si può prototipare in parallelo allo Step 3 su un branch separato, per vedere presto il risultato principale.
