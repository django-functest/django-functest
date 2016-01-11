from django.test import TestCase

from django_functest import FuncWebTestMixin
from django_functest.tests.models import Thing

# We use the Django admin for most tests, since it is very easy to create


class TestFuncWebTestMixin(FuncWebTestMixin, TestCase):

    def setUp(self):
        self.thing = Thing.objects.create(name="Henrietta")

    def test_get_url(self):
        self.get_url('admin:login')
        self.assertTrue(self.current_url.endswith("/admin/login/"))
