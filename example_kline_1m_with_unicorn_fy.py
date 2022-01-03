#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_kline_1m_with_unicorn_fy.py
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

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import logging
import time
import os


# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com", output_default="UnicornFy")

markets = {'bnbbtc', 'ethbtc', 'btcusdt', 'bchabcusdt', 'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt',
           'neousdt', 'bnbusdt', 'adabtc', 'ethusdt', 'trxbtc', 'bchabcbtc', 'ltcbtc', 'xrpbtc',
           'ontbtc', 'bttusdt', 'eosbtc', 'xlmbtc', 'bttbtc', 'tusdusdt', 'xlmusdt', 'qkcbtc', 'zrxbtc',
           'neobtc', 'adaeth', 'icxusdt', 'btctusd', 'icxbtc', 'btcusdc', 'wanbtc', 'zecbtc', 'wtcbtc',
           'batbtc', 'adabnb', 'etcusdt', 'qtumusdt', 'xmrbtc', 'trxeth', 'adatusd', 'trxxrp', 'trxbnb',
           'dashbtc', 'rvnbnb', 'bchabctusd', 'etcbtc', 'bnbeth', 'ethpax', 'nanobtc', 'xembtc', 'xrpbnb',
           'bchabcpax', 'xrpeth', 'bttbnb', 'ltcbnb', 'agibtc', 'zrxusdt', 'xlmbnb', 'ltceth', 'eoseth',
           'ltctusd', 'polybnb', 'scbtc', 'steembtc', 'trxtusd', 'npxseth', 'kmdbtc', 'polybtc', 'gasbtc',
           'engbtc', 'zileth', 'xlmeth', 'eosbnb', 'xrppax', 'lskbtc', 'npxsbtc', 'xmrusdt', 'ltcpax',
           'ethtusd', 'batusdt', 'mcobtc', 'neoeth', 'bntbtc', 'eostusd', 'lrcbtc', 'funbtc', 'zecusdt',
           'bnbpax', 'linkusdt', 'hceth', 'zrxeth', 'icxeth', 'xmreth', 'neobnb', 'etceth', 'zeceth', 'xmrbnb',
           'wanbnb', 'zrxbnb', 'agibnb', 'funeth', 'arketh', 'engeth'}

binance_websocket_api_manager.create_stream('kline_1m', markets, stream_label="UnicornFy", output="UnicornFy")

binance_websocket_api_manager.create_stream('kline_1m', markets, stream_label="dict", output="dict")

binance_websocket_api_manager.create_stream('kline_1m', markets, stream_label="raw_data", output="raw_data")

while True:
    if binance_websocket_api_manager.is_manager_stopping():
        exit(0)
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    if oldest_stream_data_from_stream_buffer is False:
        time.sleep(0.01)
    else:
        if oldest_stream_data_from_stream_buffer is not None:
            try:
                if oldest_stream_data_from_stream_buffer['event_time'] >= \
                        oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                    # print only the last kline
                    print(f"UnicornFy: {oldest_stream_data_from_stream_buffer}")
            except KeyError:
                print(f"dict: {oldest_stream_data_from_stream_buffer}")
            except TypeError:
                print(f"raw_data: {oldest_stream_data_from_stream_buffer}")
