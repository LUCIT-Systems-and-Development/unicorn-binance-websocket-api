#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev_test_dex.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://lucit-systems-and-development.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
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
import time
import threading
import os


logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)
        else:
            pass
            #print(oldest_stream_data_from_stream_buffer)


# create instance of BinanceWebSocketApiManager for Binance Chain DEX
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.org-testnet")

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

# userAddress streams
binance_dex_user_address = "bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6"
id = binance_websocket_api_manager.create_stream('orders', binance_dex_user_address)
binance_websocket_api_manager.create_stream('accounts', binance_dex_user_address)
binance_websocket_api_manager.create_stream('transfers', binance_dex_user_address)
user_address_multi_stream_id = binance_websocket_api_manager.create_stream(['orders', 'transfers', 'accounts'],
                                                                           binance_dex_user_address)

binance_websocket_api_manager.create_stream(["allTickers"], ["$all"])
binance_websocket_api_manager.create_stream(["allMiniTickers"], ["$all"])
binance_websocket_api_manager.create_stream(["blockheight"], ["$all"])

markets = ['0KI-0AF_BNB', '000-0E1_BNB', '1KVOLUME-D65_BNB', '81JIAN-3E8_BNB', 'AAA-B50_BNB', 'AAAAAA-BBA_BNB']
binance_websocket_api_manager.create_stream(["trades"], markets)
binance_websocket_api_manager.create_stream(["marketDepth"], markets)
binance_websocket_api_manager.create_stream(["kline_1m"], markets)
binance_websocket_api_manager.create_stream(["kline_1h"], markets)
binance_websocket_api_manager.create_stream(["ticker"], markets)
binance_websocket_api_manager.create_stream(["miniTicker"], markets)

channels = ['kline_1m', 'kline_5m', 'kline_15m', 'marketDepth', 'ticker', 'miniTicker', 'marketDiff', 'trades', 'allTickers']
multiplex_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
if binance_websocket_api_manager.wait_till_stream_has_started(multiplex_stream_id):
    binance_websocket_api_manager.print_stream_info(multiplex_stream_id)
    time.sleep(5)

    binance_websocket_api_manager.subscribe_to_stream(multiplex_stream_id,
                                                      channels=['kline_1m', 'kline_5m', 'kline_15m', 'marketDepth',
                                                                'ticker', 'marketDiff'])

stream_id = binance_websocket_api_manager.create_stream(["kline_1m"], markets)

while True:
    #binance_websocket_api_manager.print_summary()
    binance_websocket_api_manager.print_stream_info(multiplex_stream_id)
    time.sleep(1)
