# Academic website audit and improvement record

Audit date: 15 October 2026. Baseline: `95b9830de5d070555db449388aa5a755939797a4` on `master`. Proposed changes: `codex/academic-site-audit-2026-10-15`.

## A. Repository health assessment

**Overall:** Jekyll with al-folio is appropriate for this academic portfolio. Keep the static architecture, Markdown pages, BibTeX bibliography, JSON Resume, and existing GitHub Pages deployment. A framework migration or database would add maintenance cost without addressing the observed problems.

The complete recursive source manifest contained **311 files** in **357 tree entries**, totalling **146,131,070 bytes** (about 139 MiB of tracked file contents; this is not Git history size or browser transfer size). Inspection covered configuration, active pages, layouts/includes, custom Ruby plugins, styles and local scripts, structured content, documentation, workflow, branch metadata and recent history. Binary assets were inventoried by path/size/hash; scientific PDFs and archives were not exhaustively opened or audited internally.

The default branch is `master`; `gh-pages` also exists. Neither branch was reported protected and the ruleset endpoint returned an empty list. Recent commits use vague messages such as “Modifica”. The latest existing deployment for the baseline succeeded. Existing branches and history are preserved.

| Priority | Finding at baseline | Consequence / response |
| --- | --- | --- |
| Essential | MathJax include loads `polyfill.io` | Remove the legacy request. The service was involved in a documented supply-chain compromise; this does not establish that this particular site was exploited. |
| Essential | CSS cache digester reads `assets/_sass`, while Sass lives in `_sass` | CSS changes can keep the same empty-input hash. Hash actual Sass/CSS sources and configuration; add a regression check. |
| Essential | Two course pages reference nonexistent `Lastra_con_foro_CAD.zip` | Correct both to the existing `Lastra_con_foro.zip`. |
| Essential | Build workflow has Pages write and OIDC permissions at workflow scope, no PR checks, and path filters omit standalone teaching-download updates | Restrict write permissions to deploy, validate PRs, and build all master pushes. |
| Essential | Ruby 3.2 is beyond upstream support in October 2026 | Move the workflow to Ruby 3.3 and require the build to validate compatibility. |
| Recommended | Ruby gems are unversioned and no `Gemfile.lock` is committed | A prior successful build did not make the next resolution reproducible. A real lockfile was captured from the successful GitHub build, committed, rebuilt, and checked against Ruby advisories. |
| Recommended | Actions use movable major tags | Pin the existing action families to commit SHAs resolved from their official repositories; configure monthly update proposals. |
| Recommended | Large theme README dominates project documentation | Provide a website-specific README and preserve the original in `docs/THEME_README.md`. |
| Recommended | Template assets, example data and historical reports remain | Exclude documentation and known template pages from deployment; retain files until references and external uses can be verified. |

Dependency assessment at baseline was **incomplete**: no resolved Ruby lockfile was available and local package/audit commands could not run in this session. The review branch now includes the real lockfile from the successful hosted build and Ruby/npm advisory checks. Ruby advisory and npm audit checks subsequently reported no known vulnerabilities for the committed dependency sets. This does not certify vendored/CDN browser libraries or all possible vulnerabilities. npm contains formatting tools rather than an application runtime bundle. Bootstrap, MDB, jQuery, MathJax and Distill remain part of the existing theme. Remove or upgrade these incrementally only with representative rendering checks. The dormant external-feed plugin and its gems remain because removing them without a successful dependency/build evaluation is premature.

Exact duplicate blobs include the introductory teaching PDF at `assets/pdf/_0_Introduzione.pdf` and `TeachingMaterial/Ingegneria_Energetica/PMMEF/Introduzione_EN.pdf`, a theme screenshot, and two report badges. None is deleted because download URLs and historical references may still matter.

## B. Website and scientific content assessment

**Strengths:** clear identity and Pisa affiliation; substantial bibliography; DOI data and downloadable papers; selected publications; research explanations with equations; a structured career record; public course materials; an established restrained theme with dark mode.

**Weaknesses:** Publications is available through a Research dropdown rather than a direct navigation item; no research overview; metadata still describes a theme; the teaching overview duplicates a complex project-card template; several controls are mouse-oriented; page landmarks and image alternatives need work; template biography/CV data is still present; science content has specific bibliographic errors.

