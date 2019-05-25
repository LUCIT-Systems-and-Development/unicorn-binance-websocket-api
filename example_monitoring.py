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
import json
import logging
import os
import time
import threading


# https://docs.python.org/3/library/logging.html
logging.basicConfig(filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
logging.getLogger('unicorn-log').setLevel(logging.INFO)
logging.getLogger('unicorn-log').addHandler(logging.StreamHandler())


def report_websocket_status(binance_manager):
    # get the status from the binance_websocket_api_manager and write it to a json file every 60 seconds
    while True:
        status = binance_manager.get_monitoring_status_icinga()
        with open('./binance_websocket_status.json', 'w') as fp:
            json.dump(status, fp)
        time.sleep(20)


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    print("waiting 30 seconds, then we start flushing the stream_buffer")
    time.sleep(30)
    while True:
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)
        else:
            try:
                # remove # to activate the print function:
                #print(oldest_stream_data_from_stream_buffer)
                pass
            except Exception:
                # not able to process the data? write it back to the stream_buffer
                binance_websocket_api_manager.add_to_stream_buffer(oldest_stream_data_from_stream_buffer)


# create instance of BinanceWebSocketApiManager and provide the function for stream processing
binance_websocket_api_manager = BinanceWebSocketApiManager()

# create streams
ticker_all_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!ticker"])
miniticker_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!miniTicker"])

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
binance_websocket_api_manager.create_stream(["ticker"], markets)
binance_websocket_api_manager.create_stream(["miniTicker"], markets)
binance_websocket_api_manager.create_stream(["depth"], markets)
binance_websocket_api_manager.create_stream(["depth5"], markets)
binance_websocket_api_manager.create_stream(["depth10"], markets)
binance_websocket_api_manager.create_stream(["depth20"], markets)
binance_websocket_api_manager.create_stream(["aggTrade"], markets)

markets = {'bnbbtc', 'ethbtc', 'btcusdt', 'bchabcusdt', 'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt',
           'neobtc', 'adaeth', 'icxusdt', 'btctusd', 'icxbtc', 'btcusdc', 'wanbtc', 'zecbtc', 'wtcbtc',
           'batbtc', 'adabnb', 'etcusdt', 'qtumusdt', 'xmrbtc', 'trxeth', 'adatusd', 'trxxrp', 'trxbnb',
           'ltctusd', 'polybnb', 'scbtc', 'steembtc', 'trxtusd', 'npxseth', 'kmdbtc', 'polybtc', 'gasbtc',
           'bnbpax', 'linkusdt', 'hceth', 'zrxeth', 'icxeth', 'xmreth', 'neobnb', 'etceth', 'zeceth', 'xmrbnb'}
channels = {'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'kline_1w',
            'miniTicker', 'depth20'}
binance_websocket_api_manager.create_stream(channels, markets)

# start a worker process to process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

# start monitoring status report
thread = threading.Thread(target=report_websocket_status, args=(binance_websocket_api_manager,))
thread.start()

print("./binance_websocket_status.json will get refreshed every 20 seconds! so the tools/check_binance_websocket_api_"
      "manager check_command is able to pick it up and deliver it to the icinga daemon! the check_command returns "
      "UNKOWN if the file is older than 60 seconds...")

# show an overview
while True:
    binance_websocket_api_manager.print_summary()
    time.sleep(1)
