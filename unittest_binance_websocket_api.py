#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: test_binance_websocket_api.py
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
from unicorn_binance_websocket_api.restclient import BinanceWebSocketApiRestclient
from unicorn_binance_websocket_api.restserver import BinanceWebSocketApiRestServer
import logging
import unittest
import os
import time
import threading

import tracemalloc
tracemalloc.start(25)

BINANCE_COM_API_KEY = ""
BINANCE_COM_API_SECRET = ""

LUCIT_API_SECRET = os.environ['LUCIT_API_SECRET']
LUCIT_LICENSE_TOKEN = os.environ['LUCIT_LICENSE_TOKEN']

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

print(f"Starting unittests:")


class TestBinanceComManager(unittest.TestCase):
    # Test binance.com (Binance)
    @classmethod
    def setUpClass(cls):
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.us", disable_colorama=True,
                                              lucit_api_secret=LUCIT_API_SECRET,
                                              lucit_license_token=LUCIT_LICENSE_TOKEN)
        cls.binance_com_api_key = BINANCE_COM_API_KEY
        cls.binance_com_api_secret = BINANCE_COM_API_SECRET

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_manager_with_all_streams()

    def test_create_uri_miniticker_regular_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["!miniTicker"], ["arr"]), 'wss://stream.binance.us:9443/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["arr"], ["!miniTicker"]), 'wss://stream.binance.us:9443/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["!ticker"], ["arr"]), 'wss://stream.binance.us:9443/ws/!ticker@arr')

    def test_create_uri_ticker_reverse_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["arr"], ["!ticker"]), 'wss://stream.binance.us:9443/ws/!ticker@arr')

    def test_create_uri_userdata_regular_false_com(self):
        self.assertFalse(self.__class__.ubwa.create_websocket_uri(["!userData"], ["arr"]))

    def test_create_uri_userdata_reverse_false_com(self):
        self.assertFalse(self.__class__.ubwa.create_websocket_uri(["arr"], ["!userData"]))

    def test_create_uri_userdata_regular_com(self):
        if len(self.binance_com_api_key) == 0 or len(self.binance_com_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_regular_com() "
                  "for binance.com")
        else:
            stream_id = self.ubwa.get_new_uuid_id()
            self.__class__.ubwa._add_socket_to_socket_list(stream_id, ["!userData"], ["arr"])
            self.assertRegex(self.__class__.ubwa.create_websocket_uri(["!userData"], ["arr"],
                                                                      stream_id,
                                                                      self.binance_com_api_key,
                                                                      self.binance_com_api_secret),
                             r'wss://stream.binance.com:9443/ws/.')

    def test_create_uri_userdata_reverse_com(self):
        if len(self.binance_com_api_key) == 0 or len(self.binance_com_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_reverse_com() "
                  "for binance.com")
        else:
            self.stream_id = self.__class__.ubwa.get_new_uuid_id()
            self.__class__.ubwa._add_socket_to_socket_list(self.stream_id, ["arr"], ["!userData"])
            self.assertRegex(self.__class__.ubwa.create_websocket_uri(["arr"], ["!userData"],
                                                                      self.stream_id,
                                                                      self.binance_com_api_key,
                                                                      self.binance_com_api_secret),
                             'wss://stream.binance.com:9443/ws/.')

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.__class__.ubwa.is_exchange_type("cex"), True)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.__class__.ubwa.is_exchange_type("dex"), False)

    def test_is_update_available(self):
        self.assertEqual(self.__class__.ubwa.is_update_available(), False)

    def test_is_manager_stopping(self):
        self.assertEqual(self.__class__.ubwa.is_manager_stopping(), False)

    def test_get_human_uptime(self):
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60 * 60 * 60 * 61), "152d:12h:0m:0s")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60 * 60 * 24), "24h:0m:0s")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60 * 60), "60m:0s")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60), "60 seconds")

    def test_get_human_bytesize(self):
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024 * 1024 * 1024 * 1024), "1024.0 tB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024 * 1024 * 1024), "1024.0 gB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024 * 1024), "1024.0 mB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024), "1024.0 kB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024), "1024 B")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1), "1 B")

    def test_get_exchange(self):
        self.assertEqual(self.__class__.ubwa.get_exchange(), "binance.us")

    def test_get_listenkey_from_restclient(self):
        self.assertEqual(self.__class__.ubwa.get_listen_key_from_restclient("ID"), False)

    def test_delete_listen_key_by_stream_id(self):
        stream_id = self.__class__.ubwa.get_new_uuid_id()
        self.assertEqual(self.__class__.ubwa.delete_listen_key_by_stream_id(stream_id), False)

    def test_create_payload_subscribe(self):
        result = "[{'method': 'SUBSCRIBE', 'params': ['bnbbtc@kline_1m'], 'id': 1}]"
        stream_id = self.__class__.ubwa.get_new_uuid_id()
        self.assertEqual(str(self.__class__.ubwa.create_payload(stream_id, "subscribe", ['kline_1m'], ['bnbbtc'])), result)

    def test_fill_up_space_centered(self):
        result = "==========test text=========="
        self.assertEqual(str(self.__class__.ubwa.fill_up_space_centered(30, "test text", "=")),
                         result)

    def test_fill_up_space_right(self):
        result = "|test text||||||||||||||||||||"
        self.assertEqual(str(self.__class__.ubwa.fill_up_space_right(30, "test text", "|")),
                         result)

    def test_fill_up_space_left(self):
        result = "||||||||||||||||||||test text|"
        self.assertEqual(str(self.__class__.ubwa.fill_up_space_left(30, "test text", "|")),
                         result)

    def test_create_stream(self):
        #self.assertTrue(bool(self.ubwa.create_stream('arr', '!userData', "userData", "key", "secret")))
        self.assertTrue(bool(self.__class__.ubwa.create_stream(markets=['bnbbtc'], channels="trade", stream_label="test_stream")))
        stream_id = self.__class__.ubwa.get_stream_id_by_label("test_stream")
        #time.sleep(5)
        #self.__class__.ubwa.unsubscribe_from_stream(stream_id, markets=['bnbbtc'])
        #self.__class__.ubwa.unsubscribe_from_stream(stream_id, channels=['trade'])
        time.sleep(5)
        self.assertTrue(self.__class__.ubwa.set_restart_request(stream_id))
        time.sleep(10)
        self.__class__.ubwa.get_monitoring_status_icinga()
        self.__class__.ubwa.print_summary(title="Unittests")
        self.__class__.ubwa.print_stream_info(stream_id, title="Unittests")

    def test_restart_stream(self):
        self.assertFalse(bool(self.__class__.ubwa._restart_stream(self.__class__.ubwa.get_new_uuid_id())))

    def test_start_monitoring_api(self):
        self.assertTrue(self.__class__.ubwa.start_monitoring_api())
        time.sleep(5)
        self.assertTrue(self.__class__.ubwa.stop_monitoring_api())

    def test_stop_manager(self):
        self.__class__.ubwa.stop_manager_with_all_streams()


if __name__ == '__main__':
    unittest.main()
