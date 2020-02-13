#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_manager.py
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

from .unicorn_binance_websocket_api_socket import BinanceWebSocketApiSocket
from .unicorn_binance_websocket_api_restclient import BinanceWebSocketApiRestclient
from .unicorn_binance_websocket_api_restserver import BinanceWebSocketApiRestServer
from cheroot import wsgi
from datetime import datetime
from flask import Flask, redirect
from flask_restful import Api
import asyncio
import colorama
import copy
import logging
import platform
import re
import requests
import sys
import threading
import time
import uuid


class BinanceWebSocketApiManager(threading.Thread):
    """
    A python API to use the Binance Websocket API`s (com, com-margin, com-futures, jersey, us, dex/chain+testnet) in a easy, fast,
    flexible, robust and fully-featured way.

    This library supports two different kind of websocket endpoints:

    - CEX (Centralized exchange): binance.com, binance.je, binance.us

    - DEX (Decentralized exchange): binance.org

    Binance.com websocket API documentation:
    https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md
    https://binance-docs.github.io/apidocs/futures/en/#user-data-streams
    https://binance-docs.github.io/apidocs/spot/en/#user-data-streams

    Binance.je websocket API documentation:
    https://github.com/binance-jersey/binance-official-api-docs/blob/master/web-socket-streams.md
    https://github.com/binance-jersey/binance-official-api-docs/blob/master/user-data-stream.md

    Binance.us websocket API documentation:
    https://github.com/binance-us/binance-official-api-docs/blob/master/web-socket-streams.md
    https://github.com/binance-us/binance-official-api-docs/blob/master/user-data-stream.md

    Binance.org websocket API documentation:
    https://docs.binance.org/api-reference/dex-api/ws-connection.html

    :param process_stream_data: Provide a function/method to process the received webstream data. The function
                                will be called with one variable like `process_stream_data(data)` where
                                `data` cointains the raw_stream_data. If not provided, the raw stream_data will get
                                stored in the stream_buffer! (How to read from stream_buffer:
                                https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/README.html#and-4-more-lines-to-print-the-receives)
    :type process_stream_data: function
    :param exchange: Select binance.com, binance.com-margin, binance.com-futures, binance.je, binance.us, binance.org
                     or binance.org-testnet (default: binance.com)
    :type exchange: str

    """

    def __init__(self, process_stream_data=False, exchange="binance.com"):
        threading.Thread.__init__(self)
        self.version = "1.10.0.dev"
        logging.info("New instance of unicorn_binance_websocket_api_manager " + self.version + " started ...")
        colorama.init()
        if process_stream_data is False:
            # no special method to process stream data provided, so we use write_to_stream_buffer:
            self.process_stream_data = self.add_to_stream_buffer
        else:
            # use the provided method to process stream data:
            self.process_stream_data = process_stream_data
        self.exchange = exchange
        if self.exchange == "binance.com":
            # Binance: www.binance.com
            self.websocket_base_uri = "wss://stream.binance.com:9443/"
        elif self.exchange == "binance.com-margin":
            # Binance Margin: www.binance.com
            self.websocket_base_uri = "wss://stream.binance.com:9443/"
        elif self.exchange == "binance.com-futures":
            # Binance Futures: www.binance.com
            self.websocket_base_uri = "wss://fstream.binance.com/"
        elif self.exchange == "binance.je":
            # Binance Jersey: www.binance.je
            self.websocket_base_uri = "wss://stream.binance.je:9443/"
        elif self.exchange == "binance.us":
            # Binance US: www.binance.us
            self.websocket_base_uri = "wss://stream.binance.us:9443/"
        elif self.exchange == "binance.org":
            # Binance Chain: www.binance.org
            self.websocket_base_uri = "wss://dex.binance.org/api/"
        elif self.exchange == "binance.org-testnet":
            # Binance Chain Testnet: www.binance.org
            self.websocket_base_uri = "wss://testnet-dex.binance.org/api/"
        else:
            # Unknown Exchange
            error_msg = "Unknown exchange '" + str(self.exchange) + "'"
            logging.critical(error_msg)
            raise ValueError(error_msg)
        self.stop_manager_request = None
        self._frequent_checks_restart_request = None
        self._keepalive_streams_restart_request = None
        self.api_key = False
        self.api_secret = False
        self.binance_api_status = {'weight': None,
                                   'timestamp': 0,
                                   'status_code': None}
        self.dex_user_address = False
        self.frequent_checks_list = {}
        self.keep_max_received_last_second_entries = 5
        self.keepalive_streams_list = {}
        self.last_entry_added_to_stream_buffer = 0
        self.last_monitoring_check = time.time()
        self.last_update_check_github = {'timestamp': time.time(),
                                         'status': None}
        self.last_update_check_github_check_command = {'timestamp': time.time(),
                                                       'status': None}
        self.most_receives_per_second = 0
        self.monitoring_api_server = False
        self.monitoring_total_received_bytes = 0
        self.monitoring_total_receives = 0
        self.reconnects = 0
        self.reconnects_lock = threading.Lock()
        self.restart_requests = {}
        self.start_time = time.time()
        self.stream_buffer = []
        self.stream_list = {}
        self.total_received_bytes = 0
        self.total_received_bytes_lock = threading.Lock()
        self.total_receives = 0
        self.total_receives_lock = threading.Lock()
        self.total_transmitted = 0
        self.total_transmitted_lock = threading.Lock()
        self.websocket_list = {}
        self.request_id = 0
        self.request_id_lock = threading.Lock()
        self.start()

    def _add_socket_to_socket_list(self, stream_id, channels, markets):
        """
        Create a list entry for new sockets

        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: uuid
        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        """
        self.stream_list[stream_id] = {'exchange': self.exchange,
                                       'stream_id': copy.deepcopy(stream_id),
                                       'channels': copy.deepcopy(channels),
                                       'markets': copy.deepcopy(markets),
                                       'payload': [],
                                       'api_key': copy.deepcopy(self.api_key),
                                       'api_secret': copy.deepcopy(self.api_secret),
                                       'dex_user_address': copy.deepcopy(self.dex_user_address),
                                       'status': 'starting',
                                       'start_time': time.time(),
                                       'processed_receives_total': 0,
                                       'receives_statistic_last_second': {'most_receives_per_second': 0, 'entries': {}},
                                       'seconds_to_last_heartbeat': None,
                                       'last_heartbeat': None,
                                       'stop_request': None,
                                       'seconds_since_has_stopped': None,
                                       'has_stopped': False,
                                       'reconnects': 0,
                                       'logged_reconnects': [],
                                       'processed_transmitted_total': 0,
                                       'last_static_ping_listen_key': 0,
                                       'listen_key': False,
                                       'listen_key_cache_time': 30 * 60,
                                       'processed_receives_statistic': {},
                                       'transfer_rate_per_second': {'bytes': {}, 'speed': 0}}
        logging.debug("BinanceWebSocketApiManager->_add_socket_to_socket_list(" +
                      str(stream_id) + ", " + str(channels) + ", " + str(markets) + ")")

    def _create_stream_thread(self, loop, stream_id, channels, markets, restart=False):
        """
        Co function of self.create_stream to create a thread for the socket and to manage the coroutine

        :param loop: provide a asynio loop
        :type loop: asyncio loop
        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: uuid
        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :param restart: set to `True`, if its a restart!
        :type restart: bool
        :return:
        """
        if restart is False:
            self._add_socket_to_socket_list(stream_id, channels, markets)
        asyncio.set_event_loop(loop)
        binance_websocket_api_socket = BinanceWebSocketApiSocket(self, stream_id, channels, markets)
        try:
            loop.run_until_complete(binance_websocket_api_socket.start_socket())
        finally:
            loop.close()

    def _frequent_checks(self):
        """
        This method gets started as a thread and is doing the frequent checks
        """
        frequent_checks_id = time.time()
        self.frequent_checks_list[frequent_checks_id] = {'last_heartbeat': 0,
                                                         'stop_request': None,
                                                         'has_stopped': False}
        logging.info("BinanceWebSocketApiManager->_frequent_checks() new instance created with frequent_checks_id=" +
                     str(frequent_checks_id))
        for frequent_checks_instance in self.frequent_checks_list:
            if frequent_checks_instance != frequent_checks_id:
                try:
                    if (self.keepalive_streams_list[frequent_checks_instance]['last_heartbeat'] + 3) > time.time():
                        logging.info("BinanceWebSocketApiManager->_frequent_checks() found an other living instance, "
                                     "so i stop" + str(frequent_checks_id))
                        sys.exit(1)
                except KeyError:
                    logging.debug("BinanceWebSocketApiManager->_frequent_checks() - Info: KeyError "
                                  "" + str(frequent_checks_id))

        # threaded loop for min 1 check per second
        while self.stop_manager_request is None and self.frequent_checks_list[frequent_checks_id]['stop_request'] \
                is None:
            self.frequent_checks_list[frequent_checks_id]['last_heartbeat'] = time.time()
            time.sleep(0.8)
            current_timestamp = int(time.time())
            last_timestamp = current_timestamp - 1
            next_to_last_timestamp = current_timestamp - 2
            total_most_stream_receives_last_timestamp = 0
            total_most_stream_receives_next_to_last_timestamp = 0
            active_stream_list = self.get_active_stream_list()
            # count most_receives_per_second total last second
            if active_stream_list:
                for stream_id in active_stream_list:
                    # set the streams `most_receives_per_second` value
                    try:
                        if self.stream_list[stream_id]['receives_statistic_last_second']['entries'][last_timestamp] > \
                                self.stream_list[stream_id]['receives_statistic_last_second']['most_receives_per_second']:
                            self.stream_list[stream_id]['receives_statistic_last_second']['most_receives_per_second'] = \
                                self.stream_list[stream_id]['receives_statistic_last_second']['entries'][last_timestamp]
                    except KeyError:
                        pass
                    try:
                        total_most_stream_receives_last_timestamp += self.stream_list[stream_id]['receives_statistic_last_second']['entries'][last_timestamp]
                    except KeyError:
                        pass
                    try:
                        total_most_stream_receives_next_to_last_timestamp += self.stream_list[stream_id]['receives_statistic_last_second']['entries'][next_to_last_timestamp]
                    except KeyError:
                        pass

                    # delete list entries older than `keep_max_received_last_second_entries`
                    # receives_statistic_last_second
                    delete_index = []
                    if len(self.stream_list[stream_id]['receives_statistic_last_second']['entries']) > self.keep_max_received_last_second_entries:
                        temp_entries = copy.deepcopy(self.stream_list[stream_id]['receives_statistic_last_second']['entries'])
                        for timestamp_key in temp_entries:
                            try:
                                if timestamp_key < current_timestamp - self.keep_max_received_last_second_entries:
                                    delete_index.append(timestamp_key)
                            except ValueError as error_msg:
                                logging.error(
                                    "BinanceWebSocketManager->_frequent_checks() timestamp_key=" + str(timestamp_key) +
                                    " current_timestamp=" + str(current_timestamp) + " keep_max_received_last_second_"
                                    "entries=" + str(self.keep_max_received_last_second_entries) + " error_msg=" +
                                    str(error_msg))
                    for timestamp_key in delete_index:
                        self.stream_list[stream_id]['receives_statistic_last_second']['entries'].pop(timestamp_key, None)
                    # transfer_rate_per_second
                    delete_index = []
                    if len(self.stream_list[stream_id]['transfer_rate_per_second']['bytes']) > self.keep_max_received_last_second_entries:
                        try:
                            temp_bytes = self.stream_list[stream_id]['transfer_rate_per_second']['bytes']
                            for timestamp_key in temp_bytes:
                                try:
                                    if timestamp_key < current_timestamp - self.keep_max_received_last_second_entries:
                                        delete_index.append(timestamp_key)
                                except ValueError as error_msg:
                                    logging.error(
                                        "BinanceWebSocketManager->_frequent_checks() timestamp_key=" + str(timestamp_key) +
                                        " current_timestamp=" + str(current_timestamp) + " keep_max_received_last_second_"
                                        "entries=" + str(self.keep_max_received_last_second_entries) + " error_msg=" +
                                        str(error_msg))
                        except RuntimeError as error_msg:
                            logging.debug("Catched RuntimeError: " + str(error_msg))
                    for timestamp_key in delete_index:
                        self.stream_list[stream_id]['transfer_rate_per_second']['bytes'].pop(timestamp_key, None)

            # set most_receives_per_second
            try:
                if int(self.most_receives_per_second) < int(total_most_stream_receives_last_timestamp):
                    self.most_receives_per_second = int(total_most_stream_receives_last_timestamp)
            except ValueError as error_msg:
                logging.error("BinanceWebSocketManager->_frequent_checks() self.most_receives_per_second"
                              "=" + str(self.most_receives_per_second) +  " total_most_stream_receives_last_timestamp"
                              "=" + str(total_most_stream_receives_last_timestamp) + " total_most_stream_receives_next_"
                              "to_last_timestamp=" + str(total_most_stream_receives_next_to_last_timestamp) + " error_"
                              "msg=" + str(error_msg))
            try:
                if int(self.most_receives_per_second) < int(total_most_stream_receives_next_to_last_timestamp):
                    self.most_receives_per_second = int(total_most_stream_receives_next_to_last_timestamp)
            except ValueError as error_msg:
                logging.error("BinanceWebSocketManager->_frequent_checks() self.most_receives_per_second=" + str(
                    self.most_receives_per_second) + " total_most_stream_receives_last_timestamp=" +
                              str(total_most_stream_receives_last_timestamp) + " total_most_stream_receives_next_to_"
                                                                               "last_timestamp=" +
                              str(total_most_stream_receives_next_to_last_timestamp) + " error_msg=" + str(error_msg))
            # control _keepalive_streams
            found_alive_keepalive_streams = False
            for keepalive_streams_id in self.keepalive_streams_list:
                try:
                    if (current_timestamp - self.keepalive_streams_list[keepalive_streams_id]['last_heartbeat']) < 3:
                        found_alive_keepalive_streams = True
                except TypeError:
                    pass
            # start a new one, if there isnt one
            if found_alive_keepalive_streams is False:
                self._keepalive_streams_restart_request = True
            # send keepalive for `!userData` streams every 30 minutes
            if active_stream_list:
                for stream_id in active_stream_list:
                    if isinstance(active_stream_list[stream_id]['markets'], str):
                        active_stream_list[stream_id]['markets'] = [active_stream_list[stream_id]['markets'],]
                    if isinstance(active_stream_list[stream_id]['markets'], list):
                        if "!userData" in active_stream_list[stream_id]['markets']:
                            if (active_stream_list[stream_id]['start_time'] + active_stream_list[stream_id]['listen_key_cache_time']) \
                                    < time.time() and (active_stream_list[stream_id]['last_static_ping_listen_key'] +
                                                       active_stream_list[stream_id]['listen_key_cache_time']) < time.time():
                                # keep-alive the listenKey
                                binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.exchange,
                                                                                                 self.stream_list[stream_id]['api_key'],
                                                                                                 self.stream_list[stream_id]['api_secret'],
                                                                                                 self.get_version(),
                                                                                                 self.binance_api_status)
                                binance_websocket_api_restclient.keepalive_listen_key(self.stream_list[stream_id]['listen_key'])
                                del binance_websocket_api_restclient
                                # set last_static_ping_listen_key
                                self.stream_list[stream_id]['last_static_ping_listen_key'] = time.time()
                                self.set_heartbeat(stream_id)
                                logging.info("sent listen_key keepalive ping for stream_id=" + str(stream_id))
        sys.exit(0)

    def _keepalive_streams(self):
        """
        This method is started as a thread and is observing the streams, if neccessary it restarts a died stream
        """
        keepalive_streams_id = time.time()
        self.keepalive_streams_list[keepalive_streams_id] = {'last_heartbeat': 0,
                                                             'stop_request': None,
                                                             'has_stopped': False}
        logging.info(
            "BinanceWebSocketApiManager->_keepalive_streams() new instance created with keepalive_streams_id=" +
            str(keepalive_streams_id))
        for keepalive_streams_instance in self.keepalive_streams_list:
            if keepalive_streams_instance != keepalive_streams_id:
                if (self.keepalive_streams_list[keepalive_streams_instance]['last_heartbeat'] + 3) > time.time():
                    logging.info(
                        "BinanceWebSocketApiManager->_keepalive_streams() found an other living instance, so i stopp" +
                        str(keepalive_streams_id))
                    sys.exit(1)
        # threaded loop to restart crashed streams:
        while self.stop_manager_request is None and \
                self.keepalive_streams_list[keepalive_streams_id]['stop_request'] is None:
            self.keepalive_streams_list[keepalive_streams_id]['last_heartbeat'] = time.time()
            time.sleep(1)
            # restart streams with a restart_request (status == new)
            temp_restart_requests = copy.deepcopy(self.restart_requests)
            for stream_id in temp_restart_requests:
                # find restarts that didnt work
                try:
                    if self.restart_requests[stream_id]['status'] == "restarted" and \
                            self.restart_requests[stream_id]['last_restart_time']+5 < time.time():
                        self.restart_requests[stream_id]['status'] = "new"
                    # restart streams with requests
                    if self.restart_requests[stream_id]['status'] == "new":
                        self.restart_stream(stream_id)
                        self.restart_requests[stream_id]['status'] = "restarted"
                        self.restart_requests[stream_id]['last_restart_time'] = time.time()
                        self.stream_list[stream_id]['status'] = "restarting"
                except KeyError:
                    pass
            # control frequent_checks_threads for two cases:
            # 1) there should only be one! stop others if necessary:
            found_alive_frequent_checks = False
            current_timestamp = time.time()
            for frequent_checks_id in self.frequent_checks_list:
                try:
                    if (current_timestamp - self.frequent_checks_list[frequent_checks_id]['last_heartbeat']) < 2:
                        found_alive_frequent_checks = True
                except TypeError:
                    pass
            # 2) start a new one, if there isnt one
            if found_alive_frequent_checks is False:
                self._frequent_checks_restart_request = True
        sys.exit(0)

    def _start_monitoring_api_thread(self, host, port, warn_on_update):
        """
        Threaded method that servces the monitoring api

        :param host: IP or hostname to use
        :type host: str
        :param port: Port to use
        :type port: int
        :param warn_on_update: Should the monitoring system report available updates?
        :type warn_on_update: bool
        """
        logging.info("starting monitoring API service ...")
        app = Flask(__name__)
        @app.route('/')
        @app.route('/status/')
        def redirect_to_wiki():
            logging.debug("Visit https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki/UNICORN-"
                          "Monitoring-API-Service for further information!")
            return redirect("https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki/"
                            "UNICORN-Monitoring-API-Service", code=302)

        api = Api(app)
        api.add_resource(BinanceWebSocketApiRestServer,
                         "/status/<string:statusformat>/",
                         "/status/<string:statusformat>/<string:checkcommandversion>",
                         resource_class_kwargs={'handler_binance_websocket_api_manager': self,
                                                'warn_on_update': warn_on_update})
        try:
            dispatcher = wsgi.PathInfoDispatcher({'/': app})
            self.monitoring_api_server = wsgi.WSGIServer((host, port), dispatcher)
            self.monitoring_api_server.start()
        except RuntimeError as error_msg:
            logging.error("monitoring API service is going down! - info: " + str(error_msg))

    def add_to_stream_buffer(self, stream_data):
        """
        Kick back data to the stream_buffer

        If it is not possible to process received stream data (for example, the database is restarting, so its not
        possible to save the data), you can return the data back into the stream_buffer. After a few seconds you stopped
        writing data back to the stream_buffer, the BinanceWebSocketApiManager starts flushing back the data to normal
        processing.

        :param stream_data: the data you want to write back to the buffer
        :type stream_data: raw stream_data or unicorn_fied stream data
        """
        self.stream_buffer.append(stream_data)
        self.last_entry_added_to_stream_buffer = time.time()

    def add_total_received_bytes(self, size):
        """
        Add received bytes to the total received bytes statistic

        :param size: int value of added bytes
        :type size: int
        """
        with self.total_received_bytes_lock:
            self.total_received_bytes += int(size)

    def create_payload(self, stream_id, method, channels=False, markets=False):
        """
        Create the payload for subscriptions

        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: uuid
        :param method: `SUBSCRIBE` or `UNSUBSCRIBE`
        :type method: str
        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :return: payload (list) or False
        """
        logging.debug("BinanceWebSocketApiManager->create_payload(" + str(stream_id) + ", " + str(channels) + ", " +
                      str(markets) + ") started ...")
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        payload = []
        if self.is_exchange_type("dex"):
            if method == "subscribe":
                for channel in channels:
                    add_payload = {"method": method,
                                   "topic": channel}
                    symbols = []
                    for market in markets:
                        if re.match(r'[a-zA-Z0-9]{41,43}', market) is not None:
                            if self.stream_list[stream_id]['dex_user_address'] is False:
                                self.stream_list[stream_id]['dex_user_address'] = market
                        else:
                            symbols.append(market)
                    try:
                        if self.stream_list[stream_id]["dex_user_address"] is not False:
                            add_payload["address"] = self.stream_list[stream_id]["dex_user_address"]
                            payload.append(add_payload)
                    except KeyError:
                        pass
                    if len(symbols) > 0:
                        add_payload["symbols"] = symbols
                        payload.append(add_payload)
            elif method == "unsubscribe":
                if markets:
                    add_payload = {"method": method}
                    for market in markets:
                        if re.match(r'[a-zA-Z0-9]{41,43}', market) is not None:
                            if self.stream_list[stream_id]['dex_user_address'] is False:
                                self.stream_list[stream_id]['dex_user_address'] = market
                                markets.remove(market)
                    if len(markets) > 0:
                        add_payload["symbols"] = markets
                        payload.append(add_payload)
                if channels:
                    for channel in channels:
                        add_payload = {"method": method,
                                       "topic": channel}
                        payload.append(add_payload)
            else:
                logging.critical("BinanceWebSocketApiManager->create_payload(" + str(stream_id) + ", "
                                 + str(channels) + ", " + str(markets) + ") Allowed values for `method`: `subscribe` "
                                 "or `unsubscribe`!")
                return False
        elif self.is_exchange_type("cex"):
            if method == "subscribe":
                params = []
                for channel in channels:
                    for market in markets:
                        if market == "!ticker":
                            params.append(market + "@arr")
                        elif market == "!miniTicker":
                            params.append(market + "@arr")
                        elif market == "!bookTicker":
                            params.append(market + "@arr")
                        elif channel == "!ticker":
                            params.append(channel + "@arr")
                        elif channel == "!miniTicker":
                            params.append(channel + "@arr")
                        elif channel == "!bookTicker":
                            params.append(channel + "@arr")
                        else:
                            params.append(market + "@" + channel)
                if len(params) > 0:
                    payload = self.split_payload(params, "SUBSCRIBE")
            elif method == "unsubscribe":
                if markets:
                    params = []
                    for channel in self.stream_list[stream_id]['channels']:
                        for market in markets:
                            if market == "!ticker":
                                params.append(market + "@arr")
                            elif market == "!miniTicker":
                                params.append(market + "@arr")
                            elif market == "!bookTicker":
                                params.append(market + "@arr")
                            elif channel == "!ticker":
                                params.append(channel + "@arr")
                            elif channel == "!miniTicker":
                                params.append(channel + "@arr")
                            elif channel == "!bookTicker":
                                params.append(channel + "@arr")
                            else:
                                params.append(market + "@" + channel)
                    if len(params) > 0:
                        payload = self.split_payload(params, "UNSUBSCRIBE")
                if channels:
                        params = []
                        for market in self.stream_list[stream_id]['markets']:
                            for channel in channels:
                                if market == "!ticker":
                                    params.append(market + "@arr")
                                elif market == "!miniTicker":
                                    params.append(market + "@arr")
                                elif market == "!bookTicker":
                                    params.append(market + "@arr")
                                elif channel == "!ticker":
                                    params.append(channel + "@arr")
                                elif channel == "!miniTicker":
                                    params.append(channel + "@arr")
                                elif channel == "!bookTicker":
                                    params.append(channel + "@arr")
                                else:
                                    params.append(market + "@" + channel)
                        if len(params) > 0:
                            payload = self.split_payload(params, "UNSUBSCRIBE")
            else:
                logging.critical("BinanceWebSocketApiManager->create_payload(" + str(stream_id) + ", "
                                 + str(channels) + ", " + str(markets) + ") Allowed values for `method`: `subscribe` "
                                 "or `unsubscribe`!")
                return False
        logging.debug("BinanceWebSocketApiManager->create_payload(" + str(stream_id) + ", "
                      + str(channels) + ", " + str(markets) + ") Payload: " + str(payload))
        logging.debug("BinanceWebSocketApiManager->create_payload(" + str(stream_id) + ", " + str(channels) + ", " +
                      str(markets) + ") finished ...")
        return payload

    def create_stream(self, channels, markets):
        """
        Create a websocket stream

        If you provide 2 markets and 2 channels, then you are going to create 4 subscriptions (markets * channels).

        Example:

            markets = ['bnbbtc', 'ethbtc']

            channels = ['trade', 'kline_1']

            Finally:  bnbbtc@trade, ethbtc@trade, bnbbtc@kline_1, ethbtc@kline_1


        Create !userData streams as single streams, because its using an own endpoint and can not get combined with
        other streams in a multiplexed stream!

        Example:

        `binance_websocket_api_manager.set_private_api_config(binance_api_key, binance_api_secret)`

        `userdata_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!userData"])`

        To create a multiplexed stream which includes also `!miniTicker@arr`, `!ticker@arr` or `!bookTicker@arr` you
        just need to add `!miniTicker` to the cannels list - dont add `arr` to the markets list.

        But you have to add `arr`if you want to start it as a single stream!

        Example:

        `binance_websocket_api_manager.subscribe_to_stream(stream_id, channels=['kline_5m', 'marketDepth', '!miniTicker'])`

        :param channels: provide the channels you wish to stream
        :type channels: str, tuple, list, set
        :param markets: provide the markets you wish to stream
        :type markets: str, tuple, list, set
        :return: stream_id or 'False'
        """
        # create a stream
        stream_id = uuid.uuid4()
        logging.info("BinanceWebSocketApiManager->create_stream(" + str(channels) + ", " + str(markets) + ") "
                     "with stream_id=" + str(stream_id))
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self._create_stream_thread, args=(loop, stream_id, channels, markets))
        thread.start()
        return stream_id

    def create_websocket_uri(self, channels, markets, stream_id=False, api_key=False, api_secret=False):
        """
        Create a websocket URI

        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: uuid
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :return: str or False
        """
        payload = []
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        if len(channels) == 1 and len(markets) == 1:
            if "!userData" in channels or "!userData" in markets:
                if stream_id is not False:
                    response = self.get_listen_key_from_restclient(stream_id, api_key, api_secret)
                    try:
                        if response['code'] == -2014 or response['code'] == -2015:
                            logging.error("Received known error code from rest client: " + str(response))
                            return response
                        else:
                            logging.critical("Received unknown error code from rest client: " + str(response))
                            return response
                    except KeyError:
                        pass
                    except TypeError:
                        pass
                    if response:
                        try:
                            uri = self.websocket_base_uri + "ws/" + str(response['listenKey'])
                            return uri
                        except KeyError:
                            return False
                        except TypeError:
                            return False
                    else:
                        logging.debug("Error: Can not create websocket URI!")
                        return False
                else:
                    logging.debug("Error: Can not create websocket URI!")
                    return False
            elif "!bookTicker" in channels or "!bookTicker" in markets:
                return self.websocket_base_uri + "ws/!bookTicker"
            elif "arr" in channels or "$all" in markets:
                return self.websocket_base_uri + "ws/" + markets[0] + "@" + channels[0]
            elif "arr" in markets or "$all" in channels:
                return self.websocket_base_uri + "ws/" + channels[0] + "@" + markets[0]
            elif self.is_exchange_type("dex"):
                if re.match(r'[a-zA-Z0-9]{41,43}', markets[0]) is not None:
                    try:
                        if self.stream_list[stream_id]['dex_user_address'] is False:
                            self.stream_list[stream_id]['dex_user_address'] = markets[0]
                        if self.stream_list[stream_id]['dex_user_address'] != markets[0]:
                            logging.error(
                                "Error: once set, the dex_user_address is not allowed to get changed anymore!")
                            return False
                    except KeyError:
                        pass
                    add_payload = {"method": "subscribe",
                                   "topic": channels[0],
                                   "address": markets[0]}
                    payload.append(add_payload)
                    if stream_id:
                        self.stream_list[stream_id]['payload'] = payload
                    return self.websocket_base_uri + "ws/" + markets[0]
                elif markets[0] != "" and channels[0] != "":
                    return self.websocket_base_uri + "ws/" + markets[0] + "@" + channels[0]
                else:
                    logging.error("Error: not able to create websocket URI for DEX")
                    return False
        if self.is_exchange_type("dex"):
            query = "ws"
            if stream_id:
                payload = self.create_payload(stream_id, "subscribe", channels=channels, markets=markets)
                self.stream_list[stream_id]['payload'] = payload
            return self.websocket_base_uri + str(query)
        else:
            query = "stream?streams="
            for channel in channels:
                if channel == "!ticker":
                    self.subscribe_to_stream(stream_id, markets=channel)
                    logging.debug("Create subscription " + str(channel))
                if channel == "!miniTicker":
                    self.subscribe_to_stream(stream_id, markets=channel)
                    logging.debug("Create subscription " + str(channel))
                if channel == "!bookTicker":
                    self.subscribe_to_stream(stream_id, markets=channel)
                    logging.debug("Create subscription " + str(channel))
                if channel == "!userData":
                    logging.error("Can not create 'outboundAccountInfo' in a multi channel socket! "
                                  "Unfortunately Binance only stream it in a single stream socket! ./"
                                  "Use binance_websocket_api_manager.create_stream([\"arr\"], [\"!userData\"]) to "
                                  "initiate an extra connection.")
                    return False
                for market in markets:
                    if market == "!ticker":
                        self.subscribe_to_stream(stream_id, markets=market)
                        logging.debug("Create subscription " + str(market))
                    if market == "!miniTicker":
                        self.subscribe_to_stream(stream_id, markets=market)
                        logging.debug("Create subscription " + str(market))
                    if market == "!bookTicker":
                        self.subscribe_to_stream(stream_id, markets=market)
                        logging.debug("Create subscription " + str(market))
                    if market == "!userData":
                        logging.error("Can not create 'outboundAccountInfo' in a multi channel socket! "
                                      "Unfortunatly Binance only stream it in a single stream socket! ./"
                                      "Use binance_websocket_api_manager.create_stream([\"arr\"], [\"!userData\"]) to "
                                      "initiate an extra connection.")
                        return False
            query += market.lower() + "@" + channel
            self.subscribe_to_stream(stream_id, markets=markets, channels=channels)
            logging.debug("Created websocket URI for stream_id=" + str(stream_id) + " is " +
                          self.websocket_base_uri + str(query))
            return self.websocket_base_uri + str(query)

    def delete_listen_key_by_stream_id(self, stream_id):
        """
        Delete a binance listen_key from a specific !userData stream

        :param stream_id: id of a !userData stream
        :type stream_id: uuid
        """
        if self.stream_list[stream_id]['listen_key'] is not False:
            logging.info("BinanceWebSocketApiManager->stop_manager_with_all_streams(" + str(
                stream_id) + ")->delete_listen_key")
            binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.exchange,
                                                                             self.stream_list[stream_id]['api_key'],
                                                                             self.stream_list[stream_id]['api_secret'],
                                                                             self.get_version(),
                                                                             self.used_weight)
            binance_websocket_api_restclient.delete_listen_key(self.stream_list[stream_id]['listen_key'])
            del binance_websocket_api_restclient

    def delete_stream_from_stream_list(self, stream_id):
        """
        Delete a stream from the stream_list

        Even if a stream crashes or get stopped, its data remains in the BinanceWebSocketApiManager till you stop the
        BinanceWebSocketApiManager itself. If you want to tidy up the stream_list you can use this method.

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: bool
        """
        logging.debug("deleting " + str(stream_id) + " from stream_list")
        return self.stream_list.pop(stream_id, False)

    def fill_up_space(self, demand_of_chars, string):
        """
        Add whitespaces to `string` to a length of `demand_of_chars`

        :param demand_of_chars: how much chars does the string have to have?
        :type demand_of_chars: int
        :param string: the string that has to get filled up with spaces
        :type string: str
        :return: the filled up string
        """
        blanks_pre = ""
        blanks_post = ""
        demand_of_blanks = demand_of_chars - len(str(string)) - 1
        while len(blanks_pre) < demand_of_blanks:
            blanks_pre += " "
            blanks_post = " "
        return blanks_pre + str(string) + blanks_post

    def get_active_stream_list(self):
        """
        Get a list of all active streams

        :return: set
        """
        # get the stream_list without stopped and crashed streams
        stream_list_with_active_streams = {}
        for stream_id in self.stream_list:
            if self.stream_list[stream_id]['status'] == "running":
                stream_list_with_active_streams[stream_id] = self.stream_list[stream_id]
        try:
            if len(stream_list_with_active_streams[stream_id]) > 0:
                return stream_list_with_active_streams
        except KeyError:
            return False
        except UnboundLocalError:
            return False

    def get_all_receives_last_second(self):
        """
        Get the number of all receives of the last second

        :return: int
        """
        all_receives_last_second = 0
        last_second_timestamp = int(time.time()) - 1
        for stream_id in self.stream_list:
            try:
                all_receives_last_second += self.stream_list[stream_id]['receives_statistic_last_second']['entries'][
                    last_second_timestamp]
            except KeyError:
                pass
        return all_receives_last_second

    def get_binance_api_status(self):
        """
        Get used_weight, last status_code and the timestamp of the last status update

        :return: dict
        """
        return self.binance_api_status

    def get_current_receiving_speed(self, stream_id):
        """
        Get the receiving speed of the last second in Bytes

        :return: int
        """
        current_timestamp = int(time.time())
        last_timestamp = current_timestamp - 1
        try:
            if self.stream_list[stream_id]['transfer_rate_per_second']['bytes'][last_timestamp] > 0:
                self.stream_list[stream_id]['transfer_rate_per_second']['speed'] = \
                    self.stream_list[stream_id]['transfer_rate_per_second']['bytes'][last_timestamp]
        except TypeError:
            pass
        except KeyError:
            pass
        try:
            current_receiving_speed = self.stream_list[stream_id]['transfer_rate_per_second']['speed']
        except KeyError:
            current_receiving_speed = 0
        return current_receiving_speed

    def get_exchange(self):
        """
        Get the name of the used exchange like "binance.com" or "binance.org-testnet"

        :return: str
        """
        return self.exchange

    def get_human_bytesize(self, bytes, suffix=""):
        """
        Convert the bytes to something readable

        :param bytes: amount of bytes
        :type bytes: int
        :param suffix: add a string after
        :type suffix: str
        :return:
        """
        if bytes > 1024 * 1024 * 1024:
            bytes = str(round(bytes / (1024 * 1024 * 1024), 2)) + " gB" + suffix
        elif bytes > 1024 * 1024:
            bytes = str(round(bytes / (1024 * 1024), 2)) + " mB" + suffix
        elif bytes > 1024:
            bytes = str(round(bytes / 1024, 2)) + " kB" + suffix
        else:
            bytes = str(bytes) + " B" + suffix
        return bytes

    def get_human_uptime(self, uptime):
        """
        Convert a timespan of seconds into hours, days, ...

        :param uptime: Uptime in seconds
        :type uptime: int
        :return:
        """
        if uptime > (60 * 60 * 24):
            uptime_days = int(uptime / (60 * 60 * 24))
            uptime_hours = int(((uptime - (uptime_days * (60 * 60 * 24))) / (60 * 60)))
            uptime_minutes = int((uptime - ((uptime_days * (60 * 60 * 24)) + (uptime_hours * 60 * 60))) / 60)
            uptime_seconds = int(
                uptime - ((uptime_days * (60 * 60 * 24)) + ((uptime_hours * (60 * 60)) + (uptime_minutes * 60))))
            uptime = str(uptime_days) + "d:" + str(uptime_hours) + "h:" + str(int(uptime_minutes)) + "m:" + str(
                int(uptime_seconds)) + "s"
        elif uptime > (60 * 60):
            uptime_hours = int(uptime / (60 * 60))
            uptime_minutes = int((uptime - (uptime_hours * (60 * 60))) / 60)
            uptime_seconds = int(uptime - ((uptime_hours * (60 * 60)) + (uptime_minutes * 60)))
            uptime = str(uptime_hours) + "h:" + str(int(uptime_minutes)) + "m:" + str(int(uptime_seconds)) + "s"
        elif uptime > 60:
            uptime_minutes = int(uptime / 60)
            uptime_seconds = uptime - uptime_minutes * 60
            uptime = str(uptime_minutes) + "m:" + str(int(uptime_seconds)) + "s"
        else:
            uptime = str(int(uptime)) + " seconds"
        return uptime

    def get_latest_release_info(self):
        """
        Get infos about the latest available release

        :return: dict or False
        """
        try:
            respond = requests.get('https://api.github.com/repos/oliver-zehentleitner/unicorn-binance-websocket-api/'
                                   'releases/latest')
            latest_release_info = respond.json()
            return latest_release_info
        except Exception:
            return False

    def get_latest_release_info_check_command(self):
        """
        Get infos about the latest available `check_unicorn_monitoring_api` release
        
        :return: dict or False
        """
        try:
            respond = requests.get('https://api.github.com/repos/oliver-zehentleitner/check_unicorn_monitoring_api/'
                                   'releases/latest')
            return respond.json()
        except Exception:
            return False

    def get_latest_version(self):
        """
        Get the version of the latest available release (cache time 1 hour)

        :return: str or False
        """
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github['status'] is None or \
                (self.last_update_check_github['timestamp']+(60*60) < time.time()):
            self.last_update_check_github['status'] = self.get_latest_release_info()
        if self.last_update_check_github['status']:
            try:
                return self.last_update_check_github['status']["tag_name"]
            except KeyError:
                return "unknown"
        else:
            return "unknown"

    def get_latest_version_check_command(self):
        """
        Get the version of the latest available `check_unicorn_monitoring_api` release (cache time 1 hour)
        
        :return: str or False
        """
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github_check_command['status'] is None or \
                (self.last_update_check_github_check_command['timestamp'] + (60 * 60) < time.time()):
            self.last_update_check_github_check_command['status'] = self.get_latest_release_info_check_command()
        if self.last_update_check_github_check_command['status']:
            try:
                return self.last_update_check_github_check_command['status']["tag_name"]
            except KeyError:
                return "unknown"
        else:
            return "unknown"

    def get_listen_key_from_restclient(self, stream_id, api_key, api_secret):
        """
        Get a new or cached (<30m) listen_key

        :param stream_id: provide a stream_id
        :type stream_id: uuid
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :return: str or False
        """
        if (self.stream_list[stream_id]['start_time'] + self.stream_list[stream_id]['listen_key_cache_time']) > \
                time.time() or (self.stream_list[stream_id]['last_static_ping_listen_key'] +
                                self.stream_list[stream_id]['listen_key_cache_time']) > time.time():
            # listen_key is not older than 30 min
            if self.stream_list[stream_id]['listen_key'] is not False:
                response = {'listenKey': self.stream_list[stream_id]['listen_key']}
                return response
        # no cached listen_key or listen_key is older than 30 min
        # acquire a new listen_key:
        binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.exchange, api_key, api_secret,
                                                                         self.get_version(), self.binance_api_status)
        response = binance_websocket_api_restclient.get_listen_key()
        del binance_websocket_api_restclient
        if response:
            # save and return the valid listen_key
            try:
                self.stream_list[stream_id]['listen_key'] = str(response['listenKey'])
                return response
            except KeyError:
                # no valid listen_key, but a response from endpoint
                return response
            except TypeError:
                return response
        else:
            # no valid listen_key
            return False

    def get_most_receives_per_second(self):
        """
        Get the highest total receives per second value

        :return: int
        """
        return self.most_receives_per_second

    def get_number_of_streams_in_stream_list(self):
        """
        Get the number of streams that are stored in the stream_list

        :return: int
        """
        return len(self.stream_list)

    def get_keep_max_received_last_second_entries(self):
        """
        Get the number of how much received_last_second entries are stored till they get deleted

        :return: int
        """
        return self.keep_max_received_last_second_entries

    def get_monitoring_status_icinga(self, check_command_version=False, warn_on_update=True):
        """
        Get status and perfdata to monitor and collect metrics with ICINGA/Nagios

        status: OK, WARNING, CRITICAL
        - WARNING: on restarts, available updates
        - CRITICAL: crashed streams

        perfdata:
        - average receives per second since last status check
        - average speed per second since last status check
        - total received bytes since start
        - total received length since start
        - stream_buffer size
        - stream_buffer length
        - reconnects
        - uptime

        :param check_command_version: is the version of the calling check_command (https://github.com/oliver-zehentleitner/check_unicorn_monitoring_api)
        :type check_command_version: str
        :param warn_on_update: set to `False` to disable the update warning
        :type warn_on_update: bool
        :return: dict (text, time, return_code)
        """
        result = self.get_monitoring_status_plain(check_command_version=check_command_version,
                                                  warn_on_update=warn_on_update)
        if len(result['update_msg']) > 0 or len(result['status_msg']) > 0:
            text_msg = " -" + str(result['status_msg']) + str(result['update_msg'])
        else:
            text_msg = ""
        check_message = "BINANCE WEBSOCKETS (" + self.exchange + ") - " + result['status_text'] + ": O:" + \
                        str(result['active_streams']) + \
                        "/R:" + str(result['restarting_streams']) + "/C:" + str(result['crashed_streams']) + "/S:" + \
                        str(result['stopped_streams']) + text_msg + " | " + \
                        "active streams=" + str(result['active_streams']) + ";;;0 " + \
                        "average_receives_per_second=" + str(result['average_receives_per_second']) + \
                        ";;;0 current_receiving_speed_per_second=" + str(result['average_speed_per_second']) + \
                        "KB;;;0 total_received_length=" + str(result['total_received_length']) + "c;;;0 total_" \
                        "received_size=" + str(result['total_received_mb']) + "MB;;;0 stream_buffer_size=" + \
                        str(result['stream_buffer_mb']) + "MB;;;0 stream_buffer_length=" + \
                        str(result['stream_buffer_items']) + ";;;0 reconnects=" + str(result['reconnects']) + "c;;;0 " \
                        "uptime_days=" + str(result['uptime']) + "c;;;0"
        status = {'text': check_message,
                  'time': int(result['timestamp']),
                  'return_code': result['return_code']}
        return status

    def get_monitoring_status_plain(self, check_command_version=False, warn_on_update=True):
        """
        Get plain monitoring status data:
        active_streams, crashed_streams, restarting_streams, stopped_streams, return_code, status_text,
        timestamp, update_msg, average_receives_per_second, average_speed_per_second, total_received_mb,
        stream_buffer_items, stream_buffer_mb, reconnects, uptime

        :param check_command_version: is the version of the calling check_command (https://github.com/oliver-zehentleitner/check_unicorn_monitoring_api)
        :type check_command_version: str
        :param warn_on_update: set to `False` to disable the update warning
        :type warn_on_update: bool
        :return: dict
        """
        result = {}
        result['active_streams'] = 0
        result['crashed_streams'] = 0
        result['restarting_streams'] = 0
        result['highest_restart_per_stream_last_hour'] = 0
        result['return_code'] = 0
        result['status_text'] = "OK"
        result['status_msg'] = ""
        result['stopped_streams'] = 0
        result['timestamp'] = time.time()
        result['update_msg'] = ""
        time_period = result['timestamp'] - self.last_monitoring_check
        timestamp_last_hour = time.time() - (60*60)
        try:
            from unicorn_fy.unicorn_fy import UnicornFy
            unicorn_fy = UnicornFy()
            is_update_available_unicorn_fy = unicorn_fy.is_update_availabe()
        except ModuleNotFoundError:
            logging.debug("UnicornFy not installed!")
            is_update_available_unicorn_fy = False
        except AttributeError:
            logging.error("UnicornFy outdated!")
            is_update_available_unicorn_fy = True
        if check_command_version:
            is_update_available_check_command = self.is_update_availabe_check_command(check_command_version=check_command_version)
        else:
            is_update_available_check_command = True
        for stream_id in self.stream_list:
            stream_restarts_last_hour = 0
            for reconnect in self.stream_list[stream_id]['logged_reconnects']:
                if reconnect > timestamp_last_hour:
                    stream_restarts_last_hour += 1
            if stream_restarts_last_hour > result['highest_restart_per_stream_last_hour']:
                result['highest_restart_per_stream_last_hour'] = stream_restarts_last_hour
        for stream_id in self.stream_list:
            if self.stream_list[stream_id]['status'] == "running":
                result['active_streams'] += 1
            elif self.stream_list[stream_id]['status'] == "stopped":
                result['stopped_streams'] += 1
            elif self.stream_list[stream_id]['status'] == "restarting":
                result['restarting_streams'] += 1
            elif "crashed" in self.stream_list[stream_id]['status']:
                result['crashed_streams'] += 1
        if self.is_update_availabe() and is_update_available_unicorn_fy and is_update_available_check_command:
            result['update_msg'] = " Update available: UNICORN Binance WebSocket API, UnicornFy and " \
                                   "check_unicorn_monitoring_api!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif self.is_update_availabe() and is_update_available_unicorn_fy:
            result['update_msg'] = " Update available: UNICORN Binance WebSocket API and UnicornFy"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif self.is_update_availabe() and is_update_available_check_command:
            result['update_msg'] = " Update available: UNICORN Binance WebSocket API and check_unicorn_monitoring_api!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif is_update_available_unicorn_fy and is_update_available_check_command:
            result['update_msg'] = " Update available: UnicornFy and check_unicorn_monitoring_api!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif self.is_update_availabe():
            result['update_msg'] = " Update " + str(self.get_latest_version()) + " available!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif is_update_available_unicorn_fy:
            result['update_msg'] = " Update UnicornFy " + str(unicorn_fy.get_latest_version()) + " available!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif is_update_available_check_command:
            result['update_msg'] = " Update `check_unicorn_monitoring_api` " + \
                                   str(self.get_latest_version_check_command()) + " available!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1

        if result['highest_restart_per_stream_last_hour'] >= 10:
            result['status_text'] = "CRITICAL"
            result['return_code'] = 2
            result['status_msg'] = " Restart rate per stream last hour: " + \
                                   str(result['highest_restart_per_stream_last_hour'])
        elif result['crashed_streams'] > 0:
            result['status_text'] = "CRITICAL"
            result['return_code'] = 2
        elif result['highest_restart_per_stream_last_hour'] >= 3:
            result['status_text'] = "WARNING"
            result['return_code'] = 1
            result['status_msg'] = " Restart rate per stream last hour: " + \
                                   str(result['highest_restart_per_stream_last_hour'])

        # Perfdata
        result['average_receives_per_second'] = ((self.total_receives - self.monitoring_total_receives) /
                                                 time_period).__round__(2)
        result['average_speed_per_second'] = (((self.total_received_bytes - self.monitoring_total_received_bytes) /
                                               time_period) / 1024).__round__(2)
        result['total_received_mb'] = (self.get_total_received_bytes() / (1024 * 1024)).__round__(2)
        result['total_received_length'] = self.total_receives
        result['stream_buffer_items'] = str(self.get_stream_buffer_length())
        result['stream_buffer_mb'] = (self.get_stream_buffer_byte_size() / (1024 * 1024)).__round__(4)
        result['reconnects'] = self.get_reconnects()
        self.monitoring_total_receives = self.get_total_receives()
        self.monitoring_total_received_bytes = self.get_total_received_bytes()
        self.last_monitoring_check = result['timestamp']
        result['uptime'] = ((result['timestamp'] - self.start_time) / (60*60*24)).__round__(3)
        return result

    def get_reconnects(self):
        """
        Get the number of total reconnects

        :return: int
        """
        return self.reconnects

    def get_request_id(self):
        """
        Get a unique request ID

        :return: int
        """
        with self.request_id_lock:
            self.request_id += 1
            return self.request_id

    def get_start_time(self):
        """
        Get the start_time of the  BinanceWebSocketApiManager instance

        :return: timestamp
        """
        return self.start_time

    def get_stream_buffer_byte_size(self):
        """
        Get the current byte size of the stream_buffer

        :return: int
        """
        return sys.getsizeof(self.stream_buffer)

    def get_stream_buffer_length(self):
        """
        Get the current number of items in the stream_buffer

        :return: int
        """
        return len(self.stream_buffer)

    def get_stream_info(self, stream_id):
        """
        Get infos about a specific stream

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: set
        """
        current_timestamp = time.time()
        try:
            temp_stream_list = copy.deepcopy(self.stream_list)
        except RuntimeError:
            return self.get_stream_info(stream_id)
        if temp_stream_list[stream_id]['last_heartbeat'] is not None:
            temp_stream_list[stream_id]['seconds_to_last_heartbeat'] = \
                current_timestamp - self.stream_list[stream_id]['last_heartbeat']
        if temp_stream_list[stream_id]['has_stopped'] is not False:
            temp_stream_list[stream_id]['seconds_since_has_stopped'] = \
                int(current_timestamp) - int(self.stream_list[stream_id]['has_stopped'])
        try:
            self.stream_list[stream_id]['processed_receives_statistic'] = self.get_stream_statistic(stream_id)
        except ZeroDivisionError:
            pass
        return temp_stream_list[stream_id]

    def get_stream_subscriptions(self, stream_id, request_id=False):
        """
        Listing subscriptions

        This function is supported by CEX endpoints only!

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#listing-subscriptions

        :param stream_id: id of a stream
        :type stream_id: uuid
        :param request_id: id to use for the request
        :type request_id: int
        :return: bool
        """
        if request_id is False:
            request_id = self.get_request_id()
        if self.is_exchange_type('dex'):
            logging.error("BinanceWebSocketApiManager->get_stream_subscriptions(" + str(stream_id) + ", " +
                          str(request_id) + ") DEX websockets dont support the listing of subscriptions! Request not "
                          "sent!")
            return False
        elif self.is_exchange_type('cex'):
            payload = {"method": "LIST_SUBSCRIPTIONS",
                       "id": request_id}
            self.stream_list[stream_id]['payload'].append(payload)
            logging.debug("BinanceWebSocketApiManager->get_stream_subscriptions(" + str(stream_id) + ", " +
                          str(request_id) + ") payload added!")
            return True
        else:
            return False

    def get_stream_list(self):
        """
        Get a list of all streams

        :return: set
        """
        # get the stream list
        temp_stream_list = {}
        for stream_id in self.stream_list:
            temp_stream_list[stream_id] = self.get_stream_info(stream_id)
        return temp_stream_list

    def get_stream_receives_last_second(self, stream_id):
        """
        Get the number of receives of specific stream from the last seconds

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: int
        """
        last_second_timestamp = int(time.time()) - 1
        try:
            return self.stream_list[stream_id]['receives_statistic_last_second']['entries'][last_second_timestamp]
        except KeyError:
            return 0

    def get_stream_statistic(self, stream_id):
        """
        Get the statistic of a specific stream

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: set
        """
        stream_statistic = {'stream_receives_per_second': 0,
                            'stream_receives_per_minute': 0,
                            'stream_receives_per_hour': 0,
                            'stream_receives_per_day': 0,
                            'stream_receives_per_month': 0,
                            'stream_receives_per_year': 0}
        if self.stream_list[stream_id]['status'] == "running":
            stream_statistic['uptime'] = time.time() - self.stream_list[stream_id]['start_time']
        elif self.stream_list[stream_id]['status'] == "stopped":
            stream_statistic['uptime'] = self.stream_list[stream_id]['has_stopped'] - self.stream_list[stream_id]['start_time']
        elif "crashed" in self.stream_list[stream_id]['status']:
            stream_statistic['uptime'] = self.stream_list[stream_id]['has_stopped'] - self.stream_list[stream_id]['start_time']
        elif self.stream_list[stream_id]['status'] == "restarting":
            stream_statistic['uptime'] = time.time() - self.stream_list[stream_id]['start_time']
        else:
            stream_statistic['uptime'] = time.time() - self.stream_list[stream_id]['start_time']
        try:
            stream_receives_per_second = self.stream_list[stream_id]['processed_receives_total'] / stream_statistic['uptime']
        except ZeroDivisionError:
            stream_receives_per_second = 0
        stream_statistic['stream_receives_per_second'] = stream_receives_per_second
        if stream_statistic['uptime'] > 60:
            stream_statistic['stream_receives_per_minute'] = stream_receives_per_second * 60
        if stream_statistic['uptime'] > 60 * 60:
            stream_statistic['stream_receives_per_hour'] = stream_receives_per_second * 60 * 60
        if stream_statistic['uptime'] > 60 * 60 * 24:
            stream_statistic['stream_receives_per_day'] = stream_receives_per_second * 60 * 60 * 24
        if stream_statistic['uptime'] > 60 * 60 * 24 * 30:
            stream_statistic['stream_receives_per_month'] = stream_receives_per_second * 60 * 60 * 24 * 30
        if stream_statistic['uptime'] > 60 * 60 * 24 * 30 * 12:
            stream_statistic['stream_receives_per_year'] = stream_receives_per_second * 60 * 60 * 24 * 30 * 12
        return stream_statistic

    def get_total_received_bytes(self):
        """
        Get number of total received bytes

        :return: int
        """
        # how much bytes did we receive till now?
        return self.total_received_bytes

    def get_total_receives(self):
        """
        Get the number of total receives

        :return: int
        """
        return self.total_receives

    def get_version(self):
        """
        Get the package/module version

        :return: str
        """
        return self.version

    def get_websocket_uri_length(self, channels, markets):
        """
        Get the length of the generated websocket URI

        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :return: int
        """
        uri = self.create_websocket_uri(channels, markets)
        return len(uri)

    def increase_received_bytes_per_second(self, stream_id, size):
        """
        Add the amount of received bytes per second

        :param stream_id: id of a stream
        :type stream_id: uuid
        :param size: amount of bytes to add
        :type size: int
        """
        current_timestamp = int(time.time())
        try:
            if self.stream_list[stream_id]['transfer_rate_per_second']['bytes'][current_timestamp]:
                pass
        except KeyError:
            self.stream_list[stream_id]['transfer_rate_per_second']['bytes'][current_timestamp] = 0
        try:
            self.stream_list[stream_id]['transfer_rate_per_second']['bytes'][current_timestamp] += size
        except KeyError:
            pass

    def increase_processed_receives_statistic(self, stream_id):
        """
        Add the number of processed receives

        :param stream_id: id of a stream
        :type stream_id: uuid
        """
        current_timestamp = int(time.time())
        self.stream_list[stream_id]['processed_receives_total'] += 1
        try:
            self.stream_list[stream_id]['receives_statistic_last_second']['entries'][current_timestamp] += 1
        except KeyError:
            self.stream_list[stream_id]['receives_statistic_last_second']['entries'][current_timestamp] = 1
        with self.total_receives_lock:
            self.total_receives += 1

    def increase_reconnect_counter(self, stream_id):
        """
        Increase reconnect counter

        :param stream_id: id of a stream
        :type stream_id: uuid
        """
        self.stream_list[stream_id]['logged_reconnects'].append(time.time())
        self.stream_list[stream_id]['reconnects'] += 1
        with self.reconnects_lock:
            self.reconnects += 1

    def increase_transmitted_counter(self, stream_id):
        """
        Increase the counter of transmitted payloads
        :param stream_id: id of a stream
        :type stream_id: uuid
        """
        self.stream_list[stream_id]['processed_transmitted_total'] += 1
        with self.total_transmitted_lock:
            self.total_transmitted += 1

    def is_manager_stopping(self):
        """
        Returns `True` if the manager has a stop request, 'False' if not.

        :return: bool
        """
        if self.stop_manager_request is None:
            return False
        else:
            return True

    def is_exchange_type(self, exchange_type=False):
        """
        Check the exchange type!

        :param exchange_type: Valid types are `dex` and `cex`!
        :type exchange_type: str
        :return: bool
        """
        if exchange_type is False:
            return False
        if self.exchange == "binance.org" or \
                self.exchange == "binance.org-testnet":
            type = "dex"
        elif self.exchange == "binance.com" or \
            self.exchange == "binance.com-margin" or \
            self.exchange == "binance.com-futures" or \
            self.exchange == "binance.je" or \
            self.exchange == "binance.us":
            type = "cex"
        else:
            logging.CRITICAL("Can not determine exchange type in method unicorn_binance_websocket_api."
                             "is_exchange_type()")
            return False
        if type == exchange_type:
            return True
        else:
            return False

    def is_stop_request(self, stream_id):
        """
        Has a specific stream a stop_request?

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: bool
        """
        logging.debug("BinanceWebSocketApiManager->is_stop_request(" + str(stream_id) + ")")
        if self.stream_list[stream_id]['stop_request'] is True:
            return True
        elif self.is_manager_stopping():
            return True
        else:
            return False

    def is_update_availabe(self):
        """
        Is a new release of this package available?

        :return: bool
        """
        installed_version = self.get_version()
        if ".dev" in installed_version:
            installed_version = installed_version[:-4]
        if self.get_latest_version() == installed_version:
            return False
        elif self.get_latest_version() == "unknown":
            return False
        else:
            return True

    def is_update_availabe_check_command(self, check_command_version=False):
        """
        Is a new release of `check_unicorn_monitoring_api` available?

        :return: bool
        """
        installed_version = check_command_version
        latest_version = self.get_latest_version_check_command()
        if ".dev" in installed_version:
            installed_version = installed_version[:-4]
        if latest_version == installed_version:
            return False
        elif latest_version == "unknown":
            return False
        else:
            return True

    def is_websocket_uri_length_valid(self, channels, markets):
        """
        Is the websocket URI length valid?

        *** OBSOLETE SINCE SUBSCRIPTIONS ARE SEND VIA `send()` THROUGH THE WEBSOCKET!!! ***

        The length is always valid because subscriptions are not handled via URI anymore.

        To keep it compatible this method returns True from now on!

        Reason why we used this in the past:
        A test with https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/tools/test_max_websocket_uri_length.py
        indicates that the allowed max length of an URI to binance websocket server is 8004 characters.

        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :return: True
        """
        logging.info("is_websocket_uri_length_valid() is obsolete! DONT USE IT ANYMORE!")
        return True

    def pop_stream_data_from_stream_buffer(self):
        """
        Get oldest entry from stream_buffer and remove from stack (FIFO stack)

        :return: raw_stream_data (set) or False
        """
        try:
            stream_data = self.stream_buffer.pop(0)
            return stream_data
        except IndexError:
            return False

    def print_stream_info(self, stream_id, add_string=""):
        """
        Print all infos about a specific stream, helps debugging :)

        :param stream_id: id of a stream
        :type stream_id: uuid
        :param add_string: text to add to the output
        :type add_string: str
        :return: bool
        """
        restart_requests_row = ""
        binance_api_status_row = ""
        status_row = ""
        payload_row = ""
        dex_user_address_row = ""
        last_static_ping_listen_key = ""
        stream_info = self.get_stream_info(stream_id)
        if len(add_string) > 0:
            add_string = " " + str(add_string) + "\r\n"
        if len(self.stream_list[stream_id]['logged_reconnects']) > 0:
            logged_reconnects_row = "\r\n logged_reconnects: "
            row_prefix = ""
            for timestamp in self.stream_list[stream_id]['logged_reconnects']:
                logged_reconnects_row += row_prefix + \
                                         datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d, %H:%M:%S UTC')
                row_prefix = ", "
        else:
            logged_reconnects_row = ""
        if "running" in stream_info['status']:
            stream_row_color_prefix = "\033[1m\033[32m"
            stream_row_color_suffix = "\033[0m\r\n"
            for reconnect_timestamp in self.stream_list[stream_id]['logged_reconnects']:
                if (time.time() - reconnect_timestamp) < 2:
                    stream_row_color_prefix = "\033[1m\033[33m"
                    stream_row_color_suffix = "\033[0m\r\n"
            status_row = stream_row_color_prefix + " status: " + str(stream_info['status']) + stream_row_color_suffix
        elif "crashed" in stream_info['status']:
            stream_row_color_prefix = "\033[1m\033[31m"
            stream_row_color_suffix = "\033[0m\r\n"
            status_row = stream_row_color_prefix + " status: " + str(stream_info['status']) + stream_row_color_suffix
        elif "restarting" in stream_info['status']:
            stream_row_color_prefix = "\033[1m\033[33m"
            stream_row_color_suffix = "\033[0m\r\n"
            status_row = stream_row_color_prefix + " status: " + str(stream_info['status']) + stream_row_color_suffix
        elif "stopped" in stream_info['status']:
            stream_row_color_prefix = "\033[1m\033[33m"
            stream_row_color_suffix = "\033[0m\r\n"
            status_row = stream_row_color_prefix + " status: " + str(stream_info['status']) + stream_row_color_suffix
        else:
            stream_row_color_prefix = ""
            stream_row_color_suffix = ""
        try:
            if self.restart_requests[stream_id]['status']:
                restart_requests_row = " restart_request: " + self.restart_requests[stream_id]['status'] + "\r\n"
        except KeyError:
            pass

        if self.stream_list[stream_id]['markets'] == "!userData":
            last_static_ping_listen_key = " last_static_ping_listen_key: " + \
                                          str(self.stream_list[stream_id]['last_static_ping_listen_key']) + "\r\n"
            if self.binance_api_status['status_code'] == 200:
                binance_api_status_code = str(self.binance_api_status['status_code'])
            elif self.binance_api_status['status_code'] == 418:
                binance_api_status_code = "\033[1m\033[31m" + str(self.binance_api_status['status_code']) + "\033[0m"
            else:
                binance_api_status_code = "\033[1m\033[33m" + str(self.binance_api_status['status_code']) + "\033[0m"
            binance_api_status_row = " binance_api_status: used_weight=" + str(self.binance_api_status['weight']) + \
                                     ", status_code=" + str(binance_api_status_code) + " (last update " + \
                                     str(datetime.utcfromtimestamp(
                                         self.binance_api_status['timestamp']).strftime('%Y-%m-%d, %H:%M:%S UTC')) + \
                                     ")\r\n"
        current_receiving_speed = str(self.get_human_bytesize(self.get_current_receiving_speed(stream_id), "/s"))
        if self.stream_list[stream_id]["payload"]:
            payload_row = " payload: " + str(self.stream_list[stream_id]["payload"]) + "\r\n"
        if self.stream_list[stream_id]["dex_user_address"] is not False:
            dex_user_address_row = " user_address: " + str(self.stream_list[stream_id]["dex_user_address"]) + "\r\n"
        channels_len = len(stream_info['channels'])
        markets_len = len(stream_info['markets'])
        subscriptions = channels_len * markets_len
        try:
            uptime = self.get_human_uptime(stream_info['processed_receives_statistic']['uptime'])
            print("===============================================================================================\r\n"
                  " exchange:", str(self.stream_list[stream_id]['exchange']), "(lib " + str(self.version) + "-python_"
                  + platform.python_version() + ")\r\n" +
                  str(add_string) +
                  " stream_id:", str(stream_id), "\r\n" +
                  " channels (" + str(channels_len) + "):", str(stream_info['channels']), "\r\n" +
                  " markets (" + str(markets_len) + "):", str(stream_info['markets']), "\r\n" +
                  " subscriptions: " + str(subscriptions) + "\r\n" +
                  str(payload_row) +
                  str(status_row) +
                  str(dex_user_address_row) +
                  " start_time:", str(stream_info['start_time']), "\r\n"
                  " uptime:", str(uptime),
                  "since " + str(
                      datetime.utcfromtimestamp(stream_info['start_time']).strftime('%Y-%m-%d, %H:%M:%S UTC')) +
                  "\r\n" +
                  " reconnects:", str(stream_info['reconnects']), logged_reconnects_row, "\r\n" +
                  str(restart_requests_row) +
                  str(binance_api_status_row) +
                  str(last_static_ping_listen_key) +
                  " last_heartbeat:", str(stream_info['last_heartbeat']), "\r\n"
                  " seconds_to_last_heartbeat:", str(stream_info['seconds_to_last_heartbeat']), "\r\n"
                  " stop_request:", str(stream_info['stop_request']), "\r\n"
                  " has_stopped:", str(stream_info['has_stopped']), "\r\n"
                  " seconds_since_has_stopped:",
                  str(stream_info['seconds_since_has_stopped']), "\r\n"
                  " current_receiving_speed:", str(current_receiving_speed), "\r\n" +
                  " processed_receives:", str(stream_info['processed_receives_total']), "\r\n" +
                  " transmitted_payloads:", str(self.stream_list[stream_id]['processed_transmitted_total']), "\r\n" +
                  " stream_most_receives_per_second:",
                  str(stream_info['receives_statistic_last_second']['most_receives_per_second']), "\r\n"
                  " stream_receives_per_second:",
                  str(stream_info['processed_receives_statistic']['stream_receives_per_second'].__round__(3)), "\r\n"
                  " stream_receives_per_minute:",
                  str(stream_info['processed_receives_statistic']['stream_receives_per_minute'].__round__(3)), "\r\n"
                  " stream_receives_per_hour:",
                  str(stream_info['processed_receives_statistic']['stream_receives_per_hour'].__round__(3)), "\r\n"
                  " stream_receives_per_day:",
                  str(stream_info['processed_receives_statistic']['stream_receives_per_day'].__round__(3)), "\r\n"
                  "===============================================================================================\r\n")
        except KeyError:
            self.print_stream_info(stream_id)

    def print_summary(self, add_string=""):
        """
        Print an overview of all streams
        
        :param add_string: text to add to the output
        :type add_string: str
        """
        streams = len(self.stream_list)
        active_streams = 0
        crashed_streams = 0
        restarting_streams = 0
        stopped_streams = 0
        active_streams_row = ""
        restarting_streams_row = ""
        stopped_streams_row = ""
        all_receives_per_second = 0.0
        current_receiving_speed = 0
        streams_with_stop_request = 0
        stream_rows = ""
        crashed_streams_row = ""
        binance_api_status_row = ""
        received_bytes_per_x_row = ""
        streams_with_stop_request_row = ""
        stream_buffer_row = ""
        if len(add_string) > 0:
            add_string = " " + str(add_string) + "\r\n"
        for stream_id in self.stream_list:
            stream_row_color_prefix = ""
            stream_row_color_suffix = ""
            current_receiving_speed += self.get_current_receiving_speed(stream_id)
            stream_statistic = self.get_stream_statistic(stream_id)
            if self.stream_list[stream_id]['status'] == "running":
                active_streams += 1
                all_receives_per_second += stream_statistic['stream_receives_per_second']
                try:
                    if self.restart_requests[stream_id]['status'] == "restarted":
                        stream_row_color_prefix = "\033[1m\033[33m"
                        stream_row_color_suffix = "\033[0m"
                except KeyError:
                    pass
                try:
                    for reconnect_timestamp in self.stream_list[stream_id]['logged_reconnects']:
                        if (time.time() - reconnect_timestamp) < 1:
                            stream_row_color_prefix = "\033[1m\033[31m"
                            stream_row_color_suffix = "\033[0m"
                        elif (time.time() - reconnect_timestamp) < 2:
                            stream_row_color_prefix = "\033[1m\033[33m"
                            stream_row_color_suffix = "\033[0m"
                        elif (time.time() - reconnect_timestamp) < 4:
                            stream_row_color_prefix = "\033[1m\033[32m"
                            stream_row_color_suffix = "\033[0m"
                except KeyError:
                    pass
            elif self.stream_list[stream_id]['status'] == "stopped":
                stopped_streams += 1
                stream_row_color_prefix = "\033[1m\033[33m"
                stream_row_color_suffix = "\033[0m"
            elif self.stream_list[stream_id]['status'] == "restarting":
                restarting_streams += 1
                stream_row_color_prefix = "\033[1m\033[33m"
                stream_row_color_suffix = "\033[0m"
            elif "crashed" in self.stream_list[stream_id]['status']:
                crashed_streams += 1
                stream_row_color_prefix = "\033[1m\033[31m"
                stream_row_color_suffix = "\033[0m"
            stream_rows += stream_row_color_prefix + str(stream_id) + stream_row_color_suffix + " |" + \
                self.fill_up_space(14, self.get_stream_receives_last_second(stream_id)) + "|" + \
                self.fill_up_space(13, stream_statistic['stream_receives_per_second'].__round__(2)) + "|" + \
                self.fill_up_space(18, self.stream_list[stream_id]['receives_statistic_last_second']['most_receives_per_second']) \
                + "|" + stream_row_color_prefix + \
                self.fill_up_space(8, len(self.stream_list[stream_id]['logged_reconnects'])) + \
                stream_row_color_suffix + "\r\n "
            if self.is_stop_request(stream_id) is True and self.stream_list[stream_id]['status'] == "running":
                streams_with_stop_request += 1
        if streams_with_stop_request >= 1:
            stream_row_color_prefix = "\033[1m\033[33m"
            stream_row_color_suffix = "\033[0m"
            streams_with_stop_request_row = stream_row_color_prefix + " streams_with_stop_request: " + \
                                            str(streams_with_stop_request) + stream_row_color_suffix + "\r\n"
        if crashed_streams >= 1:
            stream_row_color_prefix = "\033[1m\033[31m"
            stream_row_color_suffix = "\033[0m"
            crashed_streams_row = stream_row_color_prefix + " crashed_streams: " + str(crashed_streams) \
                                  + stream_row_color_suffix + "\r\n"
        total_received_bytes = str(self.get_total_received_bytes()) + " (" + str(
            self.get_human_bytesize(self.get_total_received_bytes())) + ")"
        try:
            received_bytes_per_second = self.get_total_received_bytes() / (time.time() - self.start_time)
            received_bytes_per_x_row += str((received_bytes_per_second / 1024).__round__(2)) + " kB/s (per day " + \
                                        str(((received_bytes_per_second / 1024 / 1024 / 1024) * 60 * 60 * 24).__round__(2)) + " gB)"
            if self.get_stream_buffer_length() > 50:
                stream_row_color_prefix = "\033[1m\033[34m"
                stream_row_color_suffix = "\033[0m"
                stream_buffer_row += stream_row_color_prefix + " stream_buffer_stored_items: " + str(self.get_stream_buffer_length()) + "\r\n"
                stream_buffer_row += " stream_buffer_byte_size: " + str(self.get_stream_buffer_byte_size()) + \
                                     " (" + str(
                    self.get_human_bytesize(self.get_stream_buffer_byte_size())) + ")" + stream_row_color_suffix + "\r\n"

            if active_streams > 0:
                active_streams_row = " \033[1m\033[32mactive_streams: " + str(active_streams) + "\033[0m\r\n"
            if restarting_streams > 0:
                restarting_streams_row = " \033[1m\033[33mrestarting_streams: " + str(restarting_streams) + "\033[0m\r\n"
            if stopped_streams > 0:
                stopped_streams_row = " \033[1m\033[33mstopped_streams: " + str(stopped_streams) + "\033[0m\r\n"
            if self.binance_api_status['weight'] is not None:
                if self.binance_api_status['status_code'] == 200:
                    binance_api_status_code = str(self.binance_api_status['status_code'])
                elif self.binance_api_status['status_code'] == 418:
                    binance_api_status_code = "\033[1m\033[31m" + str(self.binance_api_status['status_code']) + "\033[0m"
                else:
                    binance_api_status_code = "\033[1m\033[33m" + str(self.binance_api_status['status_code']) + "\033[0m"
                binance_api_status_row = " binance_api_status: used_weight=" + str(self.binance_api_status['weight']) + \
                                         ", status_code=" + str(binance_api_status_code) + " (last update " + \
                                         str(datetime.utcfromtimestamp(
                                             self.binance_api_status['timestamp']).strftime('%Y-%m-%d, %H:%M:%S UTC')) + \
                                         ")\r\n"
            try:
                print(
                    "===============================================================================================\r\n" +
                    " exchange:", str(self.stream_list[stream_id]['exchange']), "(lib " + str(self.version) + "-python_"
                                                                                + platform.python_version() + ")\r\n" +
                    " uptime:", str(self.get_human_uptime(time.time() - self.start_time)), "since " +
                    str(datetime.utcfromtimestamp(self.start_time).strftime('%Y-%m-%d, %H:%M:%S UTC')) + "\r\n" +
                    " streams:", str(streams), "\r\n" +
                    str(active_streams_row) +
                    str(crashed_streams_row) +
                    str(restarting_streams_row) +
                    str(stopped_streams_row) +
                    str(streams_with_stop_request_row) +
                    str(stream_buffer_row) +
                    " current_receiving_speed:", str(self.get_human_bytesize(current_receiving_speed, "/s")), "\r\n" +
                    " total_receives:", str(self.total_receives), "\r\n"
                    " total_received_bytes:", str(total_received_bytes), "\r\n"
                    " total_receiving_speed:", str(received_bytes_per_x_row), "\r\n" +
                    " total_transmitted_payloads:", str(self.total_transmitted), "\r\n" +
                    str(binance_api_status_row) +
                    str(add_string) +
                    " ---------------------------------------------------------------------------------------------\r\n"
                    "              stream_id               | rec_last_sec | rec_per_sec | most_rec_per_sec | recon\r\n"
                    " ---------------------------------------------------------------------------------------------\r\n"
                    " " + str(stream_rows) +
                    "---------------------------------------------------------------------------------------------\r\n"
                    " all_streams                          |" +
                    self.fill_up_space(14, self.get_all_receives_last_second()) + "|" +
                    self.fill_up_space(13, all_receives_per_second.__round__(2)) + "|" +
                    self.fill_up_space(18, self.most_receives_per_second) + "|" +
                    self.fill_up_space(8, self.reconnects) + "\r\n"
                    "===============================================================================================\r\n")
            except UnboundLocalError:
                pass
        except ZeroDivisionError:
            pass

    def replace_stream(self, stream_id, new_channels, new_markets):
        """
        Replace a stream

        If you want to start a stream with a new config, its recommended, to first start a new stream with the new
        settings and close the old stream not before the new stream received its first data. So your data will stay
        consistent.

        :param stream_id: id of the old stream
        :type stream_id: uuid
        :param new_channels: the new channel list for the stream
        :type new_channels: str, tuple, list, set
        :param new_markets: the new markets list for the stream
        :type new_markets: str, tuple, list, set
        :return: new stream_id
        """
        # starting a new socket and stop the old stream not before the new stream received its first record
        new_stream_id = self.create_stream(new_channels, new_markets)
        if self.wait_till_stream_has_started(new_stream_id):
            self.stop_stream(stream_id)
        return new_stream_id

    def restart_stream(self, stream_id):
        """
        Restart a specific stream

        :param stream_id: id of a stream
        :type stream_id: uuid

        :return: stream_id
        """
        logging.info("BinanceWebSocketApiManager->restart_stream(" + str(self.stream_list[stream_id]['channels']) +
                     ", " + str(self.stream_list[stream_id]['markets']) + ")")
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self._create_stream_thread, args=(loop, stream_id,
                                                                           self.stream_list[stream_id]['channels'],
                                                                           self.stream_list[stream_id]['markets'],
                                                                           True))
        thread.start()
        return stream_id

    def run(self):
        """
        This method overloads `threading.run()` and starts management threads
        """
        thread_frequent_checks = threading.Thread(target=self._frequent_checks)
        thread_frequent_checks.start()
        thread_keepalive_streams = threading.Thread(target=self._keepalive_streams)
        thread_keepalive_streams.start()
        time.sleep(5)
        while self.stop_manager_request is None:
            if self._keepalive_streams_restart_request is True:
                self._keepalive_streams_restart_request = None
                thread_keepalive_streams = threading.Thread(target=self._keepalive_streams)
                thread_keepalive_streams.start()
            if self._frequent_checks_restart_request is True:
                self._frequent_checks_restart_request = None
                thread_frequent_checks = threading.Thread(target=self._frequent_checks)
                thread_frequent_checks.start()
            time.sleep(0.2)
        sys.exit(0)

    def set_private_api_config(self, binance_api_key, binance_api_secret):
        """
        Set binance_api_key and binance_api_secret

        This settings are needed to acquire a listenKey from Binance to establish a userData stream

        :param binance_api_key: The Binance API key
        :type binance_api_key: str
        :param binance_api_secret: The Binance API secret
        :type binance_api_secret: str
        """
        self.api_key = binance_api_key
        self.api_secret = binance_api_secret

    def set_private_dex_config(self, binance_dex_user_address):
        """
        Set binance_dex_user_address

        Is going to be the default user_address, once the websocket is created with this default value, its not possible
        to change it. If you plan to use different user_address its recommended to not use this method! Just provide the
        user_address with create_stream() in the market parameter.

        :param binance_dex_user_address: Binance DEX user address
        :type binance_dex_user_address: str
        """
        self.dex_user_address = binance_dex_user_address

    def set_heartbeat(self, stream_id):
        """
        Set heartbeat for a specific thread (should only be done by the stream itself)


        """
        logging.debug("BinanceWebSocketApiManager->set_heartbeat(" + str(stream_id) + ")")
        try:
            self.stream_list[stream_id]['last_heartbeat'] = time.time()
            self.stream_list[stream_id]['status'] = "running"
        except KeyError:
            pass

    def set_keep_max_received_last_second_entries(self, number_of_max_entries):
        """
        Set how much received_last_second entries are stored till they get deleted!

        :param number_of_max_entries: number of entries to keep in list
        :type number_of_max_entries: int
        """
        self.keep_max_received_last_second_entries = number_of_max_entries

    def set_restart_request(self, stream_id):
        """
        Set a restart request for a specific stream

        :param stream_id: id of the old stream
        :type stream_id: uuid
        """
        self.restart_requests[stream_id] = {'status': "new"}

    def split_payload(self, params, method, max_items_per_request=350):
        """
        Sending more than 8000 chars via websocket.send() leads to a connection loss, 350 list elements is a good limit
        to keep the payload length under 8000 chars and avoid reconnects

        :param params: params of subscribe payload
        :type params: str
        :param method: SUBSCRIBE or UNSUBSCRIBE
        :type method: str
        :param max_items_per_request: max size for params, if more it gets splitted
        :return: list or False
        """
        if self.is_exchange_type('cex'):
            count_items = 0
            add_params = []
            payload = []
            for param in params:
                add_params.append(param)
                count_items += 1
                if count_items > max_items_per_request:
                    add_payload = {"method": method,
                                   "params": add_params,
                                   "id": self.get_request_id()}
                    payload.append(add_payload)
                    count_items = 0
                    add_params = []
            if len(add_params) > 0:
                add_payload = {"method": method,
                               "params": add_params,
                               "id": self.get_request_id()}
                payload.append(add_payload)
                return payload
            else:
                return False
        elif self.is_exchange_type('dex'):
            pass
        else:
            return False

    def start_monitoring_api(self, host='127.0.0.1', port=64201, warn_on_update=True):
        """
        Start the monitoring API server

        :param host: listening ip address, use 0.0.0.0 or a specific address (default: 127.0.0.1)
        :type host: str
        :param port: listening port number (default: 64201)
        :type port: int
        :param warn_on_update: set to `False` to disable the update warning
        :type warn_on_update: bool
        """
        thread = threading.Thread(target=self._start_monitoring_api_thread, args=(host, port, warn_on_update))
        thread.start()

    def stop_manager_with_all_streams(self):
        """
        Stop the BinanceWebSocketApiManager with all streams and management threads
        """
        logging.info("Stopping unicorn_binance_websocket_api_manager " + self.version + " ...")
        # send signal to all threads
        self.stop_manager_request = True
        # delete listenKeys
        for stream_id in self.stream_list:
            self.stop_stream(stream_id)
        # stop monitoring API services
        self.stop_monitoring_api()

    def stop_monitoring_api(self):
        """
        Stop the monitoring API service
        """
        try:
            if not isinstance(self.monitoring_api_server, bool):
                self.monitoring_api_server.stop()
        except AttributeError as error_msg:
            logging.debug("can not execute self.monitoring_api_server.stop() - info: " + str(error_msg))

    def stop_stream(self, stream_id):
        """
        Stop a specific stream

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: bool
        """
        # stop a specific stream by stream_id
        logging.info("BinanceWebSocketApiManager->stop_stream(" + str(stream_id) + ")")
        try:
            del self.restart_requests[stream_id]
        except KeyError:
            pass
        self.stream_list[stream_id]['stop_request'] = True

    def stream_is_crashing(self, stream_id, error_msg=False):
        """
        If a stream can not heal itself in cause of wrong parameter (wrong market, channel type) it calls this method

        :param stream_id: id of a stream
        :type stream_id: uuid
        :param error_msg: Error msg to add to the stream status!
        :type error_msg: str
        """
        logging.critical("BinanceWebSocketApiManager->stream_is_crashing(" + str(stream_id) + ")")
        self.stream_list[stream_id]['has_stopped'] = time.time()
        self.stream_list[stream_id]['status'] = "crashed"
        if error_msg:
            self.stream_list[stream_id]['status'] += " - " + str(error_msg)

    def stream_is_stopping(self, stream_id):
        """
        Streams report with this call their shutdowns

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return:
        """
        logging.debug("BinanceWebSocketApiManager->stream_is_stopping(" + str(stream_id) + ")")
        self.stream_list[stream_id]['has_stopped'] = time.time()
        self.stream_list[stream_id]['status'] = "stopped"

    def subscribe_to_stream(self, stream_id, channels=[], markets=[]):
        """
        Subscribe channels and/or markets to an existing stream

        If you provide one channel and one market, then every subscribed market is going to get added to the new channel
        and all subscribed channels are going to get added to the new market!

        How are the parameter `channels` and `markets` used with subscriptions:
        https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream

        :param stream_id: id of a stream
        :type stream_id: uuid
        :param channels: provide the channels you wish to stream
        :type channels: str, tuple, list, set
        :param markets: provide the markets you wish to stream
        :type markets: str, tuple, list, set
        :return: bool
        """
        logging.debug("BinanceWebSocketApiManager->subscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                      ", " + str(markets) + ") started ...")
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        if type(channels) is set:
            channels = list(channels)
        if type(markets) is set:
            markets = list(markets)
        if type(self.stream_list[stream_id]['channels']) is str:
            self.stream_list[stream_id]['channels'] = [self.stream_list[stream_id]['channels']]
        if type(self.stream_list[stream_id]['markets']) is str:
            self.stream_list[stream_id]['markets'] = [self.stream_list[stream_id]['markets']]
        if type(self.stream_list[stream_id]['channels']) is set:
            self.stream_list[stream_id]['channels'] = list(self.stream_list[stream_id]['channels'])
        if type(self.stream_list[stream_id]['markets']) is set:
            self.stream_list[stream_id]['markets'] = list(self.stream_list[stream_id]['markets'])

        self.stream_list[stream_id]['channels'] = list(set(self.stream_list[stream_id]['channels'] + channels))
        self.stream_list[stream_id]['markets'] = list(set(self.stream_list[stream_id]['markets'] + markets))
        payload = self.create_payload(stream_id, "subscribe",
                                      channels=self.stream_list[stream_id]['channels'],
                                      markets=self.stream_list[stream_id]['markets'])
        for item in payload:
            self.stream_list[stream_id]['payload'].append(item)
        logging.debug("BinanceWebSocketApiManager->subscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                      ", " + str(markets) + ") finished ...")
        return True

    def unsubscribe_from_stream(self, stream_id, channels=[], markets=[]):
        """
        Unsubscribe channels and/or markets to an existing stream

        If you provide one channel and one market, then all subscribed markets from the specific channel and all
        subscribed markets from the specific channel are going to be removed!

        How are the parameter `channels` and `markets` used with subscriptions:
        https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream

        :param stream_id: id of a stream
        :type stream_id: uuid
        :param channels: provide the channels you wish to stream
        :type channels: str, tuple, list, set
        :param markets: provide the markets you wish to stream
        :type markets: str, tuple, list, set
        :return: bool
        """
        logging.debug("BinanceWebSocketApiManager->unsubscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                      ", " + str(markets) + ") started ...")
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        if type(self.stream_list[stream_id]['channels']) is str:
            self.stream_list[stream_id]['channels'] = [self.stream_list[stream_id]['channels']]
        if type(self.stream_list[stream_id]['markets']) is str:
            self.stream_list[stream_id]['markets'] = [self.stream_list[stream_id]['markets']]
        for channel in channels:
            try:
                self.stream_list[stream_id]['channels'].remove(channel)
            except ValueError:
                pass
        for market in markets:
            if re.match(r'[a-zA-Z0-9]{41,43}', market) is None:
                try:
                    self.stream_list[stream_id]['markets'].remove(market)
                except ValueError:
                    pass
        payload = self.create_payload(stream_id, "unsubscribe",
                                      channels=channels, markets=markets)
        for item in payload:
            self.stream_list[stream_id]['payload'].append(item)
        logging.debug("BinanceWebSocketApiManager->unsubscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                      ", " + str(markets) + ") finished ...")
        return True

    def wait_till_stream_has_started(self, stream_id):
        """
        Returns `True` as soon a specific stream has started

        :param stream_id: id of a stream
        :type stream_id: uuid

        :return: True
        """
        # will return `True` as soon the stream received the first data row
        while self.stream_list[stream_id]['last_heartbeat'] is None:
            time.sleep(0.2)
        else:
            return True

    def wait_till_stream_has_stopped(self, stream_id):
        """
        Returns `True` as soon a specific stream has stopped itself

        :param stream_id: id of a stream
        :type stream_id: uuid

        :return: True
        """
        while self.stream_list[stream_id]['has_stopped'] is False:
            time.sleep(0.2)
        else:
            return True
