Selenium wrapper
================

The class ``FuncSeleniumMixin`` has some Selenium/full browser specific methods, as well as the :doc:`common`.


.. class:: django_functest.FuncSeleniumMixin

   **Configuration**

   These are class attributes and class methods that determine how the browser
   will be set up and run. It is easiest to override the class attribute, but
   the class method exists also for more involved needs. Note that these are run
   when ``setUpClass`` is called.

   It is usually a good idea to set up a ``FuncSeleniumMixin`` sub-class in your
   project, to be used as a base-class for your tests, and set these
   configuration values on it.

   .. attribute:: default_timeout

      Controls Selenium timeouts, defaults to ``10`` (seconds).

   .. attribute:: display

      Controls whether browser window is displayed or not, defaults to ``False``

   .. attribute:: driver_name

      Controls which Selenium 'driver' i.e. browser will be used. Defaults to ``"Firefox"``

   .. method:: display_browser_window

      Returns boolean that determines if the browser window should be shown. Defaults to :attr:`display`.

   .. method:: get_default_timeout

      Returns the time in seconds for Selenium to wait for the browser to respond etc. Defaults to :attr:`default_timeout`.

   .. method:: get_driver_name

      Returns the driver name i.e. the browser to use. Defaults to :attr:`driver_name`.

   **Other attributes and methods**

   .. method:: click(css_selector, wait_for_reload=False, double=False, scroll=True)

      Clicks the button or control specified by the CSS selector.

      It will attempt to scroll the window to make the element visible if
      ``scroll=True`` is passed (the default) - this is usually necessary for browsers to click
      controls correctly.

      It will wait for the page to be reloaded if ``wait_for_reload=True`` is
      passed (not the default).

      If ``double=True`` is passed, a double click will be performed. Note, this
      will simply be two clicks, like a user would, rather than the Selenium
      ``double_click`` action chain, which doesn't actually trigger single click
      events.

   .. method:: is_element_displayed(css_selector)

      Returns ``True`` if the element specified by the CSS selector is both
      present (see :meth:`~django_functest.FuncCommonApi.is_element_present`)
      and visible on the page (e.g. does not have ``display: none;``),
      ``False`` otherwise.
