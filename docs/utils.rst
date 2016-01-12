Utilities
=========

.. class:: django_functest.utils.ShortcutLoginMixin

   This provides a method for doing a login without actually doing HTTP calls,
   as far as possible.

   .. method:: shortcut_login(**credentials)

      Pass credentials (typically ``username`` and ``password``), as accepted by
      ``django.contrib.auth.authenticate``, and if they are valid, you will get
      a session where the user is logged in. Otherwise an exception is raised.
