#!/bin/sh

./setup.py sdist || exit 1

# Different wheels are needed for py2 and py3 because of the faulthandler
# dependency:

python2.7 setup.py bdist_wheel --python-tag=py2 || exit 1
python3.4 setup.py bdist_wheel --python-tag=py3 || exit 1

VERSION=$(./setup.py --version) || exit 1
twine upload dist/django-functest-$VERSION.tar.gz dist/django_functest-$VERSION-py2-none-any.whl dist/django_functest-$VERSION-py3-none-any.whl || exit 1
