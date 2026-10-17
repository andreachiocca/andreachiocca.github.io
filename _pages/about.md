---
lang: en
translation_key: home
layout: about
title: Home
permalink: /
subtitle: Researcher in machine design (research contract)

profile:
  align: right
  image: prof_pic.jpg
  image_alt: Andrea Chiocca
  image_circular: true # crops the image to make it circular
  more_info: >
    <p><i class="fas fa-phone-alt" aria-hidden="true"></i><a href="tel:+390502218036">+39 050 2218036</a></p>
    <p><i class="fas fa-map-marker-alt" aria-hidden="true"></i><span>L. Lucio Lazzarino 2<br>56123, Pisa, Italy</span></p>

news: false  # includes a list of news items
recent_papers: true # five most recent published bibliography records
social: true  # includes social icons at the bottom of the page
---

{% locale home.intro %}I study **fatigue and structural integrity**, examining how repeated loads affect notched and welded components, materials and joints. My work combines **finite element modelling, analytical methods and experimental testing**, with applications in mechanical design, automotive components and additive manufacturing.{% endlocale %}

<section id="research-environment" aria-label="{{ 'Research environment' | t }}">
{% locale home.context %}<p>I work in the machine design research group (<em>Gruppo di Costruzione di Macchine</em>) within the <a href="https://www.dici.unipi.it/">Department of Civil and Industrial Engineering (DICI)</a>, <a href="https://www.unipi.it/">University of Pisa</a>. The group’s expertise in experimental mechanics and modelling provides the context for my research on fatigue and structural integrity.</p>{% endlocale %}
</section>

{% locale home.bio %}I hold a research contract at the University of Pisa and am **Co-Leader of FABER WG3 (Fatigue Estimation Competition)**. I received my PhD in Industrial Engineering from Pisa in 2021.{% endlocale %}

<ul class="inline-links home-paths"><li><a href="{{ '/research/' | local_url | relative_url }}">{{ "Research areas" | t }}</a></li><li><a href="{{ '/repositories/' | local_url | relative_url }}">{{ "Software & data" | t }}</a></li><li><a href="{{ '/teaching/' | local_url | relative_url }}">{{ "For students" | t }}</a></li><li><a href="#collaboration">{{ "Contact" | t }}</a></li></ul>
