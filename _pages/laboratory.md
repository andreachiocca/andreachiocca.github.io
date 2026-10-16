---
layout: page
title: Laboratory & Experimental Capabilities
permalink: /laboratory/
description: Experimental mechanics, material and component characterisation, fatigue and numerical–experimental correlation for academic and industrial research collaboration.
---

My research in the machine design group at the **Department of Civil and Industrial Engineering, University of Pisa** combines experimental mechanics with computational analysis to understand material behaviour, structural integrity and durability.

This page presents expertise developed through our research activities and a starting point for discussing investigations using departmental and research-group facilities. Equipment access and the feasibility of a new test campaign must be confirmed with the relevant laboratory staff.

<ul class="inline-links page-paths"><li><a href="#research-expertise">Research expertise</a></li><li><a href="#instrumentation">Instrumentation and measurements</a></li><li><a href="#laboratory-collaboration">Discuss a collaboration</a></li></ul>

<h2 id="research-expertise">What we can investigate</h2>
<p>The linked studies and datasets document existing research experience. New material, component or loading requirements need a project-specific feasibility assessment.</p>
<div class="feature-grid laboratory-capabilities">{% for resource in site.data.laboratory.capabilities %}{% include resource_card.html resource=resource kind="capability-card" %}{% endfor %}</div>

<h2 id="instrumentation"><i class="far fa-chart-bar section-icon" aria-hidden="true"></i>Instrumentation and experimental methods</h2>
<p>Previous work brings together the following measurement and analysis activities. This is an overview of research methods, rather than an equipment inventory or a catalogue of testing services.</p>
<div class="approach-list">{% for method in site.data.laboratory.measurement_context %}<section class="approach"><h3>{{ method.title }}</h3><p>{{ method.description }}</p></section>{% endfor %}</div>
<p class="scope-note">Machine models, load capacities, loading modes, operating frequencies and environmental conditions are not listed until verified. Contact me to discuss which facilities and measurement systems are suitable for a specific investigation.</p>

{% if site.data.laboratory.equipment.size > 0 %}
<h2 id="equipment">Verified instrumentation</h2>
<div class="feature-grid">{% for resource in site.data.laboratory.equipment %}{% include resource_card.html resource=resource kind="equipment-card" %}{% endfor %}</div>
{% endif %}

<section id="laboratory-collaboration" class="collaboration-panel" aria-labelledby="laboratory-contact-title"><h2 id="laboratory-contact-title">Discuss an investigation or research collaboration</h2><p>I welcome enquiries from university groups and industrial R&amp;D teams about joint research, experimental campaigns, numerical–experimental studies, research proposals, material and component investigations, and method development.</p><p>Share the scientific question, material or component, expected loading and measurements, and any timing constraints. Activities depend on laboratory availability, technical feasibility, institutional procedures and an agreed project scope.</p><a class="contact-link" href="mailto:andrea.chiocca@unipi.it?subject=Experimental%20Investigation%20and%20Research%20Collaboration">andrea.chiocca@unipi.it</a></section>

<ul class="inline-links"><li><a href="{{ '/research/' | relative_url }}#projects">Research projects</a></li><li><a href="{{ '/publications/' | relative_url }}">Publications</a></li><li><a href="{{ '/repositories/' | relative_url }}">Software and research data</a></li><li><a href="{{ '/thesis/' | relative_url }}">Thesis opportunities</a></li></ul>
