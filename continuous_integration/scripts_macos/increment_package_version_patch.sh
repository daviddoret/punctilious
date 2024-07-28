#!/bin/sh

pip install --upgrade bumpver
python -m bumpver update --patch
#python -m bumpver update --minor
#python -m bumpver update --major