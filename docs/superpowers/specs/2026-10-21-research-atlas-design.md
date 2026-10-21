# Phase 3 Research Atlas Design Specification

**Date:** 21 October 2026  
**Status:** Awaiting review and written-spec approval  
**Project:** [Academic website](https://andreachiocca.github.io/)  
**Repository:** [andreachiocca/andreachiocca.github.io](https://github.com/andreachiocca/andreachiocca.github.io)  
**Proposed branch:** `design/phase-3-research-atlas`

## 1. Objective and agreed direction

Extend the approved **Technical Editorial** design from the Phase 2 homepage to the existing Research page. The page should communicate four areas of research, their methods and related scientific outputs more clearly. It should retain the minimalist blue and teal design, monospaced display typography, numbered sections, restrained technical diagrams, and accessible layouts introduced in the homepage.

The design direction, **Technical Research Atlas**, was approved in conversation on 21 October 2026. That approval establishes the visual direction and permits this written specification. It does not authorise implementation or merging Phase 3.

The primary audiences are researchers, potential academic and industrial collaborators, students considering a thesis, and readers following publications or software links. They should be able to identify a relevant research area, understand the main methods, and reach the corresponding evidence without searching through long uninterrupted text.

## 2. Existing architecture and preservation requirements

The existing page is `_pages/research.md`, with `translation_key: research`, English route `/research/`, and an automatically generated Italian route `/it/research/`. Its four research areas come from `_data/research_areas.json`, with descriptive Italian fields in `_data/i18n/it/research_areas.json`. Section summaries, methods and resource links are rendered using `localized_record: 'research_areas'`. Do not create separate English and Italian page bodies or duplicate research records.

Projects are sourced from `site.data.resume.projects` and rendered through `_includes/research_project.html`. International experiences are rendered through `_includes/international_experiences.html`. Neither collection nor include should be copied into independent Phase 3 data files.

Keep unchanged:

- The page routes, `translation_key`, title, metadata, language switcher and reciprocal canonical/hreflang links.
- The four canonical research-area IDs and their order.
- The current summaries, technical methods, selected links, additional-study links, publication keys, external URLs and research data references.
- FABER and other project names, action dates, programme information, verified role descriptions and links, including `data-project="faber"`.
- The existing `<details>` affordances for technical context and previous projects.
- Section targets `#research-areas`, `#projects`, `#selected-collaborative-projects`, `#international-collaborations`, and `#research-environment`. Existing navigation and deep links depend on some of these IDs.
- The global navigation, common footer, homepage visual, publications, repository catalogue, laboratory, teaching, thesis and CV pages.

Do not add unverified claims about equipment, validation, research impact, scientific results or personal contributions. Apply the installed academic writing style guide to any necessary EN/IT interface wording. Existing reviewed narrative text should not be rewritten merely to fit the layout.

## 3. Page composition

### 3.1 Research introduction

Use a research-specific editorial layout with a larger visual area than the current generic page header.

On desktop, create a restrained two-column composition. The left column contains the existing page title, its existing introduction, and a compact set of three or four internal jump links. The right column contains one small static technical overview drawing, framed in the dark blue design used for the homepage illustrations. At intermediate widths, the illustration can sit below the introduction. On mobile, stack all elements vertically with text first.

The overview drawing should visually connect analytical modelling, numerical analysis and experimental investigation without asserting that every study uses all three approaches or follows one mandatory sequence. It is a conceptual map, not a scientific result. Use a localized figure label and a brief caption. Do not introduce another animated stress figure or repeat the homepage animation here.

Only one semantic `<h1>` should appear, followed by a consistent hierarchy of `<h2>` and `<h3>` elements.

### 3.2 Research areas

Keep the four areas, in their current canonical order:

1. **Fatigue assessment** (`multiaxial-fatigue-and-critical-plane-methods`).
2. **Welded structures and residual stresses** (`residual-stresses-and-welded-structures`).
3. **Additive manufacturing** (`additive-manufacturing-and-material-behaviour`).
4. **Materials and component testing** (`component-testing-and-industrial-applications`).

Represent them as **four stacked editorial research chapters** rather than a dense 2-by-2 card grid. Each chapter displays a quiet ordinal marker (01 to 04), the localized title, the existing summary, the existing methods, its primary resource links and the existing collapsible further-study list.

Use an asymmetric desktop split: readable text and links occupy the larger column, while a small SVG technical figure occupies a consistent adjacent column. Individual chapters may alternate visual alignment only if the reading order and keyboard navigation remain predictable. On narrow screens, place the visual after the title and before the summary, or at the end of the section, while keeping the semantic text order intact.

Section headings must retain their existing `id` attributes so publication and navigation links continue to work. Every primary link remains visible without expanding a disclosure. The `<details>` for additional studies remains keyboard accessible and retains all existing destinations.

### 3.3 Conceptual technical figures and scientific review

The four illustrations should be compact, static inline SVGs sharing the homepage's palette, grid density, stroke language and small figure labels. They are **conceptual schematics**, not computed fields, experimental images, actual equipment drawings or evidence of validation.

| Research area | Proposed subject | Scientific boundaries |
| --- | --- | --- |
| Fatigue assessment | Small stress element with one oriented candidate plane and resolved traction arrows. | Derive all arrows from one stated stress tensor and a common projection. Normal traction must be perpendicular to the plane and shear traction tangential. No unsupported damage contour, fatigue-life prediction or numerical dataset. |
| Welded structures | Schematic welded-joint cross-section with clearly differentiated fusion zone, surrounding material and, where appropriate, a qualitatively indicated heat-affected zone. | Do not invent measured residual stress profiles, heat input, material boundaries or process parameters. The drawing represents geometry only. |
| Additive manufacturing | Simplified stacked layers and an indicated deposition or scan path. | Avoid choosing a specific manufacturing technology or showing a computed thermal field unless the relevant paper or caption supports it. Do not suggest every additive process follows the same path. |
| Materials and component testing | Simplified specimen with an explicitly defined loading direction and abstract measurement markers. | Arrow directions must match the depicted boundary loading; do not show a real machine, sensor configuration, force capacity or dataset without evidence. This is one example, not the full range of laboratory activities. |

For each figure, record its purpose, mechanics/geometric assumptions, visible labels and scientific limitations in the implementation notes. Review coordinates and arrow directions before publication. SVG text may be hidden from assistive technology only if its relevant meaning is fully stated nearby. Informative figures must have a localized accessible name or equivalent caption.

No GIF, extra JavaScript library, remote asset or interactive animation is needed for Phase 3.

### 3.4 Research projects

Below the area chapters, introduce a more prominent project section with the same dark-blue editorial treatment used for the homepage's FABER panel. Retain the existing `#projects` section and `#selected-collaborative-projects` heading anchor.

The current project's title, summary, programme details, dates, group memberships and roles must continue to come from `_includes/research_project.html` and the existing canonical project record. The `data-project="faber"` attribute, working-group lists and their checked textual values must remain intact. The preceding design may add a decorative oversized project identifier, but it must not masquerade as an official logo.

Keep previous projects in their existing `<details class="previous-projects">` section, with unchanged content. If long role lists threaten the compact design, improve wrapping and spacing rather than omitting any item.

### 3.5 International collaborations and contact

Preserve international visits and links from `_includes/international_experiences.html`, and the final research-collaboration contact text. Give these sections matching editorial borders, numbered subheadings and consistent inline links without altering institution names, dates, attribution or destinations.

Retain the existing route links to the laboratory and thesis pages. Their visual redesign is deferred to a later phase.

## 4. Component architecture

Keep the implementation local to the Research page and avoid a broad refactor of `_layouts/page.html` or the global design system.

Proposed units:

| File | Responsibility |
| --- | --- |
| `_layouts/research_atlas.html` | Page-specific layout extending `default`. Provides the one `h1`, overview hero and a wrapper around existing content. Does not change shared navigation, metadata or `main`. |
| `_pages/research.md` | Switches to the page-specific layout and reorganizes existing research sections while preserving the canonical loop, IDs, project include and locale blocks. |
| `_includes/research_area_panel.html` | Renders one area using the existing localized record and its original links and details. Accepts a numeric index, not another data source. |
| `_includes/research_area_visual.html` | Selects an SVG by an existing canonical area ID. Uses a documented, checked figure for each area. |
| `_includes/research_overview_visual.html` | Renders the static overview illustration for the hero. |
| `_sass/_research_atlas.scss` | Research-only layout, typography, figures, responsiveness, dark theme and focus states, scoped beneath `.research-atlas`. |
| `assets/css/main.scss` | Imports the new Research stylesheet after existing shared styles. |
| `_data/i18n/en/ui.json` and `_data/i18n/it/ui.json` | Add only genuinely necessary figure captions, jump-link labels or screen-reader text, keeping key sets identical. |
| Existing verification scripts and focused new tests | Check preservation, responsive layout, localization and scientific figure contracts. |

A dedicated page layout avoids unintended changes to other pages. Reuse existing CSS custom properties and the Phase 1/2 visual language. Do not create a second CSS build or introduce new Jekyll plugins. The documentation directory is excluded from the published website.

## 5. Responsive and accessible behaviour

The research content may use a wider desktop measure than the old 800 px base layout, comparable to the Phase 2 homepage, while maintaining a comfortable line length for body copy. Test at 320, 375, 390, 768, 1280 and 1920 px. On mobile, chapters use one column and diagrams never hide text or force horizontal scrolling.

Preserve the site's skip link, single `main`, single `h1`, navigation controls, two language choices, focus indication and keyboard operation. Primary links and disclosure summaries should have at least 44 px touch-target height. Decorative figure strokes cannot be the only representation of information. Text contrast must remain legible in light and dark themes; do not use teal-on-navy accents as body text without checking contrast. Deep-link headings require an appropriate scroll margin beneath the fixed navbar.

No automatic motion is proposed. Respect reduced-motion preferences if any purely decorative transitions are retained.

## 6. Data flow and failure behaviour

1. Jekyll renders the canonical `_pages/research.md` once per supported locale using the existing bilingual generation process.
2. The page loops over `site.data.research_areas`. Each record is passed through the existing `localized_record: 'research_areas'` adapter.
3. The area panel renders the provided localized fields; no second list or separate translation schema is introduced.
4. The visual include selects only by the canonical `id`. Missing diagrams must degrade to the complete text-only chapter, not remove or mislabel research records.
5. Existing project, visits and link includes continue to consume the same shared canonical data.
6. If an optional visual cannot render, text, methods, outputs, deep links and accessibility landmarks remain usable without client-side scripting.

No network fetch or runtime API is required. The default browser experience remains static and content-complete.

## 7. Verification and release gates

### Content and structural checks

- English `/research/` and Italian `/it/research/` both build with matching canonical research records and preserved metadata.
- Exactly four research areas are rendered with the four existing IDs and the same order.
- Every existing primary and further-study link still resolves. No bibliography IDs, repository IDs, URLs or published project records change.
- `#research-areas`, `#projects`, `#selected-collaborative-projects`, `#international-collaborations` and `#research-environment` exist and remain navigable.
- The FABER `data-project` attribute and the existing WG3, WG4.3 and WG5.3 role assertions keep passing.
- The previously working disclosure for previous projects and each further-study list remains functional with keyboard and screen-reader navigation.

### Scientific and visual checks

- Each figure has a short design note identifying assumptions and whether it is merely conceptual.
- The fatigue-plane traction arrows follow their stated tensor and plane normal. The welding, additive and testing figures avoid unverified data or apparatus specifications.
- Screen captures are reviewed in English and Italian, at mobile and desktop widths, in light and dark themes.
- The page has no horizontal overflow and no overlapping figures or clipped Italian text.
- The combined original SVG source should remain modest in size, with a planning target below 35 KB before Jekyll minification. No new runtime library or recurring animation loop is permitted.

### CI and preview

- Run the existing Ruby localization and recent-publication checks, Python unit tests, `bundle exec jekyll build --trace`, `scripts/verify_site.py`, `scripts/verify_languages.py`, and browser checks.
- Add focused assertions for four research chapters, project anchors, working groups, figure captions and accessible details.
- Publish the **actual Phase 3 PR branch** through the existing Cloudflare Pages workflow. For PR number `N`, review `https://pr-N.academic-website-preview.pages.dev/research/` and `https://pr-N.academic-website-preview.pages.dev/it/research/`.
- Confirm the production GitHub Pages site remains unchanged while the PR is open. Require explicit visual approval before marking the implementation PR ready and merging.

## 8. Non-goals and next decision

Phase 3 does not redesign Publications, Software and Research Data, Laboratory, Teaching, Thesis or CV. It does not change scientific records, create publication graphics that imply experimental findings, or generalize the homepage animation into every page.

**Approval gate:** Review this specification and request amendments if needed. After explicit written-spec approval, create a detailed implementation plan for review. Only after plan approval should Phase 3 source files and a working Cloudflare preview be implemented.