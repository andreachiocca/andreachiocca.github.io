# Andrea Chiocca — academic website

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
| Thesis directions, approaches and international contacts | `_data/thesis_opportunities.json` |
| Laboratory expertise, measurement context and future equipment | `_data/laboratory.json` |
| Retired Notes source (unpublished) | `docs/retired-notes/` |
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
2. Add `bibtex_show={true}` to expose a BibTeX export. The homepage automatically shows the five most recent published records; no `selected` flag is needed.
3. Use `html={https://...}` for the publisher landing page. Use `pdf={filename.pdf}` for a file in `assets/pdf/`, or an absolute HTTPS URL for a public version. Verify that the PDF is the correct paper and that sharing it is permitted.
4. Add an abstract only if it belongs to that record. Link a representative paper from the research page using its BibTeX key: `/publications/#KEY`.
5. Preview publications and check the DOI and PDF. Year grouping, DOI links, structured data, and text filtering are generated from the bibliography.

The homepage uses `_plugins/recent-publications.rb` and `_includes/recent_papers.html` to select five records from the existing Scholar bibliography at build time, using the same publication layout and DOI links. ISO `date` takes precedence over separate `year`, `month` and `day` fields. Missing month/day sort as 1 January or the first day of the known month; no date is added to the bibliographic display. Undated, explicitly unpublished, accepted/in-press/preprint and future-dated records are excluded. Equal dates use the bibliography key for a stable order. Add a verified exact date when available; year-only ties do not imply a known within-year chronology. `scripts/check_recent_publications.rb` tests date formats, eligibility, ties and automatic selection of a newly added record.

The historical citation badges used Dimensions and Altmetric. Both remain disabled. The Dimensions script responded during this review but contained 532,701 bytes before any follow-up badge requests. Loading this provider for the optional badge is disproportionate to the current homepage; no citation counts are inferred or stored. Existing DOI links, Google Scholar profile and BibTeX exports remain available.

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
- Test keyboard navigation, narrow screens, light/dark contrast, and the thesis and laboratory pages before merging visual changes.
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

`_data/catalogue_exclusions.json` is the single exclusion policy. It contains only the four owner-requested projects (the website, Moloch, FatPy and Awesome-CV). Refreshes skip them during discovery and remove them from retained historical snapshots, including featured entries. Validation rejects their reintroduction. This affects website advertising only; the script never modifies GitHub repositories. `_data/catalogue_status.json` retains the complete discovery inventory and separately records the included count (currently 7 of 11 repositories). The catalogue contains 14 resources, preserving all 6 Zenodo resources and the additional dataset. Keep the multiaxial-fatigue repository included.

No token is required. An optional `GITHUB_TOKEN` environment variable increases GitHub rate limits and is sent only to `api.github.com`; never commit it. Refreshes are intentionally separate from website builds and require reviewing scientific descriptions. A scheduled workflow is unnecessary for this small catalogue and would risk publishing unreviewed scientific claims.

Preserve the restricted access label on deposit 21875885. Two older supporting-data deposits have publication-type labels in Zenodo: retain their official metadata and the explanatory notes. Do not infer a software archive from a DOI for a related journal article, or attach an upstream project's DOI to a personal fork. When a verified Zenodo software archive represents exactly the same GitHub project, consolidate its identifiers into the existing software card after checking provenance; keep independently useful datasets separate. The card component accepts GitHub and Zenodo links together. The refresh does not guess such cross-source equivalence from similar titles.

`earlier_versions` keeps the DOI and record URL of each version; `doi` identifies the displayed version and `concept_doi` links all versions. Keep `related_publications` as stable BibTeX keys. FABER WG3 co-leadership, WG4.3 software and the upstream FatPy WG6 activity are distinct.

PR builds run catalogue unit checks, the Jekyll build and generated-site/browser checks. They retain a seven-day `website-preview` artifact containing the generated pages and their CSS, scripts and fonts for review. This artifact does not deploy the site. The existing Pages deployment remains limited to `master`.

See [the catalogue audit](docs/REPOSITORIES_UPDATE.md) for the coverage inventory and implementation decisions.

## Navigation, research and student resources

