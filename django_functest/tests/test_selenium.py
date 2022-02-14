import os

from django.contrib.auth import get_user_model
from selenium.common.exceptions import NoSuchElementException

from django_functest import AdminLoginMixin, FuncBaseMixin

from .base import ChromeBase, FirefoxBase
from .models import Thing

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


# Tests for Selenium specific methods


class TestFuncSeleniumSpecificBase(AdminLoginMixin, FuncBaseMixin):
    def setUp(self):
        super().setUp()
        self.thing = Thing.objects.create(
            name="Rock",
            big=True,
            clever=False,
            element_type=Thing.ELEMENT_EARTH,
            category=Thing.CATEGORY_MAGMA,
        )
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "password")

    def test_is_element_displayed(self):
        self.get_url("admin:login")
        self.assertTrue(self.is_element_displayed("#id_username"))
        self.assertFalse(self.is_element_displayed("#id_something_else"))
        self.execute_script("document.querySelector('#id_username').style.display = 'none';")
        self.assertFalse(self.is_element_displayed("#id_username"))

    def test_click(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.click("button[name=check]")
        self.assertTextPresent("Everything is fine")

    def test_click_xpath(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.click(xpath='//button[@name="check"]')
        self.assertTextPresent("Everything is fine")

    def test_click_text(self):
        self.get_url("list_things")
        self.click(text="Edit Rock", text_parent_id="id_thinglist", wait_for_reload=True)
        self.assertUrlsEqual(reverse("edit_thing", kwargs={"thing_id": self.thing.id}))

    def test_click_text_missing(self):
        self.get_url("list_things")
        self.assertRaises(
            NoSuchElementException,
            lambda: self.click(text="Edit Fridge", wait_timeout=0),
        )
        self.assertRaises(
            NoSuchElementException,
            lambda: self.click(text="Edit Rock", text_parent_id="fribble", wait_timeout=0),
        )

    def test_double_click(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.click("button[name=check]", double=True)
        self.assertTextPresent("Everything is really fine")

    def test_double_click_element_that_changes(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.click("[name=debounced]", double=True)
        self.assertTextPresent("Pressed x 1")

    def test_double_click_element_that_disappears(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.click("[name=disappears]", double=True)
        self.assertTextPresent("Pressed x 1")

    def test_execute_script(self):
        self.get_url("test_misc")
        self.assertEqual(self.execute_script("return 1 + 1;"), 2)

    def test_execute_script_with_args(self):
        self.get_url("test_misc")
        retval = self.execute_script("return arguments[0] + arguments[1];", 1, 2)
        self.assertEqual(retval, 3)

    def test_hover(self):
        self.get_url("test_misc")
        get_style = "return document.defaultView.getComputedStyle(document.querySelector('#hoverable'))['font-style']"
        self.assertEqual(self.execute_script(get_style), "normal")
        self.hover("#hoverable")
        self.assertEqual(self.execute_script(get_style), "italic")

    def test_switch_window(self):
        self.do_login(username="admin", password="password")
        self.get_url("admin:auth_user_change", self.user.id)
        self.click("#add_id_groups")
        old_window, new_window = self.switch_window()
        self.fill({"#id_name": "My new group"})
        self.switch_window(old_window)
        self.fill({"#id_first_name": "My first name"})
        self.switch_window(new_window)
        self.submit("input[name=_save]", window_closes=True)
        self.switch_window(old_window)
        self.submit("input[name=_save]")

        User = get_user_model()
        user = User.objects.get(id=self.user.id)
        self.assertEqual([g.name for g in user.groups.all()], ["My new group"])
        self.assertEqual(user.first_name, "My first name")

    def test_save_screenshot(self):
        testname = f"django_functest.tests.test_selenium.{self.__class__.__name__}.test_save_screenshot"

        fname = None
        try:
            fname = self.save_screenshot()
            self.assertIn(testname, fname)
            self.assertTrue(os.path.exists(fname))
        finally:
            if fname is not None:
                os.unlink(fname)


class TestFuncSeleniumSpecificFirefox(TestFuncSeleniumSpecificBase, FirefoxBase):
    pass


class TestFuncSeleniumSpecificChrome(TestFuncSeleniumSpecificBase, ChromeBase):
    pass


# Test class attribute `browser_window_size` works correctly:


class TestBrowserSizeBase:
    browser_window_size = (800, 700)

    def _get_window_size(self):
        if self._driver.name == "phantomjs":
            return self.execute_script("return [document.width, document.height]")
        else:
            return self.execute_script("return [window.outerWidth, window.outerHeight]")

    def test_size(self):
        width, height = self._get_window_size()
        self.assertTrue(795 < width < 805)
        self.assertTrue(695 < height < 705)

    def test_resize(self):
        self.set_window_size(700, 500)
        width, height = self._get_window_size()
        self.assertTrue(695 < width < 705)
        self.assertTrue(495 < height < 505)


class TestBrowserSizeFirefox(TestBrowserSizeBase, FirefoxBase):
    pass


class TestBrowserSizeChrome(TestBrowserSizeBase, ChromeBase):
    pass
