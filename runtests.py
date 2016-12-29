#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import argparse
import os
import os.path
import signal
import sys

import faulthandler
from django.conf import settings
from django.core.management import execute_from_command_line

# If the process receives signal SIGUSR1, dump a traceback
faulthandler.enable()
faulthandler.register(signal.SIGUSR1)


parser = argparse.ArgumentParser(description="Run the test suite, or some tests. "
                                 "Also takes any options that can be passed to manage.py"
                                 " e.g. --failfast and --noinput")
parser.add_argument("--show-browser", action='store_true',
                    help="Show the browser when running Selenium tests")
parser.add_argument("--firefox-binary", action='store',
                    help="Path to binary to use for Firefox tests")
parser.add_argument("--update-migration", action='store_true',
                    help="Don't run tests - just update the migration used for tests")
parser.add_argument("-v", "--verbosity", action='store', dest="verbosity",
                    choices=[0, 1, 2, 3], type=int,
                    help="Verbosity")


known_args, remaining_args = parser.parse_known_args()

remaining_options = [a for a in remaining_args if a.startswith('-')]
test_args = [a for a in remaining_args if not a.startswith('-')]


settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "tests.db",
            "CONN_MAX_AGE": None,
        }
    },
    ROOT_URLCONF="django_functest.tests.urls",
    INSTALLED_APPS=[
        # First, see http://stackoverflow.com/questions/18281137/selenium-django-gives-foreign-key-error/18292090#18292090 # noqa
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.staticfiles",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django_functest",
        "django_functest.tests",
    ],
    SITE_ID=1,
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    STATIC_URL="/static/",
    STATIC_ROOT=os.path.join(os.path.abspath(os.path.dirname(__file__)), "/tmp_static/"),
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    LOGGING={
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        }
    }
)

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()

if known_args.show_browser:
    from django_functest.tests.base import HideBrowserMixin
    HideBrowserMixin.display = True

if known_args.firefox_binary:
    from django_functest.tests.base import FirefoxBase
    FirefoxBase.firefox_binary = known_args.firefox_binary

if known_args.update_migration:
    initial_migration = "django_functest/tests/migrations/0001_initial.py"
    if os.path.exists(initial_migration):
        os.unlink(initial_migration)
    argv = [sys.argv[0], "makemigrations", "tests"] + sys.argv[2:]
else:
    argv = [sys.argv[0], "test"]
    if known_args.verbosity:
        argv.extend(["-v", str(known_args.verbosity)])
    if len(test_args) == 0:
        argv.extend(["django_functest.tests"])
    else:
        argv.extend(test_args)

    argv.extend(remaining_options)

# Run like 'manage.py', so we can get the options it has.
execute_from_command_line(argv)
