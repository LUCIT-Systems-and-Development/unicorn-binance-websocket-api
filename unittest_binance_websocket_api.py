#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unittest_binance_websocket_api.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019-2020, Oliver Zehentleitner
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
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_restclient import BinanceWebSocketApiRestclient
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_restserver import BinanceWebSocketApiRestServer
import logging
import unittest
import uuid
import os
import time

BINANCE_COM_API_KEY = ""
BINANCE_COM_API_SECRET = ""
BINANCE_JE_API_KEY = ""
BINANCE_JE_API_SECRET = ""

# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


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
        else:
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
        else:
            stream_id = uuid.uuid4()
            self.binance_com_websocket_api_manager._add_socket_to_socket_list(stream_id, ["arr"], ["!userData"])
            self.assertRegex(self.binance_com_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"],
                                                                                         stream_id,
                                                                                         self.binance_com_api_key,
                                                                                         self.binance_com_api_secret),
                             r'wss://stream.binance.com:9443/ws/.')

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.binance_com_websocket_api_manager.is_exchange_type("cex"), True)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.binance_com_websocket_api_manager.is_exchange_type("dex"), False)

    def test_is_update_available(self):
        self.assertEqual(self.binance_com_websocket_api_manager.is_update_availabe(), False)

    def test_is_manager_stopping(self):
        self.assertEqual(self.binance_com_websocket_api_manager.is_manager_stopping(), False)

    def test_get_human_uptime(self):
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_uptime(60 * 60 * 60 * 61), "152d:12h:0m:0s")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_uptime(60 * 60 * 24), "24h:0m:0s")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_uptime(60 * 60), "60m:0s")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_uptime(60), "60 seconds")

    def test_get_human_bytesize(self):
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_bytesize(1024 * 1024 * 1024 * 1024 * 1024), "1024.0 tB")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_bytesize(1024 * 1024 * 1024 * 1024), "1024.0 gB")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_bytesize(1024 * 1024 * 1024), "1024.0 mB")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_bytesize(1024 * 1024), "1024.0 kB")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_bytesize(1024), "1024 B")
        self.assertEqual(self.binance_com_websocket_api_manager.get_human_bytesize(1), "1 B")

    def test_get_exchange(self):
        self.assertEqual(self.binance_com_websocket_api_manager.get_exchange(), "binance.com")

    def test_get_listenkey_from_restclient(self):
        self.assertEqual(self.binance_com_websocket_api_manager.get_listen_key_from_restclient(), False)

    def test_get_listenkey_from_restclient(self):
        stream_id = uuid.uuid4()
        self.assertEqual(self.binance_com_websocket_api_manager.delete_listen_key_by_stream_id(stream_id), False)

    def test_keepalive_listen_key(self):
        stream_id = uuid.uuid4()
        binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.binance_com_websocket_api_manager,
                                                                         stream_id)
        self.assertEqual(str(binance_websocket_api_restclient.keepalive_listen_key("invalid_testkey")),
                         "{'code': -2014, 'msg': 'API-key format invalid.'}")

    def test_delete_listen_key(self):
        stream_id = uuid.uuid4()
        binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.binance_com_websocket_api_manager,
                                                                         stream_id)
        self.assertEqual(str(binance_websocket_api_restclient.delete_listen_key("invalid_testkey")),
                         "{'code': -2014, 'msg': 'API-key format invalid.'}")

    def test_create_payload_subscribe(self):
        result = "[{'method': 'SUBSCRIBE', 'params': ['bnbbtc@kline_1m'], 'id': 1}]"
        stream_id = uuid.uuid4()
        self.assertEqual(str(self.binance_com_websocket_api_manager.create_payload(stream_id,
                                                                                   "subscribe",
                                                                                   ['kline_1m'],
                                                                                   ['bnbbtc'])),
                         result)

    def test_fill_up_space_centered(self):
        result = "==========test text=========="
        self.assertEqual(str(self.binance_com_websocket_api_manager.fill_up_space_centered(30, "test text", "=")),
                         result)

    def test_fill_up_space_right(self):
        result = "|test text||||||||||||||||||||"
        self.assertEqual(str(self.binance_com_websocket_api_manager.fill_up_space_right(30, "test text", "|")),
                         result)

    def test_fill_up_space_left(self):
        result = "||||||||||||||||||||test text|"
        self.assertEqual(str(self.binance_com_websocket_api_manager.fill_up_space_left(30, "test text", "|")),
                         result)

    def test_create_stream(self):
        self.assertTrue(bool(self.binance_com_websocket_api_manager.create_stream('arr', '!userData', "userData", "key", "secret")))
        self.assertTrue(bool(self.binance_com_websocket_api_manager.create_stream(markets=['bnbbtc'],
                                                                                  channels="trade",
                                                                                  stream_label="test_stream")))
        stream_id = self.binance_com_websocket_api_manager.get_stream_id_by_label("test_stream")
        #time.sleep(5)
        #self.binance_com_websocket_api_manager.unsubscribe_from_stream(stream_id, markets=['bnbbtc'])
        #self.binance_com_websocket_api_manager.unsubscribe_from_stream(stream_id, channels=['trade'])
        time.sleep(5)
        self.assertTrue(self.binance_com_websocket_api_manager.set_restart_request(stream_id))
        time.sleep(10)
        self.binance_com_websocket_api_manager.get_monitoring_status_icinga()
        self.binance_com_websocket_api_manager.print_summary()
        self.binance_com_websocket_api_manager.print_stream_info(stream_id)

    def test_restart_stream(self):
        self.assertFalse(bool(self.binance_com_websocket_api_manager._restart_stream(uuid.uuid4())))

    def test_start_monitoring_api(self):
        self.assertTrue(self.binance_com_websocket_api_manager.start_monitoring_api())
        time.sleep(5)
        self.assertTrue(self.binance_com_websocket_api_manager.stop_monitoring_api())

    def tearDown(self):
        self.binance_com_websocket_api_manager.stop_manager_with_all_streams()


