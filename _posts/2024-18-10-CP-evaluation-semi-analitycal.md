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
  - name: Novel Semi-Analytical Method
  - name: Methodology
  - name: Stress and Strain Tensors
  - name: Principal Reference Frame and Rotations
  - name: Maximum Damage Parameter

---
## Novel Semi-Analytical Method

### Methodology

Consistent with standard fatigue assessment practices, load-time history is treated as a discrete sequence of peaks and valleys rather than a continuous function over time. The stress and strain tensors for the $$ i $$-th loading condition are defined as follows:

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

During a load cycle, two successive loading conditions are denoted as $$ i $$ and $$ i+1 $$.

### Stress and Strain Ranges

Tensor quantities, such as stress and strain ranges, are defined as follows:

$$
\mathbf{\Delta \sigma} = \mathbf{\sigma}^{(i)} - \mathbf{\sigma}^{(i+1)}, \: \mathbf{\Delta \varepsilon} = \mathbf{\varepsilon}^{(i)} - \mathbf{\varepsilon}^{(i+1)}
$$

All tensor quantities are defined within the same reference frame and can be represented as matrices.

### Principal Reference Frame and Rotations

Through an eigenvalue-eigenvector analysis, principal stress and strain parameters are obtained, along with the principal directions:

$$
\mathbf{\bar{n}_1}^k =
\begin{bmatrix}
n_{11}\\
n_{21}\\
n_{31}\\
\end{bmatrix}^{k}, \;
\mathbf{\bar{n}_2}^k =
\begin{bmatrix}
n_{12}\\
n_{22}\\
n_{32}\\
\end{bmatrix}^{k}, \;
\mathbf{\bar{n}_3}^k =
\begin{bmatrix}
n_{13}\\
n_{23}\\
n_{33}\\
\end{bmatrix}^{k}
$$

These directions define the principal coordinate system, and the rotation matrix $$ R_p^k $$ describes the transformation from the global reference frame:

$$
R_p^{k} =
\begin{bmatrix}
n_{11} & n_{12} & n_{13}\\
n_{21} & n_{22} & n_{23}\\
n_{31} & n_{32} & n_{33}
\end{bmatrix}^{k}
$$

### Rotational Transformation

To describe transformations, such as rotations around the local axes, the rotation matrix $$ R_{\mathbf{\bar{n}_2}} $$ is given as:

$$
R_{\mathbf{\bar{n}_2}} =
\begin{bmatrix}
\cos(\omega) & 0 & \sin(\omega)\\
0 & 1 & 0\\
-\sin(\omega) & 0 & \cos(\omega)
\end{bmatrix}
$$

The final transformation matrix $$ R_f^k $$ is obtained by multiplying the principal and rotational matrices:

$$
R_f^k = R_p^k R_{\mathbf{\bar{n}_2}} =
\begin{bmatrix}
R_{11} & R_{12} & R_{13}\\
R_{21} & R_{22} & R_{23}\\
R_{31} & R_{32} & R_{33}
\end{bmatrix}^{k}
$$

### Maximum Damage Parameter

For fatigue assessment, local maxima of the damage parameter are identified along predefined paths, considering planes identified by points on the largest Mohr's circle of stress or strain. Closed-form expressions for shear stress and shear strain variations along these paths are:

$$
\Delta \tau(\omega) = \left( \frac{\Delta\sigma_1 - \Delta\sigma_3}{2} \right) \sin(2\omega) \quad \text{for FI}
$$

$$
\frac{\Delta \gamma}{2}(\omega) = \left( \frac{\Delta\varepsilon_1 - \Delta\varepsilon_3}{2} \right) \sin(2\omega) \quad \text{for FS}
$$

A more detailed description of the stress paths and Mohr's circles is shown in Figure~\ref{FSMAX}.