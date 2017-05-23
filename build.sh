#!/usr/bin/env bash
cd doc
make html
cd ..
python3 setup.py sdist --formats=zip
