Release process
===============

* Tests, including flake8, isort and check-manifest:

  https://github.com/django-functest/django-functest/actions?query=workflow%3A%22Python+package%22+branch%3Amaster

* Update HISTORY.rst, removing "(under development)" and adding date. Commit.

* Update the version number, removing the ``-dev1`` part if present

  * setup.py
  * django_functest/__init__.py
  * docs/conf.py

* Make sure all is committed

* Release to PyPI::

    ./release.sh

* Tag the release e.g.::

    git tag v0.1.0

* Update the version numbers again, moving to the next release, and adding "-dev1"

* Add new section to HISTORY.rst

* ``git push --tags``
