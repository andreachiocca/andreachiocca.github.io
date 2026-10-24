---
lang: en
translation_key: repositories
layout: page
permalink: /repositories/
title: Repositories & Research Outputs
nav_title: Repositories
description: Scientific software, engineering tools, fatigue benchmarks and archived research data by Andrea Chiocca.
nav: true
nav_order: 3.5
catalogue: true
---

<div class="output-catalogue output-atlas">
  {% assign software_outputs = site.data.research_outputs | where: 'kind', 'software' %}
  {% assign benchmark_outputs = site.data.research_outputs | where: 'kind', 'benchmark' %}
  {% assign data_outputs = site.data.research_outputs | where: 'kind', 'data' %}
  {% assign dataset_total = benchmark_outputs.size | plus: data_outputs.size %}
  <section class="output-atlas-hero" aria-label="{{ 'Catalogue overview' | t }}">
    <div class="output-atlas-intro">
      <p class="output-atlas-index">01 / {{ 'Scientific software and research data' | t }}</p>
      {% locale repositories.intro %}<p>Code and data supporting my <a href="{{ '/research/' | local_url | relative_url }}">research</a> and <a href="{{ '/publications/' | local_url | relative_url }}">publications</a>. Forks retain upstream attribution.</p>{% endlocale %}
      <nav class="output-atlas-jump" aria-label="{{ 'Explore resources' | t }}">
        <a href="#selected-outputs">{{ 'Jump to selected outputs' | t }} <span aria-hidden="true">↘</span></a>
        <a href="#complete-catalogue">{{ 'Jump to full catalogue' | t }} <span aria-hidden="true">↓</span></a>
      </nav>
    </div>
    <dl class="output-atlas-numbers">
      <div><dt>{{ 'Research outputs' | t }}</dt><dd>{{ site.data.research_outputs.size }}</dd></div>
      <div><dt>{{ 'Software projects' | t }}</dt><dd>{{ software_outputs.size }}</dd></div>
      <div><dt>{{ 'Datasets and benchmarks' | t }}</dt><dd>{{ dataset_total }}</dd></div>
    </dl>
  </section>
  <section class="output-atlas-selected" id="selected-outputs" aria-labelledby="selected-outputs-title">
    <p class="output-atlas-index">02 / {{ 'Selected research' | t }}</p>
    <h2 id="selected-outputs-title">{{ 'Selected outputs' | t }}</h2>
    <div class="output-atlas-featured-grid">
      {% for spotlight_id in site.data.research_output_spotlight %}
        {% assign canonical_feature = site.data.research_outputs | where: 'id', spotlight_id | first %}
        {% if canonical_feature %}
          {% assign feature = canonical_feature | localized_record: 'outputs' %}
          <article class="output-atlas-feature" data-spotlight-id="{{ canonical_feature.id | escape }}">
            <p class="output-atlas-feature-kind">{{ feature.type_label | t | escape }} / {{ feature.source | escape }}</p>
            <h3><a href="#{{ canonical_feature.id | escape }}">{{ feature.display_title | default: feature.title | escape }}</a></h3>
            <p class="output-atlas-feature-description">{{ feature.description | truncatewords: 28 | escape }}</p>
            <a class="output-atlas-feature-link" href="#{{ canonical_feature.id | escape }}">{{ 'View in catalogue' | t }} <span aria-hidden="true">↗</span></a>
          </article>
        {% endif %}
      {% endfor %}
    </div>
  </section>
  <section class="output-atlas-full" id="complete-catalogue" aria-labelledby="complete-catalogue-title">
    <p class="output-atlas-index">03 / {{ 'Research outputs' | t }}</p>
    <h2 id="complete-catalogue-title">{{ 'Complete catalogue' | t }}</h2>
    {% locale repositories.coverage %}<p class="catalogue-coverage">{{ site.data.catalogue_status.github_repositories_included }} GitHub repositories · {{ site.data.catalogue_status.zenodo_resources }} Zenodo resources · 1 additional dataset</p>{% endlocale %}
    <div class="output-atlas-search" hidden>
      <label for="output-search">{{ 'Search by title, method, material or DOI' | t }}</label>
      <input id="output-search" type="search" autocomplete="off" aria-controls="output-grid" placeholder="{{ 'e.g. fatigue, ECP, Zenodo' | t }}" hidden>
    </div>
    <div class="catalogue-filters" role="group" aria-label="{{ 'Filter research outputs' | t }}" hidden>
      <button type="button" data-filter="all" aria-pressed="true" aria-controls="output-grid">{{ 'All' | t }}</button>
      <button type="button" data-filter="software" aria-pressed="false" aria-controls="output-grid">{{ 'Software' | t }}</button>
      <button type="button" data-filter="data" aria-pressed="false" aria-controls="output-grid" aria-label="{{ 'Datasets and benchmarks' | t }}">{{ 'Datasets' | t }}</button>
      <button type="button" data-filter="other" aria-pressed="false" aria-controls="output-grid">{{ 'Other outputs' | t }}</button>
    </div>
    <p id="output-count" class="catalogue-count" data-count-template="{{ '%visible% of %total% resources shown.' | t }}" role="status" aria-live="polite" aria-atomic="true">{{ site.data.research_outputs.size }} {{ 'resources · Selected research first.' | t }}</p>
    <p id="output-empty" class="output-atlas-empty" hidden>{{ 'No research outputs match the selected filters.' | t }}</p>
    <button type="button" id="output-reset" class="output-atlas-reset" hidden>{{ 'Clear catalogue filters' | t }}</button>
    <div id="output-grid" class="output-grid">
      {% for canonical_output in site.data.research_outputs %}{% include research_output.html output=canonical_output %}{% endfor %}
    </div>
    {% locale repositories.snapshot %}<p class="catalogue-footnote">Catalogue snapshot verified {{ site.data.catalogue_status.verified_on | date: '%-d %B %Y' }}. Records link to original sources. Version history and access conditions are available under “Record details”. Code-update dates do not indicate scientific validation.</p>{% endlocale %}
  </section>
</div>
<script defer src="{{ '/assets/js/research_outputs.js' | local_url | relative_url | bust_file_cache }}"></script>
