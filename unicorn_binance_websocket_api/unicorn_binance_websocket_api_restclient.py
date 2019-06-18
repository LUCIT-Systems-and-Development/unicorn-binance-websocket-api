#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_restclient.py
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

import copy
import hashlib
import hmac
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
        elif self.exchange == "binance.je":
            self.restful_base_uri = "https://api.binance.je/"
        self.listen_key = False
        self.binance_api_status = binance_api_status

    def _get_signature(self, data):
        hmac_signature = hmac.new(self.api_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
        return hmac_signature.hexdigest()

    def _request(self, method, path, query=False, data=False):
        requests_headers = {'Accept': 'application/json',
                            'User-Agent': 'unicorn-data-analysis/unicorn-binance-websocket-api/' +
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
                             "official-api-docs/blob/master/rest-api.md#limits")
        elif request_handler.status_code == "429":
            logging.critical("BinanceWebSocketApiRestclient->_request() received status_code 429 from binance! Back off"
                             "or you are going to get banned! Read this: https://github.com/binance-exchange/binance-"
                             "official-api-docs/blob/master/rest-api.md#limits")

        respond = request_handler.json()
        self.binance_api_status['weight'] = request_handler.headers.get('X-MBX-USED-WEIGHT')
        self.binance_api_status['timestamp'] = time.time()
        self.binance_api_status['status_code'] = request_handler.status_code
        request_handler.close()
        return respond

    def delete_listen_key(self, listen_key):
        logging.debug("BinanceWebSocketApiRestclient->delete_listen_key(" + str(listen_key) + ")")
        method = "delete"
        path = "/api/v1/userDataStream"
        try:
            return self._request(method, path, False, {'listenKey': str(listen_key)})
        except KeyError:
            return False
        except TypeError:
            return False

    def get_listen_key(self):
        logging.debug("BinanceWebSocketApiRestclient->get_listen_key()")
        method = "post"
        path = "/api/v1/userDataStream"
        response = self._request(method, path)
        try:
            self.listen_key = response['listenKey']
            return response
        except KeyError:
            return response
        except TypeError:
            return False

    def keepalive_listen_key(self, listen_key):
        logging.debug("BinanceWebSocketApiRestclient->keepalive_listen_key(" + str(listen_key) + ")")
        method = "put"
        path = "/api/v1/userDataStream"
        try:
            return self._request(method, path, False, {'listenKey': str(listen_key)})
        except KeyError:
            return False
        except TypeError:
            return False
