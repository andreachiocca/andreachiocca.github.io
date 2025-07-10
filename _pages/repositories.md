---
layout: page
permalink: /repositories/
title: repositories
description: In the following some of my GitHub and Zenodo repositories containing some projects and data collected over time.
nav: false
nav_order: 3
---

{% if site.data.repositories.github_repos %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=repo %}
  {% endfor %}
</div>
{% endif %}

{% if site.data.repositories.zenodo_repos %}
<h2 class="mt-5">Zenodo records</h2>
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for record in site.data.repositories.zenodo_repos %}
    {% include repository/zenodo.html record=record %}
  {% endfor %}
</div>
{% endif %}