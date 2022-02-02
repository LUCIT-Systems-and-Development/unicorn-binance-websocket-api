#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_userdata_stream.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
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
            print(oldest_stream_data_from_stream_buffer)


# configure api key and secret for binance.com
binance_com_api_key = ""
binance_com_api_secret = ""

# configure api key and secret for binance.je
binance_je_api_key = ""
binance_je_api_secret = ""

# configure api key and secret for binance.us
binance_us_api_key = ""
binance_us_api_secret = ""

# configure api key and secret for binance.us
binance_com_iso_api_key = ""
binance_com_iso_api_secret = ""

# create instances of BinanceWebSocketApiManager
binance_com_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com",
                                                               throw_exception_if_unrepairable=True)
binance_je_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.je")
binance_us_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.us")
binance_com_isolated_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin")

# create the userData streams
binance_com_user_data_stream_id = binance_com_websocket_api_manager.create_stream('arr', '!userData',
                                                                                  api_key=binance_com_api_key,
                                                                                  api_secret=binance_com_api_secret)
binance_je_user_data_stream_id = binance_je_websocket_api_manager.create_stream('arr', '!userData',
                                                                                api_key=binance_je_api_key,
                                                                                api_secret=binance_je_api_secret)
binance_us_user_data_stream_id = binance_us_websocket_api_manager.create_stream('arr', '!userData',
                                                                                api_key=binance_us_api_key,
                                                                                api_secret=binance_us_api_secret)
binance_com_iso_user_data_stream_id = binance_com_isolated_websocket_api_manager.create_stream('arr', '!userData',
                                                                                               symbols="trxbtc",
                                                                                               api_key=binance_com_iso_api_key,
                                                                                               api_secret=binance_com_iso_api_secret)

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_com_websocket_api_manager,))
worker_thread.start()
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_je_websocket_api_manager,))
worker_thread.start()
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_us_websocket_api_manager,))
worker_thread.start()
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer,
                                 args=(binance_com_isolated_websocket_api_manager,))
worker_thread.start()

# monitor the streams
while True:
    binance_com_isolated_websocket_api_manager.print_stream_info(binance_com_iso_user_data_stream_id)
    binance_com_websocket_api_manager.print_summary()
    binance_je_websocket_api_manager.print_summary()
    binance_us_websocket_api_manager.print_summary()
    binance_com_isolated_websocket_api_manager.print_summary()
    time.sleep(5)
