from __future__ import absolute_import, print_function, unicode_literals

from importlib import import_module

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY as AUTH_BACKEND_SESSION_KEY
from django.contrib.auth import HASH_SESSION_KEY as AUTH_HASH_SESSION_KEY
from django.contrib.auth import SESSION_KEY as AUTH_ID_SESSION_KEY
from django.contrib.auth import authenticate
from furl import furl


class ShortcutLoginMixin(object):
    """
    A mixin that provides a fast way of logging in.
    """
    def shortcut_login(self, **credentials):
        user = authenticate(**credentials)
        if not user:
            raise ValueError("User {0} was not authenticated".format(user))

        session_auth_hash = ''
        if hasattr(user, 'get_session_auth_hash'):
            session_auth_hash = user.get_session_auth_hash()

        # Mimicking django.contrib.auth functionality
        self.set_session_data({AUTH_ID_SESSION_KEY: user.pk,
                               AUTH_HASH_SESSION_KEY: session_auth_hash,
                               AUTH_BACKEND_SESSION_KEY: user.backend})

    def shortcut_logout(self):
        self.set_session_data({AUTH_BACKEND_SESSION_KEY: ''})


def get_session_store(session_key=None):
    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore(session_key=session_key)
    if session_key is None:
        store.save()
    else:
        store.load()
    return store


class CommonMixin(object):

    def assertUrlsEqual(self, url, other_url=None):
        """
        Asserts that the URLs match. Empty protocol or domain are ignored.
        """
        if other_url is None:
            other_url = self.current_url
        url1 = furl(url)
        url2 = furl(other_url)
        self.assertEqual(url1.path, url2.path)
        self.assertEqual(url1.query, url2.query)
        if url1.netloc and url2.netloc:
            self.assertEqual(url1.netloc, url2.netloc)
        if url1.scheme and url2.scheme:
            self.assertEqual(url1.scheme, url2.scheme)

    def fill_by_id(self, data):
        """
        Same as ``fill`` except the keys are input IDs
        """
        self.fill({'#' + k: v for k, v in data.items()})

    def fill_by_name(self, fields, prefix=""):
        """
        Same as ``fill`` except the keys are input names
        """
        self.fill({'[name="%s%s"]' % (prefix, k): v for k, v in fields.items()})

    def get_session_data(self):
        """
        Returns the current Django session dictionary
        """
        return dict(self._get_session())


class AdminLoginMixin(ShortcutLoginMixin):
    """
    A mixin that logs in via the normal admin login page
    """
    def do_login(self, username=None, password=None, shortcut=True):
        if shortcut:
            self.shortcut_login(username=username, password=password)
            return

        self.get_url('admin:index')
        self.fill({'#id_username': username,
                   '#id_password': password,
                   })
        self.submit("input[type=submit]")

    def do_logout(self, shortcut=True):
        if shortcut:
            self.shortcut_logout()
            return

        self.get_url('admin:logout')
