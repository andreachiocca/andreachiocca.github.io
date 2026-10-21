# Research Atlas scientific diagram review

All five Phase 3 overview and area figures are conceptual vector schematics.
They are not finite-element outputs, experimental data or photographs. They
reuse the established Research-page terminology and do not claim validation.

## R02. Candidate-plane fatigue traction

Stress tensor in normalized illustrative units, in Cartesian x, y and z:

    [  0.0  0.0  0.6 ]
    [  0.0  0.0  0.0 ]
    [  0.6  0.0  1.0 ]

The tensor is symmetric. The oriented candidate-plane unit normal is
n=(1,0,1)/sqrt(2). Traction is t=σn. Its resolved normal component is
(n·t)n = 1.1n and shear traction t-(n·t)n = (-0.5,0,0.5)/sqrt(2).
Shear is orthogonal to the plane normal. The same isometric projection
P(x,y,z)=(sqrt(3)/2*(x-y),(x+y)/2-z) is used for the oriented
plane, normal, shear and resultant vectors. The arrowheads represent
the **traction vectors**, not scalar stress components or material
deformation. Numerical values are chosen for illustration only;
no fatigue damage parameter or result is calculated.

The script `scripts/generate_research_atlas_figures.py` owns the projected
traction-arrow endpoints, supports `--check` and rejects nonsymmetric
tensors and zero-length plane normals. For a different tensor/plane, update
the script inputs and rerun it before committing SVG changes.

## R03. Welded joint

Cross-section of a schematic, symmetric double-V butt joint. The upper and
lower grooves narrow towards the mid-thickness root, with an illustrative
filled fusion region. The drawing specifies no plate thickness, groove angle,
pass sequence, residual-stress distribution, thermal history or measured
heat-affected-zone boundary. The interior "geometry only" label was removed.

## R04. Layered structure

Schematic layers and a representative order-3 Hilbert infill path, not a
specific machine or a claim that this path is used in every additive process.
The deterministic 8 by 8 traversal visits each cell centre once, and every
successive move crosses one grid edge. The generator maps that planar path
onto the top-layer parallelogram; it does not represent a computed thermal
field, melt pool, material track width or validated build plan. A subdued
CSS-only trace travels along the static path. It has no JavaScript dependency
and stops moving under `prefers-reduced-motion: reduce`.

Hilbert infill has been studied as one additive-manufacturing path strategy.
See [a path-planning review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7407298/)
and [a study of Hilbert-curve filling](https://pmc.ncbi.nlm.nih.gov/articles/PMC9586239/).

## R05. Specimen loading

Idealized tensile loading applied outward at opposite specimen ends.
The paired arrows show consistent directions and no force magnitude.
A minimalist foil-gauge symbol replaces the earlier gauge-length marks. Its
long grid segments are parallel to the specimen's axial load and intended
axial-strain direction. The drawing does not specify an actual sensor,
installation, wiring, test equipment or validated experimental configuration.
The orientation follows [strain-gauge alignment guidance](https://strainblog.micro-measurements.com/tips/mark-spot).

## R01. Overview

Three connected, undirected symbols represent a Cauchy traction relation,
a triangular discretization and an idealized tensile specimen. They refer to
analytical, numerical and experimental approaches respectively. The network
does not imply a mandatory workflow or that every project uses all three
approaches; the mesh is not a calculated field and the specimen is not an
observation or equipment drawing. The line-art composition takes only general
stylistic cues from the three images supplied by the owner.

## Common constraints

All figures are inline SVGs with localized captions, no remote dependencies
and unique SVG IDs. Only the Hilbert trace moves, through a small CSS animation;
its complete base path remains visible without motion or JavaScript. Rendering
remains text-complete with JavaScript disabled. If a figure selection is not
implemented for a new canonical ID, the research chapter retains its text,
links and heading.
