.. :changelog:

History
-------

1.3 (2022-02-15)
++++++++++++++++
* Added :meth:`~django_functest.FuncCommonApi.get_element_inner_text`
* Added :meth:`~django_functest.FuncCommonApi.get_element_attribute`.
* Fixed bugs with ``follow_link()`` and path-relative URLs
* Added support for Python 3.10
* Dropped support for Python 3.6. This is because:

  * The new ``get_element_attribute`` required Selenium >= 4, which
    is not available for Python 3.6 and below
  * Python 3.6 is now End Of Life


1.2 (2022-01-25)
++++++++++++++++

* Removed need for PyVirtualDisplay, by using “headless” options instead.
* Dropped support for Python 2.7 and Django < 2.0 (!)
* Dropped support for Python 3.5
* Fixed ``set_session_data`` when using signed cookies session backend.


1.1.1 (2021-09-23)
++++++++++++++++++

* Fixed test suite failure under Django 3.2
* Fixed warnings emitted under recent Django due to deprecations.
* Tested under Django 4.0a1

1.1 (2020-01-06)
++++++++++++++++

* Fixes for various things that broke with more recent versions
  Firefox/Chrome/geckodriver/chromedriver etc.

  * It is possible that if you are on older versions of Firefox you may have
    regressions or different behaviour with handling of linebreaks e.g. sending
    ``\r\n`` into textarea.

* Installation fix so that it can be installed with poetry
* Tested against more recent Django versions (up to 3.1), and fixed issues.
* Dropped support for Python 3.3 and 3.4
* Dropped support for Django 1.8, 1.9, 1.10 (which seemed to be broken anyway?)

1.0.4
+++++

* Fixed bug with setting checkboxes if a form had multiple checkboxes of the same name
* Enabled installation on PyPy (doesn't necessarily work completely).
* Test against Django 2.1
* Removed tests and official support for PhantomJS. (No actual functionality
  was changed regarding PhantomJS).

1.0.3
+++++

* Deprecated ``fill_by_id``. Instead of ``fill_by_id({'foo': 'bar'})`` you
  should do ``fill({'#foo': 'bar'})``, because it is shorter and more flexible.
* Test against latest Firefox
* Django 2.0 compatibility
* Fix for Django 1.11.2 and later for MultiThreadedLiveServerMixin

1.0.2
+++++

* Fixes to cope with WebTest 2.0.28. We now require django-webtest 1.9.2 or
  later, and only test against the latest WebTest.
* Fixed some deprecation warnings

1.0.1
+++++

* Fixed incompatibility with django-webtest 1.9.0 and later

1.0
+++

* Added Django 1.11 support.
* Dropped official Django 1.7 support (may still work).

0.2.1
+++++

* Made :meth:`~django_functest.FuncCommonApi.get_literal_url` accept
  absolute URLs for Selenium (WebTest already worked by accident).

0.2.0
+++++

* Added :meth:`~django_functest.FuncCommonApi.new_browser_session` and
  :meth:`~django_functest.FuncCommonApi.switch_browser_session` to the common
  API. These can be used to simulate multiple devices or users accessing the
  site. See the docs for important usage information.

0.1.9
+++++

* Fix for scrolling to exactly the right place.
* Added docstrings everywhere, and a base class you can inherit from
  for the purpose of providing autocomplete help.

0.1.8
+++++

* Django 1.10 compatibility

0.1.7
+++++

* Fixed performance/reliability issue caused by browsers attempting
  to retrieve ``/favicon.ico`` after visiting ``emptypage``.

0.1.6
+++++

* Fixed bug where elements wouldn't scroll into view if html height is set to
  100%
* New method :meth:`~django_functest.FuncSeleniumMixin.get_webdriver_options`
  for customizing WebDriver behaviour.

0.1.5
+++++

* Added get_session_data()
* Improved reliability of ``FuncSeleniumMixin.get_literal_url()``
* Allow ``<select>`` elements to be set using integers for values.
* Fixed issues with ``.value()`` for radio buttons and text areas
* Fixed bug with setting radio buttons when there are more than
  one set of radio buttons in the form.

0.1.4
+++++

* Added support for file uploads

0.1.3
+++++

* Support for filling radio buttons
* More convenient support for quotes and apostrophes (" ') in text assertion methods.

0.1.2
+++++

* Fixed wheel building - again!

0.1.1
+++++

* Fixed packaging bug that caused wheels to fail on Python 3.

0.1.0
+++++

* First release on PyPI.
