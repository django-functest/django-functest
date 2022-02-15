#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "1.3"

if sys.argv[-1] == "publish":
    try:
        import wheel  # noqa
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on github:")
    os.system(f"git tag -a {version} -m 'version {version}'")
    os.system("git push --tags")
    sys.exit()

readme = open("README.rst").read()

setup(
    name="django-functest",
    version=version,
    description="""Helpers for creating functional tests in Django, with a unified API for WebTest and Selenium tests.""",  # noqa
    long_description=readme,
    author="Luke Plant",
    author_email="L.Plant.98@cantab.net",
    url="https://github.com/django-functest/django-functest",
    packages=[
        "django_functest",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        "django-webtest>=1.9.9",
        "WebTest>=3",
        "selenium>=4",
        "furl>=0.4.9",
        "pyquery>=1.2.10",
        "Django>=2.0",
    ],
    license="BSD",
    zip_safe=False,
    keywords="django-functest",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
