# Phase 5: Laboratory and Experimental Capabilities, editorial design

**Date:** 22 October 2026  
**Status:** Written specification approved by the user on 22 October 2026, including the Schenck 700 bar internal-pressure limit, historical equipment ratings and FLIR X6901sc identification. Detailed implementation plan prepared for separate review. No page implementation or merge approved at this stage.  
**Repository:** https://github.com/andreachiocca/andreachiocca.github.io  
**Target routes:** /laboratory/ and /it/laboratory/

## 1. Purpose and boundaries

Transform the existing factual but text-heavy Laboratory page into a visually strong, readable bilingual presentation of research equipment and experimental capabilities. Match the established **Technical Editorial** visual language of the homepage, Research Atlas and Publications Index. This is an academic research profile, **not** a commercial testing-service catalogue or a statement of unconditional equipment access.

Use original photographs supplied by the user, not stock imagery, synthetic machine photographs, or generic generated scientific results. Favor restrained typography, navy/teal accents, fine dividing rules, good white space and engineering-specific figures over boxed card grids. Maintain the current Jekyll/Liquid implementation, bilingual translation system, dark theme, performance and accessibility. Do not alter unrelated pages, menus or bibliography.

This replaces the existing intentionally empty equipment section with a **verified-by-user, current equipment summary** while preserving links to the relevant Research, Publications, Repositories and Thesis pages.

