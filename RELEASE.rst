Release process
===============

* Tests, including flake8, isort and check-manifest

* Update HISTORY.rst, removing "(in development)". Commit.

* Use bumpversion e.g.

  bumpversion release

* Make sure all is committed

* Release to PyPI::

    ./release.sh

* bumpversion again

  bumpversion --no-tag patch

* Add new section to HISTORY.rst

* ``git push --tags``
