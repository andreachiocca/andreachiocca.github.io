# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Academic website of Andrea Chiocca (University of Pisa): Jekyll 4 + a heavily customised al-folio theme, bilingual EN/IT, deployed by GitHub Pages from `master`. `README.md` has the content map and the editorial rules for publications, teaching, the research-output catalogue and laboratory data; read the relevant section before editing content. Planning documents: `docs/site-audit.md`, `docs/site-roadmap.md`, `docs/seo.md`.

## Commands

The Ruby, bibtex and Liquid toolchain needs a UTF-8 locale; without it the build fails with `invalid byte sequence in US-ASCII`.

```sh
export LANG=C.UTF-8 LC_ALL=C.UTF-8
bundle install
bundle exec jekyll serve                                  # local preview
JEKYLL_ENV=production bundle exec jekyll build --trace    # what CI builds
```

Checks run by `.github/workflows/build.yml`, in this order:

```sh
bundle exec ruby scripts/check_cache_bust.rb
bundle exec ruby scripts/check_localization.rb
bundle exec ruby scripts/check_recent_publications.rb
python -m unittest discover -s tests -v                   # source-level tests
python scripts/verify_site.py _site                       # links, metadata, SEO, sitemap + Playwright browser checks
python scripts/verify_languages.py _site
python scripts/verify_research_atlas.py _site
python scripts/verify_outputs_atlas.py _site
python scripts/verify_teaching_thesis_editorial.py _site
```

To run a single test: `python -m unittest tests.test_damage_sphere -v`, or `python -m unittest tests.test_research_catalogue.DiscoveryTests.<name>`.

`verify_site.py` drives a headless Chromium through `scripts/check_browser.py`, at 375, 390, 768 and 1280 px and in landscape. Where CDNs are blocked (jQuery and Bootstrap are loaded from jsdelivr), it reports a few environment-only errors on `master` too, for example "mobile CV contents must not overlay the introduction". Compare against a `master` build before treating a browser error as yours; CI is authoritative.

`bundle-audit` and `npm audit` also run in CI. New Ruby advisories can turn every open PR red at once; fix them with `bundle lock --update <gem> --conservative`.

## Previews and PRs

Every same-repository PR against `master` deploys to `https://pr-<N>.academic-website-preview.pages.dev/` (`preview.yml`, Cloudflare Pages, `noindex`). The owner reviews changes there. A PR must target `master` to get a preview; stacked branches still open their PR against `master`.

## Architecture

**Localisation (`_plugins/localization.rb`).** Italian pages are not separate files. For every page or document whose `translation_key` is listed in `academic_languages` (`_config.yml`), the generator clones it to `/it/...`, merging the front matter from `_data/i18n/it/pages.json`. That file must contain a `description` for each key, and any extra key there, such as `seo_title`, is copied too.
- Short UI strings use `{{ "English text" | t }}`. The English text is the key in `_data/i18n/{en,it}/ui.json`, and both files must have the same key set. A missing Italian key is a fatal build error.
- Long passages use `{% locale key %}English…{% endlocale %}`, with the Italian text in `_data/i18n/it/texts.json`.
- Data records are localised through `localized_record: '<group>'`, using `_data/i18n/it/<group>.json` keyed by record id.
- Institution names use `institution_display` (`it/institutions.json`). Do not add institution names as `ui.json` keys: `verify_languages.py` flags any `ui.json` key that appears untranslated on an Italian page, even inside bibliography data.
- `local_url` maps EN paths to their IT routes.

**Data-driven pages.** Most content is rendered from `_data/*.json` and `assets/json/resume.json` (JSON Resume: positions and projects). Record `id` values double as public URL anchors (for example `#github-achiocca1-ECP`): keep them stable even when the underlying repository moves.

**Research-output catalogue.** `_data/research_outputs.json` is a reviewed snapshot refreshed by `scripts/sync_research_outputs.py`. That script needs GitHub and Zenodo API access; without it, edit the snapshot by hand together with `_data/catalogue_status.json`. Repository identity ignores which owned account (`achiocca1`, `andreachiocca`) holds a repo, so transfers keep cards and exclusions. `_data/catalogue_exclusions.json` must keep FatPy, Moloch, Awesome-CV and the website excluded.

**Publications.** Publications come from `_bibliography/PersonalPub.bib` via jekyll-scholar and `_layouts/bib.html`. `_plugins/recent-publications.rb` picks the five homepage papers.

**Styles.** `assets/css/main.scss` imports the theme, then per-section editorial partials, and `_design_system.scss` **last**; a test enforces this. The design system owns the tokens: warm paper background, editorial blue accent `#2869a7` (`#8bbce9` in dark mode), and `--font-sans` / `--font-serif` / `--font-mono` for the self-hosted Inter, Source Serif 4 and JetBrains Mono in `assets/fonts/` (OFL). The theme sets `--global-*` variables on `html[data-theme='dark']`, so dark-mode overrides must be repeated in that selector. The base theme colours every `span`, `div` and `p` with `--global-text-color`, so text on dark panels needs an explicit `color: inherit` (use `:where()` to keep specificity low). `assets/js/motion.js` fades blocks in using opacity only; transforms break the browser tests' 44 px touch-target measurements.

**Figures generated from research code.** FIG. R02, the Findley damage sphere on the Thesis page (`_includes/damage_sphere.html`, `assets/js/damage-sphere.js`), only draws `assets/data/figures/damage-sphere-findley.json`. That data is produced offline by `scripts/generate_damage_sphere.py`, which calls the owner's `multifat` library (multiaxial-fatigue, pinned commit) once per plane. Never reimplement fatigue criteria in the browser. Regenerating needs `pip install git+https://github.com/andreachiocca/multiaxial-fatigue@<commit>`, and the commit shown in the include must match the JSON. `tests/test_damage_sphere.py` checks the data against closed-form Findley solutions. FIG. 01 on the homepage (`_includes/home_visual.html`, `assets/js/stress-visual.js`) is an illustrative stress element, not data. `tools/generate_og_image.js` renders the Open Graph card from the built FIG. 01.

**SEO.** `_includes/metadata.html` computes one title for `<title>`, `og:title` and `twitter:title`: `seo_title` on the home page, a course-materials suffix on `_projects` pages, otherwise `Page | Andrea Chiocca`. `verify_site.py` requires every sitemap page to have a unique title and a description of 50–160 characters (front matter `description`, `seo_description` for course pages, `it/pages.json` for Italian). `sitemap.xml` is generated in Liquid; set `sitemap: false` on non-indexable pages.

## Content constraints enforced by checks

These are deliberate owner decisions, encoded in `scripts/verify_site.py`, `scripts/check_browser.py` and `tests/`. Change them only with the owner's agreement.
- **Research summaries.** `_data/research_areas.json` summaries must be 20–45 words.
- **Thesis page.** It must keep the placement qualifications "project availability", "host-institution acceptance", "funding and mobility" and "suitable datasets".
- **Laboratory page.** It must keep "departmental", "laboratory staff", "technical feasibility" and "institutional procedures".
- **Home page.** The group appears as "Gruppo di Costruzione di Macchine" with "DICI" in `#research-environment`.
- **Navigation.** The Teaching submenu lists only the Teaching overview and Thesis opportunities. Courses are reached from `/teaching/`.

Owner preferences: concise text (one sentence per idea), visuals generated from the original research code, minimal design with light motion, the blue accent, and scientific accuracy over embellishment. Italian is the working language with the owner. Code comments are in English.
