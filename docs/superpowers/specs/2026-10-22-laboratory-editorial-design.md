# Phase 5: Laboratory and Experimental Capabilities, editorial design

**Date:** 22 October 2026  
**Status:** User has approved the proposed visual direction and supplied facility details and photographs. This written specification is submitted for approval before the implementation plan and page changes.  
**Repository:** https://github.com/andreachiocca/andreachiocca.github.io  
**Target routes:** /laboratory/ and /it/laboratory/

## 1. Purpose and boundaries

Transform the existing factual but text-heavy Laboratory page into a visually strong, readable bilingual presentation of research equipment and experimental capabilities. Match the established **Technical Editorial** visual language of the homepage, Research Atlas and Publications Index. This is an academic research profile, **not** a commercial testing-service catalogue or a statement of unconditional equipment access.

Use original photographs supplied by the user, not stock imagery, synthetic machine photographs, or generic generated scientific results. Favor restrained typography, navy/teal accents, fine dividing rules, good white space and engineering-specific figures over boxed card grids. Maintain the current Jekyll/Liquid implementation, bilingual translation system, dark theme, performance and accessibility. Do not alter unrelated pages, menus or bibliography.

This replaces the existing intentionally empty equipment section with a **verified-by-user, current equipment summary** while preserving links to the relevant Research, Publications, Repositories and Thesis pages.

The user explicitly corrected the Schenck internal-pressure limit to **700 bar**, which equals 70 MPa; do **not** publish 700 MPa. The user-provided ratings supersede conflicting or dated capacities/counts on the University's older group website. Do not infer that independent maxima can be reached at the same time.

## 2. Visual narrative and page layout

### 2.1 Editorial introduction with one genuine hero photograph

A split or asymmetric editorial opening, consistent with the homepage and Research Atlas:

