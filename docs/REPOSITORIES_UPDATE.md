# Repositories and research outputs: targeted update

Scope: existing branch `codex/academic-site-audit-2026-10-15`, PR #14; preserve the previous CV, bibliography, research and teaching work. No merge or production deployment is authorized by this update.

## Original implementation and diagnosis

The obsolete `_includes/repository/repo.html` represented a repository only as two externally generated GitHub Readme Stats images, one per theme. On 15 October 2026 a direct request to its `api/pin/` endpoint returned HTTP 500. There was no textual metadata fallback. This is an external rendering failure, not blocked GitHub iframe content. Both images used `w-100`, while the legacy `.repo` rule only constrained desktop maximum width; it provided no explicit mobile grid or content-based card sizing. An unsuccessful or differently sized SVG therefore determined the visible card and fallback layout. Repository title typography was embedded in the remote image and could not follow the site's responsive text styling. The old list also used the obsolete casing `FI-SOL` rather than the API's `FI-Sol`.

Previous work on this branch already replaced the active page with a text-only catalogue and six additional code links. The live page inspected for this task also served that text-only revision: no broken image was reproduced in the current live capture. The screenshot mentioned in the request was not available as an image in this turn. The saved before image documents the actual live baseline, rather than reconstructing or claiming to inspect the missing screenshot. Legacy image widgets remained in the repository and have now been removed after checking that no page invokes them.

The fixed navbar used a constant 56px body offset while its measured closed height was 57px. Adding a catalogue navigation item also required more width than the previous expansion threshold safely reserved. The update uses a 64px initial reservation, observes actual header height when fonts/text size/menu state change, and expands the menu at 992px. It keeps the existing navbar and design identity.

## Catalogue coverage and identity

Both GitHub connections independently identify the authenticated accounts as `achiocca1` and `andreachiocca`. Their paginated public owner lists return seven and four repositories respectively. Every one is included, including the website itself, old utilities and personal forks. There are eight non-forks and three forks; none are marked archived and none report a mirror URL. Stars are omitted. Dates use latest default-branch commits rather than general metadata update timestamps.

Zenodo discovery searched ORCID `0000-0002-1472-4398`, creator surname and verified deposit owner `275783`, with `all_versions=true`, page size 25 and next-link traversal. It found ten verified public records, grouped into six concepts. ORCID verifies identity where present; otherwise the exact creator name plus the same owner as the explicitly supplied deposits is required. A conflicting ORCID is rejected. Six surname search results by unrelated creators were excluded: 14302835, 14323405, 14416230, 19891746, 2608559, 8214402. No verified Andrea Chiocca deposit was intentionally excluded.

The five requested deposits are included, plus the verified SPR tensile-test deposit. The former single FABEST earlier-version link is expanded to all three preceding versions; the earlier SPR deposit is also retained. Four FABEST records become one card, and two SPR records become one card. Each version retains its own record URL/DOI; the concept DOI is separately labelled. There is no verified duplicate software archive across the discovered GitHub and Zenodo resources. Journal-article DOIs in GitHub READMEs identify related papers, not software deposits; an upstream theme's DOI is not assigned to a personal fork.

The existing Mendeley welding/additive-manufacturing dataset remains a separate additional resource. Total: 18 cards â€” eight Software, seven Datasets & benchmarks and three Other outputs. The FatPy fork remains under Software with fork/upstream attribution; academic template forks and this website are Other outputs.

### Included GitHub repositories

