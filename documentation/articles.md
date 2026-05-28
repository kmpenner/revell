
---
layout: default
title: Articles
permalink: /articles/
---

# Articles

<ul>
{% for page in site.pages %}
  {% if page.path contains '07a Articles' and page.title %}
    <li>
      <a href="{{ page.url | relative_url }}">{{ page.title }}</a>
      {% if page.date %}
        <span class="meta">({{ page.date | date: "%Y" }})</span>
      {% endif %}
    </li>
  {% endif %}
{% endfor %}
</ul>
