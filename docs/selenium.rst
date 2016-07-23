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

      Controls most Selenium timeouts, defaults to ``10`` (seconds).

   .. attribute:: display

      Controls whether browser window is displayed or not, defaults to ``False``.

      Note that PhantomJS is always invisible, regardless of this value.

   .. attribute:: driver_name

      Controls which Selenium 'driver' i.e. browser will be used. Defaults to ``"Firefox"``.
      You can also use ``"Chrome"`` if Chrome and chromedriver are installed, and ``"PhantomJS"``
      if PhantomJS is installed.

   .. method:: display_browser_window

      classmethod. Returns boolean that determines if the browser window should be shown. Defaults to :attr:`display`.

   .. method:: get_browser_window_size()

      Returns :attr:`browser_window_size` by default.

   .. method:: get_default_timeout()

      classmethod. Returns the time in seconds for Selenium to wait for the browser to respond etc. Defaults to :attr:`default_timeout`.

   .. method:: get_driver_name()

      classmethod. Returns the driver name i.e. the browser to use. Defaults to :attr:`driver_name`.

   .. method:: get_page_load_timeout()

      classmethod. Returns the time in seconds for Selenium to wait for the browser to return a page. Defaults to :attr:`page_load_timeout`.

   .. attribute:: page_load_timeout

      Controls Selenium timeouts for loading page, defaults to ``20`` (seconds).

   .. method:: get_webdriver_options()

      Returns options to pass to the WebDriver class. Defaults to ``{}``. This
      can be used to pass ``capabilities``, ``firefox_binary`` or
      ``firefox_options`` if you are using the Firefox driver, for example.


   **Other attributes and methods**

   .. method:: click(css_selector=None, xpath=None, text=None, text_parent_id=None, wait_for_reload=False, double=False, scroll=True, window_closes=False)

      Clicks the button or control specified by the CSS selector e.g.::

        self.click("input.default")

      Alternatively, ``xpath`` or ``text`` can be provided as keyowrd arguments,
      instead of a CSS selector e.g.::

        self.click(xpath='//a[contains(text(), "kitten")]')
        self.click(text="kitten")

      Additionally, ``text_parent_id`` can be used in combination with ``text``
      to limit the search to descendent elements of the one with the
      supplied id.

      This method will attempt to scroll the window to make the element visible
      if ``scroll=True`` is passed (the default) - this is usually necessary for
      browsers to click controls correctly.

      If ``double=True`` is passed, a double click will be performed. Note, this
      will simply be two clicks, like a user would, rather than the Selenium
      ``double_click`` action chain, which doesn't actually trigger single click
      events.

      See also the notes in :meth:`~django_functest.FuncCommonApi.submit`
      regarding ``wait_for_reload`` and ``window_closes`` (noting that the
      default values are different).

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

   .. method:: save_screenshot(dirname="./", filename=None)

      Saves a screenshot of the browser window. By default, it is saved with a
      filename that includes a timestamp and the current test being run, into
      the current working directory, but this can be overridden by passing in
      a directory path and/or a filename. The full filename of the screenshot
      is returned.

   .. method:: set_window_size(width, height)

      Sets the browser window size to the specified width and height in pixels.

      For PhantomJS browser, this sets the document size - there isn't
      really a window.

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
      to the :attr:`default_timeout`. The callback must accept a single
      parameter which will be the driver instance.

   .. method:: wait_until_loaded(css_selector)

      Waits until an element matching the CSS selector appears.
