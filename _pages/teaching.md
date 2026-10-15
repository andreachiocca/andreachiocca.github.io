---
layout: page
permalink: /teaching/
title: Teaching
description: Course materials for finite element analysis and machine design. Teaching resources are provided in Italian.
nav: true
nav_order: 4
---

Course resources cover finite element analysis, mechanical design, and computer-aided engineering. Materials are in Italian. The periods below follow my academic CV; a period ending in 2026 does not imply a continuing appointment beyond that year.

{% assign courses = site.projects | sort: "importance" %}
{% for course in courses %}
## [{{ course.title }}]({{ course.url | relative_url }})

{{ course.description }}

**{{ course.teaching_period }}** · {{ course.teaching_role }}.

{% if course.importance == 3 %}
Teaching materials are being prepared.
{% else %}
[View course materials]({{ course.url | relative_url }}).
{% endif %}
{% endfor %}

## Supervision and research mentoring

I have supervised or co-supervised master's theses on welded joints, polymer composites, hybrid SPR joints, additively manufactured aluminium structures, elastomers and automotive PCB assemblies. In August–October 2026, I also mentor a FABER short-term scientific mission involving the National Engineering School of Monastir (ENIM).

For questions about these materials or thesis enquiries, [contact me by email](mailto:andrea.chiocca@unipi.it).
