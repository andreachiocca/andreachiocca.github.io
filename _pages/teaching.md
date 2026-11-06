---
lang: en
translation_key: teaching
layout: page
permalink: /teaching/
title: Teaching
description: Courses at the University of Pisa on machine design and finite element methods, with public teaching materials (in Italian).
seo_title: Machine Design Courses & Teaching Materials
nav: true
nav_order: 4
---

<section class="teaching-editorial teaching-editorial-hero" aria-labelledby="teaching-editorial-title">
<p class="editorial-index">01 / {{ 'Teaching at the University of Pisa' | t }}</p>
<h2 id="teaching-editorial-title">{{ 'Courses and teaching materials' | t }}</h2>
{% capture teaching_intro %}{% locale teaching.intro %}Slides, notes, exercises and tutorials for each course. See also the [official course catalogue](https://unipi.coursecatalogue.cineca.it/) and the [Engineering e-learning platform](https://elearn.ing.unipi.it/).{% endlocale %}{% endcapture %}
<div class="teaching-editorial-description">{{ teaching_intro | strip | markdownify }}</div>
<nav class="teaching-editorial-links" aria-label="{{ 'Teaching resources' | t }}">
<a href="#recent-teaching">{{ 'Browse teaching materials' | t }} <span aria-hidden="true">↓</span></a>
<a href="{{ '/thesis/' | local_url | relative_url }}#specific-projects">{{ 'See available thesis projects' | t }} <span aria-hidden="true">↗</span></a>
</nav>
</section>

<section class="collaboration-panel teaching-editorial" aria-labelledby="teaching-thesis-title"><h2 id="teaching-thesis-title"><i class="far fa-lightbulb section-icon" aria-hidden="true"></i>{{ "Looking for a thesis topic?" | t }}</h2>{% locale teaching.thesis %}<p>Three thesis projects: open-source multiaxial fatigue methods, vibration testing of capacitors on circuit boards, and fatigue of coated lattice structures.</p>{% endlocale %}<a class="contact-link" href="{{ '/thesis/' | local_url | relative_url }}">{{ "Explore thesis opportunities" | t }} <span aria-hidden="true">→</span></a></section>

<h2 id="recent-teaching">{{ "Recent teaching" | t }}</h2>

{% locale teaching.periods %}Same courses and roles in 2026/27. Check the official university platforms for schedules and requirements.{% endlocale %}

{% assign courses = site.projects | sort: 'importance' %}
{% for group in (1..2) %}
{% if group == 2 %}<h2>{{ "Previous teaching" | t }}</h2>{% endif %}
<div class="course-list teaching-editorial teaching-editorial-course-grid">
{% for course in courses %}
{% if group == 1 and course.teaching_group != 'recent' %}{% continue %}{% endif %}
{% if group == 2 and course.teaching_group != 'previous' %}{% continue %}{% endif %}
{% assign materials = site.data.teaching_materials[course.materials_key] %}
<section class="course-summary">
  <h3><a href="{{ course.url | local_url | relative_url }}">{{ course.title }}</a></h3>
  <p class="course-programme">{{ course.description }} · {{ "University of Pisa" | institution_display }}</p>
  <p>{{ course.teaching_period }} · {{ course.teaching_role | t }}.</p>
  {% if materials.size > 0 %}<a class="course-material-link" href="{{ course.url | local_url | relative_url }}">{{ "View course materials" | t }}</a>{% else %}<p class="course-availability">{{ "No public materials listed." | t }}</p>{% endif %}
</section>
{% endfor %}
</div>
{% endfor %}

## {{ "Supervision and research mentoring" | t }}

{% locale teaching.supervision %}Master’s theses supervised or co-supervised on welded joints, polymer composites, hybrid SPR joints, additively manufactured aluminium, elastomers and automotive PCB assemblies. August–October 2026: mentor of a FABER short-term scientific mission with the National Engineering School of Monastir (ENIM).{% endlocale %}

{% locale teaching.contact %}Questions on materials, theses or projects: [email me](mailto:andrea.chiocca@unipi.it).{% endlocale %}

