---
layout: distill
title: Efficient Method for the Evaluation of CP Factor and CP Orientation
description: A detailed explanation of an efficient method for evaluating the Critical Plane (CP) factor and orientation.
tags: fatigue evaluation, critical plane, strain tensor
giscus_comments: false
date: 2024-10-18
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
  - name: Methodology
  - name: Stress and Strain Tensors
  - name: Principal Directions and Rotations
  - name: Local Maxima Search
  - name: Summary

---

## Novel semi-analytical method
\label{Methodology}

Consistently with standard fatigue assessment practices, the load-time history is treated as a discrete sequence of peaks and valleys rather than a continuous function over time. Within this framework, the stress and strain tensors $\mathbf{\sigma}^{(i)}$ and $\mathbf{\varepsilon}^{(i)}$ referring to the $i$-th loading condition can be defined as follows:

$$
\mathbf{\sigma}^i =
\begin{bmatrix}
\sigma_{xx}^i & \tau_{xy}^i & \tau_{xz}^i \\
\tau_{yx}^i & \sigma_{yy}^i & \tau_{yz}^i \\
\tau_{zx}^i & \tau_{zy}^i & \sigma_{zz}^i \\
\end{bmatrix}, \;
\mathbf{\varepsilon}^i =
\begin{bmatrix}
\varepsilon_{xx}^i & \frac{\gamma_{xy}^i}{2} & \frac{\gamma_{xz}^i}{2} \\
\frac{\gamma_{yx}^i}{2} & \varepsilon_{yy}^i & \frac{\gamma_{yz}^i}{2} \\
\frac{\gamma_{zx}^i}{2} & \frac{\gamma_{zy}^i}{2} & \varepsilon_{zz}^i \\
\end{bmatrix}
$$

During a load cycle, two successive loading conditions, denoted as $i$ and $i+1$, are considered. This work does not address how to find these load steps; these can be derived through standard cycle counting methods such as level-crossing, peak-to-peak, simple-range, or rainflow counting~\cite{International2005}.

Accordingly, tensor quantities like stress and strain ranges are defined, respectively, as $\mathbf{\Delta \sigma}$ and $\mathbf{\Delta \varepsilon}$:

$$
\mathbf{\Delta \sigma} = \mathbf{\sigma}^{(i)} - \mathbf{\sigma}^{(i+1)}, \quad \mathbf{\Delta \varepsilon} = \mathbf{\varepsilon}^{(i)} - \mathbf{\varepsilon}^{(i+1)}
$$

All tensor quantities are defined in the same reference frame and can be represented as matrices, as shown in Equation~\ref{eq_2}.

{% details Click here to view the stress and strain range tensors %}
Equation for stress and strain range tensors:

$$
\mathbf{\sigma}^{(i)} =
\begin{bmatrix}
\sigma_{xx} & \tau_{xy} & \tau_{xz} \\
 & \sigma_{yy} & \tau_{yz} \\
 \multicolumn{2}{c}{\scriptsize \text{sym.}} & \sigma_{zz} \\
\end{bmatrix}^{(i)}, \quad
\mathbf{\varepsilon}^{(i)} =
\begin{bmatrix}
\varepsilon_{xx} & \frac{\gamma_{xy}}{2} & \frac{\gamma_{xz}}{2} \\
& \varepsilon_{yy} & \frac{\gamma_{yz}}{2} \\
\multicolumn{2}{c}{\scriptsize \text{sym.}} & \varepsilon_{zz} \\
\end{bmatrix}^{(i)}
$$
{% enddetails %}

## Principal Directions and Rotations

Through an eigenvalue-eigenvector analysis, the principal stress and strain parameters ($\Delta\sigma_{1}$, $\Delta\sigma_{2}$, $\Delta\sigma_{3}$) are obtained together with the principal directions ($\mathbf{\bar{n}_1}^{k}$, $\mathbf{\bar{n}_2}^{k}$, and $\mathbf{\bar{n}_3}^{k}$). These define the principal coordinate system.

$$
R_p^{k} =
\begin{bmatrix}
n_{11} & n_{12} & n_{13} \\
n_{21} & n_{22} & n_{23} \\
n_{31} & n_{32} & n_{33} \\
\end{bmatrix}^{k}
$$

The full rotation matrix $R^k_f$ describing the transformation from the global to the final reference frame can be derived through the concatenation of the principal rotation matrices, as shown in Equation~\ref{Rmatrix}.

## Local Maxima Search

To find the maximum value of the damage parameter, different paths through the largest Mohr's circles are considered. For the $FS$ or $FI$ damage parameter, the semi-analytical method is broken down into three distinct steps as described below:

{% details Click to expand steps %}

1. In the first step, planes lying on the largest Mohr's circle are considered.
2. The damage factor is calculated for different orientations.
3. The maximum value is found for planes rotated about different axes.

{% enddetails %}

### Stress and Strain Ranges:

$$
\Delta\tau(\omega) = \left( \frac{\Delta\sigma_1 - \Delta\sigma_3}{2} \right)\sin(2\omega) \quad \text{for} \, FI
$$

$$
\frac{\Delta\gamma}{2}(\omega) = \left( \frac{\Delta\varepsilon_1 - \Delta\varepsilon_3}{2} \right)\sin(2\omega) \quad \text{for} \, FS
$$

### Graphical representation:

{% details Click to view graphical representation %}
![Mohr's Circles Representation](/assets/img/FEM_2.jpg)
{% enddetails %}

## Summary

The semi-analytical method provides a framework to evaluate the fatigue damage factor based on tensor ranges. By analyzing stress and strain through different load cycles, the method accounts for complex loading scenarios and material plasticity.

