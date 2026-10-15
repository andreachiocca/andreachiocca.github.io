---
layout: page
permalink: /teaching/
title: Teaching
description: Course materials for finite element analysis and machine design. Teaching resources are provided in Italian.
nav: true
nav_order: 4
---

Course resources cover finite element analysis, mechanical design, and computer-aided engineering. Materials are in Italian. The list describes the resources available here; it does not imply that every course is currently being taught.

{% assign courses = site.projects | sort: "importance" %}
{% for course in courses %}
## [{{ course.title }}]({{ course.url | relative_url }})

{{ course.description }}

{% if course.importance == 3 %}
Teaching materials are being prepared.
{% else %}
[View course materials]({{ course.url | relative_url }}).
{% endif %}
{% endfor %}

For questions about these materials or thesis enquiries, [contact me by email](mailto:andrea.chiocca@unipi.it).
