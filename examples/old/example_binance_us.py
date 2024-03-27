#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_binance_us.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api
# LUCIT Online Shop: https://shop.lucit.services/software
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2024, LUCIT Systems and Development (https://www.lucit.tech)
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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import time
import threading
import os


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is None:
            time.sleep(0.01)


logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# To use this library you need a valid UNICORN Binance Suite License:
# https://medium.lucit.tech/87b0088124a8

# create instance of BinanceWebSocketApiManager for Binance US
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.us")

userdata_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!userData"], api_key="aaa", api_secret="bb")

ticker_all_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!ticker"])
miniticker_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!miniTicker"])

markets = {'btcusd', 'btcxrp', 'ethusd', 'bnbusd', 'busdusd'}

binance_websocket_api_manager.create_stream(["aggTrade"], markets)
binance_websocket_api_manager.create_stream(["trade"], markets)
binance_websocket_api_manager.create_stream(["kline_1m"], markets)
binance_websocket_api_manager.create_stream(["kline_5m"], markets)
binance_websocket_api_manager.create_stream(["kline_15m"], markets)
binance_websocket_api_manager.create_stream(["kline_1h"], markets)
binance_websocket_api_manager.create_stream(["kline_12h"], markets)
binance_websocket_api_manager.create_stream(["kline_1w"], markets)
binance_websocket_api_manager.create_stream(["ticker"], markets)
binance_websocket_api_manager.create_stream(["miniTicker"], markets)
binance_websocket_api_manager.create_stream(["depth"], markets)
binance_websocket_api_manager.create_stream(["depth5"], markets)
binance_websocket_api_manager.create_stream(["depth10"], markets)
binance_websocket_api_manager.create_stream(["depth20"], markets)
binance_websocket_api_manager.create_stream(["aggTrade"], markets)


channels = {'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'kline_1w',
            'miniTicker', 'depth20'}
binance_websocket_api_manager.create_stream(channels, markets)

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

# show an overview
while True:
    binance_websocket_api_manager.print_summary()
    time.sleep(1)