class TestBinanceComManagerTest(unittest.TestCase):
    # Test testnet.binance.vision (Binance Testnet)

    def setUp(self):
        self.binance_com_testnet_api_key = BINANCE_COM_API_KEY
        self.binance_com_testnet_api_secret = BINANCE_COM_API_SECRET
        self.binance_com_testnet_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-testnet")

    def test_create_uri_miniticker_regular_com(self):
        self.assertEqual(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://testnet.binance.vision/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_com(self):
        self.assertEqual(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://testnet.binance.vision/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_com(self):
        self.assertEqual(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://testnet.binance.vision/ws/!ticker@arr')

    def test_create_uri_ticker_reverse_com(self):
        self.assertEqual(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://testnet.binance.vision/ws/!ticker@arr')

    def test_create_uri_userdata_regular_false_com(self):
        self.assertFalse(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["!userData"], ["arr"]))

    def test_create_uri_userdata_reverse_false_com(self):
        self.assertFalse(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"]))

    def test_create_uri_userdata_regular_com(self):
        if len(self.binance_com_testnet_api_key) == 0 or len(self.binance_com_testnet_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_regular_com() "
                  "for binance.com-testnet")
        else:
            stream_id = uuid.uuid4()
            self.binance_com_testnet_websocket_api_manager._add_socket_to_socket_list(stream_id, ["!userData"], ["arr"])
            self.assertRegex(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["!userData"], ["arr"],
                                                                                         stream_id,
                                                                                         self.binance_com_testnet_api_key,
                                                                                         self.binance_com_testnet_api_secret),
                             r'wss://testnet.binance.vision/ws/.')

    def test_create_uri_userdata_reverse_com(self):
        if len(self.binance_com_testnet_api_key) == 0 or len(self.binance_com_testnet_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_reverse_com() "
                  "for binance.com-testnet")
        else:
            stream_id = uuid.uuid4()
            self.binance_com_testnet_websocket_api_manager._add_socket_to_socket_list(stream_id, ["arr"], ["!userData"])
            self.assertRegex(self.binance_com_testnet_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"],
                                                                                         stream_id,
                                                                                         self.binance_com_testnet_api_key,
                                                                                         self.binance_com_testnet_api_secret),
                             r'wss://stream.binance.com:9443/ws/.')

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.binance_com_testnet_websocket_api_manager.is_exchange_type("cex"), True)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.binance_com_testnet_websocket_api_manager.is_exchange_type("dex"), False)

    def tearDown(self):
        self.binance_com_testnet_websocket_api_manager.stop_manager_with_all_streams()


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
                  "for binance.je")
        else:
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
                  "for binance.je")
        else:
            stream_id = uuid.uuid4()
            self.binance_je_websocket_api_manager._add_socket_to_socket_list(stream_id, ["arr"], ["!userData"])
            self.assertRegex(self.binance_je_websocket_api_manager.create_websocket_uri(["arr"], ["!userData"],
                                                                                        stream_id,
                                                                                        self.binance_je_api_key,
                                                                                        self.binance_je_api_secret),
                             r'wss://stream.binance.je:9443/ws')

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.binance_je_websocket_api_manager.is_exchange_type("cex"), True)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.binance_je_websocket_api_manager.is_exchange_type("dex"), False)

    def tearDown(self):
        self.binance_je_websocket_api_manager.stop_manager_with_all_streams()


