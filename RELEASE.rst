Release process
===============

* Tests, including flake8 and check-manifest

* Update HISTORY.rst, removing "(in development)"

* Use bumpversion e.g.

  bumpversion release

* Make sure all is committed

* Release to PyPI::

    ./setup.py sdist bdist_wheel register upload

* bumpversion again

  bumpversion --no-tag patch

* Add new section to HISTORY.rst

* ``git push --tags``
