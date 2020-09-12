#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_restclient.py
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

import copy
import hashlib
import hmac
import json
import logging
import requests
import socket
import time


class BinanceWebSocketApiRestclient(object):
    def __init__(self, exchange, binance_api_key, binance_api_secret, unicorn_binance_websocket_api_version,
                 binance_api_status):
        self.exchange = exchange
        self.api_key = copy.deepcopy(binance_api_key)
        self.api_secret = copy.deepcopy(binance_api_secret)
        self.unicorn_binance_websocket_api_version = unicorn_binance_websocket_api_version
        if self.exchange == "binance.com":
            self.restful_base_uri = "https://api.binance.com/"
            self.path_userdata = "api/v3/userDataStream"
        elif self.exchange == "binance.com-margin":
            self.restful_base_uri = "https://api.binance.com/"
            self.path_userdata = "sapi/v1/userDataStream"
        elif self.exchange == "binance.com-isolated_margin":
            self.restful_base_uri = "https://api.binance.com/"
            self.path_userdata = "sapi/v1/userDataStream/isolated"
        elif self.exchange == "binance.com-futures":
            self.restful_base_uri = "https://fapi.binance.com/"
            self.path_userdata = "fapi/v1/listenKey"
        elif self.exchange == "binance.je":
            self.restful_base_uri = "https://api.binance.je/"
            self.path_userdata = "api/v1/userDataStream"
        elif self.exchange == "binance.us":
            self.restful_base_uri = "https://api.binance.us/"
            self.path_userdata = "api/v1/userDataStream"
        elif self.exchange == "jex.com":
            self.restful_base_uri = "https://www.jex.com/"
            self.path_userdata = "api/v1/userDataStream"
        self.listen_key = False
        self.binance_api_status = binance_api_status

    def _get_signature(self, data):
        """
        Get the signature of 'data'

        :param data: the data you want to sign
        :type data: str

        :return: signature
        :rtype: str
        """
        hmac_signature = hmac.new(self.api_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
        return hmac_signature.hexdigest()

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
                            'User-Agent': 'oliver-zehentleitner/unicorn-binance-websocket-api/' +
                                          self.unicorn_binance_websocket_api_version,
                            'X-MBX-APIKEY': str(self.api_key)}
        if query is not False:
            uri = self.restful_base_uri + path + "?" + query
        else:
            uri = self.restful_base_uri + path
        try:
            if method == "post":
                request_handler = requests.post(uri, headers=requests_headers)
            elif method == "put":
                request_handler = requests.put(uri, headers=requests_headers, data=data)
            elif method == "delete":
                request_handler = requests.delete(uri, headers=requests_headers)
            else:
                request_handler = False
        except requests.exceptions.ConnectionError as error_msg:
            logging.critical("BinanceWebSocketApiRestclient->_request() - error_msg: " + str(error_msg))
            return False
        except socket.gaierror as error_msg:
            logging.critical("BinanceWebSocketApiRestclient->_request() - error_msg: " + str(error_msg))
            return False
        if request_handler.status_code == "418":
            logging.critical("BinanceWebSocketApiRestclient->_request() received status_code 418 from binance! You got"
                             "banned from the binance api! Read this: https://github.com/binance-exchange/binance-"
                             "official-api-sphinx/blob/master/rest-api.md#limits")
        elif request_handler.status_code == "429":
            logging.critical("BinanceWebSocketApiRestclient->_request() received status_code 429 from binance! Back off"
                             "or you are going to get banned! Read this: https://github.com/binance-exchange/binance-"
                             "official-api-sphinx/blob/master/rest-api.md#limits")
        try:
            respond = request_handler.json()
        except json.decoder.JSONDecodeError as error_msg:
            logging.error("BinanceWebSocketApiRestclient->_request() - error_msg: " + str(error_msg))
            return False
        self.binance_api_status['weight'] = request_handler.headers.get('X-MBX-USED-WEIGHT')
        self.binance_api_status['timestamp'] = time.time()
        self.binance_api_status['status_code'] = request_handler.status_code
        request_handler.close()
        return respond

    def delete_listen_key(self, listen_key):
        """
        Delete a specific listen key

        :param listen_key: the listenkey you want to delete
        :type listen_key: str

        :return: the response
        :rtype: str or False
        """
        logging.info("BinanceWebSocketApiRestclient->delete_listen_key(" + str(listen_key) + ")")
        method = "delete"
        try:
            return self._request(method, self.path_userdata, False, {'listenKey': str(listen_key)})
        except KeyError:
            return False
        except TypeError:
            return False

    def get_listen_key(self):
        """
        Request a valid listen_key from binance

        :return: listen_key
        :rtype: str or False
        """
        logging.info("BinanceWebSocketApiRestclient->get_listen_key()")
        method = "post"
        response = self._request(method, self.path_userdata)
        try:
            self.listen_key = response['listenKey']
            return response
        except KeyError:
            return response
        except TypeError:
            return False

    def keepalive_listen_key(self, listen_key):
        """
        Ping a listenkey to keep it alive

        :param listen_key: the listenkey you want to keepalive
        :type listen_key: str

        :return: the response
        :rtype: str or False
        """
        logging.info("BinanceWebSocketApiRestclient->keepalive_listen_key(" + str(listen_key) + ")")
        method = "put"
        try:
            return self._request(method, self.path_userdata, False, {'listenKey': str(listen_key)})
        except KeyError:
            return False
        except TypeError:
            return False
