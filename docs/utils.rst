Utilities
=========

.. currentmodule:: django_functest

.. class:: AdminLoginMixin

   This provides helpers for logging into the admin interface using the standard
   login page. It assumes logging in with username and password.

   This works with both ``FuncWebTestMixin`` and ``FuncSeleniumMixin``.

   .. method:: do_login(username=None, password=None, shortcut=True)

      Do an admin login for the provided username and password. However, it will
      actually do a shortcut by default, unless `shortcut=False` is passed,
      using the :meth:`~django_functest.ShortcutLoginMixin.shortcut_login`.

   .. method:: do_logout(shortcut=True)

      Do a log out for the current user, using
      :meth:`~django_functest.ShortcutLoginMixin.shortcut_logout` if
      ``shortcut=True`` (the default), or using the admin logout page if
      ``shortcut=False``

.. class:: ShortcutLoginMixin

   This provides a method for doing a login without actually doing HTTP-level work,
   as far as possible.

   This works with both ``FuncWebTestMixin`` and ``FuncSeleniumMixin``. These
   methods do *not* simulate exactly what happens when a user logs in and out
   with real HTTP requests — they only do enough to get you to "logged in user",
   or "logged out user" state. In particular, other side effects on the session
   that normally happen (such as session key rotation, or anything that
   responds to the ``user_logged_in`` signal etc.) will not be done.

   .. method:: shortcut_login(user=None, **credentials)

      Pass either a user object, or credentials.

      For a user object, you don’t need to provide a password or any
      authentication.

      For credentials, it will typically be ``username`` and ``password``, or
      anything else accepted by ``django.contrib.auth.authenticate``. If they
      are not valid, an exception is raised.

      Manipulates the session and cookies directly.

   .. method:: shortcut_logout()

      Logs out the user from the current session

      Manipulates the session and cookies directly.
