---
lang: en
translation_key: thesis
layout: page
title: Thesis Opportunities
permalink: /thesis/
description: Explore thesis directions in computational mechanics, experimental testing, fatigue and structural integrity at the University of Pisa and with potential research contacts abroad.
section: teaching
---

<section class="thesis-editorial thesis-editorial-banner">
<div class="thesis-editorial-banner-copy">
<p class="editorial-index">01 / {{ 'Thesis topics and projects' | t }}</p>
<h2>{{ 'Research-led thesis opportunities' | t }}</h2>
{% capture thesis_intro %}{% locale thesis.intro %}Bachelor’s and master’s students in mechanical engineering and related fields can work on why materials and structures fail and how to predict it, through **mechanics, simulation, programming or laboratory work**.{% endlocale %}

{% locale thesis.scope %}Three computational and experimental thesis projects are available, plus open research directions. We agree the objectives together, based on your background and interests.{% endlocale %}{% endcapture %}
<div class="thesis-editorial-banner-text">{{ thesis_intro | strip | markdownify }}</div>
<a href="#specific-projects">{{ 'See available thesis projects' | t }} <span aria-hidden="true">↗</span></a>
</div>
<div class="thesis-editorial-banner-illustration">{% include damage_sphere.html %}</div>
</section>

<ul class="inline-links page-paths"><li><a href="#specific-projects">{{ "Specific thesis projects" | t }}</a></li><li><a href="#research-directions">{{ "Research topics" | t }}</a></li><li><a href="#ways-of-working">{{ "Ways of working" | t }}</a></li><li><a href="#italy-and-abroad">{{ "Italy and abroad" | t }}</a></li><li><a href="#discuss-a-thesis">{{ "Discuss a thesis" | t }}</a></li></ul>

{% if site.data.thesis_opportunities.projects.size > 0 %}
<section class="thesis-editorial thesis-editorial-projects" id="specific-projects" aria-labelledby="thesis-projects-title">
  <p class="editorial-index">02 / {{ 'Student projects' | t }}</p>
  <h2 id="thesis-projects-title">{{ 'Available thesis projects' | t }}</h2>
  <div class="thesis-editorial-project-list">
    {% for canonical_project in site.data.thesis_opportunities.projects %}
      {% include thesis_project_panel.html project=canonical_project ordinal=forloop.index %}
    {% endfor %}
  </div>
</section>
{% endif %}

<p class="editorial-index">03 / {{ "Research topics" | t }}</p>
<h2 id="research-directions">{{ "Explore a research direction" | t }}</h2>
<div class="feature-grid thesis-topics">{% for canonical_resource in site.data.thesis_opportunities.directions %}{% include resource_card.html resource=canonical_resource group="thesis" kind="thesis-topic" %}{% endfor %}</div>

<h2 id="ways-of-working">{{ "Choose how you work" | t }}</h2>
{% locale thesis.approaches %}<p>Choose computation, experiments or both; we will agree a feasible plan.</p>{% endlocale %}
<div class="approach-list">{% for canonical_approach in site.data.thesis_opportunities.approaches %}{% assign approach = canonical_approach | localized_record: 'thesis' %}<section class="approach"><h3>{{ approach.title }}</h3><p>{{ approach.description }}</p></section>{% endfor %}</div>
<ul class="inline-links"><li><a href="{{ '/laboratory/' | local_url | relative_url }}">{{ "Explore experimental capabilities" | t }}</a></li><li><a href="{{ '/teaching/' | local_url | relative_url }}">{{ "Courses and materials" | t }}</a></li></ul>



<section class="opportunity-context" aria-labelledby="italy-and-abroad">
  <h2 id="italy-and-abroad">{{ "Thesis activities in Italy and abroad" | t }}</h2>
  {% locale thesis.italy %}<p>Projects run at the <a href="https://www.dici.unipi.it/">Department of Civil and Industrial Engineering, University of Pisa</a>, with companies, or with international research institutions.</p>{% endlocale %}
  {% locale thesis.abroad %}<p>Research contacts from previous exchanges, to discuss a thesis abroad:</p>{% endlocale %}
  <ul class="institution-list">{% for institution in site.data.thesis_opportunities.international_contacts %}<li><a href="{{ institution.url }}">{{ institution.name }}</a><span>{{ institution.location | t }}{% if institution.detail %} · {{ institution.detail }}{% endif %}</span></li>{% endfor %}</ul>
  {% locale thesis.conditions %}<p class="scope-note">Placements abroad are not guaranteed: they depend on project availability, supervisors, host-institution acceptance, academic rules, and funding and mobility arrangements.</p>{% endlocale %}
</section>

<section id="discuss-a-thesis" class="collaboration-panel thesis-editorial" aria-labelledby="thesis-contact-title"><h2 id="thesis-contact-title">{{ "Interested in one of these topics?" | t }}</h2>{% locale thesis.contact %}<p>Email me your degree programme, interests, relevant experience and timeframe. Mention the project title if one interests you.</p>{% endlocale %}<a class="contact-link" href="mailto:andrea.chiocca@unipi.it?subject=Thesis%20Opportunity%20Research%20Interest">andrea.chiocca@unipi.it</a></section>