class TestBinanceOrgManager(unittest.TestCase):
    # Test binance.org (Binance Chain Dex)

    def setUp(self):
        self.binance_org_testnet = BinanceWebSocketApiManager(exchange="binance.org-testnet")
        self.binance_org_testnet.set_private_dex_config("tbnb1unxhf8fat985ksajatfa5jea58j2kzg7mfy0e7")
        self.binance_org_testnet.unsubscribe_from_stream("tbnb1unxhf8fat985ksajatfa5jea58j2kzg7mfy0e7")

    def tearDown(self):
        self.binance_org_testnet.stop_manager_with_all_streams()


class TestBinanceOrgManager(unittest.TestCase):
    # Test binance.org (Binance Chain Dex)

    def setUp(self):
        self.binance_org_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.org")

    def test_create_uri_alltickers_regular_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["$all"], ["allTickers"]),
                         'wss://dex.binance.org/api/ws/$all@allTickers')

    def test_create_uri_alltickers_reverse_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["allTickers"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@allTickers')

    def test_create_uri_allminitickers_regular_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["$all"], ["allMiniTickers"]),
                         'wss://dex.binance.org/api/ws/$all@allMiniTickers')

    def test_create_uri_allminitickers_reverse_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["allMiniTickers"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@allMiniTickers')

    def test_create_uri_blockheight_regular_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["$all"], ["blockheight"]),
                         'wss://dex.binance.org/api/ws/$all@blockheight')

    def test_create_uri_blockheight_reverse_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["blockheight"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@blockheight')

    def test_create_uri_single_trades_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["trades"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@trades')

    def test_create_uri_single_marketdepth_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["marketDepth"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@marketDepth')

    def test_create_uri_single_kline_1h_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["kline_1h"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@kline_1h')

    def test_create_uri_single_ticker_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["ticker"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@ticker')

    def test_create_uri_single_miniTicker_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(["miniTicker"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@miniTicker')

    def test_create_uri_multi_org_subscribe(self):
        self.assertEqual(self.binance_org_websocket_api_manager.create_websocket_uri(['trades', 'kline_1h'],
                                                                                     ['RAVEN-F66_BNB', 'ANKR-E97_BNB']),
                         'wss://dex.binance.org/api/ws')

        stream_id = self.binance_org_websocket_api_manager.create_stream(['trades', 'kline_1h'],
                                                                  ['RAVEN-F66_BNB', 'ANKR-E97_BNB'])
        payload = self.binance_org_websocket_api_manager.create_payload(stream_id, "subscribe", ['trades', 'kline_1h'],
                                                                        ['RAVEN-F66_BNB', 'ANKR-E97_BNB'])
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'trades', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}, "
                         "{'method': 'subscribe', 'topic': 'kline_1h', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}]")

    def test_create_uri_user_address_orders_single_org_subscribe(self):
        self.assertEqual(
            self.binance_org_websocket_api_manager.create_websocket_uri('orders',
                                                                        'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'),
            'wss://dex.binance.org/api/ws/bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')

    def test_create_uri_user_address_accounts_single_org_subscribe(self):
        self.assertEqual(
            self.binance_org_websocket_api_manager.create_websocket_uri('accounts',
                                                                        'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'),
            'wss://dex.binance.org/api/ws/bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')

    def test_create_uri_user_address_transfers_single_org_subscribe(self):
        self.assertEqual(
            self.binance_org_websocket_api_manager.create_websocket_uri('transfers',
                                                                        'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'),
            'wss://dex.binance.org/api/ws/bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')

    def test_create_uri_user_address_multi_org_subscribe(self):
        stream_id = self.binance_org_websocket_api_manager.create_stream(['orders', 'transfers', 'accounts'],
                                                                         'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')
        payload = self.binance_org_websocket_api_manager.create_payload(stream_id, 'subscribe',
                                                                        ['orders', 'transfers', 'accounts'],
                                                                        'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'orders', 'address': 'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'}, "
                         "{'method': 'subscribe', 'topic': 'transfers', 'address': 'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'}, "
                         "{'method': 'subscribe', 'topic': 'accounts', 'address': 'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'}]")

    def test_create_misc_single_org_subscribe(self):
        stream_id = self.binance_org_websocket_api_manager.create_stream(["trades"], ["RAVEN-F66_BNB"])
        payload = self.binance_org_websocket_api_manager.create_payload(stream_id, 'subscribe',
                                                                         ['trades'],
                                                                         'RAVEN-F66_BNB')
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'trades', 'symbols': ['RAVEN-F66_BNB']}]")

    def test_create_misc_multi_org_subscribe(self):
        stream_id = self.binance_org_websocket_api_manager.create_stream(["trades", 'kline_1m'],
                                                                         ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        payload = self.binance_org_websocket_api_manager.create_payload(stream_id, 'subscribe',
                                                                        ["trades", 'kline_1m'],
                                                                        ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'trades', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}, "
                         "{'method': 'subscribe', 'topic': 'kline_1m', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}]")

    def test_create_misc_multi_org_unsubscribe(self):
        stream_id = self.binance_org_websocket_api_manager.create_stream(["trades", 'kline_1m'],
                                                                         ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        payload = self.binance_org_websocket_api_manager.create_payload(stream_id, 'unsubscribe',
                                                                        ["trades", 'kline_1m'],
                                                                        ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        self.assertEqual(str(payload),
                         "[{'method': 'unsubscribe', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}, "
                         "{'method': 'unsubscribe', 'topic': 'trades'}, "
                         "{'method': 'unsubscribe', 'topic': 'kline_1m'}]")

    def test_create_misc_single_org_unsubscribe(self):
        stream_id = self.binance_org_websocket_api_manager.create_stream(["trades"],
                                                                         ["RAVEN-F66_BNB"])
        payload = self.binance_org_websocket_api_manager.create_payload(stream_id, 'unsubscribe',
                                                                        ["trades"],
                                                                        ["RAVEN-F66_BNB"])
        self.assertEqual(str(payload),
                         "[{'method': 'unsubscribe', 'symbols': ['RAVEN-F66_BNB']}, "
                         "{'method': 'unsubscribe', 'topic': 'trades'}]")

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.binance_org_websocket_api_manager.is_exchange_type("cex"), False)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.binance_org_websocket_api_manager.is_exchange_type("dex"), True)

    def test_create_payload(self):
        result = "[{'method': 'subscribe', 'topic': 'kline_1m', 'symbols': ['RAVEN-F66_BNB']}]"
        stream_id = uuid.uuid4()
        self.assertEqual(str(self.binance_org_websocket_api_manager.create_payload(stream_id,
                                                                                   "subscribe",
                                                                                   ['kline_1m'],
                                                                                   ['RAVEN-F66_BNB'])),
                         result)

    def tearDown(self):
        self.binance_org_websocket_api_manager.stop_manager_with_all_streams()


class TestRestApi(unittest.TestCase):

    def setUp(self):
        self.stream_id = uuid.uuid4()

    def test_rest_binance_com(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-testnet")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_margin(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-margin")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-margin-testnet")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin-testnet")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures-testnet")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.je")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.us")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_isolated_margin_testnet(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="jex.com")
        BinanceWebSocketApiRestclient(binance_websocket_api_manager, self.stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_rest_binance_com_get_signature(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        stream_id = binance_websocket_api_manager.create_stream("arr", "!userData", api_key="key", api_secret="secret")
        rest = BinanceWebSocketApiRestclient(binance_websocket_api_manager, stream_id)
        rest._get_signature("test_data")
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_invalid_exchange(self):
        from unicorn_binance_websocket_api.unicorn_binance_websocket_api_exceptions import UnknownExchange
        try:
            BinanceWebSocketApiManager(exchange="invalid-exchange.com")
        except UnknownExchange:
            pass

    def test_isolated_margin(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin")
        stream_id = binance_websocket_api_manager.create_stream('arr', '!userData', symbols="CELRBTC", api_key="key", api_secret="secret")
        time.sleep(10)
        binance_websocket_api_manager.print_stream_info(stream_id)
        binance_websocket_api_manager.stop_manager_with_all_streams()

    def test_live_run(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager()
        binance_websocket_api_manager.get_active_stream_list()
        binance_websocket_api_manager.get_limit_of_subscriptions_per_stream()
        binance_websocket_api_manager.get_stream_list()

        markets = ['xrpbearbusd', 'zeceth', 'cndbtc', 'dashbtc', 'atompax', 'perlbtc', 'ardreth', 'zecbnb',
                   'bchabctusd',
                   'usdsbusdt', 'winbnb', 'xzcxrp', 'bchusdc', 'wavesbnb', 'kavausdt', 'btsusdt', 'chzbnb', 'tusdbnb',
                   'xtzbusd', 'bcptusdc', 'dogebnb', 'eosbearusdt', 'ambbnb', 'wrxbnb', 'poabtc', 'wanbtc', 'ardrbtc',
                   'icnbtc',
                   'tusdusdt', 'atombusd', 'nxseth', 'bnbusdt', 'trxxrp', 'erdpax', 'erdbtc', 'icxbusd', 'nulsbtc',
                   'hotusdt',
                   'wavespax', 'zilbnb', 'arnbtc', 'nulsusdt', 'wintrx', 'npxsbtc', 'busdtry', 'qtumbnb', 'eosbtc',
                   'xlmpax',
                   'tomobnb', 'eosbnb', 'engbtc', 'linketh', 'xrpbtc', 'fetbtc', 'stratusdt', 'navbnb', 'bcneth',
                   'yoyobtc',
                   'nanobnb', 'saltbtc', 'tfuelusdc', 'skybnb', 'fuelbtc', 'bnbusdc', 'inseth', 'btcpax', 'batbtc',
                   'rlceth',
                   'arketh', 'ltcpax', 'ltcbusd', 'duskbtc', 'mftusdt', 'bntusdt', 'mdabtc', 'enjbtc', 'poabnb',
                   'nanobusd',
                   'paxtusd', 'hotbtc', 'bcdbtc', 'beambnb', 'trxeth', 'omgbnb', 'cdtbtc', 'eosusdc', 'dashbusd',
                   'cocosbtc',
                   'dasheth', 'xrptusd', 'atomtusd', 'rcneth', 'rpxeth', 'xlmusdc', 'aionbusd', 'nxsbtc', 'chateth',
                   'repbtc',
                   'tctusdt', 'linkusdt', 'nasbtc', 'usdsusdc', 'xvgbtc', 'elfeth', 'ctxcbtc', 'cmteth', 'gnteth',
                   'usdspax',
                   'zilbtc', 'batpax', 'stratbtc', 'xzcbtc', 'iotausdt', 'etcbnb', 'ankrusdt', 'xlmeth', 'loombtc',
                   'erdusdc',
                   'rdnbnb', 'icneth', 'vetbtc', 'cvcusdt', 'ftmpax', 'ethbullusdt', 'edoeth', 'steemeth', 'gobnb',
                   'hsrbtc',
                   'ambbtc', 'bchabcbtc', 'dntbtc', 'btctusd', 'denteth', 'snglsbtc', 'eosbullusdt', 'xlmtusd',
                   'tnteth',
                   'sysbnb', 'renusdt', 'zrxusdt', 'xlmbtc', 'stormbtc', 'ncashbnb', 'omgusdt', 'troyusdt', 'venbtc',
                   'modbtc',
                   'dogepax', 'ontusdc', 'eurbusd', 'tctbnb', 'gxsbtc', 'celrbnb', 'adausdt', 'beambtc', 'elfbtc',
                   'celrbtc',
                   'rvnusdt', 'poaeth', 'wavesusdc', 'trxbnb', 'trxusdc', 'ethbearusdt', 'ethpax', 'bateth', 'kavabtc',
                   'paxbtc', 'trigbnb', 'btcusdc', 'oneusdc', 'xrptry', 'stxusdt', 'strateth', 'lendeth', 'neousdc',
                   'mithusdt', 'btcngn', 'blzeth', 'evxeth', 'dnteth', 'grsbtc', 'arneth', 'iotabnb', 'waneth',
                   'xtzbnb',
                   'subeth', 'btsbtc', 'cvceth', 'ethusdc', 'etctusd', 'cloakbtc', 'grseth', 'eospax', 'cdteth',
                   'bchusdt',
                   'lskusdt', 'enjbusd', 'drepbtc', 'manaeth', 'tomousdt', 'algobnb', 'wtceth', 'linkpax', 'batbnb',
                   'sceth',
                   'rvnbusd', 'cvcbnb', 'manabtc', 'gasbtc', 'stxbtc', 'cloaketh', 'neotusd', 'lrceth', 'thetabtc',
                   'dogeusdt',
                   'aionbnb', 'viabtc', 'keyeth', 'nanoeth', 'ncasheth', 'bgbpusdc', 'ltobnb', 'snmeth', 'adabtc',
                   'btseth',
                   'qtumbusd', 'wtcbnb', 'dcrbtc', 'fttbnb', 'paxbnb', 'insbtc', 'gntbnb', 'etheur', 'dashusdt',
                   'rcnbtc',
                   'btcusdt', 'wanusdt', 'powrbnb', 'xmrbnb', 'trigeth', 'xzceth', 'bchbtc', 'qspbnb', 'scbnb',
                   'mcoeth',
                   'powrbtc', 'algotusd', 'ankrbtc', 'tusdeth', 'keybtc', 'usdcusdt', 'ftmusdc', 'atombnb', 'zenbtc',
                   'dockbtc',
                   'neobtc', 'phbbnb', 'bnbpax', 'brdbnb', 'trxusdt', 'trxbusd', 'mtlbtc', 'ftmtusd', 'perlusdc',
                   'mithbnb',
                   'eosbullbusd', 'reqeth', 'bccbnb', 'veneth', 'loombnb', 'trxpax', 'usdcpax', 'stormusdt', 'ognbtc',
                   'gvtbtc',
                   'iotaeth', 'naseth', 'drepusdt', 'gvteth', 'wrxusdt', 'bchabcpax', 'ongbtc', 'usdcbnb', 'dgdeth',
                   'salteth',
                   'mtleth', 'bcnbnb', 'neblbnb', 'wanbnb', 'ontusdt', 'npxsusdt', 'mftbtc', 'eosbearbusd', 'bntbtc',
                   'gtoeth',
                   'modeth', 'etcusdc', 'veteth', 'bcptpax', 'atomusdc', 'duskpax', 'kavabnb', 'lunbtc', 'adxbtc',
                   'bnteth',
                   'funbtc', 'knceth', 'dogebtc', 'bchsvpax', 'bcpttusd', 'osteth', 'oaxeth', 'wabibtc', 'appcbtc',
                   'qkcbtc',
                   'nanousdt', 'wingsbtc', 'hbarusdt', 'eurusdt', 'waveseth', 'asteth', 'linkbusd', 'btttusd',
                   'zecusdc',
                   'bnbusds', 'linkbtc', 'venusdt', 'hotbnb', 'usdtrub', 'tctbtc', 'ankrpax', 'btctry', 'adabnb',
                   'polybtc',
                   'bcceth', 'enjeth', 'bnbbusd', 'repbnb', 'bullusdt', 'vitebtc', 'btgbtc', 'renbtc', 'thetausdt',
                   'troybtc',
                   'dentbtc', 'ostbtc', 'nxsbnb', 'mithbtc', 'xmrbtc', 'tomobtc', 'nulseth', 'phbbtc', 'duskbnb',
                   'yoyoeth',
                   'ontbusd', 'btgeth', 'etcusdt', 'atomusdt', 'hcbtc', 'brdbtc', 'fttbtc', 'celrusdt', 'lskbnb',
                   'phbpax',
                   'xtzbtc', 'batusdt', 'viteusdt', 'trxbtc', 'bchtusd', 'xtzusdt', 'ftmbtc', 'enjbnb', 'arkbtc',
                   'wavesusdt',
                   'ftmusdt', 'neobusd', 'stormbnb', 'luneth', 'gntbtc', 'gtousdt', 'chzusdt', 'sntbtc', 'bandbnb',
                   'hoteth',
                   'wingseth', 'mcobtc', 'docketh', 'drepbnb', 'eosusdt', 'eostusd', 'npxseth', 'thetaeth', 'iotxbtc',
                   'phxbnb',
                   'enjusdt', 'tfuelbnb', 'mcobnb', 'ontpax', 'dcrbnb', 'batusdc', 'snglseth', 'qlcbtc', 'qspeth',
                   'cndeth',
                   'appcbnb', 'wprbtc', 'sysbtc', 'iostusdt', 'btceur', 'mtlusdt', 'ethrub', 'tfuelpax', 'maticusdt',
                   'ftmbnb',
                   'xrpbusd', 'iotxusdt', 'tusdbtusd', 'trigbtc', 'atombtc', 'bchpax', 'eosbusd', 'zileth', 'gtotusd',
                   'xrpbullusdt', 'onetusd', 'algobtc', 'bchsvusdt', 'gtopax', 'etceth', 'vibebtc', 'bttusdt', 'repeth',
                   'iostbnb', 'usdttry', 'btsbnb', 'ankrbnb', 'dltbnb', 'snteth', 'linktusd', 'nknusdt', 'rpxbtc',
                   'rdneth',
                   'cocosusdt', 'etcbusd', 'btttrx', 'bandbtc', 'steembnb', 'zecpax', 'viabnb', 'cosbnb', 'mtheth',
                   'xrpusdc',
                   'xemeth', 'pivxbnb', 'phxbtc', 'zilusdt', 'poeeth', 'bnbeur', 'bandusdt', 'vetbnb', 'lendbtc',
                   'xlmbnb',
                   'duskusdt', 'mfteth', 'funusdt', 'adabusd', 'perlbnb', 'btcbusd', 'ltobtc', 'nasbnb', 'algousdt',
                   'zeneth',
                   'bchsvusdc', 'mcousdt', 'venbnb', 'hceth', 'fetusdt', 'edobtc', 'mftbnb', 'cosusdt', 'arpausdt',
                   'xmrusdt',
                   'ctxcusdt', 'bqxbtc', 'npxsusdc', 'icxbnb', 'bchbnb', 'phbusdc', 'tomousdc', 'nulsbnb', 'rcnbnb',
                   'arpabnb',
                   'qtumbtc', 'keyusdt', 'agibtc', 'mblbtc', 'eoseth', 'tusdbtc', 'aioneth', 'storjbtc', 'lsketh',
                   'bchsvbtc',
                   'bntbusd', 'ncashbtc', 'mblbnb', 'polybnb', 'aebnb', 'ltceth', 'dogeusdc', 'wpreth', 'syseth',
                   'bcnbtc',
                   'ognusdt', 'nanobtc', 'astbtc', 'zrxeth', 'adxeth', 'gxseth', 'ethbearbusd', 'onepax', 'scbtc',
                   'icxbtc',
                   'ontbnb', 'qlceth', 'btsbusd', 'rlcbtc', 'chatbtc', 'wabibnb', 'renbnb', 'xrpbullbusd', 'wavesbtc',
                   'funeth',
                   'rlcbnb', 'phxeth', 'winbtc', 'storjeth', 'wavesbusd', 'iostbtc', 'icxeth', 'adatusd', 'nknbnb',
                   'btcrub',
                   'pivxbtc', 'perlusdt', 'bullbusd', 'bttusdc', 'bcptbtc', 'aebtc', 'ethusdt', 'ltousdt', 'subbtc',
                   'thetabnb',
                   'blzbtc', 'tfuelusdt', 'evxbtc', 'hbarbtc', 'ambeth', 'winusdt', 'qtumeth', 'dgdbtc', 'adaeth',
                   'busdusdt',
                   'xrpbnb', 'adapax', 'usdsbusds', 'cocosbnb', 'navbtc', 'rvnbtc', 'tnbbtc', 'bnbbtc', 'neopax',
                   'bearusdt',
                   'usdstusd', 'snmbtc', 'rvnbnb', 'gtobnb', 'phbtusd', 'hcusdt', 'btcusds', 'reqbtc', 'ognbnb',
                   'lrcbtc',
                   'xrpeth', 'loometh', 'zectusd', 'vibeeth', 'gobtc', 'bnbtry', 'bcdeth', 'qkceth', 'neoeth',
                   'paxusdt',
                   'bchsvtusd', 'fetbnb', 'yoyobnb', 'xlmbusd', 'skyeth', 'paxeth', 'ltcbtc', 'xvgeth', 'tnbeth',
                   'stratbusd',
                   'agieth', 'xlmusdt', 'lskbtc', 'bearbusd', 'hsreth', 'ctxcbnb', 'oaxbtc', 'qspbtc', 'iotxeth',
                   'qlcbnb',
                   'algousdc', 'etcpax', 'fueleth', 'aionusdt', 'xmreth', 'maticbtc', 'dashbnb', 'oneusdt', 'brdeth',
                   'viaeth',
                   'omgeth', 'ankrtusd', 'usdsusdt', 'ethtusd', 'wavestusd', 'iosteth', 'cmtbnb', 'ostbnb', 'ltcusdt',
                   'ethtry',
                   'zrxbtc', 'bchabcusdt', 'onebnb', 'beamusdt', 'nebleth', 'bcptbnb', 'adxbnb', 'ontbtc', 'bttbnb',
                   'dockusdt',
                   'bccbtc', 'omgbtc', 'algopax', 'neousdt', 'xrprub', 'busdngn', 'appceth', 'dentusdt', 'xzcbnb',
                   'tfueltusd',
                   'xembnb', 'arpabtc', 'ankrusdc', 'adausdc', 'kmdeth', 'troybnb', 'bnbeth', 'ltcusdc', 'databtc',
                   'blzbnb',
                   'naveth', 'btcbbtc', 'battusd', 'bnbngn', 'bchbusd', 'busdrub', 'ltctusd', 'vetbusd', 'ongbnb',
                   'fttusdt',
                   'bccusdt', 'ongusdt', 'engeth', 'usdctusd', 'etcbtc', 'gtousdc', 'mdaeth', 'vitebnb', 'erdusdt',
                   'dltbtc',
                   'bnbtusd', 'wtcbtc', 'xrpusdt', 'xrpeur', 'agibnb', 'trxtusd', 'ethbullbusd', 'iotabtc', 'xembtc',
                   'bchabcusdc', 'duskusdc', 'xrppax', 'mblusdt', 'kmdbtc', 'neblbtc', 'maticbnb', 'bnbrub', 'bcpteth',
                   'bttbtc', 'stxbnb', 'dlteth', 'onteth', 'vetusdt', 'ppteth', 'ethbtc', 'onebtc', 'ethbusd', 'zecbtc',
                   'erdbnb', 'xrpbearusdt', 'stratbnb', 'cmtbtc', 'cvcbtc', 'kncbtc', 'rpxbnb', 'zenbnb', 'cndbnb',
                   'ardrbnb',
                   'bchabcbusd', 'ltcbnb', 'pivxeth', 'skybtc', 'tntbtc', 'poebtc', 'steembtc', 'icxusdt', 'tfuelbtc',
                   'chzbtc',
                   'vibeth', 'winusdc', 'gtobtc', 'linkusdc', 'batbusd', 'rdnbtc', 'dataeth', 'bttpax', 'zrxbnb',
                   'vibbtc',
                   'neobnb', 'cosbtc', 'powreth', 'rlcusdt', 'hbarbnb', 'wabieth', 'bqxeth', 'aionbtc', 'aeeth',
                   'mthbtc',
                   'wrxbtc', 'pptbtc', 'nknbtc', 'zecusdt', 'stormeth', 'qtumusdt']

        channels = ['kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'kline_1w', 'trade',
                    'miniTicker', 'depth20']

        binance_websocket_api_manager.create_stream(False, False, stream_label="error")

        for channel in channels:
            stream_id1 = binance_websocket_api_manager.create_stream(channel, markets, output="UnicornFy")

        time.sleep(5)
        binance_websocket_api_manager.set_restart_request(stream_id1)
        time.sleep(10)
        binance_websocket_api_manager.set_restart_request(stream_id1)

        restserver = BinanceWebSocketApiRestServer(binance_websocket_api_manager)
        restserver.get("icinga")
        restserver.get("invalid")

        markets = ['xrpbearbusd', 'zeceth', 'cndbtc', 'dashbtc', 'atompax', 'perlbtc', 'ardreth', 'zecbnb',
                   'erdbnb', 'xrpbearusdt', 'stratbnb', 'cmtbtc', 'cvcbtc', 'kncbtc', 'rpxbnb', 'zenbnb', 'cndbnb',
                   'wrxbtc', 'pptbtc', 'nknbtc', 'zecusdt', 'stormeth', 'qtumusdt']

        for channel in channels:
            stream_id2 = binance_websocket_api_manager.create_stream(channel, markets, stream_buffer_name=channel)

        time.sleep(10)
        binance_websocket_api_manager.unsubscribe_from_stream(stream_id2, markets="erdbnb")
        binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        binance_websocket_api_manager.pop_stream_data_from_stream_buffer(stream_buffer_name="invalid")
        binance_websocket_api_manager.replace_stream(stream_id1, 'trade', 'kncbtc', "name")

        binance_websocket_api_manager.get_results_from_endpoints()
        binance_websocket_api_manager.get_stream_subscriptions(stream_id2)
        binance_websocket_api_manager.get_reconnects()
        binance_websocket_api_manager.get_errors_from_endpoints()
        binance_websocket_api_manager.get_monitoring_status_plain()
        binance_websocket_api_manager.get_ringbuffer_error_max_size()
        binance_websocket_api_manager.set_private_api_config("aaaa", "bbbb")
        binance_websocket_api_manager.get_ringbuffer_result_max_size()
        binance_websocket_api_manager.get_websocket_uri_length('trade', 'kncbtc', False)
        binance_websocket_api_manager.set_ringbuffer_error_max_size(200)
        binance_websocket_api_manager.set_ringbuffer_result_max_size(300)
        binance_websocket_api_manager.set_stream_label(stream_id2, "blub")
        binance_websocket_api_manager.delete_stream_from_stream_list(stream_id1)
        binance_websocket_api_manager.delete_listen_key_by_stream_id(stream_id1)
        binance_websocket_api_manager.create_payload(stream_id2, "invalid", channels="trade")
        time.sleep(10)
        binance_websocket_api_manager.set_keep_max_received_last_second_entries(30)
        binance_websocket_api_manager.stop_stream_as_crash(stream_id2)
        binance_websocket_api_manager.stop_stream(stream_id2)
        binance_websocket_api_manager.add_to_ringbuffer_error("test")
        binance_websocket_api_manager.add_to_ringbuffer_result("test")
        binance_websocket_api_manager.get_number_of_free_subscription_slots(stream_id2)
        binance_websocket_api_manager.get_most_receives_per_second()
        binance_websocket_api_manager.get_number_of_streams_in_stream_list()
        binance_websocket_api_manager.is_update_availabe_check_command()
        binance_websocket_api_manager.wait_till_stream_has_stopped(stream_id2)
        binance_websocket_api_manager.print_stream_info(stream_id2)
        binance_websocket_api_manager.print_summary()
        binance_websocket_api_manager.print_summary_to_png(".", 12.5)
        binance_websocket_api_manager.get_latest_release_info()
        binance_websocket_api_manager.get_latest_release_info_check_command()
        binance_websocket_api_manager.set_private_dex_config("blasfjsalkfjsf222lks")
        binance_websocket_api_manager.get_version()
        binance_websocket_api_manager.help()
        binance_websocket_api_manager.wait_till_stream_has_started(stream_id2)
        binance_websocket_api_manager.remove_ansi_escape_codes("test text")
        time.sleep(10)
        binance_websocket_api_manager.stop_manager_with_all_streams()


if __name__ == '__main__':
    unittest.main()
