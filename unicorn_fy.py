#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: unicorn_fy.py
#
# Part of ‘UnicornFy’
# Project website: https://github.com/oliver-zehentleitner/unicorn_fy
# Documentation: https://oliver-zehentleitner.github.io/unicorn_fy
# PyPI: https://pypi.org/project/unicorn-fy
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019, Oliver Zehentleitner
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

import ujson as json
import logging
import time
import requests


class UnicornFy(object):
    """
    Unify received data from crypto exchanges

    Supported exchanges:
        - Binance.com
        - Binance-com-futures
        - Binance-com-margin
        - Binance.je
        - Binance.us
        - Binance.org
    """
    VERSION = "0.3.5"

    def __init__(self):
        self.last_update_check_github = {'timestamp': time.time(),
                                         'status': None}

    @staticmethod
    def is_json(data):
        """
        Is the string in json format?

        :param data: the data to verify
        :type data: str

        :return: True or False
        :rtype: bool
        """
        try:
            json.loads(data)
        except ValueError:
            return False
        except TypeError:
            return False
        return True

    @staticmethod
    def set_to_false_if_not_exist(value, key):
        """
        some vars are non existent if they would be empty, so we create the missing vars with default values

        :param value: default value
        :type value: str

        :param key: the key name
        :type key: str

        :return: final value
        :rtype: str
        """
        try:
            if value[key]:
                return value[key]
        except KeyError:
            value[key] = False
            return value
        except IndexError:
            value[key] = False
            return value

    @staticmethod
    def binance_org_websocket(stream_data_json):
        """
        unicorn_fy binance.org (incl testnet) raw_stream_data

        :param stream_data_json: The received raw stream data from the Binance websocket
        :type stream_data_json: json

        :return: dict
        """
        return stream_data_json

    @staticmethod
    def binance_com_websocket(stream_data_json):
        """
        unicorn_fy binance.com raw_stream_data

        :param stream_data_json: The received raw stream data from the Binance websocket
        :type stream_data_json: json

        :return: dict
        """
        return UnicornFy.binance_websocket(stream_data_json, exchange="binance.com", show_deprecated_warning=False)

    @staticmethod
    def binance_je_websocket(stream_data_json):
        """
        unicorn_fy binance.je (Jersey) raw_stream_data

        :param stream_data_json: The received raw stream data from the Binance websocket
        :type stream_data_json: json

        :return: dict
        """
        return UnicornFy.binance_websocket(stream_data_json, exchange="binance.je", show_deprecated_warning=False)

    @staticmethod
    def binance_us_websocket(stream_data_json):
        """
        unicorn_us binance.us (US) raw_stream_data

        :param stream_data_json: The received raw stream data from the Binance websocket
        :type stream_data_json: json

        :return: dict
        """
        return UnicornFy.binance_websocket(stream_data_json, exchange="binance.us", show_deprecated_warning=False)

    @staticmethod
    def binance_websocket(stream_data_json, exchange="binance", show_deprecated_warning=True):
        """
        unicorn_fy binance.com raw_stream_data

        :param stream_data_json: The received raw stream data from the Binance websocket
        :type stream_data_json: json

        :param exchange: Exchange endpoint.
        :type exchange: str

        :param show_deprecated_warning: Show or hide warning
        :type show_deprecated_warning: bool

        :return: dict
        """
        unicorn_fied_data = False

        logging.debug("UnicornFy->binance_websocket(" + str(stream_data_json) + ")")
        if show_deprecated_warning is True:
            logging.warning("Using `UnicornFy.binance_websocket()` is deprecated, use "
                            "`UnicornFy.binance_com_websocket()` or `UnicornFy.binance_je_websocket()` instead!")

        if UnicornFy.is_json(stream_data_json) is False:
            return stream_data_json

        stream_data = json.loads(stream_data_json)

        try:
            if stream_data[0]['e'] == "24hrMiniTicker":
                stream_data = {'data': {'e': "24hrMiniTicker"},
                               'items': stream_data}
            elif stream_data[0]['e'] == "24hrTicker":
                stream_data = {'data': {'e': "24hrTicker"},
                               'items': stream_data}
        except KeyError:
            pass

        try:
            if stream_data['data'][0]['e'] == "24hrMiniTicker":
                stream_data = {'data': {'e': "24hrMiniTicker"},
                               'items': stream_data['data']}
            elif stream_data['data'][0]['e'] == "24hrTicker":
                stream_data = {'data': {'e': "24hrTicker"},
                               'items': stream_data['data']}
        except KeyError:
            pass

        try:
            if stream_data['e'] == 'outboundAccountInfo':
                stream_data = {'data': stream_data}
            elif stream_data['e'] == 'executionReport':
                stream_data = {'data': stream_data}
        except KeyError:
            pass
        try:
            if stream_data['stream'].find('@depth5') != -1:
                stream_data['data']['e'] = "depth"
                stream_data['data']['depth_level'] = 5
            elif stream_data['stream'].find('@depth10') != -1:
                stream_data['data']['e'] = "depth"
                stream_data['data']['depth_level'] = 10
            elif stream_data['stream'].find('@depth20') != -1:
                stream_data['data']['e'] = "depth"
                stream_data['data']['depth_level'] = 20
            elif "@bookTicker" in stream_data['stream']:
                stream_data['data']['e'] = "bookTicker"
            elif "!miniTicker@arr" in stream_data['stream']:
                stream_data['data']['e'] = "bookTicker"
        except KeyError:
            pass

        try:
            # return if already unicorn_fied
            if stream_data['unicorn_fied']:
                return stream_data['unicorn_fied']
        except KeyError:
            pass

        try:
            if stream_data['data']['e'] == 'aggTrade':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'aggregate_trade_id': stream_data['data']['a'],
                                     'price': stream_data['data']['p'],
                                     'quantity': stream_data['data']['q'],
                                     'first_trade_id': stream_data['data']['f'],
                                     'last_trade_id': stream_data['data']['l'],
                                     'trade_time': stream_data['data']['T'],
                                     'is_market_maker': stream_data['data']['m'],
                                     'ignore': stream_data['data']['M']}
            elif stream_data['data']['e'] == 'trade':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'trade_id': stream_data['data']['t'],
                                     'price': stream_data['data']['p'],
                                     'quantity': stream_data['data']['q'],
                                     'buyer_order_id': stream_data['data']['b'],
                                     'seller_order_id': stream_data['data']['a'],
                                     'trade_time': stream_data['data']['T'],
                                     'is_market_maker': stream_data['data']['m'],
                                     'ignore': stream_data['data']['M']}
            elif stream_data['data']['e'] == 'bookTicker':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'order_book_update_id': stream_data['data']['u'],
                                     'symbol': stream_data['data']['s'],
                                     'best_bid_price': stream_data['data']['b'],
                                     'best_bid_quantity': stream_data['data']['B'],
                                     'best_ask_price': stream_data['data']['a'],
                                     'best_ask_quantity': stream_data['data']['A'],
                                     'event_type': stream_data['data']['e']}
            elif stream_data['data']['e'] == 'kline':
                stream_data['data'] = UnicornFy.set_to_false_if_not_exist(stream_data['data'], 'f')
                stream_data['data'] = UnicornFy.set_to_false_if_not_exist(stream_data['data'], 'L')
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'kline': {'kline_start_time': stream_data['data']['k']['t'],
                                               'kline_close_time': stream_data['data']['k']['T'],
                                               'symbol': stream_data['data']['k']['s'],
                                               'interval': stream_data['data']['k']['i'],
                                               'first_trade_id': stream_data['data']['f'],
                                               'last_trade_id': stream_data['data']['L'],
                                               'open_price': stream_data['data']['k']['o'],
                                               'close_price': stream_data['data']['k']['c'],
                                               'high_price': stream_data['data']['k']['h'],
                                               'low_price': stream_data['data']['k']['l'],
                                               'base_volume': stream_data['data']['k']['v'],
                                               'number_of_trades': stream_data['data']['k']['n'],
                                               'is_closed': stream_data['data']['k']['x'],
                                               'quote': stream_data['data']['k']['q'],
                                               'taker_by_base_asset_volume': stream_data['data']['k']['V'],
                                               'taker_by_quote_asset_volume': stream_data['data']['k']['Q'],
                                               'ignore': stream_data['data']['k']['B']}}
            elif stream_data['data']['e'] == '24hrMiniTicker':
                try:
                    if stream_data['stream']:
                        pass
                except KeyError:
                    stream_data['stream'] = '!miniTicker@arr'
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'data': []}

                try:
                    for item in stream_data['items']:
                        data = {'stream_type': stream_data['stream'],
                                'event_type': item['e'],
                                'event_time': item['E'],
                                'symbol': item['s'],
                                'close_price': item['c'],
                                'open_price': item['o'],
                                'high_price': item['h'],
                                'low_price': item['l'],
                                'taker_by_base_asset_volume': item['v'],
                                'taker_by_quote_asset_volume': item['q']}
                        unicorn_fied_data['data'].append(data)
                except KeyError:
                    data = {'stream_type': stream_data['stream'],
                            'event_type': stream_data['data']['e'],
                            'event_time': stream_data['data']['E'],
                            'symbol': stream_data['data']['s'],
                            'close_price': stream_data['data']['c'],
                            'open_price': stream_data['data']['o'],
                            'high_price': stream_data['data']['h'],
                            'low_price': stream_data['data']['l'],
                            'taker_by_base_asset_volume': stream_data['data']['v'],
                            'taker_by_quote_asset_volume': stream_data['data']['q']}
                    unicorn_fied_data['data'].append(data)
            elif stream_data['data']['e'] == '24hrTicker':
                try:
                    if stream_data['stream']:
                        pass
                except KeyError:
                    stream_data['stream'] = '!ticker@arr'
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'data': []}
                try:
                    for item in stream_data['items']:
                        data = {'stream_type': stream_data['stream'],
                                'event_type': item['e'],
                                'event_time': item['E'],
                                'symbol': item['s'],
                                'price_change': item['p'],
                                'price_change_percent': item['P'],
                                'weighted_average_price': item['w'],
                                'trade_before_24h_window': item['x'],
                                'last_price': item['c'],
                                'last_quantity': item['Q'],
                                'best_bid_price': item['b'],
                                'best_bid_quantity': item['B'],
                                'best_ask_price': item['a'],
                                'best_ask_quantity': item['A'],
                                'open_price': item['o'],
                                'high_price': item['h'],
                                'low_price': item['l'],
                                'total_traded_base_asset_volume': item['v'],
                                'total_traded_quote_asset_volume': item['q'],
                                'statistics_open_time': item['O'],
                                'statistics_close_time': item['C'],
                                'first_trade_id': item['F'],
                                'last_trade_id': item['L'],
                                'total_nr_of_trades': item['n']}
                        unicorn_fied_data['data'].append(data)
                except KeyError:
                    data = {'stream_type': stream_data['stream'],
                            'event_type': stream_data['data']['e'],
                            'event_time': stream_data['data']['E'],
                            'symbol': stream_data['data']['s'],
                            'price_change': stream_data['data']['p'],
                            'price_change_percent': stream_data['data']['P'],
                            'weighted_average_price': stream_data['data']['w'],
                            'trade_before_24h_window': stream_data['data']['x'],
                            'last_price': stream_data['data']['c'],
                            'last_quantity': stream_data['data']['Q'],
                            'best_bid_price': stream_data['data']['b'],
                            'best_bid_quantity': stream_data['data']['B'],
                            'best_ask_price': stream_data['data']['a'],
                            'best_ask_quantity': stream_data['data']['A'],
                            'open_price': stream_data['data']['o'],
                            'high_price': stream_data['data']['h'],
                            'low_price': stream_data['data']['l'],
                            'total_traded_base_asset_volume': stream_data['data']['v'],
                            'total_traded_quote_asset_volume': stream_data['data']['q'],
                            'statistics_open_time': stream_data['data']['O'],
                            'statistics_close_time': stream_data['data']['C'],
                            'first_trade_id': stream_data['data']['F'],
                            'last_trade_id': stream_data['data']['L'],
                            'total_nr_of_trades': stream_data['data']['n']}
                    unicorn_fied_data['data'].append(data)
            elif stream_data['data']['e'] == 'depth':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'symbol': stream_data['stream'][:stream_data['stream'].find('@')].upper(),
                                     'last_update_id': stream_data['data']['lastUpdateId'],
                                     'bids': stream_data['data']['bids'],
                                     'asks': stream_data['data']['asks']}
            elif stream_data['data']['e'] == 'depthUpdate':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'first_update_id_in_event': stream_data['data']['U'],
                                     'final_update_id_in_event': stream_data['data']['u'],
                                     'bids': stream_data['data']['b'],
                                     'asks': stream_data['data']['a']}
            elif stream_data['data']['e'] == 'outboundAccountInfo':
                unicorn_fied_data = {'stream_type': '!userData@arr',
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'maker_commission_rate': stream_data['data']['m'],
                                     'taker_commission_rate': stream_data['data']['t'],
                                     'buyer_commission_rate': stream_data['data']['b'],
                                     'seller_commission_rate': stream_data['data']['s'],
                                     'can_trade': stream_data['data']['T'],
                                     'can_withdraw': stream_data['data']['W'],
                                     'can_deposit': stream_data['data']['D'],
                                     'balances': []}
                for item in stream_data['data']['B']:
                    new_item = {'asset': item['a'],
                                'free': item['f'],
                                'locked': item['l']}
                    unicorn_fied_data['balances'] += [new_item]
            elif stream_data['data']['e'] == 'executionReport':
                unicorn_fied_data = {'stream_type': '!userData@arr',
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'client_order_id': stream_data['data']['c'],
                                     'side': stream_data['data']['S'],
                                     'order_type': stream_data['data']['o'],
                                     'time_in_force': stream_data['data']['f'],
                                     'order_quantity': stream_data['data']['q'],
                                     'order_price': stream_data['data']['p'],
                                     'stop_price': stream_data['data']['P'],
                                     'iceberg_quantity': stream_data['data']['F'],
                                     'ignore_g': stream_data['data']['g'],
                                     'original_client_order_id': stream_data['data']['C'],
                                     'current_execution_type': stream_data['data']['x'],
                                     'current_order_status': stream_data['data']['X'],
                                     'order_reject_reason': stream_data['data']['r'],
                                     'order_id': stream_data['data']['i'],
                                     'last_executed_quantity': stream_data['data']['l'],
                                     'cumulative_filled_quantity': stream_data['data']['z'],
                                     'last_executed_price': stream_data['data']['L'],
                                     'commission_amount': stream_data['data']['n'],
                                     'commission_asset': stream_data['data']['N'],
                                     'transaction_time': stream_data['data']['T'],
                                     'trade_id': stream_data['data']['t'],
                                     'ignore_I': stream_data['data']['I'],
                                     'is_order_working': stream_data['data']['w'],
                                     'is_trade_maker_side': stream_data['data']['m'],
                                     'ignore_M': stream_data['data']['M'],
                                     'order_creation_time': stream_data['data']['O'],
                                     'cumulative_quote_asset_transacted_quantity': stream_data['data']['Z'],
                                     'last_quote_asset_transacted_quantity': stream_data['data']['Y']}
            unicorn_fied_version = [exchange, UnicornFy.VERSION]
            unicorn_fied_data['unicorn_fied'] = unicorn_fied_version
            logging.debug("UnicornFy->binance_com_futures_websocket(" + str(unicorn_fied_data) + ")")
            return unicorn_fied_data
        except KeyError as error_msg:
            if "result" not in stream_data:
                logging.error("Detected unknown data stream format (type1) in module `unicorn_fy`: please report to "
                              "https://github.com/oliver-zehentleitner/unicorn_fy/issues " + str(stream_data) + " - " +
                              str(error_msg))
            return stream_data
        except TypeError as error_msg:
            logging.error("Detected unknown data stream format (type2) in module `unicorn_fy`: please report to "
                          "https://github.com/oliver-zehentleitner/unicorn_fy/issues " + str(stream_data) + " - " +
                          str(error_msg))
            return stream_data


    @staticmethod
    def binance_com_futures_websocket(stream_data_json, exchange="binance.com-futures", show_deprecated_warning=False):
        """
        unicorn_fy binance.com-futures raw_stream_data

        :param stream_data_json: The received raw stream data from the Binance websocket
        :type stream_data_json: json

        :param exchange: Exchange endpoint.
        :type exchange: str

        :param show_deprecated_warning: Show or hide warning
        :type show_deprecated_warning: bool

        :return: dict
        """
        unicorn_fied_data = False

        logging.debug("UnicornFy->binance_websocket(" + str(stream_data_json) + ")")
        if show_deprecated_warning is True:
            logging.warning("Using `UnicornFy.binance_websocket()` is deprecated, use "
                            "`UnicornFy.binance_com_websocket()` or `UnicornFy.binance_je_websocket()` instead!")

        if UnicornFy.is_json(stream_data_json) is False:
            return stream_data_json

        stream_data = json.loads(stream_data_json)

        try:
            if stream_data[0]['e'] == "24hrMiniTicker":
                stream_data = {'data': {'e': "24hrMiniTicker"},
                               'items': stream_data}
            elif stream_data[0]['e'] == "24hrTicker":
                stream_data = {'data': {'e': "24hrTicker"},
                               'items': stream_data}
        except KeyError:
            pass
        try:
            if stream_data['e'] == 'outboundAccountInfo':
                stream_data = {'data': stream_data}
            elif stream_data['e'] == 'executionReport':
                stream_data = {'data': stream_data}
        except KeyError:
            pass
        try:
            if stream_data['stream'].find('@depth5') != -1:
                stream_data['data']['e'] = "depth"
                stream_data['data']['depth_level'] = 5
            elif stream_data['stream'].find('@depth10') != -1:
                stream_data['data']['e'] = "depth"
                stream_data['data']['depth_level'] = 10
            elif stream_data['stream'].find('@depth20') != -1:
                stream_data['data']['e'] = "depth"
                stream_data['data']['depth_level'] = 20
            elif "@bookTicker" in stream_data['stream']:
                stream_data['data']['e'] = "bookTicker"
        except KeyError:
            pass

        try:
            # return if already unicorn_fied
            if stream_data['unicorn_fied']:
                return stream_data['unicorn_fied']
        except KeyError:
            pass

        try:
            if stream_data['data']['e'] == 'aggTrade':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'aggregate_trade_id': stream_data['data']['a'],
                                     'price': stream_data['data']['p'],
                                     'quantity': stream_data['data']['q'],
                                     'first_trade_id': stream_data['data']['f'],
                                     'last_trade_id': stream_data['data']['l'],
                                     'trade_time': stream_data['data']['T'],
                                     'is_market_maker': stream_data['data']['m']}
            elif stream_data['data']['e'] == 'trade':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'trade_id': stream_data['data']['t'],
                                     'price': stream_data['data']['p'],
                                     'quantity': stream_data['data']['q'],
                                     'buyer_order_id': stream_data['data']['b'],
                                     'seller_order_id': stream_data['data']['a'],
                                     'trade_time': stream_data['data']['T'],
                                     'is_market_maker': stream_data['data']['m'],
                                     'ignore': stream_data['data']['M']}
            elif stream_data['data']['e'] == 'kline':
                stream_data['data'] = UnicornFy.set_to_false_if_not_exist(stream_data['data'], 'f')
                stream_data['data'] = UnicornFy.set_to_false_if_not_exist(stream_data['data'], 'L')
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'kline': {'kline_start_time': stream_data['data']['k']['t'],
                                               'kline_close_time': stream_data['data']['k']['T'],
                                               'symbol': stream_data['data']['k']['s'],
                                               'interval': stream_data['data']['k']['i'],
                                               'first_trade_id': stream_data['data']['f'],
                                               'last_trade_id': stream_data['data']['L'],
                                               'open_price': stream_data['data']['k']['o'],
                                               'close_price': stream_data['data']['k']['c'],
                                               'high_price': stream_data['data']['k']['h'],
                                               'low_price': stream_data['data']['k']['l'],
                                               'base_volume': stream_data['data']['k']['v'],
                                               'number_of_trades': stream_data['data']['k']['n'],
                                               'is_closed': stream_data['data']['k']['x'],
                                               'quote': stream_data['data']['k']['q'],
                                               'taker_by_base_asset_volume': stream_data['data']['k']['V'],
                                               'taker_by_quote_asset_volume': stream_data['data']['k']['Q'],
                                               'ignore': stream_data['data']['k']['B']}}
            elif stream_data['data']['e'] == '24hrMiniTicker':
                try:
                    if stream_data['stream']:
                        pass
                except KeyError:
                    stream_data['stream'] = '!miniTicker@arr'
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'data': []}

                try:
                    for item in stream_data['items']:
                        data = {'stream_type': stream_data['stream'],
                                'event_type': item['e'],
                                'event_time': item['E'],
                                'symbol': item['s'],
                                'close_price': item['c'],
                                'open_price': item['o'],
                                'high_price': item['h'],
                                'low_price': item['l'],
                                'taker_by_base_asset_volume': item['v'],
                                'taker_by_quote_asset_volume': item['q']}
                        unicorn_fied_data['data'].append(data)
                except KeyError:
                    data = {'stream_type': stream_data['stream'],
                            'event_type': stream_data['data']['e'],
                            'event_time': stream_data['data']['E'],
                            'symbol': stream_data['data']['s'],
                            'close_price': stream_data['data']['c'],
                            'open_price': stream_data['data']['o'],
                            'high_price': stream_data['data']['h'],
                            'low_price': stream_data['data']['l'],
                            'taker_by_base_asset_volume': stream_data['data']['v'],
                            'taker_by_quote_asset_volume': stream_data['data']['q']}
                    unicorn_fied_data['data'].append(data)
            elif stream_data['data']['e'] == '24hrTicker':
                try:
                    if stream_data['stream']:
                        pass
                except KeyError:
                    stream_data['stream'] = '!ticker@arr'
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'data': []}
                try:
                    for item in stream_data['items']:
                        data = {'stream_type': stream_data['stream'],
                                'event_type': item['e'],
                                'event_time': item['E'],
                                'symbol': item['s'],
                                'price_change': item['p'],
                                'price_change_percent': item['P'],
                                'weighted_average_price': item['w'],
                                'trade_before_24h_window': item['x'],
                                'last_price': item['c'],
                                'last_quantity': item['Q'],
                                'best_bid_price': item['b'],
                                'best_bid_quantity': item['B'],
                                'best_ask_price': item['a'],
                                'best_ask_quantity': item['A'],
                                'open_price': item['o'],
                                'high_price': item['h'],
                                'low_price': item['l'],
                                'total_traded_base_asset_volume': item['v'],
                                'total_traded_quote_asset_volume': item['q'],
                                'statistics_open_time': item['O'],
                                'statistics_close_time': item['C'],
                                'first_trade_id': item['F'],
                                'last_trade_id': item['L'],
                                'total_nr_of_trades': item['n']}
                        unicorn_fied_data['data'].append(data)
                except KeyError:
                    data = {'stream_type': stream_data['stream'],
                            'event_type': stream_data['data']['e'],
                            'event_time': stream_data['data']['E'],
                            'symbol': stream_data['data']['s'],
                            'price_change': stream_data['data']['p'],
                            'price_change_percent': stream_data['data']['P'],
                            'weighted_average_price': stream_data['data']['w'],
                            'trade_before_24h_window': stream_data['data']['x'],
                            'last_price': stream_data['data']['c'],
                            'last_quantity': stream_data['data']['Q'],
                            'best_bid_price': stream_data['data']['b'],
                            'best_bid_quantity': stream_data['data']['B'],
                            'best_ask_price': stream_data['data']['a'],
                            'best_ask_quantity': stream_data['data']['A'],
                            'open_price': stream_data['data']['o'],
                            'high_price': stream_data['data']['h'],
                            'low_price': stream_data['data']['l'],
                            'total_traded_base_asset_volume': stream_data['data']['v'],
                            'total_traded_quote_asset_volume': stream_data['data']['q'],
                            'statistics_open_time': stream_data['data']['O'],
                            'statistics_close_time': stream_data['data']['C'],
                            'first_trade_id': stream_data['data']['F'],
                            'last_trade_id': stream_data['data']['L'],
                            'total_nr_of_trades': stream_data['data']['n']}
                    unicorn_fied_data['data'].append(data)
            elif stream_data['data']['e'] == 'depth':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'symbol': stream_data['stream'][:stream_data['stream'].find('@')].upper(),
                                     'last_update_id': stream_data['data']['lastUpdateId'],
                                     'bids': stream_data['data']['bids'],
                                     'asks': stream_data['data']['asks']}
            elif stream_data['data']['e'] == 'depthUpdate':
                unicorn_fied_data = {'stream_type': stream_data['stream'],
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'first_update_id_in_event': stream_data['data']['U'],
                                     'final_update_id_in_event': stream_data['data']['u'],
                                     'bids': stream_data['data']['b'],
                                     'asks': stream_data['data']['a']}
            elif stream_data['data']['e'] == 'outboundAccountInfo':
                unicorn_fied_data = {'stream_type': '!userData@arr',
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'maker_commission_rate': stream_data['data']['m'],
                                     'taker_commission_rate': stream_data['data']['t'],
                                     'buyer_commission_rate': stream_data['data']['b'],
                                     'seller_commission_rate': stream_data['data']['s'],
                                     'can_trade': stream_data['data']['T'],
                                     'can_withdraw': stream_data['data']['W'],
                                     'can_deposit': stream_data['data']['D'],
                                     'balances': []}
                for item in stream_data['data']['B']:
                    new_item = {'asset': item['a'],
                                'free': item['f'],
                                'locked': item['l']}
                    unicorn_fied_data['balances'] += [new_item]
            elif stream_data['data']['e'] == 'executionReport':
                unicorn_fied_data = {'stream_type': '!userData@arr',
                                     'event_type': stream_data['data']['e'],
                                     'event_time': stream_data['data']['E'],
                                     'symbol': stream_data['data']['s'],
                                     'client_order_id': stream_data['data']['c'],
                                     'side': stream_data['data']['S'],
                                     'order_type': stream_data['data']['o'],
                                     'time_in_force': stream_data['data']['f'],
                                     'order_quantity': stream_data['data']['q'],
                                     'order_price': stream_data['data']['p'],
                                     'stop_price': stream_data['data']['P'],
                                     'iceberg_quantity': stream_data['data']['F'],
                                     'ignore_g': stream_data['data']['g'],
                                     'original_client_order_id': stream_data['data']['C'],
                                     'current_execution_type': stream_data['data']['x'],
                                     'current_order_status': stream_data['data']['X'],
                                     'order_reject_reason': stream_data['data']['r'],
                                     'order_id': stream_data['data']['i'],
                                     'last_executed_quantity': stream_data['data']['l'],
                                     'cumulative_filled_quantity': stream_data['data']['z'],
                                     'last_executed_price': stream_data['data']['L'],
                                     'commission_amount': stream_data['data']['n'],
                                     'commission_asset': stream_data['data']['N'],
                                     'transaction_time': stream_data['data']['T'],
                                     'trade_id': stream_data['data']['t'],
                                     'ignore_I': stream_data['data']['I'],
                                     'is_order_working': stream_data['data']['w'],
                                     'is_trade_maker_side': stream_data['data']['m'],
                                     'ignore_M': stream_data['data']['M'],
                                     'order_creation_time': stream_data['data']['O'],
                                     'cumulative_quote_asset_transacted_quantity': stream_data['data']['Z'],
                                     'last_quote_asset_transacted_quantity': stream_data['data']['Y']}
            unicorn_fied_version = [exchange, UnicornFy.VERSION]
            unicorn_fied_data['unicorn_fied'] = unicorn_fied_version
            logging.debug("UnicornFy->binance_com_futures_websocket(" + str(unicorn_fied_data) + ")")
            return unicorn_fied_data
        except KeyError:
            if "result" not in stream_data:
                logging.error("Detected unknown data stream format (type1) in module `unicorn_fy`: please report to "
                              "https://github.com/oliver-zehentleitner/unicorn_fy/issues " + str(stream_data))
            return stream_data
        except TypeError:
            logging.error("Detected unknown data stream format (type2) in module `unicorn_fy`: please report to "
                          "https://github.com/oliver-zehentleitner/unicorn_fy/issues " + str(stream_data))
            return stream_data

    @staticmethod
    def get_latest_release_info():
        """
        Get infos about the latest available release

        :return: dict or False
        """
        try:
            respond = requests.get('https://api.github.com/repos/oliver-zehentleitner/unicorn_fy/releases/latest')
            return respond.json()
        except Exception:
            return False

    @staticmethod
    def get_version():
        """
        Get the package/module version

        :return: str
        """
        return UnicornFy.VERSION

    def get_latest_version(self):
        """
        Get the version of the latest available release (cache time 1 hour)

        :return: str or False
        """
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github['status'] is None or \
                (self.last_update_check_github['timestamp'] + (60 * 60) < time.time()):
            self.last_update_check_github['status'] = self.get_latest_release_info()
        if self.last_update_check_github['status']:
            try:
                return self.last_update_check_github['status']["tag_name"]
            except KeyError:
                return "unknown"
        else:
            return "unknown"

    def is_update_availabe(self):
        """
        Is a new release of this package available?

        :return: bool
        """
        installed_version = self.get_version()
        latest_version = self.get_latest_version()
        if ".dev" in installed_version:
            installed_version = installed_version[:-4]
        if latest_version == installed_version:
            return False
        elif latest_version == "unknown":
            return False
        else:
            return True

