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
