=============================
django-functest
=============================

.. image:: https://travis-ci.org/spookylukey/django-functest.png?branch=master
    :target: https://travis-ci.org/spookylukey/django-functest

Helpers for creating functional tests in Django, with a unified API for WebTest and Selenium tests.

Documentation
-------------

The full documentation is at https://django-functest.readthedocs.org.

Quickstart
----------

Install django-functest::

    pip install django-functest

Then use it in a project::

    import django_functest

Features
--------

* A simplified API for writing functional tests in Django (tests that check the
  behaviour of entire views, or sets of views, e.g. a checkout process).

* A unified API that works with both WebTest and Selenium - write two tests at once!

Running Tests
--------------

To run the tests:

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ ./setup.py develop
    (myenv) $ ./runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/pydanny/cookiecutter-djangopackage
