.. :changelog:

History
-------

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
* New method ``get_webdriver_options`` for customizing WebDriver behaviour.

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
