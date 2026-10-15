---
layout: page
permalink: /repositories/
title: Research outputs
description: Scientific software, fatigue benchmarks, and supporting research data by Andrea Chiocca, with repository links, DOIs and access information.
nav: false
---

Research software and archived data complement my [publications]({{ '/publications/' | relative_url }}) and [research activities]({{ '/research/' | relative_url }}). Access conditions and development scope are stated for each resource.

## Scientific software

{% assign software = site.data.research_outputs | where: 'kind', 'software' %}
{% for output in software %}{% include research_output.html %}{% endfor %}

This WG4.3 software activity is distinct from my [WG3 co-leadership]({{ '/research/' | relative_url }}#international-collaborations).

## Fatigue benchmarks

{% assign benchmarks = site.data.research_outputs | where: 'kind', 'benchmark' %}
{% for output in benchmarks %}{% include research_output.html %}{% endfor %}

## Supporting data and archived research outputs

{% assign datasets = site.data.research_outputs | where: 'kind', 'data' %}
{% for output in datasets %}{% include research_output.html %}{% endfor %}

## Additional code repositories

{% for repo in site.data.repositories.github_repos %}
- [{{ repo }}](https://github.com/{{ repo }})
{% endfor %}
