import warnings
from importlib import import_module

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY as AUTH_BACKEND_SESSION_KEY
from django.contrib.auth import HASH_SESSION_KEY as AUTH_HASH_SESSION_KEY
from django.contrib.auth import SESSION_KEY as AUTH_ID_SESSION_KEY
from django.contrib.auth import authenticate
from django.utils.html import escape
from furl import furl
from lxml import etree


class _NotPassed:
    pass


NotPassed = _NotPassed()


class ShortcutLoginMixin:
    """
    A mixin that provides a fast way of logging in and out.
    """

    def shortcut_login(self, user=None, **credentials):
        """
        Login a user directly. Pass the user object, without a password,
        or pass in credentials like: username="me", password="my_password"
        """
        if user is not None:
            if credentials:
                raise AssertionError("Either pass 'user' or **credentials, not both")

            def get_backend():
                from django.contrib.auth import load_backend

                for backend_path in settings.AUTHENTICATION_BACKENDS:
                    backend = load_backend(backend_path)
                    if hasattr(backend, "get_user"):
                        return backend_path

            user.backend = get_backend()
        else:
            user = authenticate(**credentials)
            if not user:
                raise ValueError(f"User {user} was not authenticated")

        session_auth_hash = ""
        if hasattr(user, "get_session_auth_hash"):
            session_auth_hash = user.get_session_auth_hash()

        # Mimicking django.contrib.auth functionality
        self.set_session_data(
            {
                AUTH_ID_SESSION_KEY: user.pk,
                AUTH_HASH_SESSION_KEY: session_auth_hash,
                AUTH_BACKEND_SESSION_KEY: user.backend,
            }
        )

    def shortcut_logout(self):
        self.flush_session()


def get_session_store(session_key=None):
    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore(session_key=session_key)
    if session_key is None:
        store.save()
    else:
        store.load()
    return store


class CommonMixin:
    def assertion_passes(self, a_callable, *args, **kwargs):
        """
        Given a callable which may raise an AssertionError, plus optional arguments to pass
        to it,  returns a callable that wraps it and returns True if no AssertionError
        is raised, False otherwise.

        Useful for converting assertion methods into callables that can be passed
        to `wait_until`.
        """

        # We make wrapper accept and ignore any args due to the use case, where
        # typically `driver` will be passed as an argument (see `wait_until`)
        def wrapper(*wrapper_args, **wrapper_kwargs):
            try:
                a_callable(*args, **kwargs)
            except AssertionError:
                return False
            return True

        return wrapper

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
        warnings.warn(
            "instead of `fill_by_id({'foo': 'bar'})` do `fill({'#foo': 'bar'})`",
            DeprecationWarning,
        )
        self.fill({"#" + k: v for k, v in data.items()})

    def fill_by_name(self, fields, prefix="", scroll=NotPassed):
        """
        Same as ``fill`` except the keys are input names
        """
        self.fill({f'[name="{prefix}{k}"]': v for k, v in fields.items()}, scroll=scroll)

    def _assertTextPresent(self, text, pyquery_obj, within):
        norm_text = html_norm(escape(text))
        matching_elements = pyquery_obj.find(within)
        if len(matching_elements) == 0:
            self.fail(f"No elements matched the CSS selector {within!r}")
        elif len(matching_elements) == 1:
            # Better error message for the common case:
            self.assertIn(
                norm_text,
                etree.tostring(matching_elements[0], encoding="unicode"),
            )
        else:
            self.assertTrue(
                any(norm_text in etree.tostring(elem, encoding="unicode") for elem in matching_elements),
                "Didn't find {!r} inside any of the {} matching elements for {!r}".format(
                    text, len(matching_elements), within
                ),
            )

    def _assertTextAbsent(self, text, pyquery_obj, within):
        norm_text = html_norm(escape(text))
        matching_elements = pyquery_obj.find(within)
        if len(matching_elements) == 1:
            # Better error message for the common case:
            self.assertNotIn(
                norm_text,
                etree.tostring(matching_elements[0], encoding="unicode"),
            )
        else:
            self.assertFalse(
                any(norm_text in etree.tostring(elem, encoding="unicode") for elem in matching_elements),
                "Didn't find {!r} inside any of the {} matching_elements for {!r}".format(
                    text,
                    len(matching_elements),
                    within,
                ),
            )


class AdminLoginMixin(ShortcutLoginMixin):
    """
    A mixin that logs in via the normal admin login page
    """

    def do_login(self, username=None, password=None, shortcut=True):
        if shortcut:
            self.shortcut_login(username=username, password=password)
            return

        self.get_url("admin:index")
        self.fill(
            {
                "#id_username": username,
                "#id_password": password,
            }
        )
        self.submit("input[type=submit]")

    def do_logout(self, shortcut=True):
        if shortcut:
            self.shortcut_logout()
            return

        self.get_url("admin:logout")


class BrowserSessionToken:
    # Simple container class to hide the fact that the value is really a
    # webdriver instance or webtest instance (but that may change in future)
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"<BrowserSessionToken {id(self.value)}>"


def html_norm(html):
    return html.replace("&quot;", '"').replace("&apos;", "'").replace("&#39;", "'").replace("&#x27;", "'")
