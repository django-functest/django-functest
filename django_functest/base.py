from __future__ import absolute_import, print_function, unicode_literals


class FuncBaseMixin(object):
    """
    Abstract base class that exists only to provide autocomplete help.
    """
    # Any docstrings added here also need to be added to
    # FuncSeleniumMixin/FuncWebTestMixin/CommonMixin.

    # In theory we could do this automatically using a decorator or something.
    # However, some code autocomplete tools such as Jedi do not import modules
    # to find docstrings, they do their own parsing. In this case the docstring
    # has to be on the overridden method itself to be found.

    def assertUrlsEqual(self, url, other_url=None):
        """
        Asserts that the URLs match. Empty protocol or domain are ignored.
        """
        raise NotImplementedError()

    def assertTextPresent(self, text):
        """
        Asserts that the text is present on the current page
        """
        raise NotImplementedError()

    def assertTextAbsent(self, text):
        """
        Asserts that the text is not present on the current page
        """
        raise NotImplementedError()

    def back(self):
        """
        Go back in the browser.
        """
        raise NotImplementedError()

    @property
    def current_url(self):
        """
        The current full URL
        """
        raise NotImplementedError()

    def follow_link(self, css_selector):
        """
        Follows the link specified in the CSS selector.
        """
        raise NotImplementedError()

    def fill(self, fields):
        """
        Fills form inputs using the values in fields, which is a dictionary
        of CSS selectors to values.
        """
        raise NotImplementedError()

    def fill_by_id(self, fields):
        """
        Same as ``fill`` except the keys are input IDs
        """
        raise NotImplementedError()

    def fill_by_name(self, fields):
        """
        Same as ``fill`` except the keys are input names
        """
        raise NotImplementedError()

    def fill_by_text(self, fields):
        """
        Same as ``fill`` except the values are text captions. Useful for ``select`` elements.
        """
        raise NotImplementedError()

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        raise NotImplementedError()

    def get_literal_url(self, url, auto_follow=None, expect_errors=None):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        raise NotImplementedError()

    def is_element_present(self, css_selector):
        """
        Returns True if the element specified by the CSS selector is present on the current page,
        False otherwise.
        """
        raise NotImplementedError()

    @property
    def is_full_browser_test(self):
        """
        True for Selenium tests, False for WebTest tests.
        """
        return NotImplemented

    def set_session_data(self, item_dict):
        """
        Set a dictionary of items directly into the Django session.
        """
        raise NotImplementedError()

    def get_session_data(self):
        """
        Returns the current Django session dictionary
        """

    def submit(self, css_selector, wait_for_reload=True, auto_follow=None, window_closes=False):
        """
        Submit the form using the input given in the CSS selector
        """
        raise NotImplementedError()

    def value(self, css_selector):
        """
        Returns the value of the form input specified in the CSS selector
        """
        raise NotImplementedError()
