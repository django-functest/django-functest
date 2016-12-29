#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa  (for FI14 error)
from __future__ import absolute_import, print_function


import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.1.9"

if sys.argv[-1] == 'publish':
    try:
        import wheel  # noqa
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

if sys.version_info < (3, 3):
    extra_requires = ['faulthandler>=2.4']
else:
    extra_requires = []


setup(
    name='django-functest',
    version=version,
    description="""Helpers for creating functional tests in Django, with a unified API for WebTest and Selenium tests.""",  # noqa
    long_description=readme + '\n\n' + history,
    author='Luke Plant',
    author_email='L.Plant.98@cantab.net',
    url='https://github.com/django-functest/django-functest',
    packages=[
        'django_functest',
    ],
    include_package_data=True,
    install_requires=[
        'django-webtest>=1.7.8',
        'selenium>=2.48.0',
        'PyVirtualDisplay>=0.1.4',
        'six>=1.10.0',
        'furl>=0.4.9',
        'pyquery>=1.2.10',
    ] + extra_requires,
    license="BSD",
    zip_safe=False,
    keywords='django-functest',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
