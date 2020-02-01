#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_binance_dex.py
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
import time
import threading
import os


# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
logging.getLogger('unicorn-log').addHandler(logging.StreamHandler())
logging.getLogger('unicorn-log').setLevel(logging.INFO)


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
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.org")

print("starting monitoring api!")
binance_websocket_api_manager.start_monitoring_api()

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

# userAddress streams
#binance_dex_user_address = ""
#id = binance_websocket_api_manager.create_stream('orders', binance_dex_user_address)
#binance_websocket_api_manager.create_stream('accounts', binance_dex_user_address)
#binance_websocket_api_manager.create_stream('transfers', binance_dex_user_address)
#user_address_multi_stream_id = binance_websocket_api_manager.create_stream(['orders', 'transfers', 'accounts'],
#                                                                           binance_dex_user_address)

binance_websocket_api_manager.create_stream(["allTickers"], ["$all"])
binance_websocket_api_manager.create_stream(["allMiniTickers"], ["$all"])
binance_websocket_api_manager.create_stream(["blockheight"], ["$all"])

markets = 'RAVEN-F66_BNB'
binance_websocket_api_manager.create_stream(["trades"], markets)
binance_websocket_api_manager.create_stream(["marketDepth"], markets)
binance_websocket_api_manager.create_stream(["kline_1h"], markets)
binance_websocket_api_manager.create_stream(["kline_1h"], markets)
binance_websocket_api_manager.create_stream(["ticker"], markets)
binance_websocket_api_manager.create_stream(["miniTicker"], markets)

markets = ['RAVEN-F66_BNB', 'ANKR-E97_BNB', 'AWC-986_BNB', 'COVA-218_BNB', 'BCPT-95A_BNB', 'WISH-2D5_BNB',
           'MITH-C76_BNB', 'BNB_BTCB-1DE', 'BNB_USDSB-1AC', 'BTCB-1DE_USDSB-1AC', 'NEXO-A84_BNB']
channels = ['trades']
channels = ['kline_1m', 'kline_5m', 'kline_15m', 'marketDepth', 'ticker', 'miniTicker', 'marketDiff', 'trades']
multiplex_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
if binance_websocket_api_manager.wait_till_stream_has_started(multiplex_stream_id):
    binance_websocket_api_manager.print_stream_info(multiplex_stream_id)
    time.sleep(5)

    binance_websocket_api_manager.subscribe_to_stream(multiplex_stream_id,
                                                      channels=['kline_1m', 'kline_5m', 'kline_15m', 'marketDepth',
                                                                'ticker', 'miniTicker', 'marketDiff'])

stream_id = binance_websocket_api_manager.create_stream(["kline_1m"], ['RAVEN-F66_BNB'])

while True:
    binance_websocket_api_manager.print_summary()
    #binance_websocket_api_manager.print_stream_info(stream_id)
    time.sleep(1)
