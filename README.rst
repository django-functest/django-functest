===============
django-functest
===============

.. image:: https://github.com/django-functest/django-functest/workflows/Python%20package/badge.svg
   :target: https://github.com/django-functest/django-functest/actions?query=workflow%3A%22Python+package%22+branch%3Amaster

.. image:: https://readthedocs.org/projects/django-functest/badge/?version=latest
   :target: https://django-functest.readthedocs.org/en/latest/


Helpers for creating high-level functional tests in Django, with a unified API
for WebTest and Selenium tests.

    Exploring django-functest makes me angry! Why? Because I've wasted so much
    time writing low-level, boilerplate-filled tests for the past few years
    instead of using it —
    `jerivas <https://github.com/stephenmcd/mezzanine/issues/1012#issuecomment-666802439>`_

What is `WebTest
<https://docs.pylonsproject.org/projects/webtest/en/latest/index.html>`__?
Imagine a text-based, HTML-only browser that doesn’t load CSS, Javascript etc,
operates directly on a WSGI interface in a synchronous fashion for performance
and robustness, and is controlled programmatically.

What is `Selenium <https://www.selenium.dev/>`__? A tool that opens full browsers
like Firefox and Chrome (with an isolated profile), and provides an API for
controlling them.

For an idea of what writing tests with django-functest looks like in practice,
you might be interested in the video in our `writing tests interactively
documentation
<https://django-functest.readthedocs.io/en/latest/interactive.html>`_.

Documentation
-------------

The full documentation is at https://django-functest.readthedocs.org.

Installation
------------

Python 3.7 and later, Django 2.0 and later are required.

::

   pip install django-functest

See also the `dependencies documentation
<http://django-functest.readthedocs.io/en/latest/installation.html#dependencies>`_
for important compatibility information.

Features
--------

* A simplified API for writing functional tests in Django (tests that check the
  behaviour of entire views, or sets of views, e.g. a checkout process).

* A unified API that abstracts over both `WebTest
  <http://webtest.pythonpaste.org/en/latest/>`__ and `Selenium
  <https://pypi.python.org/pypi/selenium>`__ - write two tests at once!

* Many of the gotchas and difficulties of using WebTest and Selenium ironed out
  for you.

* Well tested - as well as its own test suite, which is run against Firefox
  and Chrome, it is also used by `Wolf & Badger
  <https://www.wolfandbadger.com/>`_ for tests covering many business critical
  functionalities.

* Supports running with pytest (using pytest-django) as well as Django’s
  ``manage.py test``

Typical usage
-------------

In your tests.py:

.. code-block:: python

   from django.test import LiveServerTestCase, TestCase
   from django_functest import FuncWebTestMixin, FuncSeleniumMixin, FuncBaseMixin


   class ContactTestBase(FuncBaseMixin):
       # Abstract class, doesn't inherit from TestCase

       def test_contact_form(self):
           self.get_url("contact_form")
           self.fill(
               {
                   "#id_name": "Joe",
                   "#id_message": "Hello",
               }
           )
           self.submit("input[type=submit]")
           self.assertTextPresent("Thanks for your message")


   class ContactWebTest(ContactTestBase, FuncWebTestMixin, TestCase):
       pass


   class ContactSeleniumTest(ContactTestBase, FuncSeleniumMixin, LiveServerTestCase):
       pass


In this way, you can write a single test with a high-level API, and run it in
two ways - using a fast, WSGI-based method which emulates typical HTTP usage of a
browser, and using a full browser that actually executes Javascript (if present)
etc.

The approach taken by django-functest is ideal if your web app is mostly a
"classic" app with server-side rendered HTML combined with a careful sprinkling
of Javascript to enhance the UI, which you also need to be able to test. If such
an approach seems old-fashioned to you, have a look at `htmx.org
<https://htmx.org/>`_ or `hotwire <https://hotwired.dev/>`_ and get with the new
kids! (OK most of are actually quite old but we make fast web sites...)

Under the hood, the WSGI-based method uses and builds upon `WebTest
<http://webtest.pythonpaste.org/en/latest/>`_ and `django-webtest
<https://pypi.python.org/pypi/django-webtest>`_.

django-functest provides its functionality as mixins, so that you can have your
own base class for tests.

Contributing and tests
----------------------

See `CONTRIBUTING.rst <CONTRIBUTING.rst>`_ for information about running the test suite and
contributing to django-functest.


Building on Mac OS
------------------

While [this lxml bug](https://bugs.launchpad.net/lxml/+bug/1949271) is in
effect `lxml` cannot handle certain unicode characters in HTML (or XML!)
documents on Mac OS, including the emoji used in one of the files in the test
suite.

Therefore, if you are affected by this bug, you will find that certain tests
fail with the error `lxml.etree.ParserError: Document is empty`.

You will also find that `lxml`'s own test suite fails on your machine.

A workaround is to compile `libxml2` yourself, which `lxml` will take care of for you.
To do this, run the following:

```
STATICBUILD=true python -m pip install lxml --force-reinstall --no-binary=:all:
```

Paid support
------------

Some of the maintainers are able to provide support on a paid basis for this
Open Source project. This includes the following kinds of things:

* Paying for bug fixes or new features (with the understanding that these
  changes will become freely available as part of the project and are not
  'owned' by the person who paid for them).

* Debugging or other support for integrating django-functest into your project.

* Writing a test suite for you from scratch using django-functest.

If you are interested in these, you can contact the following developers:

* Luke Plant - long time Django expert and contributor - `info and status <https://lukeplant.me.uk/development-work.html>`_.


Credits
-------

This library was written originally by `spookylukey <https://github.com/spookylukey/>`_,
further improved by developers at `Wolf & Badger
<https://www.wolfandbadger.com/>`_, and released with the kind permission of that
company.

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
