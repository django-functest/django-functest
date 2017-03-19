Release process
===============

* Tests, including flake8, isort and check-manifest

* Update HISTORY.rst, removing "(in development)". Commit.

* Update the version number, removing the ``-dev`` part

  * setup.py
  * django_functest/__init__.py
  * docs/conf.py

* Make sure all is committed

* Release to PyPI::

    ./release.sh

* Tag the release e.g.::

    git tag v0.1.0

* Update the version numbers again, moving to the next release, and adding "-dev"

* Add new section to HISTORY.rst

* ``git push --tags``
