# Phase 3 Research Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the bilingual Research page as a Technical Research Atlas with four documented scientific schematics, while preserving canonical records, published links, project roles and the existing website.

**Architecture:** Keep the existing Jekyll data flow and the single Research source page. Add a page-specific `research_atlas` layout and small Liquid includes, with scoped Sass and no runtime dependency; use a deterministic offline generator only for the mechanics-based fatigue schematic. Test source contracts before the build and rendered English/Italian pages after the build.

**Tech Stack:** Existing Ruby/Jekyll/Liquid/Sass, static inline SVG, Python 3.11 standard library (`unittest`, `html.parser`, `xml.etree.ElementTree`), existing Chrome-based smoke harness, GitHub Actions and Cloudflare Pages Direct Upload.

**Spec:** [Approved Phase 3 Research Atlas specification](../specs/2026-10-21-research-atlas-design.md)

## Global Constraints

- Restrict public-facing changes to the Research page, `/research/` and `/it/research/`.
- Preserve all four IDs and ordering from `_data/research_areas.json`; reuse `localized_record: 'research_areas'`.
- Preserve the published intro, summaries, methods, links, bibliography keys, project metadata and shared research-project and visit includes.
- Preserve anchors `research-areas`, `projects`, `selected-collaborative-projects`, `international-collaborations`, and `research-environment`.
- Preserve `data-project="faber"` and the established WG3, WG4.3 and WG5.3 role assertions.
- Maintain exactly one semantic `main` and `h1`, with correct headings and accessible `details`.
- Ensure every primary link and disclosure summary has an effective touch-target height of at least 44 px.
- Check viewport widths 320, 375, 390, 768, 1280 and 1920 px, in EN/IT and light/dark themes.
- Four SVG schematics must have documented scientific assumptions; combined original SVG source should target less than 35 KB.
- No new runtime JavaScript, GIF, remote assets, fonts, Jekyll plugins, duplicated data collections or global redesign.
- Keep `_layouts/page.html`, navigation, homepage, publications, CV, teaching and laboratory outputs unchanged.
- Use the installed Andrea Chiocca academic-writing profile for any new EN/IT copy; no unsupported claims or general text rewrite.
- Only a same-repository PR preview may deploy; never merge Phase 3 without explicit approval.

## Review Focus

1. **Missing optional figure**: the corresponding research chapter, summary, methods, anchors and all links must still render without a visual. Pinned in Tasks 2 and 3.
2. **Long Italian labels / wrapped FABER roles**: the design must avoid clipping, horizontal scrolling and lost WG text at 320 and 390 px. Pinned in Tasks 4 and 5.
3. **Direct deep-link navigation under the fixed navbar**: `#projects` and the four area IDs must remain visible when opened directly or through the navigation. Pinned in Tasks 1 and 5.
4. **Scientific arrow orientation**: changing a tensor component or normal must yield a traction decomposed into a perpendicular normal and tangential shear part, with the same projection as the cube. Pinned in Task 3.
5. **No-JavaScript / keyboard / dark-theme use**: all records, primary links, disclosure controls and figure meaning remain available with no client script and in either colour scheme. Pinned in Tasks 1, 4 and 5.

---

## File and interface map

| Path | Single responsibility |
| --- | --- |
| `_layouts/research_atlas.html` | Research-only hero, title, intro, jump links, overview illustration and content wrapper. Extends `default`. |
| `_pages/research.md` | Original canonical record loop, projects, visits and anchors; switches to dedicated layout. |
| `_includes/research_overview_visual.html` | Small static introductory SVG with localized `title`/`desc`. |
| `_includes/research_area_panel.html` | A research chapter. Inputs `area` (localized record), `canonical_id` (string), `ordinal` (integer). |
| `_includes/research_area_visual.html` | Static dispatch by `canonical_id`; unmatched IDs result in no visual. |
| `_includes/research_figures/{fatigue,weld,additive,testing}.svg` | One physically limited diagram per research area, static and included inline. |
| `scripts/generate_research_atlas_figures.py` | Deterministically generate/check the geometrically defined fatigue SVG; no web access. |
| `_sass/_research_atlas.scss` | Research-only composition, palette, responsive behaviour, focus and contrast. |
| `assets/css/main.scss` | One additional import after `stress_visual`. |
| `_data/i18n/{en,it}/ui.json` | Matching localization keys for jump links and informational captions, only as required. |
| `tests/test_research_atlas.py` | Source-level contracts and geometry, run in the existing pre-build `unittest` suite. |
| `scripts/verify_research_atlas.py` | Post-build HTML, link, label and figure-structure verification for EN/IT. |
| `scripts/check_browser.py` | Visual bounds, touch targets, deep links and keyboard smoke checks for Research. |
| `.github/workflows/{build,preview}.yml` | Execute `verify_research_atlas.py` **after** each successful Jekyll build. |
| `docs/scientific-figures/research-atlas.md` | Diagram assumptions, labels, limitations and review evidence. |

