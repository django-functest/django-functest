Common WebTest/Selenium API
===========================

The following methods and attributes are common to ``FuncWebTestMixin`` and
``FuncSeleniumMixin``:

.. class:: FuncCommonApi

   .. attribute:: current_url

      The current full URL

   .. attribute:: is_full_browser_test

      True for Selenium tests, False for WebTest tests.

   .. method:: get_url(name, *args, **kwargs)

      Gets the named URL, passing it through ``django.core.urlresolvers.reverse`` with ``*args`` and ``**kwargs``.

   .. method:: get_literal_url(relative_url)

      Gets the URL given by the relative URL passed in.
