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
import uuid

BINANCE_COM_API_KEY = ""
BINANCE_COM_API_SECRET = ""
BINANCE_JE_API_KEY = ""
BINANCE_JE_API_SECRET = ""


class TestBinanceComManager(unittest.TestCase):
    # Test binance.com (Binance)

    def setUp(self):
        self.binance_com_api_key = BINANCE_COM_API_KEY
        self.binance_com_api_secret = BINANCE_COM_API_SECRET
        self.binance_com_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")

    def test_create_uri_miniticker_regular_com(self):
        self.assertEqual(self.binance_com_websocket_api_manager.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_com(self):
        self.assertEqual(self.binance_com_websocket_api_manager.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://stream.binance.com:9443/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_com(self):
        self.assertEqual(self.binance_com_websocket_api_manager.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr')

    def test_create_uri_ticker_reverse_com(self):
        self.assertEqual(self.binance_com_websocket_api_manager.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr')

    def test_create_uri_userdata_regular_false_com(self):
        self.assertFalse(self.binance_com_websocket_api_manager.create_websocket_uri(["!userData"], ["arr"]))

    def test_create_uri_userdata_reverse_false_com(self):
        self.assertFalse(self.binance_com_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"]))

    def test_create_uri_userdata_regular_com(self):
        if len(self.binance_com_api_key) == 0 or len(self.binance_com_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_regular_com() "
                  "for binance.com")
        stream_id = uuid.uuid4()
        self.binance_com_websocket_api_manager._add_socket_to_socket_list(stream_id, ["!userData"], ["arr"])
        self.assertRegex(self.binance_com_websocket_api_manager.create_websocket_uri(["!userData"], ["arr"],
                                                                                     stream_id,
                                                                                     self.binance_com_api_key,
                                                                                     self.binance_com_api_secret),
                         r'wss://stream.binance.com:9443/ws/.')

    def test_create_uri_userdata_reverse_com(self):
        if len(self.binance_com_api_key) == 0 or len(self.binance_com_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_reverse_com() "
                  "for binance.com")
        stream_id = uuid.uuid4()
        self.binance_com_websocket_api_manager._add_socket_to_socket_list(stream_id, ["arr"], ["!userData"])
        self.assertRegex(self.binance_com_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"],
                                                                                     stream_id,
                                                                                     self.binance_com_api_key,
                                                                                     self.binance_com_api_secret),
                         r'wss://stream.binance.com:9443/ws/.')

    def test_create_uri_single_com(self):
        self.assertEqual(self.binance_com_websocket_api_manager.create_websocket_uri(["trade"], ["bnbbtc"]),
                         'wss://stream.binance.com:9443/stream?streams=bnbbtc@trade/')

    def test_create_uri_multi_com(self):
        self.assertEqual(self.binance_com_websocket_api_manager.create_websocket_uri(['trade', 'kline_1'],
                                                                                     ['bnbbtc', 'ethbtc']),
                         'wss://stream.binance.com:9443/stream?streams=bnbbtc@trade/ethbtc@trade/'
                         'bnbbtc@kline_1/ethbtc@kline_1/')

    def tearDown(self):
        self.binance_com_websocket_api_manager.stop_manager_with_all_streams()


class TestBinanceJeManager(unittest.TestCase):
    # Test binance.je (Binance Jersey)

    def setUp(self):
        self.binance_je_api_key = BINANCE_JE_API_KEY
        self.binance_je_api_secret = BINANCE_JE_API_SECRET

        self.binance_je_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.je")

    def test_create_uri_miniticker_regular_je(self):
        self.assertEqual(self.binance_je_websocket_api_manager.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://stream.binance.je:9443/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_je(self):
        self.assertEqual(self.binance_je_websocket_api_manager.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://stream.binance.je:9443/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_je(self):
        self.assertEqual(self.binance_je_websocket_api_manager.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://stream.binance.je:9443/ws/!ticker@arr')

    def test_create_uri_ticker_reverse_je(self):
        self.assertEqual(self.binance_je_websocket_api_manager.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://stream.binance.je:9443/ws/!ticker@arr')

    def test_create_uri_userdata_regular_false_je(self):
        self.assertFalse(self.binance_je_websocket_api_manager.create_websocket_uri(["!userData"], ["arr"]))

    def test_create_uri_userdata_reverse_false_je(self):
        self.assertFalse(self.binance_je_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"]))

    def test_create_uri_userdata_regular_je(self):
        if len(self.binance_je_api_key) == 0 or len(self.binance_je_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_regular_je() "
                  "for binance.com")
        stream_id = uuid.uuid4()
        self.binance_je_websocket_api_manager._add_socket_to_socket_list(stream_id, ["!userData"], ["arr"])
        self.assertRegex(self.binance_je_websocket_api_manager.create_websocket_uri(["!userData"], ["arr"],
                                                                                     stream_id,
                                                                                     self.binance_je_api_key,
                                                                                     self.binance_je_api_secret),
                         r'wss://stream.binance.je:9443/ws/.')

    def test_create_uri_userdata_reverse_je(self):
        if len(self.binance_je_api_key) == 0 or len(self.binance_je_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_reverse_je() "
                  "for binance.com")
        stream_id = uuid.uuid4()
        self.binance_je_websocket_api_manager._add_socket_to_socket_list(stream_id, ["arr"], ["!userData"])
        self.assertRegex(self.binance_je_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"],
                                                                                     stream_id,
                                                                                     self.binance_je_api_key,
                                                                                     self.binance_je_api_secret),
                         r'wss://stream.binance.je:9443/ws/.')

    def test_create_uri_single_je(self):
        self.assertEqual(self.binance_je_websocket_api_manager.create_websocket_uri(["trade"], ["bnbbtc"]),
                         'wss://stream.binance.je:9443/stream?streams=bnbbtc@trade/')

    def test_create_uri_multi_je(self):
        self.assertEqual(self.binance_je_websocket_api_manager.create_websocket_uri(['trade', 'kline_1'],
                                                                                     ['bnbbtc', 'ethbtc']),
                         'wss://stream.binance.je:9443/stream?streams=bnbbtc@trade/ethbtc@trade/'
                         'bnbbtc@kline_1/ethbtc@kline_1/')

    def tearDown(self):
        self.binance_je_websocket_api_manager.stop_manager_with_all_streams()


class TestBinanceOrgManager(unittest.TestCase):
    # Test binance.org (Binance Chain Dex)

    def setUp(self):
        self.binance_org_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.org")

    def test_create_uri_alltickers_regular_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["$all"], ["allTickers"]),
                         'wss://dex.binance.org/api/ws/$all@allTickers')

    def test_create_uri_alltickers_reverse_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["allTickers"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@allTickers')

    def test_create_uri_allminitickers_regular_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["$all"], ["allMiniTickers"]),
                         'wss://dex.binance.org/api/ws/$all@allMiniTickers')

    def test_create_uri_allminitickers_reverse_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["allMiniTickers"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@allMiniTickers')

    def test_create_uri_blockheight_regular_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["$all"], ["blockheight"]),
                         'wss://dex.binance.org/api/ws/$all@blockheight')

    def test_create_uri_blockheight_reverse_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["blockheight"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@blockheight')

    def test_create_uri_single_trades_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["trades"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@trades')

    def test_create_uri_single_marketdepth_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["marketDepth"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@marketDepth')

    def test_create_uri_single_kline_1h_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["kline_1h"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@kline_1h')

    def test_create_uri_single_ticker_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["ticker"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@ticker')

    def test_create_uri_single_miniTicker_org(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["miniTicker"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@miniTicker')


    def tearDown(self):
        self.binance_org_websocket_api_manager.stop_manager_with_all_streams()


if __name__ == '__main__':
    unittest.main()
