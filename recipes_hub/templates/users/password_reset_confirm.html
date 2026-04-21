{% extends "includes/auth_shell.html" %}
{% load i18n %}
{% load form_tags %}

{% block title %}{% trans "Set new password" %}{% endblock %}

{% block auth_title %}{% trans "Choose a fresh password" %}{% endblock %}
{% block auth_description %}{% trans "A strong new password will get you back into your profile in a moment." %}{% endblock %}

{% block auth_card %}
  <div class="rh-card-header">
    <h2 class="rh-card-title">{% trans "Set new password" %}</h2>
    <p class="rh-card-text">{% trans "Use a password you do not reuse elsewhere." %}</p>
  </div>
  {% if validlink %}
    <form method="post" novalidate>
      {% csrf_token %}
      {% for field in form %}
        {% include "includes/form_field.html" with field=field %}
      {% endfor %}
      <button type="submit" class="btn btn-warning text-white w-100 mt-4 rh-btn-main">{% trans "Save new password" %}</button>
    </form>
  {% else %}
    <div class="alert alert-warning rh-note-box" role="alert">
      {% trans "This reset link is invalid or already used." %}
    </div>
  {% endif %}
  <div class="rh-inline-links mt-4">
    <a href="{% url 'users:login' %}" class="text-decoration-none">{% trans "Back to login" %}</a>
  </div>
{% endblock %}
