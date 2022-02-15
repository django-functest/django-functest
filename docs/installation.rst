============
Installation
============

At the command line::

    $ easy_install django-functest

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv django-functest
    $ pip install django-functest

You will also need to add django-functest to your URLs. In your URLconf::

  urlpatterns += patterns('',
      url(r'^django_functest/', include('django_functest.urls'))
  )

or::

  urlpatterns += [
      url(r'^django_functest/', include('django_functest.urls'))
  ]


This is only necessary for running tests, so the above can be done conditionally
for test mode only, if possible.

When running tests, you will also need to have ``localhost`` in your
``ALLOWED_HOSTS`` setting.

Dependencies
============

Python dependencies are automatically installed, including the Python
``selenium`` package. However, due the nature of Selenium, if you are writing
Selenium tests (i.e. if you are not simply using the WebTest wrapper),
dependencies are quite complex.

Selenium uses a ``WebDriver`` protocol for talking to browsers that is more or
less supported by different browsers. Please see the
:attr:`django_functest.FuncSeleniumMixin.driver_name` attribute for selecting
the browser to use.

In addition to needing web browsers installed, you often need additional driver
programs that speak the WebDriver protocol. These programs are not 100% complete
with each other, and have their own bugs and incompatibilities depending on
their version, and the version of the browser. Our policy is to try to test
against the latest version of the browser and latest version of the driver at
the time of release - see table below.

Tested browser versions:

+-------------------+---------------------+----------------------------+
| django-functest   | Firefox             | Chrome                     |
+===================+=====================+============================+
| 1.3               | Firefox 96.0        | Chrome 98.0                |
|                   | geckodriver 0.30.0  | chromedriver 98.0.4758.80  |
+-------------------+---------------------+----------------------------+
| 1.2               | Firefox 96.0        | Chrome 97.0                |
|                   | geckodriver 0.30.0  | chromedriver 97.0.4692.71  |
+-------------------+---------------------+----------------------------+
| 1.1.1             | Firefox 92.0        | Chrome 94                  |
|                   | geckodriver 0.30.0  | chromedriver 94.0.4606.41  |
+-------------------+---------------------+----------------------------+
| 1.1.0             | Firefox 84          | Chrome 87                  |
|                   | geckodriver 0.28.0  | chromedriver 87.0.4280.88  |
+-------------------+---------------------+----------------------------+
| 1.0.4             | Firefox 58          | Chrome ?                   |
|                   | geckodriver 0.20.0  | chromedriver 2.37          |
+-------------------+---------------------+----------------------------+

Browser specific notes below:

Chrome
------

Chrome can be used if `chromedriver
<https://sites.google.com/a/chromium.org/chromedriver/>`_ is installed.

Firefox
-------

You need to install the `Marionette
<https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver>`_
driver, also known as ``geckodriver`` (`download releases here
<https://github.com/mozilla/geckodriver/releases>`_).

If you need to run your own tests with a different version of Firefox than the
default one on your system, it is recommended you follow the pattern used by
django-functest's own `runtests.py
<https://github.com/django-functest/django-functest/blob/master/runtests.py>`_
script which allows you to pass a ``--firefox-binary`` option. This is then
eventually returned by
:meth:`~django_functest.FuncSeleniumMixin.get_webdriver_options` as argument
``firefox_binary`` (see `tests/base.py
<https://github.com/django-functest/django-functest/blob/master/django_functest/tests/base.py>`_).
You could also make ``get_webdriver_options`` look in ``os.environ`` if that is
easier to arrange. If you are using pytest, see the :doc:`pytest` tips for some
better patterns for doing this kind of thing.