- [andreachiocca/multiaxial-fatigue](https://github.com/andreachiocca/multiaxial-fatigue)
- [andreachiocca/andreachiocca.github.io](https://github.com/andreachiocca/andreachiocca.github.io)
- [andreachiocca/moloch](https://github.com/andreachiocca/moloch) â€” fork of https://github.com/jolars/moloch
- [achiocca1/ECP](https://github.com/achiocca1/ECP)
- [andreachiocca/FatPy](https://github.com/andreachiocca/FatPy) â€” fork of https://github.com/faberorg/FatPy
- [achiocca1/CPOpt-v1.0](https://github.com/achiocca1/CPOpt-v1.0)
- [achiocca1/FI-Sol](https://github.com/achiocca1/FI-Sol)
- [achiocca1/SeAn-CP](https://github.com/achiocca1/SeAn-CP)
- [achiocca1/FS-Sol](https://github.com/achiocca1/FS-Sol)
- [achiocca1/APDL-WB-ssr-v1.0](https://github.com/achiocca1/APDL-WB-ssr-v1.0)
- [achiocca1/Awesome-CV](https://github.com/achiocca1/Awesome-CV) â€” fork of https://github.com/aminmkhan/Awesome-CV

### Included Zenodo records

| Resource | Displayed record | Earlier versions |
| --- | --- | --- |
| FABEST: blind fatigue-life prediction | [21534682](https://zenodo.org/records/21534682) | [21166758](https://zenodo.org/records/21166758); [21010662](https://zenodo.org/records/21010662); [20934798](https://zenodo.org/records/20934798) |
| Sharp-notch fatigue: Mode I and Mode III | [21875885](https://zenodo.org/records/21875885) | None discovered |
| Welded joints under multiaxial loading | [18416255](https://zenodo.org/records/18416255) | None discovered |
| Ductile cast iron under non-proportional loading | [14198237](https://zenodo.org/records/14198237) | None discovered |
| Hybrid self-piercing riveted joints | [12741922](https://zenodo.org/records/12741922) | [12734069](https://zenodo.org/records/12734069) |
| Structural components: ECP fatigue assessment | [12721131](https://zenodo.org/records/12721131) | None discovered |

## Implementation

- One centrally maintained JSON catalogue, a discovery-coverage snapshot and a standard-library Python refresh command. Public APIs are used only when deliberately refreshing; Jekyll builds and visitors consume the checked-in snapshot. Failed or incomplete API requests preserve the last catalogue. Curated science, access caveats and stable anchors survive refreshes. New records require description review. Missing older entries are retained for investigation.
- Native HTML cards, compact local typography, one column on mobile and two at sufficient tablet/desktop width within the existing 800px content area. No fixed image boxes, external preview screenshots, iframes or essential browser API requests. Existing locally hosted GitHub/Zenodo icon fonts have visible source-text fallbacks.
- Four accessible category buttons, result counts, keyboard operation and recovery of links to filtered resources. With JavaScript disabled every card remains visible. Direct links and disclosures have 44px minimum targets.
- Official titles, ordered creators, exact version/concept DOIs, access, scientific caveats, fork provenance and related bibliography entries are in native expandable details. Short dataset headings improve browsing without replacing official metadata. The restricted deposit remains explicitly restricted. Two supporting-data deposits retain notes explaining their Zenodo publication-type labels.
- Research cross-links use existing headings. FABER WG4.3 software, WG3 responsibility and upstream FatPy WG6 remain distinct. No academic content or downloadable document is removed.
- PR-only preview artifact supports inspection of the actual built Jekyll page. Deployment conditions and permissions remain restricted to the existing master workflow; no product dependency or framework was added.

Removed: the three unused repository/user/trophy preview includes and obsolete manually selected `_data/repositories.yml`. All six listed repositories are preserved in the full catalogue. Their unused style/configuration settings were also removed. Git history and branches are preserved.

## Maintenance and limitations

Run `python scripts/sync_research_outputs.py --write`, review the diff and new descriptions, then commit on a branch. Run without `--write` to inspect discovery without modifying files. README documents fields and scientific review rules. An optional GitHub token only increases API limits; it is never required by the site. No unattended schedule publishes unreviewed scientific material.

Coverage is complete for the public APIs of the two verified accounts and the verified Zenodo searches on 15 October 2026. Private repositories, unpublished deposits, organization-owned repositories not in those owner lists, and deposits with neither a matching ORCID nor verifiable owner/name evidence are outside that completeness claim. Search indexing can lag. Zenodo metadata is public even where files are restricted; restricted files were not downloaded.

## Verification

Nine offline regression tests cover pagination, incomplete results, creator identity, version consolidation, preservation of scientific annotations/access, service failures and complete catalogue coverage. Generated-site checks validate every discovered repository/version URL and card anchor and reject external previews. Browser checks cover catalogue/header bounds, touch target sizes, filters and deep links alongside the existing academic-page checks. Jekyll/CI and actual rendered visual results are recorded in the final task report and PR verification run.
