Release process
===============

* Tests, including flake8, isort and check-manifest:

  https://github.com/django-functest/django-functest/actions?query=workflow%3A%22Python+package%22+branch%3Amaster


* Update HISTORY.rst, removing "(unreleased)" and adding date.

* From the last test run on CI, add version numbers of Firefox/Chrome etc. into
  the table in installation.rst.

* Update the version number, removing the ``-dev1`` part if present

  * setup.py
  * django_functest/__init__.py
  * docs/conf.py

* Commit.

* Release to PyPI::

    ./release.sh

* Tag the release e.g.::

    git tag v0.1.0

* Update the version numbers again, moving to the next release, and adding "-dev1"

* Add new section to HISTORY.rst

* ``git push --tags``
