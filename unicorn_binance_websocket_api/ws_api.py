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

class BinanceWebSocketApiWsApi(object):
    """
    An unofficial Python API to use the Binance Websocket API`s (com+testnet, com-margin+testnet,
    com-isolated_margin+testnet, com-futures+testnet, us, jex, dex/chain+testnet) in a easy, fast, flexible,
    robust and fully-featured way.

    This library supports two different kind of websocket endpoints:

        - CEX (Centralized exchange): binance.com, binance.vision, binance.je, binance.us, trbinance.com, jex.com

        - DEX (Decentralized exchange): binance.org

    Binance.com websocket API documentation:

        - https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md

        - https://binance-docs.github.io/apidocs/futures/en/#user-data-streams

        - https://binance-docs.github.io/apidocs/spot/en/#user-data-streams

    Binance.vision (Testnet) websocket API documentation:

        - https://testnet.binance.vision/

    Binance.us websocket API documentation:

        - https://docs.binance.us/#introduction

    TRBinance.com websocket API documentation:

        - https://www.trbinance.com/apidocs/#general-wss-information

    Jex.com websocket API documentation:

        - https://jexapi.github.io/api-doc/option.html#web-socket-streams

        - https://jexapi.github.io/api-doc/option.html#user-data-streams

    Binance.org websocket API documentation:

        - https://docs.binance.org/api-reference/dex-api/ws-connection.html

    :param process_stream_data: Provide a function/method to process the received webstream data (callback). The function
                                will be called instead of
                                `add_to_stream_buffer() <unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_buffer>`_
                                like `process_stream_data(stream_data, stream_buffer_name)` where
                                `stream_data` cointains the raw_stream_data. If not provided, the raw stream_data will
                                get stored in the stream_buffer or provided to a specific callback function of
                                `create_stream()`! `How to read from stream_buffer!
                                <https://unicorn-binance-websocket-api.docs.lucit.tech/README.html#and-4-more-lines-to-print-the-receives>`_
    :type process_stream_data: function
    :param exchange: Select binance.com, binance.com-testnet, binance.com-margin, binance.com-margin-testnet,
                     binance.com-isolated_margin, binance.com-isolated_margin-testnet, binance.com-futures,
                     binance.com-futures-testnet, binance.com-coin_futures, binance.us, trbinance.com,
                     jex.com, binance.org, binance.org-testnet (default: binance.com)
    :type exchange: str
    :param warn_on_update: set to `False` to disable the update warning of UBWA and also in UBRA used as submodule.
    :type warn_on_update: bool
    :param throw_exception_if_unrepairable: set to `True` to activate exceptions if a crashed stream is unrepairable
                                            (invalid API key, exceeded subscription limit) or an unknown exchange is
                                            used
    :type throw_exception_if_unrepairable: bool
    :param restart_timeout: A stream restart must be successful within this time, otherwise a new restart will be
                            initialized. Default is 6 seconds.
    :type restart_timeout: int
    :param show_secrets_in_logs: set to True to show secrets like listen_key, api_key or api_secret in log file
                                 (default=False)
    :type show_secrets_in_logs: bool
    :param output_default: set to "dict" to convert the received raw data to a python dict, set to "UnicornFy" to
                           convert with `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_ -  otherwise
                           with the default setting "raw_data" the output remains unchanged and gets delivered as
                           received from the endpoints. Change this for a specific stream with the `output` parameter
                           of `create_stream()` and `replace_stream()`
    :type output_default: str
    :param enable_stream_signal_buffer: set to True to enable the
                                        `stream_signal_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signal_buffer%60>`_
                                        and receive information about
                                        disconnects and reconnects to manage a restore of the lost data during the
                                        interruption or to recognize your bot got blind.
    :type enable_stream_signal_buffer: bool
    :param disable_colorama: set to True to disable the use of `colorama <https://pypi.org/project/colorama/>`_
    :type disable_colorama: bool
    :param stream_buffer_maxlen: Set a max len for the generic `stream_buffer`. This parameter can also be used within
                                 `create_stream()` for a specific `stream_buffer`.
    :type stream_buffer_maxlen: int or None
    :param process_stream_signals: Provide a function/method to process the received stream signals. The function is running inside an asyncio loop and will be
                                   called instead of
                                   `add_to_stream_signal_buffer() <unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_signal_buffer>`_
                                   like `process_stream_data(signal_type=False, stream_id=False, data_record=False)`.
    :type process_stream_signals: function
    :param close_timeout_default: The `close_timeout` parameter defines a maximum wait time in seconds for
                                completing the closing handshake and terminating the TCP connection.
                                This parameter is passed through to the `websockets.client.connect()
                                <https://websockets.readthedocs.io/en/stable/topics/design.html?highlight=close_timeout#closing-handshake>`_
    :type close_timeout_default: int
    :param ping_interval_default: Once the connection is open, a `Ping frame` is sent every
                                `ping_interval` seconds. This serves as a keepalive. It helps keeping
                                the connection open, especially in the presence of proxies with short
                                timeouts on inactive connections. Set `ping_interval` to `None` to
                                disable this behavior.
                                This parameter is passed through to the `websockets.client.connect()
                                <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websock ets>`_
    :type ping_interval_default: int
    :param ping_timeout_default: If the corresponding `Pong frame` isn't received within
                               `ping_timeout` seconds, the connection is considered unusable and is closed with
                               code 1011. This ensures that the remote endpoint remains responsive. Set
                               `ping_timeout` to `None` to disable this behavior.
                               This parameter is passed through to the `websockets.client.connect()
                               <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`_
    :type ping_timeout_default: int
    :param high_performance: Set to True makes `create_stream()` a non-blocking function
    :type high_performance:  bool
    :param debug: If True the lib adds additional information to logging outputs
    :type debug:  bool
    :param restful_base_uri: Override `restful_base_uri`. Example: `https://127.0.0.1`
    :type restful_base_uri:  str
    :param websocket_base_uri: Override `websocket_base_uri`. Example: `ws://127.0.0.1:8765/`
    :type websocket_base_uri:  str
    :param websocket_api_base_uri: Override `websocket_api_base_uri`. Example: `ws://127.0.0.1:8765/`
    :type websocket_api_base_uri:  str
    :param max_subscriptions_per_stream: Override the `max_subscriptions_per_stream` value. Example: 1024
    :type max_subscriptions_per_stream:  int
    :param exchange_type: Override the exchange type. Valid options are: 'cex', 'dex'
    :type exchange_type:  str
    :param socks5_proxy_server: Set this to activate the usage of a socks5 proxy. Example: '127.0.0.1:9050'
    :type socks5_proxy_server:  str
    :param socks5_proxy_user: Set this to activate the usage of a socks5 proxy user. Example: 'alice'
    :type socks5_proxy_user:  str
    :param socks5_proxy_pass: Set this to activate the usage of a socks5 proxy password.
    :type socks5_proxy_pass:  str
    :param socks5_proxy_ssl_verification: Set to `False` to disable SSL server verification. Default is `True`.
    :type socks5_proxy_ssl_verification:  bool
    """

    def __init__(self, manager=None):
        self.manager = manager

    def cancel_open_orders(self, stream_id=None, symbol: str = None) -> bool:
        """
        Cancel all open orders on a symbol, including OCO orders.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: int
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
        Get the Binance server time.

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
        :param order_type: `LIMIT` or `MARKET`
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


