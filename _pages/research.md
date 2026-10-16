---
lang: en
translation_key: research
layout: page
title: Research
permalink: /research/
description: Fatigue assessment, welded structures, additive manufacturing and component testing at the University of Pisa.
nav: true
nav_order: 1
---

{% locale research.intro %}I study how materials and components respond to repeated loads, combining analytical models, finite element analysis and experiments. Explore the areas below, then follow the linked studies for technical detail.{% endlocale %}

<div class="research-areas">
{% for canonical_area in site.data.research_areas %}{% assign area = canonical_area | localized_record: 'research_areas' %}
<section class="research-area" aria-labelledby="{{ area.id }}">
  <h2 id="{{ area.id }}"><i class="far {{ area.icon }} section-icon" aria-hidden="true"></i>{{ area.title }}</h2>
  <p class="research-summary">{{ area.summary }}</p>
  <p class="research-methods"><strong>{{ "Methods" | t }}</strong> {{ area.methods }}</p>
  <ul class="inline-links" aria-label="{{ 'Related outputs for' | t }} {{ area.title }}">{% for link in area.links %}<li><a href="{{ link.url | local_url | relative_url }}">{{ link.label | t }}</a></li>{% endfor %}</ul>
  <details class="context-details"><summary>{{ "Further studies and technical context" | t }}</summary><ul>{% for link in area.further %}<li><a href="{{ link.url | local_url | relative_url }}">{{ link.label | t }}</a></li>{% endfor %}</ul></details>
</section>
{% endfor %}
</div>

<section id="projects" aria-labelledby="selected-collaborative-projects">
  <h2 id="selected-collaborative-projects">{{ "Research projects" | t }}</h2>
  <div class="project-list">{% assign project = site.data.resume.projects.first %}{% include research_project.html project=project %}</div>
  <details class="context-details previous-projects"><summary>{{ "Previous projects" | t }}</summary><div class="project-list">{% for project in site.data.resume.projects offset:1 %}{% include research_project.html project=project %}{% endfor %}</div></details>
</section>

<h2 id="international-collaborations"><i class="far fa-handshake section-icon" aria-hidden="true"></i>{{ "International collaborations" | t }}</h2>
{% locale research.exchanges %}<p>Research exchanges connect my work with European universities and research institutes. My current FABER responsibilities are listed under <a href="#projects">research projects</a>.</p>{% endlocale %}
{% locale research.visits %}<details class="context-details"><summary>{{ "Research visits" | t }}</summary><p>Czech Technical University in Prague (FABER WG6, June 2026); Aarhus University (Circle U., January 2026); NTNU (Erasmus+, July 2024); Fraunhofer LBF (doctoral research, February–June 2021).</p></details>{% endlocale %}

<ul class="inline-links"><li><a href="{{ '/laboratory/' | local_url | relative_url }}">{{ "Laboratory and experimental capabilities" | t }}</a></li><li><a href="{{ '/thesis/' | local_url | relative_url }}">{{ "Thesis opportunities for students" | t }}</a></li></ul>

<h2 id="research-environment">{{ "Research environment" | t }}</h2>
{% locale research.environment %}<p>I work in the machine design group at the <a href="https://www.dici.unipi.it/">Department of Civil and Industrial Engineering</a>, <a href="https://www.unipi.it/">University of Pisa</a>. For shared research questions, methodological work or industrial challenges, <a href="mailto:andrea.chiocca@unipi.it">contact me</a>.</p>{% endlocale %}
