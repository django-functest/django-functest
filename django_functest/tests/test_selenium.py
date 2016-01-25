import unittest

from .base import ChromeBase, FirefoxBase
from .models import Thing


# Tests for Selenium specific methods

class TestFuncSeleniumSpecificBase(object):

    def setUp(self):
        super(TestFuncSeleniumSpecificBase, self).setUp()
        self.thing = Thing.objects.create(name="Rock",
                                          big=True,
                                          clever=False,
                                          element_type=Thing.ELEMENT_EARTH)

    def test_is_element_displayed(self):
        self.get_url('admin:login')
        self.assertTrue(self.is_element_displayed('#id_username'))
        self.assertFalse(self.is_element_displayed('#id_something_else'))
        self.execute_script("document.querySelector('#id_username').style.display = 'none';")
        self.assertFalse(self.is_element_displayed('#id_username'))

    def test_click(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.click('input[name=check]')
        self.assertTextPresent("Everything is fine")

    def test_click_xpath(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.click(xpath='//input[@name="check"]')
        self.assertTextPresent("Everything is fine")

    def test_double_click(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.click('input[name=check]', double=True)
        self.assertTextPresent("Everything is really fine")

    def test_execute_script(self):
        self.get_url('django_functest.test_misc')
        self.assertEqual(self.execute_script("return 1 + 1;"), 2)

    def test_execute_script_with_args(self):
        self.get_url('django_functest.test_misc')
        retval = self.execute_script("return arguments[0] + arguments[1];", 1, 2)
        self.assertEqual(retval, 3)

    def test_hover(self):
        self.get_url('django_functest.test_misc')
        get_style = "return document.defaultView.getComputedStyle(document.querySelector('#hoverable'))['font-style']"
        self.assertEqual(self.execute_script(get_style),
                         "normal")
        self.hover('#hoverable')
        self.assertEqual(self.execute_script(get_style),
                         "italic")


class TestFuncSeleniumSpecificFirefox(TestFuncSeleniumSpecificBase, FirefoxBase):

    # This fails on some Firefox versions, at least on Travis, but not locally,
    # so it is difficult to know how to write a better test.
    test_hover = unittest.expectedFailure(TestFuncSeleniumSpecificBase.test_hover)


class TestFuncSeleniumSpecificChrome(TestFuncSeleniumSpecificBase, ChromeBase):
    pass


# Test class attribute `browser_window_size` works correctly:

class TestBrowserSizeBase(object):
    browser_window_size = (2800, 1400)

    def test_size(self):
        width, height = self.execute_script("return [window.outerWidth, window.outerHeight]")
        self.assertEqual((width, height),
                         (2800, 1400))

    def test_resize(self):
        self.set_window_size(400, 300)
        width, height = self.execute_script("return [window.outerWidth, window.outerHeight]")
        self.assertEqual((width, height),
                         (400, 300))


class TestBrowserSizeFirefox(TestBrowserSizeBase, FirefoxBase):
    pass


class TestBrowserSizeChrome(TestBrowserSizeBase, ChromeBase):
    pass
