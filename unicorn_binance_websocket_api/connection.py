#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/connection.py
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

from unicorn_binance_websocket_api.exceptions import StreamRecoveryError, Socks5ProxyConnectionError
from urllib.parse import urlparse
import asyncio
import copy
import logging
import socket
import socks  # PySocks https://pypi.org/project/PySocks/
import ssl
import sys
import time
import websockets

connect = websockets.connect
logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiConnection(object):
    def __init__(self,
                 manager,
                 stream_id,
                 socket_id,
                 channels,
                 markets,
                 symbols):
        self.manager = manager
        self.stream_id = copy.deepcopy(stream_id)
        self.socket_id = copy.deepcopy(socket_id)
        self.api_key = copy.deepcopy(self.manager.stream_list[stream_id]['api_key'])
        self.api_secret = copy.deepcopy(self.manager.stream_list[stream_id]['api_secret'])
        self.ping_interval = copy.deepcopy(self.manager.stream_list[stream_id]['ping_interval'])
        self.ping_timeout = copy.deepcopy(self.manager.stream_list[stream_id]['ping_timeout'])
        self.close_timeout = copy.deepcopy(self.manager.stream_list[stream_id]['close_timeout'])
        self.channels = copy.deepcopy(channels)
        self.markets = copy.deepcopy(markets)
        self.symbols = copy.deepcopy(symbols)
        self.api = copy.deepcopy(self.manager.stream_list[stream_id]['api'])
        self.add_timeout = True if "!userData" in str(str(channels) + str(markets)) or self.api is True else False
        if self.add_timeout:
            logger.debug(f"BinanceWebSocketApiConnection.receive({str(self.stream_id)}) socket_id="
                         f"{str(self.socket_id)}) - Adding timeout to `websocket.recv()` ")

    async def __aenter__(self):
        if self.manager.is_stop_request(self.stream_id):
            self.manager.stream_is_stopping(self.stream_id)
            sys.exit(0)
        uri = self.manager.create_websocket_uri(self.channels,
                                                self.markets,
                                                self.stream_id,
                                                self.api_key,
                                                self.api_secret,
                                                symbols=self.symbols,
                                                api=self.manager.stream_list[self.stream_id]['api'])
        if uri is False:
            # cant get a valid URI, so this stream has to crash
            error_msg = "Probably no internet connection?"
            logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                            str(self.channels) + ", " + str(self.markets) + ") - " + " error: 5 - " + str(error_msg))
            self.manager.stream_is_crashing(self.stream_id, str(error_msg))
            self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        else:
            self.manager.stream_list[self.stream_id]['websocket_uri'] = uri
        try:
            if isinstance(uri, dict):
                # dict = error, string = valid url
                if uri['code'] == -1102 or \
                        uri['code'] == -2008 or \
                        uri['code'] == -2014 or \
                        uri['code'] == -2015 or \
                        uri['code'] == -11001:
                    # -1102 = Mandatory parameter 'symbol' was not sent, was empty/null, or malformed.
                    # -2008 = Invalid Api-Key ID
                    # -2014 = API-key format invalid
                    # -2015 = Invalid API-key, IP, or permissions for action
                    # -11001 = Isolated margin account does not exist.
                    # Can not get a valid listen_key, so this stream has to crash:
                    logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                                    ", " + str(self.channels) + ", " + str(self.markets) + ") - error: 4 - " +
                                    str(uri['msg']))
                    try:
                        del self.manager.restart_requests[self.stream_id]
                    except KeyError as error_msg:
                        logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                                        ", " + str(self.channels) + ", " + str(self.markets) + ") - error: 6 - "
                                        + str(error_msg))
                    except TypeError as error_msg:
                        logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                                        ", " + str(self.channels) + ", " + str(self.markets) + ") - error: 3 - "
                                        + str(error_msg))
                else:
                    logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                                    ", " + str(self.channels) + ", " + str(self.markets) + ") -  Received unknown"
                                    " error msg from Binance: " + str(uri['msg']))
                self.manager.stream_is_crashing(self.stream_id, str(uri['msg']))
                if self.manager.throw_exception_if_unrepairable:
                    raise StreamRecoveryError("stream_id " + str(self.stream_id) + ": " + str(uri))
                sys.exit(1)
        except KeyError as error_msg:
            logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                            ", " + str(self.channels) + ", " + str(self.markets) + ") - error: 1 - "
                            + str(error_msg))
        if self.manager.socks5_proxy_address is None or self.manager.socks5_proxy_port is None:
            self._conn = connect(uri,
                                 ping_interval=self.ping_interval,
                                 ping_timeout=self.ping_timeout,
                                 close_timeout=self.close_timeout,
                                 extra_headers={'User-Agent': str(self.manager.get_user_agent())})
            logger.info(f"BinanceWebSocketApiConnection.await._conn.__aenter__(\"{self.stream_id}, {self.channels}"
                        f", {self.markets}\") - No proxy used!")
        else:
            websocket_socks5_proxy = socks.socksocket()
            websocket_socks5_proxy.set_proxy(proxy_type=socks.SOCKS5,
                                             addr=self.manager.socks5_proxy_address,
                                             port=int(self.manager.socks5_proxy_port),
                                             username=self.manager.socks5_proxy_user,
                                             password=self.manager.socks5_proxy_pass)
            netloc = urlparse(self.manager.websocket_base_uri).netloc
            try:
                host, port = netloc.split(":")
            except ValueError as error_msg:
                logger.debug(f"'netloc' split error: {netloc} - {error_msg}")
                host = netloc
                port = 443
            try:
                logger.info(f"Connect to socks5 proxy {host}:{port} (ssl_verification: "
                            f"{self.manager.socks5_proxy_ssl_verification})")
                websocket_socks5_proxy.connect((host, int(port)))
                websocket_server_hostname = netloc
            except socks.ProxyConnectionError as error_msg:
                error_msg = f"{error_msg} ({host}:{port})"
                logger.critical(error_msg)
                raise Socks5ProxyConnectionError(error_msg)
            except socks.GeneralProxyError as error_msg:
                error_msg = f"{error_msg} ({host}:{port})"
                logger.critical(error_msg)
                raise Socks5ProxyConnectionError(error_msg)

            self._conn = connect(uri,
                                 ssl=self.manager.websocket_ssl_context,
                                 sock=websocket_socks5_proxy,
                                 server_hostname=websocket_server_hostname,
                                 ping_interval=self.ping_interval,
                                 ping_timeout=self.ping_timeout,
                                 close_timeout=self.close_timeout,
                                 extra_headers={'User-Agent': str(self.manager.get_user_agent())})
            logger.info(f"BinanceWebSocketApiConnection.await._conn.__aenter__(\"{self.stream_id}, {self.channels}"
                        f", {self.markets}\") - Using proxy: {self.manager.socks5_proxy_address} "
                        f"{self.manager.socks5_proxy_port} SSL: {self.manager.socks5_proxy_ssl_verification}")
        try:
            try:
                self.manager.websocket_list[self.stream_id] = await self._conn.__aenter__()
            except websockets.exceptions.InvalidMessage as error_msg:
                logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                             ", " + str(self.channels) + ", " + str(self.markets) + ") - InvalidMessage error_msg:  " +
                             str(error_msg))
                self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                time.sleep(2)
                self.manager.set_restart_request(self.stream_id)
                sys.exit(1)
            except websockets.exceptions.InvalidStatusCode as error_msg:
                if "HTTP 429" in str(error_msg):
                    logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                                 ", " + str(self.channels) + ", " + str(self.markets) + ") InvalidStatusCode-HTTP429" +
                                 str(error_msg))
                    self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                    time.sleep(2)
                    self.manager.set_restart_request(self.stream_id)
                    sys.exit(1)
                else:
                    logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) +
                                 ", " + str(self.channels) + ", " + str(self.markets) + ") - InvalidStatusCode" +
                                 " error_msg: " + str(error_msg))
            self.manager.stream_list[self.stream_id]['status'] = "running"
            self.manager.stream_list[self.stream_id]['has_stopped'] = False
            try:
                if self.manager.restart_requests[self.stream_id]['status'] == "restarted":
                    self.manager.increase_reconnect_counter(self.stream_id)
                    del self.manager.restart_requests[self.stream_id]
            except KeyError:
                pass
            self.manager.set_heartbeat(self.stream_id)
            self.manager.process_stream_signals("CONNECT", self.stream_id)
            self.manager.stream_list[self.stream_id]['last_stream_signal'] = "CONNECT"
        except websockets.exceptions.NegotiationError as error_msg:
            logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ")" + " - NegotiationError - " +
                         "error_msg: " + str(error_msg))
        except ConnectionResetError as error_msg:
            logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ")" + " - ConnectionResetError - " +
                         "error_msg: " + str(error_msg))
        except socket.gaierror as error_msg:
            logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                            str(self.channels) + ", " + str(self.markets) + ")" + " - No internet connection? "
                            "- error_msg: " + str(error_msg) + ": " + self.manager.websocket_base_uri)
            self.manager.stream_is_crashing(self.stream_id, " - No internet connection? "
                                            "- error_msg: " + str(error_msg) + ": " + self.manager.websocket_base_uri)
            self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except OSError as error_msg:
            logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                            str(self.channels) + ", " + str(self.markets) + ")" + " - OSError - error_msg: " +
                            str(error_msg))
            self.manager.stream_is_crashing(self.stream_id, (str(error_msg)))
            self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except websockets.exceptions.InvalidStatusCode as error_msg:
            if "Status code not 101: 414" in str(error_msg):
                # Since we subscribe via websocket.send() and not with URI anymore, this is obsolete code I guess.
                self.manager.stream_is_crashing(self.stream_id, str(error_msg) + " --> URI too long?")
                logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                str(self.channels) + ", " + str(self.markets) + ")" + " - URI Too Long? - error_msg: "
                                + str(error_msg))
                try:
                    self.manager.websocket_list[self.stream_id].close()
                except KeyError:
                    pass
                sys.exit(1)
            elif "Status code not 101: 400" in str(error_msg):
                logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                str(self.channels) + ", " + str(self.markets) + ") - error_msg: " + str(error_msg))
            elif "Status code not 101: 429" in str(error_msg):
                logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") - error_msg: " + str(error_msg))
                self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                time.sleep(2)
                self.manager.set_restart_request(self.stream_id)
                sys.exit(1)
            elif "Status code not 101: 500" in str(error_msg):
                logger.critical("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                                str(self.channels) + ", " + str(self.markets) + ") - error_msg: " + str(error_msg))
                self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                sys.exit(1)
            else:
                logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                             str(self.channels) + ", " + str(self.markets) + ") - error_msg: " + str(error_msg))
                try:
                    self.manager.websocket_list[self.stream_id].close()
                except KeyError:
                    pass
                self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                self.manager.set_restart_request(self.stream_id)
                sys.exit(1)
        except websockets.exceptions.ConnectionClosed as error_msg:
            logger.error("BinanceWebSocketApiConnection.await._conn.__aenter__(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ") - Exception ConnectionClosed"
                         " - error_msg:  " + str(error_msg))
            if "WebSocket connection is closed: code = 1006" in str(error_msg):
                self.manager.websocket_list[self.stream_id].close()
                self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                sys.exit(1)
            else:
                logger.critical(f"BinanceWebSocketApiConnection.await._conn.__aenter__({self.stream_id}, "
                                f"{self.channels}, {self.markets}) - UnhandledException ConnectionClosed - {error_msg}")
        return self

    async def __aexit__(self, *args, **kwargs):
        try:
            await self._conn.__aexit__(*args, **kwargs)
        except RuntimeError as error_msg:
            logger.debug(f"BinanceWebSocketApiConnection.__aexit__({self.stream_id}) - RuntimeError - {error_msg}")
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False and \
                    self.manager.is_stop_as_crash_request is False:
                self.manager.set_restart_request(self.stream_id)
        except AttributeError as error_msg:
            logger.error(f"BinanceWebSocketApiConnection.__aexit__({self.stream_id}) - AttributeError - {error_msg}")
        except websockets.exceptions.ConnectionClosed as error_msg:
            logger.error(f"BinanceWebSocketApiConnection.__aexit__({self.stream_id}) - ConnectionClosed - {error_msg}")
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False and \
                    self.manager.is_stop_as_crash_request is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)

    async def close(self):
        if self.manager.is_stop_as_crash_request(self.stream_id) is False:
            self.manager.stream_is_stopping(self.stream_id)
        logger.info(f"BinanceWebSocketApiConnection.close({str(self.stream_id)})")
        try:
            await self.manager.websocket_list[self.stream_id].close()
        except KeyError:
            logger.error(f"BinanceWebSocketApiConnection.close({str(self.stream_id)}) - Stream not found!")
        except RuntimeError as error_msg:
            logger.error(f"BinanceWebSocketApiConnection.close({str(self.stream_id)}) - RuntimeError: {str(error_msg)}")
        except ValueError as error_msg:
            # ValueError: The future belongs to a different loop than the one specified as the loop argument
            logger.error(f"BinanceWebSocketApiConnection.close({str(self.stream_id)}) socket_id="
                         f"{str(self.socket_id)}) - Closing this socket! - ValueError: {str(error_msg)}")
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)

    async def receive(self):
        self.manager.set_heartbeat(self.stream_id)
        if self.manager.is_stop_request(self.stream_id):
            return False
        try:
            if self.add_timeout:
                if self.api is True:
                    timeout = 0.1
                else:
                    timeout = 1
                received_data_json = await asyncio.wait_for(self.manager.websocket_list[self.stream_id].recv(),
                                                            timeout=timeout)
            else:
                received_data_json = await self.manager.websocket_list[self.stream_id].recv()
            if self.manager.is_stop_request(self.stream_id):
                return False
            try:
                if self.manager.restart_requests[self.stream_id]['status'] == "restarted":
                    self.manager.increase_reconnect_counter(self.stream_id)
                    del self.manager.restart_requests[self.stream_id]
            except KeyError:
                pass
            if received_data_json is not None:
                size = sys.getsizeof(str(received_data_json))
                self.manager.increase_processed_receives_statistic(self.stream_id)
                self.manager.add_total_received_bytes(size)
                self.manager.increase_received_bytes_per_second(self.stream_id, size)
            return received_data_json
        except RuntimeError as error_msg:
            logger.error("BinanceWebSocketApiConnection.receive(" +
                         str(self.stream_id) + ") - RuntimeError - error_msg: " + str(error_msg))
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except ssl.SSLError as error_msg:
            logger.error("BinanceWebSocketApiConnection.receive(" +
                         str(self.stream_id) + ") - ssl.SSLError - error_msg: " + str(error_msg))
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except KeyError as error_msg:
            logger.error("BinanceWebSocketApiConnection.receive(" +
                         str(self.stream_id) + ") - KeyError - error_msg: " + str(error_msg))
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except ValueError as error_msg:
            # ValueError: The future belongs to a different loop than the one specified as the loop argument
            logger.error(f"BinanceWebSocketApiConnection.receive({str(self.stream_id)}) socket_id="
                         f"{str(self.socket_id)}) - Closing this socket! - ValueError: {str(error_msg)}")
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)

    async def send(self, data):
        self.manager.set_heartbeat(self.stream_id)
        try:
            await self.manager.websocket_list[self.stream_id].send(data)
            self.manager.increase_transmitted_counter(self.stream_id)
        except websockets.exceptions.ConnectionClosed as error_msg:
            logger.error("BinanceWebSocketApiConnection.send(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ") - Exception ConnectionClosed "
                         "- error_msg:  " + str(error_msg))
            self.manager.stream_is_crashing(self.stream_id, str(error_msg))
            self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except RuntimeError as error_msg:
            logger.error("BinanceWebSocketApiConnection.send(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ") - Exception RuntimeError "
                         "- error_msg:  " + str(error_msg))
            self.manager.stream_is_crashing(self.stream_id, str(error_msg))
            self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
        except IndexError as error_msg:
            logger.error("BinanceWebSocketApiConnection.send(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ") - Exception IndexError "
                         "- error_msg:  " + str(error_msg))
        except KeyError as error_msg:
            logger.error("BinanceWebSocketApiConnection.send(" + str(self.stream_id) + ", " +
                         str(self.channels) + ", " + str(self.markets) + ") - Exception KeyError "
                         "- error_msg:  " + str(error_msg))
        except ValueError as error_msg:
            # ValueError: The future belongs to a different loop than the one specified as the loop argument
            logger.error(f"BinanceWebSocketApiConnection.send({str(self.stream_id)}) socket_id="
                         f"{str(self.socket_id)}) - Closing this socket! - ValueError: {str(error_msg)}")
            self.manager.stream_is_stopping(self.stream_id)
            if self.manager.is_stop_request(self.stream_id) is False:
                self.manager.set_restart_request(self.stream_id)
            sys.exit(1)
