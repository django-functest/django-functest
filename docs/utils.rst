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

   .. method:: shortcut_login(**credentials)

      Pass credentials (typically ``username`` and ``password``), as accepted by
      ``django.contrib.auth.authenticate``, and if they are valid, you will get
      a session where the user is logged in. Otherwise an exception is raised.

      Manipulates the session and cookies directly.

   .. method:: shortcut_logout()

      Logs out the user from the current session

      Manipulates the session and cookies directly.


.. class:: MultiThreadedLiveServerMixin

      Add this as a mixin to any test class (or test class base) to enable
      a multi-threaded live server. This is only needed for Django < 2.0
      and on Django 2.0 and greater it does nothing because the test server
      has the required behaviour built in.

      This mixin it possible to use some browsers (e.g. Chrome) in combination
      with test methods like
      :meth:`~django_functest.FuncCommonApi.new_browser_session`.

      Note that there are some limitations:

      * You cannot use this with an in-memory SQLite test database. You will
        need to set a NAME parameter for `the test database
        <https://docs.djangoproject.com/en/1.10/topics/testing/overview/#the-test-database>`_
        to force it to be a non-in-memory database.
