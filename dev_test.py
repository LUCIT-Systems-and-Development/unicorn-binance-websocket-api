#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: dev_test.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api
# Documentation: https://www.unicorn-data.com/unicorn-binance-websocket-api.html
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

markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt', 'bnbbtc', 'ethbtc', 'btcusdt', 'bnbustd',
           'bchabcusdt', 'eosusdt'}

# Multi types and multi market socket (all types X all markets)
channels = {'trade', 'kline_1', 'kline_5', 'kline_15', 'kline_30', 'kline_1h', 'kline_12h', 'kline_1w',
                'miniTicker', 'depth20', '!miniTicker', '!ticker', '!userData'}

id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(id)
time.sleep(30)
id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(id)
time.sleep(30)
id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(id)
time.sleep(30)
id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(id)
time.sleep(30)
id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(id)

# This sockets can not get combined with other streams
#binance_websocket_api_manager.create_stream(["arr", ["!miniTicker"])
#binance_websocket_api_manager.create_stream(["arr", ["!ticker"])
#binance_websocket_api_manager.create_stream(["arr", ["!userData"])
# MULTI MARKET SOCKET
#binance_websocket_api_manager.create_stream(["aggTrade"], markets)
#binance_websocket_api_manager.create_stream(["trade"], markets)
#binance_websocket_api_manager.create_stream(["kline_1m"], markets)
#binance_websocket_api_manager.create_stream(["kline_5m"], markets)
#binance_websocket_api_manager.create_stream(["miniTicker"], markets)
#binance_websocket_api_manager.create_stream(["ticker"], markets)
#binance_websocket_api_manager.create_stream(["depth5"], markets)
#binance_websocket_api_manager.create_stream(["depth10"], ['xrpusdt'])
#binance_websocket_api_manager.create_stream(["depth"], markets)

print("\r\n=============================== Stopping BinanceWebSocketManager ======================================\r\n")
binance_websocket_api_manager.stop_manager_with_all_streams()
print("finished!")
