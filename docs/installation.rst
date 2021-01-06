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
``selenium`` package automatically. However, due the nature of Selenium, if you
are writing Selenium tests (i.e. if you are not simply using the WebTest
wrapper), dependencies are quite complex.

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

In addition, in order to hide the browser window (the default behaviour),
`PyVirtualDisplay <https://github.com/ponty/pyvirtualdisplay`_ is used. Please
see the `PyVirtualDisplay installation dependencies
<https://github.com/ponty/pyvirtualdisplay>`_ - it has various supported
"backends", one of which needs to be installed.

Tested browser versions:

+-------------------+---------------------+----------------------------+
| django-functest   | Firefox             | Chrome                     |
+===================+=====================+============================+
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

For recent versions of Firefox, you can use Selenium 3 or later, if you install
the new `Marionette
<https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver>`_
driver, also known as ``geckodriver`` (`download releases here
<https://github.com/mozilla/geckodriver/releases>`_).

This implementation currently is `incomplete
<https://bugzilla.mozilla.org/show_bug.cgi?id=721859>`_ and has `bugs
<https://bugzilla.mozilla.org/buglist.cgi?bug_status=__open__&columnlist=assigned_to,bug_status,resolution,short_desc,changeddate,keywords,status_whiteboard&component=Marionette&product=Testing>`_
and various incompatibilities. However, with the most recent versions the
django-functest suite passes fully.

Firefox 45 and older can be used with Selenium < 3 without anything additional
installed. Old versions of Firefox can be found here:
https://ftp.mozilla.org/pub/firefox/releases/ You may need older versions of
django-functest for this to work.

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
easier to arrange.

PhantomJS
---------

If installed, `PhantomJS <http://phantomjs.org/>`_ can be used. PhantomJS is no
longer officially supported - the test suite does not run against it and bugs
for it will not be fixed. This is because the project has been abandoned, and
Selenium also no longer supports it.


Other notes about old versions
------------------------------

* If you are using Django < 1.11, you should install django-functest < 1.0.1 and
  django-webtest < 1.9.1.

* If you are using Firefox 45 or older, you will need Selenium < 3
