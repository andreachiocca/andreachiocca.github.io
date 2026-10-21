---
lang: en
translation_key: research
layout: research_atlas
title: Research
permalink: /research/
description: Fatigue assessment, welded structures, additive manufacturing and component testing at the University of Pisa.
nav: true
nav_order: 1
---

<div id="research-areas" class="research-areas">
{% for canonical_area in site.data.research_areas %}{% assign area = canonical_area | localized_record: 'research_areas' %}
{% include research_area_panel.html area=area canonical_id=canonical_area.id ordinal=forloop.index %}
{% endfor %}
</div>

<section id="projects" aria-labelledby="selected-collaborative-projects">
  <h2 id="selected-collaborative-projects">{{ "Research projects" | t }}</h2>
  <div class="project-list">{% assign project = site.data.resume.projects.first %}{% include research_project.html project=project %}</div>
  <details class="context-details previous-projects"><summary>{{ "Previous projects" | t }}</summary><div class="project-list">{% for canonical_project in site.data.resume.projects offset:1 %}{% include research_project.html project=canonical_project %}{% endfor %}</div></details>
</section>

<h2 id="international-collaborations"><i class="far fa-handshake section-icon" aria-hidden="true"></i>{{ "International collaborations" | t }}</h2>
{% include international_experiences.html %}

<ul class="inline-links"><li><a href="{{ '/laboratory/' | local_url | relative_url }}">{{ "Laboratory and experimental capabilities" | t }}</a></li><li><a href="{{ '/thesis/' | local_url | relative_url }}">{{ "Thesis opportunities for students" | t }}</a></li></ul>

<h2 id="research-environment">{{ "Research collaborations" | t }}</h2>
{% locale research.contact %}<p>For potential academic or industrial research collaborations, <a href="mailto:andrea.chiocca@unipi.it">contact me</a>.</p>{% endlocale %}
