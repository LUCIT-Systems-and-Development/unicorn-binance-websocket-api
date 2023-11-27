#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev/test_live_demo.py
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
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech)
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

import logging
import math
import os
import requests
import sys
import time
import threading

try:
    from unicorn_binance_rest_api.manager import BinanceRestApiManager
except ImportError:
    print("Please install `unicorn-binance-rest-api`! "
          "https://www.lucit.tech/unicorn-binance-rest-api.html#installation-and-upgrade")
    sys.exit(1)

try:
    from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
except ImportError:
    print("Please install `unicorn-binance-rest-api`! "
          "https://www.lucit.tech/unicorn-binance-websocket-api.html#installation-and-upgrade")
    sys.exit(1)

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

binance_api_key = ""
binance_api_secret = ""
exchange = "binance.com"

arr_channels = {'!miniTicker', '!ticker', '!bookTicker'}

channels = {'trade', 'kline_1m', 'depth20'}
# channels = {'aggTrade', 'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h',
#            'kline_6h', 'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M', 'miniTicker',
#            'ticker', 'bookTicker', 'depth5', 'depth10', 'depth20', 'depth', 'depth@100ms'}


def print_stream_data_from_stream_buffer(ubwa_manager):
    while True:
        if ubwa_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = ubwa_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is not False:
            # print(oldest_stream_data_from_stream_buffer)
            pass
        else:
            time.sleep(0.01)

# To use this library you need a valid UNICORN Binance Suite License:
# https://medium.lucit.tech/87b0088124a8
try:
    ubra = BinanceRestApiManager(exchange=exchange)
    ubwa = BinanceWebSocketApiManager(exchange=exchange)
except requests.exceptions.ConnectionError:
    print("No internet connection?")
    sys.exit(1)

worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(ubwa,))
worker_thread.start()

markets = []
data = ubra.get_all_tickers()
for item in data:
    markets.append(item['symbol'])

userdata_stream_id = ubwa.create_stream(["!userData"],
                                        ["arr"],
                                        "userData stream",
                                        api_key=binance_api_key,
                                        api_secret=binance_api_secret)

arr_stream_id = ubwa.create_stream(arr_channels, "arr", "arr channels")

divisor = math.ceil(len(markets) / ubwa.get_limit_of_subscriptions_per_stream())
max_subscriptions = math.ceil(len(markets) / divisor)

for channel in channels:
    if len(markets) <= max_subscriptions:
        ubwa.create_stream(channel, markets, stream_label=channel)
    else:
        loops = 1
        i = 1
        markets_sub = []
        for market in markets:
            markets_sub.append(market)
            if i == max_subscriptions or loops*max_subscriptions + i == len(markets):
                ubwa.create_stream(channel, markets_sub, stream_label=str(channel+"_"+str(i)))
                markets_sub = []
                i = 1
                loops += 1
            i += 1

while True:
    if ubwa.is_manager_stopping() is False:
        ubwa.print_summary()
        time.sleep(1)
