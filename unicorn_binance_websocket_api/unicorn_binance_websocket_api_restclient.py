#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api_restclient.py
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

import hashlib
import hmac
import requests


class BinanceWebSocketApiRestclient(object):
    def __init__(self, binance_api_key, binance_api_secret, unicorn_binance_websocket_api_version):
        self.BinanceRestApi = {'base_uri': "https://api.binance.com/",
                               'key': binance_api_key,
                               'secret': binance_api_secret,
                               'request_headers': {'Accept': 'application/json',
                                                   'User-Agent': 'unicorn-data-analysis/unicorn-binance-websocket-api/' + unicorn_binance_websocket_api_version,
                                                   'X-MBX-APIKEY': str(binance_api_key)}}
        self.listen_key = False

    def _get_signature(self, data):
        hmac_signature = hmac.new(self.BinanceRestApi['secret'].encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
        return hmac_signature.hexdigest()

    def _request(self, method, path, query=False, data=False):
        if query is not False:
            uri = self.BinanceRestApi['base_uri'] + path + "?" + query
        else:
            uri = self.BinanceRestApi['base_uri'] + path
        if method == "post":
            request_handler = requests.post(uri, headers=self.BinanceRestApi['request_headers'])
        elif method == "put":
            request_handler = requests.put(uri, headers=self.BinanceRestApi['request_headers'], data=data)
        elif method == "delete":
            request_handler = requests.delete(uri, headers=self.BinanceRestApi['request_headers'])
        else:
            request_handler = False
        return request_handler.json()

    def delete_listen_key(self, listen_key):
        method = "delete"
        path = "/api/v1/userDataStream"
        try:
            return self._request(method, path, False, {'listenKey': str(listen_key)})
        except KeyError:
            return False

    def get_listen_key(self):
        method = "post"
        path = "/api/v1/userDataStream"
        response = self._request(method, path)
        try:
            self.listen_key = response['listenKey']
            return self.listen_key
        except KeyError:
            return False

    def keepalive_listen_key(self, listen_key):
        method = "put"
        path = "/api/v1/userDataStream"
        try:
            return self._request(method, path, False, {'listenKey': str(listen_key)})
        except KeyError:
            return False

