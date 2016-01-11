from django.test import LiveServerTestCase, TestCase

from django_functest import FuncWebTestMixin, FuncSeleniumMixin
from django_functest.tests.models import Thing

# We use the Django admin for most tests, since it is very easy to create


class TestCommonBase(object):
    def setUp(self):
        super(TestCommonBase, self).setUp()
        self.thing = Thing.objects.create(name="Henrietta")

    def test_get_url(self):
        self.get_url('admin:login')
        url = self.current_url
        self.assertTrue(url.endswith("/admin/login/"))
        self.assertTrue(url.startswith("http://"))


class TestFuncWebTestCommon(TestCommonBase, FuncWebTestMixin, TestCase):

    def test_is_full_browser_attribute(self):
        self.assertEqual(self.is_full_browser_test, False)


class TestFuncSeleniumCommon(TestCommonBase, FuncSeleniumMixin, LiveServerTestCase):

    def test_is_full_browser_attribute(self):
        self.assertEqual(self.is_full_browser_test, True)
