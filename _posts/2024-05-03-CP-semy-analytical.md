---
layout: distill
title: Rapid and Accurate Semi-Analytical Method for Fatigue Assessment
description: A semi-analytical method for fatigue assessment using critical plane methods under non-proportional loading and material plasticity.
tags: fatigue assessment, critical plane, semi-analytical method
giscus_comments: false
date: 2024-03-05
featured: true

authors:
  - name: Andrea Chiocca
    url: "https://andreachiocca.github.io/"
    affiliations:
      name: Department of Civil and Industrial Engineering - University of Pisa
  - name: Francesco Frendo
    url: "https://unimap.unipi.it/cercapersone/dettaglio.php?ri=5946"
    affiliations:
      name: Department of Civil and Industrial Engineering - University of Pisa
  - name: Michele Sgamma
    affiliations:
      name: Department of Civil and Industrial Engineering - University of Pisa

bibliography: 2024-10-18-CP-eval.bib

toc:
  - name: Introduction
  - name: Critical Plane Factors
  - name: Standard Plane Scanning Method
  - name: Semi-Analytical Method
  - name: Results and Discussion

---

## Introduction

Fatigue assessment remains a crucial concern for designers due to unexpected failures during in-service loading. Critical plane methods identify early crack propagation directions but are computationally demanding when dealing with real-world scenarios, complex geometries, and loading conditions. This study introduces a semi-analytical method to efficiently calculate critical plane factors, particularly for finite element analysis (FEA) under elastic-plastic material behavior and non-proportional loading conditions.

## Critical Plane Factors

The proposed method <d-cite key="Sgamma2024a"></d-cite> applies to all critical plane factors that require maximization of the entire formulation. In this case two critical plane factors will be used as examples, the extended Fatemi-Socie critical plane factor $$FS$$ and the Findley critical plane factor $$FI$$:

$$
FS = \max \left[ \frac{\Delta \gamma}{2} \left( 1 + k_{FS} \frac{\sigma_{n,max}}{\sigma_y} \right) \right]
$$

$$
FI = \Delta \tau + k_{FI} \sigma_{n,max}
$$

Where:
- $$ \Delta \gamma $$: Shear strain range
- $$ \Delta \tau $$: Shear stress range
- $$ \sigma_{n,max} $$: Maximum normal stress
- $$ \sigma_y $$: Yield strength

## Standard Plane Scanning Method

The standard approach involves scanning all possible plane orientations around each node in the finite element model (FEM), which involves rotating the plane in increments and calculating critical plane parameters, resulting in substantial computational demands. Angular increments are typically 10°, but finer grids (5°–8°) are recommended for higher accuracy.

The scanning method uses the following rotation matrix:

$$
R = R_z(\psi) R_y(\theta) = \begin{bmatrix} \cos(\theta) \cos(\psi) & -\sin(\psi) & \cos(\psi) \sin(\theta) \\ \sin(\psi) \cos(\theta) & \cos(\psi) & \sin(\psi) \sin(\theta) \\ -\sin(\theta) & 0 & \cos(\theta) \end{bmatrix}
$$

## Semi-Analytical Method

This novel semi-analytical method discretizes the load-time history as peaks and valleys, defining stress $$ \sigma^{(i)} $$ and strain $$ \varepsilon^{(i)} $$ tensors for each loading condition. Successive load conditions $$ i $$ and $$ i+1 $$ allow the calculation of tensor ranges:

$$
\Delta \sigma = \sigma^{(i)} - \sigma^{(i+1)}, \: \Delta \varepsilon = \varepsilon^{(i)} - \varepsilon^{(i+1)}
$$

Principal stress/strain parameters are obtained via eigenvalue analysis, and critical plane orientations are determined by rotating around the principal axes&#8203;:contentReference[oaicite:3]{index=3}.

The rotation matrix for the transformation is:

$$
R_{\bar{n}_2} = \begin{bmatrix} \cos(\omega) & 0 & \sin(\omega) \\ 0 & 1 & 0 \\ -\sin(\omega) & 0 & \cos(\omega) \end{bmatrix}
$$

The method evaluates critical plane parameters along predefined paths in three steps, reducing computational demands compared to the standard scanning method.

## Results and Discussion

Finite element simulations were performed on a notched specimen under proportional and non-proportional loading. The proposed semi-analytical method achieved a 97% reduction in computation time compared to the standard plane scanning method, while maintaining high accuracy (error < 0.5%). The method was validated by comparing it with the standard plane scanning results under different loading conditions.

The performance index $$ PI $$, defined as:

$$
PI = \left( 1 - \frac{t_{sa}}{t_{ps}} \right)
$$

where $$ t_{sa} $$ is the computation time for the semi-analytical method and $$ t_{ps} $$ is for the plane scanning method, shows the efficiency of the proposed approach.

## Conclusion

This semi-analytical method for critical plane evaluation significantly reduces computational time while retaining accuracy, making it a promising tool for complex FEM fatigue assessments under multiaxial, non-proportional, and elastic-plastic loading conditions. The method's simplicity allows for easy implementation in existing computational tools.

A supplementary Matlab® script implementing the method is available on GitHub: [SeAn-CP](https://github.com/achiocca1/SeAn-CP).