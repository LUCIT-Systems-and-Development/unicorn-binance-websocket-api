#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: example_monitoring.py
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
import time
import logging
import os

# https://docs.python.org/3/library/logging.html
logging.basicConfig(filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
logging.getLogger('unicorn-log').setLevel(logging.INFO)
logging.getLogger('unicorn-log').addHandler(logging.StreamHandler())

# create instance of BinanceWebSocketApiManager and provide the function for stream processing
binance_websocket_api_manager = BinanceWebSocketApiManager()

# create streams
markets = {'bnbbtc', 'ethbtc', 'btcusdt', 'bchabcusdt', 'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt',
           'neousdt', 'bnbusdt', 'adabtc', 'ethusdt', 'trxbtc', 'trxbtc', 'bchabcbtc', 'ltcbtc', 'xrpbtc',
           'ontbtc', 'bttusdt', 'eosbtc', 'xlmbtc', 'bttbtc', 'tusdusdt', 'xlmusdt', 'qkcbtc', 'zrxbtc',
           'neobtc', 'adaeth', 'icxusdt', 'btctusd', 'icxbtc', 'btcusdc', 'wanbtc', 'zecbtc', 'wtcbtc',
           'batbtc', 'adabnb', 'etcusdt', 'qtumusdt', 'xmrbtc', 'trxeth', 'adatusd', 'trxxrp', 'trxbnb',
           'dashbtc', 'rvnbnb', 'bchabctusd', 'etcbtc', 'bnbeth', 'ethpax', 'nanobtc', 'xembtc', 'xrpbnb',
           'bchabcpax', 'xrpeth', 'bttbnb', 'ltcbnb', 'agibtc', 'zrxusdt', 'xlmbnb', 'ltceth', 'eoseth',
           'ltctusd', 'polybnb', 'scbtc', 'steembtc', 'trxtusd', 'npxseth', 'kmdbtc', 'polybtc', 'gasbtc',
           'engbtc', 'zileth', 'xlmeth', 'eosbnb', 'xrppax', 'lskbtc', 'npxsbtc', 'xmrusdt', 'ltcpax', 'xmrusdt',
           'ethtusd', 'batusdt', 'mcobtc', 'neoeth', 'bntbtc', 'eostusd', 'lrcbtc', 'funbtc', 'zecusdt',
           'bnbpax', 'linkusdt', 'hceth', 'zrxeth', 'icxeth', 'xmreth', 'neobnb', 'etceth', 'zeceth', 'xmrbnb',
           'wanbnb', 'zrxbnb', 'agibnb', 'funeth', 'arketh', 'engeth'}

binance_websocket_api_manager.create_stream(["aggTrade"], markets)
binance_websocket_api_manager.create_stream(["trade"], markets)
binance_websocket_api_manager.create_stream(["kline_1m"], markets)
binance_websocket_api_manager.create_stream(["kline_5m"], markets)
binance_websocket_api_manager.create_stream(["kline_15m"], markets)
binance_websocket_api_manager.create_stream(["kline_1h"], markets)
binance_websocket_api_manager.create_stream(["kline_12h"], markets)
binance_websocket_api_manager.create_stream(["kline_1w"], markets)

while True:
    monitoring_status_nagios_icinga = binance_websocket_api_manager.get_monitoring_status()
    print(monitoring_status_nagios_icinga)
    time.sleep(10)