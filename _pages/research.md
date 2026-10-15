---
layout: page
title: Research
permalink: /research/
description: Fatigue assessment, welded structures, additive manufacturing and component testing at the University of Pisa.
nav: true
nav_order: 1
---

I study how materials and components respond to repeated loads, combining analytical models, finite element analysis and experiments. Explore the areas below, then follow the linked studies for technical detail.

<div class="research-areas">
{% for area in site.data.research_areas %}
<section class="research-area" aria-labelledby="{{ area.id }}">
  <h2 id="{{ area.id }}">{{ area.title }}</h2>
  <p class="research-summary">{{ area.summary }}</p>
  <p class="research-methods"><strong>Methods:</strong> {{ area.methods }}</p>
  <ul class="inline-links" aria-label="Related outputs for {{ area.title }}">{% for link in area.links %}<li><a href="{{ link.url | relative_url }}">{{ link.label }}</a></li>{% endfor %}</ul>
  <details class="context-details"><summary>Further studies and technical context</summary><ul>{% for link in area.further %}<li><a href="{{ link.url | relative_url }}">{{ link.label }}</a></li>{% endfor %}</ul></details>
</section>
{% endfor %}
</div>

<section id="projects" aria-labelledby="selected-collaborative-projects">
  <h2 id="selected-collaborative-projects">Research projects</h2>
  <div class="project-list">{% assign project = site.data.resume.projects.first %}{% include research_project.html project=project %}</div>
  <details class="context-details previous-projects"><summary>Previous projects</summary><div class="project-list">{% for project in site.data.resume.projects offset:1 %}{% include research_project.html project=project %}{% endfor %}</div></details>
</section>

<h2 id="international-collaborations">International collaborations</h2>
<p>The FABER WG3 responsibility above is separate from the <a href="{{ '/repositories/' | relative_url }}#multiaxial-fatigue">WG4.3 multiaxial fatigue software and review activity</a>. Research exchanges also connect my work with European universities and research institutes.</p>
<details class="context-details"><summary>Research visits</summary><p>Czech Technical University in Prague (FABER WG6, June 2026); Aarhus University (Circle U., January 2026); NTNU (Erasmus+, July 2024); Fraunhofer LBF (doctoral research, February–June 2021).</p></details>

<h2 id="research-environment">Research environment</h2>
<p>I work in the machine design group at the <a href="https://www.dici.unipi.it/">Department of Civil and Industrial Engineering</a>, <a href="https://www.unipi.it/">University of Pisa</a>. For shared research questions, methodological work or industrial challenges, <a href="mailto:andrea.chiocca@unipi.it">contact me</a>.</p>
