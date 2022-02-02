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
# Copyright (c) 2019-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
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

import json
import logging
import requests
import socket
import threading
import time

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
        self.last_static_ping_listen_key = False
        self.listen_key_output = False
        self.threading_lock = threading.Lock()
        if self.manager.exchange == "binance.com":
            self.restful_base_uri = "https://api.binance.com/"
            self.path_userdata = "api/v3/userDataStream"
        elif self.manager.exchange == "binance.com-testnet":
            self.restful_base_uri = "https://testnet.binance.vision/"
            self.path_userdata = "api/v3/userDataStream"
        elif self.manager.exchange == "binance.com-margin":
            self.restful_base_uri = "https://api.binance.com/"
            self.path_userdata = "sapi/v1/userDataStream"
        elif self.manager.exchange == "binance.com-margin-testnet":
            self.restful_base_uri = "https://testnet.binance.vision/"
            self.path_userdata = "sapi/v1/userDataStream"
        elif self.manager.exchange == "binance.com-isolated_margin":
            self.restful_base_uri = "https://api.binance.com/"
            self.path_userdata = "sapi/v1/userDataStream/isolated"
        elif self.manager.exchange == "binance.com-isolated_margin-testnet":
            self.restful_base_uri = "https://testnet.binance.vision/"
            self.path_userdata = "sapi/v1/userDataStream/isolated"
        elif self.manager.exchange == "binance.com-futures":
            self.restful_base_uri = "https://fapi.binance.com/"
            self.path_userdata = "fapi/v1/listenKey"
        elif self.manager.exchange == "binance.com-futures-testnet":
            self.restful_base_uri = "https://testnet.binancefuture.com/"
            self.path_userdata = "fapi/v1/listenKey"
        elif self.manager.exchange == "binance.com-coin-futures" or self.manager.exchange == "binance.com-coin_futures":
            self.restful_base_uri = "https://dapi.binance.com/"
            self.path_userdata = "dapi/v1/listenKey"
        elif self.manager.exchange == "binance.je":
            self.restful_base_uri = "https://api.binance.je/"
            self.path_userdata = "api/v1/userDataStream"
        elif self.manager.exchange == "binance.us":
            self.restful_base_uri = "https://api.binance.us/"
            self.path_userdata = "api/v1/userDataStream"
        elif self.manager.exchange == "trbinance.com":
            self.restful_base_uri = "https://api.binance.cc/"
            self.path_userdata = "api/v1/userDataStream"
        elif self.manager.exchange == "jex.com":
            self.restful_base_uri = "https://www.jex.com/"
            self.path_userdata = "api/v1/userDataStream"

    def _do_request(self, action=False):
        """
        Do a request!

        :param action: choose "delete" or "keepalive"
        :type action: str
        :return: the response
        :rtype: str or False
        """
        if action == "keepalive":
            logger.info(f"BinanceWebSocketApiRestclient.keepalive_listen_key({str(self.listen_key_output)})")
            method = "put"
            try:
                response = self._request(method, self.path_userdata, False, {'listenKey': str(self.listen_key)})
                self.last_static_ping_listen_key = time.time()
                return response
            except KeyError:
                return False
            except TypeError:
                return False
        elif action == "delete":
            logger.info(f"BinanceWebSocketApiRestclient.delete_listen_key({str(self.listen_key_output)})")
            method = "delete"
            try:
                response = self._request(method, self.path_userdata, False, {'listenKey': str(self.listen_key)})
                self.listen_key = False
                return response
            except KeyError as error_msg:
                logger.error(f"BinanceWebSocketApiRestclient.delete_listen_key({str(self.listen_key_output)}) - "
                              f"KeyError - error_msg: {str(error_msg)}")
                return False
            except TypeError as error_msg:
                logger.error(f"BinanceWebSocketApiRestclient.delete_listen_key({str(self.listen_key_output)}) - "
                              f"KeyError - error_msg: {str(error_msg)}")
                return False
        else:
            return False

    def _init_vars(self,
                   stream_id,
                   api_key=False,
                   api_secret=False,
                   symbol=False,
                   listen_key=False,
                   last_static_ping_listen_key=False):
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

    def _request(self, method, path, query=False, data=False):
        """
        Do the request

        :param method: choose the method to use (post, put or delete)
        :type method: str
        :param path: choose the path to use
        :type path: str
        :param query: choose the query to use
        :type query: str
        :param data: the payload for the post method
        :type data: str
        :return: the response
        :rtype: str or False
        """
        requests_headers = {'Accept': 'application/json',
                            'User-Agent': str(self.manager.get_user_agent()),
                            'X-MBX-APIKEY': str(self.api_key)}
        if query is not False:
            uri = self.restful_base_uri + path + "?" + query
        else:
            uri = self.restful_base_uri + path
        try:
            if method == "post":
                if data is False:
                    request_handler = requests.post(uri, headers=requests_headers)
                else:
                    request_handler = requests.post(uri, headers=requests_headers, data=data)
            elif method == "put":
                request_handler = requests.put(uri, headers=requests_headers, data=data)
            elif method == "delete":
                request_handler = requests.delete(uri, headers=requests_headers)
            else:
                request_handler = False
        except requests.exceptions.ConnectionError as error_msg:
            logger.critical(f"BinanceWebSocketApiRestclient._request() - error: 9 -  error_msg: {str(error_msg)}")
            return False
        except socket.gaierror as error_msg:
            logger.critical(f"BinanceWebSocketApiRestclient._request() - error: 10 -  error_msg: {str(error_msg)}")
            return False
        if request_handler.status_code == "418":
            logger.critical("BinanceWebSocketApiRestclient._request() - error_msg: received status_code 418 from binance! You got"
                             "banned from the binance api! Read this: https://github.com/binance-exchange/binance-"
                             "official-api-sphinx/blob/master/rest-api.md#limits")
        elif request_handler.status_code == "429":
            logger.critical("BinanceWebSocketApiRestclient._request() - error_msg: received status_code 429 from "
                             "binance! Back off or you are going to get banned! Read this: "
                             "https://github.com/binance-exchange/binance-official-api-sphinx/blob/master/"
                             "rest-api.md#limits")
        try:
            respond = request_handler.json()
        except json.decoder.JSONDecodeError as error_msg:
            logger.error(f"BinanceWebSocketApiRestclient._request() - error_msg: {str(error_msg)}")
            return False
        self.manager.binance_api_status['weight'] = request_handler.headers.get('X-MBX-USED-WEIGHT')
        self.manager.binance_api_status['timestamp'] = time.time()
        self.manager.binance_api_status['status_code'] = request_handler.status_code
        request_handler.close()
        return respond

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
            method = "post"
            if self.manager.exchange == "binance.com-isolated_margin" or \
                    self.manager.exchange == "binance.com-isolated_margin-testnet":
                if self.symbol is False:
                    logger.critical("BinanceWebSocketApiRestclient.get_listen_key() - error_msg: Parameter "
                                     "`symbol` is missing!")
                    return False
                else:
                    response = self._request(method, self.path_userdata, False, {'symbol': str(self.symbol)})
            else:
                try:
                    response = self._request(method, self.path_userdata)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                     f"error_msg: {error_msg} - Can not acquire listen_key!")
                    return False
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
            return self._do_request("delete")

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
        :param last_static_ping_listen_key: the `last_static_ping_listen_key` variable of the `listen_key` you want to keepalive
        :type last_static_ping_listen_key: int
        :return: the response
        :rtype: str or False
        """
        logger.info(f"BinanceWebSocketApiRestclient.get_listen_key() stream_id='{str(stream_id)}')")
        if stream_id is False:
            return False
        with self.threading_lock:
            self._init_vars(stream_id, api_key, api_secret, listen_key, last_static_ping_listen_key)
            return self._do_request("keepalive")
