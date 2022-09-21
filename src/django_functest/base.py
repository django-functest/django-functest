from .utils import NotPassed


class FuncBaseMixin:
    """
    Abstract base class that exists only to provide autocomplete help.
    """

    # Any docstrings added here also need to be added to
    # FuncSeleniumMixin/FuncWebTestMixin/CommonMixin.

    # In theory we could do this automatically using a decorator or something.
    # However, some code autocomplete tools such as Jedi do not import modules
    # to find docstrings, they do their own parsing. In this case the docstring
    # has to be on the overridden method itself to be found.
    def assertion_passes(self, a_callable, *args, **kwargs):
        """
        Given a callable which may raise an AssertionError, plus optional arguments to pass
        to it,  returns a callable that wraps it and returns True if no AssertionError
        is raised, False otherwise.

        Useful for converting assertion methods into callables that can be passed
        to `wait_until`.
        """
        raise NotImplementedError()

    def assertUrlsEqual(self, url, other_url=None):
        """
        Asserts that the URLs match. Empty protocol or domain are ignored.
        """
        raise NotImplementedError()

    def assertTextPresent(self, text, within="body", wait=True):
        """
        Asserts that the text is present within the body of the current page,
        or within an element matching the CSS selector passed as `within`.
        """
        raise NotImplementedError()

    def assertTextAbsent(self, text, within="body"):
        """
        Asserts that the text is not present within the body of the current page,
        or within any element matching the CSS selector passed as `within`.
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

    def fill(self, fields, scroll=NotPassed):
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

    def fill_by_name(self, fields, scroll=NotPassed):
        """
        Same as ``fill`` except the keys are input names
        """
        raise NotImplementedError()

    def fill_by_text(self, fields, scroll=NotPassed):
        """
        Same as ``fill`` except the values are text captions. Useful for ``select`` elements.
        """
        raise NotImplementedError()

    def get_element_attribute(self, css_selector, attribute):
        """
        Returns the value of the attribute of the element matching the css_selector,
        or None if there is no such element or attribute.
        """
        raise NotImplementedError()

    def get_element_inner_text(self, css_selector):
        """
        Returns the "inner text" (innerText in JS) of the element matching
        the css_selector, or None if there is none.
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
        raise NotImplementedError()

    def new_browser_session(self):
        """
        Creates (and switches to) a new session that is separate from previous
        sessions. Returns a tuple (old_session_token, new_session_token). These
        values should be treated as opaque tokens that can be used with
        switch_browser_session.
        """
        raise NotImplementedError()

    def switch_browser_session(self, session_token):
        """
        Switch to the browser session indicated by the supplied token.
        Returns a tuple (old_session_token, new_session_token).
        """
        raise NotImplementedError()

    def submit(self, css_selector, wait_for_reload=True, auto_follow=None, window_closes=False, scroll=NotPassed):
        """
        Submit the form. css_selector should refer to a form, or a button/input to use
        to submit the form.
        """
        raise NotImplementedError()

    def value(self, css_selector):
        """
        Returns the value of the form input specified in the CSS selector
        """
        raise NotImplementedError()
