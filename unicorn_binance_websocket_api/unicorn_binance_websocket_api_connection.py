#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api_connection.py
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

from websockets import connect
import copy
import logging
import socket
import ssl
import sys
import time
import websockets


class BinanceWebSocketApiConnection(object):
    def __init__(self, handler_binance_websocket_api_manager, stream_id, channels, markets):
        self.handler_binance_websocket_api_manager = handler_binance_websocket_api_manager
        self.api_key = copy.deepcopy(self.handler_binance_websocket_api_manager.api_key)
        self.api_secret = copy.deepcopy(self.handler_binance_websocket_api_manager.api_secret)
        self.channels = copy.deepcopy(channels)
        self.markets = copy.deepcopy(markets)
        self.stream_id = copy.deepcopy(stream_id)

    async def __aenter__(self):
        # inherited start method
        if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id):
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            sys.exit(0)
        uri = self.handler_binance_websocket_api_manager.create_websocket_uri(self.channels, self.markets,
                                                                              self.stream_id, self.api_key,
                                                                              self.api_secret)
        if uri is False:
            # cant get a valid URI, so this stream has to crash
            error_msg = "Probably no internet connection?"
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") - " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
            time.sleep(0.5)
            self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        try:
            if uri['code'] == -2014 or uri['code'] == -2015:
                # cant get a valid listen_key, so this stream has to crash
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") - " + str(uri['msg']))
                try:
                    del self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]
                except KeyError:
                    pass
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(uri['msg']))
                sys.exit(1)
        except KeyError:
            pass
        except TypeError:
            pass
        logging.debug("BinanceWebSocketApiConnection->__enter__(" + str(self.stream_id) + ", " + str(self.channels) +
                      ", " + str(self.markets) + ")" + " connecting to " + str(uri))
        self._conn = connect(uri, ping_interval=10, ping_timeout=10, close_timeout=5,
                             extra_headers={'User-Agent': 'unicorn-data-analysis/unicorn-binance-websocket-api/' +
                                            self.handler_binance_websocket_api_manager.version})
        try:
            self.handler_binance_websocket_api_manager.websocket_list[self.stream_id] = await self._conn.__aenter__()
            self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['status'] = "running"
            self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['has_stopped'] = False
            try:
                if self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]['status'] == "restarted":
                    self.handler_binance_websocket_api_manager.increase_reconnect_counter(self.stream_id)
                    del self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]
            except KeyError:
                pass
        except ConnectionResetError as error_msg:
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ")" + " - ConnectionResetError "
                             ";) - " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, (str(error_msg) +
                                                                          " - ConnectionResetError"))
            time.sleep(0.5)
            self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except OSError as error_msg:
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ")" + " - OSError "
                             ";) - " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, (str(error_msg) +
                                                                          " - OSError"))
            time.sleep(0.5)
            self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except socket.gaierror as error_msg:
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ")" + " - No internet connection? "
                             ";) - " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, (str(error_msg) +
                                                                          " - No internet connection?"))
            time.sleep(0.5)
            self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except websockets.exceptions.InvalidStatusCode as error_msg:
            if "Status code not 101: 414" in str(error_msg):
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg) +
                                                                              " --> URI too long? ;)")
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ")" + " - URI Too Long? To many "
                                 "streams in on socket? ;) - " + str(error_msg))
                try:
                    self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
                except KeyError:
                    pass
                sys.exit(1)
            elif "Status code not 101: 400" in str(error_msg):
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                # Test!!! This block is deactivated and `async def __aexit__(self, *args, **kwargs):` is now doing the job...
                #self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str (error_msg))
                #time.sleep(5)
                #self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                #sys.exit(1)
            elif "Status code not 101: 500" in str(error_msg):
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                sys.exit(1)
            else:
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                sys.exit(1)
        except websockets.exceptions.ConnectionClosed as error_msg:
            logging.info("BinanceWebSocketApiSocket->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ") Exception ConnectionClosed "
                                                                         "Info: " + str(error_msg))
            if "WebSocket connection is closed: code = 1006" in str(error_msg):
                self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
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
            try:
                self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
            except KeyError:
                pass
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(0)

    def close(self):
        # used to close the stream
        self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
        logging.debug("binance_websocket_api_connection->close(" + str(self.stream_id) + ")")
        self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
        sys.exit(0)

    async def receive(self):
        # method to catch the data from the stream
        try:
            received_data = await self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].recv()
        except ssl.SSLError as error_msg:
            logging.debug("binance_websocket_api_connection->close(" + str(self.stream_id) + ") - error_msg:" +
                          str(error_msg))
        try:
            if self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]['status'] == "restarted":
                self.handler_binance_websocket_api_manager.increase_reconnect_counter(self.stream_id)
                del self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]
        except KeyError:
            pass
        self.handler_binance_websocket_api_manager.increase_processed_receives_statistic(self.stream_id)
        self.handler_binance_websocket_api_manager.set_heartbeat(self.stream_id)
        return received_data
