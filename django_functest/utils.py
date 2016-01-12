from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY as AUTH_BACKEND_SESSION_KEY
from django.contrib.auth import SESSION_KEY as AUTH_ID_SESSION_KEY
from django.contrib.auth import authenticate


class ShortcutLoginMixin(object):
    def shortcut_login(self, **credentials):
        user = authenticate(**credentials)
        if not user:
            raise ValueError("User {0} was not authenticated".format(user))

        self.set_session_vars(
            {AUTH_ID_SESSION_KEY: user.pk,
             AUTH_BACKEND_SESSION_KEY: user.backend})


def get_session_store(session_key=None):
    from django.utils.importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore(session_key=session_key)
    if session_key is None:
        store.save()
    else:
        store.load()
    return store
