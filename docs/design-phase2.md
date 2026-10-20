# Phase 2 homepage visual prototype

Branch: `design/phase-2-homepage-editorial`. This is a review-only first
iteration of the approved Direction B.

## Scope

- Homepage-only wider composition, with a left text column and right technical
  schematic, portrait and office-contact rail.
- Custom inline vector illustration of schematic combined loading and geometry.
  This is **conceptual artwork**, not a fatigue result, measurement, simulation
  or published research figure.
- Editorial treatment of existing research, FABER, publication, open-science
  and collaboration sections.
- Mobile stacking and dark-mode compatibility.
- Existing localized content, publication ordering, navigation, URLs, research
  records and shared templates are retained.
- Styling is isolated in `_sass/_homepage_phase2.scss`; all rules are scoped
  to `.home-page--editorial` or `body.academic-home-v2`.

## Preview

Cloudflare Pages should deploy an isolated review build for the PR number.
The pull request workflow uses the actual head SHA and publishes a branch alias
`https://pr-N.academic-website-preview.pages.dev/`, with Italian home at
`/it/`. These links become available only after the workflow succeeds.

## Review criteria

- Verify the first fold at 375, 390, 768, 1280 and desktop widths.
- Test Italian homepage content length, header and contact rail.
- Confirm all 5 most recent papers, metadata and page links remain.
- Inspect focus states and contrast in light and dark themes.
- Avoid representing the technical drawing as experimental data.
- Confirm that the production homepage is unchanged before the Phase 2 merge.

## Follow-up refinements

- FIG. 01 uses a true isometric **cube** with matched projected edge lengths
  and representative normal and shear traction arrows, recalling the Cauchy
  stress element. The vectors are illustrative, not a complete stress tensor.
- FIG. 02 is a compact branching line diagram accompanying the section for
  students and research partners, balancing the more prominent FIG. 01 and the
  FABER panel in section 03.
- After review, propagate the approved design incrementally to the research,
  publications, research-output catalogue, laboratory, teaching, thesis and CV
  pages using shared styles and page-level patterns. Preserve content, routes,
  published data and accessibility checks for each step.
