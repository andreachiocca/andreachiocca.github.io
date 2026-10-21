# Phase 4 Editorial Publication Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a lightweight bilingual Publications page in the established Technical Editorial style, with native category and keyword filters, accessible entries and unchanged scholarly metadata.

**Architecture:** Continue using `PersonalPub.bib`, the existing Jekyll Scholar queries and `_layouts/bib.html`. Add a page-scoped Sass layer and extend `bibsearch.js` as optional progressive enhancement over already rendered HTML; introduce no new client library, external citation service or data source. Use source tests before building and rendered HTML/Chromium checks after building.

**Tech Stack:** Jekyll/Liquid, Jekyll Scholar, Sass, vanilla JavaScript, Python 3.11 `unittest`/`HTMLParser`, existing Chromium smoke suite, GitHub Actions and Cloudflare Pages.

**Spec:** [Approved Phase 4 Editorial Publication Index specification](../specs/2026-10-21-publications-index-design.md)

## Global Constraints

- Change only the Publications page in English and Italian. Preserve the existing `translation_key: publications` and bilingual Jekyll page generation; no duplicate Italian page.
- Leave all 30 current canonical BibTeX records in `_bibliography/PersonalPub.bib` intact, including entry keys, titles, authors, DOIs, years, abstracts and URLs. Never hardcode 30 as a UI count.
- Preserve the three `{% bibliography --query @article %}`, `@inproceedings` and `@phdthesis` blocks, in their current order and year groups. Keep JSON-LD and individual bibliography anchors.
- Retain `#journal-articles`, `#conference-contributions`, `#doctoral-thesis` and `#Moda2022a`; preserve links to Software & Research Data.
- Keep `enable_publication_badges.altmetric`, `enable_publication_badges.dimensions` and `enable_publication_thumbnails` disabled. Do not add Google Scholar counts, badge images, extra gems/packages, fonts, animations, remote scripts or APIs.
- Scope new CSS to `.publications-index` so the five recent homepage publications and other bibliography embeds remain visually unchanged.
- Preserve one semantic `main` and `h1` per page, native `details`, keyboard access, 44 px interactive targets, light/dark themes and no-JavaScript visibility of **every** publication.
- Add minimal paired EN/IT keys using `andrea-chiocca-academic-writing`, without rewriting reviewed introduction or scientific text.
- Test widths 320, 375, 390, 768, 1280 and 1920 px; measure added JS/CSS bytes and preserve performance.
- Keep PR #32 in Draft and do not merge before the user reviews both Cloudflare previews and explicitly approves.

## Review Focus

1. **JavaScript absent or failing:** no bibliography row is initially hidden; the search/filter controls stay hidden, and every record/link/detail remains accessible. Pin with source and browser tests in Tasks 1, 2 and 4.
2. **Search and type filter interaction:** an empty year group must hide only its own header/list; empty categories and subsequent reset must recover properly. Pin with browser regression cases in Tasks 2 and 4.
3. **Incomplete and Unicode bibliographic data:** missing year or DOI must not throw, and accented, mixed-case queries should still match. Pin with isolated DOM-fixture cases in Task 2.
4. **Existing deep links and publication identity:** article key anchors, `#Moda2022a` and DOI/PDF destinations survive unchanged. Pin with generated-page contracts in Task 4.
5. **Long titles/Italian labels:** mobile light/dark layouts have no overflow and disclosure controls remain keyboard-operable. Pin with Task 3 CSS checks and Task 4 Chromium checks.

---

## File and interface map

| File | Responsibility |
| --- | --- |
| `_pages/publications.md` | Add page wrapper and canonical type markers without touching three bibliography queries. |
| `_includes/bib_search.liquid` | Localized progressive search, category buttons, count, empty and clear controls. |
| `assets/js/bibsearch.js` | Filter existing Jekyll HTML by text/type; show counts; preserve DOM identity. |
| `_sass/_publications_index.scss` | Editorial typography, responsive links/disclosures, visible focus and dark mode. |
| `assets/css/main.scss` | Import the one new scoped Sass partial. |
| `_data/i18n/en/ui.json`, `_data/i18n/it/ui.json` | Paired strings for new controls and empty states. |
| `_layouts/bib.html` | Prefer unchanged; minimal semantic hook only if needed, never rewrite metadata. |
| `tests/test_publications_index.py` | Source and contract tests run by existing pre-build `unittest` suite. |
| `scripts/verify_publications_index.py` | Verify published EN/IT records, anchors, DOI/resources and controls after build. |
| `scripts/check_browser.py` | Existing Chromium harness extended for filters, accessibility and responsiveness. |
| `.github/workflows/build.yml`, `.github/workflows/preview.yml` | Execute verifier after Jekyll, existing site, language and Research checks. |

