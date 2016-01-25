Selenium wrapper
================

The class ``FuncSeleniumMixin`` has some Selenium/full browser specific methods, as well as the :doc:`common`.


.. class:: django_functest.FuncSeleniumMixin

   .. _selenium-configuration:

   **Configuration**

   These are class attributes and class methods that determine how the browser
   will be set up and run. It is easiest to override the class attribute, but
   the class method exists also for more involved needs. Note that most of these
   are used when ``setUpClass`` is called, and most of the related methods
   are therefore classmethods. Some are called within ``setUp``

   It is usually a good idea to set up a ``FuncSeleniumMixin`` sub-class in your
   project, to be used as a base-class for your tests, and set these
   configuration values on it.

   .. attribute:: browser_window_size

      If set, should be a tuple containing ``(width, height)`` in pixels. This
      will be used inside ``setUp`` to set the browser window size. Defaults
      to ``None``.

   .. attribute:: default_timeout

      Controls Selenium timeouts, defaults to ``10`` (seconds).

   .. attribute:: display

      Controls whether browser window is displayed or not, defaults to ``False``

   .. attribute:: driver_name

      Controls which Selenium 'driver' i.e. browser will be used. Defaults to ``"Firefox"``.
      You can also use ``"Chrome"`` if Chrome and chromedriver are installed.

   .. method:: display_browser_window

      classmethod. Returns boolean that determines if the browser window should be shown. Defaults to :attr:`display`.

   .. method:: get_browser_window_size()

      Returns :attr:`browser_window_size` by default.

   .. method:: get_default_timeout()

      classmethod. Returns the time in seconds for Selenium to wait for the browser to respond etc. Defaults to :attr:`default_timeout`.

   .. method:: get_driver_name()

      classmethod. Returns the driver name i.e. the browser to use. Defaults to :attr:`driver_name`.

   **Other attributes and methods**

   .. method:: click(css_selector=None, xpath=None, wait_for_reload=False, double=False, scroll=True)

      Clicks the button or control specified by the CSS selector e.g.::

        self.click("input.default")

      If ``xpath`` is specified instead, ``css_selector`` does not need to be
      passed, and the element will be found using the XPath selector e.g.::

        self.click(xpath='//a[contains(text(), "kitten")]')

      This method will attempt to scroll the window to make the element visible
      if ``scroll=True`` is passed (the default) - this is usually necessary for
      browsers to click controls correctly.

      It will wait for the page to be reloaded if ``wait_for_reload=True`` is
      passed (not the default).

      If ``double=True`` is passed, a double click will be performed. Note, this
      will simply be two clicks, like a user would, rather than the Selenium
      ``double_click`` action chain, which doesn't actually trigger single click
      events.

   .. method:: execute_script(script, *args)

      Executes the suppplied Javascript in the browser and returns the results.

      If you need to pass arguments, you can receive them in the script using
      ``arguments`` e.g.::

        self.execute_script("return arguments[0] + arguments[1];", 1, 2)

      Arguments and return values are serialized and deserialized by Selenium.

   .. method:: hover(css_selector)

      Peform a mouse hover over the element specified by the CSS selector.

   .. method:: is_element_displayed(css_selector)

      Returns ``True`` if the element specified by the CSS selector is both
      present (see :meth:`~django_functest.FuncCommonApi.is_element_present`)
      and visible on the page (e.g. does not have ``display: none;``),
      ``False`` otherwise.

   .. method:: set_window_size(width, height)

      Sets the browser window size to the specified width and height in pixels.

   .. method:: switch_window(handle=None)

      Switches the browser window that has focus.

      If there are only 2 windows, it can work out which window to switch to.
      Otherwise, you must pass in the window handle as the ``handle`` kwarg.

      The method returns a tuple of ``(old_window_handle, new_window_handle)``
      which can be used in subsequent calls to ``switch_window``.

   .. method:: wait_for_page_load()

      Waits until the page has finished loading. You may want to override this
      to add extra things if a page has specific requirements.

   .. method:: wait_until(callback, timeout=None)

      Waits until the callback returns ``True``, with a timeout that defaults
      to the :attr:`default_timeout`.

   .. method:: wait_until_loaded(css_selector)

      Waits until an element matching the CSS selector appears.
