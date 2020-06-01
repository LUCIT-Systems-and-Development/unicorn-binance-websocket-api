#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev_test_heartbeat.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019, Oliver Zehentleitner
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
import logging
import IPython
import sys
import time
import os
try:
    from unicorn_fy.unicorn_fy import UnicornFy
except ImportError:
    print("Please install `unicorn-fy`! https://pypi.org/project/unicorn-fy/")
    sys.exit(1)


# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")

binance_api_key = "I25sjQLfPuTBzMGNiHGPFq7UpxSZ9kdjjvgBri20sDHxJqFG21WabzpHAk1P9To1"
binance_api_secret = "ogrjfEnUpokY8VKKtlPNNUS3iWTqX9QuwS5vYwcs8fBThIRhQn4AyNL35cRWhuz5"

binance_websocket_api_manager.set_private_api_config(binance_api_key, binance_api_secret)
userdata_stream_id = binance_websocket_api_manager.create_stream(["!userData"], ["arr"], "userData stream")

ubwa = binance_websocket_api_manager
IPython.embed()