**DOM interface:** `#publication-list` contains three `section[data-publication-category]` values `article`, `inproceedings`, `phdthesis`, each holding its unmodified `ol.bibliography > li` records and year headings. Preserve `#bibsearch` and `#bibsearch-status`. Add `#publication-type-filters[hidden]` with four `button[data-publication-filter]` values `all`, `article`, `inproceedings`, `phdthesis`, `aria-pressed` and accessible category names; add `#bibsearch-empty[hidden]` and `#bibsearch-clear[hidden]`. The status keeps `data-count-template` with `%visible%`/`%total%`. `filterPublications()` is private to `bibsearch.js`, operates on these existing DOM nodes and never fetches or reconstructs publications.

## Task 1: Scoped editorial Publications shell

**Files:** Modify `_pages/publications.md`, `assets/css/main.scss`; create `_sass/_publications_index.scss`, `tests/test_publications_index.py`.

**Interfaces:** Produces one `.publications-index` wrapper and three `data-publication-category` section markers, used by all following tasks. Keeps `layout: page` and its only `h1` in `_layouts/page.html`.

- [ ] **Step 1: Write failing source test.** `PublicationsIndexSourceTests.test_page_scope_and_canonical_bibliographies` asserts `translation_key: publications`, the new wrapper and three exact data markers, unchanged heading IDs, exact bibliography queries, `id="Moda2022a"`, `include bib_search.liquid`, and one `@import "publications_index";` in `main.scss`. Assert the stylesheet exists.

- [ ] **Step 2: Prove red.** Run `python -m unittest discover -s tests -p "test_publications_index.py" -v`; FAIL because the wrapper and partial do not yet exist.

- [ ] **Step 3: Implement shell.** Keep the existing introduction locale block and link to repositories intact; wrap introduction, search and bibliography without duplicating `h1`. Add unobtrusive kicker, sections' type markers and a restrained page-scoped Sass base using existing Technical Editorial variables. Any wider `main` rule must be scoped to this specific page, not all `.post` pages.

- [ ] **Step 4: Prove green.** Run focused unit test, `bundle exec jekyll build --trace`, `python scripts/verify_site.py _site`, `python scripts/verify_languages.py _site`. Check canonical bibliography count/order and no JS fallback. Commit `feat: establish Phase 4 publication shell`.

## Task 2: Native keyword and type filters

**Files:** Modify `_includes/bib_search.liquid`, `assets/js/bibsearch.js`, both `_data/i18n/{en,it}/ui.json`, `tests/test_publications_index.py`.

**Interfaces:** Consumes the DOM interface above. Produces live visible/total counts, four category buttons, transient empty state and clear action, with no extra data source. Reuse existing `All`, `Journal articles`, `Conference contributions`, `Doctoral thesis`; add only necessary `Publication type`, `No publications match your search.`, `Clear filters` with idiomatic IT counterparts.

- [ ] **Step 1: Write failing source contract test.** `test_filter_controls_and_i18n` asserts the four exact `data-publication-filter` values, initial All `aria-pressed="true"`, `#publication-type-filters[hidden]`, original labelled `#bibsearch[hidden]`, status `role="status"`/`aria-live`, empty and clear elements initially hidden, and identical EN/IT UI key sets. Assert badge flags remain disabled.

- [ ] **Step 2: Prove red.** Run focused tests; FAIL due to absent filter controls.

- [ ] **Step 3: Implement progressive filtering.** Attach DOMContentLoaded listeners before revealing input/buttons. Match normalized query terms against existing `li.textContent` plus its nearest year heading when available; combine keyword matches with the selected section type using logical AND. Recompute visibility of `li`, `ol.bibliography`, its adjacent `h2.bibliography`, and each type section; never remove/reorder nodes. Derive counts from rendered entries. Reflect selection in `aria-pressed`, update `#bibsearch-status`, show/hide no-results and clear controls, and restore everything on clear. If controls are missing, exit without changing HTML. Keep UI hidden until initialized. Respect `[hidden]` styling.

- [ ] **Step 4: Prove behavior and green.** Add focused Chromium DOM tests (in the existing smoke harness, using synthetic test DOM only when necessary) for All, article, conference + `2026`, unmatched text, reset, two terms, accented casefolding, absent year/DOI and reappearing year headers. Run unit tests and full Jekyll/site/language checks. Commit `feat: add progressive type and keyword publication filters`.

## Task 3: Scholarly entry styling

**Files:** Modify `_sass/_publications_index.scss`, `tests/test_publications_index.py`; modify `_layouts/bib.html` only if an indispensable class is missing.

**Interfaces:** Consumes the original Jekyll Scholar `ol.bibliography > li` and its `.title`, `.author`, `.periodical`, `.links`, `details.publication-details`, `h2.bibliography`. Produces consistent Technical Editorial styling without changing other bibliography placements.

