#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: example_version_of_this_package.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api
# Documentation: https://www.unicorn-data.com/unicorn-binance-websocket-api.html
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: UNICORN Data Analysis
#         https://www.unicorn-data.com/
#
# Copyright (c) 2019, UNICORN Data Analysis
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager

# create instance of BinanceWebSocketApiManager
binance_websocket_api_manager = BinanceWebSocketApiManager()

# get version of the used UNICORN Binance WebSocket API
if binance_websocket_api_manager.is_update_availabe():
    print("yes, please upgrade to " + binance_websocket_api_manager.get_latest_version() + ", you are on", binance_websocket_api_manager.get_version())

    latest_release_info = binance_websocket_api_manager.get_latest_release_info()
    if latest_release_info:
        print("please download the latest release or run `pip install unicorn-binance-websocket-api --upgrade`: ")
        print("\ttar: " + latest_release_info["tarball_url"])
        print("\tzip: " + latest_release_info["zipball_url"])
        print("release info:")
        print(latest_release_info["body"])
else:
    print("no,", binance_websocket_api_manager.get_version(), "is the latest version!")


binance_websocket_api_manager.stop_manager_with_all_streams()
