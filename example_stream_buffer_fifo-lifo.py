#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_stream_buffer_fifo-lifo.py
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
import time
import os


logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com", stream_buffer_maxlen=3)


binance_websocket_api_manager.create_stream('kline_1m', 'bnbbtc',
                                            stream_buffer_name="buffer1",
                                            stream_buffer_maxlen=4,
                                            output="UnicornFy")

binance_websocket_api_manager.create_stream('kline_1m', 'bnbbtc',
                                            stream_buffer_name="buffer2",
                                            stream_buffer_maxlen=4,
                                            output="UnicornFy")

time.sleep(4)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"clearing...")
binance_websocket_api_manager.clear_stream_buffer(stream_buffer_name="buffer1")
binance_websocket_api_manager.clear_stream_buffer(stream_buffer_name="buffer2")
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")
time.sleep(1)
print(f"sb-len: {binance_websocket_api_manager.get_stream_buffer_length()}")

print(f"FIFO START ##################################################")
i = 0
while i < 5:
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer(stream_buffer_name="buffer1")
    if oldest_stream_data_from_stream_buffer is False:
        time.sleep(0.01)
    else:
        if oldest_stream_data_from_stream_buffer is not None:
            print(f"FIFO: {oldest_stream_data_from_stream_buffer}")
    i += 1

print(f"LIFO START ##################################################")
i = 0
while i < 5:
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer(stream_buffer_name="buffer2",
                                                                                                             mode="LIFO")
    if oldest_stream_data_from_stream_buffer is False:
        time.sleep(0.01)
    else:
        if oldest_stream_data_from_stream_buffer is not None:
            print(f"LIFO: {oldest_stream_data_from_stream_buffer}")
    i += 1

binance_websocket_api_manager.stop_manager_with_all_streams()
