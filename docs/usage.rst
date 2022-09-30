=====
Usage
=====


    Exploring django-functest makes me angry! Why? Because I've wasted so much
    time writing low-level, boilerplate-filled tests for the past few years
    instead of using it —
    `jerivas <https://github.com/stephenmcd/mezzanine/issues/1012#issuecomment-666802439>`_


There are two main ideas behind django-functest:

1. Write functional tests for Django apps using a high level API.

   If you are using Selenium, you might see things like::

       self.driver.get(self.live_server_url + reverse("contact_form"))
       self.driver.find_element_by_css_selector('#id_email').send_keys('my@email.com')
       self.driver.find_element_by_css_selector('#id_message').send_keys('Hello')
       self.driver.find_element_by_css_selector('input[type=submit]').click()
       WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_css_selector('body'))

   With `django-webtest <https://pypi.python.org/pypi/django-webtest>`_, it might look like::

       response = self.app.get(reverse("contact_form"))
       form = response.form
       form["email"] = "my@email.com"
       form["message"] = "Hello"
       response2 = form.submit().follow()

   Both of these are verbose, and much lower-level than you would like to write
   for testing a Django web app. (Tests that use `Django test client
   <https://docs.djangoproject.com/en/dev/topics/testing/tools/#the-test-client>`_
   are even worse, and additionally do a really bad job of modelling what
   happens when a user interacts with a web page.)

   With django-functest, the lower-level details are hidden, and instead you
   would write::

       self.get_url("contact_form")
       self.fill(
           {
               "#id_email": "my@email.com",
               "#id_message": "Hello",
           }
       )
       self.submit("input[type=submit]")


2. Write two sets of tests at once, by using an API that is unified as well as high level.

   For many web sites, you need them to work without Javascript, as well as
   having some Javascript functionality to enhance. This is good practice where
   possible, and it also means that you can write fast functional tests -
   Selenium tests are often hundreds of times slower than tests that simply use
   HTTP.

   django-functest provides wrappers for WebTest and Selenium that use the
   **same** API. This means you can write a test targeting both, and run in two
   different ways.

   The fast WebTest tests can be used when you need to iterate quickly, because
   WebTest operates at the WSGI level (without a separate web server process),
   and doesn’t load or use all the extra sutff (CSS, Javascript etc.) that makes
   a real web browser much slower and more complicated. But you can still run
   the same tests against a full browser.


In addition, django-functest provides various helps to smooth things along:

* :meth:`~django_functest.FuncCommonApi.get_url` has Django URL reversing
  built-in, covering the common case.

* short-cuts for putting things into the session so that you can skip steps.

* For both Selenium and WebTest helpers, there are additional methods. For
  example, there is :meth:`~django_functest.FuncSeleniumMixin.click`, which does
  element clicking in a browser, but takes care of many details like scrolling
  elements into view, using battle-hardened strategies.


Getting started
===============

It is recommended for both Selenium and WebTest, you should create your own base
classes. These can have :ref:`configuration <selenium-configuration>`, helpers
and functionality that are specific to your project as needed:


``yourproject.tests.base``:

.. code-block:: python

   from django.test import TestCase
   from django.contrib.staticfiles.testing import StaticLiveServerTestCase
   from django_functest import FuncSeleniumMixin, FuncWebTestMixin

   class WebTestBase(FuncWebTestMixin, TestCase):
       def setUp(self):
           super(WebTestBase, self).setUp()  # Remember to call this!
           # Your custom stuff here etc.

   class SeleniumTestBase(FuncSeleniumMixin, StaticLiveServerTestCase):
       driver_name = "Firefox"


Normally ``StaticLiveServerTestCase`` will be better than
``LiveServerTestCase``.

django-functest deliberately does not provide the base classes as above, only
the mixins, to make life easier especially in the case where you already have
another base class you want to inherit from (for example, if you have custom
needs instead of using ``StaticLiveServerTestCase``).

Then:

``yourapp.tests``::

    from yourproject.tests.base import SeleniumTestBase, WebTestBase
    from django_functest import FuncBaseMixin


    class ContactFormTestBase(FuncBaseMixin):
        def test_contact_form(self):
            self.get_url("contact_form")
            self.fill({"#id_email": "my@email.com", "#id_message": "Hello"})
            self.submit("input[type=submit]")
            self.assertTextPresent("Thanks for your message!")


    class ContactFormWebTests(ContactFormTestBase, WebTestBase):
        pass


    class ContactFormSeleniumTests(ContactFormTestBase, SeleniumTestBase):
        pass


You now have two tests for the price of one!

Of course:

* You don't have to use both — the high level API provided by django-functest is
  still useful for writing either kind of test.

* Sometimes you have pages that require Javascript to work for some parts. This
  can be handled by adding tests to the Selenium subclass only.

Sometimes you need different actions to be done if Javascript is enabled.
In this case, there are several options:

1) Use an abstract method in the base class, and create different
   implementations of it in the subclasses::

       class ContactFormTestBase(FuncBaseMixin):
           def test_foo(self):
               self.get_url("foo")
               self.do_thing()
               self.assertTextPresent("Success!")


       class ContactFormWebTests(ContactFormTestBase, WebTestBase):
           def do_thing(self):
               pass  # etc.


       class ContactFormSeleniumTests(ContactFormTestBase, SeleniumTestBase):
           def do_thing(self):
               pass  # etc.

2) Test the attribute ``is_full_browser_test``. This is ``True`` for Selenium,
   and ``False`` for WebTest. For example::

       def test_foo(self):
           self.get_url("foo")
           if self.is_full_browser_test:
               # Form is not visible until we click this button
               self.click("input.foo")
           self.fill_form()
           self.submit("input[type=submit]")
           self.assertTextPresent("Success!")
