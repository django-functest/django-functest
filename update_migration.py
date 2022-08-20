#!/usr/bin/env python

import os
import os.path
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line

settings_dict = dict(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "main.db",
            "CONN_MAX_AGE": 0,
            "TEST": {
                "NAME": "tests.db",
            },
        }
    },
    INSTALLED_APPS=[
        "django_functest",
        "django_functest_tests",
    ],
)


settings.configure(**settings_dict)


try:
    setup = django.setup
except AttributeError:
    pass
else:
    setup()

initial_migration = "tests/django_functest_tests/migrations/0001_initial.py"
if os.path.exists(initial_migration):
    os.unlink(initial_migration)
argv = [sys.argv[0], "makemigrations", "tests"] + sys.argv[2:]
execute_from_command_line(argv)
