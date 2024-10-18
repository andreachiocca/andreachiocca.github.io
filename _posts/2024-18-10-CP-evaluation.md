---
layout: distill
title: Efficient Method for the Evaluation of CP Factor and CP Orientation
description: A detailed explanation of an efficient method for evaluating the Critical Plane (CP) factor and orientation.
tags: fatigue evaluation, critical plane, strain tensor
giscus_comments: true
date: 2024-10-18
featured: true

authors:
  - name: Andrea Chiocca
    url: "https://andreachiocca.github.io/"
    affiliations:
      name: Department of Civil and Industrial Engineering - University of Pisa

bibliography: 2024-10-18-CP-eval.bib

# Optionally, you can add a table of contents to your post.
toc:
  - name: Introduction
  - name: Theoretical Background
  - name: Equations and Method
  - name: References

---

## Introduction

In this post, we discuss an efficient method to evaluate the Critical Plane (CP) factor and CP orientation, as commonly applied in fatigue assessments. This method maximizes the shear strain amplitude, aligning with the original Fatemi-Socie critical plane factor.

## Theoretical Background

As commonly done in fatigue assessments, the load-time history is considered as a discrete sequence of peaks and valleys instead of a continuous function over time. The stress and strain tensors related to the generic $i-th$ loading condition can be defined as:

$$
\vect{\sigma}^i =
\begin{bmatrix}
\sigma_{xx}^i & \tau_{xy}^i & \tau_{xz}^i \\
\tau_{yx}^i & \sigma_{yy}^i & \tau_{yz}^i \\
\tau_{zx}^i & \tau_{zy}^i & \sigma_{zz}^i \\
\end{bmatrix}, \;
\vect{\varepsilon}^i =
\begin{bmatrix}
\varepsilon_{xx}^i & \frac{\gamma_{xy}^i}{2} & \frac{\gamma_{xz}^i}{2} \\
\frac{\gamma_{yx}^i}{2} & \varepsilon_{yy}^i & \frac{\gamma_{yz}^i}{2} \\
\frac{\gamma_{zx}^i}{2} & \frac{\gamma_{zy}^i}{2} & \varepsilon_{zz}^i \\
\end{bmatrix}
$$

We can now define the strain tensor range relative to the loading conditions $i$ and $i+1$ as the difference between strain tensors $\vect{\varepsilon}^i$ and $\vect{\varepsilon}^{i+1}$:

$$
\vect{\Delta \varepsilon} = \vect{\varepsilon}^i - \vect{\varepsilon}^{i+1}
$$

## Equations and Method

To compute the principal strain tensor range parameters ($\Delta\varepsilon_{1}$, $\Delta\varepsilon_{2}$, $\Delta\varepsilon_{3}$), we first define them as the eigenvalues of the matrix $\vect{\Delta \varepsilon}$:

$$
\vect{\Delta\varepsilon} =
\begin{bmatrix}
\Delta\varepsilon_{xx} & \frac{\Delta\gamma_{xy}}{2} & \frac{\Delta\gamma_{xz}}{2} \\
\frac{\Delta\gamma_{yx}}{2} & \Delta\varepsilon_{yy} & \frac{\Delta\gamma_{yz}}{2} \\
\frac{\Delta\gamma_{zx}}{2} & \frac{\Delta\gamma_{zy}}{2} & \Delta\varepsilon_{zz} \\
\end{bmatrix}
=
\begin{bmatrix}
\Delta\varepsilon_{1} & 0 & 0 \\
0   & \Delta\varepsilon_{2} & 0 \\
0   & 0  & \Delta\varepsilon_{3} \\
\end{bmatrix}
$$

The maximum shear strain range $\Delta\gamma_{max}$ can be computed using the principal strain variations:

$$
\frac{\Delta\gamma_{max}}{2} = \frac{(\Delta\varepsilon_{1} - \Delta\varepsilon_{3})}{2}
$$

To compute the CP factor, we need to evaluate the normal directions to $\Delta\gamma_{max}$ planes using the eigenvectors of $\vect{\Delta\varepsilon}$:

$$
R_p =
\begin{bmatrix}
n_{11} & n_{12} & n_{13}\\
n_{21} & n_{22} & n_{23}\\
n_{31} & n_{32} & n_{33}\\
\end{bmatrix}
$$

By rotating the system of reference by $\omega =\frac{\pi}{4}$ about the local $y$-axis, we get the rotation matrix:

$$
R_y =
\begin{bmatrix}
\cos(\frac{\pi}{4}) & 0 & \sin(\frac{\pi}{4})\\
0 & 1 & 0\\
-\sin(\frac{\pi}{4}) & 0 & \cos(\frac{\pi}{4})\\
\end{bmatrix}
$$

The final rotation matrix that defines the orientation of the $\Delta \gamma_{max}$ plane is:

$$
R = R_pR_y
$$

## Conclusion

This method simplifies the evaluation of CP orientation and $\Delta \gamma_{max}$ for fatigue assessments, providing a streamlined and computationally efficient approach.