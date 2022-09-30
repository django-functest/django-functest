====
Tips
====

The following are various tips for writing reliable tests.

Avoid arbitrary “sleeps”
------------------------

For Selenium, due to things happening asynchronously, you often have to wait a
little bit of time before something appears on the page or is saved into the
database. In many cases, django-functest has appropriate waiting behaviour
built in. When this is not sufficient, however, it’s tempting do a bit of::

  import time

  time.sleep(0.2)  # Should be enough…


This works great until you run the test on CI or on a busy machine and it take
205ms instead of 200ms. You don’t really want to add 10 second delay to be
**really** sure, so you end with a flaky test suite that fails randomly, and
life is miserable.

Instead, use :meth:`~django_functest.FuncSeleniumMixin.wait_until` to wait for
the thing you are expecting. For example, to wait for some text to appear on the
page::

  self.wait_until(self.assertion_passes(self.assertTextPresent, "Data saved"))

Or for an element to be present::

  self.wait_until(lambda *args: self.is_element_present("#my-id"))

Or for the data to be saved in the DB::

    self.wait_until(lambda *args: MyModel.objects.filter(text="Updated").exists())

If these fail, they fail with a timeout, which means they wait a long time
before failing. This is a bit annoying, but it’s usually better than the
alternative.


Use FuncBaseMixin
-----------------

In the above example, ``FuncBaseMixin`` is not strictly needed at all — it
provides method definitions which all raise ``NotImplementedError`` — so you
could remove it. However, it can be very useful for editors that provide code
auto-completion help, which can find the docstrings on ``FuncBaseMixin`` when
you are writing methods like ``ContactFormTestBase.test_contact_form``. You may
want to inherit from it in your own base class.


Avoid 404s
----------

For Selenium tests, the browser will load not only the main page, but various
other resources (Javascript, CSS etc.). It can be important to ensure that these
resources will be served by your dev server. Requesting pages that don't exist
will slow down your tests, and it can introduce unreliability. This can
especially be true if your site has complex middleware, redirects etc. and
things that affect the session. Unnecessary requests could trigger some of these
actions and complicate things.

In particular, in the absence of a `defined favicon location
<https://www.w3.org/2005/10/howto-favicon>`_, browsers will request
``/favicon.ico``. This will typically hit your app and produce 1) a redirect
since it does not end with ``/`` and 2) a 404. Depending on your URLs it could
also trigger other work, since it does not have the static URL prefix, and so it
won't be handled by the normal staticfiles finder. To workaround this, it is
recommended to put your favicon in the staticfiles folder, and specify its
location in your HTML, or add a view that serves ``/favicon.ico``.
