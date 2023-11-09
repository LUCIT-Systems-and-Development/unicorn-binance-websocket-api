#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_stream_signals.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api
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

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import os
import time
import threading

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# To use this library you need a valid UNICORN Binance Suite License:
# https://medium.lucit.tech/87b0088124a8
binance_websocket_api_manager = BinanceWebSocketApiManager(enable_stream_signal_buffer=True)


def print_stream_signals(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        stream_signal = binance_websocket_api_manager.pop_stream_signal_from_stream_signal_buffer()
        if stream_signal is False:
            time.sleep(0.01)
        else:
            print(stream_signal)

# start a worker process to process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_signals, args=(binance_websocket_api_manager,))
worker_thread.start()

print("\r\n========================================== Starting aggTrade ==========================================\r\n")
# start

markets = ['xrpbearbusd', 'zeceth', 'cndbtc', 'dashbtc', 'atompax', 'perlbtc', 'ardreth', 'zecbnb', 'bchabctusd',
           'usdsbusdt', 'winbnb', 'xzcxrp', 'bchusdc', 'wavesbnb', 'kavausdt', 'btsusdt', 'chzbnb', 'tusdbnb',
           'xtzbusd', 'bcptusdc', 'dogebnb', 'eosbearusdt', 'ambbnb', 'wrxbnb', 'poabtc', 'wanbtc', 'ardrbtc', 'icnbtc',
           'bchabcbusd', 'ltcbnb', 'pivxeth', 'skybtc', 'tntbtc', 'poebtc', 'steembtc', 'icxusdt', 'tfuelbtc', 'chzbtc',
           'vibeth', 'winusdc', 'gtobtc', 'linkusdc', 'batbusd', 'rdnbtc', 'dataeth', 'bttpax', 'zrxbnb', 'vibbtc',
           'neobnb', 'cosbtc', 'powreth', 'rlcusdt', 'hbarbnb', 'wabieth', 'bqxeth', 'aionbtc', 'aeeth', 'mthbtc',
           'wrxbtc', 'pptbtc', 'nknbtc', 'zecusdt', 'stormeth', 'qtumusdt']

aggtrade_stream_id = binance_websocket_api_manager.create_stream(["aggTrade"], markets)
time.sleep(7)
# stop
binance_websocket_api_manager.stop_stream(aggtrade_stream_id)
time.sleep(2)
print("\r\n=========================================== Stopped aggTrade ==========================================\r\n")

print("\r\n====================================== Starting trade and kline_1m ====================================\r\n")
trade_stream_id = binance_websocket_api_manager.create_stream(["trade"], markets)
kline_1m_stream_id = binance_websocket_api_manager.create_stream("kline_1m", markets)
time.sleep(7)
binance_websocket_api_manager.stop_stream(trade_stream_id)
binance_websocket_api_manager.stop_stream(kline_1m_stream_id)
time.sleep(2)
print("\r\n====================================== Stopped trade and kline_1m =====================================\r\n")

print("\r\n======================================== Starting ticker ==============================================\r\n")
ticker_bnbbtc_stream_id = binance_websocket_api_manager.create_stream(["ticker"], markets)
time.sleep(7)
binance_websocket_api_manager.stop_stream(ticker_bnbbtc_stream_id)
time.sleep(2)
print("\r\n======================================== Stopped ticker ===============================================\r\n")

print("\r\n========================================== Starting miniticker ========================================\r\n")
miniticker_stream_id = binance_websocket_api_manager.create_stream(["miniTicker"], markets)
time.sleep(7)
binance_websocket_api_manager.stop_stream(miniticker_stream_id)
time.sleep(2)
print("\r\n========================================= Stopped miniticker  =========================================\r\n")

print("\r\n========================================== Starting kline_5m ==========================================\r\n")
kline_5m_stream_id = binance_websocket_api_manager.create_stream(["kline_5m"], markets)
time.sleep(7)
binance_websocket_api_manager.stop_stream(kline_5m_stream_id)
time.sleep(2)
print("\r\n========================================= Stopped kline_5m  ===========================================\r\n")

print("\r\n=========================================== Starting depth5 ===========================================\r\n")
depth5_stream_id = binance_websocket_api_manager.create_stream(["depth5"], markets)
time.sleep(7)
binance_websocket_api_manager.stop_stream(depth5_stream_id)
time.sleep(2)
print("\r\n========================================== Stopped depth5  ============================================\r\n")

print("\r\n========================================== Starting depth =============================================\r\n")
depth_stream_id = binance_websocket_api_manager.create_stream(["depth"], markets)
time.sleep(7)
binance_websocket_api_manager.stop_stream(depth_stream_id)
time.sleep(2)
print("\r\n============================================ Stopped depth  ===========================================\r\n")

print("\r\n========================================== Starting !miniticker ========================================\r\n")
miniticker_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!miniTicker"])
time.sleep(7)
binance_websocket_api_manager.stop_stream(miniticker_stream_id)
time.sleep(2)
print("\r\n========================================= Stopped !miniticker  =========================================\r\n")

print("\r\n========================================== Starting ticker all ========================================\r\n")
ticker_all_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!ticker"])
time.sleep(7)
binance_websocket_api_manager.stop_stream(ticker_all_stream_id)
time.sleep(2)
print("\r\n=========================================== Stopped ticker all ========================================\r\n")

print("\r\n=================================== Starting multi multi socket =======================================\r\n")
channels = {'trade', 'kline_1', 'kline_5', 'kline_15', 'kline_30', 'kline_1h', 'kline_12h', 'kline_1w',
            'miniTicker', 'depth20'}
print(channels)
print(markets, "\r\n")
time.sleep(3)
multi_multi_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(multi_multi_stream_id)
time.sleep(2)
print("\r\n================================== Stopped multi multi socket  ========================================\r\n")

print("\r\n============================= Starting multi multi socket subscribe ===================================\r\n")
channels = {'trade', 'kline_1', 'kline_5', 'kline_15', 'kline_30', 'kline_1h', 'kline_12h', 'kline_1w',
            'miniTicker', 'depth20', '!miniTicker', '!ticker'}
multi_multi_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(5)
binance_websocket_api_manager.stop_stream(multi_multi_stream_id)
time.sleep(2)
print("\r\n============================== Stopped multi multi socket subscribe ===================================\r\n")

print("\r\n=============================== Stopping BinanceWebSocketManager ======================================\r\n")
binance_websocket_api_manager.stop_manager_with_all_streams()
print("finished!")
