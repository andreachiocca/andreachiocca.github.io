---
layout: page
title: project 1
description: Teaching materials for the course "PROGETTAZIONE MECCANICA COL METODO DEGLI ELEMENTI FINITI"
img: assets/img/12.jpg
importance: 1
category: Energy Engineering (LM-30)
MAT_1: Prova.pdf
TMAT_1 : Introduzione al Metodo degli Elementi Finiti
---

<header class="post-header">
  <h1 class="post-title">{{ page.TMAT_1 }} {% if page.MAT_1 %}<a href="{{ page.MAT_1 | prepend: 'assets/pdf/' | relative_url}}" target="_blank" rel="noopener noreferrer" class="float-right"><i class="fas fa-file-pdf"></i></a>{% endif %}</h1>
    {% if page.description %}<p class="post-description"></p>{% endif %}
</header>
