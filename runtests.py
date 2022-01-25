#!/usr/bin/env python

import argparse
import faulthandler
import os
import os.path
import signal
import sys
import warnings

import django
from django.conf import settings
from django.core.management import execute_from_command_line

# If the process receives signal SIGUSR1, dump a traceback
faulthandler.enable()
faulthandler.register(signal.SIGUSR1)

warnings.simplefilter("once", PendingDeprecationWarning)
warnings.simplefilter("once", DeprecationWarning)


parser = argparse.ArgumentParser(
    description="Run the test suite, or some tests. "
    "Also takes any options that can be passed to manage.py"
    " e.g. --failfast and --noinput"
)
parser.add_argument(
    "--show-browser",
    action="store_true",
    help="Show the browser when running Selenium tests",
)
parser.add_argument("--firefox-binary", action="store", help="Path to binary to use for Firefox tests")
parser.add_argument("--skip-selenium", action="store_true", help="Skip Selenium tests")
parser.add_argument(
    "--update-migration",
    action="store_true",
    help="Don't run tests - just update the migration used for tests",
)
parser.add_argument("--signed-cookies", action="store_true", help="Use signed cookies session backend")
parser.add_argument(
    "-v",
    "--verbosity",
    action="store",
    dest="verbosity",
    choices=[0, 1, 2, 3],
    type=int,
    help="Verbosity",
)
parser.add_argument(
    "--database",
    action="store",
    default="sqlite",
    choices=["sqlite", "postgres"],
    type=str,
    help="Database driver to test against",
)


known_args, remaining_args = parser.parse_known_args()

remaining_options = [a for a in remaining_args if a.startswith("-")]
test_args = [a for a in remaining_args if not a.startswith("-")]

if known_args.database == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "main.db",
            "CONN_MAX_AGE": 0,
            "TEST": {
                "NAME": "tests.db",
            },
        }
    }
elif known_args.database == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "djangofunctest",
            "USER": "djangofunctest",
            "PASSWORD": "djangofunctest",
            "HOST": "localhost",
            "CONN_MAX_AGE": 0,
        }
    }


settings_dict = dict(
    DEBUG=True,
    USE_TZ=True,
    DATABASES=DATABASES,
    ROOT_URLCONF="django_functest.tests.urls",
    INSTALLED_APPS=[
        # First, see http://stackoverflow.com/questions/18281137/selenium-django-gives-foreign-key-error/18292090#18292090 # noqa
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django_functest",
        "django_functest.tests",
    ],
    SITE_ID=1,
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ],
    STATIC_URL="/static/",
    STATIC_ROOT=os.path.join(os.path.abspath(os.path.dirname(__file__)), "/tmp_static/"),
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ],
    LOGGING={
        "version": 1,
        "disable_existing_loggers": True,
        "root": {
            "level": "WARNING",
            "handlers": ["console"],
        },
        "formatters": {
            "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
    },
    SECRET_KEY="foo",
)

if known_args.signed_cookies:
    settings_dict["SESSION_ENGINE"] = "django.contrib.sessions.backends.signed_cookies"

if django.VERSION < (1, 10):
    settings_dict["MIDDLEWARE_CLASSES"] = settings_dict.pop("MIDDLEWARE")


settings.configure(**settings_dict)


try:
    setup = django.setup
except AttributeError:
    pass
else:
    setup()

if known_args.show_browser:
    from django_functest.tests.base import HideBrowserMixin

    HideBrowserMixin.display = True


def set_firefox_binary(path):
    from django_functest.tests.base import FirefoxBase

    FirefoxBase.firefox_binary = path


if known_args.firefox_binary:
    set_firefox_binary(known_args.firefox_binary)
elif "TEST_FIREFOX_BINARY" in os.environ:
    set_firefox_binary(os.environ["TEST_FIREFOX_BINARY"])

if known_args.skip_selenium:
    os.environ["TEST_SKIP_SELENIUM"] = "TRUE"

if known_args.update_migration:
    initial_migration = "django_functest/tests/migrations/0001_initial.py"
    if os.path.exists(initial_migration):
        os.unlink(initial_migration)
    argv = [sys.argv[0], "makemigrations", "tests"] + sys.argv[2:]
else:
    argv = [sys.argv[0], "test", "--noinput"]
    if known_args.verbosity:
        argv.extend(["-v", str(known_args.verbosity)])
    if len(test_args) == 0:
        argv.extend(["django_functest.tests"])
    else:
        argv.extend(test_args)

    argv.extend(remaining_options)

# Run like 'manage.py', so we can get the options it has.
execute_from_command_line(argv)
