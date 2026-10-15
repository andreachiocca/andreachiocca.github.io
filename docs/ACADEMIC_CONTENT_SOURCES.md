# Academic content sources and reconciliation

Updated 15 October 2026. Source-dependent updates continue PR #14 on `codex/academic-site-audit-2026-10-15`; the production branch is `master`.

## Starting state

PR #14 at `1538bdd8cb2f6e6ea6ad1e80400c4ec9a9bb0f37` was open, conflict-free and passing. The local checkout was clean. [Run 38719317813](https://github.com/andreachiocca/andreachiocca.github.io/actions/runs/38719317813) passed build, generated-site verification and Ruby/npm advisory checks. Deployment was intentionally skipped: the existing job requires `refs/heads/master` and a non-pull-request event. That workflow remains unchanged. No merge or production deployment is authorized by this update.

## CV sources and selection

The supplied Italian LaTeX CV was read through its main file and imported career, education, research, projects, visiting, teaching, qualification and award sections. A compact structured summary was kept outside the website repository. PDF source files were not used as extraction substitutes.

The update records a research contract from January 2026; the February 2025-January 2026 research fellowship; the February 2022-January 2025 fixed-term RTDa and industrial collaboration; national scientific qualification for associate-professor functions (November 2024); three degrees; teaching periods through 2026; selected research visits, projects and supervision. The qualification is not represented as an associate-professor appointment. Teaching titles and materials retain their existing Italian context; public biographical prose and the new public CV are in English.

The public PDF is generated from sanitized academic data and visually reviewed. Personal mobile number, personal email, signatures, signed PDFs, contract amounts and bibliometric counters from the source CV are excluded. Source archives are not added to this repository. Professional institutional contact information is retained.

## Scholarly bibliography

The publication archive contains 35 records: 17 journal articles, 11 conference contributions, six data/package records and one thesis. Its bibliography is identical to the copy accompanying the CV. DOI comparison matched all 25 previous website records: 24 scholarly works and one dataset.

The website now has **30 scholarly records: 18 journal articles, 11 conference contributions and one doctoral thesis**. Five scholarly works came from the archive; one further 2026 article was verified using the publisher and Crossref when reconciling a requested dataset. All 24 existing scholarly records remain. The previous Mendeley dataset is preserved in the research-output catalogue and the old bibliography anchor links to it.

New scholarly keys: `Frendo2019784`, `Chiocca2025ab`, `Chiocca2025a`, `Frendo2025`, `Chiocca2025`, `Chiocca2026WeldedECP`.

Corrections and reconciliations:

- Five existing proceedings records were reclassified from journal articles: `Chiocca2023a`, `Fontana2023`, `Chiocca2020`, `Chiocca2019c`, `Chiocca2022a`. Existing complete author names and working links were preserved.
- `Chiocca2023b`: the Wiley issue citation is **2024, 47(1), 72-87**; first online publication was October 2023. The original key stays stable and the online date is noted. Its correct title retains “critical plane”, despite omission in the archive's exported title.
- `Chiocca2022b`: retain the verified 2022 proceedings year rather than reintroducing the archive's 2021 error.
- `Chiocca2025a`: the conference publisher lists **Chiocca, Frendo, Sgamma**, differing from the archive order. The publisher order is used. The DOI resolves although its Crossref endpoint did not return a record.
- `Sgamma2023`: volume 2, issue 4 added from the supplied structured metadata.
- `Frendo2019784`: the source lists no DOI. The record is retained without inventing one; a corrupted page-range separator is normalized to 784-785.
- `Chiocca2026WeldedECP`: DOI `10.1111/ffe.70429`, authors Andrea Chiocca and Francesco Frendo, volume 49, issue 11, pages 5048-5064. The paper was published online on 25 August 2026; the assigned print issue is November 2026.

All **29 supplied scholarly DOIs resolved** in a direct DOI resolver check. No duplicate scholarly DOI or BibTeX key remains. Four representative publications are selected for the homepage.

## FABER responsibility

The user's explicit current statement is authoritative: **Co-Leader of Working Group 3 (Fatigue Estimation Competition), COST Action CA23109 - Fatigue Benchmark Repository (FABER).** It is stored in `_data/academic_service.json`, appears fully in Research and the public CV, and has a concise homepage reference.

The public FABER WG3 page retrieved for this update lists Michaela Gkantou as leader and does not yet reflect Andrea Chiocca's co-leadership. The COST page did not expose a matching name in the retrieved listing. This is reported as an unreflected role, not as a reason to override the user's statement. WG4.3 methodological/software activity and the 2026 WG6 visit remain separate.

## Software and research data

