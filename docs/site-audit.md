# Audit visivo e di contenuto: andreachiocca.github.io

Data: 4 novembre 2026. Baseline: `master` @ `b69cc4b`. Documento di sola analisi: **nessuna modifica al sito**.

## 0. Metodo e stato attuale

- **Stack**: Jekyll 4.4.1 + tema **al-folio** fortemente personalizzato (Bootstrap 4 + MDB, jekyll-scholar, i18n EN/IT con plugin locali). Deploy con GitHub Actions (`.github/workflows/build.yml`) e preview Cloudflare per le PR (`preview.yml`). La CI fa test unitari Python, verifiche Ruby, controlli browser Playwright e audit delle dipendenze.
- **Build locale riuscita** (`JEKYLL_ENV=production`, Ruby 3.3.6, ~10 s). Ho fatto screenshot con Chromium a 1440 px (chiaro/scuro) e 390 px di home, research, publications, repositories, laboratory, teaching, thesis, cv e `/it/`. Google Fonts non era raggiungibile dalla sandbox: **non ho potuto valutare la resa reale dei font**.
- **Contesto**: il sito ha già avuto 7 fasi di redesign ("Technical Editorial", direzione B, vedi `docs/design-phase2.md` e `docs/ACADEMIC_SITE_AUDIT.md`). Ci sono già un hero SVG animato (cubo di Cauchy con carico assiale-torsionale sfasato, `_includes/home_visual.html`), figure concettuali per le aree di ricerca, un catalogo di 14 output con schema.org `SoftwareSourceCode`/`Dataset`, pubblicazioni con DOI, JSON-LD `Person` + `ScholarlyArticle`, e dark mode. Questo report **non riparte da zero**. Si concentra su ciò che ancora manca per l'effetto "wow" e per un pubblico nerd, e sulle incoerenze rimaste.

**Giudizio sintetico.** Le basi sono solide: accessibilità, metadati, bilinguismo e test sono sopra la media dei siti accademici. Restano tre limiti:

1. **Manca la scienza visibile**: nel sito non c'è nemmeno un'equazione renderizzata, i tre articoli tecnici sono stati ritirati e le figure sono illustrative, non dati.
2. **Il layout è incoerente tra le pagine**: home e research sono larghe (~1130 px), publications e repositories strette (800 px). I font e le "voci" visive sono diversi tra le pagine.
3. **Il software si presenta come una tabella di testo**: non ci sono badge, figure, DOI software né snippet di codice.

Legenda effort: **S** < 1 h · **M** ½–1 giorno · **L** 2–5 giorni.

---

## 1. Quick win (alto impatto, basso rischio)

