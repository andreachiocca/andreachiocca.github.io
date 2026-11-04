# SEO: what the site does and what only the owner can do

Date: 4 November 2026.

## In the site (automated, checked by `scripts/verify_site.py`)

- **Titles.** One title per page, unique across EN and IT. The home title adds keywords through `seo_title`: *Andrea Chiocca – Fatigue Research, University of Pisa*. Course pages carry a language-specific suffix (*Course materials* / *Materiali del corso*).
- **Descriptions.** 50–160 characters, written for search results and not repeated between pages. Course pages use `seo_description` in English and `pages.json` in Italian.
- **Languages.** `hreflang` alternates for `en`, `it` and `x-default`, plus canonical URLs.
- **Structured data.** A schema.org `Person` with `jobTitle`, affiliation, department (`worksFor`), `alumniOf`, image, email, `knowsAbout` research topics and `sameAs` profiles (ORCID, Google Scholar, Scopus, ResearchGate, GitHub, LinkedIn). Pages also carry `ScholarlyArticle`, `SoftwareSourceCode` and `Dataset` records.
- **Sharing.** Open Graph and Twitter large card with `assets/img/og-card.png`.
- **Sitemap.** Generated at build time, listing indexable pages only (no 404, no retired notes). `robots.txt` points to it.
- **Verification.** Google Search Console meta tag present. The Bing tag is emitted only when `bing_site_verification` is set.

## Owner actions (cannot be done from the repository)

Ordered by impact:

1. **Google Search Console.** In the property for `https://andreachiocca.github.io/`, submit `sitemap.xml` and request indexing of `/`, `/it/`, `/publications/` and `/thesis/`. Check *Pages* after one or two weeks.
2. **Bing Webmaster Tools.** Use *Import from Google Search Console*, which needs no extra tag. This also covers DuckDuckGo and Ecosia.
3. **Link back to the site from your profiles.** These links drive both ranking and discovery:
   - ORCID: *Websites & social links*;
   - Google Scholar: *Homepage* field;
   - ResearchGate: *Website*;
   - LinkedIn: *Contact info → Website*;
   - GitHub: profile *Website*, plus a profile README;
   - Scopus: request the website through the Author Feedback Wizard, if available.
4. **University of Pisa.** Ask for the site to be linked from your UniPi people page and from the DICI machine design group page. Institutional links carry the most weight.
5. **Zenodo and repositories.** Add the site URL as a *related identifier* (`isDocumentedBy`) in the Zenodo records, and in the `CITATION.cff` / README of `multiaxial-fatigue`, `sharCP` and the other tools.
6. **Papers and talks.** Put the site URL in email signatures, slide footers and the author-information field where journals allow it.

## Next technical step (proposed)

**One page per publication** (`/publications/<key>/`) with Google Scholar `citation_*` meta tags (title, authors, date, journal, DOI and, where the licence allows, the PDF). It would also carry the abstract and links to the related code and data. Google Scholar indexes individual article pages, not bibliography lists, so this is the largest remaining gain for academic search.
