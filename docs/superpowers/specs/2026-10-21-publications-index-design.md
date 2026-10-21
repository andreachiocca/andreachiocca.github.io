# Phase 4 Editorial Publication Index

**Date:** 21 October 2026  
**Status:** Design direction approved. Written specification awaiting review.  
**Repository:** [andreachiocca/andreachiocca.github.io](https://github.com/andreachiocca/andreachiocca.github.io)  
**Target pages:** `/publications/` and `/it/publications/`

## 1. Goal and design constraints

Extend the approved Technical Editorial visual identity of the homepage and Research Atlas to the Publications page. The intended audience is researchers, collaborators and students searching for scholarly work, bibliographic details and available documents.

The user explicitly approved the **Editorial Publication Index** direction, with three priorities. The result must be lightweight, easy to maintain and visually rewarding without unnecessary movement, large graphics, external dependencies or complicated administration. The existing scholarly metadata and bilingual structure take precedence over visual novelty.

**Completion criteria:** Visitors can browse the bibliography in the original journal/conference/thesis categories and year order, search by keyword, narrow results by type, read abstracts, follow DOI and file links and obtain BibTeX. Without JavaScript, every record and its links remain available. Both locales have equivalent content and behavior.

## 2. Existing architecture and facts

The current page is `_pages/publications.md` and has `translation_key: publications`. Its body uses an existing Jekyll bilingual rendering system that generates `/it/publications/` from the same canonical page. The actual bibliography comes from `_bibliography/PersonalPub.bib` configured through `jekyll-scholar` in `_config.yml`. It currently has **30** entries, comprising **18 journal articles**, **11 conference contributions** and **one doctoral thesis**.

The template `_layouts/bib.html` owns individual publication records, bibliographic title, authors, venue, date, DOI and document links, abstracts, BibTeX, metadata scripts and optional badges. The existing `_includes/bib_search.liquid` and `assets/js/bibsearch.js` provide progressive-enhancement text search. The bibliography is rendered into three static category sections by type, with Jekyll Scholar year grouping and descending year order.

Current `_config.yml` sets `enable_publication_badges.altmetric: false`, `enable_publication_badges.dimensions: false`, `enable_publication_thumbnails: false` and `bib_search: true`. **Do not switch them on as part of this phase.** The current BibTeX entries, custom publication links, published names and metadata are the canonical source, not a copy generated for filtering.

Keep all current publication entry keys, author order, year, publication type, paper title, journal/conference/thesis title, DOI, abstracts, source links, PDF/supplemental links, BibTeX access and existing JSON-LD. Keep the existing Rosenthal dataset anchor `#Moda2022a` pointing to the research-output catalogue. Do not edit the bibliography content, inferred citation totals, venues, or output catalogue records to achieve the visual layout.

## 3. Evaluated implementation approaches

| Approach | Benefits | Costs | Decision |
| --- | --- | --- | --- |
| CSS-only adaptation of existing bibliography | Lowest implementation and runtime cost | Leaves discovery and filters unchanged | Good fallback |
| **Scoped editorial styling plus a small extension to existing filtering JavaScript** | Consistent design, clearer browsing, keyboard-operable filters, no new library | Requires a limited amount of extra tests | **Chosen for Phase 4** |
| Rebuild with card components, live citation widgets and richer JavaScript | Additional displays and metrics | More moving parts, maintenance, external traffic and potential loading delays | Rejected for this phase |

The chosen approach reuses the Jekyll Scholar HTML and changes presentation locally. It does not create a second publications database, a new plugin, a client-side search index, or a dependency on a live citation service.

## 4. Editorial structure

### 4.1 Introduction

Provide a wide, restrained Publications introduction that feels part of the homepage and Research Atlas family, with a small ordinal/kicker, strong typography, existing concise introductory text and a link to the Software and Research Data catalogue.

A compact publication overview may show the number of journal articles, conference contributions and doctoral theses **only if the counts are derived from generated records at build time or computed from the rendered HTML**. Never hardcode the present counts as permanent site copy; counts must not become stale when `PersonalPub.bib` changes. Do not make editorial charts or pretend the counters are citation totals.

There is no need for another animated engineering diagram. Use simple rules, metadata typography, subtle grid or small typographic folio numbers instead of decorative scientific imagery.

### 4.2 Browsing and filters

Keep the current keyword-search field, including the existing EN/IT accessible label and placeholder. Provide compact category controls for **All**, **Journal articles**, **Conference contributions**, **Doctoral thesis**, using the same design language as the Research page's anchor controls.

- On initial load with JavaScript, the default filter is All and all records are visible.
- Keyword terms and type selection combine with logical AND; matching is case-insensitive. Preserve search by title, author, publication year and keywords as supported by the current script.
- A short localized live-region status updates the number of visible records without hiding or removing any bibliographic element from the original DOM.
- If a category/year grouping has no visible entries, only its visual wrapper and corresponding year heading may be hidden; a category can reappear when filters change.
- When no items match, show one concise localized no-results message and a clear/reset control. The empty state is transient, not a server-side empty bibliography.
- Initial static HTML shows every publication. The search field and category controls are revealed through progressive enhancement only after their event handlers are attached. If scripts fail or are disabled, the entire bibliography remains readable.
- Preserve matching against the original Jekyll Scholar `ol.bibliography > li` output, including category and year group structure; do not serialize or duplicate bibliography data into JSON.

Use native buttons with `aria-pressed` and a logical focus order. Do not introduce debouncing, remote search, history state, category URLs or a new filtering package without a demonstrated need.

### 4.3 Publication entries

Replace the current sparse, generic bibliography-item presentation with a restrained **editorial entry**. Keep the list structure and document order rather than converting each item to an isolated boxed card.

Visually foreground the scientific paper title, then authors, venue/year and available links. Use subtle rules, a small year/section marker, monospaced metadata and the navy/teal palette established in Phases 1–3. Sections for journal articles, conferences and doctoral thesis retain their original order, and entries retain descending year order.

Retain the author highlighting, coauthor links, DOI, publisher, PDF, supplements, code, slides and other existing actions. Long titles, long author lists and long Italian labels must wrap without truncation or horizontal overflow. Abbreviations or venue badges may remain where there is verified source data; do not invent a publication image or a journal logo.

Keep the existing `details` blocks for abstracts and BibTeX. Their keyboard operation, focus styles, meaningful labels and full text must survive the restyling. Avoid opening or loading all abstracts automatically; hiding them behind native disclosure is sufficient.

### 4.4 Visual continuity

Use existing design tokens and font choices from `_sass/_technical_editorial.scss`, `_sass/_research_atlas.scss` and the homepage phase. Prefer a page-specific class such as `.publications-index` and a scoped stylesheet import. Do not modify generic `.post`, navigation, card or catalogue selectors, and do not redesign Research or the homepage.

The design should work with light/dark themes and `prefers-reduced-motion`. Interactive states should rely on clear borders/underlines, not animated cards or large effects. No new fonts, icon packages, hero photographs, network-loaded images or external JavaScript are needed.

## 5. Citation metrics decision

The user requested an optional feasibility review of the citation badges used by [al-folio](https://github.com/alshedivat/al-folio).

### Findings from upstream

al-folio's current bibliography template supports:

- **Google Scholar citation badges** based on `google_scholar_id`, a Jekyll citation tag (`google_scholar_citations`) and a badge image supplied by `shields.io`.
- **INSPIRE-HEP citation badges**, principally useful for related research domains.
- **Dimensions badges**, potentially displaying citation-related information through an external service.
- **Altmetric badges**, representing online attention and not equivalent to academic citation counts.

Its architecture documents the `al_citations` extension for the citation tags. The current website includes some Altmetric/Dimensions markup but disables the badges. Replicating live Google Scholar counts would introduce an additional mechanism for fetching and exposing counts, per-record identifiers, potential failure/rate-limit behavior and remote badge traffic. A live count does not belong in the critical path for building or browsing the bibliography.

### Recommended scope

**Phase 4 must not fetch or render live citation counts.** The DOI and existing publication links remain the dependable way to reach authoritative records. If a trustworthy, low-maintenance citation-data source becomes available later, treat it as an independent enhancement, reviewed separately for data provenance, update cadence, accuracy, licensing and failure behavior. An optional future static snapshot stored in a small generated JSON file could be evaluated, but should not be added now.

Do not display zero citations merely because metadata is missing. Do not equate Altmetric attention with scholarly citations. Avoid external badge embeds and do not require an API key for a personal academic website.

## 6. Implementation boundaries and data flow

Expected source changes after implementation-plan approval:

| Existing/new file | Intended responsibility |
| --- | --- |
| `_pages/publications.md` | Add an editorial page wrapper/section introduction and a small discovery/filter region, preserving existing Liquid bibliography queries |
| `_layouts/bib.html` | Minimal extra semantic classes/data attributes, only if needed for presentation; preserve JSON-LD and all links |
| `_includes/bib_search.liquid` | Accessible keyword search and category controls, with EN/IT label keys |
| `assets/js/bibsearch.js` | Extend the existing progressive-enhancement filter, without a new dependency |
| `_sass/_publications_index.scss` | Publication-only styling, mobile layouts, dark-mode and focus states |
| `assets/css/main.scss` | Import the new scoped stylesheet |
| `_data/i18n/en/ui.json`, `_data/i18n/it/ui.json` | Minimal paired strings for filters, totals, empty/reset states |
| Existing checks, plus focused tests | Verify unchanged bibliography, localization, accessibility and new filtering semantics |

Data flow: `PersonalPub.bib` → Jekyll Scholar → same server-generated category/year bibliography HTML → scoped CSS plus lightweight, optional client-side filtering. Count labels and category filters derive their data from the rendered entries. All DOI and resource URLs remain original Jekyll-rendered links.

The page should still work when JavaScript is unavailable, even if search controls are not. A missing `doi` should simply omit a DOI action without hiding the publication. A year missing from one bibliographic record should not break the page or filter logic. The existing category sections remain the source of category identity, not a second manually maintained mapping of publications.

## 7. Quality gates and previews

### Data integrity

- Both `/publications/` and `/it/publications/` render all canonical `PersonalPub.bib` records in the same three category sections and original chronological order.
- All bibliographic keys and existing deep links, including `#Moda2022a`, continue to resolve.
- No paper titles, author lists, DOIs, publication types, abstracts, BibTeX or external links are changed.
- Existing ScholarlyArticle/Thesis JSON-LD remains valid, with one applicable record per publication.
- The page still has one semantic `main` and `h1` in both languages.

### Interaction and accessibility

- Search by title, author, year and keywords; combined search/type filters; per-category visibility; total and visible counts; empty/reset behavior.
- All entries remain visible without JS. Native disclosure controls still work with keyboard.
- Accessible search label, localized category names, pressed state and live count/status region.
- Desktop/mobile and light/dark rendering, with no clipping or horizontal overflow, tested at 320, 375, 390, 768, 1280 and 1920 px.
- Focus indicators and at least 44 px interactive targets for search controls, filter buttons and key action links.

### Performance and release

- No new runtime library, analytics embed, remote badge or API call.
- Favor reuse of the existing `bibsearch.js`; add only the minimal code needed for filtering. Measure JS/CSS payload against baseline and document the small delta.
- No layout/content changes to Research, the homepage, Software, Laboratory, Teaching or CV.
- Keep the existing Jekyll, localization, publication, link, security and browser verification suites passing.
- Develop on a separate Phase 4 branch and draft PR, with Cloudflare EN/IT preview. Do not merge before user inspection and explicit authorization.

## 8. Stage approvals

The Editorial Publication Index **direction** and its lightweight/maintainable constraints are approved. **This written specification requires a separate review.** Only after its approval should the detailed implementation plan be written. Only after approving that plan and choosing the execution method should source files be changed. The draft PR at the specification stage must remain documentation-only.
