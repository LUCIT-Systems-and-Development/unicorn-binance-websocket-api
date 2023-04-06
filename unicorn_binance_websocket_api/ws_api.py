#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/ws_api.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
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

import logging
import websockets

connect = websockets.connect
logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiWsApi(object):
    def __init__(self, manager=None):
        """
        Create a websocket api instance!

        :param manager: provide `self` of `BinanceWebsocketApiManager()`
        :type manager: object
        """
        self.manager = manager

    def cancel_open_orders(self, stream_id=None, symbol: str = None):
        """
        Cancel all open orders on a symbol, including OCO orders.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: str
        :return: bool
        """

        if stream_id is None:
            return False
        method = "openOrders.cancelAll"
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": str(symbol).upper(),
                  "timestamp": self.manager.get_timestamp()}
        params['signature'] = self.manager.generate_signature(
            api_secret=self.manager.stream_list[stream_id]['api_secret'],
            data=params)
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": method,
                   "params": params}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def cancel_order(self, stream_id=None, symbol: str = None, order_id: int = None, client_order_id: str = None):
        """
        Cancel an active order.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol of the order you want to cancel
        :type symbol: str
        :param order_id: Cancel by `order_id`
        :type order_id: str
        :param client_order_id: Cancel by `origClientOrderId`
        :type client_order_id: str

        :return: bool
        """
        if stream_id is None:
            return False
        method = "order.cancel"
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": str(symbol).upper(),
                  "timestamp": self.manager.get_timestamp()}
        if order_id is not None:
            params['orderId'] = order_id
        if client_order_id is not None:
            params['origClientOrderId'] = client_order_id
        params['signature'] = self.manager.generate_signature(
            api_secret=self.manager.stream_list[stream_id]['api_secret'],
            data=params)
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": method,
                   "params": params}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def create_order(self, stream_id=None, price=0.0, order_type=None,
                     quantity=0.0, side=None, symbol=None, time_in_force="GTC", test=False):
        """
        Get te Binance server time.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param price: Price eg. 10.223
        :type price: float
        :param quantity: Amount eg. 20.5
        :type quantity: float
        :param side: `BUY` or `SELL`
        :type side: str
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param time_in_force: Default `GTC`
        :type time_in_force: str
        :param order_type:`LIMIT` or `MARKET`
        :type order_type: str
        :param test: Test order placement. Validates new order parameters and verifies your signature but does not
                     send the order into the matching engine.
        :type test: new_client_order_id or False

        :return: bool
        """
        if stream_id is None:
            return False
        new_client_order_id = self.manager.get_request_id()
        method = "order.test" if test is True else "order.place"
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "newClientOrderId": new_client_order_id,
                  "price": str(price),
                  "quantity": quantity,
                  "side": side,
                  "symbol": symbol.upper(),
                  "timeInForce": time_in_force,
                  "timestamp": self.manager.get_timestamp(),
                  "type": order_type}
        params['signature'] = self.manager.generate_signature(api_secret=self.manager.stream_list[stream_id]['api_secret'],
                                                              data=params)
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": method,
                   "params": params}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return new_client_order_id

    def get_account_status(self, stream_id=None):
        """
        Get the user account status.

        :param stream_id: id of a stream to send the request
        :type stream_id: str

        :return: bool
        """
        if stream_id is None:
            return False
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "timestamp": self.manager.get_timestamp()}
        signature = self.manager.generate_signature(api_secret=self.manager.stream_list[stream_id]['api_secret'],
                                                    data=params)
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": "account.status",
                   "params": {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                              "signature": signature,
                              "timestamp": self.manager.get_timestamp()}}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def get_exchange_info(self, stream_id=None, symbols=list):
        """
        Get the Exchange Information

        :param stream_id: id of a stream to send the request
        :type stream_id: str

        :param symbols: List of selected symbols
        :type symbols: list

        :return: bool
        """
        if stream_id is None:
            return False
        symbols = [symbol.upper() for symbol in symbols]
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": "exchangeInfo",
                   "params": {"symbols": symbols}}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def get_open_orders(self, stream_id=None, symbol: str = None):
        """
        Query execution status of all open orders.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: str

        :return: bool
        """
        if stream_id is None:
            return False
        method = "openOrders.status"
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": str(symbol).upper(),
                  "timestamp": self.manager.get_timestamp()}
        params['signature'] = self.manager.generate_signature(
            api_secret=self.manager.stream_list[stream_id]['api_secret'],
            data=params)
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": method,
                   "params": params}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def get_order(self, stream_id=None, symbol: str = None, order_id: int = None):
        """
        Check execution status of an order.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param order_id: The order ID
        :type order_id: str

        :return: bool
        """
        if stream_id is None:
            return False
        method = "order.status"
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "orderId": int(order_id),
                  "timestamp": self.manager.get_timestamp()}
        params['signature'] = self.manager.generate_signature(
            api_secret=self.manager.stream_list[stream_id]['api_secret'],
            data=params)
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": method,
                   "params": params}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def get_order_book(self, stream_id=None, symbol: str = None, limit=5):
        """
        Get the order book

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The selected symbol
        :type symbol: str
        :param limit: Depth limit
        :type limit: int

        :return: bool
        """
        if stream_id is None:
            return False
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": "depth",
                   "params": {"symbol": symbol.upper(),
                              "limit": limit}}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def get_server_time(self, stream_id=None):
        """
        Get te Binance server time.

        :param stream_id: id of a stream to send the request
        :type stream_id: str

        :return: bool
        """
        if stream_id is None:
            return False
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": "time"}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True

    def ping(self, stream_id=None):
        """
        Ping the Binance Websocket API

        :param stream_id: id of a stream to send the request
        :type stream_id: str

        :return: bool
        """
        if stream_id is None:
            return False
        payload = {"id": self.manager.get_new_uuid_id(),
                   "method": "ping"}
        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)
        return True


