#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_ticker_and_miniticker.py
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
import time
import logging

# import class to process stream data
from unicorn_binance_websocket_api_process_streams import BinanceWebSocketApiProcessStreams

# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
logging.getLogger('unicorn-log').setLevel(logging.INFO)
logging.getLogger('unicorn-log').addHandler(logging.StreamHandler())

# create instance of BinanceWebSocketApiManager and provide the function for stream processing
binance_websocket_api_manager = BinanceWebSocketApiManager(BinanceWebSocketApiProcessStreams.process_stream_data)

# create streams
print("\r\n========================================== Starting ticker all ========================================\r\n")
ticker_arr_stream_id = binance_websocket_api_manager.create_stream("arr", "!ticker")
time.sleep(7)
binance_websocket_api_manager.stop_stream(ticker_arr_stream_id)
time.sleep(2)
print("\r\n=========================================== Stopp ticker all ==========================================\r\n")

print("\r\n============================================ Starting ticker ==========================================\r\n")
ticker_stream_id = binance_websocket_api_manager.create_stream("ticker", ['bnbbtc', 'ethbtc'])
time.sleep(7)
binance_websocket_api_manager.stop_stream(ticker_stream_id)
time.sleep(2)
print("\r\n============================================== Stop ticker  ===========================================\r\n")

print("\r\n======================================== Starting !miniTicker arr =====================================\r\n")
miniTicker_arr_stream_id = binance_websocket_api_manager.create_stream("arr", "!miniTicker")
time.sleep(7)
binance_websocket_api_manager.stop_stream(miniTicker_arr_stream_id)
time.sleep(2)
print("\r\n========================================== Stop !miniTicker arr =======================================\r\n")

print("\r\n========================================== Starting miniTicker ========================================\r\n")
miniTicker_stream_id = binance_websocket_api_manager.create_stream("miniTicker", ['bnbbtc', 'ethbtc'])
time.sleep(7)
binance_websocket_api_manager.stop_stream(miniTicker_stream_id)
time.sleep(7)
print("\r\n============================================ Stop miniTicker==========================================\r\n")

binance_websocket_api_manager.print_summary()

binance_websocket_api_manager.stop_manager_with_all_streams()