Interface contract: use `include.area`, `include.canonical_id`, `include.ordinal`. Do not introduce a second table of research areas, a new global layout, or a generic site-wide figure registry. `scripts/verify_research_atlas.py` accepts one positional argument `_site` and exits nonzero with named failures.

## Task 1: Research page shell and editorial hero

**Files:**
- Create: `_layouts/research_atlas.html`
- Create: `_includes/research_overview_visual.html`
- Create: `_sass/_research_atlas.scss`
- Modify: `_pages/research.md` (front matter and opening intro only)
- Modify: `assets/css/main.scss` (append stylesheet import)
- Modify: `_data/i18n/en/ui.json`, `_data/i18n/it/ui.json` (paired, minimal labels)
- Create: `tests/test_research_atlas.py`

**Interfaces:**
- Consumes: the unchanged English fallback of `research.intro`, Italian translation `site.data.i18n.it.texts['research.intro']`, and the five existing anchors.
- Produces: `<div class="post research-atlas">` containing one hero and `{{ content }}`; research content is still supplied by the existing page.

- [ ] **Step 1: Write failing `ResearchAtlasSourceTests.test_layout_and_localized_intro`.** Assert `_pages/research.md` uses `layout: research_atlas`; `_layouts/research_atlas.html` extends `default`, declares one `h1`, contains one `{% locale research.intro %}` block, the existing English fallback, and `{{ content }}`; `main.scss` imports `research_atlas` once; both UI JSON objects have identical key sets. Add `test_jump_link_targets` for `#research-areas`, `#projects`, and `#international-collaborations`.

- [ ] **Step 2: Run the focused test and observe the initial failure.** Run `python -m unittest discover -s tests -p "test_research_atlas.py" -v`; expected FAIL, since the layout does not exist yet.

- [ ] **Step 3: Add the smallest page shell.** Move the existing `research.intro` locale block verbatim from the page into the new layout, without duplicating the source. Place the original page title and description in its hero; add three anchored links and the static overview illustration (not an experimental graph). Use `{{ content }}` once. Use a `figure` and localized accessible caption, keeping `h1` singular.

- [ ] **Step 4: Implement scoped Sass and locale keys.** Style only `.research-atlas` and `body` selectors tied to `page.translation_key == 'research'` if a wider `main` is needed. Keep text-first mobile ordering, maximum readable prose width, and `scroll-margin-top` on deep-link headings. Add EN/IT keys for newly authored UI labels using identical keys, not separate pages.

- [ ] **Step 5: Verify, then commit.** Run `python -m unittest discover -s tests -p "test_research_atlas.py" -v`, `bundle exec jekyll build --trace`, `python scripts/verify_site.py _site` and `python scripts/verify_languages.py _site`; all must pass. Commit the page shell, overview, stylesheet and tests as `feat: add Research Atlas page shell`.

## Task 2: Four canonical research chapters

**Files:**
- Create: `_includes/research_area_panel.html`
- Modify: `_pages/research.md` (four-area loop only)
- Modify: `tests/test_research_atlas.py`

**Interfaces:**
- Consumes: `include.area` (localized record), `include.canonical_id` (original record ID), `include.ordinal` (1 through 4).
- Produces: four `section.research-area` elements within `#research-areas`. Keep `id="{{ include.canonical_id }}"` on each existing `h2`; retain `.research-summary`, `.research-methods`, `.inline-links` and `details.context-details`.

- [ ] **Step 1: Add failing `test_four_canonical_chapters`.** Assert the page still loops over `site.data.research_areas` and `localized_record: 'research_areas'`, includes one panel per record and passes canonical ID plus `forloop.index`. Assert the include retains the exact `local_url | relative_url` link transformation and `details` semantics; no JSON or translated text is copied into new arrays.

- [ ] **Step 2: Run the focused test and observe failure.** `python -m unittest discover -s tests -p "test_research_atlas.py" -v`; expected FAIL because the include is not present.

- [ ] **Step 3: Extract and restyle the chapter.** Move the existing section markup to `research_area_panel.html` while preserving every summary, method, visible link, and further-study destination. Display ordinal `01`–`04` from `include.ordinal` using Liquid formatting; add semantic chapter content and a figure slot that can remain empty if no SVG is available. Do not introduce a new data source.

- [ ] **Step 4: Verify rendered EN/IT equivalence and commit.** Run the focused tests, Jekyll build, site and language verifiers. Compare rendered chapter ID order and counts, primary/further link destinations and Italian labels to the pre-change baseline. Commit as `feat: render canonical research chapters`.

