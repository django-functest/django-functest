import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from django_functest import FuncBaseMixin, Upload
from django_functest.exceptions import (
    SeleniumCantUseElement,
    WebTestCantUseElement,
    WebTestMultipleElementsException,
    WebTestNoSuchElementException,
)

from .base import ChromeBase, FirefoxBase, WebTestBase
from .models import Thing

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class CommonBase(FuncBaseMixin):
    def setUp(self):
        super().setUp()
        self.thing = Thing.objects.create(
            name="Rock",
            big=True,
            clever=False,
            element_type=Thing.ELEMENT_EARTH,
            category=Thing.CATEGORY_MAGMA,
            count=1,
            description="Hard thing",
        )

    def test_get_url(self):
        self.get_url("admin:login")
        url = self.current_url
        assert url.endswith("/admin/login/")
        assert url.startswith("http://")

    def test_get_literal_url(self):
        url = reverse("admin:login")
        self.get_literal_url(url)
        self.assertUrlsEqual(url)

    def test_get_literal_url_with_full_url(self):
        url = reverse("admin:login")
        self.get_literal_url(url)
        # Specifically check this idiom for refreshing a page:
        self.get_literal_url(self.current_url)
        self.assertUrlsEqual(url)

    def test_assertUrlsEqual_default(self):
        self.get_url("admin:login")
        with pytest.raises(AssertionError):
            self.assertUrlsEqual("foo")
        self.assertUrlsEqual("/admin/login/")

    def test_assertUrlsEqual_path(self):
        with pytest.raises(AssertionError):
            self.assertUrlsEqual("/login/", "/admin/login/")
        self.assertUrlsEqual("/login/", "/login/")

    def test_assertUrlsEqual_query(self):
        with pytest.raises(AssertionError):
            self.assertUrlsEqual("/foo/?q=1", "/foo/")
        with pytest.raises(AssertionError):
            self.assertUrlsEqual("/foo/?q=1", "/foo/?q=2")
        self.assertUrlsEqual("/foo/?q=1", "/foo/?q=1")

    def test_assertUrlsEqual_host(self):
        self.assertUrlsEqual("/foo/", "//example.com/foo/")
        self.assertUrlsEqual("//example.com/foo/", "//example.com/foo/")
        with pytest.raises(AssertionError):
            self.assertUrlsEqual("//example.com/foo/", "//other.com/foo/")

    def test_assertUrlsEqual_protocol(self):
        self.assertUrlsEqual("http://example.com/foo/", "//example.com/foo/")
        self.assertUrlsEqual("http://example.com/foo/", "http://example.com/foo/")
        with pytest.raises(AssertionError):
            self.assertUrlsEqual("http://example.com/foo/", "https://example.com/foo/")

    def test_assertTextPresent(self):
        self.get_url("test_misc")
        self.assertTextPresent("Hello world")
        # Check escaping
        # NB we are using " here, not the &quot; found in the template source.
        self.assertTextPresent("from 'me' & \"friends\"")
        self.assertTextPresent("""It's also allowed to have "quotes" without escaping in text in valid HTML""")

        with pytest.raises(AssertionError):
            self.assertTextPresent("Something definitely not there")

    def test_assertTextAbsent(self):
        self.get_url("test_misc")
        self.assertTextAbsent("Something definitely not there")
        with pytest.raises(AssertionError):
            self.assertTextAbsent("Hello world")
        with pytest.raises(AssertionError):
            self.assertTextAbsent("from 'me' & \"friends\"")
        with pytest.raises(AssertionError):
            self.assertTextAbsent(
                """It's also allowed to have "quotes" """ """without escaping in text in valid HTML"""
            )

    def test_assertTextPresent_within(self):
        self.get_url("test_misc")
        self.assertTextPresent("Hello world", within="p")
        with pytest.raises(AssertionError):
            self.assertTextPresent("Hello world", within="p.myclass")
        with pytest.raises(AssertionError, match="No elements matched the CSS selector 'p.not-a-real-class'"):
            self.assertTextPresent("Hello world", within="p.not-a-real-class", wait=False)

    def test_assertTextAbsent_within(self):
        self.get_url("test_misc")
        self.assertTextAbsent("Hello world", within="p.myclass")
        with pytest.raises(AssertionError):
            self.assertTextAbsent("Hello world", within="p")

        self.assertTextAbsent("Hello world", within="p#this-is-not-a-dom-node")

    def test_assertTextAbsent_script(self):
        # This is a test that we are parsing script tags properly.
        self.get_literal_url(reverse("delayed_appearance") + "?add_js_delay=100")
        self.assertTextAbsent("Hello!", within="#new_stuff")

    def test_current_url(self):
        self.get_url("admin:login")
        # Check it really is a full URL
        assert self.current_url.startswith("http")

    def test_is_element_present(self):
        self.get_url("admin:login")
        assert self.is_element_present("#id_username")
        assert not self.is_element_present("#id_something_not_there")

    def refresh_thing(self):
        self.thing = Thing.objects.get(id=self.thing.id)
        return self.thing

    def test_fill(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.fill(
            {
                "#id_name": "New name",
                "#id_big": False,
                "#id_clever": True,
                "#id_element_type": Thing.ELEMENT_AIR,
                "#id_category_1": Thing.CATEGORY_QUASIGROUP,
                "#id_count": 5,
                "#id_description": "Soft thing\r\nwith line breaks",
            }
        )
        self.submit("input[name=change]")
        self._assertThingChanged()

    def test_fill_by_id(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.fill_by_id(
            {
                "id_name": "New name",
                "id_big": False,
                "id_clever": True,
                "id_element_type": Thing.ELEMENT_AIR,
                "id_category_1": Thing.CATEGORY_QUASIGROUP,
                "id_count": 5,
                "id_description": "Soft thing\r\nwith line breaks",
            }
        )
        self.submit("input[name=change]")
        self._assertThingChanged()

    def test_fill_by_name(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.fill_by_name(
            {
                "name": "New name",
                "big": False,
                "clever": True,
                "element_type": Thing.ELEMENT_AIR,
                "category": Thing.CATEGORY_QUASIGROUP,
                "count": 5,
                "description": "Soft thing\r\nwith line breaks",
            }
        )
        self.submit("input[name=change]")
        self._assertThingChanged()

    def test_fill_by_text(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.fill_by_text({"#id_element_type": "Water"})
        self.submit("input[name=change]")
        self.refresh_thing()
        assert self.thing.element_type == Thing.ELEMENT_WATER

    def test_fill_by_text_missing(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        with pytest.raises(self.TextNotFoundException):
            self.fill_by_text({"#id_element_type": "Plasma"})

    def test_fill_by_text_for_unsupported(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        with pytest.raises(self.ElementUnusableException):
            self.fill_by_text({"#id_count": "Water"})

    def _assertThingChanged(self):
        thing = self.refresh_thing()
        assert thing.name == "New name"
        assert not thing.big
        assert thing.clever
        assert thing.element_type == Thing.ELEMENT_AIR
        assert thing.category == Thing.CATEGORY_QUASIGROUP
        assert thing.count == 5
        assert thing.description == "Soft thing\r\nwith line breaks"

    def test_fill_no_element_error(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        with pytest.raises(self.ElementNotFoundException):
            self.fill({"#id_blahblah": "New name"})

    def test_fill_select_by_integer(self):
        url = reverse("edit_thing", kwargs=dict(thing_id=self.thing.id)) + "?select_for_category=1"
        self.get_literal_url(url)
        self.fill_by_name(
            {
                "name": "New name",
                "big": False,
                "clever": True,
                "element_type": Thing.ELEMENT_AIR,
                "category": Thing.CATEGORY_QUASIGROUP,
                "count": 5,
                "description": "Soft thing\r\nwith line breaks",
            }
        )
        self.submit("input[name=change]")
        self._assertThingChanged()

    def test_fill_checkbox_with_same_name(self):
        # It is allowed to have two checkboxes with the same name. It should result
        # in a submission with repeated values of
        self.thing2 = Thing.objects.create(
            name="Flower",
            big=False,
            clever=True,
            element_type=Thing.ELEMENT_EARTH,
            category=Thing.CATEGORY_MONOID,
            count=1,
            description="Soft thing",
        )
        self.thing3 = Thing.objects.create(
            name="Water",
            big=False,
            clever=False,
            element_type=Thing.ELEMENT_WATER,
            category=Thing.CATEGORY_MAGMA,
            count=1,
            description="Wet thing",
        )
        self.get_url("list_things")

        # Select:
        self.fill(
            {
                f'input[name=select_thing][value="{self.thing.id}"]': True,
                f'input[name=select_thing][value="{self.thing2.id}"]': True,
            }
        )
        self.submit("input[name=select]")
        self.assertTextPresent(f"{self.thing.name} is selected")
        self.assertTextPresent(f"{self.thing2.name} is selected")
        self.assertTextAbsent(f"{self.thing3.name} is selected")

        # Unselect:
        self.fill({f'input[name=select_thing][value="{self.thing.id}"]': False})
        self.submit("input[name=select]")
        self.assertTextAbsent(f"{self.thing.name} is selected")
        self.assertTextPresent(f"{self.thing2.name} is selected")
        self.assertTextAbsent(f"{self.thing3.name} is selected")

    def test_fill_no_scroll(self):
        self.get_literal_url(reverse("overflowing"))

        # scroll makes no different to WebTest, but we should
        # still be able to specify it for compatibility

        # With scroll=False
        self.fill({"[name=name]": "Peter"}, scroll=False)
        self.fill_by_text({"[name=itemdropdown]": "Item 2"}, scroll=False)
        self.submit("[type=submit]")
        self.assertTextPresent("Name submitted: Peter")
        self.assertTextPresent("Item submitted: item-2")

        # With auto_scroll_by_default=False
        self.auto_scroll_by_default = False
        self.fill({"[name=name]": "Annabelle"})
        self.fill_by_text({"[name=itemdropdown]": "Item 2"})
        self.submit("[type=submit]")
        self.assertTextPresent("Name submitted: Annabelle")
        self.assertTextPresent("Item submitted: item-2")

    def test_submit(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.submit("button[name=clear]")
        thing = self.refresh_thing()
        assert thing.name == ""

    def test_submit_no_scroll(self):
        self.get_literal_url(reverse("overflowing"))

        # scroll makes no different to WebTest, but we should
        # still be able to specify it for compatibility

        # With scroll=False to submit
        self.submit("[type=submit]", scroll=False)
        self.assertTextPresent("Submitted so far: 1")

        # With auto_scroll_by_default=False
        self.auto_scroll_by_default = False
        self.submit("[type=submit]")
        self.assertTextPresent("Submitted so far: 2")

    def test_submit_form(self):
        self.get_url("auto_submit_form")
        self.assertTextPresent("Method used: GET", within="#method")
        self.fill({"select": "ice-cream"})
        if not self.is_full_browser_test:
            # Need to manually submit
            self.submit("#the-form")
        self.assertTextPresent("Method used: POST", within="#method")
        self.assertTextPresent("You chose ice-cream")

        # Test that we can use the same API with Selenium
        self.submit("#the-form")

    def test_follow_link(self):
        self.get_url("list_things")
        self.follow_link("a.edit")
        self.assertUrlsEqual(reverse("edit_thing", kwargs={"thing_id": self.thing.id}))

    def test_follow_link_not_found(self):
        self.get_url("list_things")
        with pytest.raises(self.ElementNotFoundException):
            self.follow_link("a.foobar")

    def test_follow_link_path_relative(self):
        self.get_url("test_misc")
        self.follow_link('a[href="."]')
        self.assertUrlsEqual(reverse("test_misc"))

        self.follow_link('a[href="?param1=val1"]')
        self.assertUrlsEqual(reverse("test_misc") + "?param1=val1")

        self.follow_link('a[href="?param1=val2&param2"]')
        self.assertUrlsEqual(reverse("test_misc") + "?param1=val2&param2")

        self.follow_link('a[href="."]')  # This should clear queries
        self.assertUrlsEqual(reverse("test_misc"))

    def test_back(self):
        self.get_url("list_things")
        self.follow_link("a.edit")
        self.back()
        self.assertUrlsEqual(reverse("list_things"))

    def test_multiple_back(self):
        # We could test the behaviour regarding forms, especially those that
        # submit to the same URL and then redirect to the same URL. However,
        # Firefox and Chrome behave differently here - Firefox produces
        # fewer history entries.
        self.get_url("list_things")
        self.follow_link("a.edit")
        edit_url = reverse("edit_thing", kwargs={"thing_id": self.thing.id})
        self.assertUrlsEqual(edit_url)
        self.submit("button[name=clear]")
        self.assertUrlsEqual(reverse("thing_cleared", kwargs={"thing_id": self.thing.id}))
        self.assertTextPresent("was cleared")
        self.back()
        self.assertUrlsEqual(edit_url)
        self.back()
        self.assertUrlsEqual(reverse("list_things"))

    def test_set_session_data(self):
        self.set_session_data({"name": "The Jabberwocky"})
        self.get_url("test_misc")
        self.assertTextPresent("Hello to The Jabberwocky")

    def test_get_session_data(self):
        self.get_url("set_sess_foo_to_bar")
        sess_dict = self.get_session_data()
        assert sess_dict == {"foo": "bar"}

    def test_value(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        assert self.value("#id_name") == "Rock"
        assert self.value("#id_big") is True
        assert self.value("#id_clever") is False
        assert self.value("#id_element_type") == "e"
        assert self.value("[name=category]") == str(Thing.CATEGORY_MAGMA)
        assert self.value("#id_description") == "Hard thing"

    def test_value_immediately_after_fill(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.fill_by_name(
            {
                "name": "Some changed name",
                "big": False,
                "clever": True,
                "element_type": "w",
                "category": Thing.CATEGORY_MONOID,
                "description": "Some changed description",
            }
        )
        assert self.value("#id_name") == "Some changed name"
        assert self.value("#id_big") is False
        assert self.value("#id_clever") is True
        assert self.value("#id_element_type") == "w"
        assert self.value("#id_description") == "Some changed description"
        assert self.value("[name=category]") == str(Thing.CATEGORY_MONOID)

    def test_file_upload(self):
        self.get_url("edit_thing_with_upload", thing_id=self.thing.id)
        data = b"This is my data"
        self.fill({"#id_notes_file": Upload("notes.txt", content=data)})
        self.submit("[name=change]")
        thing = self.refresh_thing()
        assert thing.notes_file.file.read() == data

    def test_new_browser_session(self):
        self.get_url("new_browser_session_test")
        self.assertTextPresent("Hello new user")
        self.assertTextAbsent("Welcome back")
        uid_1 = self.get_session_data()["UID"]

        # Sanity check our view behaves as expected
        self.get_url("new_browser_session_test")
        self.assertTextPresent("Welcome back")
        uid_1b = self.get_session_data()["UID"]

        assert uid_1 == uid_1b

        first_session_token, second_session_token = self.new_browser_session()
        self.get_url("new_browser_session_test")
        self.assertTextPresent("Hello new user")
        self.assertTextAbsent("Welcome back")
        uid_2 = self.get_session_data()["UID"]
        assert uid_1 != uid_2

        # Tests for switch_browser_session
        ot2, nt2 = self.switch_browser_session(first_session_token)
        assert nt2 == first_session_token
        assert ot2 == second_session_token

        self.get_url("new_browser_session_test")
        self.assertTextPresent("Welcome back")
        self.assertTextPresent(uid_1)
        assert self.get_session_data()["UID"] == uid_1

        self.switch_browser_session(second_session_token)
        self.get_url("new_browser_session_test")
        self.assertTextPresent("Welcome back")
        self.assertTextPresent(uid_2)
        assert self.get_session_data()["UID"] == uid_2

        # assertTextPresent (etc.) should work without refetching
        # a page. This requires things like `last_response`
        # automatically switching.

        self.switch_browser_session(first_session_token)
        self.assertTextPresent(uid_1)
        self.assertTextAbsent(uid_2)
        self.switch_browser_session(second_session_token)
        self.assertTextPresent(uid_2)
        self.assertTextAbsent(uid_1)

    def test_get_element_inner_text(self):
        self.get_url("test_misc")
        assert self.get_element_inner_text("#inner-text-test-1") == "A paragraph with “this” & that 😄"
        assert self.get_element_inner_text("#inner-text-test-2") == "Some text with bold and italic."
        assert self.get_element_inner_text("#inner-text-test-3") == ""
        assert self.get_element_inner_text("#does-not-exist-3") is None

    def test_get_element_attribute(self):
        self.get_url("test_misc")
        assert self.get_element_attribute("#inner-text-test-1", "id") == "inner-text-test-1"
        # href tests are important here, because of the difference between
        # Selenium's `WebElement.get_attribute` and `get_dom_attribute`
        assert self.get_element_attribute("#self-link-3", "href") == "?param1=val2&param2"
        assert self.get_element_attribute("#self-link-3", "does-not-exist") is None
        assert self.get_element_attribute("#does-not-exist-3", "id") is None


class TestFuncWebTestCommon(CommonBase, WebTestBase):

    ElementNotFoundException = WebTestNoSuchElementException
    TextNotFoundException = ValueError
    ElementUnusableException = WebTestCantUseElement

    def test_is_full_browser_attribute(self):
        assert self.is_full_browser_test is False

    def test_fill_multiple_matches(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        with pytest.raises(WebTestMultipleElementsException):
            self.fill({"input[type=checkbox]": True})

    def test_fill_element_without_name(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        with pytest.raises(WebTestCantUseElement):
            self.fill({"#id_badinput1": "Hello"})

    def test_fill_element_outside_form(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        with pytest.raises(WebTestCantUseElement):
            self.fill({"#id_badinput2": "Hello"})

    def test_submit_no_auto_follow(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.submit("input[name=change]", auto_follow=False)
        assert self.last_response.status_int == 302

    def test_follow_link_multiple_matches(self):
        Thing.objects.create(name="Another")
        self.get_url("list_things")
        with pytest.raises(WebTestMultipleElementsException):
            self.follow_link("a.edit")

    def test_follow_link_no_href(self):
        self.get_url("list_things")
        with pytest.raises(WebTestCantUseElement):
            self.follow_link("a.javascriptonly")

    def test_get_literal_url_auto_follow(self):
        url = "/redirect_to_misc/"
        self.get_literal_url(url, auto_follow=True)
        self.assertUrlsEqual("/test_misc/")

        self.get_literal_url(url, auto_follow=False)
        self.assertUrlsEqual(url)
        assert self.last_response.status_int == 302

    def test_get_literal_url_expect_errors(self):
        url = "/a_404_url/"
        self.get_literal_url(url, expect_errors=True)
        assert self.last_response.status_int == 404
        with pytest.raises(Exception):
            self.get_literal_url(url, expect_errors=False)

    def test_get_element_inner_text_multiple(self):
        self.get_url("test_misc")
        with pytest.raises(WebTestMultipleElementsException):
            self.get_element_inner_text("p")

    def test_get_element_attribute_multiple(self):
        self.get_url("test_misc")
        with pytest.raises(WebTestMultipleElementsException):
            self.get_element_attribute("a", "id")

    def test_submit_form_multiple_matching(self):
        self.get_url("auto_submit_form")
        with pytest.raises(WebTestMultipleElementsException):
            self.submit("form")


class FuncSeleniumCommonBase(CommonBase):

    ElementNotFoundException = TimeoutException
    TextNotFoundException = NoSuchElementException
    ElementUnusableException = SeleniumCantUseElement

    def test_is_full_browser_attribute(self):
        assert self.is_full_browser_test is True

    def test_fill_with_scrolling(self):
        url = reverse("edit_thing", kwargs=dict(thing_id=self.thing.id)) + "?add_spacers=1"
        self.get_literal_url(url)
        self.fill(
            {
                "#id_name": "New name",
                "#id_big": False,
                "#id_clever": True,
                "#id_element_type": Thing.ELEMENT_AIR,
                "#id_category_1": Thing.CATEGORY_QUASIGROUP,
                "#id_count": 5,
                "#id_description": "Soft thing\r\nwith line breaks",
            }
        )
        self.submit("input[name=change]")
        self._assertThingChanged()

    def test_submit_no_wait_for_reload(self):
        self.get_url("edit_thing", thing_id=self.thing.id)
        self.submit("button[name=check]", wait_for_reload=False)
        self.assertTextPresent("Everything is fine")

    def test_submit_slow_page(self):
        url = reverse("edit_thing", kwargs=dict(thing_id=self.thing.id)) + "?add_js_delay=5"
        self.get_literal_url(url)
        self.fill(
            {
                "#id_name": "New name",
                "#id_big": False,
                "#id_clever": True,
                "#id_category_1": Thing.CATEGORY_QUASIGROUP,
                "#id_element_type": Thing.ELEMENT_AIR,
                "#id_count": 5,
                "#id_description": "Soft thing\r\nwith line breaks",
            }
        )
        self.submit("input[name=change]")
        self._assertThingChanged()

    def test_assertTextPresent_auto_wait(self):
        self.get_literal_url(reverse("delayed_appearance") + "?add_js_delay=3")

        # Should automatically wait if we pass within specifying an element not present at first:
        self.assertTextPresent("Hello!", within="#new_stuff")

    def test_assertTextPresent_no_wait(self):
        self.get_literal_url(reverse("test_misc"))
        with pytest.raises(TimeoutException):
            self.assertTextPresent("Hello world", within="p.not-a-real-class")


class TestFuncSeleniumCommonFirefox(FuncSeleniumCommonBase, FirefoxBase):
    pass


class TestFuncSeleniumCommonChrome(FuncSeleniumCommonBase, ChromeBase):
    pass
