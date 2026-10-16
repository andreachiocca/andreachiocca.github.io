---
lang: en
translation_key: publications
layout: page
permalink: /publications/
title: Publications
description: Journal articles, conference contributions and doctoral thesis by Andrea Chiocca, grouped by type and year, newest first.
nav: true
nav_order: 2
---

Journal articles, conference contributions and my doctoral thesis are listed separately below. [Research software, datasets and benchmark packages]({{ '/repositories/' | local_url | relative_url }}) have their own catalogue.

{% include bib_search.liquid %}

<div class="publications" id="publication-list">
<section aria-labelledby="journal-articles">
<h2 id="journal-articles">Journal articles</h2>
{% bibliography --query @article %}
</section>
<section aria-labelledby="conference-contributions">
<h2 id="conference-contributions">Conference contributions</h2>
{% bibliography --query @inproceedings %}
</section>
<section aria-labelledby="doctoral-thesis">
<h2 id="doctoral-thesis">Doctoral thesis</h2>
{% bibliography --query @phdthesis %}
</section>
</div>

<p id="Moda2022a">The Rosenthal-solution dataset is listed under <a href="{{ '/repositories/' | local_url | relative_url }}#Moda2022a">research outputs</a>.</p>
