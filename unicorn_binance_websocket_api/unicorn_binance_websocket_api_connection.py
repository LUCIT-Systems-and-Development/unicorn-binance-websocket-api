#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api_connection.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api
# Documentation: https://www.unicorn-data.com/unicorn-binance-websocket-api.html
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

from .unicorn_binance_websocket_api_restclient import BinanceWebSocketApiRestclient
from websockets import connect
import copy
import logging
import socket
import sys
import websockets


class BinanceWebSocketApiConnection(object):
    def __init__(self, handler_binance_websocket_api_manager, stream_id, channels, markets):
        self.handler_binance_websocket_api_manager = handler_binance_websocket_api_manager
        self.api_key = copy.deepcopy(self.handler_binance_websocket_api_manager.api_key)
        self.api_secret = copy.deepcopy(self.handler_binance_websocket_api_manager.api_secret)
        self.BinanceWebSocketApi = {'base_uri': "wss://stream.binance.com:9443/"}
        self.channels = copy.deepcopy(channels)
        self.markets = copy.deepcopy(markets)
        self.stream_id = copy.deepcopy(stream_id)

    async def __aenter__(self):
        # inherited start method
        if type(self.channels) is str:
            self.channels = [self.channels]
        if type(self.markets) is str:
            self.markets = [self.markets]
        if len(self.channels) == 1:
            if "arr" in self.channels:
                query = "ws/"
            else:
                query = "stream?streams="
        else:
            query = "stream?streams="
        for channel in self.channels:
            if channel == "!ticker":
                logging.error("Can not create 'arr@!ticker' in a multi channel socket! "
                              "Unfortunatly Binance only stream it in a single stream socket! "
                              "Use binance_websocket_api_manager.create_stream([\"arr\"], [\"!ticker\"]) to initiate "
                              "an extra connection.")
                continue
            if channel == "!miniTicker":
                logging.error("Can not create 'arr@!miniTicker' in a multi channel socket! "
                              "Unfortunatly Binance only stream it in a single stream socket! ./"
                              "Use binance_websocket_api_manager.create_stream([\"arr\"], [\"!miniTicker\"]) to "
                              "initiate an extra connection.")
                continue
            if channel == "!userData":
                logging.error("Can not create 'outboundAccountInfo' in a multi channel socket! "
                              "Unfortunatly Binance only stream it in a single stream socket! ./"
                              "Use binance_websocket_api_manager.create_stream([\"arr\"], [\"!userData\"]) to "
                              "initiate an extra connection.")
                continue
            for market in self.markets:
                if market == "!userData":
                    binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.api_key, self.api_secret)
                    self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['listen_key'] = \
                        binance_websocket_api_restclient.get_listen_key()
                    del binance_websocket_api_restclient
                    if self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['listen_key']:
                        query += str(self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['listen_key'])
                    else:
                        error_msg = "Can not acquire a valid listen_key from binance! Did you provide a valid api_key and api_secret?"
                        logging.error(error_msg)
                        self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, error_msg)
                        sys.exit(1)
                else:
                    query += market + "@" + channel + "/"
        uri = self.BinanceWebSocketApi['base_uri'] + str(query)
        logging.debug("BinanceWebSocketApiConnection->__enter__(" + str(self.stream_id) + ", " + str(self.channels) +
                      ", " + str(self.markets) + ")" + " connecting to " + uri)
        self._conn = connect(uri, ping_interval=20, close_timeout=10)
        try:
            self.handler_binance_websocket_api_manager.websocket_list[self.stream_id] = await self._conn.__aenter__()
            self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['status'] = "running"
        except socket.gaierror as error_msg:
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ")" + " --> No internet connection??? "
                             ";) - " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, (str(error_msg) +
                                                                          " --> NO INTERNET CONNECTION??? "))
            self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except websockets.exceptions.InvalidStatusCode as error_msg:
            if "Status code not 101: 414" in str(error_msg):
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg) +
                                                                              " --> URI too long??? ;)")
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ")" + " --> URI Too Long? To many "
                                 "streams in on socket? ;) - " + str(error_msg))
                sys.exit(1)
            else:
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, error_msg)
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                sys.exit(1)
        return self

    async def __aexit__(self, *args, **kwargs):
        # inherited exit function
        try:
            await self._conn.__aexit__(*args, **kwargs)
        except AttributeError as error_msg:
            logging.critical("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
                             "ConnectionClosed - " + str(error_msg))
        except websockets.exceptions.ConnectionClosed as error_msg:
            logging.critical("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
                             "ConnectionClosed - " + str(error_msg))
        finally:
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(0)

    def close(self):
        # used to close the stream
        self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id, "binance_websocket_api_"
                                                                      "connection->__aexit__(*args, **kwargs): "
                                                                      "ConnectionClosed")
        logging.debug("binance_websocket_api_connection->close(" + str(self.stream_id) + ")")
        self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
        sys.exit(0)

    async def receive(self):
        # method to catch the data from the stream
        received_data = await self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].recv()
        try:
            if self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]['status'] == "restarted":
                self.handler_binance_websocket_api_manager.increase_reconnect_counter(self.stream_id)
                del self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]
        except KeyError:
            pass
        self.handler_binance_websocket_api_manager.increase_processed_receives_statistic(self.stream_id)
        self.handler_binance_websocket_api_manager.set_heartbeat(self.stream_id)
        return received_data

    def pong(self):
        self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].pong()
        self.handler_binance_websocket_api_manager.set_heartbeat(self.stream_id)
