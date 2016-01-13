from django_functest.tests.models import Thing

from .base import ChromeBase, FirefoxBase, WebTestBase


class TestCommonBase(object):
    def setUp(self):
        super(TestCommonBase, self).setUp()
        self.thing = Thing.objects.create(name="Henrietta")

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
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("//example.com/foo/", "//other.com/foo/"))

    def test_assertUrlsEqual_protocol(self):
        self.assertUrlsEqual("http://example.com/foo/", "//example.com/foo/")
        self.assertUrlsEqual("http://example.com/foo/", "http://example.com/foo/")
        self.assertRaises(AssertionError, lambda: self.assertUrlsEqual("http://example.com/foo/", "https://example.com/foo/"))


class TestFuncWebTestCommon(TestCommonBase, WebTestBase):

    def test_is_full_browser_attribute(self):
        self.assertEqual(self.is_full_browser_test, False)


class TestFuncSeleniumCommonBase(TestCommonBase):

    def test_is_full_browser_attribute(self):
        self.assertEqual(self.is_full_browser_test, True)


class TestFuncSeleniumCommonFirefox(TestFuncSeleniumCommonBase, FirefoxBase):
    pass


class TestFuncSeleniumCommonChrome(TestFuncSeleniumCommonBase, ChromeBase):
    pass
