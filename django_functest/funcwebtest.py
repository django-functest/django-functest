from __future__ import unicode_literals

import six
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django_webtest import WebTestMixin
from six import text_type
from six.moves import http_cookiejar

from .utils import CommonMixin, get_session_store


class FuncWebTestMixin(WebTestMixin, CommonMixin):

    # Public Common API
    is_full_browser_test = False

    @property
    def current_url(self):
        return self.last_response.request.url

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

    def assertTextPresent(self, text):
        self.assertIn(escape(text), self.last_response.content.decode('utf-8'))

    def assertTextAbsent(self, text):
        self.assertNotIn(escape(text), self.last_response.content.decode('utf-8'))

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