- Section identifier, prominent page title, two or three concise sentences introducing fatigue-related research across metals, polymers, composites and additively manufactured materials.
- Featured real photograph of the machined axial specimen, **IMG_3207.jpeg** (new image). Use a purposeful close crop and negative space, maintaining the recognisable specimen geometry. **IMG_3209.jpeg** is a good alternate, not an additional near-duplicate on the same page.
- At most three short, readable topic anchors: Testing systems, Test conditions and preparation, Research collaboration. The existing anchors \`#research-expertise\`, \`#instrumentation\`, \`#equipment\` (once present) and \`#laboratory-collaboration\` must continue to resolve.
- A useful caption identifying the image accurately as a machined test specimen. Do not imply it is a failed specimen, represents measured strain or documents a specific paper unless confirmed.

### 2.2 Primary fatigue and mechanical testing facilities

Treat each featured system as one editorial row, with a photographic image when suitable, a text title, a compact description and a few carefully labelled specifications. Vary image/text placement in a controlled way; avoid six identical cards.

- **StepLab axial–torsional electrodynamic machine**. Maximum static load 33 kN, maximum dynamic load 43.5 kN, maximum frequency 250 Hz (specimen and operating-mode dependent); circular gripping Ø 6–12 mm; flat specimens up to 15 mm thick. Use a clearly identified StepLab photograph. **IMG_1270.jpg** and **IMG_3200.jpeg** are candidates, but confirm which of these depicts the main 33/43.5 kN machine before applying a model-specific caption.
- **Schenck servo-hydraulic axial–torsional system**. Axial tension/compression up to 250 kN, torque up to 2000 N·m, internal-pressure actuator up to **700 bar** for tubular specimens; circular Ø 5–40 mm; flat 8–20 mm thick. Use **IMG_3186.jpeg** if this is the correctly identified Schenck setup, cropped to favour the actuators; do not misidentify a separate rig from its background.
- **Rumul resonant system**. User-supplied tension/compression rating up to 100 kN; a crack-growth controller enables fracture mechanics tests on compatible standard specimen geometries. **IMG_3190.jpeg** is a candidate with an edit to crop out the handwritten paper and distracting tabletop, without altering the machine or removing safety notices through content editing.
- **MTS uniaxial servo-hydraulic machines**. Uniaxial tension/compression rating up to 100 kN, no invented frequencies or total machine counts. Describe compactly, without a weak photograph if none of the images cleanly identifies the system.
- **Smaller StepLab electromechanical system**. Up to 10 kN and 20 Hz. The two StepLab photographs require identification before assigning either image to this machine. If uncertain, use a neutral equipment caption and avoid asserting the wrong model.

The apparent precision of a metric must not become an unqualified operating guarantee. Use short footnotes indicating that specimens, grips, fixture, control mode and configuration determine feasible combinations.

### 2.3 Configurable structural and vibration testing

- A configurable experimental bench with **three Schenck hydraulic actuators**; potential setups include tensile/torsional loading of welded joints and fatigue tests on vehicle frames. It may serve different component-level test configurations after bespoke setup and feasibility assessment. Photograph **IMG_0167.JPG** is the preferred large landscape image; identify the bench, not an entire test as performed, in its caption.
- A smaller secondary segment for structural-dynamics/vibration investigations, with a real experimental setup photograph **IMG_8745.JPG** (TIRA shaker test arrangement) if room allows. **IMG_3192.jpeg** is an alternate technical close-up, not a required sixth hero-quality photograph. Distinguish the vibration shaker from the axial–torsional fatigue machines and do not transfer the 250 Hz StepLab limit to a separate shaker.
- The older Machine Design Group site documents ABB-assisted laser-vibrometer measurements. The user also supplied **IMG_0169.JPG** showing the robot. Include this only as an optional, correctly attributed existing group capability, in a short supporting link or a second-phase enhancement. Avoid implying it is a StepLab, MTS or Schenck setup.

### 2.4 Environmental testing, specimen preparation and metrology

A visually lighter section with concise grouped text rather than one photograph for every tool.

- Induction oven: up to 900 °C, used for relevant creep–fatigue/high-temperature fatigue configurations.
- Resistance oven: 200–1000 °C.
- StepLab climatic chamber: −30 to +180 °C, available for compatible StepLab experimental configurations. The earlier stand-alone climatic chamber entry with the same range must **not** be double-counted as a second chamber.
- In-house specimen preparation: CNC lathe, milling machines and machining/tooling for round, flat, notched/unnotched and tubular specimens.
- Characterisation and metrology: contact/optical surface roughness measurement with Ra and Rz reporting; Vickers hardness testing.

### 2.5 What can be investigated and collaboration

A compact, understandable capabilities summary near the end. Categories include:

- Constant-amplitude multiaxial loading (axial, torsional and, with the suitable tubular setup, steady internal pressure).
- Variable-amplitude/spectrum loading, including appropriate random or PSD-type excitation in vibration-fatigue setups. Do **not** claim all rigs support arbitrary PSD inputs or that 250 Hz applies universally.
- Creep, creep–fatigue, thermally assisted fatigue and selected environmental conditions.
- Fatigue crack growth and selected fracture mechanics procedures.
- Customized structural/component testing and numerical–experimental correlation.

Retain the current explicit condition that actual tests depend on staffing, facility access, specimen/test-fixture geometry, operating limits and the agreed research project. Preserve the existing email enquiry and links to related pages. Do not promise accredited services, certified measurements, or routine industrial commercial availability.

## 3. Image shortlist, licensing and asset preparation

All photographs are user-provided and depict laboratory equipment or specimens, so they are preferred over stock. The candidate selection is deliberately strict.

| File from conversation | Intended use | Priority | Editorial note |
| --- | --- | --- | --- |
| \`IMG_3207.jpeg\` | Hero or large opening specimen photograph | Primary | Most restrained composition and negative space; crop conservatively. |
| \`IMG_0167.JPG\` | Configurable structural bench | Primary | Landscape format expresses scale and capability. |
| \`IMG_3186.jpeg\` | Schenck actuators / structural testing | Primary | Tight composition; verify exact hardware identification. |
| \`IMG_3200.jpeg\` | StepLab equipment | Primary | Clear guard frame; verify whether this is the 10 kN or main machine. |
| \`IMG_3190.jpeg\` | Rumul resonant system | Secondary | Crop distracting handwritten notice without hiding safety-related equipment signs. |
| \`IMG_8745.JPG\` | Vibration-testing setup | Secondary | Real experimental setup, useful if this section is sufficiently prominent. |
| \`IMG_1270.jpg\` | Alternate StepLab environmental setup | Alternate | Avoid duplicating indistinguishable views. |
| \`IMG_3209.jpeg\` | Alternate hero specimen | Alternate | Do not use alongside \`IMG_3207.jpeg\` in the same short page. |
| \`IMG_3192.jpeg\` | Alternate small shaker | Alternate | Narrow technical detail, not featured. |
| \`IMG_0169.JPG\` | Optional modal/robotics capability | Optional | Only if page text explicitly describes the setup. |

Exclude \`IMG_8606.jpg\`, \`IMG_3185 1.jpeg\`, \`IMG_3187.jpeg\` and any weakly identified or visually distracting photographs from the initial featured set.

**Asset policy:** Optimize selected real photos locally into responsive, EXIF-stripped WebP and, if necessary, one JPEG fallback each; use fixed aspect ratios, width and height to avoid layout shift. Prefer two output widths (approximately 640 and 1280 pixels), quality around 78–84, and target an initial above-the-fold photographic payload below 250 kB. A photo can be omitted if visual quality does not survive the target crop. Do not embed base64 photographs directly in HTML or use third-party image CDNs. Each photo has bilingual alt text and a short matter-of-fact caption, but never contains speculative machine identification.

**Photo upload provenance:** The original conversation uploads are available as inputs during this design, but binary assets must be included in the final GitHub PR as optimized files and have their real file paths verified. The draft PR must never reference images only in the ChatGPT sandbox. All photo filenames must be mapped to machine descriptions explicitly, and uncertain matches checked before the final preview.

## 4. Bilingual content architecture

Current canonical source locations:
- \`_pages/laboratory.md\` is the one bilingual page with \`translation_key: laboratory\`.
- \`_data/laboratory.json\` contains canonical laboratory capabilities, measurement contexts and an empty \`equipment\` array.
- \`_data/i18n/it/laboratory.json\` holds Italian text keyed by canonical record IDs.
- \`_includes/resource_card.html\` already handles \`localized_record: 'laboratory'\` and simple equipment data, but the redesigned *featured* equipment should use a dedicated, scoped editorial include rather than globally changing resource cards.
- \`_sass/_academic.scss\`, \`_sass/_technical_editorial.scss\` and \`_sass/_research_atlas.scss\` establish palette, typography and baseline page behaviors.

Proposed implementation boundaries after plan approval:

1. Create/add canonical structured equipment entries by stable IDs in \`_data/laboratory.json\`. Keep numeric ranges, unit symbols, and explicit operating limitations in one record, not scattered through Markdown. Retain the existing research capabilities and valid links.
2. Add Italian counterparts to \`_data/i18n/it/laboratory.json\` using the user's academic-writing Skill. Preserve English machine brand/model names and standardized units. Use *fatica multiassiale*, *prove assiali–torsionali*, *pressione interna fino a 700 bar*, *camera climatica*, *prove di propagazione della cricca*, and other appropriate technical terminology.
3. Use one small, maintainable include such as \`_includes/laboratory_equipment.html\`, only for primary machine rows. Represent ancillary capabilities as editorial typographic sections, not excessive repeated cards.
4. Add one page-scoped Sass partial \`_sass/_laboratory_editorial.scss\` and import it once in \`assets/css/main.scss\`. No new fonts, icon package, JavaScript framework or custom backend.
5. Link local optimized image files under \`assets/img/laboratory/\` and include accessible \`<picture>\` / \`<img>\` markup with localized alt text, width/height, and lazy loading outside the hero.
6. Keep headings/anchors stable, including \`#research-expertise\`, \`#instrumentation\` and \`#laboratory-collaboration\`. Add \`#equipment\` only when equipment exists (it now will).

Style writing must respect \`andrea-chiocca-academic-writing\`: concise scientific prose, no promotional claims, no em dashes or formulaic framing, collective voice for group-owned facilities, and no translation of official machine names.

## 5. Acceptance and regression checks

- English \`/laboratory/\` and Italian \`/it/laboratory/\` render in the existing bilingual system with exactly one \`main\` and \`h1\` each.
- Same equipment IDs/order, capabilities, numerical specifications and limits in both locales, especially **700 bar** (and never the prior mistaken 700 MPa). Verify no duplicate environmental chamber and no implication that 250 Hz applies to every machine.
- All public photo references resolve, have bilingual alt text, fixed intrinsic dimensions and reasonable file sizes. No duplicate hero images or broken source sets.
- Preserve every currently valid anchor and cross-page link, original collaboration contact and project feasibility disclaimer.
- Light/dark themes, keyboard links, 320/375/390/768/1280/1920-pixel layouts, reduced-motion settings and no horizontal overflow. Images may be stacked responsively, not scrolled horizontally.
- Loading behavior is static progressive enhancement: visitors can read all equipment and details without JavaScript. No extra runtime package, font or remote asset request. Track HTML/CSS/above-the-fold photo byte deltas.
- Integrate focused post-build EN/IT Laboratory verification with the existing \`verify_site.py\`, \`verify_languages.py\`, and Chromium browser checks. Avoid multiplying unrelated route tests unnecessarily.
- Produce a **separate draft PR and Cloudflare EN/IT previews**. Verify the exact commit SHA's checks before requesting the user's visual approval. Do not merge without explicit authorization.

## 6. Review and stage boundaries

The **visual direction** presented in the preceding conversation is approved; the user has asked to proceed and has supplied final photographs and equipment information. This specification records that design as a durable source of truth and requires the user's **written-spec approval**. After approval, produce a task-by-task implementation plan, review it, and then execute it on the same separate branch. Until the written spec and plan are reviewed, PR changes are documentation-only; the live website stays untouched.
