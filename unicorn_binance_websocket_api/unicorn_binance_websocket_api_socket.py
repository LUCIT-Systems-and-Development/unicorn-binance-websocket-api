#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_socket.py
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

from __future__ import print_function
from .unicorn_binance_websocket_api_connection import BinanceWebSocketApiConnection
import logging
import websockets
import sys


class BinanceWebSocketApiSocket(object):
    def __init__(self, handler_binance_websocket_api_manager, loop, stream_id, channels, markets):
        self.handler_binance_websocket_api_manager = handler_binance_websocket_api_manager
        self.loop = loop
        self.stream_id = stream_id
        self.channels = channels
        self.markets = markets

    async def start_socket(self):
        logging.debug("BinanceWebSocketApiSocket->start_socket(" +
                      str(self.stream_id) + ", " + str(self.channels) + ", " + str(self.markets) + ")")
        async with BinanceWebSocketApiConnection(self.handler_binance_websocket_api_manager, self.stream_id,
                                                 self.channels, self.markets) as websocket:
            while True:
                if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id):
                    self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
                    websocket.close()
                    sys.exit(0)
                try:
                    received_stream_data_json = await websocket.receive()
                    if received_stream_data_json is not None:
                        self.handler_binance_websocket_api_manager.process_stream_data(received_stream_data_json)
                except websockets.exceptions.ConnectionClosed as error_msg:
                    logging.critical("BinanceWebSocketApiSocket->start_socket(" + str(self.stream_id) + ", " +
                                     str(self.channels) + ", " + str(self.markets) + ") Exception ConnectionClosed "
                                     "Info: " + str(error_msg))
                    if "WebSocket connection is closed: code = 1008" in str(error_msg):
                        websocket.close()
                        self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, error_msg)
                        self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                        sys.exit(1)
                    elif "WebSocket connection is closed: code = 1006" in str(error_msg):
                        self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, error_msg)
                        self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                        sys.exit(1)
                    else:
                        self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                        self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                        sys.exit(1)
                except AttributeError as error_msg:
                    logging.debug("BinanceWebSocketApiSocket->start_socket(" + str(self.stream_id) + ", " +
                                  str(self.channels) + ", " + str(self.markets) + ") Exception AttributeError Info: " +
                                  str(error_msg))
                    break
