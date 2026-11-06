---
lang: en
translation_key: laboratory
layout: page
title: Laboratory & Experimental Capabilities
permalink: /laboratory/
description: Fatigue and multiaxial testing, material and component characterisation and numerical–experimental research at the University of Pisa.
seo_title: Fatigue Testing & Experimental Mechanics
---

<div class="laboratory-editorial">

<section class="laboratory-hero" aria-label="{{ 'Research facilities' | t }}">
  <div class="laboratory-hero-copy">
    <p class="laboratory-kicker">01 / {{ "Research facilities" | t }}</p>
    {% capture laboratory_intro %}{% locale laboratory.intro %}Experimental and computational research on fatigue, structural integrity and material behaviour at the **Department of Civil and Industrial Engineering, University of Pisa**: metals, polymers, composites and additively manufactured materials.{% endlocale %}{% endcapture %}
    {{ laboratory_intro | strip | markdownify }}
    {% capture laboratory_scope %}{% locale laboratory.scope %}The departmental facilities used by our group. Access and new tests are agreed with the laboratory staff.{% endlocale %}{% endcapture %}
    <div class="laboratory-hero-scope">{{ laboratory_scope | strip | markdownify }}</div>
    <nav aria-label="{{ 'Research facilities' | t }}" class="laboratory-quick-links">
      <a href="#equipment">{{ "Testing systems" | t }}</a>
      <a href="#instrumentation">{{ "Experimental measurement" | t }}</a>
      <a href="#laboratory-collaboration">{{ "Discuss a collaboration" | t }}</a>
    </nav>
  </div>
  {% assign hero = site.data.laboratory.hero | localized_record: 'laboratory' %}
  {% assign hero_640 = hero.image.base | append: '-640.webp' | local_url | relative_url %}
  {% assign hero_1280 = hero.image.base | append: '-1280.webp' | local_url | relative_url %}
  <figure class="laboratory-hero-figure">
    <picture>
      <source type="image/webp" srcset="{{ hero_640 }} 640w, {{ hero_1280 }} 1280w" sizes="(max-width: 767px) 92vw, 38vw">
      <img src="{{ hero_640 }}" alt="{{ hero.image_alt | escape }}" width="{{ hero.image.width }}" height="{{ hero.image.height }}" loading="eager" decoding="async" fetchpriority="high">
    </picture>
    <figcaption>{{ hero.image_caption | escape }}</figcaption>
  </figure>
</section>

<section class="laboratory-section laboratory-testing-systems" aria-labelledby="equipment">
  <p class="laboratory-section-index">02 / {{ "Featured equipment" | t }}</p>
  <h2 id="equipment">{{ "Experimental facilities" | t }}</h2>
  <div class="laboratory-machines">
    {% for canonical_resource in site.data.laboratory.equipment %}
      {% if canonical_resource.category == "featured" %}
        {% include laboratory_equipment.html resource=canonical_resource %}
      {% endif %}
    {% endfor %}
  </div>
  {% locale laboratory.specifications %}<p class="scope-note">Ranges depend on specimen and setup; feasibility is assessed per project.</p>{% endlocale %}
</section>

<section class="laboratory-section laboratory-support" aria-labelledby="instrumentation">
  <p class="laboratory-section-index">03 / {{ "Experimental measurement" | t }}</p>
  <h2 id="instrumentation">{{ "Instrumentation and experimental methods" | t }}</h2>
  {% locale laboratory.methods %}<p>Further equipment for structural, vibration and thermal testing and specimen preparation.</p>{% endlocale %}
  <div class="laboratory-machines laboratory-supporting-machines">
    {% for canonical_resource in site.data.laboratory.equipment %}
      {% if canonical_resource.category == "supporting" %}
        {% include laboratory_equipment.html resource=canonical_resource %}
      {% endif %}
    {% endfor %}
  </div>
  <div class="approach-list laboratory-approaches">
    {% for canonical_method in site.data.laboratory.measurement_context %}
      {% assign method = canonical_method | localized_record: 'laboratory' %}
      <section class="approach"><h3>{{ method.title }}</h3><p>{{ method.description }}</p></section>
    {% endfor %}
  </div>
</section>

<section class="laboratory-section laboratory-research" aria-labelledby="research-expertise">
  <p class="laboratory-section-index">04 / {{ "Research facilities" | t }}</p>
  <h2 id="research-expertise">{{ "What we can investigate" | t }}</h2>
  {% locale laboratory.evidence %}<p>Previous studies and datasets. New materials or loading cases need a specific feasibility check.</p>{% endlocale %}
  <div class="laboratory-research-domains">
    {% for canonical_resource in site.data.laboratory.capabilities %}
      {% include resource_card.html resource=canonical_resource group="laboratory" kind="capability-card" %}
    {% endfor %}
  </div>
</section>

<section id="laboratory-collaboration" class="collaboration-panel laboratory-collaboration" aria-labelledby="laboratory-contact-title">
  <p class="laboratory-section-index">05 / {{ "Discuss a collaboration" | t }}</p>
  <h2 id="laboratory-contact-title">{{ "Discuss an investigation or research collaboration" | t }}</h2>
  {% locale laboratory.contact %}<p>University groups and industrial R&amp;D teams are welcome to propose joint research, test campaigns or method development.</p><p>Please describe the question, material or component, loading and measurements, and timing. Activities depend on technical feasibility and institutional procedures.</p>{% endlocale %}
  <a class="contact-link" href="mailto:andrea.chiocca@unipi.it?subject=Experimental%20Investigation%20and%20Research%20Collaboration">andrea.chiocca@unipi.it</a>
</section>

<ul class="inline-links laboratory-related">
  <li><a href="{{ '/research/' | local_url | relative_url }}#projects">{{ "Research projects" | t }}</a></li>
  <li><a href="{{ '/publications/' | local_url | relative_url }}">{{ "Publications" | t }}</a></li>
  <li><a href="{{ '/repositories/' | local_url | relative_url }}">{{ "Software and research data" | t }}</a></li>
  <li><a href="{{ '/thesis/' | local_url | relative_url }}">{{ "Thesis opportunities" | t }}</a></li>
</ul>

</div>
