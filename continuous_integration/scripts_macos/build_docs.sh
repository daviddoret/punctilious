#!/bin/sh

PROJECT_PATH=$(cd "$(dirname "$0")/../.."; pwd -P) || exit
ECHO "$DOCS_PATH"

DOCS_PATH=$(cd "$(dirname "$0")/../../docs"; pwd -P) || exit
ECHO "$DOCS_PATH"

DOCS_SOURCE_PATH=$(cd "$(dirname "$0")/../../docs/source"; pwd -P) || exit
ECHO "$DOCS_SOURCE_PATH"

DOCS_BUILD_PATH=$(cd "$(dirname "$0")/../../docs/build"; pwd -P) || exit
ECHO "$DOCS_BUILD_PATH"


python -m pip install --upgrade --no-cache-dir pip setuptools

python -m pip install --upgrade --no-cache-dir sphinx readthedocs-sphinx-ext

#python -m pip install --exists-action=w --no-cache-dir -r "$DOCS_PATH/requirements.txt"

#python -m pip install --exists-action=w --no-cache-dir -r "$PROJECT_PATH/requirements.txt"

#python -m pip install -e "$PROJECT_PATH"

which sphinx-quickstart

#python -m sphinx -T -E -b html -d _build/doctrees -D language=en "$DOCS_SOURCE_PATH" "$DOCS_BUILD_PATH"