All requested resources appear at `/repositories/`, linked from Home and Research. The catalogue has **eight distinct outputs**. The six requested resources are supplemented by the SPR-joint dataset and the existing Mendeley dataset from the supplied bibliography. FABEST version v2.0.0 (record 21166758) is linked as an earlier version of v2.1.0 (record 21534682); both share concept record 20934797.

Zenodo metadata were retrieved directly through the public records API, without downloading data files. Resource titles, creator order, dates, DOIs, registry types and access conditions are retained.

| Resource | Official title / documented project title | Type and access | DOI or repository |
| --- | --- | --- | --- |
| multiaxial-fatigue | FABER WG4.3 - multiaxial fatigue assessment library | Research software; Public repository; licence not yet selected | [GitHub](https://github.com/andreachiocca/multiaxial-fatigue) |
| zenodo-21534682 | FABEST High-Cycle Fatigue Competition: Participant Package for Blind Fatigue-Life Prediction | Benchmark participant package; Open files | [10.5281/zenodo.21534682](https://zenodo.org/records/21534682) |
| zenodo-21875885 | Dataset for: "Fatigue assessment of sharp notches under Mode I and Mode III loading by means of a process volume based critical plane approach" | Supporting research data; Restricted files | [10.5281/zenodo.21875885](https://zenodo.org/records/21875885) |
| zenodo-18416255 | Dataset for: "Fatigue assessment of welded joints subjected to multiaxial loading conditions through the Effective Critical Plane approach" | Supporting research data; Open files | [10.5281/zenodo.18416255](https://zenodo.org/records/18416255) |
| zenodo-14198237 | Dataset for: "Application of the Effective Critical Plane approach for the fatigue assessment of ductile cast iron under multiaxial and non-proportional loading conditions" | Supporting research data; Open files | [10.5281/zenodo.14198237](https://zenodo.org/records/14198237) |
| zenodo-12721131 | Dataset for: "Fatigue assessment of structural components through the Effective Critical Plane factor" | Supporting research data; Open files | [10.5281/zenodo.12721131](https://zenodo.org/records/12721131) |
| zenodo-12741922 | Tensile tests on PEEL and LAP hybrid self-pierce riveting joints with and without adhesive | Supporting research data; Open files | [10.5281/zenodo.12741922](https://zenodo.org/records/12741922) |
| Moda2022a | Dataset of dimensionless operating conditions for welding and metal additive manufacturing | Research dataset; Public record; consult repository for file access | [10.17632/b2437352ky.2](https://data.mendeley.com/datasets/b2437352ky/2) |

Zenodo 18416255 is labelled “Journal” and 14198237 “Data paper” in registry metadata; their descriptions and files identify supporting data, so the catalogue explains the distinction and does not treat either deposit as an additional peer-reviewed paper. Record 21875885 has restricted files and no descriptive abstract in the public API response: its short description is limited to its official title and access status. The associated sharp-notch article is not added without a verified scholarly citation.

The multiaxial-fatigue README and method-audit documentation support a description of current single-frequency harmonic calculations for plain/smooth geometries, elastic strain estimates, damage assessment, optional life fitting, and methodological comparison. Planned variable-amplitude histories, notch gradients and constitutive plasticity are not presented as implemented. Independent validation remains outstanding and a software licence has not yet been selected. The scientific review is in preparation. External repositories and deposits were not modified.

## Verification and maintenance

Existing Jekyll build, cache regression and advisory checks are retained. Verification now also covers local fragments, required rendered resource records, six core pages at 390/768/1280px, keyboard skip navigation and mobile menu, native publication disclosures and filtering. Browser unavailability is reported explicitly. New fragment checks exposed two old research-note table-of-contents entries without matching headings; those entries were corrected while keeping article URLs and scientific text stable.

Final observed check results are reported on PR #14 and in the delivery report; successful compilation alone is not treated as visual/accessibility certification. The public CV was rendered and visually checked. No complete WCAG audit, Lighthouse/field Core Web Vitals study or production deployment is claimed.

## Primary verification sources

- [COST Action CA23109](https://www.cost.eu/actions/CA23109/) and [FABER WG3](https://faber-cost.eu/wg3-fatigue-estimation-competition/)
- [Multiaxial-fatigue documentation](https://github.com/andreachiocca/multiaxial-fatigue)
- [2026 welded-joints article](https://onlinelibrary.wiley.com/doi/10.1111/ffe.70429)
- [2024 Wiley issue citation](https://onlinelibrary.wiley.com/doi/10.1111/ffe.14153)
- [ICMFF14 publisher record](https://dvm-wissen.de/de/14-international-conference-on-multiaxial-fatigue-and-fracture-2025/523-ICMFF14-2025-25.html)
- [2025 cast-iron article](https://www.sciencedirect.com/science/article/pii/S0142112324005759)
- Crossref's official `/works/{doi}` endpoint and the individual Zenodo record API endpoints.
