===============
django-url-health
===============

.. image:: https://travis-ci.org/denisviklov/django-url-health.png?branch=master
   :target: https://travis-ci.org/denisviklov/django-url-health

**django-url-health** is a simple but powerful app to perform various actions on http pages.

It doesn't restrict only with URL checking because it supports custom ``BOTS`` what might perform any checks and send
appropriate data back on server

Requirements
============

``Python 3+``

``Django 2+``

``Celery 3+``

``CasperJS``


Installation
============

Clone and add 'url_health' in your ``INSTALLED_APPS`` section.
Also don't forget to recollect your static files that's how bot file appers in the avaliable directory
