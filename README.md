# Andrea Chiocca — academic website

Personal academic website at [andreachiocca.github.io](https://andreachiocca.github.io), built with Jekyll and the al-folio theme. The site presents publications, research, academic experience, and teaching materials.

## Content map

| Update | Source |
| --- | --- |
| Home introduction and contact details | `_pages/about.md` |
| Research areas and links to representative papers | `_pages/research.md` |
| Publications | `_bibliography/PersonalPub.bib` |
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

GitHub Actions runs the build and checks for pull requests. Only a successful build on `master` can deploy through GitHub Pages. Documentation, scripts, theme examples, and historical performance reports are excluded from the published site but remain in this repository.

## Adding a publication

1. Add a uniquely keyed BibTeX record to `PersonalPub.bib`. Preserve author names, title, publication type, year, venue, and DOI exactly as supported by the publisher or institutional repository.
2. Add `bibtex_show={true}` to expose a BibTeX export and `selected={true}` only for papers to highlight on the homepage.
3. Use `html={https://...}` for the publisher landing page. Use `pdf={filename.pdf}` for a file in `assets/pdf/`, or an absolute HTTPS URL for a public version. Verify that the PDF is the correct paper and that sharing it is permitted.
4. Add an abstract only if it belongs to that record. Link a representative paper from the research page using its BibTeX key: `/publications/#KEY`.
5. Preview publications and check the DOI and PDF. Year grouping, DOI links, structured data, and text filtering are generated from the bibliography.

Publications are grouped by descending year. The text filter supports titles, authors, years, and terms in the bibliography; all entries remain readable without JavaScript. Publication structured data improves machine readability but does not guarantee search-engine or Google Scholar indexing.

## Updating teaching and career information

Keep course titles, codes, and downloads in the existing course pages. Include the academic year and your role only when confirmed. Update JSON Resume and the PDF CV together when your position changes. Do not infer appointment dates, supervision responsibilities, awards, or collaborators.

Keep existing post dates and public URLs stable, even when a filename has a historical typo.

## Optional integrations and privacy

Google Analytics, Cronitor, publication badge widgets, and the decorative reading progress bar are disabled by default. Existing integration settings remain available in `_config.yml`. Review privacy requirements before enabling analytics or third-party widgets; this configuration is not a legal compliance certification. Google Fonts and some script libraries still use third-party hosts.

Bootstrap Table loads only on pages with `table: true` in front matter. Native HTML tables do not need it. MathJax loads on research-note (Distill) pages or pages with `math: true`. Masonry is disabled because the teaching overview now uses a plain list.

## Maintenance priorities

- Generate and commit a reviewed `Gemfile.lock` after a successful build; Ruby dependencies currently resolve at build time.
- Review Dependabot updates and periodically audit both the resolved Ruby dependency set and `package-lock.json`.
- Test keyboard navigation, narrow screens, light/dark contrast, and representative research notes before merging visual changes.
- Measure the actual deployed site with Lighthouse and field Core Web Vitals. Historical theme reports are not measurements of this website.
- Preserve documents and download URLs when considering future asset cleanup.

See [the audit and verification record](docs/ACADEMIC_SITE_AUDIT.md) for findings and remaining recommendations. The [original theme README](docs/THEME_README.md), [customization guide](CUSTOMIZE.md), and [theme project](https://github.com/alshedivat/al-folio) remain available.
