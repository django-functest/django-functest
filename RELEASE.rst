Release process
===============

* Tests, including flake8, isort and check-manifest

* Update HISTORY.rst, removing "(in development)". Commit.

* Use bumpversion e.g.

  bumpversion release

* Make sure all is committed

* Release to PyPI::

    ./setup.py sdist register upload
    python2.7 setup.py bdist_wheel --python-tag=py2 upload
    python3.4 setup.py bdist_wheel --python-tag=py3 upload

  (Different wheels are needed for py2 and py3 because of the faulthandler
  dependency).

* bumpversion again

  bumpversion --no-tag patch

* Add new section to HISTORY.rst

* ``git push --tags``
