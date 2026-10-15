# Andrea Chiocca â€” academic website

Personal academic website at [andreachiocca.github.io](https://andreachiocca.github.io), built with Jekyll and the al-folio theme. The site presents publications, research, academic experience, and teaching materials.

## Content map

| Update | Source |
| --- | --- |
| Home introduction and contact details | `_pages/about.md` |
| Research areas and links to representative papers | `_pages/research.md` |
| Scholarly publications | `_bibliography/PersonalPub.bib` |
| Software, benchmarks, datasets and deposit versions | `_data/research_outputs.json` |
| International responsibilities | `_data/academic_service.json` |
| Academic positions, education, and awards | `assets/json/resume.json` |
| Downloadable CV | `assets/pdf/resume_ENG.pdf` |
| Teaching overview | `_pages/teaching.md` |
| Course pages | `_projects/*.md` |
| Teaching downloads | `TeachingMaterial/` |
| Research notes | `_posts/` |
| Site identity and optional features | `_config.yml` |
| Targeted visual refinements | `_sass/_academic.scss` |

The active CV uses JSON Resume. `_data/cv.yml` is a minimal fallback, not a second detailed CV. Course pages retain their existing `/projects/...` URLs.

## Preview and verification

Use Ruby 3.3, Bundler, ImageMagick with WebP support, and Pandoc. Python 3.11 with Jupyter and nbconvert supports the existing notebook plugin.

```sh
bundle install
bundle exec jekyll serve
```

Before opening a pull request:

```sh
bundle exec ruby scripts/check_cache_bust.rb
JEKYLL_ENV=production bundle exec jekyll build --trace
python scripts/verify_site.py _site
```

GitHub Actions runs the build, generated-site checks, and Ruby/npm advisory checks for pull requests. Only a successful build on `master` can deploy through GitHub Pages. Documentation, scripts, theme examples, and historical performance reports are excluded from the published site but remain in this repository.

## Adding a publication

1. Add a uniquely keyed BibTeX record to `PersonalPub.bib`. Preserve author names, title, publication type, year, venue, and DOI exactly as supported by the publisher or institutional repository.
2. Add `bibtex_show={true}` to expose a BibTeX export and `selected={true}` only for papers to highlight on the homepage.
3. Use `html={https://...}` for the publisher landing page. Use `pdf={filename.pdf}` for a file in `assets/pdf/`, or an absolute HTTPS URL for a public version. Verify that the PDF is the correct paper and that sharing it is permitted.
4. Add an abstract only if it belongs to that record. Link a representative paper from the research page using its BibTeX key: `/publications/#KEY`.
5. Preview publications and check the DOI and PDF. Year grouping, DOI links, structured data, and text filtering are generated from the bibliography.

Publications are separated into journal articles, conference contributions and the doctoral thesis, then grouped by descending year. Datasets and archived packages belong in the research-output catalogue, not the scholarly bibliography. The text filter supports titles, authors, years, and terms in the bibliography; all entries remain readable without JavaScript. Publication structured data improves machine readability but does not guarantee search-engine or Google Scholar indexing.

## Updating teaching and career information

Keep course titles, codes, and downloads in the existing course pages. Include the academic year and your role only when confirmed. Update JSON Resume and the PDF CV together when your position changes. Do not infer appointment dates, supervision responsibilities, awards, or collaborators.

The downloadable CV is a sanitized public English PDF. Do not replace it with a signed source CV containing personal contact details or a signature. Keep the public PDF and JSON Resume consistent.

Keep existing post dates and public URLs stable, even when a filename has a historical typo.

## Optional integrations and privacy

Google Analytics, Cronitor, publication badge widgets, and the decorative reading progress bar are disabled by default. Existing integration settings remain available in `_config.yml`. Review privacy requirements before enabling analytics or third-party widgets; this configuration is not a legal compliance certification. Google Fonts and some script libraries still use third-party hosts.

Bootstrap Table loads only on pages with `table: true` in front matter. Native HTML tables do not need it. MathJax loads on research-note (Distill) pages or pages with `math: true`. Masonry is disabled because the teaching overview now uses a plain list.

## Maintenance priorities

- Keep `Gemfile.lock` committed. It records the dependency set resolved by the verified GitHub build. Update it deliberately and rerun the build and advisory checks.
- Review Dependabot updates and periodically audit both the resolved Ruby dependency set and `package-lock.json`.
- Test keyboard navigation, narrow screens, light/dark contrast, and representative research notes before merging visual changes.
- Measure the actual deployed site with Lighthouse and field Core Web Vitals. Historical theme reports are not measurements of this website.
- Preserve documents and download URLs when considering future asset cleanup.

See [the audit and verification record](docs/ACADEMIC_SITE_AUDIT.md) for findings and remaining recommendations. The [original theme README](docs/THEME_README.md), [customization guide](CUSTOMIZE.md), and [theme project](https://github.com/alshedivat/al-folio) remain available.

## Repositories and research outputs

`_data/research_outputs.json` is the single content catalogue. Jekyll renders every card and link at `/repositories/` without contacting GitHub or Zenodo. Category buttons progressively enhance the static page; with JavaScript disabled every record remains visible. No preview-image service is used.

To discover new public repositories and deposits, using Python 3.11 or later:

```sh
python scripts/sync_research_outputs.py           # report discovery; no writes
python scripts/sync_research_outputs.py --write   # refresh the snapshot
python -m unittest discover -s tests -v
```

Review the resulting diff and commit it on a branch. The refresh preserves reviewed descriptions, topic labels, scientific caveats, bibliography keys and existing anchors. New entries are marked `needs_review`: inspect the README/deposit, write a concise description and remove that flag. Use `display_title` for a short card heading while retaining the official `title`. `featured` gives a small number of current research activities first position. `kind` is `software`, `data`, `benchmark` or `other`; benchmarks share the dataset filter. Forks retain upstream attribution.

The script paginates both APIs (Zenodo anonymous page size 25), verifies deposits by ORCID or the verified owner plus exact creator name, groups versions by concept record, and refreshes dates, access, language and fork/archive metadata. A conflicting ORCID is rejected. It keeps missing historical entries for review rather than silently deleting them. GitHub dates are latest default-branch commit dates, not evidence of validation or an undertaking to maintain software. API failures or incomplete searches stop before replacing the content snapshot. `_data/catalogue_status.json` records discovery coverage and identity exclusions; it is refreshed by the same command.

No token is required. An optional `GITHUB_TOKEN` environment variable increases GitHub rate limits and is sent only to `api.github.com`; never commit it. Refreshes are intentionally separate from website builds and require reviewing scientific descriptions. A scheduled workflow is unnecessary for this small catalogue and would risk publishing unreviewed scientific claims.

Preserve the restricted access label on deposit 21875885. Two older supporting-data deposits have publication-type labels in Zenodo: retain their official metadata and the explanatory notes. Do not infer a software archive from a DOI for a related journal article, or attach an upstream project's DOI to a personal fork. When a verified Zenodo software archive represents exactly the same GitHub project, consolidate its identifiers into the existing software card after checking provenance; keep independently useful datasets separate. The card component accepts GitHub and Zenodo links together. The refresh does not guess such cross-source equivalence from similar titles.

`earlier_versions` keeps the DOI and record URL of each version; `doi` identifies the displayed version and `concept_doi` links all versions. Keep `related_publications` as stable BibTeX keys. FABER WG3 co-leadership, WG4.3 software and the upstream FatPy WG6 activity are distinct.

PR builds run catalogue unit checks, the Jekyll build and generated-site/browser checks. They retain a seven-day `catalogue-preview` artifact containing the built catalogue and its CSS, scripts and fonts for review. This artifact does not deploy the site. The existing Pages deployment remains limited to `master`.

See [the catalogue audit](docs/REPOSITORIES_UPDATE.md) for the coverage inventory and implementation decisions.
