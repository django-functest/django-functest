from __future__ import unicode_literals

import pyquery
import six
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django_webtest import WebTestMixin
from six import text_type
from six.moves import http_cookiejar

from .exceptions import WebTestCantUseElement, WebTestMultipleElementsException, WebTestNoSuchElementException
from .utils import CommonMixin, get_session_store


class FuncWebTestMixin(WebTestMixin, CommonMixin):

    # Public Common API
    is_full_browser_test = False

    def assertTextAbsent(self, text):
        self.assertNotIn(escape(text), self.last_response.content.decode('utf-8'))

    def assertTextPresent(self, text):
        self.assertIn(escape(text), self.last_response.content.decode('utf-8'))

    @property
    def current_url(self):
        return self.last_response.request.url

    def fill(self, data):
        for selector, value in data.items():
            form, field_name = self._find_form_and_field_by_css_selector(self.last_response, selector)
            form[field_name] = value

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        return self.get_literal_url(reverse(name, args=args, kwargs=kwargs))

    def get_literal_url(self, url):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        return self._get_url_raw(url)

    def is_element_present(self, css_selector):
        return len(self._make_pq(self.last_response).find(css_selector)) > 0

    def submit(self, css_selector, wait_for_reload=None, auto_follow=True):
        form, field_name = self._find_form_and_field_by_css_selector(self.last_response,
                                                                     css_selector,
                                                                     require_name=False,
                                                                     filter_selector="input[type=submit], button")
        response = form.submit(field_name)
        self.last_response = response
        if auto_follow:
            while 300 <= response.status_int < 400:
                response = response.follow()
        self.last_response = response

    # Implementation methods - private

    def add_cookie(self, cookie_dict):
        # Same API as for SeleniumTest

        # We don't use self.app.set_cookie since it has undesirable behaviour
        # with domain and value fields that causes issues.
        value = cookie_dict['value']
        if six.PY2:
            value = value.encode('utf-8')

        cookie = http_cookiejar.Cookie(
            version=0,
            name=cookie_dict['name'],
            value=value,
            port=None,
            port_specified=False,
            domain='localhost.local',
            domain_specified=True,
            domain_initial_dot=False,
            path='/',
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
        )
        self.app.cookiejar.set_cookie(cookie)

    def set_session_vars(self, item_dict):
        session = self.get_session()
        for name, value in item_dict.items():
            session[name] = text_type(value)
        session.save()

    def get_session(self):
        session_key = self.app.cookies.get(settings.SESSION_COOKIE_NAME, None)
        if session_key is None:
            # Create new
            session = get_session_store()
            self.add_cookie({'name': settings.SESSION_COOKIE_NAME,
                             'value': session.session_key})
        else:
            session = get_session_store(session_key=session_key)
        return session

    def _get_url_raw(self, url, auto_follow=True, expect_errors=False):
        """
        'raw' method for getting URL - not compatible between FullBrowserTest and WebTestBase
        """
        self.last_response = self.app.get(url, auto_follow=auto_follow, expect_errors=expect_errors)
        return self.last_response

    def _find_form_and_field_by_css_selector(self, response, css_selector, filter_selector=None,
                                             require_name=True):
        pq = self._make_pq(response)
        items = pq.find(css_selector)

        found = []
        if filter_selector:
            items = items.filter(filter_selector)
        for item in items:
            form_elem = self._find_parent_form(item)
            if form_elem is None:
                raise WebTestCantUseElement("Can't find form for input {0}.".format(css_selector))
            form = self._match_form_elem_to_webtest_form(form_elem, response)
            field = item.name
            if field is None and require_name:
                raise WebTestCantUseElement(
                    "Element {0} needs 'name' attribute in order to use it".format(css_selector))
            found.append((form, field))

        if len(found) == 1:
            return found[0]

        if len(found) > 1:
            raise WebTestMultipleElementsException(
                "Multiple elements found matching '{0}'".format(css_selector))

        raise WebTestNoSuchElementException(
            "Can't find element matching {0} in response {1}.".format(css_selector, response))

    def _find_parent_form(self, elem):
        p = elem.getparent()
        if p is None:
            return None
        if p.tag == 'form':
            return p
        return self._find_parent_form(p)

    def _match_form_elem_to_webtest_form(self, form_elem, response):
        pq = self._make_pq(response)
        forms = pq('form')
        form_index = forms.index(form_elem)
        webtest_form = response.forms[form_index]
        form_sig = {'action': form_elem.attrib.get('action', ''),
                    'id': form_elem.attrib.get('id', ''),
                    'method': form_elem.attrib.get('method', '').lower(),
                    }
        webtest_sig = {
            'action': getattr(webtest_form, 'action', ''),
            'id': getattr(webtest_form, 'id', ''),
            'method': getattr(webtest_form, 'method', '').lower(),
        }
        webtest_sig = {k: v if v is not None else '' for k, v in webtest_sig.items()}
        assert form_sig == webtest_sig
        return webtest_form

    def _make_pq(self, response):
        # Cache to save parsing every time
        if not hasattr(self, '_pq_cache'):
            self._pq_cache = {}
        if response in self._pq_cache:
            return self._pq_cache[response]
        pq = pyquery.PyQuery(response.content)
        self._pq_cache[response] = pq
        return pq