## Task 3: Four scientifically constrained, static SVG figures

**Files:**
- Create: `_includes/research_area_visual.html`
- Create: `_includes/research_figures/fatigue.svg`, `weld.svg`, `additive.svg`, `testing.svg`
- Create: `scripts/generate_research_atlas_figures.py`
- Create: `docs/scientific-figures/research-atlas.md`
- Modify: `_includes/research_area_panel.html`
- Modify: `tests/test_research_atlas.py`

**Interfaces:**
- Consumes: only `include.canonical_id`; unknown IDs or a missing include dispatch must render no SVG without affecting the chapter.
- Produces: at most one appropriately labelled, static inline SVG per canonical chapter. Fatigue figure geometry comes from `traction_components(sigma, normal)` and `project_iso(vector)` in `scripts/generate_research_atlas_figures.py`.

**Fixed scientific example for reproducibility:** Illustrate the symmetric Cauchy tensor `sigma = [[0,0,0.6],[0,0,0],[0.6,0,1]]` in arbitrary normalized units, with unit candidate-plane normal `n=(1,0,1)/sqrt(2)`. Then `t = sigma*n = (0.6,0,1.6)/sqrt(2)`, the normal traction magnitude is `sigma_n = n·t = 1.1`, and the tangent traction vector is `t - sigma_n*n = (-0.5,0,0.5)/sqrt(2)`. The 3D dot product between `n` and the tangent traction must equal zero; use the single projection `P(x,y,z)=(sqrt(3)/2*(x-y), (x+y)/2-z)` for all visible geometry and arrows. The figure is an example, not data or a second homepage animation.

- [ ] **Step 1: Write failing `ResearchAtlasFigureTests` methods.** `test_fatigue_traction_decomposition` asserts the values above to within `1e-9` and symmetry of the tensor; `test_projected_vectors_share_one_mapping` checks `project_iso` against the fixed projection; `test_four_svg_figures_and_total_size` requires four parseable SVGs and fewer than 35,000 bytes combined; `test_unknown_figure_id_falls_back_to_text` verifies the dispatch contains no unconditional SVG.

- [ ] **Step 2: Observe failures.** Run `python -m unittest discover -s tests -p "test_research_atlas.py" -v`; expected FAIL because the generator, dispatch and SVG files do not yet exist.

- [ ] **Step 3: Implement the verified fatigue model and generator.** Define `traction_components(sigma: list[list[float]], normal: tuple[float,float,float]) -> tuple[tuple[float,float,float], tuple[float,float,float]]` returning normal and shear traction vectors; define `project_iso(vector: tuple[float,float,float]) -> tuple[float,float]`. Normalize the plane normal or reject a zero-length vector. Generate the fatigue SVG deterministically, including the plane, projected traction arrows and arrowheads. Support `python scripts/generate_research_atlas_figures.py --check` to detect outdated committed output.

- [ ] **Step 4: Add the remaining SVGs and dispatch.** `weld.svg` depicts only a generic weld cross-section and qualitative zone labels; `additive.svg` depicts a generic layered build/path without a thermal field; `testing.svg` depicts a specimen with paired, consistent axial loading arrows and abstract measurement markers. Ensure SVG IDs do not collide when embedded in one HTML page. Add localized accessible captions for all figures, avoiding claims of measured fields. Link dispatch to the chapter figure slot.

- [ ] **Step 5: Validate scientific notes and commit.** Document assumptions and limitations for all four images in `docs/scientific-figures/research-atlas.md`. Run unit tests, generator `--check`, Jekyll build, site and language verification. Confirm an unknown-area fixture still exposes title, methods, links and disclosure while omitting the figure. Commit as `feat: add reviewed Research Atlas schematics`.

## Task 4: Projects, international visits and collaboration panels

**Files:**
- Modify: `_pages/research.md` (projects and remaining sections)
- Modify: `_sass/_research_atlas.scss`
- Modify: `tests/test_research_atlas.py`

**Interfaces:**
- Consumes the existing `_includes/research_project.html`, `_includes/international_experiences.html` and localized `research.contact` block unchanged.
- Produces differentiated section composition while preserving `#projects`, `#selected-collaborative-projects`, `#international-collaborations`, `#research-environment` and all existing FABER markup.

- [ ] **Step 1: Add failing `test_projects_and_visits_preserved`.** Assert Research uses the existing project and visit includes, retains the `data-project="faber"` output through that include, keeps `details.previous-projects`, and retains the lab/thesis route links and localized contact block. Assert the five legacy navigation IDs are present.

- [ ] **Step 2: Run focused tests and observe failure.** `python -m unittest discover -s tests -p "test_research_atlas.py" -v`; expected FAIL until new presentation wrappers and classes are introduced.