| Before | Change and practical benefit |
| --- | --- |
| Publications nested in a Research dropdown; homepage research link points directly to the bibliography | Expose Publications and add Research, with topic summaries linked to existing BibTeX anchors. |
| Teaching overview repeats roughly 1.6 KB of conditional card layout | Use a short list generated from the same existing course collection; stable course URLs and files remain. |
| Abstract/Bib links are anchors without destinations | Use native details/summary controls supporting keyboard operation and operation without JavaScript. |
| Author truncation uses a mouse-click span | Show the full author list by default. |
| Empty thumbnail columns reduce bibliography space | Disable unused publication thumbnails. |
| Entry month/year variables can retain preceding values | Reset both for every bibliography entry; avoid displaying a previous paper’s month. |
| No visible DOI resolver links | Generate DOI links directly from the existing DOI field. |
| Search include refers to a missing script and is disabled | Add a small local text filter with result announcements. It adds no framework or dependency. |
| Generic site/CV descriptions; malformed Scholar query suffix | Use specific factual descriptions and the existing Scholar account ID. |
| Metadata concatenates social links and interpolates JSON strings manually | Serialize a Person/WebSite/WebPage graph and publication records using JSON filters. |
| Stale manually generated 2024 sitemap | Generate sitemap entries from current pages and documents at build time, without invented modification dates. |
| No skip link/main landmark; low-contrast light accent; icon-only links | Add landmarks, skip navigation, focus indicators, labels, a darker light-theme accent, and reduced-motion support. |
| Math, badge, analytics and table resources requested broadly | Remove the obsolete polyfill; disable analytics and badge widgets by default; load Bootstrap Table only on opted-in pages; enable font swapping. |

The portrait original is **2,286,210 bytes**. Preserve it and use the existing WebP generation at responsive widths; request the homepage portrait eagerly and other figures lazily. Correct the previous global image-error handler so one failed responsive image does not alter every image. Actual transfer savings and Core Web Vitals remain unmeasured.

### Bibliographic corrections supported by sources

- `Chiocca2021`: the attached abstract describes critical-plane algorithms rather than the residual-stress paper identified by DOI `10.1016/j.ijmecsci.2021.106401`. Remove the misattributed abstract; retain the record, DOI, publisher, PDF and selection. The original text remains in Git history. A replacement abstract requires accurate attribution, not an invented rewrite.
- `Chiocca2024`: the PDF points to the 2023 Fatemi-Socie paper. Replace the link with the publisher’s open PDF for `10.3221/IGF-ESIS.67.11`; retain the existing local PDF for its correct record.
- `Chiocca2022b`: change publication year from 2021 to 2022, supported by Procedia Structural Integrity volume 38 (2022). The BibTeX key remains unchanged to preserve anchors.
- `Moda2022a`: the record explicitly describes a dataset with a Mendeley Data DOI. Use `misc` rather than representing it as a journal article.
- Remove the duplicate `dimensions` field in `Chiocca2021`.
- Replace the Einstein Twitter placeholder in JSON Resume with academic profile URLs already present in site settings. Replace the unused fallback CV’s Einstein positions and awards with a minimal factual fallback.
- Clean stray trailing punctuation in existing award descriptions without adding or reinterpreting achievements.

No new publications, appointments, dates, degrees, achievements, collaborations, or supervision responsibilities are invented. Research summaries are grounded in the existing home text, bibliography and CV. The primary source remains the bibliography; no duplicate publication database is added.

### Content needing owner confirmation

1. Confirm that “Research fellow” and the 2025–present entry remain current in October 2026; confirm earlier appointment titles and dates as recorded.
2. The bibliography ends in 2024. Determine whether later outputs are missing; do not infer them from inactivity.
3. Confirm teaching academic years and responsibilities. One course still says materials are under preparation. Supervision information is absent.
4. Review the complete PDF CV against JSON Resume and confirm permitted sharing of publisher PDFs, teaching archives and industrial material.
5. Check the research-note date/filename discrepancies. Existing front-matter dates and public URLs are preserved.
6. Confirm projects, funding, research groups, and collaborators before adding dedicated project descriptions.

## C. Changes implemented

The existing Jekyll/al-folio identity and deployment model remain. Targeted changes address scientific accuracy, navigation, metadata, accessible interactions, responsive assets, caching, privacy defaults, and CI safeguards. No academic document, teaching archive, branch or historical commit is deleted. Known theme demo pages and the three sample announcements are excluded from publication while their sources remain. The former Research dropdown is replaced by direct Publications and Research links.

Files added or modified:

- `_config.yml`
- `_pages/about.md`
- `_pages/publications.md`
- `_pages/cv.md`
- `_pages/research.md`
- `_pages/teaching.md`
- `_projects/1_project.md`
- `_projects/2_project.md`
- `_projects/4_project.md`
- `assets/json/resume.json`
- `_data/cv.yml`
- `_includes/metadata.html`
- `_layouts/default.html`
- `_layouts/distill.html`
- `_includes/header.html`
- `_layouts/about.html`
- `_includes/figure.html`
- `_layouts/bib.html`
- `assets/js/common.js`
- `_includes/bib_search.liquid`
- `assets/js/bibsearch.js`
- `_includes/scripts/mathjax.html`
- `_includes/scripts/analytics.html`
- `_includes/head.html`
- `_includes/scripts/misc.html`
- `_plugins/cache-bust.rb`
- `_sass/_academic.scss`
- `assets/css/main.scss`
- `_layouts/cv.html`
- `_includes/social.html`
- `sitemap.xml`
- `_bibliography/PersonalPub.bib`
- `scripts/verify_site.py`
- `scripts/check_cache_bust.rb`
- `.github/workflows/build.yml`
- `.github/dependabot.yml`
- `docs/THEME_README.md`
- `README.md`
- `Gemfile.lock`
- `docs/ACADEMIC_SITE_AUDIT.md`

