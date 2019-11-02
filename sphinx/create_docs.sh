#!/usr/bin/env bash

# pip install sphinx
# mkdir sphinx
# cd sphinx
# sphinx-quickstart

## edit source/conf.py
# import os
# import sys
# sys.path.insert(0, os.path.abspath('../..'))

# sphinx-apidoc -f -o source/ ../unicorn_binance_websocket_api/

# pip install python_docs_theme
## edit source/conf.py:
# html_theme = 'python_docs_theme'

# pip install recommonmark
# add 'recommonmark' to extentions in conf.py

make html -d
