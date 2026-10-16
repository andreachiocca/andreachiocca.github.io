---
lang: en
translation_key: laboratory
layout: page
title: Laboratory & Experimental Capabilities
permalink: /laboratory/
description: Experimental mechanics, material and component characterisation, fatigue and numerical–experimental correlation for academic and industrial research collaboration.
---

{% locale laboratory.intro %}My research in the machine design group at the **Department of Civil and Industrial Engineering, University of Pisa** combines experimental mechanics with computational analysis to understand material behaviour, structural integrity and durability.{% endlocale %}

{% locale laboratory.scope %}This page presents expertise developed through our research activities and a starting point for discussing investigations using departmental and research-group facilities. Equipment access and the feasibility of a new test campaign must be confirmed with the relevant laboratory staff.{% endlocale %}

<ul class="inline-links page-paths"><li><a href="#research-expertise">{{ "Research expertise" | t }}</a></li><li><a href="#instrumentation">{{ "Instrumentation and measurements" | t }}</a></li><li><a href="#laboratory-collaboration">{{ "Discuss a collaboration" | t }}</a></li></ul>

<h2 id="research-expertise">{{ "What we can investigate" | t }}</h2>
{% locale laboratory.evidence %}<p>The linked studies and datasets document existing research experience. New material, component or loading requirements need a project-specific feasibility assessment.</p>{% endlocale %}
<div class="feature-grid laboratory-capabilities">{% for canonical_resource in site.data.laboratory.capabilities %}{% include resource_card.html resource=canonical_resource group="laboratory" kind="capability-card" %}{% endfor %}</div>

<h2 id="instrumentation"><i class="far fa-chart-bar section-icon" aria-hidden="true"></i>{{ "Instrumentation and experimental methods" | t }}</h2>
{% locale laboratory.methods %}<p>Previous work brings together the following measurement and analysis activities. This is an overview of research methods, rather than an equipment inventory or a catalogue of testing services.</p>{% endlocale %}
<div class="approach-list">{% for canonical_method in site.data.laboratory.measurement_context %}{% assign method = canonical_method | localized_record: 'laboratory' %}<section class="approach"><h3>{{ method.title }}</h3><p>{{ method.description }}</p></section>{% endfor %}</div>
{% locale laboratory.specifications %}<p class="scope-note">Machine models, load capacities, loading modes, operating frequencies and environmental conditions are not listed until verified. Contact me to discuss which facilities and measurement systems are suitable for a specific investigation.</p>{% endlocale %}

{% if site.data.laboratory.equipment.size > 0 %}
<h2 id="equipment">{{ "Verified instrumentation" | t }}</h2>
<div class="feature-grid">{% for canonical_resource in site.data.laboratory.equipment %}{% include resource_card.html resource=canonical_resource group="laboratory" kind="equipment-card" %}{% endfor %}</div>
{% endif %}

<section id="laboratory-collaboration" class="collaboration-panel" aria-labelledby="laboratory-contact-title"><h2 id="laboratory-contact-title">{{ "Discuss an investigation or research collaboration" | t }}</h2>{% locale laboratory.contact %}<p>I welcome enquiries from university groups and industrial R&amp;D teams about joint research, experimental campaigns, numerical–experimental studies, research proposals, material and component investigations, and method development.</p><p>Share the scientific question, material or component, expected loading and measurements, and any timing constraints. Activities depend on laboratory availability, technical feasibility, institutional procedures and an agreed project scope.</p>{% endlocale %}<a class="contact-link" href="mailto:andrea.chiocca@unipi.it?subject=Experimental%20Investigation%20and%20Research%20Collaboration">andrea.chiocca@unipi.it</a></section>

<ul class="inline-links"><li><a href="{{ '/research/' | local_url | relative_url }}#projects">{{ "Research projects" | t }}</a></li><li><a href="{{ '/publications/' | local_url | relative_url }}">{{ "Publications" | t }}</a></li><li><a href="{{ '/repositories/' | local_url | relative_url }}">{{ "Software and research data" | t }}</a></li><li><a href="{{ '/thesis/' | local_url | relative_url }}">{{ "Thesis opportunities" | t }}</a></li></ul>
