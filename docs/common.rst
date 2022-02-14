Common WebTest/Selenium API
===========================

This page documents the methods and attributes that are provided by both
:class:`django_functest.FuncWebTestMixin` and
:class:`django_functest.FuncSeleniumMixin`.

Conventions:

unittest provides assertion methods that are ``camelCased``. Django follows
suit with assertion methods, but for other things defaults to the PEP8
recommendation of ``name_with_underscores`` e.g. ``live_server_url``. We have
followed the same pattern.

.. currentmodule:: django_functest

.. class:: FuncCommonApi

   **Assertion methods**

   .. method:: assertUrlsEqual(url, other_url=None)

      Checks that the URLs are equal, with ``other_url`` defaulting to the
      current URL if not passed. The path and query are checked, and if both
      URLs contain a domain name and/or protocol, these are also checked. This
      means that relative URLs can be used, or protocol-relative URLs.

   .. method:: assertTextPresent(text)

      Asserts that the text is present on the current page

   .. method:: assertTextAbsent(text)

      Asserts that the text is not present on the current page

   **Other methods and attributes**

   .. method:: back()

      Go back in the browser.

      For WebTest, this will not make additional requests. For Selenium tests,
      this may or may not make additional requests, depending on caching etc. and what
      happens when you press 'Back' in the browser being used.

   .. attribute:: current_url

      The current full URL

   .. method:: follow_link(css_selector)

      Follows the link specified in the CSS selector.

      You will get an exception if no links match.

      For :class:`django_functest.FuncWebTestMixin`, you will get an exception if multiple
      links match and they don't have the same href.


   .. method:: fill(data_dict)

      Fills form inputs using the values in ``data_dict``. The keys are CSS
      selectors, and the values are the values for the inputs. Works for text
      inputs, radio boxes, check boxes, and select fields. Checkbox values can
      be specified using ``True`` and ``False``. Radio button values should be
      specified using the ``value`` attribute that should be matched, and the radio
      button that matches that will be selected (even if the selector matched another
      button in that group).

      To upload a file, pass an :class:`~django_functest.Upload` instance as the value.

      This will raise an exception if the fields can't be found. It will be a
      timeout exception for Selenium tests, so you will want to avoid attempting
      to fill in fields that don't exist.

      If multiple fields match, you will get an exception for
      :class:`~django_functest.FuncWebTestMixin` but not for
      :class:`~django_functest.FuncSeleniumMixin` due to the way Selenium finds
      elements.

   .. method:: fill_by_id(data_dict)

      Same as :meth:`fill` except the keys are element IDs. **Deprecated** —
      instead of ``fill_by_id({'foo': 'bar'})`` you should do ``fill({'#foo':
      'bar'})``, because it is shorter and more flexible.

   .. method:: fill_by_name(data_dict)

      Same as :meth:`fill` except the keys are input names.

   .. method:: fill_by_text(data_dict)

      Same as :meth:`fill`, except the values are text captions. This can be
      used only for ``select`` elements.

   .. method:: get_element_attribute(css_selector, attribute)

      Returns the value of the attribute of the element matching the css_selector,
      or None if there is no such element or attribute.

      For :class:`django_functest.FuncWebTestMixin`, you will get an exception
      if multiple elements match.

   .. method:: get_element_inner_text(css_selector)

      Returns the "inner text" (``innerText`` in JS) of the element matching
      the ``css_selector``, or ``None`` if there is no match.

      For :class:`django_functest.FuncWebTestMixin`, you will get an exception
      if multiple elements match.


   .. method:: get_url(name, *args, **kwargs)

      Gets the named URL, passing it through ``django.core.urlresolvers.reverse`` with ``*args`` and ``**kwargs``.

      e.g.::

        self.get_url('admin:auth_user_change', object_id=1)

   .. method:: get_literal_url(relative_url, auto_follow=True, expect_errors=False)

      Gets the URL given by the relative URL passed in.

      For :class:`~django_functest.FuncWebTestMixin`, pass ``auto_follow=False``
      if you don't want redirects to be followed. This parameter is ignored by
      :class:`~django_functest.FuncSeleniumMixin`.

      For :class:`~django_functest.FuncWebTestMixin`, pass ``expect_errors=True``
      if you are expecting an error code e.g. a 404, otherwise you will get an
      exception. This parameter is ignored by :class:`~django_functest.FuncSeleniumMixin`.

   .. method:: is_element_present(css_selector)

      Returns ``True`` if the element specified by the CSS selector is present, ``False`` otherwise.
      See also :meth:`~django_functest.FuncSeleniumMixin.is_element_displayed`.

   .. attribute:: is_full_browser_test

      True for Selenium tests, False for WebTest tests.

   .. method:: set_session_data(data_dict)

      Set data directly into the Django session from the supplied dictionary.
      This is useful for implementing setup/shortcuts needed for specific views.

   .. method:: get_session_data()

      Get the Django session as a dictionary. This is useful for creating
      assertions.

   .. method:: new_browser_session()

      Creates (and switches to) a new session that is separate from previous
      sessions. This can be used to simulate multiple devices/users accessing a
      site at the same time.

      Returns a tuple (old_session_token, new_session_token). These values
      should be treated as opaque tokens that can be used with
      :meth:`switch_browser_session`.

      For Selenium tests, a new instance of the web driver is created, which
      results in a new browser instance with a separate profile being used. In
      this case, however, there are complications:

      Before Django 2.0, ``LiveServerTestCase`` was single threaded. Some
      browsers keep multiple connections open to a domain, and Chrome especially
      can lock up the test server when multiple sessions are open.

      If you are using Django < 2.0, a fix for this is to add
      :class:`django_functest.MultiThreadedLiveServerMixin` to any test class
      that needs this functionality, especially if run against Chrome. However,
      please note the issues documented for that mixin.

   .. method:: switch_browser_session(session_token)

      Switch to the browser session indicated by the supplied token. The token
      must be an object returned from a previous call to :meth:`new_browser_session`
      or :meth:`switch_browser_session`.

      Returns a tuple (old_session_token, new_session_token).

   .. method:: submit(css_selector, wait_for_reload=True, auto_follow=True, window_closes=False)

      Submits a form via the button specified in ``css_selector``.

      For :class:`~django_functest.FuncSeleniumMixin`, ``wait_for_reload=True``
      causes it to wait until a whole new page is loaded (which always happens
      with :class:`~django_functest.FuncWebTestMixin`). If you are expecting an
      AJAX submission or Javascript code to stop a new page from actually
      being loaded, pass ``wait_for_reload=False``.

      For Selenium tests, if you are expecting the window to close, pass
      ``window_closes=False`` and then use
      :meth:`~django_functest.FuncSeleniumMixin.switch_window`, or you may
      experience long timeouts with Chrome. This implies
      ``wait_for_reload=False`` and other tweaks. It does nothing when running
      WebTest tests.

      For :class:`~django_functest.FuncWebTestMixin`, ``auto_follow=True``
      causes redirects to be followed automatically (which always happens with
      :class:`~django_functest.FuncSeleniumMixin`). Pass ``False`` to allow
      intermediate responses (i.e. 3XX redirect responses) to be inspected via
      :attr:`~django_functest.FuncWebTestMixin.last_response`.

   .. method:: value(css_selector)

      Returns the value of the form input specified in CSS selector.

      The types of the values correspond to those that are passed to :meth:`fill`:

      * For check boxes, it will return ``True`` or ``False``.
      * For text inputs, returns the text value.
      * For selects, returns the internal ``value`` attribute of the selected item.


.. class:: Upload

   .. method:: __init__(filename, content=data)

      Construct an object for uploading in a normal file upload field.
      ``filename`` is a string, and the ``content`` parameter must be a
      ``bytes`` instance.
