#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_connection.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019, Oliver Zehentleitner
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

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_exceptions import *
from websockets import connect
import asyncio
import copy
import ujson as json
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
                if self.handler_binance_websocket_api_manager.throw_exception_if_unrepairable:
                    raise StreamRecoveryError("stream_id " + str(self.stream_id) + ": " + str(uri['msg']))
                sys.exit(1)
        except KeyError:
            pass
        except TypeError:
            pass
        logging.debug("BinanceWebSocketApiConnection->__enter__(" + str(self.stream_id) + ", " + str(self.channels) +
                      ", " + str(self.markets) + ")" + " connecting to " + str(uri))
        self._conn = connect(uri, ping_interval=20, close_timeout=10,
                             extra_headers={'User-Agent': 'oliver-zehentleitner/unicorn-binance-websocket-api/' +
                                            self.handler_binance_websocket_api_manager.version})
        try:
            try:
                self.handler_binance_websocket_api_manager.websocket_list[self.stream_id] = await self._conn.__aenter__()
            except websockets.exceptions.InvalidMessage as error_msg:
                logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) +
                              ", " + str(self.channels) + ", " + str(self.markets) + ") InvalidMessage " +
                              str(error_msg))
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                time.sleep(2)
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                sys.exit(1)
            except websockets.exceptions.InvalidStatusCode as error_msg:
                if "HTTP 429" in str(error_msg):
                    logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) +
                                  ", " + str(self.channels) + ", " + str(self.markets) + ") InvalidStatusCode-HTTP429" +
                                  str(error_msg))
                    self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                    time.sleep(2)
                    self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                    sys.exit(1)
                else:
                    logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) +
                                  ", " + str(self.channels) + ", " + str(self.markets) + ") InvalidStatusCode" +
                                  str(error_msg))
            while self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['payload']:
                payload = self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['payload'].pop(0)
                await self.send(json.dumps(payload, ensure_ascii=False))
            self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['status'] = "running"
            self.handler_binance_websocket_api_manager.stream_list[self.stream_id]['has_stopped'] = False
            try:
                if self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]['status'] == "restarted":
                    self.handler_binance_websocket_api_manager.increase_reconnect_counter(self.stream_id)
                    del self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]
            except KeyError:
                pass
            self.handler_binance_websocket_api_manager.set_heartbeat(self.stream_id)
        except ConnectionResetError as error_msg:
            logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                          str(self.channels) + ", " + str(self.markets) + ")" + " - ConnectionResetError - " +
                          str(error_msg))
        except OSError as error_msg:
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ")" + " - OSError "
                             "- " + str(error_msg))
        except socket.gaierror as error_msg:
            logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ")" + " - No internet connection? "
                             "- " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, (str(error_msg) +
                                                                          " - No internet connection?"))
            self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except websockets.exceptions.InvalidStatusCode as error_msg:
            if "Status code not 101: 414" in str(error_msg):
                # Since we subscribe via websocket.send() and not with URI anymore, this is obsolete code I guess.
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg) +
                                                                              " --> URI too long?")
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ")" + " - URI Too Long? - "
                                 + str(error_msg))
                try:
                    self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
                except KeyError:
                    pass
                sys.exit(1)
            elif "Status code not 101: 400" in str(error_msg):
                logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                              str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
            elif "Status code not 101: 429" in str(error_msg):
                logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                              str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                time.sleep(2)
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
                sys.exit(1)
            elif "Status code not 101: 500" in str(error_msg):
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                self.handler_binance_websocket_api_manager.stream_is_crashing(self.stream_id, str(error_msg))
                sys.exit(1)
            else:
                logging.critical("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                 str(self.channels) + ", " + str(self.markets) + ") " + str(error_msg))
                try:
                    self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
                except KeyError:
                    pass
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
            else:
                logging.error("BinanceWebSocketApiConnection->await._conn.__aenter__(" + str(self.stream_id) +
                              ", " + str(self.channels) + ", " + str(self.markets) + ") UnhandledException "
                             "ConnectionClosed" + str(error_msg))
        return self

    async def __aexit__(self, *args, **kwargs):
        try:
            await self._conn.__aexit__(*args, **kwargs)
        except AttributeError as error_msg:
            logging.error("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
                          "AttributeError - " + str(error_msg))
            # TODO: obsolete?
            #try:
            #    self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
            #    logging.debug("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
            #                  "AttributeError - close() - done!")
            #except KeyError as error_msg:
            #    logging.debug("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
            #                  "KeyError - " + str(error_msg))
            #except RuntimeWarning as error_msg:
            #    logging.debug("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
            #                  "RuntimeWarning - " + str(error_msg))
            #except AttributeError:
            #    sys.exit(1)
        except websockets.exceptions.ConnectionClosed as error_msg:
            logging.critical("binance_websocket_api_connection->__aexit__(*args, **kwargs): "
                             "ConnectionClosed - " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False and \
                    self.handler_binance_websocket_api_manager.is_stop_as_crash_request is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)

    async def close(self):
        if self.handler_binance_websocket_api_manager.is_stop_as_crash_request(self.stream_id) is False:
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
        logging.info("binance_websocket_api_connection->close(" + str(self.stream_id) + ")")
        try:
            await self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].close()
        except KeyError:
            logging.debug("binance_websocket_api_connection->close(" +
                          str(self.stream_id) + ") - Stream not found!")

    async def receive(self):
        self.handler_binance_websocket_api_manager.set_heartbeat(self.stream_id)
        try:
            received_data_json = await self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].recv()
            try:
                if self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]['status'] == "restarted":
                    self.handler_binance_websocket_api_manager.increase_reconnect_counter(self.stream_id)
                    del self.handler_binance_websocket_api_manager.restart_requests[self.stream_id]
            except KeyError:
                pass
            if received_data_json is not None:
                size = sys.getsizeof(received_data_json)
                self.handler_binance_websocket_api_manager.increase_processed_receives_statistic(self.stream_id)
                self.handler_binance_websocket_api_manager.add_total_received_bytes(size)
                self.handler_binance_websocket_api_manager.increase_received_bytes_per_second(self.stream_id,
                                                                                              size)
            return received_data_json
        except RuntimeError as error_msg:
            logging.debug("binance_websocket_api_connection->receive(" +
                          str(self.stream_id) + ") - RuntimeError - error_msg: " + str(error_msg))
            sys.exit(1)
        except ssl.SSLError as error_msg:
            logging.debug("binance_websocket_api_connection->receive(" +
                          str(self.stream_id) + ") - ssl.SSLError - error_msg: " + str(error_msg))
        except KeyError as error_msg:
            logging.debug("binance_websocket_api_connection->receive(" +
                          str(self.stream_id) + ") - KeyError - error_msg: " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except asyncio.base_futures.InvalidStateError as error_msg:
            logging.critical("binance_websocket_api_connection->receive(" +
                             str(self.stream_id) + ") - asyncio.base_futures.InvalidStateError - error_msg: " +
                             str(error_msg) + " - Extra info: https://github.com/oliver-zehentleitner/unicorn-binance-"
                                              "websocket-api/issues/18 - open an own issue if needed!")
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)

    async def send(self, data):
        try:
            await self.handler_binance_websocket_api_manager.websocket_list[self.stream_id].send(data)
            self.handler_binance_websocket_api_manager.increase_transmitted_counter(self.stream_id)
        except websockets.exceptions.ConnectionClosed as error_msg:
            logging.critical("BinanceWebSocketApiSocket->send(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") Exception ConnectionClosed "
                             "Info: " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except RuntimeError as error_msg:
            logging.critical("BinanceWebSocketApiSocket->send(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") Exception RuntimeError "
                             "Info: " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except IndexError as error_msg:
            logging.critical("BinanceWebSocketApiSocket->send(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") Exception IndexError "
                             "Info: " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except KeyError as error_msg:
            logging.critical("BinanceWebSocketApiSocket->send(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") Exception KeyError "
                             "Info: " + str(error_msg))
            self.handler_binance_websocket_api_manager.stream_is_stopping(self.stream_id)
            if self.handler_binance_websocket_api_manager.is_stop_request(self.stream_id) is False:
                self.handler_binance_websocket_api_manager.set_restart_request(self.stream_id)
            sys.exit(1)
