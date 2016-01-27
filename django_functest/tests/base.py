import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from django_functest import FuncSeleniumMixin, FuncWebTestMixin


firefox_available = os.system("which firefox") == 0
chrome_available = os.system("which chromedriver") == 0


class WebTestBase(FuncWebTestMixin, TestCase):
    pass


class HideBrowserMixin(object):
    display = False  # hacked by runtests.py


@unittest.skipIf(not firefox_available, "Firefox not available, skipping")
class FirefoxBase(HideBrowserMixin, FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = "Firefox"


# Chrome/ChromeDriver don't work on Travis
# https://github.com/travis-ci/travis-ci/issues/272
@unittest.skipIf(not chrome_available or os.environ.get('TRAVIS'), "Chrome not available, skipping")
class ChromeBase(HideBrowserMixin, FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = "Chrome"
