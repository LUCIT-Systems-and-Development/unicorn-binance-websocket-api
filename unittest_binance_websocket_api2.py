#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unittest_binance_websocket_api.py
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
import time

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import unittest
import os
import threading

import tracemalloc
tracemalloc.start(25)

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

print(f"Starting unittests!")


class TestBinanceComManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\r\nTestBinanceComManager:")
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.us",
                                              disable_colorama=True,
                                              debug=False)

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_manager()
        print(f"\r\nTestBinanceComManager threads:")
        for thread in threading.enumerate():
            print(thread.name)
        print(f"TestBinanceComManager stopping:")

    def test_create_stream_userdata(self):
        with BinanceWebSocketApiManager(exchange="binance.us") as ubwa:
            ubwa.create_stream('arr', '!userData', stream_label="userDataBad")
            time.sleep(10)


if __name__ == '__main__':
    unittest.main()
