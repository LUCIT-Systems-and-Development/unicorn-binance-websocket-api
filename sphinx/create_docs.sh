#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# File: sphinx/create_docs.sh
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/main/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

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
#python3 -m sphinx source ../docs