| # | Problema concreto | Proposta | Effort |
|---|---|---|---|
| Q1 | **Nessuna immagine Open Graph**: `_config.yml:53` `og_image:` è vuoto e `_includes/metadata.html:61` emette `og:image` vuoto; `twitter:card` è `summary` (`metadata.html:66`). I link condivisi su LinkedIn, Slack o email appaiono senza anteprima. | Creare una card 1200×630 (nome, affiliazione, cubo di FIG. 01 come sfondo) da generare una volta dall'SVG esistente. Impostare `og_image` e `summary_large_image`. | S |
| Q2 | **Icone social enormi**: `.contact-icons { font-size: 4rem; }` (`_sass/_base.scss:355`). In fondo alla home le 7 icone sono il blocco più "pesante" della pagina (vedi screenshot) e stonano con il registro editoriale. | Ridurle a 1.5–1.75rem, con etichetta testuale (ORCID, Scholar, Scopus, RG, GitHub) in monospace e bordo sottile. Spostarle anche nel footer. | S |
| Q3 | **Footer vuoto**: `_includes/footer.html:4` mostra solo "© Copyright 2026 Andrea Chiocca." | Footer a due colonne: affiliazione + indirizzo DICI, poi ORCID, Scholar, Scopus, GitHub, "last updated" (commit hash corto, `site.github` o `git log` in CI), licenza contenuti (es. CC BY 4.0 per i testi). | S |
| Q4 | **Testo ripetuto in Publications**: `_pages/publications.md:7` (description) e `:14` (intro) dicono la stessa cosa, una sotto l'altra (vedi screenshot dark). | Tenere la description e sostituire l'intro con una riga di sintesi numerica (es. "18 articoli su rivista · 11 contributi a congresso · h-index Scopus N"), oppure eliminarla. | S |
| Q5 | **Il ritratto non compare nel primo schermo su mobile**: a 390 px (`_layouts/about.html:5-30`) il primo schermo è tutto testo, mentre la FIG. 01 e la foto finiscono sotto la bio. Il "wow" del sito resta invisibile a chi apre da telefono. | Su `< 576px` mostrare una versione compatta della FIG. 01 (altezza ~220 px, solo cubo e onde) subito sotto il nome, e la foto piccola accanto al nome. | S–M |
| Q6 | **La variante WebP a 1400 px è in realtà a 800 px**: `_config.yml:353-354` `webp: "-resize 800x"` forza 800 px su tutte le larghezze (`prof_pic-800.webp` e `prof_pic-1400.webp` sono identici, 27 958 B). I `srcset` sono quindi inutili sopra 800 px. | Rimuovere il `-resize` globale e lasciare che `widths` generi le varianti. Nel repo il ritratto originale pesa 2,29 MB (`assets/img/prof_pic.jpg`) e viene pubblicato com'è: valutare un master a 1600 px. | S |
| Q7 | **Font caricati ma non coerenti**: `_includes/head.html:16` carica Roboto, Roboto Slab **e Material Icons** da Google Fonts. Material Icons e Roboto Slab non sono usati nei template personalizzati. I titoli usano `ui-monospace, SFMono, Consolas, Liberation Mono` (`_sass/_homepage_phase2.scss:24`), quindi il nome in home cambia aspetto su Mac, Windows e Linux. | Scegliere 2 famiglie (vedi §4), servirle self-hosted come WOFF2 con subset latin + greco (σ, τ, Δ, φ) ed eliminare la richiesta a Google. Ne guadagnano privacy (GDPR, soggetto a contenzioso in UE) e coerenza. | S–M |
| Q8 | **Favicon = logo UniPi** (`_config.yml:16`, `assets/img/UnipiLogo.png`, 141 kB). Pesa, è un marchio istituzionale con regole d'uso proprie e non distingue il sito personale da quelli d'Ateneo. | Favicon SVG personale (monogramma "AC", oppure un cubo isometrico stilizzato come quello di FIG. 01), più PNG 32/180 px. | S |
| Q9 | **Resti del template ancora in build**: `assets/jupyter/blog.ipynb` costringe la CI a installare Jupyter (`build.yml`, step "Install notebook support"), `assets/plotly/demo.html` viene pubblicato e `_bibliography/papers.bib` (84 righe di esempio, con `example_pdf.pdf`) e `assets/pdf/Prova.pdf` / `example_pdf.pdf` sono ancora nel repo. | Escludere o rimuovere: la CI si accorcia (niente pip install di jupyter) e la superficie pubblica si pulisce. | S |
| Q10 | **Selected outputs duplicati**: in `/repositories/` le 4 card "Selected outputs" (`_pages/repositories.md:31-48`) ricompaiono identiche in testa al catalogo completo. In desktop la pagina è lunga 5 600 px, in mobile 9 800 px. | Escludere gli spotlight dal catalogo completo, oppure trasformare gli spotlight in card visive (vedi M3) e lasciare il catalogo come elenco compatto. | S |

## 2. Interventi medi

