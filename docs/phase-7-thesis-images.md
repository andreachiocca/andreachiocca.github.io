# Phase 7 thesis illustrations

The image files are provided by the website owner. Optimized WebP copies should be committed into `assets/img/thesis/` on the Phase 7 PR branch, using these exact filenames.

- `multiaxial-phase-comparison.webp` — illustrative proportional and non-proportional harmonic stresses. This is not experimental or validation data. Displayed for the open-source multiaxial fatigue thesis.
- `pcb-bending-setup.webp` — a bending-test fixture with a thin specimen. The proposed PCBA-capacitor thesis involves shaker experiments; do not identify the photo as a shaker test or as a completed PCBA experiment.

Technical mapping, captions, alternative text and dimensions are maintained in `_data/thesis_opportunities.json` with the Italian localization in `_data/i18n/it/thesis.json`.

The thesis include conditionally displays a figure only when the corresponding static image is present, so a missing photo never creates a broken image link in production.