- [ ] **Step 1: Write failing `test_scoped_entry_styles_and_no_external_badges`.** Assert new selectors for title, authors, venue, document links, native details, focus, year headings and responsive screens under `.publications-index`. Assert no configuration change enables badge services or thumbnails; keep `_layouts/bib.html` unmodified unless a needed hook has an independent regression test.

- [ ] **Step 2: Prove red.** Run `python -m unittest discover -s tests -p "test_publications_index.py" -v`; FAIL because entry-specific styles are missing.

- [ ] **Step 3: Implement entry styling.** Use quiet rules, compact monospaced metadata, airy line spacing, clear title hierarchy, no decorative card shadows or animation. Set min 44 px action links and disclosure summaries, preserve `summary` native keyboard operation, wrap long titles/URLs/BibTeX `pre`, provide visible keyboard focus and light/dark contrast. Keep `.publications-index [hidden]` truly hidden even with display rules, including on narrow screens.

- [ ] **Step 4: Prove green and commit.** Run unit tests, Jekyll build, `verify_site.py`, `verify_languages.py`, `verify_research_atlas.py`; check no unintended homepage changes. Commit `style: refine publication entries for Technical Editorial`.

## Task 4: Independent HTML checks, browser QA and preview

**Files:** Create `scripts/verify_publications_index.py`; modify `tests/test_publications_index.py`, `scripts/check_browser.py`, `.github/workflows/build.yml`, `.github/workflows/preview.yml`.

**Interfaces:** Define `verify_publications_index(root: pathlib.Path) -> None` and CLI `python scripts/verify_publications_index.py _site`, raising `ValueError` with a specific paper/route on mismatch. Existing `scripts/verify_site.py` invokes `check_browser(root)`; do not run browser checks directly as a separate CLI.

- [ ] **Step 1: Write failing verifier tests.** `test_verifier_detects_missing_publication_and_locale` checks missing paper ID, wrong section, absent Italian file and altered DOI link; `test_verifier_accepts_current_bibliography` uses the actual built site. Derive expected keys/types from canonical `PersonalPub.bib` rather than hardcoding totals; synthetic negative fixtures may be generated by perturbing valid generated HTML. Preserve optional DOI and year.

- [ ] **Step 2: Prove red, then implement verifier.** Run focused tests; FAIL because `verify_publications_index.py` is absent. Implement a stdlib HTML reader of `_site/publications/index.html` and `_site/it/publications/index.html` that compares entry IDs and ordering, DOI/PDF/resource links, three sections, accessible controls and `#Moda2022a`, and ensures one scholarly JSON-LD record per publication in both locales. Keep the existing `verify_site.py` and `verify_languages.py` as the sources of shared-site/locale checks. Wire new verifier **after** those checks and Jekyll in both workflows.

- [ ] **Step 3: Add browser regressions.** At 390 px in both languages, cover combined text/type filters, counts, no matches, clearing, aria-pressed and Enter/Space disclosures. Add publication-only passes at 320 and 1920 px, and check existing widths 375/768/1280, in light and dark modes. Test no JavaScript (all original rows visible), touch targets >=44 px, overflow and hash navigation to section, paper and `Moda2022a` IDs. Continue existing whole-site smoke suite without multiplying every other route.

- [ ] **Step 4: Run full verification and commit.** Execute `python -m unittest discover -s tests -v`; `bundle exec ruby scripts/check_localization.rb`; `bundle exec ruby scripts/check_recent_publications.rb`; `bundle exec jekyll build --trace`; `python scripts/verify_site.py _site`; `python scripts/verify_languages.py _site`; `python scripts/verify_research_atlas.py _site`; `python scripts/verify_publications_index.py _site`. Missing Chromium is a skipped check, never evidence of rendering success. Measure the added JS/CSS byte and network footprint. Commit `test: verify bilingual publication index integrity`.

- [ ] **Step 5: Publish draft preview for approval.** Push/attach only fast-forward commits, confirm `build`, `Generated site verification` and Cloudflare `preview` are green on the **same final PR head SHA**, and inspect in browser: EN `https://pr-32.academic-website-preview.pages.dev/publications/` and IT `https://pr-32.academic-website-preview.pages.dev/it/publications/`. Record screenshots/viewport tests and performance delta in PR #32, request explicit user visual approval and do **not** merge.

## Execution discipline

- Use an isolated worktree or the already separate branch `design/phase-4-publications-index`, checking HEAD before each push. No force-push.
- Carry out each task red/green with a small commit and a review gate. Never report a preview or test as passed before its precise commit is verified.
- If GitHub write approval expires, record the unpublished full commit SHA and stop retries; after checking its parent, the user can advance the PR branch through GitHub Codespaces, as in Phase 3.
- PR #32 stays in Draft until complete bilingual visual review and final merge authorization.
