#!/bin/sh

umask 000
git ls-tree --full-tree --name-only -r HEAD | xargs chmod ugo+r
./setup.py sdist || exit 1
python setup.py bdist_wheel || exit 1

VERSION=$(./setup.py --version) || exit 1
twine upload dist/django-functest-$VERSION.tar.gz dist/django_functest-$VERSION-*.whl || exit 1
