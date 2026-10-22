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
    {% locale laboratory.intro %}Our group at the **Department of Civil and Industrial Engineering, University of Pisa** investigates fatigue, structural integrity and material behaviour through experimental mechanics and computational analysis. Research addresses metals, polymers, composites and additively manufactured materials.{% endlocale %}
    <div class="laboratory-hero-scope" markdown="1">{% locale laboratory.scope %}This page presents research expertise and departmental facilities associated with our group. Equipment access and the technical feasibility of a new test campaign must be agreed with the relevant laboratory staff.{% endlocale %}</div>
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
  {% locale laboratory.specifications %}<p class="scope-note">The values reported describe specific machines, not necessarily simultaneous operating limits. Historical equipment details and availability should be confirmed when defining a new experimental campaign.</p>{% endlocale %}
</section>

<section class="laboratory-section laboratory-support" aria-labelledby="instrumentation">
  <p class="laboratory-section-index">03 / {{ "Experimental measurement" | t }}</p>
  <h2 id="instrumentation">{{ "Instrumentation and experimental methods" | t }}</h2>
  {% locale laboratory.methods %}<p>Additional facilities support structural testing, vibration measurements, thermal investigations and specimen preparation. The experimental arrangement and acquisition settings depend on the specific research question.</p>{% endlocale %}
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
  {% locale laboratory.evidence %}<p>The studies and datasets linked below document existing research experience. Each new material, component and loading configuration requires a project-specific feasibility assessment.</p>{% endlocale %}
  <div class="laboratory-research-domains">
    {% for canonical_resource in site.data.laboratory.capabilities %}
      {% include resource_card.html resource=canonical_resource group="laboratory" kind="capability-card" %}
    {% endfor %}
  </div>
</section>

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
