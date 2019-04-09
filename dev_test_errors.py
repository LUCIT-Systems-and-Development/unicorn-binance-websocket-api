#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: dev_test_errors.py
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
import logging
import time

# import class to process stream data
from unicorn_binance_websocket_api_process_streams import BinanceWebSocketApiProcessStreams

# https://docs.python.org/3/library/logging.html#logging-levels
logging.getLogger('websockets').setLevel(logging.DEBUG)
logging.getLogger('websockets').addHandler(logging.StreamHandler())

# create instance of BinanceWebSocketApiManager and provide the callback function
binance_websocket_api_manager = BinanceWebSocketApiManager(BinanceWebSocketApiProcessStreams.process_stream_data)

markets = {'bnbbtc', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}

print("TESTING WRONG CHANNEL FORMAT")
trade_stream_id1 = binance_websocket_api_manager.create_stream("trade", markets)
time.sleep(5)
binance_websocket_api_manager.stop_stream(trade_stream_id1)
print("TESTING WRONG MARKET FORMAT")
trade_stream_id2 = binance_websocket_api_manager.create_stream(["trade"], "bnbbtc")
time.sleep(5)
binance_websocket_api_manager.stop_stream(trade_stream_id2)
print("TESTING !ticker and !miniTicker in multi stream")
trade_stream_id3 = binance_websocket_api_manager.create_stream("trade", ['eosusdt', '!ticket'])
binance_websocket_api_manager.stop_stream(trade_stream_id3)
time.sleep(5)
trade_stream_id3 = binance_websocket_api_manager.create_stream("trade", ['eosusdt', '!miniTicket'])
binance_websocket_api_manager.stop_stream(trade_stream_id3)
time.sleep(5)
trade_stream_id3 = binance_websocket_api_manager.create_stream("trade", ['eosusdt', '!userData'])
binance_websocket_api_manager.stop_stream(trade_stream_id3)
time.sleep(5)
print("TESTING UNKNOWN MARKET")
trade_stream_id4 = binance_websocket_api_manager.create_stream(["trade"], "unicorn-data")
time.sleep(5)
print("TESTING UNKNOWN CHANNEL")
trade_stream_id5 = binance_websocket_api_manager.create_stream(["unicorn-data"], "bnbbtc")

print("\r\ntrade_stream_list:")
print(binance_websocket_api_manager.get_stream_list())

print("\r\n=============================== Stopping BinanceWebSocketManager ======================================\r\n")
binance_websocket_api_manager.stop_manager_with_all_streams()
print("finished!")
