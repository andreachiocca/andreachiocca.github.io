# Targeted academic UX and mobile update

The four supplied mobile screenshots are the debugging reference: duplicated/unclear navigation naming, a CV Projects block missing FABER and repeating 2025, oversized Notes headings, fixed three-column featured cards and historical broken repository previews. The live Notes baseline reproduced 90px-wide cards at 390px and an 80px H1. The Repositories catalogue from the previous work remains intact.

## Implementation scope

- Central menu: Home, Research, Publications, Repositories, Teaching, Notes, CV. One source controls all layouts and active-section marking, including course pages and scientific articles. The opaque fixed header prevents text showing through it. On mobile the navigation is a deliberate modal layer: its opening leaves page geometry unchanged, background content becomes inert, keyboard focus stays in the menu, and Escape/backdrop/link selection close it. Header space follows the closed header's actual height. A no-JavaScript fallback exposes the navigation in normal flow.
- Four source-grounded research summaries of 44–47 words, each followed by methods, related outputs and optional further studies. Existing research anchors and study links remain. Earlier projects and research visits remain in native disclosures. Detailed articles retain their scientific body text unchanged.
- Shared project data now includes FABER prominently on Research and CV. Andrea Chiocca's WG3 Co-Leader role follows the owner's explicit statement. The official COST page verifies the Action's 25 September 2024–24 September 2028 duration and benchmarking objectives; these are labelled Action dates, not personal role dates. WG4.3 software activity and the WG6 visit remain distinct. PRIN/PRA roles and dates follow the existing CV; PON activity follows the prior verified Research/CV content. The same-year project displays 2025 once.
- Homepage identity, role and research introduction precede the portrait on mobile. It links current FABER activity, selected publications, software/data and a restrained collaboration invitation using the established university email. Prior career history remains in CV; office contact remains available in a disclosure.
- All 30 existing public course-resource entries are moved without changing URLs into a shared data catalogue, grouped by course and type. No material year is invented. The overview distinguishes recent documented teaching through 2026 from the 2021–2024 course. An existing course with no public resources says so without promising unpublished materials. Verified official university catalogue/e-learning links are retained as the place for current requirements. Supplementary Notes are linked, not copied.
- Notes uses one responsive grid instead of duplicating featured posts and the chronological list. The old unconditional `row-cols-3` and oversized `header-bar` title/subtitle are removed from this page. Cards have a short heading, source excerpt, date and direct link. Scientific articles use the same 800px content width and proportionate headings. Wide mathematical expressions, tables and code can scroll locally without shrinking text; scrollable regions are keyboard accessible.

## Source verification

- COST Action: https://www.cost.eu/actions/CA23109/
- FABER project: https://faber-cost.eu/
- WG3: https://faber-cost.eu/wg3-fatigue-estimation-competition/
- University course catalogue: https://unipi.coursecatalogue.cineca.it/
- Engineering e-learning: https://elearn.ing.unipi.it/

The public leadership pages do not yet establish the owner's co-leadership date; no such date was added. The explicit owner-provided role remains authoritative. Existing CV sources provide teaching periods, project roles and professional contact details; no archives were reopened unnecessarily. The existing bibliography, public CV PDF, output catalogue and research-note article bodies remain preserved.

## Verification

CI checks now include Notes, all scientific articles and all course pages at 375, 390, 768 and 1280px, alongside existing catalogue/publication checks. They test narrow-card regression, heading sizes, active navigation, menu geometry, background isolation and Escape/focus restoration. Generated-site checks verify local assets, links/anchors, core metadata and required FABER/teaching content. The final PR and task report record the actual build, external-link checks, browser results and inspected screenshots.

Deployment remains restricted to master; this update does not authorize a merge or deployment. The previous PR #20 was already merged, so the current work uses a follow-up PR on the existing branch.

The existing Google Drive tutorial folder returned HTTP 404 to anonymous access. Its URL remains in the source data for provenance, but the two course listings mark it unavailable and offer a contact link rather than sending students to a broken destination. A replacement or restored public sharing setting needs owner-supplied information.
