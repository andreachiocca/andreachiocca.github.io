---
lang: en
translation_key: teaching
layout: page
permalink: /teaching/
title: Teaching
description: University of Pisa courses, public teaching materials and thesis opportunities in computational and experimental mechanics. Public course materials are in Italian.
nav: true
nav_order: 4
---

Find your course below for slides, notes, exercises and tutorials. These resources complement the [official course catalogue](https://unipi.coursecatalogue.cineca.it/) and [Engineering e-learning platform](https://elearn.ing.unipi.it/).

<section class="collaboration-panel" aria-labelledby="teaching-thesis-title"><h2 id="teaching-thesis-title"><i class="far fa-lightbulb section-icon" aria-hidden="true"></i>Looking for a thesis topic?</h2><p>Explore five research directions, from welded structures and multiaxial fatigue to polymers, PCB reliability and prospective AI applications. Choose numerical, experimental or combined work and discuss possibilities in Pisa or abroad.</p><a class="contact-link" href="{{ '/thesis/' | local_url | relative_url }}">Explore thesis opportunities <span aria-hidden="true">→</span></a></section>

## Recent teaching

The latest documented teaching periods extend through 2026; current academic-year details are available through the university platforms.

{% assign courses = site.projects | sort: 'importance' %}
{% for group in (1..2) %}
{% if group == 2 %}<h2>Previous teaching</h2>{% endif %}
<div class="course-list">
{% for course in courses %}
{% if group == 1 and course.teaching_group != 'recent' %}{% continue %}{% endif %}
{% if group == 2 and course.teaching_group != 'previous' %}{% continue %}{% endif %}
{% assign materials = site.data.teaching_materials[course.materials_key] %}
<section class="course-summary">
  <h3><a href="{{ course.url | local_url | relative_url }}">{{ course.title }}</a></h3>
  <p class="course-programme">{{ course.description }} · University of Pisa</p>
  <p>{{ course.teaching_period }} · {{ course.teaching_role }}.</p>
  {% if materials.size > 0 %}<a class="course-material-link" href="{{ course.url | local_url | relative_url }}">View course materials</a>{% else %}<p class="course-availability">No public materials listed.</p>{% endif %}
</section>
{% endfor %}
</div>
{% endfor %}

## Supervision and research mentoring

I have supervised or co-supervised master's theses on welded joints, polymer composites, hybrid SPR joints, additively manufactured aluminium structures, elastomers and automotive PCB assemblies. In August–October 2026, I also mentor a FABER short-term scientific mission involving the National Engineering School of Monastir (ENIM).

For materials, thesis topics or project questions, [contact me by email](mailto:andrea.chiocca@unipi.it).