The user explicitly corrected the Schenck internal-pressure limit to **700 bar** (70 MPa); do **not** publish 700 MPa. The user also confirmed that the historical technical ratings on the [Machine Design Group facilities page](https://machinedesign.ing.unipi.it/laboratory-facilities/) were correct for the machines described **at the time of that inventory**. Therefore, use that site as the source for its historical MTS, Rumul, Schenck, modal-analysis and full-scale bench specifications. The user's more recent StepLab, climatic-chamber, 700 bar pressure actuator, three-actuator bench and FLIR information supplements the older inventory. Do not silently merge earlier and newer machine counts into one current inventory or imply that every historical system remains in service. Do not infer that independent maxima can be reached at the same time.

## 2. Visual narrative and page layout

### 2.1 Editorial introduction with one genuine hero photograph

A split or asymmetric editorial opening, consistent with the homepage and Research Atlas:

- Section identifier, prominent page title, two or three concise sentences introducing fatigue-related research across metals, polymers, composites and additively manufactured materials.
- Featured real photograph of the machined axial specimen, **IMG_3207.jpeg** (new image). Use a purposeful close crop and negative space, maintaining the recognisable specimen geometry. **IMG_3209.jpeg** is a good alternate, not an additional near-duplicate on the same page.
- At most three short, readable topic anchors: Testing systems, Test conditions and preparation, Research collaboration. The existing anchors `#research-expertise`, `#instrumentation`, `#equipment` (once present) and `#laboratory-collaboration` must continue to resolve.
- A useful caption identifying the image accurately as a machined test specimen. Do not imply it is a failed specimen, represents measured strain or documents a specific paper unless confirmed.

### 2.2 Primary fatigue and mechanical testing facilities

Treat each featured system as one editorial row, with a photographic image when suitable, a text title, a compact description and a few carefully labelled specifications. Vary image/text placement in a controlled way; avoid six identical cards.

- **StepLab axial–torsional electrodynamic machine**. Maximum static load 33 kN, maximum dynamic load 43.5 kN, maximum frequency 250 Hz (specimen and operating-mode dependent); circular gripping Ø 6–12 mm; flat specimens up to 15 mm thick. Use a clearly identified StepLab photograph. **IMG_1270.jpg** and **IMG_3200.jpeg** are candidates, but confirm which of these depicts the main 33/43.5 kN machine before applying a model-specific caption.
- **Schenck servo-hydraulic axial–torsional system**. Axial tension/compression up to 250 kN, torque up to 2000 N·m, with a historically published maximum testing frequency of approximately 10–20 Hz. The user additionally documented an internal-pressure actuator up to **700 bar** for tubular specimens, circular gripping Ø 5–40 mm and flat specimens 8–20 mm thick. Do not assume the stated pressure, force, torque and frequency maxima are simultaneously attainable. Use **IMG_3186.jpeg** only if it depicts the correctly identified Schenck equipment; crop to favour the actuators without identifying a different rig as this machine.
- **Rumul resonant fatigue-testing machines**. The historical group facilities page documents **two systems rated 20 kN and 150 kN**, with typical operating frequencies of approximately **100–150 Hz**, for high-cycle fatigue, S–N curves and crack-growth investigations. The user's earlier approximate 100 kN figure should not replace these historically documented individual ratings. The user identified **IMG_3189.jpeg** as showing a Rumul resonant machine; do not assign that photograph to either the 20 kN or 150 kN system, or claim both systems remain in service, until machine identity/current availability is confirmed. Keep its real green frame, grips and safety label visible. **IMG_3190.jpeg** remains a less suitable alternative.
- **MTS uniaxial servo-hydraulic machines**. The historical group facilities page documents **two machines, rated 25 kN and 100 kN**, with typical maximum testing frequencies of approximately **10–20 Hz**. These are documented historical ratings, not a newly verified current inventory. Describe compactly, without a weak photograph if none cleanly identifies the systems.
- **Smaller StepLab electromechanical system**. Up to 10 kN and 20 Hz. The two StepLab photographs require identification before assigning either image to this machine. If uncertain, use a neutral equipment caption and avoid asserting the wrong model.

The apparent precision of a metric must not become an unqualified operating guarantee. Use short footnotes indicating that specimens, grips, fixture, control mode and configuration determine feasible combinations.

### 2.3 Configurable structural and vibration testing

- A configurable experimental bench currently described by the user with **three Schenck hydraulic actuators**; potential setups include tensile/torsional loading of welded joints and fatigue tests on vehicle frames. The historical group webpage separately reports a **full-scale bench that could use up to seven hydraulic actuators**. These statements may describe earlier versus later configurations or different facilities; **do not conflate them into a single current seven-actuator capacity** without confirmation. The caption for **IMG_0167.JPG** should identify a configurable bench, not a specific test performed or a seven-actuator arrangement. Project-specific setup and feasibility assessment apply.
- A smaller secondary segment for structural-dynamics/vibration investigations, with a real experimental setup photograph **IMG_8745.JPG** (TIRA shaker test arrangement) if room allows. **IMG_3192.jpeg** is an alternate technical close-up, not a required sixth hero-quality photograph. Distinguish the vibration shaker from the axial–torsional fatigue machines and do not transfer the 250 Hz StepLab limit to a separate shaker.
- The historical group facilities page documents an ABB robotic system with a Polytec laser vibrometer for **six-degree-of-freedom vibration measurements**, using electrodynamic shakers with a published frequency span **up to 10 kHz**. The user supplied **IMG_0169.JPG** showing the robot. Include this as an optional, historically documented capability, or a short supporting link, rather than asserting the robot and vibrometer are currently operational. Do not imply the 10 kHz shaker range belongs to StepLab, MTS or Schenck equipment.

**Source and time reference.** Historical system numbers, capacities and approximate frequencies above are from the [Machine Design Group's Laboratory Facilities page](https://machinedesign.ing.unipi.it/laboratory-facilities/), confirmed by the user as accurate for the equipment at that time. The newer StepLab ratings, thermal camera, 700 bar pressure limit, climatic-chamber details and three Schenck actuators are directly supplied in this conversation. Avoid asserting that all historic and more recently described devices are simultaneously present or accessible.

### 2.4 Environmental testing, specimen preparation and metrology

A visually lighter section with concise grouped text rather than one photograph for every tool.

- Induction oven: up to 900 °C, used for relevant creep–fatigue/high-temperature fatigue configurations.
- Resistance oven: 200–1000 °C.
- StepLab climatic chamber: −30 to +180 °C, available for compatible StepLab experimental configurations. The earlier stand-alone climatic chamber entry with the same range must **not** be double-counted as a second chamber.
- In-house specimen preparation: CNC lathe, milling machines and machining/tooling for round, flat, notched/unnotched and tubular specimens.
- Characterisation and metrology: contact/optical surface roughness measurement with Ra and Rz reporting; Vickers hardness testing. The historical group page additionally documents **optical/SEM microscopy, customized Charpy impact testing and strain-gauge hole-drilling residual-stress measurements**; present these only as previously documented capabilities unless present-day instruments and availability are verified. Do not imply SEM, Charpy or hole-drilling are available solely from the old site.
- **High-speed infrared thermography, FLIR X6901sc**. The user photographed the camera (**IMG_0418.JPG**) and its model label (**IMG_0420.JPG**). The model label establishes **X6901sc**, not **X6901sc SLS**. The original [FLIR X6901sc InSb datasheet, P/N 29267-201](https://support.flir.com/dsdownload/assets/29267-201-en-us.html) specifies a cooled **InSb detector**, **3.0–5.0 µm** MWIR spectral band, **640 × 512 pixels**, programmable **full-frame rate up to 1004 Hz**, **NETD ≤20 mK**, and **14-bit** digital dynamic range. Its standard **−20 to 350 °C** measurement range requires band-matched optics; optional extended ranges depend on specific filters/optics and must not be claimed as installed. These are **manufacturer instrument specifications**, not verified achievable performance for every experimental setup. Do not infer thermoelastic stress analysis, phase-locking, calibrated accuracy in the user's laboratory, or quantitative fatigue-damage detection solely from the camera's specification.

For experimental measurement, include a compact **High-speed infrared thermography** item with **IMG_0418.JPG**. The manufacturer's measured-data capabilities (640 × 512, up to 1004 full-frame images per second, 3–5 µm) are verified for FLIR X6901sc, but actual laboratory optics, calibration and acquisition settings have not been supplied. Do not add the newly provided serial-number label image **IMG_0420.JPG** to the published image gallery; it is only evidence for identifying the device.

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
| `IMG_3207.jpeg` | Hero or large opening specimen photograph | Primary | Most restrained composition and negative space; crop conservatively. |
| `IMG_0167.JPG` | Configurable structural bench | Primary | Landscape format expresses scale and capability. |
| `IMG_3186.jpeg` | Schenck actuators / structural testing | Primary | Tight composition; verify exact hardware identification. |
| `IMG_3200.jpeg` | StepLab equipment | Primary | Clear guard frame; verify whether this is the 10 kN or main machine. |
| `IMG_3189.jpeg` | Rumul resonant machine | Primary | User-identified machine, substantially clearer than IMG_3190; show machine body and gripping region. |
| `IMG_0418.JPG` | FLIR X6901sc high-speed infrared camera | Secondary | Close-up of the genuine camera. Manufacturer-verified 640 × 512, up to 1004 Hz full-frame and 3–5 µm; do not attribute unavailable accessories or undocumented test techniques. |
| `IMG_0420.JPG` | Camera model identification, not a website image | Reference only | Confirms X6901sc; label also carries an equipment serial number. Keep this photo out of the public gallery and out of the final repository assets. |
| `IMG_3190.jpeg` | Alternate Rumul image | Alternate | Less visually suitable due to handwritten notice and clutter; do not use unless IMG_3189 fails technical requirements. |
| `IMG_8745.JPG` | Vibration-testing setup | Secondary | Real experimental setup, useful if this section is sufficiently prominent. |
| `IMG_1270.jpg` | Alternate StepLab environmental setup | Alternate | Avoid duplicating indistinguishable views. |
| `IMG_3209.jpeg` | Alternate hero specimen | Alternate | Do not use alongside `IMG_3207.jpeg` in the same short page. |
| `IMG_3192.jpeg` | Alternate small shaker | Alternate | Narrow technical detail, not featured. |
| `IMG_0169.JPG` | Optional modal/robotics capability | Optional | Only if page text explicitly describes the setup. |

Exclude `IMG_8606.jpg`, `IMG_3185 1.jpeg`, `IMG_3187.jpeg` and any weakly identified or visually distracting photographs from the initial featured set.

**Asset policy:** Optimize selected real photos locally into responsive, EXIF-stripped WebP and, if necessary, one JPEG fallback each; use fixed aspect ratios, width and height to avoid layout shift. Prefer two output widths (approximately 640 and 1280 pixels), quality around 78–84, and target an initial above-the-fold photographic payload below 250 kB. A photo can be omitted if visual quality does not survive the target crop. Do not embed base64 photographs directly in HTML or use third-party image CDNs. Each photo has bilingual alt text and a short matter-of-fact caption, but never contains speculative machine identification.

**Photo upload provenance:** The original conversation uploads are available as inputs during this design, including newly attached IMG_3189.jpeg and IMG_0418.JPG, and the model-label reference IMG_0420.JPG. Optimized public-use images (excluding IMG_0420.JPG) must be included in the final GitHub PR as actual files with verified repository paths. The draft PR must never reference images only in the ChatGPT sandbox. All photo filenames must be mapped to machine descriptions explicitly, and uncertain matches checked before the final preview.

## 4. Bilingual content architecture

Current canonical source locations:
- `_pages/laboratory.md` is the one bilingual page with `translation_key: laboratory`.
- `_data/laboratory.json` contains canonical laboratory capabilities, measurement contexts and an empty `equipment` array.
- `_data/i18n/it/laboratory.json` holds Italian text keyed by canonical record IDs.
- `_includes/resource_card.html` already handles `localized_record: 'laboratory'` and simple equipment data, but the redesigned *featured* equipment should use a dedicated, scoped editorial include rather than globally changing resource cards.
- `_sass/_academic.scss`, `_sass/_technical_editorial.scss` and `_sass/_research_atlas.scss` establish palette, typography and baseline page behaviors.

Proposed implementation boundaries after plan approval:

1. Create/add canonical structured equipment entries by stable IDs in `_data/laboratory.json`. Keep numeric ranges, unit symbols, and explicit operating limitations in one record, not scattered through Markdown. Retain the existing research capabilities and valid links.
2. Add Italian counterparts to `_data/i18n/it/laboratory.json` using the user's academic-writing Skill. Preserve English machine brand/model names and standardized units. Use *fatica multiassiale*, *prove assiali–torsionali*, *pressione interna fino a 700 bar*, *camera climatica*, *prove di propagazione della cricca*, and other appropriate technical terminology.
3. Use one small, maintainable include such as `_includes/laboratory_equipment.html`, only for primary machine rows. Represent ancillary capabilities as editorial typographic sections, not excessive repeated cards.
4. Add one page-scoped Sass partial `_sass/_laboratory_editorial.scss` and import it once in `assets/css/main.scss`. No new fonts, icon package, JavaScript framework or custom backend.
5. Link local optimized image files under `assets/img/laboratory/` and include accessible `<picture>` / `<img>` markup with localized alt text, width/height, and lazy loading outside the hero.
6. Keep headings/anchors stable, including `#research-expertise`, `#instrumentation` and `#laboratory-collaboration`. Add `#equipment` only when equipment exists (it now will).

Style writing must respect `andrea-chiocca-academic-writing`: concise scientific prose, no promotional claims, no em dashes or formulaic framing, collective voice for group-owned facilities, and no translation of official machine names.

## 5. Acceptance and regression checks

- English `/laboratory/` and Italian `/it/laboratory/` render in the existing bilingual system with exactly one `main` and `h1` each.
- Same equipment IDs/order, capabilities, numerical specifications and limits in both locales, especially **700 bar** (and never the prior mistaken 700 MPa). Historical 25/100 kN MTS and 20/150 kN Rumul systems must not be replaced with a current-inventory claim. Distinguish the historical seven-actuator capacity from the user's currently described three-actuator configuration. Verify exact FLIR X6901sc manufacturer specs, not the separate SLS variant, and distinguish camera capability from lab-verified techniques. The Rumul caption must not guess which unit is photographed. Verify no duplicate environmental chamber and no implication that 250 Hz applies to every machine.
- All public photo references resolve, have bilingual alt text, fixed intrinsic dimensions and reasonable file sizes. No duplicate hero images or broken source sets.
- Preserve every currently valid anchor and cross-page link, original collaboration contact and project feasibility disclaimer.
- Light/dark themes, keyboard links, 320/375/390/768/1280/1920-pixel layouts, reduced-motion settings and no horizontal overflow. Images may be stacked responsively, not scrolled horizontally.
- Loading behavior is static progressive enhancement: visitors can read all equipment and details without JavaScript. No extra runtime package, font or remote asset request. Track HTML/CSS/above-the-fold photo byte deltas.
- Integrate focused post-build EN/IT Laboratory verification with the existing `verify_site.py`, `verify_languages.py`, and Chromium browser checks. Avoid multiplying unrelated route tests unnecessarily.
- Produce a **separate draft PR and Cloudflare EN/IT previews**. Verify the exact commit SHA's checks before requesting the user's visual approval. Do not merge without explicit authorization.

## 6. Review and stage boundaries

The **visual direction** presented in the preceding conversation is approved; the user has asked to proceed and has supplied final photographs and equipment information. This specification records that design as a durable source of truth. The user approved the written specification on 22 October 2026. A task-by-task implementation plan is now available for a separate review, after which execution may proceed on the same draft branch. Until the implementation plan is approved, PR changes remain documentation-only; the live website stays untouched.