`_data/navigation.yml` is the single ordered menu for desktop and mobile. Keep a short label and a stable URL for each section. Teaching course pages and Thesis Opportunities retain Teaching as their parent. Laboratory is a direct navigation entry. The shared navigation controller handles focus, Escape, background interaction and header spacing on every layout.

Edit `_data/research_areas.json` for the brief research summaries (40–70 words), methods and evidence links. Preserve the existing `id` values: datasets and other pages link to these anchors. Publications provide the detailed scientific evidence. Project records live in `assets/json/resume.json` and render consistently on Research and CV. FABER's `working_groups` array is the shared responsibility list. WG3 is Fatigue Estimation Competition (Co-Leader); WG4.3 is Multiaxial fatigue (Participant), officially Load Multiaxiality Effect; WG5.3 is Welding (Participant), officially Welded Joints. Official names and links were checked on the FABER working-group pages; roles follow the owner's current instructions. `periodLabel` can distinguish an Action's overall lifetime from a person's role dates. Do not infer appointment dates from an Action's duration. A one-year project is displayed as one year.

Public educational resources live in `_data/teaching_materials.json`, keyed by the existing course filename. Each entry has `title`, `url`, `format`, `type` and optional `academic_year`. Add an approved public PDF/ZIP to the existing `TeachingMaterial/` directory (or an authorized external repository URL), then add its entry. Course pages automatically group by academic year, when known, and material type. Leave `academic_year` null when the source does not identify it; do not infer a material's year from the teaching appointment. Existing shared resources have no fabricated year labels. Keep restricted materials on the official university platform.

The course front matter identifies `materials_key`, `teaching_period`, `teaching_role` and `teaching_group` (`recent` or `previous`). Verify a new academic-year appointment before extending these periods. The present overview reports documented teaching through 2026 and links current requirements to official university platforms. No new placeholder courses are needed.

### Thesis opportunities and laboratory capabilities

`_pages/thesis.md` presents potential directions, not current vacancies. Edit `directions`, `approaches` and `international_contacts` in `_data/thesis_opportunities.json`. The `projects` array stays empty until a specific proposal is confirmed. Each future project can use `id`, `title`, `description`, `activities`, `mode`, `level`, `status`, `supervisors`, `host`, `location`, `links`, and optional image fields. Use `links` for supporting papers, repositories, official opportunities or a verified contact. Keep availability accurate and retain the international-placement qualifications. No empty project section is rendered.

`_pages/laboratory.md` distinguishes documented research expertise from facilities that need feasibility and access checks. Edit `capabilities` and `measurement_context` in `_data/laboratory.json`. The `equipment` array stays empty until an inventory is verified. Each future instrument uses `id`, `title`, `description`, optional `image`, `image_alt`, `image_width`, `image_height`, supporting `links` and a `specifications` array of `{ "label": "…", "value": "…" }` pairs. Add only confirmed manufacturer/model, force/torque, loading modes, static/cyclic/dynamic capability, frequency, specimen limits, environmental conditions, sensors and acquisition details; omit unknown fields. Record provenance in a `verification_source` field. Do not infer standards, accreditation or commercial service availability. The equipment heading and cards are omitted when the array is empty.

Both pages share `_includes/resource_card.html`. Approved photographs belong in `assets/img/`; give their relative path, descriptive alternative text and actual pixel dimensions. The component reserves image proportions and adapts to one mobile column or two wider columns. Do not add placeholder images or unverified proposals to demonstrate the layout.

Notes are retired. Three unchanged source articles remain in the excluded `docs/retired-notes/` directory; none is published in posts, archives or the feed. `_data/retired_notes_urls.json` records 16 former catalogue, archive and article routes. `_plugins/retired-notes.rb` and `_layouts/retired-notes.html` provide immediate lightweight redirects to Research, with a canonical destination, `noindex` and a manual link. These routes stay out of the sitemap. The RSS icon and Notes-only interface code are removed; the legacy feed is empty for existing subscribers. Restoring an article requires a separate editorial decision.

PR builds retain a seven-day `website-preview` artifact containing generated HTML, styles, scripts, fonts, bibliography and the profile image for visual review. This replaces the narrower catalogue-only preview; deployment remains master-only.