## D. Verification record

- Repository source inventory: complete manifest, not truncated.
- Bibliography source checks: 25 uniquely keyed records; no duplicate field names after the targeted correction; every local publication PDF reference exists in the source manifest.
- Teaching source checks: all 28 local download references across the three populated course pages resolve to existing source files after the two corrections.
- Live home, publications and CV pages were readable through web retrieval. Some other routes returned retrieval/cache errors; these are inconclusive and are not labelled as confirmed website 404s.
- Jekyll compilation and the stylesheet cache regression check passed on the review branch. Generated-site checks exposed six broken tag/category shortcuts inherited from theme examples; these are removed. Final generated-site verification passed: 28 HTML pages and 774 local references; core metadata, publication JSON-LD and sitemap checks passed. Ruby advisory checks (database updated 10 October 2026, commit a6847b0651a702488f5844081e848dd1ec9dbf1d) and npm audit both reported no known vulnerabilities.
- New CI checks cover Ruby/npm advisory audits, stylesheet fingerprint changes, Jekyll compilation, generated local file references, core metadata/landmarks, publication JSON-LD, and sitemap entries.
- Local command execution and interactive browser inspection failed because the available host processes could not start. Hosted Jekyll compilation and automated site/advisory checks passed. Local lint, viewport screenshots, keyboard interaction, assistive-technology testing, automated browser accessibility scans, Lighthouse, and field performance measurements are not completed.
- External DOI/publisher/profile endpoints can deny automated requests. Sample bibliographic corrections were verified with primary sources; a complete external-link status audit is not claimed.
- The PR remains separate from production. A successful PR build establishes compilation and the included checks, not comprehensive WCAG conformance or production deployment success.

## E. Remaining recommendations

**Essential before merging:** inspect desktop/tablet/mobile and keyboard behavior on the built result; confirm the role/current-affiliation content and bibliographic corrections. Review generated structured data and the new sitemap. Retain the production deployment until review is complete.

**Recommended next:** review ongoing dependency advisory results and vendored browser dependencies; measure actual Lighthouse and field Core Web Vitals; review publication PDF sharing rights; synchronize the PDF and web CV; add teaching years and confirmed research projects; enable branch protection with required checks through repository settings.

**Optional:** add curated publication-type sections after reviewing Procedia/conference classifications; replace third-party fonts with locally hosted files; curate downloadable research data/software links; compress unusually large PDF copies while preserving originals and URLs. A database, CMS, framework migration, elaborate animation and a wholesale redesign are unnecessary.

## Evidence

- [Baseline source](https://github.com/andreachiocca/andreachiocca.github.io/tree/95b9830de5d070555db449388aa5a755939797a4)
- [Existing successful deployment](https://github.com/andreachiocca/andreachiocca.github.io/actions/runs/18683975589)
- [2021 residual-stress paper, publisher](https://www.sciencedirect.com/science/article/pii/S0020740321001363)
- [2022 proceedings paper, publisher](https://www.sciencedirect.com/science/article/pii/S245232162200258X)
- [FSAE paper, institutional repository](https://arpi.unipi.it/handle/11568/1236469)
- [FSAE paper, publisher](https://www.fracturae.com/index.php/fis/article/view/4626)
- [Cloudflare’s primary account of the polyfill.io incident](https://blog.cloudflare.com/automatically-replacing-polyfill-io-links-with-cloudflares-mirror-for-a-safer-internet/)
- [Ruby upstream maintenance status](https://www.ruby-lang.org/en/downloads/branches/)

### Additional verification evidence

Source-based contrast calculations: original cyan on white 3.34:1; revised accent on white 6.04:1; revised secondary text on white 6.10:1; dark accent on the existing dark background 8.73:1. These are selected color-pair measurements, not a complete WCAG audit. Six publication-filter behavior checks passed in an isolated JavaScript harness (initial count, progressive reveal, combined year/text matching, empty groups, no matches, and reset); actual browser interaction remains outstanding.

### Final hosted verification

[GitHub Actions run 38719041748](https://github.com/andreachiocca/andreachiocca.github.io/actions/runs/38719041748) checked code commit `50c735a8b663bc46b37a68ec1ba981814033b030`. Jekyll build, cache regression checks, generated-site validation, Ruby advisory audit, and npm audit passed. Production deployment was intentionally skipped for the pull request. The final follow-up commit changes only this excluded audit document.

The vendored Bootstrap files identify version 4.6.2, which is an end-of-life major series ([upstream status](https://getbootstrap.com/docs/4.6/end-of-life/)). They remain a maintenance concern outside Ruby/npm coverage. The unused local MDB JavaScript identifies MDB5 6.4.0 while active includes use CDN MDB 4.20.0; this reinforces the need to review references before attempting asset deduplication or library substitution.
