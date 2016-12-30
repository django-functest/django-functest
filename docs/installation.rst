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

  urlpatterns += [,
      url(r'^django_functest/', include('django_functest.urls'))
  ]


This is only necessary for running tests, so the above can be done conditionally
for test mode only, if possible.

Dependencies
============

Installing django-functest will install the Python ``selenium`` package
automatically. However, due the nature of Selenium, if you are writing Selenium
tests (i.e. if you are not simply using the WebTest wrapper), dependencies are
quite complex.

Selenium uses a ``WebDriver`` protocol for talking to browsers that is more or
less supported by different browsers. Please see the
:attr:`django_functest.FuncSeleniumMixin.driver_name` attribute for selecting
the browser to use, and note the following:

* Chrome can be used if `chromedriver
  <https://sites.google.com/a/chromium.org/chromedriver/>`_ is installed.

* Firefox 45 and older can be used with Selenium < 3 without anything additional
  installed. Old versions of Firefox can be found here:
  https://www.mozilla.org/en-US/firefox/organizations/all/

  If you need to run your own tests with a different version of Firefox than the
  default one on your system, it is recommended you follow the pattern used by
  django-functests own ``runtests.py`` script which allows you to pass a
  ``--firefox-binary`` option. This is then eventually returned by
  ``get_webdriver_options`` as argument ``firefox_binary``. You could also make
  ``get_webdriver_options`` look in ``os.environ`` if that is easier to arrange.

* Selenium >= 3 will not work with Firefox 45 or older.

* For newer versions of Firefox (tested with 50 and later), you can use Selenium
  3 or later, if you install the new `Marionette
  <https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver>`_
  driver, also known as ``geckodriver``. Unfortunately this currently is
  `incomplete
  <https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver/status>`_
  and has `many bugs
  <https://bugzilla.mozilla.org/buglist.cgi?bug_status=__open__&columnlist=assigned_to,bug_status,resolution,short_desc,changeddate,keywords,status_whiteboard&component=Marionette&product=Testing>`_
  and various incompatibilities. The django-functest suite fails in various
  places with this combination.

* If installed `PhantomJS <http://phantomjs.org/>`_ can be used.
