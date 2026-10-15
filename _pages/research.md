---
layout: page
title: Research
permalink: /research/
description: Research by Andrea Chiocca on multiaxial fatigue, residual stresses, welded structures, additive manufacturing, and computational mechanics.
nav: true
nav_order: 3
---

My research combines numerical modelling, analytical methods, and experimental testing to assess the structural integrity of engineering materials and components. The areas below connect my research activities to representative publications.

## Multiaxial fatigue and critical plane methods

I investigate efficient methods for evaluating critical plane damage parameters and assessing fatigue under complex loading. Topics include closed-form and semi-analytical algorithms, proportional and non-proportional loading, and the Effective Critical Plane approach.

Representative publications:

- [Fatigue assessment through the Effective Critical Plane factor]({{ '/publications/' | relative_url }}#Chiocca2024b) (2024).
- [A closed-form solution for evaluating the Findley critical plane factor]({{ '/publications/' | relative_url }}#Chiocca2024a) (2024).
- [An efficient algorithm for critical plane factors evaluation]({{ '/publications/' | relative_url }}#Chiocca2023) (2023).

Representative extensions include [ductile cast iron under non-proportional loading]({{ '/publications/' | relative_url }}#Chiocca2025) and a [perspective on notched components]({{ '/publications/' | relative_url }}#Frendo2025). Related [ECP datasets]({{ '/repositories/' | relative_url }}#zenodo-14198237) support reproducibility.

Further explanations are available in my [research notes]({{ '/blog/' | relative_url }}).

## Residual stresses and welded structures

I study how welding processes generate residual stresses and how these stresses affect fatigue life. This work combines thermal-structural simulations with experimental measurements and fatigue testing.

Representative publications:

- [Influence of residual stresses on the fatigue life of welded joints: numerical simulation and experimental tests]({{ '/publications/' | relative_url }}#Chiocca2022) (2022).
- [Evaluation of residual stresses in a pipe-to-plate welded joint]({{ '/publications/' | relative_url }}#Chiocca2021) (2021).

The [2026 welded-joints study]({{ '/publications/' | relative_url }}#Chiocca2026WeldedECP) connects ECP predictions to weld-metal and base-metal calibration. Its [supporting data]({{ '/repositories/' | relative_url }}#zenodo-18416255) are archived separately.

## Additive manufacturing and material behaviour

My work includes numerical and experimental assessment of additively manufactured structures, representative structure elements, and process-related thermal effects.

Representative outputs:

- [Representative structure elements for the fatigue assessment of additively manufactured components]({{ '/publications/' | relative_url }}#Wagener2021) (2021).
- [Technological implications of the Rosenthal solution for welding and additive manufacturing]({{ '/publications/' | relative_url }}#Moda2022) (2022).
- [Effects of coating on the fatigue endurance of FDM lattice structures]({{ '/publications/' | relative_url }}#Chiocca2022a) (2022).

## Component testing and industrial applications

Experimental methods include static and fatigue testing at controlled temperatures, strain measurement, vibration measurements and thermal monitoring. My [2025 study of thermoset and thermoplastic composites]({{ '/publications/' | relative_url }}#Chiocca2025ab) addresses temperature effects. [Hybrid SPR-joint tensile data]({{ '/repositories/' | relative_url }}#zenodo-12741922) are also available.

The [academic CV]({{ '/cv/' | relative_url }}) documents work on composite materials and joints, automotive components, and printed circuit board assemblies. Related publications include [dynamic characterisation of PCB assemblies for fatigue analysis]({{ '/publications/' | relative_url }}#Fontana2023) and [fatigue assessment of a Formula SAE rear upright]({{ '/publications/' | relative_url }}#Chiocca2024).

## International collaborations

{% for service in site.data.academic_service %}
**{{ service.role }}** {{ service.description }} [Working group]({{ service.url }}) · [COST Action]({{ service.action_url }}).
{% endfor %}

The [FABEST participant package]({{ '/repositories/' | relative_url }}#zenodo-21534682) supports a blind fatigue-life prediction competition. Separately, my [multiaxial fatigue repository]({{ '/repositories/' | relative_url }}#multiaxial-fatigue) contributes to the WG4.3 methodological comparison and review activity.

Research visits include Czech Technical University in Prague (FABER WG6, June 2026), Aarhus University (Circle U., January 2026), NTNU (Erasmus+, July 2024), and Fraunhofer LBF (doctoral research, February–June 2021).

## Selected collaborative projects

- **PRA 2022, University of Pisa (2022–2024):** project co-lead for optimisation of extrusion-based additive manufacturing of metal and ceramic components.
- **PRIN PNRR 2022 (2025):** team member on experimental characterisation, theoretical modelling and CAE simulation of hybrid joints between dissimilar metals for lightweight vehicle structures.
- **PON 2014–2020 programme (2022–2025):** research on structural integrity in automotive applications, including collaboration with Pierburg Pump Technology Italy / Rheinmetall.

## Research environment

I work in the machine design group in the [Department of Civil and Industrial Engineering](https://www.dici.unipi.it/) at the [University of Pisa](https://www.unipi.it/). Previous research experience at Fraunhofer LBF and industrial research activities are documented in the CV.

For scientific enquiries and potential collaborations, please [contact me by email](mailto:andrea.chiocca@unipi.it).
