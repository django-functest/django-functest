Shadow DOM
==========

The `shadow DOM provided by custom web components <https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM>`_ provides some challenges for django-functest.

For WebTest, the only element visible is the custom element, and not the shadow DOM which is created by Javascript. Tests that rely on functionality provided via Javascript cannot be tested via WebTest.

For Selenium, we still have the difficulty that traversing the DOM is difficult due to the boundaries of the shadow DOM. In order to traverse into a custom element’s shadow DOM, you can supply a sequence (tuple or list) of CSS selectors instead of a single CSS selector. Each CSS selector after the first one will be used starting from the `shadowRoot <https://developer.mozilla.org/en-US/docs/Web/API/Element/shadowRoot>`_ of the element located so far.

For example, if instead of an ``<input>`` you have a custom ``my-input`` element whose shadow DOM contains a single real ``<input>``, you can fill it like this:

.. code-block:: python

   self.fill({("my-input#my-id", "input"): "Text"})


This works for every API that supports CSS selectors, currently with the following exceptions:

* ``assertTextPresent``
* ``assertTextAbsent``

You should note that not every element that is “part of” a custom element is within the shadow DOM:

.. code-block:: html

   <my-custom-element>
     <div>This is a normal element within the normal DOM</div>
   </my-custom-element>


If you are using shadow DOM a lot, this may still be too awkward, and you might be better of using `Playwright for Python <https://playwright.dev/python/>`_, which `has more seamless support for shadow DOM <https://playwright.dev/python/docs/locators#locate-in-shadow-dom>`_.

At the time of writing, geckodriver does not support finding elements within a shadow root – see `https://github.com/mozilla/geckodriver/issues/2005 <https://github.com/mozilla/geckodriver/issues/2005>`_.
