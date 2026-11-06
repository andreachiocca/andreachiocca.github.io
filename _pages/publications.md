---
lang: en
translation_key: publications
layout: page
permalink: /publications/
title: Publications
description: Journal articles, conference papers and PhD thesis by Andrea Chiocca on multiaxial fatigue, welded joints and residual stresses.
seo_title: Fatigue & Structural Integrity Publications
nav: true
nav_order: 2
---

<div class="publications-index">
<div class="publications-index-intro" markdown="1">
{% locale publications.intro %}[Research software, datasets and benchmark packages]({{ '/repositories/' | local_url | relative_url }}) linked to these papers have their own catalogue.{% endlocale %}
</div>

{% include bib_search.liquid %}

<div class="publications" id="publication-list">
<section aria-labelledby="journal-articles" data-publication-category="article">
<h2 id="journal-articles">{{ "Journal articles" | t }}</h2>
{% bibliography --query @article %}
</section>
<section aria-labelledby="conference-contributions" data-publication-category="inproceedings">
<h2 id="conference-contributions">{{ "Conference contributions" | t }}</h2>
{% bibliography --query @inproceedings %}
</section>
<section aria-labelledby="doctoral-thesis" data-publication-category="phdthesis">
<h2 id="doctoral-thesis">{{ "Doctoral thesis" | t }}</h2>
{% bibliography --query @phdthesis %}
</section>
</div>

{% locale publications.dataset %}<p id="Moda2022a">The Rosenthal-solution dataset is listed under <a href="{{ '/repositories/' | local_url | relative_url }}#Moda2022a">research outputs</a>.</p>{% endlocale %}
</div>
