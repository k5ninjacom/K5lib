#!/usr/bin/env bash
pycodestyle --count --ignore=E121,E123,E126,E226,E24,E704,W503,E501 k5lib
#pydocstyle --count k5lib
