import conftest
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from django_functest import FuncSeleniumMixin, FuncWebTestMixin


class WebTestBase(FuncWebTestMixin, TestCase):
    pass


@pytest.mark.selenium
class SeleniumTestBase(FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = conftest.BROWSER
    display = conftest.SHOW_BROWSER