| # | Problema concreto | Proposta | Effort |
|---|---|---|---|
| M1 | **Larghezza incoerente**: `_config.yml:43` `max_width: 800px` (usato in `_sass/_layout.scss:26`) vale per publications, repositories, cv e teaching, mentre home, research e laboratory si allargano a ~1130 px. Si passa da una pagina "rivista" a una "colonna da blog". | Griglia unica a 12 colonne con max 1200 px; testo corrente a 68–72 caratteri e figure e margini che usano la colonna larga (stile Tufte: margin notes per DOI e badge). | M |
| M2 | **Nessuna equazione nel sito**: MathJax è attivo (`_config.yml:374`) ma `_includes/scripts/mathjax.html:2` lo carica solo con `page.math` o con il layout distill, e nessuna pagina lo usa (0 occorrenze di `$$` in `_pages/*.md` e `_data/research_areas.json`). Per chi lavora con il piano critico manca proprio la parte più interessante. | Passare a **KaTeX** (più leggero, rendering sincrono, adatto a poche formule) e aggiungere in ogni area di ricerca 1–2 formule chiave. Esempi: traslazione di trazione $\mathbf{t}(\mathbf{n}) = \boldsymbol{\sigma}\,\mathbf{n}$; Fatemi–Socie $\gamma_a\left(1 + k\,\dfrac{\sigma_{n,\max}}{\sigma_y}\right)$; ricerca del piano $\mathbf{n}^\ast = \arg\max_{\mathbf{n}\in S^2} D(\mathbf{n})$. Formule numerate e con citazione del paper sorgente. | M |
| M3 | **Le card software sono solo testo**: `_includes/research_output.html:8-18` rende titolo, descrizione e link. I titoli in monospace grande vanno a capo male ("Multiaxial / fatigue library"). Non ci sono licenza, versione, DOI software, citazione, immagine o snippet. Inoltre nessun repo software ha un DOI Zenodo nel catalogo (`_data/research_outputs.json`: nessun campo DOI per i 7 `kind: software`). Nota: `sharCP` non compare nell'inventario GitHub (`_data/catalogue_status.json`) e `FatPy` è escluso su tua richiesta (`_data/catalogue_exclusions.json`). Se `sharCP` esiste su un altro account, va aggiunto. | Card "software" dedicata: linguaggio (pallino colorato GitHub-style), licenza, ultima release, badge DOI Zenodo (dopo aver attivato l'integrazione GitHub→Zenodo sui repo), pulsante "Cite" che copia BibTeX/CFF, snippet di 3 righe (`from multiaxial_fatigue import ...` / chiamata MATLAB) e una mini-figura generata dal codice stesso (es. il cerchio di Mohr o la mappa del danno sul piano). Dati da `sync_research_outputs.py` già esistente, statici al build: nessuna chiamata API dal browser. | M–L |
| M4 | **I tre articoli tecnici sono stati ritirati**: `docs/retired-notes/` contiene tre note già scritte (soluzione in forma chiusa del piano critico, metodo semi-analitico, ECP), oggi sostituite da redirect `noindex` (`_data/retired_notes_urls.json`). Sono il contenuto più "nerd" che il sito abbia mai avuto. | Ripubblicarle come **"Technical notes"**: layout dedicato con KaTeX, numerazione delle equazioni, figure, DOI del paper collegato, link al codice e data di revisione. Bastano 1–2 note fatte bene per dare carattere al sito. Serve una scelta editoriale (rivedere i contenuti); il README dei retired-notes lo richiede esplicitamente. | M |
| M5 | **Pubblicazioni piatte**: 30 voci in una lista lunga 10 700 px, con soli pulsanti DOI, Publisher, PDF e BibTeX (`_layouts/bib.html:160-200`). Badge Altmetric e Dimensions disattivati (`_config.yml:310-312`), anteprime disattivate. | (a) Thumbnail della figura grafica principale per le 4 `selected`. (b) Badge tipo rivista/anno/OA in monospace. (c) Pulsanti "Cite" (BibTeX/RIS copia-negli-appunti), "Code" e "Data" collegati agli output con lo stesso `related_publications`: il legame esiste già nei dati ma non si vede dal lato pubblicazione. (d) Facoltativo: conteggio citazioni statico aggiornato in CI da OpenAlex/Crossref (niente widget di terze parti). | M |
| M6 | **PDF degli editori nel repo**: `assets/pdf/` pesa 88 MB e contiene file chiaramente in versione editoriale, ad esempio `2021_1-s2.0-S0020740321001363-main.pdf` e `2024_1-s2.0-S0142112324000495-main.pdf` (Elsevier, non tutti OA). Pubblicarli può violare gli accordi di copyright. Non l'ho verificato voce per voce. | Controllare ciascun PDF su Sherpa Romeo/Unpaywall. Tenere i PDF solo se OA o nella versione consentita (accepted manuscript), linkare ARPI/IRIS UniPi per il resto e mostrare un badge "OA / AAM / Publisher". Sito più leggero, rischio legale più basso. | M |
| M7 | **Pagina Talks/Service assente**: `_data/academic_service.json` esiste, ma non c'è una pagina per seminari, keynote e congressi (ICMFF, FABER, ESIS). Per un pubblico accademico è un segnale di attività. | Pagina "Talks & service" con timeline (anno → evento → titolo → slide PDF se disponibili), alimentata da YAML. | M |
| M8 | **Test browser locale fallito**: `scripts/verify_site.py` riporta in sandbox "mobile CV contents must not overlay the introduction" (`scripts/check_browser.py:119`). Probabilmente dipende dall'ambiente (CDN e font bloccati), ma vale la pena capire se la regola CSS di `#toc-sidebar` dipende da risorse esterne. | Verificare nell'ultima run CI e, se la regola dipende da CSS esterno, spostarla in `_sass/_cv.scss`. | S |

