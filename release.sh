#!/bin/sh

umask 000
./setup.py sdist || exit 1

# Different wheels are needed for CPython 2/CPython 3/PyPy because of the faulthandler
# dependency:

python2.7 setup.py bdist_wheel --python-tag=cp2 || exit 1
python3.5 setup.py bdist_wheel --python-tag=cp3 || exit 1
pypy setup.py bdist_wheel --python-tag=pp || exit 1

VERSION=$(./setup.py --version) || exit 1
twine upload dist/django-functest-$VERSION.tar.gz dist/django_functest-$VERSION-cp2-none-any.whl dist/django_functest-$VERSION-cp3-none-any.whl dist/django_functest-$VERSION-pp-none-any.whl || exit 1
