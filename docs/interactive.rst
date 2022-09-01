Writing tests interactively with a browser
==========================================

Since your website is going to be used interactively, it can be helpful to write
your tests in a similar way to how a user views the website, rather than doing
it “blind”. This page outlines a method for doing that.

You can also view the content of this page `as a video <https://www.youtube.com/watch?v=nEr6T2pL8Es>`_:

.. raw:: html

   <div style="display: flex; align-items: center; justify-content: center;">
     <iframe width="560" height="315"
     src="https://www.youtube.com/embed/nEr6T2pL8Es" title="YouTube video
     player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;
     encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>


A complete example project for the setup can be found in the `examples folder
<https://github.com/django-functest/django-functest/tree/master/examples/example_project>`_.

We are going to use pytest and pytest-django, and use all the :doc:`pytest`
tips, including the ``--show-browser`` option.

The essential technique is:

* use `REPL programming with IPython
  <https://lukeplant.me.uk/blog/posts/repl-python-programming-and-debugging-with-ipython/>`_.
* ensure the browser window is visible.

Using the example from the project, we’ve got a custom user class, and we’re
going to test that the admin interface has been registered and still works.

We start with a test that looks like this:

.. code-block:: python

   from django_functest import FuncBaseMixin, ShortcutLoginMixin

   from .base import SeleniumTestBase, WebTestBase
   from .factories import create_user


   class UserAdminBase(FuncBaseMixin, ShortcutLoginMixin):
       def test_change_details(self):
           pass


   class UserAdminWT(UserAdminBase, WebTestBase):
       pass


   class UserAdminSL(UserAdminBase, SeleniumTestBase):
       pass


The code here is just following the pattern from the guide, plus two things:

* Adding the ``ShortcutLoginMixin``
* Importing a little custom utility function for creating users.

We now add our IPython prompt code into the base class method, so it looks like this:


.. code-block:: python

   def test_change_details(self):
        import IPython; IPython.embed()



Next, we are going to run the Selenium version of this test, with the browser
window visible. Since I’ve only got one test so far, we can select it like this,
using the ``selenium`` marker:

.. code-block:: shell

   pytest accounts/tests/test_admin.py -m selenium --show-browser -s


Notice the use of ``-s`` to ensure that pytest doesn’t capture our input, which
would break IPython.

This will run the test, and we’ll find ourselves at an IPython prompt with a
browser window open.

We can then interactively write the test into IPython a line at a time, and
watch our commands being executed. We’ll probably start something like this:

.. code-block:: python

   user = create_user(is_superuser=True)
   self.shortcut_login(user)
   self.get_url("admin:accounts_user_changelist")

We can then use “Inspect” and web browser dev tools to work out what elements to
refer to and interact with. We might continue like this:


.. code-block:: python

   self.follow_link("#result_list tbody a")
   self.fill({"#id_first_name": "Joe", "#id_last_name": "Bloggs"})
   self.submit('input[value="Save"]')

We can also do our asserts:

.. code-block:: python

   user.refresh_from_db()
   assert user.first_name == "Joe"

If we found that some of our setup code was actually wrong, or we missed
something, there is no need to restart — just fix it by executing commands
interactively and carry on.

Finally, we can copy back code from the terminal into our editor. You can use
the history functionality in IPython (PageUp and PageDown) to look back through
everything you typed. Use ``Ctrl-D`` to exit from IPython and allow pytest to
finish.

In our editor, we’ll probably want to clean it up, and once done, we can run the
tests again. This time, we’ll want to run both the WebTest and Selenium
versions:

.. code-block:: shell

   pytest accounts/tests/test_admin.py -v


.. raw:: html

   <style type="text/css">
   .ansi2html-content { display: inline; white-space: pre-wrap; word-wrap: break-word; border: 0; font-size: 75%;}

   .body_foreground { color: #AAAAAA; }
   .body_background { background-color: #000000; }
   .inv_foreground { color: #000000; }
   .inv_background { background-color: #AAAAAA; }
   .ansi1 { font-weight: bold; }
   .ansi32 { color: #00aa00; }
   </style>
   <pre class="ansi2html-content">
   <span class="ansi1">============================= test session starts ==============================</span>
   platform linux -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0 -- /home/luke/.virtualenvs/django-functest-example/bin/python
   cachedir: .pytest_cache
   django: settings: example_project.settings (from ini)
   rootdir: /home/luke/devel/django-functest/examples/example_project, configfile: pytest.ini
   plugins: django-4.5.2, django-webtest-1.9.10
   <span class="ansi1">collecting ... </span>collected 2 items

   accounts/tests/test_admin.py::UserAdminWT::test_change_own_details  <span class="ansi32">PASSED</span><span class="ansi32"> [ 50%]</span>
   accounts/tests/test_admin.py::UserAdminSL::test_change_own_details  <span class="ansi32">PASSED</span><span class="ansi32"> [100%]</span>

   <span class="ansi32">=============================== </span><span class="ansi32"></span><span class="ansi1 ansi32">2 passed</span><span class="ansi32"> in 1.87s</span><span class="ansi32"> ===============================</span>

   </pre>


If we get any failures, we can also use the IPython prompt technique to debug
easily, by insert the “embed” line just before the failing line of code.

Hopefully you’ll enjoy this method of writing tests! If you’ve got any more
tips for improving this method, do let us know.