## 3. Redesign e idee "nerd" (ma sobrie)

| # | Idea | Dettaglio | Effort |
|---|---|---|---|
| R1 | **Widget "Critical plane explorer"** (pezzo forte) | Una piccola sfera unitaria (canvas/SVG, JS puro, < 15 kB) colorata con il parametro di danno $D(\theta,\varphi)$ per un caso di carico scelto: assiale-torsionale con sfasamento $\Delta\varphi$, rapporto $\lambda=\tau_a/\sigma_a$ e criterio a scelta (Findley, Fatemi–Socie, ...). L'utente trascina gli slider e vede migrare il piano critico. Il cursore di fase esiste già in `stress-visual.js`: il widget ne è l'estensione naturale. Il calcolo è deterministico e va **validato contro `multiaxial-fatigue`** (stessi input → stesso $\mathbf{n}^\ast$), con un test di regressione in `tests/`. | L |
| R2 | **Diagrammi interattivi didattici** | Curva S-N (Basquin $\sigma_a = \sigma_f'(2N_f)^b$) con banda di dispersione, diagramma di Haigh (Goodman/Gerber/SWT), cerchi di Mohr 3D. Vanno bene anche per la pagina Teaching, legati ai corsi PMMEF e PF60. Sempre con legenda "illustrativo / parametri da ref. X". | M ciascuno |
| R3 | **Timeline della ricerca** | Linea orizzontale 2017→2026: PhD, visite estere (`_data/research_visits.json`), progetti, paper `selected`, release software, FABER. Generata dai dati esistenti, senza duplicazioni. | M |
| R4 | **Figure reali al posto di quelle concettuali** | Oggi FIG. R01 e le figure delle aree sono illustrazioni. Una riga per area con **dati veri**, ad esempio uno scatter vita predetta vs sperimentale con banda ±3 dai dataset Zenodo già pubblicati (ECP su ghisa sferoidale, Mode I/III), generata da script in `scripts/generate_research_atlas_figures.py` (esiste già). Didascalia con DOI del dataset. | M–L |
| R5 | **Palette e tipografia "da notebook scientifico"** | Un'unica scala di token CSS (`--ink`, `--paper`, `--grid`, `--accent-σ`, `--accent-τ`). Le due tinte σ (teal) e τ (bianco/ambra) dell'hero diventano il sistema di colori per **tutte** le figure e i grafici: chi le vede impara che "teal = normale, ambra = taglio". | M |
| R6 | **Command palette / ricerca globale** (`/` o `Ctrl-K`) | Indice JSON statico di pubblicazioni, output, corsi e tesi generato al build; ricerca client-side minimale. Un tocco da sviluppatore, utile per 30+ paper e 14 output. | M |

---

## 4. Tre direzioni di design tra cui scegliere

### A. "Engineering Drawing": evoluzione dell'attuale
Il registro tecnico esistente (FIG. NN, indici `01 /`, blu tavola), portato a sistema e coerente su tutte le pagine.
- **Mood**: tavola tecnica, cartiglio, quote e griglia millimetrata leggera; sfondo carta in chiaro, blu cianografico in scuro.
- **Palette**: `#F7F5EF` carta · `#14213D` inchiostro · `#0F4C75` blu tavola · `#2EC4B6` σ (teal) · `#F4A259` τ (ambra) · `#D9DDE3` griglia.
- **Font**: *IBM Plex Sans* (testo) + *IBM Plex Mono* (etichette, titoli FIG., numeri), entrambi con greco, self-hosted.
- **Pro / contro**: minimo rischio e continuità con le fasi 1–7, ma l'effetto sorpresa resta contenuto se non arrivano R1/R4.

### B. "Lab Notebook": pagina di quaderno scientifico
Ispirata a Distill e a Tufte: testo serif a colonna stretta, margin notes, equazioni e figure interattive integrate nel flusso, sensazione di "leggere un paper vivo".
- **Mood**: carta avorio, note a margine, numerazione delle equazioni, figure con bordo sottile e didascalie lunghe. Dark mode "lavagna".
- **Palette**: `#FFFDF7` avorio · `#1B1B1B` testo · `#8C1C13` rosso pisano (accento, link) · `#2F6690` blu · `#3A7D44` verde per i dati sperimentali · `#E8E2D0` filetti.
- **Font**: *Source Serif 4* (testo) + *Inter* (UI) + *JetBrains Mono* (codice e numeri); KaTeX per la matematica.
- **Pro / contro**: è la direzione che esalta di più technical notes (M4) e widget (R1–R2) e piace molto al pubblico nerd. Chiede però più contenuto scritto per non sembrare vuota.

### C. "Terminal / Simulation": dark-first, da post-processore FEM
Sfondo scuro come di default, colormap stile contour plot (viridis/cividis, accessibili ai daltonici), card con estetica da finestra di solver, prompt `$` sulle card software.
- **Mood**: post-processore ANSYS/ParaView, griglia di mesh, legenda a barra di colore, numeri tabulari ovunque.
- **Palette**: `#0B1020` sfondo · `#E6EDF3` testo · colormap *cividis* (`#00204D → #FFEA46`) per figure e stati · `#58A6FF` link · `#3FB950` "open data" · `#D29922` "in development".
- **Font**: *Space Grotesk* (titoli) + *Inter* (testo) + *JetBrains Mono* (codice/etichette).
- **Pro / contro**: impatto visivo forte e immediato per il software. Rischia di sembrare meno "istituzionale" a commissioni e industria, e la modalità chiara va curata a parte.

**Raccomandazione**: **B** sul contenuto (note tecniche + KaTeX + widget) con la **palette σ/τ di A**. Mantiene la continuità visiva con l'hero attuale, che funziona, e sposta l'identità del sito da "bella vetrina" a "posto dove si capisce come ragiono sul piano critico". Ordine di lavoro: Q1–Q10 → M1, M2, M4 → R1 → resto.

---

## Appendice: misure raccolte

| Pagina (desktop 1440) | Altezza px | Richieste | Peso trasferito* |
|---|---|---|---|
| `/` | 4 082 | 21 | ~840 kB |
| `/research/` | 4 361 | 17 | ~640 kB |
| `/publications/` | 10 682 | 17 | ~730 kB |
| `/repositories/` | 5 637 | 19 | ~810 kB |
| `/laboratory/` | 10 001 | 23 | ~910 kB |

\* Misura locale senza compressione HTTP e senza Google Fonts (bloccati nella sandbox); serve solo come confronto relativo. Il grosso viene da `mdb.min.js` (152 kB), Bootstrap (83 kB), jQuery e Font Awesome. Una futura migrazione via da MDB/jQuery (fuori scope ora) è il guadagno di performance più grosso.

Dimensione `_site`: 138 MB (88 MB `assets/pdf`, 25 MB `TeachingMaterial`). Nessuno scroll orizzontale a 390 px. Test unitari (`python -m unittest discover -s tests`): 54/54 OK.
