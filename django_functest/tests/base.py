import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from django_functest import FuncSeleniumMixin, FuncWebTestMixin


class WebTestBase(FuncWebTestMixin, TestCase):
    pass


class FirefoxBase(FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = "Firefox"


# Chrome/ChromeDriver don't work on Travis
# https://github.com/travis-ci/travis-ci/issues/272
@unittest.skipIf(os.environ.get('TRAVIS'), "Skipping Chrome tests")
class ChromeBase(FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = "Chrome"
