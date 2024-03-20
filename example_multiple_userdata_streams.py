#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_multiple_userdata_streams.py
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

from unicorn_binance_websocket_api.manager_old import BinanceWebSocketApiManager
import logging
import time
import threading
import os


logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


def print_stream_buffer_data(binance_websocket_api_manager, stream_id):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer(stream_id)
        if oldest_stream_data_from_stream_buffer is None:
            time.sleep(0.01)
        else:
            print(oldest_stream_data_from_stream_buffer)


# To use this library you need a valid UNICORN Binance Suite License:
# https://medium.lucit.tech/87b0088124a8
# create instances of BinanceWebSocketApiManager
binance_com_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")

# configure api key and secret for binance.com for Alice
alice_api_key = "aaaa"
alice_api_secret = "bbbb"
# create the userData streams
alice_stream_id = binance_com_websocket_api_manager.create_stream('arr', '!userData', stream_label="Alice",
                                                                  stream_buffer_name=True,
                                                                  api_key=alice_api_key, api_secret=alice_api_secret)
# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_buffer_data, args=(binance_com_websocket_api_manager,
                                                                        alice_stream_id))
worker_thread.start()

# configure api key and secret for binance.com for Bob
bob_api_key = "cccc"
bob_api_secret = "dddd"
# create the userData streams
bob_stream_id = binance_com_websocket_api_manager.create_stream('arr', '!userData', stream_label="Bob",
                                                                stream_buffer_name=True,
                                                                api_key=bob_api_key, api_secret=bob_api_secret)
# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_buffer_data, args=(binance_com_websocket_api_manager,
                                                                        bob_stream_id))
worker_thread.start()

# monitor the streams
while True:
    binance_com_websocket_api_manager.print_summary()
    time.sleep(1)
