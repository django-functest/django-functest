import os.path

import conftest

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "main.db",
        "CONN_MAX_AGE": 0,
    }
}


DEBUG = True
USE_TZ = True
ROOT_URLCONF = "django_functest_tests.urls"
INSTALLED_APPS = [
    # First, see http://stackoverflow.com/questions/18281137/selenium-django-gives-foreign-key-error/18292090#18292090 # noqa
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django_functest",
    "django_functest_tests",
]
SITE_ID = 1
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "/tmp_static/")
TEMPLATES = [
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
]

LOGGING = {
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
}
SECRET_KEY = "foo"


if conftest.SIGNED_COOKIES:
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
