#!/bin/sh

uv sync
test $(git rev-parse --abbrev-ref HEAD | tr -d '\n') = 'master' || { echo "Must be on master branch"; exit 1; }
uv run check-manifest || exit 1

umask 000
rm -rf build dist
git ls-tree --full-tree --name-only -r HEAD | xargs chmod ugo+r
uv build --sdist --wheel || exit 1
uv publish || exit 1

VERSION=$(uv pip show django-functest | grep 'Version: ' | cut -f 2 -d ' ' | tr -d '\n') || exit 1

git tag $VERSION || exit 1
git push || exit 1
git push --tags || exit 1
