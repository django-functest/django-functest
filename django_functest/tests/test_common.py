from django.core.urlresolvers import reverse
from selenium.common.exceptions import TimeoutException

from django_functest.exceptions import (
    WebTestCantUseElement, WebTestMultipleElementsException, WebTestNoSuchElementException
)
from django_functest.tests.models import Thing

from .base import ChromeBase, FirefoxBase, WebTestBase


class TestCommonBase(object):
    def setUp(self):
        super(TestCommonBase, self).setUp()
        self.thing = Thing.objects.create(name="Rock",
                                          big=True,
                                          clever=False,
                                          element_type=Thing.ELEMENT_EARTH)

    def test_get_url(self):
        self.get_url('admin:login')
        url = self.current_url
        self.assertTrue(url.endswith("/admin/login/"))
        self.assertTrue(url.startswith("http://"))

    def test_assertUrlsEqual_default(self):
        self.get_url('admin:login')
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("foo"))
        self.assertUrlsEqual("/admin/login/")

    def test_assertUrlsEqual_path(self):
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("/login/", "/admin/login/"))
        self.assertUrlsEqual("/login/", "/login/")

    def test_assertUrlsEqual_query(self):
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("/foo/?q=1", "/foo/"))
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("/foo/?q=1", "/foo/?q=2"))
        self.assertUrlsEqual("/foo/?q=1", "/foo/?q=1")

    def test_assertUrlsEqual_host(self):
        self.assertUrlsEqual("/foo/", "//example.com/foo/")
        self.assertUrlsEqual("//example.com/foo/", "//example.com/foo/")
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("//example.com/foo/",
                                                                       "//other.com/foo/"))

    def test_assertUrlsEqual_protocol(self):
        self.assertUrlsEqual("http://example.com/foo/", "//example.com/foo/")
        self.assertUrlsEqual("http://example.com/foo/", "http://example.com/foo/")
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("http://example.com/foo/",
                                                                       "https://example.com/foo/"))

    def test_assertTextPresent(self):
        self.get_url('django_functest.test1')
        self.assertTextPresent("Hello world")
        # Check escaping
        self.assertTextPresent("from me & friends")
        self.assertRaises(AssertionError, lambda: self.assertTextPresent("Something definitely not there"))

    def test_assertTextAbsent(self):
        self.get_url('django_functest.test1')
        self.assertTextAbsent("Something definitely not there")
        self.assertRaises(AssertionError, lambda: self.assertTextAbsent("Hello world"))
        self.assertRaises(AssertionError, lambda: self.assertTextAbsent("from me & friends"))

    def test_is_element_present(self):
        self.get_url('admin:login')
        self.assertTrue(self.is_element_present('#id_username'))
        self.assertFalse(self.is_element_present('#id_something_not_there'))

    def refresh_thing(self):
        self.thing = Thing.objects.get(id=self.thing.id)
        return self.thing

    def test_fill(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.fill({'#id_name': "New name",
                   '#id_big': False,
                   '#id_clever': True,
                   '#id_element_type': Thing.ELEMENT_AIR
                   })
        self.submit('input[name=change]')
        self._assertThingChanged()

    def test_fill_by_id(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.fill_by_id({'id_name': "New name",
                         'id_big': False,
                         'id_clever': True,
                         'id_element_type': Thing.ELEMENT_AIR
                         })
        self.submit('input[name=change]')
        self._assertThingChanged()

    def test_fill_by_name(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.fill_by_name({'name': "New name",
                           'big': False,
                           'clever': True,
                           'element_type': Thing.ELEMENT_AIR
                           })
        self.submit('input[name=change]')
        self._assertThingChanged()

    def _assertThingChanged(self):
        thing = self.refresh_thing()
        self.assertEqual(thing.name, "New name")
        self.assertEqual(thing.big, False)
        self.assertEqual(thing.clever, True)
        self.assertEqual(thing.element_type, Thing.ELEMENT_AIR)

    def test_fill_no_element_error(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.assertRaises(self.ElementNotFoundException, lambda: self.fill({'#id_blahblah': "New name"}))

    def test_submit(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.submit('input[name=clear]')
        thing = self.refresh_thing()
        self.assertEqual(thing.name, "")


class TestFuncWebTestCommon(TestCommonBase, WebTestBase):

    ElementNotFoundException = WebTestNoSuchElementException

    def test_is_full_browser_attribute(self):
        self.assertEqual(self.is_full_browser_test, False)

    def test_fill_multiple_matches(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.assertRaises(WebTestMultipleElementsException, lambda: self.fill({'input[type=checkbox]': True}))

    def test_fill_element_without_name(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.assertRaises(WebTestCantUseElement, lambda: self.fill({'#id_badinput1': "Hello"}))

    def test_fill_element_outside_form(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.assertRaises(WebTestCantUseElement, lambda: self.fill({'#id_badinput2': "Hello"}))

    def test_submit_no_auto_follow(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.submit('input[name=change]', auto_follow=False)
        self.assertEqual(self.last_response.status_int, 302)


class TestFuncSeleniumCommonBase(TestCommonBase):

    ElementNotFoundException = TimeoutException

    def test_is_full_browser_attribute(self):
        self.assertEqual(self.is_full_browser_test, True)

    def test_fill_with_scrolling(self):
        url = reverse('edit_thing', kwargs=dict(thing_id=self.thing.id)) + "?add_spacers=1"
        self.get_literal_url(url)
        self.fill({'#id_name': "New name",
                   '#id_big': False,
                   '#id_clever': True,
                   '#id_element_type': Thing.ELEMENT_AIR
                   })
        self.submit('input[name=change]')
        self._assertThingChanged()

    def test_submit_no_wait_for_reload(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.submit('input[name=check]', wait_for_reload=False)
        self.assertTextPresent("Everything is fine")


class TestFuncSeleniumCommonFirefox(TestFuncSeleniumCommonBase, FirefoxBase):
    pass


class TestFuncSeleniumCommonChrome(TestFuncSeleniumCommonBase, ChromeBase):
    pass
