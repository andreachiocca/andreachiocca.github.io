---
layout: page
permalink: /repositories/
title: Repositories & Research Outputs
nav_title: Outputs
description: Scientific software, engineering tools, fatigue benchmarks and archived research data by Andrea Chiocca.
nav: true
nav_order: 3.5
catalogue: true
---

<div class="output-catalogue">
  <p>Explore the software and data supporting my <a href="{{ '/research/' | relative_url }}">research</a> and <a href="{{ '/publications/' | relative_url }}">publications</a>, alongside engineering and academic tools. Forks are labelled and link to their upstream projects.</p>
  <p class="catalogue-coverage">{{ site.data.catalogue_status.github_repositories }} GitHub repositories · {{ site.data.catalogue_status.zenodo_resources }} Zenodo resources · 1 additional dataset</p>
  <div class="catalogue-filters" role="group" aria-label="Filter research outputs" hidden>
    <button type="button" data-filter="all" aria-pressed="true" aria-controls="output-grid">All</button>
    <button type="button" data-filter="software" aria-pressed="false" aria-controls="output-grid">Software</button>
    <button type="button" data-filter="data" aria-pressed="false" aria-controls="output-grid">Datasets & benchmarks</button>
    <button type="button" data-filter="other" aria-pressed="false" aria-controls="output-grid">Other outputs</button>
  </div>
  <p id="output-count" class="catalogue-count" role="status" aria-live="polite" aria-atomic="true">{{ site.data.research_outputs.size }} resources. Selected research activities first, then latest commit or publication date.</p>
  <div id="output-grid" class="output-grid">
    {% for output in site.data.research_outputs %}{% include research_output.html %}{% endfor %}
  </div>
  <p class="catalogue-footnote">Snapshot verified {{ site.data.catalogue_status.verified_on | date: '%-d %B %Y' }}. All public repositories from <a href="https://github.com/achiocca1">achiocca1</a> and <a href="https://github.com/andreachiocca">andreachiocca</a> are included. The {{ site.data.catalogue_status.zenodo_records }} verified Zenodo records are grouped into {{ site.data.catalogue_status.zenodo_resources }} resources; earlier versions remain accessible under “Record details”. Commit dates indicate code history, not scientific validation or maintenance commitments.</p>
</div>
<script defer src="{{ '/assets/js/research_outputs.js' | relative_url | bust_file_cache }}"></script>
