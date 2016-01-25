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

.. class:: django_functest.FuncCommonApi

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
      selectors, and the values and the values for the inputs. Works for text
      inputs, radio boxes, check boxes, and select fields. Checkbox values can
      be specified using ``True`` and ``False``.

      This will raise an exception if the fields can't be found. It will be a
      timeout exception for Selenium tests, so you will want to avoid attempting
      to fill in fields that don't exist.

      If multiple fields match, you will get an exception for
      :class:`django_functest.FuncWebTestMixin` but not for
      :class:`django_functest.FuncSeleniumMixin` due to the way Selenium finds
      elements.

   .. method:: fill_by_id(data_dict)

      Same as :meth:`fill` except the keys are element IDs.

   .. method:: fill_by_name(data_dict)

      Same as :meth:`fill` except the keys are input names.

   .. method:: fill_by_text(data_dict)

      Same as :meth:`fill`, except the values are text captions. This can be
      used only for ``select`` elements.

   .. method:: get_url(name, *args, **kwargs)

      Gets the named URL, passing it through ``django.core.urlresolvers.reverse`` with ``*args`` and ``**kwargs``.

      e.g.::

        self.get_url('admin:auth_user_change', object_id=1)

   .. method:: get_literal_url(relative_url)

      Gets the URL given by the relative URL passed in.

   .. method:: is_element_present(css_selector)

      Returns ``True`` if the element specified by the CSS selector is present, ``False`` otherwise.
      See also :meth:`~django_functest.FuncSeleniumMixin.is_element_displayed`.

   .. attribute:: is_full_browser_test

      True for Selenium tests, False for WebTest tests.

   .. method:: submit(css_selector, wait_for_reload=True, auto_follow=True)

      Submits a form via the button specified in ``css_selector``.

      For :class:`~django_functest.FuncSeleniumMixin`, ``wait_for_reload=True``
      causes it to wait until a whole new page is loaded (which always happens
      with :class:`~django_functest.FuncWebTestMixin`). If you are expecting an AJAX
      submission, or a Javascript error to stop a new page from actually being
      loaded, pass ``wait_for_reload=False``.

      For :class:`~django_functest.FuncWebTestMixin`, ``auto_follow=True`` causes
      redirects to be followed automatically (which always happens with
      :class:`~django_functest.FuncSeleniumMixin`).

   .. method:: value(css_selector)

      Returns the value of the form input specified in CSS selector.

      The types of the values correspond to those that are passed to :meth:`fill`:

      * For check boxes, it will return ``True`` or ``False``.
      * For text inputs, returns the text value.
      * For selects, returns the internal ``value`` attribute of the selected item.
