import os
import subprocess
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from django_functest import FuncSeleniumMixin, FuncWebTestMixin


def binary_available(filename):
    return subprocess.call(["which", filename], stdout=subprocess.PIPE) == 0

firefox_available = binary_available("firefox")
chrome_available = binary_available("chromedriver")
phantomjs_available = binary_available("phantomjs")


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


@unittest.skipIf(not phantomjs_available, "PhantomJS not available, skipping")
class PhantomJSBase(FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = "PhantomJS"
