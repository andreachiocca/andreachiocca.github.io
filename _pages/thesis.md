---
lang: en
translation_key: thesis
layout: page
title: Thesis Opportunities
permalink: /thesis/
description: Explore thesis directions in computational mechanics, experimental testing, fatigue and structural integrity at the University of Pisa and with potential research contacts abroad.
section: teaching
---

{% locale thesis.intro %}Interested in understanding why materials and structures fail and how to improve predictions? Bachelor’s and master’s students in mechanical engineering and related disciplines can discuss a thesis combining **mechanics, simulations, programming or laboratory work**.{% endlocale %}

{% locale thesis.scope %}These are research directions to develop together, rather than a list of current vacancies. The topic and scope will reflect your background, interests and the available projects.{% endlocale %}

<ul class="inline-links page-paths"><li><a href="#research-directions">{{ "Research topics" | t }}</a></li><li><a href="#ways-of-working">{{ "Ways of working" | t }}</a></li><li><a href="#italy-and-abroad">{{ "Italy and abroad" | t }}</a></li><li><a href="#discuss-a-thesis">{{ "Discuss a thesis" | t }}</a></li></ul>

<h2 id="research-directions">{{ "Explore a research direction" | t }}</h2>
<div class="feature-grid thesis-topics">{% for canonical_resource in site.data.thesis_opportunities.directions %}{% include resource_card.html resource=canonical_resource group="thesis" kind="thesis-topic" %}{% endfor %}</div>

<h2 id="ways-of-working">{{ "Choose how you work" | t }}</h2>
{% locale thesis.approaches %}<p>You can focus on computation, experiments, or their combination. The activity labels above are starting points; we will agree a feasible approach for your thesis.</p>{% endlocale %}
<div class="approach-list">{% for canonical_approach in site.data.thesis_opportunities.approaches %}{% assign approach = canonical_approach | localized_record: 'thesis' %}<section class="approach"><h3>{{ approach.title }}</h3><p>{{ approach.description }}</p></section>{% endfor %}</div>
<ul class="inline-links"><li><a href="{{ '/laboratory/' | local_url | relative_url }}">{{ "Explore experimental capabilities" | t }}</a></li><li><a href="{{ '/teaching/' | local_url | relative_url }}">{{ "Courses and materials" | t }}</a></li></ul>

{% if site.data.thesis_opportunities.projects.size > 0 %}
<h2 id="specific-projects">{{ "Specific thesis projects" | t }}</h2>
<div class="feature-grid">{% for canonical_resource in site.data.thesis_opportunities.projects %}{% include resource_card.html resource=canonical_resource group="thesis" kind="thesis-project" %}{% endfor %}</div>
{% endif %}

<section class="opportunity-context" aria-labelledby="italy-and-abroad">
  <h2 id="italy-and-abroad">{{ "Thesis activities in Italy and abroad" | t }}</h2>
  {% locale thesis.italy %}<p>Projects may be developed within the <a href="https://www.dici.unipi.it/">Department of Civil and Industrial Engineering, University of Pisa</a>, with local industrial companies, or by exploring collaboration with international research institutions.</p>{% endlocale %}
  {% locale thesis.abroad %}<p>Previous research exchanges provide contacts for discussing fatigue, structural integrity, computational and experimental mechanics, and potentially AI-supported modelling. Research environments to explore include:</p>{% endlocale %}
  <ul class="institution-list">{% for institution in site.data.thesis_opportunities.international_contacts %}<li><a href="{{ institution.url }}">{{ institution.name }}</a><span>{{ institution.location | t }}{% if institution.detail %} · {{ institution.detail }}{% endif %}</span></li>{% endfor %}</ul>
  {% locale thesis.conditions %}<p class="scope-note">These contacts do not imply permanently open or guaranteed placements. Any international thesis depends on project availability, agreement of potential supervisors, host-institution acceptance, academic requirements, and funding and mobility arrangements where relevant.</p>{% endlocale %}
</section>

<section id="discuss-a-thesis" class="collaboration-panel" aria-labelledby="thesis-contact-title"><h2 id="thesis-contact-title">{{ "Interested in one of these topics?" | t }}</h2>{% locale thesis.contact %}<p>Tell me about your degree programme, research interests, background, preferred type of work and possible timeframe. We can discuss suitable projects and whether work in Pisa or abroad is feasible.</p>{% endlocale %}<a class="contact-link" href="mailto:andrea.chiocca@unipi.it?subject=Thesis%20Opportunity%20Research%20Interest">andrea.chiocca@unipi.it</a></section>