- [ ] **Step 3: Implement the new presentation wrappers.** Add an editorial dark project panel scoped to the Research page; retain the current project include and FABER role list without copying data. Style previous projects, visits, cross-links and contact consistently with the approved homepage. Do not place previous projects inside an additional disclosure or alter the international visit structure.

- [ ] **Step 4: Run tests and commit.** Run unit tests, Jekyll build, `verify_site.py`, `verify_languages.py` and the existing browser smoke script. Confirm long Italian roles wrap at narrow widths. Commit as `feat: style Research projects and collaborations`.

## Task 5: Generated-page checks, responsive QA and Cloudflare review handoff

**Files:**
- Create: `scripts/verify_research_atlas.py`
- Modify: `scripts/check_browser.py`
- Modify: `.github/workflows/build.yml`, `.github/workflows/preview.yml`
- Modify: `tests/test_research_atlas.py`
- Modify: `docs/scientific-figures/research-atlas.md` (review notes only)

**Interfaces:**
- `verify_research_atlas(root: pathlib.Path) -> None` raises an informative exception on a failed check; CLI `python scripts/verify_research_atlas.py _site` returns exit code 0 on success, nonzero otherwise.
- `check_browser(root)` adds scoped checks on Research routes while retaining the rest of the site's existing smoke tests.

- [ ] **Step 1: Write failing rendered-contract tests.** For `research/index.html` and `it/research/index.html`, require exactly one `main` and `h1`, four research-area IDs in canonical order, four chapter figures with localized names/captions, all deep-link targets, preserved project role text and existing research output links. Compare canonical and localized records using the existing `verify_languages.py` behaviour. A missing visual fixture must not suppress the chapter or its links.

- [ ] **Step 2: Prove the checks reject an incorrect build.** On a fixture HTML directory, remove one chapter ID, suppress one role, or corrupt one figure caption. Run `python scripts/verify_research_atlas.py <fixture-dir>`; expected nonzero and an actionable error for each case.

- [ ] **Step 3: Finish the post-build verifier.** Implement `verify_research_atlas(root)` using the standard-library `HTMLParser` and existing canonical JSON data. Preserve integration with `verify_site.py` and `verify_languages.py`; do not duplicate general site validation. Both build and preview workflows must call this script immediately after their existing page/language verifiers, never before `jekyll build`.

- [ ] **Step 4: Extend browser smoke checks.** At minimum assert Research figure bounds, no horizontal overflow, mobile one-column stacking, 44 px primary-link/disclosure targets, content in EN/IT and visible headings on deep links under the fixed navbar. Add 320 and 1920 px to the existing 375/390/768/1280 matrix **only if** it can be done without destabilizing unrelated pages; otherwise add a scoped Research-only pass at those widths. Exercise `details` via Enter/Space, keyboard focus, no-JavaScript rendering and light/dark themes.

- [ ] **Step 5: Run final local gate, then commit.** In order: `python -m unittest discover -s tests -v`; `python scripts/generate_research_atlas_figures.py --check`; `bundle exec ruby scripts/check_localization.rb`; `bundle exec ruby scripts/check_recent_publications.rb`; `bundle exec jekyll build --trace`; `python scripts/verify_site.py _site`; `python scripts/verify_languages.py _site`; `python scripts/verify_research_atlas.py _site`. The existing `scripts/verify_site.py` invokes `check_browser(root)` automatically, so do not run `scripts/check_browser.py` as a standalone command. Treat a printed `SKIP` as missing browser coverage rather than visual validation. Record screenshots for English and Italian Research at 320, 390, 768, 1280 and 1920 px in light and dark themes. Commit as `test: verify bilingual Research Atlas and accessibility`.

- [ ] **Step 6: Push and verify PR #30 without merging.** Request an independent code/science review, verify the GitHub build, generated verification and Cloudflare preview jobs all pass for the **exact PR head SHA**, and compare the diff against `master` for unintended changes. Open `https://pr-30.academic-website-preview.pages.dev/research/` and `https://pr-30.academic-website-preview.pages.dev/it/research/` only once deployment succeeds; check actual browser rendering and noindex headers. Attach preview URLs, screenshots and an implementation checklist to PR #30, then request the user's explicit visual approval. Do not mark ready, merge or deploy to production before approval.

## Execution discipline

- Use an isolated branch/worktree at execution time; the existing spec-and-plan branch is `design/phase-3-research-atlas`.
- Read this plan alongside the approved spec; implement one task at a time, with a red test before each change, a green test afterwards, a commit and a reviewer gate.
- Stop for a newly discovered scientific inconsistency rather than adjusting a figure to look plausible.
- Preserve any interim documentation and test artifacts so the user can resume review without repeating work.
- Phase 3 ends with a Cloudflare preview and reviewable draft PR, not an automatic production merge.
