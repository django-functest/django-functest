import os
import subprocess
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, override_settings

from django_functest import FuncSeleniumMixin, FuncWebTestMixin, MultiThreadedLiveServerMixin

# Getting some errors that seem related to this:
# http://stackoverflow.com/questions/18281137/selenium-django-gives-foreign-key-error/18292090#18292090 # noqa
# producing a stacktrace in which a postmigrate handler attempts to
# create permissions as part of fixture teardown and fails.
# This is not fixed by change the order of INSTALLED_APPS. However,
# we can avoid the code path by using TestCase.available_apps

AVAILABLE_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django_functest",
    "django_functest.tests",
]


def binary_available(filename):
    return subprocess.call(["which", filename], stdout=subprocess.PIPE) == 0


firefox_available = binary_available("firefox")
chrome_available = binary_available("chromedriver")


@override_settings(DEBUG=True)  # easier debugging
class MyLiveServerTestCase(StaticLiveServerTestCase):
    available_apps = AVAILABLE_APPS


class WebTestBase(FuncWebTestMixin, TestCase):
    available_apps = AVAILABLE_APPS


class HideBrowserMixin:
    display = False  # hacked by runtests.py


@unittest.skipIf(os.environ.get("TEST_SKIP_SELENIUM"), "Skipping Selenium tests")
class SeleniumBaseMixin:
    browser_window_size = (1024, 768)


@unittest.skipIf(not firefox_available, "Firefox not available, skipping")
class FirefoxBase(HideBrowserMixin, SeleniumBaseMixin, FuncSeleniumMixin, MyLiveServerTestCase):
    driver_name = "Firefox"

    firefox_binary = None  # default, hacked by runtests.py

    @classmethod
    def get_webdriver_options(cls):
        kwargs = super().get_webdriver_options()
        if cls.firefox_binary is not None:
            from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

            kwargs["firefox_binary"] = FirefoxBinary(firefox_path=cls.firefox_binary)
        return kwargs


@unittest.skipIf(not chrome_available, "Chrome not available, skipping")
class ChromeBase(
    HideBrowserMixin,
    SeleniumBaseMixin,
    FuncSeleniumMixin,
    MultiThreadedLiveServerMixin,
    MyLiveServerTestCase,
):
    driver_name = "Chrome"
