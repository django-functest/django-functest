Utilities
=========

.. class:: django_functest.AdminLoginMixin

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

.. class:: django_functest.ShortcutLoginMixin

   This provides a method for doing a login without actually doing HTTP-level work,
   as far as possible.

   This works with both ``FuncWebTestMixin`` and ``FuncSeleniumMixin``.

   .. method:: shortcut_login(**credentials)

      Pass credentials (typically ``username`` and ``password``), as accepted by
      ``django.contrib.auth.authenticate``, and if they are valid, you will get
      a session where the user is logged in. Otherwise an exception is raised.

      Manipulates the session and cookies directly.

   .. method:: shortcut_logout()

      Logs out the user from the current session

      Manipulates the session and cookies directly.
