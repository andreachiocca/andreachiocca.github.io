---
lang: en
translation_key: publications
layout: publications_atlas
permalink: /publications/
title: Publications
description: Journal articles, conference contributions and doctoral thesis by Andrea Chiocca, grouped by type and year, newest first.
nav: true
nav_order: 2
---

{% include bib_search.liquid %}

<div class="publications" id="publication-list">
<section class="publication-section" data-publication-type="article" aria-labelledby="journal-articles">
<h2 id="journal-articles"><span aria-hidden="true">01 / </span>{{ "Journal articles" | t }}</h2>
{% bibliography --query @article %}
</section>
<section class="publication-section" data-publication-type="inproceedings" aria-labelledby="conference-contributions">
<h2 id="conference-contributions"><span aria-hidden="true">02 / </span>{{ "Conference contributions" | t }}</h2>
{% bibliography --query @inproceedings %}
</section>
<section class="publication-section" data-publication-type="phdthesis" aria-labelledby="doctoral-thesis">
<h2 id="doctoral-thesis"><span aria-hidden="true">03 / </span>{{ "Doctoral thesis" | t }}</h2>
{% bibliography --query @phdthesis %}
</section>
</div>

<div class="publication-note">
{% locale publications.dataset %}<p id="Moda2022a">The Rosenthal-solution dataset is listed under <a href="{{ '/repositories/' | local_url | relative_url }}#Moda2022a">research outputs</a>.</p>{% endlocale %}
</div>
