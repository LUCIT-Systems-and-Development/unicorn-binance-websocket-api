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
# Copyright (c) 2019-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
from unicorn_binance_websocket_api.exceptions import *
from unicorn_binance_websocket_api.restserver import BinanceWebSocketApiRestServer
from unicorn_binance_websocket_api.restclient import BinanceWebSocketApiRestclient
from unicorn_binance_websocket_api.licensing_manager import LucitLicensingManager
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import unittest
import os
import platform
import time
import threading

import tracemalloc
tracemalloc.start(25)

BINANCE_COM_API_KEY = ""
BINANCE_COM_API_SECRET = ""

BINANCE_COM_TESTNET_API_KEY = ""
BINANCE_COM_TESTNET_API_SECRET = ""

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

print(f"Starting unittests!")


async def processing_of_new_data_async(data):
    print(f"`processing_of_new_data_async()` test - Received: {data}")
    await asyncio.sleep(0.001)
    print("AsyncIO Check done!")


def handle_socket_message(data):
    print(f"Received ws api data:\r\n{data}\r\n")


def processing_of_new_data(data):
    print(f"`processing_of_new_data()` test - Received: {data}")


def is_github_action_env():
    try:
        print(f"{os.environ[f'LUCIT_LICENSE_TOKEN']}")
        return True
    except KeyError:
        return False


class TestBinanceComManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\r\nTestBinanceComManager:")
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.us",
                                              disable_colorama=True,
                                              debug=True)
        cls.binance_com_api_key = ""
        cls.binance_com_api_secret = ""

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_monitoring_api()
        cls.ubwa.stop_manager()
        print(f"\r\nTestBinanceComManager threads:")
        for thread in threading.enumerate():
            print(thread.name)
        print(f"TestBinanceComManager stopping:")

    def test_create_uri_miniticker_regular_com(self):
        print(f"test_create_uri_miniticker_regular_com():")
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://stream.binance.us:9443/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_com(self):
        print(f"test_create_uri_miniticker_reverse_com():")
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://stream.binance.us:9443/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_com(self):
        print(f"test_create_uri_ticker_regular_com():")
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://stream.binance.us:9443/ws/!ticker@arr')

    def test_create_uri_ticker_reverse_com(self):
        print(f"test_create_uri_ticker_reverse_com():")
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://stream.binance.us:9443/ws/!ticker@arr')

    def test_create_uri_userdata_regular_false_com(self):
        print(f"test_create_uri_userdata_regular_false_com():")
        self.assertFalse(self.__class__.ubwa.create_websocket_uri(["!userData"], ["arr"]))

    def test_create_uri_userdata_reverse_false_com(self):
        print(f"test_create_uri_userdata_reverse_false_com():")
        self.assertFalse(self.__class__.ubwa.create_websocket_uri(["arr"], ["!userData"]))

    def test_create_uri_userdata_regular_com(self):
        print(f"test_create_uri_userdata_regular_com():")
        if len(self.binance_com_api_key) == 0 or len(self.binance_com_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_regular_com() "
                  "for binance.com")
        else:
            stream_id = self.ubwa.get_new_uuid_id()
            self.__class__.ubwa._add_stream_to_stream_list(stream_id, ["!userData"], ["arr"])
            self.assertRegex(self.__class__.ubwa.create_websocket_uri(["!userData"], ["arr"],
                                                                      stream_id,
                                                                      self.binance_com_api_key,
                                                                      self.binance_com_api_secret),
                             r'wss://stream.binance.com:9443/ws/.')

    def test_create_uri_userdata_reverse_com(self):
        print(f"test_create_uri_userdata_reverse_com():")
        if len(self.binance_com_api_key) == 0 or len(self.binance_com_api_secret) == 0:
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_reverse_com() "
                  "for binance.com")
        else:
            self.stream_id = self.__class__.ubwa.get_new_uuid_id()
            self.__class__.ubwa._add_stream_to_stream_list(self.stream_id, ["arr"], ["!userData"])
            self.assertRegex(self.__class__.ubwa.create_websocket_uri(["arr"], ["!userData"],
                                                                      self.stream_id,
                                                                      self.binance_com_api_key,
                                                                      self.binance_com_api_secret),
                             'wss://stream.binance.com:9443/ws/.')

    def test_is_exchange_type_cex(self):
        print(f"test_is_exchange_type_cex():")
        self.assertEqual(self.__class__.ubwa.is_exchange_type("cex"), True)

    def test_is_exchange_type_dex(self):
        print(f"test_is_exchange_type_dex():")
        self.assertEqual(self.__class__.ubwa.is_exchange_type("dex"), False)

    def test_is_update_available(self):
        print(f"test_is_update_available():")
        result = self.__class__.ubwa.is_update_available()
        is_valid_result = result is True or result is False
        self.assertTrue(is_valid_result, False)

    def test_is_manager_stopping(self):
        print(f"test_is_manager_stopping():")
        self.assertEqual(self.__class__.ubwa.is_manager_stopping(), False)

    def test_get_human_uptime(self):
        print(f"test_get_human_uptime():")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60 * 60 * 60 * 61), "152d:12h:0m:0s")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60 * 60 * 24), "24h:0m:0s")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60 * 60), "60m:0s")
        self.assertEqual(self.__class__.ubwa.get_human_uptime(60), "60 seconds")

    def test_get_human_bytesize(self):
        print(f"test_get_human_bytesize():")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024 * 1024 * 1024 * 1024), "1024.0 tB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024 * 1024 * 1024), "1024.0 gB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024 * 1024), "1024.0 mB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024 * 1024), "1024.0 kB")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1024), "1024 B")
        self.assertEqual(self.__class__.ubwa.get_human_bytesize(1), "1 B")

    def test_get_exchange(self):
        print(f"test_get_exchange():")
        self.assertEqual(self.__class__.ubwa.get_exchange(), "binance.us")

    def test_get_listenkey_from_restclient(self):
        print(f"test_get_listenkey_from_restclient():")
        self.assertEqual(self.__class__.ubwa.get_listen_key_from_restclient("ID"), False)

    def test_delete_listen_key_by_stream_id(self):
        print(f"test_delete_listen_key_by_stream_id():")
        stream_id = self.__class__.ubwa.get_new_uuid_id()
        self.assertEqual(self.__class__.ubwa.delete_listen_key_by_stream_id(stream_id), False)

    def test_create_payload_subscribe(self):
        print(f"test_create_payload_subscribe():")
        result = "[{'method': 'SUBSCRIBE', 'params': ['bnbbtc@kline_1m'], 'id': 1}]"
        stream_id = self.__class__.ubwa.get_new_uuid_id()
        self.assertEqual(str(self.__class__.ubwa.create_payload(stream_id, "subscribe",
                                                                ['kline_1m'], ['bnbbtc'])), result)

    def test_fill_up_space_centered(self):
        print(f"test_fill_up_space_centered():")
        result = "==========test text=========="
        self.assertEqual(str(self.__class__.ubwa.fill_up_space_centered(30, "test text", "=")),
                         result)

    def test_fill_up_space_right(self):
        print(f"test_fill_up_space_right():")
        result = "|test text||||||||||||||||||||"
        self.assertEqual(str(self.__class__.ubwa.fill_up_space_right(30, "test text", "|")),
                         result)

    def test_fill_up_space_left(self):
        print(f"test_fill_up_space_left():")
        result = "||||||||||||||||||||test text|"
        self.assertEqual(str(self.__class__.ubwa.fill_up_space_left(30, "test text", "|")),
                         result)

    def test_create_stream_userdata_with(self):
        print(f"test_create_stream_userdata_with():")
        with BinanceWebSocketApiManager(exchange="binance.us") as ubwa:
            ubwa.create_stream('arr', '!userData', stream_label="userDataBad")
            time.sleep(10)
        print(f"Leaving ... ")

    def test_create_stream(self):
        print(f"test_create_stream():")
        self.assertTrue(bool(self.__class__.ubwa.create_stream(markets=['bnbbtc'], channels="trade",
                                                               stream_label="test_stream")))
        stream_id = self.__class__.ubwa.get_stream_id_by_label("test_stream")
        time.sleep(5)
        self.__class__.ubwa.unsubscribe_from_stream(stream_id, markets=['bnbbtc'])
        self.__class__.ubwa.unsubscribe_from_stream(stream_id, channels=['trade'])
        time.sleep(6)
        self.__class__.ubwa.get_monitoring_status_icinga()
        self.__class__.ubwa.print_summary(title="Unittests")
        self.__class__.ubwa.print_stream_info(stream_id, title="Unittests")

    def test_start_monitoring_api(self):
        print(f"test_start_monitoring_api():")
        with BinanceWebSocketApiManager(exchange="binance.com-testnet",
                                        debug=True,) as ubwa:
            self.assertTrue(ubwa.start_monitoring_api())
            time.sleep(6)
            self.assertTrue(ubwa.stop_monitoring_api())


class TestBinanceComManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\r\nTestBinanceComManagerTest:")
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.com-testnet",
                                              debug=True)
        cls.binance_com_testnet_api_key = BINANCE_COM_TESTNET_API_KEY
        cls.binance_com_testnet_api_secret = BINANCE_COM_TESTNET_API_SECRET

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_manager()
        print(f"\r\nTestBinanceComManagerTest threads:")
        for thread in threading.enumerate():
            print(thread.name)
        print(f"TestBinanceComManagerTest stopping:")

    def test_create_uri_miniticker_regular_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://testnet.binance.vision/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://testnet.binance.vision/ws/!miniTicker@arr')

    def test_create_uri_ticker_regular_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://testnet.binance.vision/ws/!ticker@arr')

    def test_create_uri_ticker_reverse_com(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://testnet.binance.vision/ws/!ticker@arr')

    def test_create_uri_userdata_regular_false_com(self):
        self.assertFalse(self.__class__.ubwa.create_websocket_uri(["!userData"], ["arr"]))

    def test_create_uri_userdata_reverse_false_com(self):
        self.assertFalse(self.__class__.ubwa.create_websocket_uri(["arr"], ["!userData"]))

    def test_create_uri_userdata_regular_com(self):
        if (len(self.__class__.binance_com_testnet_api_key) == 0 or
                len(self.__class__.binance_com_testnet_api_secret) == 0):
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_regular_com() "
                  "for binance.com-testnet")
        else:
            stream_id = self.__class__.ubwa.get_new_uuid_id()
            self.__class__.ubwa._add_stream_to_stream_list(stream_id, ["!userData"], ["arr"])
            self.assertRegex(self.__class__.ubwa.create_websocket_uri(["!userData"], ["arr"],
                                                                      stream_id,
                                                                      self.__class__.binance_com_testnet_api_key,
                                                                      self.__class__.binance_com_testnet_api_secret),
                             r'wss://testnet.binance.vision/ws/.')

    def test_create_uri_userdata_reverse_com(self):
        if (len(self.__class__.binance_com_testnet_api_key) == 0 or
                len(self.__class__.binance_com_testnet_api_secret) == 0):
            print("\r\nempty API key and/or secret: can not successfully test test_create_uri_userdata_reverse_com() "
                  "for binance.com-testnet")
        else:
            stream_id = self.__class__.ubwa.get_new_uuid_id()
            self.__class__.ubwa._add_stream_to_stream_list(stream_id, ["arr"], ["!userData"])
            self.assertRegex(self.__class__.ubwa.create_websocket_uri(["arr"], ["!userData"],
                                                                      stream_id,
                                                                      self.binance_com_testnet_api_key,
                                                                      self.binance_com_testnet_api_secret),
                             r'wss://stream.binance.com:9443/ws/.')

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.__class__.ubwa.is_exchange_type("cex"), True)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.__class__.ubwa.is_exchange_type("dex"), False)

    def test_z_stop_manager(self):
        time.sleep(6)
        self.__class__.ubwa.stop_manager()


