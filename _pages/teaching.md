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

<section class="teaching-editorial teaching-editorial-hero" aria-labelledby="teaching-editorial-title">
<p class="editorial-index">01 / {{ 'Teaching at the University of Pisa' | t }}</p>
<h2 id="teaching-editorial-title">{{ 'Courses and teaching materials' | t }}</h2>
{% capture teaching_intro %}{% locale teaching.intro %}Find your course below for slides, notes, exercises and tutorials. These resources complement the [official course catalogue](https://unipi.coursecatalogue.cineca.it/) and [Engineering e-learning platform](https://elearn.ing.unipi.it/).{% endlocale %}{% endcapture %}
<div class="teaching-editorial-description">{{ teaching_intro | strip | markdownify }}</div>
<nav class="teaching-editorial-links" aria-label="{{ 'Teaching resources' | t }}">
<a href="#recent-teaching">{{ 'Browse teaching materials' | t }} <span aria-hidden="true">↓</span></a>
<a href="{{ '/thesis/' | local_url | relative_url }}#specific-projects">{{ 'See available thesis projects' | t }} <span aria-hidden="true">↗</span></a>
</nav>
</section>

<section class="collaboration-panel teaching-editorial" aria-labelledby="teaching-thesis-title"><h2 id="teaching-thesis-title"><i class="far fa-lightbulb section-icon" aria-hidden="true"></i>{{ "Looking for a thesis topic?" | t }}</h2>{% locale teaching.thesis %}<p>Two specific thesis projects are available for discussion, covering open-source implementation of multiaxial fatigue methods and vibration testing of capacitor assemblies. Other research directions remain open for exploration.</p>{% endlocale %}<a class="contact-link" href="{{ '/thesis/' | local_url | relative_url }}">{{ "Explore thesis opportunities" | t }} <span aria-hidden="true">→</span></a></section>

<h2 id="recent-teaching">{{ "Recent teaching" | t }}</h2>

{% locale teaching.periods %}Teaching continues in the 2026/27 academic year with the same courses and roles as the preceding year. For current requirements and schedules, consult the official university platforms.{% endlocale %}

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

{% locale teaching.supervision %}I have supervised or co-supervised master's theses on welded joints, polymer composites, hybrid SPR joints, additively manufactured aluminium structures, elastomers and automotive PCB assemblies. In August–October 2026, I also mentor a FABER short-term scientific mission involving the National Engineering School of Monastir (ENIM).{% endlocale %}

{% locale teaching.contact %}For materials, thesis topics or project questions, [contact me by email](mailto:andrea.chiocca@unipi.it).{% endlocale %}

