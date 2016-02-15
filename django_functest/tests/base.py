import os
import subprocess
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

from django_functest import FuncSeleniumMixin, FuncWebTestMixin

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

IN_TRAVIS = os.environ.get('TRAVIS')


def binary_available(filename):
    return subprocess.call(["which", filename], stdout=subprocess.PIPE) == 0

firefox_available = binary_available("firefox")
chrome_available = binary_available("chromedriver")
phantomjs_available = binary_available("phantomjs")


class MyLiveServerTestCase(StaticLiveServerTestCase):
    available_apps = AVAILABLE_APPS


class WebTestBase(FuncWebTestMixin, TestCase):
    available_apps = AVAILABLE_APPS


class HideBrowserMixin(object):
    display = False  # hacked by runtests.py


class SeleniumBaseMixin(object):
    browser_window_size = (1024, 768)
    if IN_TRAVIS:
        default_timeout = 40
        page_load_timeout = 60


@unittest.skipIf(not firefox_available, "Firefox not available, skipping")
class FirefoxBase(HideBrowserMixin, SeleniumBaseMixin, FuncSeleniumMixin, MyLiveServerTestCase):
    driver_name = "Firefox"


# Chrome/ChromeDriver don't work on Travis
# https://github.com/travis-ci/travis-ci/issues/272
@unittest.skipIf(not chrome_available or IN_TRAVIS, "Chrome not available, skipping")
class ChromeBase(HideBrowserMixin, SeleniumBaseMixin, FuncSeleniumMixin, MyLiveServerTestCase):
    driver_name = "Chrome"


@unittest.skipIf(not phantomjs_available, "PhantomJS not available, skipping")
class PhantomJSBase(SeleniumBaseMixin, FuncSeleniumMixin, MyLiveServerTestCase):
    driver_name = "PhantomJS"