class TestBinanceOrgManagerTestnet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\r\nTestBinanceOrgManagerTestnet:")
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.org-testnet",
                                              debug=True)

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_manager()
        print(f"\r\nTestBinanceOrgManagerTestnet threads:")
        for thread in threading.enumerate():
            print(thread.name)
        print(f"TestBinanceOrgManagerTestnet stopping:")

    def test_testnet(self):
        stream_id = self.__class__.ubwa.create_stream(['orders', 'transfers', 'accounts'],
                                                      "tbnb1unxhf8fat985ksajatfa5jea58j2kzg7mfy0e7")
        time.sleep(6)
        self.__class__.ubwa.unsubscribe_from_stream(stream_id, "tbnb1unxhf8fat985ksajatfa5jea58j2kzg7mfy0e7")

    def test_z_stop_manager(self):
        self.__class__.ubwa.stop_manager()


class TestBinanceOrgManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\r\nTestBinanceOrgManager:")
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.org",
                                              debug=True)

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_manager()
        print(f"\r\nTestBinanceOrgManager threads:")
        for thread in threading.enumerate():
            print(thread.name)
        print(f"TestBinanceOrgManager stopping:")

    def test_create_uri_alltickers_regular_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["$all"], ["allTickers"]),
                         'wss://dex.binance.org/api/ws/$all@allTickers')

    def test_create_uri_alltickers_reverse_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["allTickers"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@allTickers')

    def test_create_uri_allminitickers_regular_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["$all"], ["allMiniTickers"]),
                         'wss://dex.binance.org/api/ws/$all@allMiniTickers')

    def test_create_uri_allminitickers_reverse_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["allMiniTickers"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@allMiniTickers')

    def test_create_uri_blockheight_regular_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["$all"], ["blockheight"]),
                         'wss://dex.binance.org/api/ws/$all@blockheight')

    def test_create_uri_blockheight_reverse_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["blockheight"], ["$all"]),
                         'wss://dex.binance.org/api/ws/$all@blockheight')

    def test_create_uri_single_trades_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["trades"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@trades')

    def test_create_uri_single_marketdepth_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["marketDepth"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@marketDepth')

    def test_create_uri_single_kline_1h_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["kline_1h"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@kline_1h')

    def test_create_uri_single_ticker_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["ticker"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@ticker')

    def test_create_uri_single_miniTicker_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(["miniTicker"], ["RAVEN-F66_BNB"]),
                         'wss://dex.binance.org/api/ws/RAVEN-F66_BNB@miniTicker')

    def test_create_uri_multi_org_subscribe(self):
        self.assertEqual(self.__class__.ubwa.create_websocket_uri(['trades', 'kline_1h'],
                                                                  ['RAVEN-F66_BNB', 'ANKR-E97_BNB']),
                         'wss://dex.binance.org/api/ws')

        stream_id = self.__class__.ubwa.create_stream(['trades', 'kline_1h'],
                                                      ['RAVEN-F66_BNB', 'ANKR-E97_BNB'])
        payload = self.__class__.ubwa.create_payload(stream_id, "subscribe", ['trades', 'kline_1h'],
                                                     ['RAVEN-F66_BNB', 'ANKR-E97_BNB'])
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'trades', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}, "
                         "{'method': 'subscribe', 'topic': 'kline_1h', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}]")

    def test_create_uri_user_address_orders_single_org_subscribe(self):
        self.assertEqual(
            self.__class__.ubwa.create_websocket_uri('orders',
                                                     'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'),
            'wss://dex.binance.org/api/ws/bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')

    def test_create_uri_user_address_accounts_single_org_subscribe(self):
        self.assertEqual(
            self.__class__.ubwa.create_websocket_uri('accounts',
                                                     'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'),
            'wss://dex.binance.org/api/ws/bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')

    def test_create_uri_user_address_transfers_single_org_subscribe(self):
        self.assertEqual(
            self.__class__.ubwa.create_websocket_uri('transfers',
                                                     'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'),
            'wss://dex.binance.org/api/ws/bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')

    def test_create_uri_user_address_multi_org_subscribe(self):
        stream_id = self.__class__.ubwa.create_stream(['orders', 'transfers', 'accounts'],
                                                      'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')
        payload = self.__class__.ubwa.create_payload(stream_id, 'subscribe',
                                                     ['orders', 'transfers', 'accounts'],
                                                     'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6')
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'orders', "
                         "'address': 'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'}, "
                         "{'method': 'subscribe', 'topic': 'transfers', "
                         "'address': 'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'}, "
                         "{'method': 'subscribe', 'topic': 'accounts', "
                         "'address': 'bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6'}]")

    def test_create_misc_single_org_subscribe(self):
        stream_id = self.__class__.ubwa.create_stream(["trades"], ["RAVEN-F66_BNB"])
        payload = self.__class__.ubwa.create_payload(stream_id, 'subscribe', ['trades'], 'RAVEN-F66_BNB')
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'trades', 'symbols': ['RAVEN-F66_BNB']}]")

    def test_create_misc_multi_org_subscribe(self):
        stream_id = self.__class__.ubwa.create_stream(["trades", 'kline_1m'], ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        payload = self.__class__.ubwa.create_payload(stream_id, 'subscribe',
                                                     ["trades", 'kline_1m'],
                                                     ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        self.assertEqual(str(payload),
                         "[{'method': 'subscribe', 'topic': 'trades', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}, "
                         "{'method': 'subscribe', 'topic': 'kline_1m', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}]")

    def test_create_misc_multi_org_unsubscribe(self):
        stream_id = self.__class__.ubwa.create_stream(["trades", 'kline_1m'], ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        payload = self.__class__.ubwa.create_payload(stream_id, 'unsubscribe',
                                                     ["trades", 'kline_1m'],
                                                     ["RAVEN-F66_BNB", "ANKR-E97_BNB"])
        self.assertEqual(str(payload),
                         "[{'method': 'unsubscribe', 'symbols': ['RAVEN-F66_BNB', 'ANKR-E97_BNB']}, "
                         "{'method': 'unsubscribe', 'topic': 'trades'}, "
                         "{'method': 'unsubscribe', 'topic': 'kline_1m'}]")

    def test_create_misc_single_org_unsubscribe(self):
        stream_id = self.__class__.ubwa.create_stream(["trades"], ["RAVEN-F66_BNB"])
        payload = self.__class__.ubwa.create_payload(stream_id, 'unsubscribe', ["trades"], ["RAVEN-F66_BNB"])
        self.assertEqual(str(payload),
                         "[{'method': 'unsubscribe', 'symbols': ['RAVEN-F66_BNB']}, "
                         "{'method': 'unsubscribe', 'topic': 'trades'}]")

    def test_is_exchange_type_cex(self):
        self.assertEqual(self.__class__.ubwa.is_exchange_type("cex"), False)

    def test_is_exchange_type_dex(self):
        self.assertEqual(self.__class__.ubwa.is_exchange_type("dex"), True)

    def test_create_payload(self):
        result = "[{'method': 'subscribe', 'topic': 'kline_1m', 'symbols': ['RAVEN-F66_BNB']}]"
        stream_id = self.__class__.ubwa.get_new_uuid_id()
        self.assertEqual(str(self.__class__.ubwa.create_payload(stream_id,
                                                                "subscribe",
                                                                ['kline_1m'],
                                                                ['RAVEN-F66_BNB'])),
                         result)

    def test_z_stop_manager(self):
        self.__class__.ubwa.stop_manager()

    class TestWSApiLive(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            print(f"\r\nTestWSApiLive:")

        @classmethod
        def tearDownClass(cls):
            print(f"\r\nTestWSApiLive threads:")
            for thread in threading.enumerate():
                print(thread.name)
            print(f"TestApiLive stopping:")

    def test_lucitlicmgr(self):
        print(f"License Manager ...")
        ubwam = BinanceWebSocketApiManager(exchange='binance.com')
        ubwam.llm.get_info()
        ubwam.llm.get_module_version()
        ubwam.llm.get_quotas()
        ubwam.llm.get_timestamp()
        ubwam.llm.get_version()
        ubwam.llm.is_verified()
        ubwam.llm.sync_time()
        ubwam.llm.test()
        ubwam.llm.process_licensing_error()
        ubwam.llm.stop()
        llm = LucitLicensingManager(api_secret="wrong", license_token="credentials")
        time.sleep(3)
        ubwam.stop_manager()
        llm.stop()

    def test_live_api_ws(self):
        print(f"Test Websocket API ...")
        if not is_github_action_env():
            ubwam = BinanceWebSocketApiManager(exchange='binance.com')
            api_stream = ubwam.create_stream(api=True, api_key=BINANCE_COM_API_KEY, api_secret=BINANCE_COM_API_SECRET,
                                             stream_label="Bobs Websocket API",
                                             process_stream_data=handle_socket_message)
            time.sleep(5)
            ubwam.api.get_listen_key(stream_id=api_stream)
            ubwam.api.get_server_time(stream_id=api_stream)
            ubwam.api.get_account_status(stream_id=api_stream)
            orig_client_order_id = ubwam.api.create_order(stream_id=api_stream, price=1.0, order_type="LIMIT",
                                                         quantity=15.0, side="SELL", symbol="BUSDUSDT")
            ubwam.api.create_test_order(stream_id=api_stream, price=1.2, order_type="LIMIT",
                                       quantity=12.0, side="SELL", symbol="BUSDUSDT")
            ubwam.api.ping(stream_id=api_stream)
            ubwam.api.get_exchange_info(stream_id=api_stream, symbols=['BUSDUSDT'])
            ubwam.api.get_order_book(stream_id=api_stream, symbol="BUSDUSDT", limit=2)
            ubwam.api.cancel_order(stream_id=api_stream, symbol="BUSDUSDT", orig_client_order_id=orig_client_order_id)
            ubwam.api.get_open_orders(stream_id=api_stream, symbol="BUSDUSDT")
            ubwam.api.get_open_orders(stream_id=api_stream)
            ubwam.api.cancel_open_orders(stream_id=api_stream, symbol="BUSDUSDT")
            ubwam.api.get_order(stream_id=api_stream, symbol="BUSDUSDT", orig_client_order_id=orig_client_order_id)
            time.sleep(5)
            ubwam.stop_manager()


class TestApiLive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f"\r\nTestApiLive:")
        cls.ubwa = BinanceWebSocketApiManager(exchange="binance.us",
                                              debug=True,
                                              enable_stream_signal_buffer=True,
                                              auto_data_cleanup_stopped_streams=True)
        cls.count_receives = 0

    @classmethod
    def tearDownClass(cls):
        cls.ubwa.stop_manager()
        print(f"\r\nTestApiLive threads:")
        for thread in threading.enumerate():
            print(thread.name)
        print(f"TestApiLive stopping:")

    def test_get_new_uuid_id(self):
        self.__class__.ubwa.get_new_uuid_id()

    def test_rest_binance_com(self):
        BinanceWebSocketApiRestclient(self.__class__.ubwa)

    def test_z_rest_binance_com_isolated_margin(self):
        ubwa = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin")
        BinanceWebSocketApiRestclient(ubwa)
        ubwa.stop_manager()

    def test_z_rest_binance_com_isolated_margin_testnet(self):
        ubwa = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin-testnet")
        BinanceWebSocketApiRestclient(ubwa)
        ubwa.stop_manager()

    def test_z_invalid_exchange(self):
        from unicorn_binance_websocket_api.exceptions import UnknownExchange
        with self.assertRaises(UnknownExchange):
            ubwa_error = BinanceWebSocketApiManager(exchange="invalid-exchange.com")
            ubwa_error.stop_manager()

# Todo: Needs a proxy ...
#    def test_isolated_margin(self):
#        self.__class__.ubwa = BinanceWebSocketApiManager(exchange="binance.com-isolated_margin")
#        stream_id = self.__class__.ubwa.create_stream('arr', '!userData', symbols="CELRBTC",
#                                                      api_key="key", api_secret="secret")
#        time.sleep(10)
#        print("\r\n")
#        self.__class__.ubwa.print_stream_info(stream_id)
#        self.__class__.ubwa.stop_manager()

    def test_live_receives_stream_specific_with_stream_buffer(self):
        print(f"Test receiving with stream specific stream_buffer ...")
        stream_id = self.__class__.ubwa.create_stream(["arr"], ["!miniTicker"], stream_buffer_name=True)
        count_receives = 0
        while count_receives < 5:
            received = self.__class__.ubwa.pop_stream_data_from_stream_buffer(stream_id)
            if received:
                print(f"Received: {received}")
                count_receives += 1
        self.assertEqual(count_receives, 5)

    def test_live_receives_asyncio_queue(self):
        async def process_asyncio_queue(stream_id=None):
            print(f"Start processing data of {stream_id} from asyncio_queue...")
            self.count_receives = 0
            while self.count_receives < 5:
                data = await self.__class__.ubwa.get_stream_data_from_asyncio_queue(stream_id)
                print(f"Received async: {data}")
                self.count_receives += 1
                self.__class__.ubwa.asyncio_queue_task_done(stream_id)
            print(f"Closing asyncio_queue consumer!")

        print(f"Test receiving with stream specific asyncio_queue ...")
        stream_id_1 = self.__class__.ubwa.create_stream(["arr"], ["!miniTicker"],
                                                        process_asyncio_queue=process_asyncio_queue)
        while self.count_receives < 5:
            time.sleep(1)
        self.assertEqual(self.count_receives, 5)
        time.sleep(3)
        self.__class__.ubwa.stop_stream(stream_id=stream_id_1)

    def test_exceptions(self):
        try:
            raise StreamIsStopping(stream_id="blah", reason="test")
        except StreamIsStopping as e:
            print(str(e))

    def test_live_run(self):
        self.__class__.ubwa.get_active_stream_list()
        self.__class__.ubwa.get_limit_of_subscriptions_per_stream()
        self.__class__.ubwa.get_stream_list()

        markets = ['xrpbearbusd', 'zeceth', 'cndbtc', 'dashbtc', 'atompax', 'perlbtc', 'ardreth', 'zecbnb',
                   'usdsbusdt', 'winbnb', 'xzcxrp', 'bchusdc', 'wavesbnb', 'kavausdt', 'btsusdt', 'chzbnb', 'tusdbnb',
                   'xtzbusd', 'bcptusdc', 'dogebnb', 'eosbearusdt', 'ambbnb', 'wrxbnb', 'poabtc', 'wanbtc', 'ardrbtc',
                   'tusdusdt', 'atombusd', 'nxseth', 'bnbusdt', 'trxxrp', 'erdpax', 'erdbtc', 'icxbusd', 'nulsbtc',
                   'wavespax', 'zilbnb', 'arnbtc', 'nulsusdt', 'wintrx', 'npxsbtc', 'busdtry', 'qtumbnb', 'eosbtc',
                   'tomobnb', 'eosbnb', 'engbtc', 'linketh', 'xrpbtc', 'fetbtc', 'stratusdt', 'navbnb', 'bcneth',
                   'nanobnb', 'saltbtc', 'tfuelusdc', 'skybnb', 'fuelbtc', 'bnbusdc', 'inseth', 'btcpax', 'batbtc',
                   'arketh', 'ltcpax', 'ltcbusd', 'duskbtc', 'mftusdt', 'bntusdt', 'mdabtc', 'enjbtc', 'poabnb',
                   'paxtusd', 'hotbtc', 'bcdbtc', 'beambnb', 'trxeth', 'omgbnb', 'cdtbtc', 'eosusdc', 'dashbusd',
                   'dasheth', 'xrptusd', 'atomtusd', 'rcneth', 'rpxeth', 'xlmusdc', 'aionbusd', 'nxsbtc', 'chateth',
                   'tctusdt', 'linkusdt', 'nasbtc', 'usdsusdc', 'xvgbtc', 'elfeth', 'ctxcbtc', 'cmteth', 'gnteth',
                   'zilbtc', 'batpax', 'stratbtc', 'xzcbtc', 'iotausdt', 'etcbnb', 'ankrusdt', 'xlmeth', 'loombtc',
                   'rdnbnb', 'icneth', 'vetbtc', 'cvcusdt', 'ftmpax', 'ethbullusdt', 'edoeth', 'steemeth', 'gobnb',
                   'ambbtc', 'bchabcbtc', 'dntbtc', 'btctusd', 'denteth', 'snglsbtc', 'eosbullusdt', 'xlmtusd',
                   'sysbnb', 'renusdt', 'zrxusdt', 'xlmbtc', 'stormbtc', 'ncashbnb', 'omgusdt', 'troyusdt', 'venbtc',
                   'dogepax', 'ontusdc', 'eurbusd', 'tctbnb', 'gxsbtc', 'celrbnb', 'adausdt', 'beambtc', 'elfbtc',
                   'rvnusdt', 'poaeth', 'wavesusdc', 'trxbnb', 'trxusdc', 'ethbearusdt', 'ethpax', 'bateth', 'kavabtc',
                   'paxbtc', 'trigbnb', 'btcusdc', 'oneusdc', 'xrptry', 'stxusdt', 'strateth', 'lendeth', 'neousdc',
                   'mithusdt', 'btcngn', 'blzeth', 'evxeth', 'dnteth', 'grsbtc', 'arneth', 'iotabnb', 'waneth',
                   'subeth', 'btsbtc', 'cvceth', 'ethusdc', 'etctusd', 'cloakbtc', 'grseth', 'eospax', 'cdteth',
                   'lskusdt', 'enjbusd', 'drepbtc', 'manaeth', 'tomousdt', 'algobnb', 'wtceth', 'linkpax', 'batbnb',
                   'rvnbusd', 'cvcbnb', 'manabtc', 'gasbtc', 'stxbtc', 'cloaketh', 'neotusd', 'lrceth', 'thetabtc',
                   'aionbnb', 'viabtc', 'keyeth', 'nanoeth', 'ncasheth', 'bgbpusdc', 'ltobnb', 'snmeth', 'adabtc',
                   'qtumbusd', 'wtcbnb', 'dcrbtc', 'fttbnb', 'paxbnb', 'insbtc', 'gntbnb', 'etheur', 'dashusdt',
                   'btcusdt', 'wanusdt', 'powrbnb', 'xmrbnb', 'trigeth', 'xzceth', 'bchbtc', 'qspbnb', 'scbnb',
                   'powrbtc', 'algotusd', 'ankrbtc', 'tusdeth', 'keybtc', 'usdcusdt', 'ftmusdc', 'atombnb', 'zenbtc',
                   'neobtc', 'phbbnb', 'bnbpax', 'brdbnb', 'trxusdt', 'trxbusd', 'mtlbtc', 'ftmtusd', 'perlusdc',
                   'eosbullbusd', 'reqeth', 'bccbnb', 'veneth', 'loombnb', 'trxpax', 'usdcpax', 'stormusdt', 'ognbtc',
                   'iotaeth', 'naseth', 'drepusdt', 'gvteth', 'wrxusdt', 'bchabcpax', 'ongbtc', 'usdcbnb', 'dgdeth',
                   'mtleth', 'bcnbnb', 'neblbnb', 'wanbnb', 'ontusdt', 'npxsusdt', 'mftbtc', 'eosbearbusd', 'bntbtc',
                   'modeth', 'etcusdc', 'veteth', 'bcptpax', 'atomusdc', 'duskpax', 'kavabnb', 'lunbtc', 'adxbtc',
                   'funbtc', 'knceth', 'dogebtc', 'bchsvpax', 'bcpttusd', 'osteth', 'oaxeth', 'wabibtc', 'appcbtc',
                   'nanousdt', 'wingsbtc', 'hbarusdt', 'eurusdt', 'waveseth', 'asteth', 'linkbusd', 'btttusd',
                   'bnbusds', 'linkbtc', 'venusdt', 'hotbnb', 'usdtrub', 'tctbtc', 'ankrpax', 'btctry', 'adabnb',
                   'bcceth', 'enjeth', 'bnbbusd', 'repbnb', 'bullusdt', 'vitebtc', 'btgbtc', 'renbtc', 'thetausdt',
                   'dentbtc', 'ostbtc', 'nxsbnb', 'mithbtc', 'xmrbtc', 'tomobtc', 'nulseth', 'phbbtc', 'duskbnb',
                   'ontbusd', 'btgeth', 'etcusdt', 'atomusdt', 'hcbtc', 'brdbtc', 'fttbtc', 'celrusdt', 'lskbnb',
                   'xtzbtc', 'batusdt', 'viteusdt', 'trxbtc', 'bchtusd', 'xtzusdt', 'ftmbtc', 'enjbnb', 'arkbtc',
                   'ftmusdt', 'neobusd', 'stormbnb', 'luneth', 'gntbtc', 'gtousdt', 'chzusdt', 'sntbtc', 'bandbnb',
                   'wingseth', 'mcobtc', 'docketh', 'drepbnb', 'eosusdt', 'eostusd', 'npxseth', 'thetaeth', 'iotxbtc',
                   'enjusdt', 'tfuelbnb', 'mcobnb', 'ontpax', 'dcrbnb', 'batusdc', 'snglseth', 'qlcbtc', 'qspeth',
                   'appcbnb', 'wprbtc', 'sysbtc', 'iostusdt', 'btceur', 'mtlusdt', 'ethrub', 'tfuelpax', 'maticusdt',
                   'xrpbusd', 'iotxusdt', 'tusdbtusd', 'trigbtc', 'atombtc', 'bchpax', 'eosbusd', 'zileth', 'gtotusd',
                   'xrpbullusdt', 'onetusd', 'algobtc', 'bchsvusdt', 'gtopax', 'etceth', 'vibebtc', 'bttusdt', 'repeth',
                   'iostbnb', 'usdttry', 'btsbnb', 'ankrbnb', 'dltbnb', 'snteth', 'linktusd', 'nknusdt', 'rpxbtc',
                   'cocosusdt', 'etcbusd', 'btttrx', 'bandbtc', 'steembnb', 'zecpax', 'viabnb', 'cosbnb', 'mtheth',
                   'xemeth', 'pivxbnb', 'phxbtc', 'zilusdt', 'poeeth', 'bnbeur', 'bandusdt', 'vetbnb', 'lendbtc',
                   'duskusdt', 'mfteth', 'funusdt', 'adabusd', 'perlbnb', 'btcbusd', 'ltobtc', 'nasbnb', 'algousdt',
                   'bchsvusdc', 'mcousdt', 'venbnb', 'hceth', 'fetusdt', 'edobtc', 'mftbnb', 'cosusdt', 'arpausdt',
                   'ctxcusdt', 'bqxbtc', 'npxsusdc', 'icxbnb', 'bchbnb', 'phbusdc', 'tomousdc', 'nulsbnb', 'rcnbnb',
                   'qtumbtc', 'keyusdt', 'agibtc', 'mblbtc', 'eoseth', 'tusdbtc', 'aioneth', 'storjbtc', 'lsketh',
                   'bntbusd', 'ncashbtc', 'mblbnb', 'polybnb', 'aebnb', 'ltceth', 'dogeusdc', 'wpreth', 'syseth',
                   'ognusdt', 'nanobtc', 'astbtc', 'zrxeth', 'adxeth', 'gxseth', 'ethbearbusd', 'onepax', 'scbtc',
                   'ontbnb', 'qlceth', 'btsbusd', 'rlcbtc', 'chatbtc', 'wabibnb', 'renbnb', 'xrpbullbusd', 'wavesbtc',
                   'rlcbnb', 'phxeth', 'winbtc', 'storjeth', 'wavesbusd', 'iostbtc', 'icxeth', 'adatusd', 'nknbnb',
                   'pivxbtc', 'perlusdt', 'bullbusd', 'bttusdc', 'bcptbtc', 'aebtc', 'ethusdt', 'ltousdt', 'subbtc',
                   'blzbtc', 'tfuelusdt', 'evxbtc', 'hbarbtc', 'ambeth', 'winusdt', 'qtumeth', 'dgdbtc', 'adaeth',
                   'xrpbnb', 'adapax', 'usdsbusds', 'cocosbnb', 'navbtc', 'rvnbtc', 'tnbbtc', 'bnbbtc', 'neopax',
                   'neobnb', 'cosbtc', 'powreth', 'rlcusdt', 'hbarbnb', 'wabieth', 'bqxeth', 'aionbtc', 'aeeth',
                   'wrxbtc', 'pptbtc', 'nknbtc', 'zecusdt', 'stormeth', 'qtumusdt']

        channels = ['kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'kline_1w', 'trade',
                    'miniTicker', 'depth20']

        self.__class__.ubwa.create_stream(False, False, stream_label="error")

        stream_id1 = ""
        for channel in channels:
            stream_id1 = self.__class__.ubwa.create_stream(channel, markets)

        time.sleep(6)

        restserver = BinanceWebSocketApiRestServer(self.__class__.ubwa)
        restserver.get("icinga")
        restserver.get("invalid")
        del restserver

        markets = ['xrpbearbusd', 'zeceth', 'cndbtc', 'dashbtc', 'atompax', 'perlbtc', 'ardreth', 'zecbnb',
                   'erdbnb', 'xrpbearusdt', 'stratbnb', 'cmtbtc', 'cvcbtc', 'kncbtc', 'rpxbnb', 'zenbnb', 'cndbnb',
                   'wrxbtc', 'pptbtc', 'nknbtc', 'zecusdt', 'stormeth', 'qtumusdt']

        streams = []
        for channel in channels:
            stream_id = self.__class__.ubwa.create_stream(channel, markets, stream_buffer_name=channel,
                                                          ping_interval=10, ping_timeout=10, close_timeout=5)
            streams.append(stream_id)

        time.sleep(1)
        stream_id2 = streams.pop()
        stream_id3 = streams.pop()
        stream_id4 = streams.pop()
        self.__class__.ubwa.create_stream('depth20', markets, stream_buffer_name=True)
        self.__class__.ubwa.create_stream("kline_1s", "btceth", process_stream_data=processing_of_new_data)
        self.__class__.ubwa.create_stream("kline_1s", "btceth", process_stream_data_async=processing_of_new_data_async)
        time.sleep(6)
        self.__class__.ubwa.print_summary()
        self.__class__.ubwa.print_stream_info(stream_id4)
        print(f"Stop stream as crash ...")
        self.__class__.ubwa._crash_stream(streams.pop())
        print(f"Stop stream as crash ... done")
        print(f"create_websocket_uri ...")
        self.__class__.ubwa.create_websocket_uri(False, False, stream_id1)
        print(f"create_websocket_uri ... done")
        print(f"unsubscribe_from_stream ...")
        self.__class__.ubwa.unsubscribe_from_stream(stream_id2, markets="erdbnb")
        self.__class__.ubwa.unsubscribe_from_stream(stream_id2, channels="trade")
        print(f"unsubscribe_from_stream ... done")
        self.__class__.ubwa.pop_stream_data_from_stream_buffer()
        self.__class__.ubwa.pop_stream_data_from_stream_buffer()
        self.__class__.ubwa.pop_stream_data_from_stream_buffer()
        self.__class__.ubwa.pop_stream_data_from_stream_buffer(stream_buffer_name="invalid")
        print(f"Replace stream ...")
        for i in range(1):
            self.__class__.ubwa.print_summary()
            self.__class__.ubwa.print_stream_info(stream_id4)
            time.sleep(1)
        stream_id_1_1 = self.__class__.ubwa.replace_stream(stream_id4, 'trade', 'btceth', "name")
        self.__class__.ubwa.replace_stream(stream_id_1_1, 'trade', 'btceth', "name2",
                                           new_ping_interval=10, new_ping_timeout=10, new_close_timeout=5)
        print(f"Replace stream ... Done")
        self.__class__.ubwa.get_results_from_endpoints()
        self.__class__.ubwa.get_used_weight()
        self.__class__.ubwa.get_start_time()
        self.__class__.ubwa.get_stream_label(stream_id1)
        self.__class__.ubwa.get_stream_label(False)
        self.__class__.ubwa.get_keep_max_received_last_second_entries()
        request_id = self.__class__.ubwa.get_stream_subscriptions(stream_id2)
        self.__class__.ubwa.get_result_by_request_id(request_id)
        self.__class__.ubwa.get_reconnects()
        self.__class__.ubwa.get_errors_from_endpoints()
        self.__class__.ubwa.get_monitoring_status_plain()
        self.__class__.ubwa.get_ringbuffer_error_max_size()
        self.__class__.ubwa.get_ringbuffer_result_max_size()
        self.__class__.ubwa.set_ringbuffer_error_max_size(200)
        self.__class__.ubwa.set_ringbuffer_result_max_size(300)
        self.__class__.ubwa.set_stream_label(stream_id2, "blub")
        self.__class__.ubwa._add_stream_to_stream_list(self.__class__.ubwa.get_new_uuid_id(),
                                                       'trade', 'btceth')
        self.__class__.ubwa.delete_stream_from_stream_list(stream_id1)
        self.__class__.ubwa.delete_listen_key_by_stream_id(stream_id1)
        self.__class__.ubwa.is_update_availabe_unicorn_fy()
        self.__class__.ubwa.get_version_unicorn_fy()
        self.__class__.ubwa.create_payload(stream_id2, "invalid", channels="trade")
        time.sleep(6)
        self.__class__.ubwa.get_result_by_request_id(request_id)
        self.__class__.ubwa.get_result_by_request_id()
        self.__class__.ubwa.set_keep_max_received_last_second_entries(30)
        self.__class__.ubwa._crash_stream(stream_id2)
        time.sleep(6)
        print(f"Waiting for {stream_id3} has started ...")
        self.__class__.ubwa.print_summary()
        self.__class__.ubwa.print_stream_info(stream_id3)
        self.__class__.ubwa.wait_till_stream_has_started(stream_id3)
        print(f"Waiting for {stream_id3} has started ... done!")
        print(f"Start Stop stream {stream_id2}...")
        self.__class__.ubwa.stop_stream(stream_id2)
        print(f" done!")
        self.__class__.ubwa.add_to_ringbuffer_error("test")
        self.__class__.ubwa.add_to_ringbuffer_result("test")
        self.__class__.ubwa.get_number_of_free_subscription_slots(stream_id2)
        self.__class__.ubwa.get_most_receives_per_second()
        self.__class__.ubwa.get_number_of_streams_in_stream_list()
        self.__class__.ubwa.is_update_availabe_check_command()
        print(f"Waiting for {stream_id2} has stopped")
        self.__class__.ubwa.wait_till_stream_has_stopped(stream_id2)
        print(f"Done!")
        self.__class__.ubwa.print_stream_info(stream_id2)
        self.__class__.ubwa.print_summary()
        if platform.system() != 'Windows':
            self.__class__.ubwa.print_summary_to_png(".", 12.5, add_string="test: blah", title="UBWA Demo")
        self.__class__.ubwa.get_latest_release_info()
        self.__class__.ubwa.get_latest_release_info_check_command()
        self.__class__.ubwa.set_private_dex_config("bnb1v566f3avl2ud5z0jepazsrguzkj367snlx4jm6")
        self.__class__.ubwa.get_version()
        self.__class__.ubwa.help()
        self.__class__.ubwa.get_current_receiving_speed_global()
        self.__class__.ubwa.remove_ansi_escape_codes("test text")
        self.__class__.ubwa.pop_stream_signal_from_stream_signal_buffer()

        with BinanceRestApiManager(exchange="binance.us") as ubra:
            markets = []
            data = ubra.get_all_tickers()
            for item in data:
                markets.append(item['symbol'])
        self.__class__.ubwa.create_stream("trade", markets, stream_label="too much!")
        time.sleep(1)
        self.__class__.ubwa.stop_manager()
        time.sleep(1)


if __name__ == '__main__':
    try:
        unittest.main()
    except KeyboardInterrupt:
        pass