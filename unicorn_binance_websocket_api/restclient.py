#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/restclient.py
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

from unicorn_binance_rest_api import BinanceRestApiManager
import logging
import threading
import time
from typing import Optional, Union

logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiRestclient(object):
    def __init__(self, manager):
        """
        Create a restclient instance!

        :param manager: provide `self` of `BinanceWebsocketApiManager()`
        :type manager: object
        """
        self.manager = manager
        self.api_key = False
        self.api_secret = False
        self.symbol = False
        self.listen_key = False
        self.last_static_ping_listen_key: Optional[Union[bool, int]] = False
        self.listen_key_output = False
        self.threading_lock = threading.Lock()
        self.restful_base_uri = self.manager.restful_base_uri

    def _init_vars(self,
                   stream_id,
                   api_key=False,
                   api_secret=False,
                   symbol=False,
                   listen_key=False,
                   last_static_ping_listen_key: Optional[Union[bool, int]] = False):
        """
        set default values and load values from stream_list

        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param symbol: provide the symbol for isolated_margin user_data listen_key
        :type symbol: str
        :param listen_key: provide the listen_key
        :type listen_key: str
        :param listen_key: the `last_static_ping_listen_key` variable of the `listen_key` you want to keepalive
        :type listen_key: int
        :return: bool
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.listen_key = listen_key
        self.symbol = symbol
        self.last_static_ping_listen_key = last_static_ping_listen_key
        self.listen_key_output = self.manager.replacement_text
        try:
            if self.api_key is False:
                self.api_key = self.manager.stream_list[stream_id]['api_key']
            if self.api_secret is False:
                self.api_secret = self.manager.stream_list[stream_id]['api_secret']
            if self.symbol is False:
                self.symbol = self.manager.stream_list[stream_id]['symbols']
            if self.listen_key is False:
                self.listen_key = self.manager.stream_list[stream_id]['listen_key']
            if self.last_static_ping_listen_key is False:
                self.last_static_ping_listen_key = self.manager.stream_list[stream_id]['last_static_ping_listen_key']
            if self.manager.show_secrets_in_logs is True:
                self.listen_key_output = self.listen_key
        except KeyError as error_msg:
            logger.error(f"BinanceWebSocketApiRestclient.init_vars() - TypeError - error_msg: {str(error_msg)}")
            return False
        return True

    def get_listen_key(self,
                       stream_id=False,
                       api_key=False,
                       api_secret=False,
                       last_static_ping_listen_key=False,
                       symbol=False):
        """
        Request a valid listen_key from binance

        :param stream_id: provide a stream_id
        :type stream_id: str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param last_static_ping_listen_key: the `last_static_ping_listen_key` variable of the `listen_key` you want to keepalive
        :type last_static_ping_listen_key: int
        :param symbol: provide the symbol for isolated_margin user_data listen_key
        :type symbol: str
        :return: listen_key
        :rtype: str or False
        """
        logger.info(f"BinanceWebSocketApiRestclient.get_listen_key() symbol='{str(self.symbol)}' "
                    f"stream_id='{str(stream_id)}')")
        if stream_id is False:
            return False
        with self.threading_lock:
            self._init_vars(stream_id,
                            api_key=api_key,
                            api_secret=api_secret,
                            symbol=symbol,
                            last_static_ping_listen_key=last_static_ping_listen_key)
            ubra = BinanceRestApiManager(api_key=self.api_key, api_secret=self.api_secret,
                                         exchange=self.manager.exchange,
                                         socks5_proxy_server=self.manager.socks5_proxy_server,
                                         socks5_proxy_user=self.manager.socks5_proxy_user,
                                         socks5_proxy_pass=self.manager.socks5_proxy_pass,
                                         warn_on_update=self.manager.warn_on_update)
            if self.manager.exchange == "binance.com-margin" or \
                    self.manager.exchange == "binance.com-margin-testnet":
                try:
                    if self.manager.restful_base_uri is not None:
                        ubra.MARGIN_API_URL = self.manager.restful_base_uri
                    response = ubra.margin_stream_get_listen_key(output="raw_data", throw_exception=False)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for margin!")
                    return False
            elif self.manager.exchange == "binance.com-isolated_margin" or \
                    self.manager.exchange == "binance.com-isolated_margin-testnet":
                if self.symbol is False:
                    logger.critical("BinanceWebSocketApiRestclient.get_listen_key() - error_msg: Parameter "
                                    "`symbol` is missing!")
                    return False
                else:
                    try:
                        if self.manager.restful_base_uri is not None:
                            ubra.MARGIN_API_URL = self.manager.restful_base_uri
                        response = ubra.isolated_margin_stream_get_listen_key(symbol=str(self.symbol), output="raw_data",
                                                                              throw_exception=False)
                    except AttributeError as error_msg:
                        logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                        f"error_msg: {error_msg} - Can not acquire listen_key for isolated_margin!")
                        return False
            elif self.manager.exchange == "binance.com-futures":
                try:
                    if self.manager.restful_base_uri is not None:
                        ubra.FUTURES_URL = self.manager.restful_base_uri
                    response = ubra.futures_stream_get_listen_key(output="raw_data", throw_exception=False)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for futures!!")
                    return False
            elif self.manager.exchange == "binance.com-coin_futures":
                try:
                    if self.manager.restful_base_uri is not None:
                        ubra.FUTURES_COIN_URL = self.manager.restful_base_uri
                    response = ubra.futures_coin_stream_get_listen_key(output="raw_data", throw_exception=False)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for coin futures!!")
                    return False
            else:
                try:
                    if self.manager.restful_base_uri is not None:
                        ubra.API_URL = self.manager.restful_base_uri
                    response = ubra.stream_get_listen_key(output="raw_data", throw_exception=False)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for exchange='"
                                    f"{self.manager.exchange}'!")
                    return False
            # used weight:
            self.manager.binance_api_status = ubra.get_used_weight()
            weight = self.manager.binance_api_status['weight']
            self.manager.binance_api_status['weight'] = 0 if weight is None else weight
            self.manager.binance_api_status['timestamp'] = time.time()
            try:
                self.listen_key = response['listenKey']
                self.last_static_ping_listen_key = time.time()
                return response
            except KeyError:
                return response
            except TypeError:
                return False

    def delete_listen_key(self,
                          stream_id=False,
                          api_key=False,
                          api_secret=False,
                          listen_key=False):
        """
        Delete a specific listen key

        :param stream_id: provide a stream_id
        :type stream_id: str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param listen_key: the listenkey you want to delete
        :type listen_key: str or bool
        :return: the response
        :rtype: str or False
        """
        logger.info(f"BinanceWebSocketApiRestclient.delete_listen_key() stream_id='{str(stream_id)}')")
        if stream_id is False:
            return False
        with self.threading_lock:
            self._init_vars(stream_id, api_key, api_secret, listen_key)
            ubra = BinanceRestApiManager(api_key=self.api_key, api_secret=self.api_secret,
                                         exchange=self.manager.exchange,
                                         socks5_proxy_server=self.manager.socks5_proxy_server,
                                         socks5_proxy_user=self.manager.socks5_proxy_user,
                                         socks5_proxy_pass=self.manager.socks5_proxy_pass,
                                         warn_on_update=self.manager.warn_on_update)
            if self.manager.exchange == "binance.com-margin" or \
                    self.manager.exchange == "binance.com-margin-testnet":
                if self.manager.restful_base_uri is not None:
                    ubra.MARGIN_API_URL = self.manager.restful_base_uri
                result = ubra.margin_stream_close(listenKey=str(self.listen_key), throw_exception=False)
            elif self.manager.exchange == "binance.com-isolated_margin" or \
                    self.manager.exchange == "binance.com-isolated_margin-testnet":
                if self.manager.restful_base_uri is not None:
                    ubra.MARGIN_API_URL = self.manager.restful_base_uri
                result = ubra.isolated_margin_stream_close(symbol=str(self.symbol), listenKey=str(self.listen_key),
                                                           throw_exception=False)
                self.symbol = False
            elif self.manager.exchange == "binance.com-futures":
                if self.manager.restful_base_uri is not None:
                    ubra.FUTURES_URL = self.manager.restful_base_uri
                result = ubra.futures_stream_close(listenKey=str(self.listen_key), throw_exception=False)
            elif self.manager.exchange == "binance.com-coin_futures":
                if self.manager.restful_base_uri is not None:
                    ubra.FUTURES_COIN_URL = self.manager.restful_base_uri
                result = ubra.futures_coin_stream_close(listenKey=str(self.listen_key), throw_exception=False)
            else:
                if self.manager.restful_base_uri is not None:
                    ubra.API_URL = self.manager.restful_base_uri
                result = ubra.stream_close(listenKey=str(self.listen_key), throw_exception=False)
            self.listen_key = False
            # used weight:
            self.manager.binance_api_status = ubra.get_used_weight()
            weight = self.manager.binance_api_status['weight']
            self.manager.binance_api_status['weight'] = 0 if weight is None else weight
            self.manager.binance_api_status['timestamp'] = time.time()
            return result

    def keepalive_listen_key(self,
                             stream_id=False,
                             api_key=False,
                             api_secret=False,
                             listen_key=False,
                             last_static_ping_listen_key=False):
        """
        Ping a listenkey to keep it alive

        :param stream_id: provide a stream_id
        :type stream_id: str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param listen_key: the listenkey you want to keepalive
        :type listen_key: str
        :param last_static_ping_listen_key: the `last_static_ping_listen_key` variable of the `listen_key` you want to
                                                keepalive
        :type last_static_ping_listen_key: int
        :return: the response
        :rtype: str or False
        """
        logger.info(f"BinanceWebSocketApiRestclient.get_listen_key() stream_id='{str(stream_id)}')")
        if stream_id is False:
            return False
        with self.threading_lock:
            self._init_vars(stream_id, api_key, api_secret, listen_key, last_static_ping_listen_key)
            ubra = BinanceRestApiManager(api_key=self.api_key, api_secret=self.api_secret,
                                         exchange=self.manager.exchange,
                                         socks5_proxy_server=self.manager.socks5_proxy_server,
                                         socks5_proxy_user=self.manager.socks5_proxy_user,
                                         socks5_proxy_pass=self.manager.socks5_proxy_pass,
                                         warn_on_update=self.manager.warn_on_update)
            if self.manager.exchange == "binance.com-margin" or \
                    self.manager.exchange == "binance.com-margin-testnet":
                if self.manager.restful_base_uri is not None:
                    ubra.MARGIN_API_URL = self.manager.restful_base_uri
                result = ubra.margin_stream_keepalive(listenKey=str(self.listen_key), throw_exception=False)
            elif self.manager.exchange == "binance.com-isolated_margin" or \
                    self.manager.exchange == "binance.com-isolated_margin-testnet":
                if self.manager.restful_base_uri is not None:
                    ubra.MARGIN_API_URL = self.manager.restful_base_uri
                result = ubra.isolated_margin_stream_keepalive(symbol=str(self.symbol), listenKey=str(self.listen_key),
                                                               throw_exception=False)
            elif self.manager.exchange == "binance.com-futures":
                if self.manager.restful_base_uri is not None:
                    ubra.FUTURES_URL = self.manager.restful_base_uri
                result = ubra.futures_stream_keepalive(listenKey=str(self.listen_key), throw_exception=False)
            elif self.manager.exchange == "binance.com-coin_futures":
                if self.manager.restful_base_uri is not None:
                    ubra.FUTURES_URL = self.manager.restful_base_uri
                result = ubra.futures_stream_keepalive(listenKey=str(self.listen_key), throw_exception=False)
            else:
                if self.manager.restful_base_uri is not None:
                    ubra.API_URL = self.manager.restful_base_uri
                result = ubra.stream_keepalive(listenKey=str(self.listen_key), throw_exception=False)
            self.last_static_ping_listen_key = time.time()
            # used weight:
            self.manager.binance_api_status = ubra.get_used_weight()
            weight = self.manager.binance_api_status['weight']
            self.manager.binance_api_status['weight'] = 0 if weight is None else weight
            self.manager.binance_api_status['timestamp'] = time.time()
            return result
