import os
import unittest

from django.test import LiveServerTestCase, TestCase

from django_functest import FuncSeleniumMixin, FuncWebTestMixin
from django_functest.tests.models import Thing


# We use the Django admin for most tests, since it is very easy to create

class WebTestBase(FuncWebTestMixin, TestCase):
    pass


class FirefoxBase(FuncSeleniumMixin, LiveServerTestCase):
    pass


# Chrome/ChromeDriver don't work on Travis
# https://github.com/travis-ci/travis-ci/issues/272
@unittest.skipIf(os.environ.get('TRAVIS'), "Skipping Chrome tests")
class ChromeBase(FuncSeleniumMixin, LiveServerTestCase):
    @classmethod
    def get_driver_name(cls):
        return "Chrome"


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
