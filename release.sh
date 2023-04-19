#!/bin/sh

test $(git rev-parse --abbrev-ref HEAD | tr -d '\n') = 'master' || { echo "Must be on master branch"; exit 1; }
check-manifest || exit 1

umask 000
git ls-tree --full-tree --name-only -r HEAD | xargs chmod ugo+r
python setup.py sdist || exit 1
python setup.py bdist_wheel || exit 1

VERSION=$(python setup.py --version) || exit 1
twine upload dist/django-functest-$VERSION.tar.gz dist/django_functest-$VERSION-*.whl || exit 1
git tag v$VERSION || exit 1
git push || exit 1
git push --tags || exit 1
