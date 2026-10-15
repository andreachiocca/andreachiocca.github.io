---
layout: page
permalink: /teaching/
title: Teaching
description: University of Pisa courses, lecture materials, exercises and supplementary technical reading. Public materials are in Italian.
nav: true
nav_order: 4
---

Find your course below for slides, notes, exercises and tutorials. These resources complement the [official course catalogue](https://unipi.coursecatalogue.cineca.it/) and [Engineering e-learning platform](https://elearn.ing.unipi.it/).

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
  <h3><a href="{{ course.url | relative_url }}">{{ course.title }}</a></h3>
  <p class="course-programme">{{ course.description }} · University of Pisa</p>
  <p>{{ course.teaching_period }} · {{ course.teaching_role }}.</p>
  {% if materials.size > 0 %}<a class="course-material-link" href="{{ course.url | relative_url }}">View course materials</a>{% else %}<p class="course-availability">No public materials listed.</p>{% endif %}
</section>
{% endfor %}
</div>
{% endfor %}

## Supplementary technical reading

My research notes explain critical plane fatigue methods and may be useful for related projects or theses. They supplement the course material above.

<ul class="reading-list">{% for note in site.posts %}<li><a href="{{ note.url | relative_url }}">{{ note.short_title | default: note.title }}</a></li>{% endfor %}</ul>

## Supervision and research mentoring

I have supervised or co-supervised master's theses on welded joints, polymer composites, hybrid SPR joints, additively manufactured aluminium structures, elastomers and automotive PCB assemblies. In August–October 2026, I also mentor a FABER short-term scientific mission involving the National Engineering School of Monastir (ENIM).

For materials, thesis topics or project questions, [contact me by email](mailto:andrea.chiocca@unipi.it).
