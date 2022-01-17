#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev_live_demo.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://lucit-systems-and-development.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: LUCIT Systems and Development
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

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import math
import os
import requests
import sys
import time
import threading

try:
    import unicorn_binance_rest_api
except ImportError:
    print("Please install `unicorn-binance-rest-api`! https://pypi.org/project/unicorn-binance-rest-api/")
    sys.exit(1)
try:
    import IPython
except ImportError:
    print("Please install `ipython`!")
    sys.exit(1)

binance_api_key = ""
binance_api_secret = ""

#channels = {'aggTrade', 'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h',
#            'kline_6h', 'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M', 'miniTicker',
#            'ticker', 'bookTicker', 'depth5', 'depth10', 'depth20', 'depth', 'depth@100ms'}
channels = {'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h',
            'kline_1d', 'miniTicker', 'ticker', 'bookTicker', 'depth20', 'depth@100ms'}
arr_channels = {'!miniTicker', '!ticker', '!bookTicker'}

logging.getLogger("unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is not False:
            pass
        else:
            time.sleep(0.01)


def print_stream_to_png(manager):
    while True:
        manager.print_summary_to_png("/var/www/html/", hight_per_row=13.5)
        time.sleep(10)


try:
    binance_rest_client = unicorn_binance_rest_api.BinanceRestApiManager(binance_api_key, binance_api_secret)
    ws_manager = BinanceWebSocketApiManager()
except requests.exceptions.ConnectionError:
    print("No internet connection?")
    sys.exit(1)

worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(ws_manager,))
worker_thread.start()

export_thread = threading.Thread(target=print_stream_to_png, args=(ws_manager,))
export_thread.start()

markets = []
data = binance_rest_client.get_all_tickers()
for item in data:
    markets.append(item['symbol'])

userdata_stream_id = ws_manager.create_stream(["!userData"],
                                              ["arr"],
                                              "userData stream",
                                              api_key=binance_api_key,
                                              api_secret=binance_api_secret)
arr_stream_id = ws_manager.create_stream(arr_channels, "arr", "arr channels")

divisor = math.ceil(len(markets) / ws_manager.get_limit_of_subscriptions_per_stream())
max_subscriptions = math.ceil(len(markets) / divisor)

for channel in channels:
    if len(markets) <= max_subscriptions:
        ws_manager.create_stream(channel, markets, stream_label=channel)
    else:
        loops = 1
        i = 1
        markets_sub = []
        for market in markets:
            markets_sub.append(market)
            if i == max_subscriptions or loops*max_subscriptions + i == len(markets):
                ws_manager.create_stream(channel, markets_sub, stream_label=str(channel+"_"+str(i)))
                markets_sub = []
                i = 1
                loops += 1
            i += 1

IPython.embed()
