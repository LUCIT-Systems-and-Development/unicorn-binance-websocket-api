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
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.


from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import unittest
import os
import time
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
