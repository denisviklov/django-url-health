==================
django-url-health
==================

.. image:: https://travis-ci.org/denisviklov/django-url-health.png?branch=master
   :target: https://travis-ci.org/denisviklov/django-url-health
.. image:: https://coveralls.io/repos/github/denisviklov/django-url-health/badge.svg?branch=master
   :target: https://coveralls.io/github/denisviklov/django-url-health?branch=master


**django-url-health** is a simple but powerful app to perform various actions on web pages.

It doesn't restrict only with URL checking because it supports custom ``BOTS`` what might perform any checks and send
appropriate data back on server

Requirements
============

`Python 3+`

`Django 2+`

`Celery 3+`

`CasperJS`

Installation
============

    ``pip install git+https://github.com:denisviklov/django-url-health.git``

Add ``'url_health'`` into your ``INSTALLED_APPS`` section.
Declare app's links in your url's configuration

   ``path(r'url_health/', include('url_health.urls')),``
 
**Don't forget** to recollect your static files.

Configuration
==============
If you respect requirements it works just out of the box. But configuration is available through standard Django's setting file::

    URL_HEALTH_RUNNER' = ['casperjs', BOT_PATH]

With this option you may point on your own bot implementation  