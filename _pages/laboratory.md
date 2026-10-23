---
lang: en
translation_key: laboratory
layout: page
title: Laboratory & Experimental Capabilities
permalink: /laboratory/
description: Experimental facilities for fatigue, multiaxial loading, material and component characterisation and numerical–experimental research at the University of Pisa.
---

<div class="laboratory-editorial">

<section class="laboratory-hero" aria-label="{{ 'Research facilities' | t }}">
  <div class="laboratory-hero-copy" markdown="1">
    <p class="laboratory-kicker">01 / {{ "Research facilities" | t }}</p>
    <div class="laboratory-editorial">
  <section class="laboratory-hero" aria-labelledby="laboratory-hero-label">
    <div class="laboratory-hero-copy">
      <p class="laboratory-eyebrow" id="laboratory-hero-label">{{ "Experimental equipment" | t }} / 01</p>
      {% locale laboratory.intro %}<p>Our research investigates fatigue, material response and structural integrity in metallic, polymeric, composite and additively manufactured materials. Experimental work is combined with structural analysis and numerical–experimental correlation.</p>{% endlocale %}
      <p class="laboratory-hero-brief">{% locale laboratory.hero_note %}The equipment described below includes facilities recently documented by the research group and capabilities recorded in the historical Machine Design laboratory inventory. Operating limits and current availability depend on the experimental setup.{% endlocale %}</p>
    </div>
    <figure class="laboratory-hero-figure">
      <div class="laboratory-hero-image" aria-label="{{ "Machined fatigue specimen" | t }}">
        <img src="{{ '/assets/img/laboratory/specimen-640.webp' | local_url | relative_url }}"
          srcset="{{ '/assets/img/laboratory/specimen-640.webp' | local_url | relative_url }} 640w, {{ '/assets/img/laboratory/specimen-1280.webp' | local_url | relative_url }} 1280w"
          sizes="(max-width: 850px) 100vw, 44vw"
          width="640" height="800" alt="{{ "Machined fatigue specimen" | t }}" fetchpriority="high" decoding="async">
      </div>
      <figcaption>{% locale laboratory.hero_caption %}Machined specimen prepared for mechanical testing. No experimental result is implied by this photograph.{% endlocale %}</figcaption>
    </figure>
  </section>

  {% locale laboratory.scope %}<p class="laboratory-scope-note">This page presents research capabilities, not an accredited commercial testing service. Test feasibility and access to individual systems must be confirmed with the relevant laboratory staff.</p>{% endlocale %}

  <nav class="laboratory-local-nav" aria-label="{{ "Laboratory page sections" | t }}">
    <a href="#equipment">{{ "Experimental equipment" | t }}</a>
    <a href="#instrumentation">{{ "Instrumentation and measurements" | t }}</a>
    <a href="#research-expertise">{{ "Research expertise" | t }}</a>
    <a href="#laboratory-collaboration">{{ "Discuss a collaboration" | t }}</a>
  </nav>

  <section class="laboratory-equipment-section" aria-labelledby="equipment">
    <div class="laboratory-section-heading">
      <p class="laboratory-eyebrow">02 / {{ "Experimental equipment" | t }}</p>
      <h2 id="equipment">{{ "Verified instrumentation" | t }}</h2>
      {% locale laboratory.equipment_intro %}<p>Principal machines and experimental rigs. Maximum values refer to specific machines or operating modes and must not be interpreted as simultaneous loading limits.</p>{% endlocale %}
    </div>
    <div class="laboratory-featured-list">
      {% for canonical_resource in site.data.laboratory.equipment %}{% if canonical_resource.category == 'featured' %}
      {% include laboratory_equipment.html resource=canonical_resource featured=true %}
      {% endif %}{% endfor %}
    </div>
    <div class="laboratory-secondary-list">
      {% for canonical_resource in site.data.laboratory.equipment %}{% if canonical_resource.category == 'supporting' %}
      {% include laboratory_equipment.html resource=canonical_resource featured=false %}
      {% endif %}{% endfor %}
    </div>
  </section>

  <section class="laboratory-methods-section" aria-labelledby="instrumentation">
    <p class="laboratory-eyebrow">03 / {{ "Instrumentation and measurements" | t }}</p>
    <h2 id="instrumentation">{{ "Instrumentation and experimental methods" | t }}</h2>
    {% locale laboratory.methods %}<p>Our experimental work encompasses specimen and component loading, deformation and vibration measurements, environmental conditioning, thermal imaging and comparison with numerical models. The specific sensors and procedures are selected for each research question.</p>{% endlocale %}
    <div class="laboratory-methods-grid">
      {% for canonical_method in site.data.laboratory.measurement_context %}
      {% assign method = canonical_method | localized_record: 'laboratory' %}
      <section class="laboratory-method" id="{{ method.id | escape }}">
        <h3>{{ method.title }}</h3><p>{{ method.description }}</p>
      </section>
      {% endfor %}
    </div>
  </section>

  <section class="laboratory-research" aria-labelledby="research-expertise">
    <p class="laboratory-eyebrow">04 / {{ "Research expertise" | t }}</p>
    <h2 id="research-expertise">{{ "What we can investigate" | t }}</h2>
    {% locale laboratory.evidence %}<p>Documented publications and data illustrate previous experimental experience. A new material, structure or loading scenario requires a project-specific assessment.</p>{% endlocale %}
    <div class="laboratory-research-list">
      {% for canonical_resource in site.data.laboratory.capabilities %}
      {% assign capability = canonical_resource | localized_record: 'laboratory' %}
      <section class="laboratory-research-row">
        <h3>{{ capability.title }}</h3>
        <div><p>{{ capability.description }}</p>
        {% if capability.links.size > 0 %}<ul class="inline-links">{% for link in capability.links %}<li><a href="{{ link.url | local_url | relative_url }}">{{ link.label | t }}</a></li>{% endfor %}</ul>{% endif %}
        </div>
      </section>
      {% endfor %}
    </div>
  </section>

  {% locale laboratory.specifications %}<p class="laboratory-scope-note">Published maximum capacities and frequencies are indicative of specific machines and historical configurations. They do not replace equipment documentation or project-level feasibility checks.</p>{% endlocale %}
