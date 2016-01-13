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

   .. method:: display_browser_window

      Returns boolean that determines if the browser window should be shown. Defaults to ``cls.display``.

   .. attribute:: display

      Defaults to ``False``

   .. method:: get_default_timeout

      Returns the time in seconds for Selenium to wait for the browser to respond etc. Defaults to ``cls.default_timeout``

   .. attribute:: default_timeout

      Defaults to ``10``.

   .. method:: get_driver_name

      Returns the driver name i.e. the browser to use. Defaults to ``cls.driver_name``

   .. attribute:: driver_name

      Defaults to ``"Firefox"``
