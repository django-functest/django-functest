Release process
===============

* Tests, including flake8, isort and check-manifest

* Update HISTORY.rst, removing "(in development)". Commit.

* Use bumpversion e.g.::

      bumpversion release

* Check the commit log and undo any nastiness that bumpversion did to setup.cfg

* Make sure all is committed

* Release to PyPI::

    ./release.sh

* bumpversion again::

      bumpversion --no-tag patch

  And fix again.

* Add new section to HISTORY.rst

* ``git push --tags``
