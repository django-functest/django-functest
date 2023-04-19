import os
from functools import wraps

import pytest
from django.contrib.auth import get_user_model
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from django_functest import AdminLoginMixin, FuncBaseMixin

from .base import ChromeBase, FirefoxBase
from .models import Thing

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


# Tests for Selenium specific methods


class FuncSeleniumSpecificBase(AdminLoginMixin, FuncBaseMixin):
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
        assert self.is_element_displayed("#id_username")
        assert not self.is_element_displayed("#id_something_else")
        self.execute_script("document.querySelector('#id_username').style.display = 'none';")
        assert not self.is_element_displayed("#id_username")

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
        with pytest.raises(NoSuchElementException):
            self.click(text="Edit Fridge", wait_timeout=0)
        with pytest.raises(NoSuchElementException):
            self.click(text="Edit Rock", text_parent_id="fribble", wait_timeout=0)

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

    def test_alert_handling_accept(self):
        self.get_url("with_confirm")
        self.assertTextPresent("Some text to be deleted")
        self.click("button", expect_alert=True)
        self.accept_alert()
        self.assertTextAbsent("Some text to be deleted")

    def test_alert_handling_dismiss(self):
        self.get_url("with_confirm")
        self.assertTextPresent("Some text to be deleted")
        self.click("button", expect_alert=True)
        self.dismiss_alert()
        self.assertTextPresent("Some text to be deleted")

    def test_execute_script(self):
        self.get_url("test_misc")
        assert self.execute_script("return 1 + 1;") == 2

    def test_execute_script_with_args(self):
        self.get_url("test_misc")
        retval = self.execute_script("return arguments[0] + arguments[1];", 1, 2)
        assert retval == 3

    def test_hover(self):
        self.get_url("test_misc")
        get_style = "return document.defaultView.getComputedStyle(document.querySelector('#hoverable'))['font-style']"
        assert self.execute_script(get_style) == "normal"
        self.hover("#hoverable")
        assert self.execute_script(get_style) == "italic"

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
        assert [g.name for g in user.groups.all()] == ["My new group"]
        assert user.first_name == "My first name"

    def test_save_screenshot(self):
        testname = f"tests.test_selenium.{self.__class__.__name__}.test_save_screenshot"

        fname = None
        try:
            fname = self.save_screenshot()
            assert testname in fname
            assert os.path.exists(fname)
        finally:
            if fname is not None:
                os.unlink(fname)

    def test_wait_until(self):
        self.get_literal_url(reverse("delayed_appearance") + "?add_js_delay=2")
        self.wait_until(lambda driver: self.is_element_present("#new_stuff"))
        self.assertTextPresent("Hello!", within="#id_container")

    def test_wait_until_timeout(self):
        self.get_literal_url(reverse("delayed_appearance") + "?add_js_delay=100")
        with pytest.raises(TimeoutException):
            self.wait_until(lambda driver: self.is_element_present("#new_stuff"), timeout=1)

    def test_wait_until_assertion_passes(self):
        self.get_literal_url(reverse("delayed_appearance") + "?add_js_delay=2")
        self.wait_until(self.assertion_passes(self.assertTextPresent, "Hello!", within="#id_container"))
        self.assertTextPresent("Hello!", within="#id_container")

    def test_scroll_method_legacy(self):
        self.scroll_method = "legacyWindowScrollTo"
        self.get_literal_url(reverse("long_page") + "?count=1000")
        self.submit('[name="mybutton"]')
        self.assertTextPresent("mybutton was pressed")

    def test_scroll_method_auto(self):
        self.scroll_method = "auto"
        self.get_literal_url(reverse("long_page") + "?count=1000")
        self.submit('[name="mybutton"]')
        self.assertTextPresent("mybutton was pressed")

    def test_fill_with_shadow_root(self):
        self.get_url("web_components")
        self.fill({("my-input#id-query", "input"): "My query text"})
        self.submit('[type="submit"]')
        self.assertTextPresent("Submitted query: My query text")

    def test_click_with_shadow_root(self):
        self.get_url("web_components")
        self.submit(["my-submit", "button"])
        self.assertTextPresent("my-submit was pressed")

    def test_element_utils_with_shadow_root(self):
        self.get_url("web_components")
        assert self.is_element_present(("my-div", "div.my-div-inner"))
        assert not self.is_element_present(("my-div", "my-div"))  # Nested my-div is in real DOM, not shadow DOM

        assert self.is_element_displayed(("my-div", "div.my-div-inner"))

        assert self.get_element_inner_text(("my-div", "div > h3")) == "my-div heading"
        assert self.get_element_inner_text(("my-div my-div", "div > h3")) == "my-div heading"

        assert self.get_element_attribute(("my-div", "div"), "class") == "my-div-inner"


def wrap(func):
    """
    Returns function with a wrapper
    """
    # Can be useful for badly behaved decorators that don't themselves wrap the
    # callable and return a new one, but modify the original directly, like
    # pytest.mark.xfail
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


class TestFuncSeleniumSpecificFirefox(FuncSeleniumSpecificBase, FirefoxBase):
    # Finding elements from shadow_root in Firefox currently fails:
    # https://github.com/mozilla/geckodriver/issues/2005
    # From https://bugzilla.mozilla.org/show_bug.cgi?id=1700097 it may be implemented
    # in Firefox 113 and related geckodriver

    test_fill_with_shadow_root = pytest.mark.xfail(wrap(FuncSeleniumSpecificBase.test_fill_with_shadow_root))
    test_click_with_shadow_root = pytest.mark.xfail(wrap(FuncSeleniumSpecificBase.test_click_with_shadow_root))
    test_element_utils_with_shadow_root = pytest.mark.xfail(
        wrap(FuncSeleniumSpecificBase.test_element_utils_with_shadow_root)
    )


class TestFuncSeleniumSpecificChrome(FuncSeleniumSpecificBase, ChromeBase):
    pass


# Test class attribute `browser_window_size` works correctly:


class BrowserSizeBase:
    browser_window_size = (800, 700)

    def _get_window_size(self):
        if self._driver.name == "phantomjs":
            return self.execute_script("return [document.width, document.height]")
        else:
            return self.execute_script("return [window.outerWidth, window.outerHeight]")

    def test_size(self):
        width, height = self._get_window_size()
        assert 795 < width < 805
        assert 695 < height < 705

    def test_resize(self):
        self.set_window_size(700, 500)
        width, height = self._get_window_size()
        assert 695 < width < 705
        assert 495 < height < 505


class TestBrowserSizeFirefox(BrowserSizeBase, FirefoxBase):
    pass


class TestBrowserSizeChrome(BrowserSizeBase, ChromeBase):
    pass
