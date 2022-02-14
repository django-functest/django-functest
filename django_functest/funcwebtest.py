import urllib
from collections import defaultdict

from django.conf import settings
from django.utils.html import escape
from django_webtest import WebTestMixin
from webtest.forms import Checkbox

from .base import FuncBaseMixin
from .exceptions import WebTestCantUseElement, WebTestMultipleElementsException, WebTestNoSuchElementException
from .utils import BrowserSessionToken, CommonMixin, get_session_store

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


def html_norm(html):
    return html.replace("&quot;", '"').replace("&apos;", "'").replace("&#39;", "'").replace("&#x27;", "'")


class FuncWebTestMixin(WebTestMixin, CommonMixin, FuncBaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._all_last_responses = defaultdict(list)
        self._all_apps = []

    # Public Common API
    def assertTextAbsent(self, text):
        """
        Asserts that the text is not present on the current page
        """
        self.assertNotIn(
            html_norm(escape(text)),
            html_norm(self.last_response.content.decode("utf-8")),
        )

    def assertTextPresent(self, text):
        """
        Asserts that the text is present on the current page
        """
        self.assertIn(
            html_norm(escape(text)),
            html_norm(self.last_response.content.decode("utf-8")),
        )

    def back(self):
        """
        Go back in the browser.
        """
        self.last_responses.pop()

    @property
    def current_url(self):
        """
        The current full URL
        """
        return self.last_response.request.url

    def follow_link(self, css_selector):
        """
        Follows the link specified in the CSS selector.
        """
        elems = self._make_pq(self.last_response).find(css_selector)
        if len(elems) == 0:
            raise WebTestNoSuchElementException(f"Can't find element matching '{css_selector}'")

        hrefs = []
        for e in elems:
            if "href" in e.attrib:
                hrefs.append(e.attrib["href"])

        if not hrefs:
            raise WebTestCantUseElement(f"No href attribute found for '{css_selector}'")

        if not all(h == hrefs[0] for h in hrefs):
            raise WebTestMultipleElementsException(
                f"Different href values for links '{css_selector}': '{' ,'.join(hrefs)}'"
            )
        final_url = urllib.parse.urljoin(self.current_url, hrefs[0])
        self.get_literal_url(final_url)

    def fill(self, data):
        """
        Fills form inputs using the values in fields, which is a dictionary
        of CSS selectors to values.
        """
        for selector, value in data.items():
            form, field_name, elem = self._find_form_and_field_by_css_selector(self.last_response, selector)
            field_items = form.fields[field_name]
            if isinstance(field_items, list) and len(field_items) > 1:
                # We've got something like a set of checkboxes with the same name.
                selected_value = elem.attrib["value"]
                for checkbox in field_items:
                    if checkbox._value == selected_value:
                        checkbox.checked = value
            else:
                form[field_name] = value

    def fill_by_text(self, fields):
        """
        Same as ``fill`` except the values are text captions. Useful for ``select`` elements.
        """
        for selector, text in fields.items():
            form, field_name, _ = self._find_form_and_field_by_css_selector(self.last_response, selector)
            self._fill_field_by_text(form, field_name, text)

    def get_element_attribute(self, css_selector, attribute):
        """
        Returns the value of the attribute of the element matching the css_selector,
        or None if there is no such element or attribute.
        """
        elems = self._make_pq(self.last_response).find(css_selector)
        if len(elems) == 0:
            return None
        if len(elems) > 1:
            raise WebTestMultipleElementsException(f"Multiple elements found matching '{css_selector}'")
        return elems[0].attrib.get(attribute, None)

    def get_element_inner_text(self, css_selector):
        """
        Returns the "inner text" (innerText in JS) of the element matching
        the css_selector, or None if there is none.
        """
        elems = self._make_pq(self.last_response).find(css_selector)
        if len(elems) == 0:
            return None
        if len(elems) > 1:
            raise WebTestMultipleElementsException(f"Multiple elements found matching '{css_selector}'")
        return inner_text(elems[0])

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        return self.get_literal_url(reverse(name, args=args, kwargs=kwargs))

    def get_literal_url(self, url, auto_follow=True, expect_errors=False):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        return self._get_url_raw(url, auto_follow=auto_follow, expect_errors=expect_errors)

    def is_element_present(self, css_selector):
        """
        Returns True if the element specified by the CSS selector is present on the current page,
        False otherwise.
        """
        return len(self._make_pq(self.last_response).find(css_selector)) > 0

    @property
    def is_full_browser_test(self):
        """
        True for Selenium tests, False for WebTest tests.
        """
        return False

    def set_session_data(self, item_dict):
        """
        Set a dictionary of items directly into the Django session.
        """
        session = self._get_session()
        for name, value in item_dict.items():
            session[name] = str(value)
        session.save()
        self._update_session_cookie(session)  # Required for signed_cookie backend

    def new_browser_session(self):
        """
        Creates (and switches to) a new session that is separate from previous
        sessions. Returns a tuple (old_session_token, new_session_token). These
        values should be treated as opaque tokens that can be used with
        switch_browser_session.
        """
        # WebTestMixin creates the instance as 'self.app', so we just just move
        # that value around.
        last_app = self.app
        self.renew_app()
        return (BrowserSessionToken(last_app), BrowserSessionToken(self.app))

    def switch_browser_session(self, session_token):
        """
        Switch to the browser session indicated by the supplied token.
        Returns a tuple (old_session_token, new_session_token).
        """
        last_app = self.app
        self.app = session_token.value
        return (BrowserSessionToken(last_app), BrowserSessionToken(self.app))

    def submit(self, css_selector, wait_for_reload=None, auto_follow=True, window_closes=None):
        """
        Submit the form using the input given in the CSS selector
        """
        form, field_name, _ = self._find_form_and_field_by_css_selector(
            self.last_response,
            css_selector,
            require_name=False,
            filter_selector="input[type=submit], button",
        )
        response = form.submit(field_name)
        if auto_follow:
            while 300 <= response.status_int < 400:
                response = response.follow()
        self.last_responses.append(response)

    def value(self, css_selector):
        """
        Returns the value of the form input specified in the CSS selector
        """
        form, field_name, _ = self._find_form_and_field_by_css_selector(
            self.last_response, css_selector, require_name=False
        )
        field = form[field_name]
        if isinstance(field, Checkbox):
            return field.checked
        else:
            return field.value

    # WebTest specific

    @property
    def last_response(self):
        """
        Returns the last WebTest response received.
        """
        return self.last_responses[-1]

    # Implementation methods - private
    @property
    def last_responses(self):
        return self._all_last_responses[self.app]

    def _set_cookie(self, name, value):
        self.app.set_cookie(name, value)

    def _get_session(self):
        session_key = self.app.cookies.get(settings.SESSION_COOKIE_NAME, None)
        if session_key is None:
            # Create new
            session = get_session_store()
            self._update_session_cookie(session)
        else:
            session_key = session_key.strip('"')
            session = get_session_store(session_key=session_key)
        return session

    def _update_session_cookie(self, session):
        self._set_cookie(settings.SESSION_COOKIE_NAME, session.session_key)

    def _get_url_raw(self, url, auto_follow=True, expect_errors=False):
        """
        'raw' method for getting URL - not compatible between FullBrowserTest and WebTestBase
        """
        self.last_responses.append(self.app.get(url, auto_follow=auto_follow, expect_errors=expect_errors))
        return self.last_response

    def _find_form_and_field_by_css_selector(self, response, css_selector, filter_selector=None, require_name=True):
        pq = self._make_pq(response)
        items = pq.find(css_selector)

        found = []
        if filter_selector:
            items = items.filter(filter_selector)
        for item in items:
            form_elem = self._find_parent_form(item)
            if form_elem is None:
                raise WebTestCantUseElement(f"Can't find form for input {css_selector}.")
            form = self._match_form_elem_to_webtest_form(form_elem, response)
            field = item.name if hasattr(item, "name") else item.attrib.get("name", None)
            if field is None and require_name:
                raise WebTestCantUseElement(f"Element {css_selector} needs 'name' attribute in order to use it")
            found.append((form, field, item))

        if len(found) > 1:
            if not all(f[0:2] == found[0][0:2] for f in found):
                raise WebTestMultipleElementsException(f"Multiple elements found matching '{css_selector}'")

        if len(found) > 0:
            return found[0]

        raise WebTestNoSuchElementException(f"Can't find element matching {css_selector} in response {response}.")

    def _find_parent_form(self, elem):
        p = elem.getparent()
        if p is None:
            return None
        if p.tag == "form":
            return p
        return self._find_parent_form(p)

    def _fill_field_by_text(self, form, field_name, text):
        field = form[field_name]
        if field.tag == "select":
            for val, _, t in field.options:
                if t == text:
                    form[field_name] = val
                    break
            else:
                raise ValueError(f"No option matched '{text}'")
        else:
            raise WebTestCantUseElement(f"Don't know how to 'fill_by_text' for elements of type '{field.tag}'")

    def _match_form_elem_to_webtest_form(self, form_elem, response):
        pq = self._make_pq(response)
        forms = pq("form")
        form_index = forms.index(form_elem)
        webtest_form = response.forms[form_index]
        form_sig = {
            "action": form_elem.attrib.get("action", ""),
            "id": form_elem.attrib.get("id", ""),
            "method": form_elem.attrib.get("method", "").lower(),
        }
        webtest_sig = {
            "action": getattr(webtest_form, "action", ""),
            "id": getattr(webtest_form, "id", ""),
            "method": getattr(webtest_form, "method", "").lower(),
        }
        webtest_sig = {k: v if v is not None else "" for k, v in webtest_sig.items()}
        assert form_sig == webtest_sig
        return webtest_form

    def _make_pq(self, response):
        # Cache to save parsing every time
        if not hasattr(self, "_pq_cache"):
            self._pq_cache = {}
        if response in self._pq_cache:
            return self._pq_cache[response]
        pq = response.pyquery
        self._pq_cache[response] = pq
        return pq


def inner_text(elem, root=True):
    return (elem.text or "") + "".join(inner_text(e, root=False) for e in elem) + ("" if root else (elem.tail or ""))
