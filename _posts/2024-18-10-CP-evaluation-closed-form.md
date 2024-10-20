---
layout: distill
title: Closed-Form Solution for the Evaluation of CP Factor and CP Orientation
description: A detailed explanation of an efficient method for evaluating the Critical Plane (CP) factor and orientation.
tags: fatigue evaluation, critical plane, strain tensor
giscus_comments: false
date: 2023-03-18
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

# Optionally, you can add a table of contents to your post.
toc:
  - name: Introduction
  - name: Theoretical Background
  - name: Equations and Method
  - name: Application Example
  - name: References

---

## Introduction

In this post, we present an optimized method for evaluating the Critical Plane (CP) factor and determining CP orientation for fatigue analysis under multiaxial loading conditions. This approach is based on an efficient algorithm that streamlines the identification of the maximum shear strain amplitude and normal stress, aligning with critical plane criteria such as the Fatemi-Socie CP factor. The method is ideal for structural components with complex geometries, such as notched specimens, and significantly reduces calculation time while maintaining accuracy.

The application of this method can be found detailed in some of the author's publications: Chiocca et al. <d-cite key="Chiocca2023"></d-cite>, <d-cite key="Chiocca2023a"></d-cite>,<d-cite key="Chiocca2024c"></d-cite>, <d-cite key="Chiocca2024"></d-cite>.



## Theoretical Background

The Fatemi-Socie CP factor ($$FS$$) <d-cite key="Fatemi1988"></d-cite> is considered as a reference:

$$
FS=\frac{\Delta \gamma}{2} \left( 1 + k \frac{\sigma_{n,max}}{S_y} \right)
$$

where $$k$$ is the material parameter found by fitting the uniaxial experimental data against the pure torsion data, $$\Delta \gamma$$ is the shear strain range, $$\sigma_{n,max}$$ is the normal stress acting on the plane where the shear strain range is evaluated and $$S_y$$ is the material yield strength.

In fatigue analysis, the stress and strain tensors for the $$i-th$$ loading condition are defined as follows:

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

The strain tensor range, considering two successive loading conditions $$i$$ and $$i+1$$, is computed as the difference between the two strain tensors:

$$
\mathbf{\Delta \varepsilon} = \mathbf{\varepsilon}^i - \mathbf{\varepsilon}^{i+1}
$$

## Equations and Method

### Principal Strain Calculation

To evaluate the principal strain tensor range ($$\Delta\varepsilon_{1}$$, $$\Delta\varepsilon_{2}$$, $$\Delta\varepsilon_{3}$$), we compute the eigenvalues of the matrix $$\mathbf{\Delta \varepsilon}$$:

$$
\mathbf{\Delta\varepsilon} =
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

The principal strains $$\Delta\varepsilon_{1}$$, $$\Delta\varepsilon_{2}$$, and $$\Delta\varepsilon_{3}$$ represent the maximum, intermediate, and minimum normal strains, respectively, in their corresponding principal directions. These directions are defined by the eigenvectors of the strain tensor $$\mathbf{\Delta\varepsilon}$$.

### Eigenvectors

The eigenvectors corresponding to the principal strains define the orientation of the planes on which these principal strains act. These eigenvectors are represented as the columns of the eigenvector matrix $$R_p$$:

$$
R_p =
\begin{bmatrix}
n_{11} & n_{12} & n_{13}\\
n_{21} & n_{22} & n_{23}\\
n_{31} & n_{32} & n_{33}\\
\end{bmatrix}
$$

- The first column vector, $$\mathbf{n}_1 = \begin{bmatrix} n_{11} \\ n_{21} \\ n_{31} \end{bmatrix}$$, corresponds to the principal direction associated with the maximum principal strain $$\Delta\varepsilon_{1}$$.
- The second column vector, $$\mathbf{n}_2 = \begin{bmatrix} n_{12} \\ n_{22} \\ n_{32} \end{bmatrix}$$, corresponds to the direction of the intermediate principal strain $$\Delta\varepsilon_{2}$$.
- The third column vector, $$\mathbf{n}_3 = \begin{bmatrix} n_{13} \\ n_{23} \\ n_{33} \end{bmatrix}$$, corresponds to the direction of the minimum principal strain $$\Delta\varepsilon_{3}$$.

These eigenvectors define the orientation of the principal planes (the planes on which no shear strain occurs) and are used to establish the local coordinate system for evaluating the Critical Plane.

### Maximum Shear Strain

The maximum shear strain range $$\Delta\gamma_{max}$$ is calculated as:

$$
\frac{\Delta\gamma_{max}}{2} = \frac{(\Delta\varepsilon_{1} - \Delta\varepsilon_{3})}{4}
$$

### Rotation for Critical Plane Orientation

To adjust the reference system for proper plane alignment, a rotation by $$\omega = \frac{\pi}{4}$$ about the local $$y$$-axis is applied, resulting in the following rotation matrix:

$$
R_y =
\begin{bmatrix}
\cos(\frac{\pi}{4}) & 0 & \sin(\frac{\pi}{4})\\
0 & 1 & 0\\
-\sin(\frac{\pi}{4}) & 0 & \cos(\frac{\pi}{4})\\
\end{bmatrix}
$$

The final rotation matrix, $R$, defining the CP orientation is obtained by multiplying $$R_p$$ with $$R_y$$:

$$
R = R_pR_y
$$

### Maximum Normal Stress ($\sigma_{n,\text{max}}$)

The maximum normal stress, $$\sigma_{n,\text{max}}$$, on the critical plane is calculated by projecting the stress tensor $$\mathbf{\sigma}$$ onto the normal vector $$\mathbf{n}$$ of the critical plane. The normal vectors to the critical plane are two in this case represented by $$\mathbf{\widetilde{n_1}}=R(:,1)$$ or $$\mathbf{\widetilde{n_3}}=R(:,3)$$. The normal stress is computed as follows:

$$
\sigma_{n,\text{max}} = \max \left( \mathbf{\widetilde{n_1}}^T \mathbf{\sigma} \mathbf{\widetilde{n_1}},\mathbf{\widetilde{n_3}}^T \mathbf{\sigma} \mathbf{\widetilde{n_3}} \right)
$$



## Application Example

This method has been applied to various notched specimens subjected to multiaxial loading, and under elastic-plastic material hypotesis. The approach not only accurately predicts fatigue life but also demonstrates a significant reduction in computational effort compared to traditional critical plane evaluation methodologies.

## Conclusion

This optimized algorithm for evaluating CP factors and determining the orientation of critical planes enhances the efficiency of fatigue assessments, especially for components under complex multiaxial loading conditions. The approach has been successfully validated against experimental data and offers practical advantages in engineering applications.

A supplementary Matlab® script implementing the method is available on GitHub: [CPOpt](https://github.com/achiocca1/CPOpt-v1.0).