<section id="laboratory-collaboration" class="collaboration-panel laboratory-collaboration" aria-labelledby="laboratory-contact-title">
  <p class="laboratory-section-index">05 / {{ "Discuss a collaboration" | t }}</p>
  <h2 id="laboratory-contact-title">{{ "Discuss an investigation or research collaboration" | t }}</h2>
  {% locale laboratory.contact %}<p>I welcome enquiries from university groups and industrial R&amp;D teams about joint research, experimental campaigns, numerical–experimental studies, research proposals, material and component investigations, and method development.</p><p>Share the scientific question, material or component, expected loading and measurements, and any timing constraints. Activities depend on laboratory availability, technical feasibility, institutional procedures and an agreed project scope.</p>{% endlocale %}
  <a class="contact-link" href="mailto:andrea.chiocca@unipi.it?subject=Experimental%20Investigation%20and%20Research%20Collaboration">andrea.chiocca@unipi.it</a>
</section>

<ul class="inline-links laboratory-related">
  <li><a href="{{ '/research/' | local_url | relative_url }}#projects">{{ "Research projects" | t }}</a></li>
  <li><a href="{{ '/publications/' | local_url | relative_url }}">{{ "Publications" | t }}</a></li>
  <li><a href="{{ '/repositories/' | local_url | relative_url }}">{{ "Software and research data" | t }}</a></li>
  <li><a href="{{ '/thesis/' | local_url | relative_url }}">{{ "Thesis opportunities" | t }}</a></li>
</ul>

</div>

</div>
