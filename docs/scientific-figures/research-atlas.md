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

Cross-section of a schematic, symmetric butt-weld preparation and filled
joint. Colour distinguishes the central fusion region from surrounding
material. No residual-stress distribution, thermal history, or measured
heat-affected-zone boundary is indicated.

## R04. Layered structure

Schematic layers and a representative scan/deposition path, not a
specific machine or additive manufacturing process. The figure does not
imply a melt-pool geometry, computed thermal field or validated path.

## R05. Specimen loading

Idealized tensile loading applied outward at opposite specimen ends.
The paired arrows show consistent directions and no force magnitude.
Measurement marks indicate a generic gauge region, not actual sensors,
test equipment or a validated experimental configuration.

## R01. Overview

The triangular network suggests complementary analytical, computational
and experimental activities. It does not imply one mandatory workflow or
that every project uses all three approaches.

## Common constraints

All figures are inline, static SVGs with localized captions, no remote
dependencies and unique SVG IDs. Rendering remains text-complete with
JavaScript disabled. If a figure selection is not implemented for a new
canonical ID, the research chapter retains its text, links and heading.
