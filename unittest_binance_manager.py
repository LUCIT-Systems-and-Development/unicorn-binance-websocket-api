#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unittest_binance_manager.py
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
import unittest


class TestBinanceManager(unittest.TestCase):

    def setUp(self):
        self.binance_com_api_key = "aaaa"
        self.binance_com_api_secret = "bbbb"

        self.binance_websocket_api_manager_com = BinanceWebSocketApiManager(exchange="binance.com")
        self.binance_websocket_api_manager_je = BinanceWebSocketApiManager(exchange="binance.je")
        self.binance_websocket_api_manager_org = BinanceWebSocketApiManager(exchange="binance.org")
        self.binance_websocket_api_manager_org_testnet = BinanceWebSocketApiManager(exchange="binance.org-testnet")

    def test_create_uri_miniticker_regular_com(self):
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_com(self):
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://stream.binance.com:9443/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_com(self):
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr/')

    def test_create_uri_ticker_reverse_com(self):
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr/')

    def test_create_uri_userdata_regular_com_false(self):
        self.assertFalse(self.binance_websocket_api_manager_com.create_websocket_uri(["!userData"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!userData@arr/')

    def test_create_uri_userdata_reverse_com_false(self):
        self.assertFalse(self.binance_websocket_api_manager_com.create_websocket_uri(["arr"], ["!userData"]),
                         'wss://stream.binance.com:9443/ws/!userData@arr/')

    def test_create_uri_userdata_regular_com(self):
        self.binance_websocket_api_manager_com.set_private_api_config(self.binance_com_api_key,
                                                                      self.binance_com_api_secret)

        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["!userData"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!userData@arr/')

    def test_create_uri_userdata_reverse_com(self):
        self.binance_websocket_api_manager_com.set_private_api_config(self.binance_com_api_key,
                                                                      self.binance_com_api_secret)
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["arr"], ["!userData"]),
                         'wss://stream.binance.com:9443/ws/!userData@arr/')

    def test_create_uri_single_regular_com(self):
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(["trade"], ["bnbbtc"]),
                         'wss://stream.binance.com:9443/ws/bnbbtc@trade/')

    def test_create_uri_multi_regular_com(self):
        self.assertEqual(self.binance_websocket_api_manager_com.create_websocket_uri(['trade', 'kline_1'],
                                                                                     ['bnbbtc', 'ethbtc']),
                         'wss://stream.binance.com:9443/stream?streams=bnbbtc@trade/ethbtc@trade/'
                         'bnbbtc@kline_1/ethbtc@kline_1/')

    def tearDown(self):
        self.binance_websocket_api_manager_com.stop_manager_with_all_streams()
        self.binance_websocket_api_manager_je.stop_manager_with_all_streams()
        self.binance_websocket_api_manager_org.stop_manager_with_all_streams()
        self.binance_websocket_api_manager_org_testnet.stop_manager_with_all_streams()




if __name__ == '__main__':
    unittest.main()
