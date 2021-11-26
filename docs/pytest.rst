==================
Pytest integration
==================

You can use django-functest with pytest, using the `pytest-django
<https://pytest-django.readthedocs.io/en/latest/index.html>`_ plugin. The
supported pattern is that you write your tests in the unittest style as per the
:doc:`usage` docs, and run them with pytest, as per the pytest-django docs.

Below are some optional but very helpful tips to make things nicer:

1. Use `conftest.py
   <https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option>`_
   to add some ``pytest`` command line arguments that control which browser to
   use, and whether to show the browser or not.

2. Use a pytest `mark <https://docs.pytest.org/en/latest/how-to/mark.html>`_ on
   your base class for Selenium tests to be able to mark all your Selenium
   tests, and therefore easily select or de-select them.

An example of putting these together is below.

In ``conftest.py``:

.. code-block:: python

   BROWSER = "Firefox"
   SHOW_BROWSER = False


   def pytest_addoption(parser):
       parser.addoption(
           "--browser", type=str, default="Firefox", help="Selenium driver_name to use", choices=["Firefox", "Chrome"]
       )
       parser.addoption("--show-browser", action="store_true", default=False, help="Show web browser window")


   def pytest_configure(config):
       global SHOW_BROWSER, BROWSER
       BROWSER = config.option.browser
       SHOW_BROWSER = config.option.show_browser


Then write your ``SeleniumTestBase`` something like this:

.. code-block:: python

   from django.test import TestCase
   from django.contrib.staticfiles.testing import StaticLiveServerTestCase
   from django_functest import FuncSeleniumMixin

   import conftest


   @pytest.mark.selenium
   class SeleniumTestBase(FuncSeleniumMixin, StaticLiveServerTestCase):
       driver_name = conftest.BROWSER
       display = conftest.SHOW_BROWSER


You can now de-select all Selenium tests by doing ``pytest -m 'not selenium'``,
and use ``--show-browser`` or ``--browser=Chrome`` etc. as needed.
