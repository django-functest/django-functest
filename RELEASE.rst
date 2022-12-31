Release process
===============

* Tests, including flake8, isort and check-manifest:

  https://github.com/django-functest/django-functest/actions?query=workflow%3A%22Python+package%22+branch%3Amaster

* Make sure you have pulled latest master locally and are on the master branch.

* Update HISTORY.rst, removing "(unreleased)" and adding date.

* Update the version number, removing the ``-dev1`` part if present

  * django_functest/__init__.py
  * docs/conf.py

* Commit.

* Release to PyPI::

    ./release.sh

* Update the version numbers again, moving to the next release, and adding "-dev1"

* Add new section to HISTORY.rst
