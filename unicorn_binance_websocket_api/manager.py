#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/manager.py
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

from unicorn_binance_websocket_api.connection_settings import CEX_EXCHANGES, DEX_EXCHANGES, CONNECTION_SETTINGS
from unicorn_binance_websocket_api.exceptions import StreamRecoveryError, UnknownExchange
from unicorn_binance_websocket_api.restclient import BinanceWebSocketApiRestclient
from unicorn_binance_websocket_api.restserver import BinanceWebSocketApiRestServer
from unicorn_binance_websocket_api.sockets import BinanceWebSocketApiSocket
from unicorn_binance_websocket_api.api import BinanceWebSocketApiApi
from cheroot import wsgi
from collections import deque
from datetime import datetime
from flask import Flask, redirect
from flask_restful import Api
from operator import itemgetter
from typing import Optional, Union
try:
    # python <=3.7 support
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import asyncio
import colorama
import copy
import logging
import hmac
import hashlib
import os
import platform
import psutil
import re
import requests
import ssl
import sys
import threading
import time
import traceback
import uuid
import ujson as json
import websockets

logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiManager(threading.Thread):
    """
    An unofficial Python API to use the Binance Websocket API`s (com+testnet, com-margin+testnet,
    com-isolated_margin+testnet, com-futures+testnet, us, dex/chain+testnet) in a easy, fast, flexible,
    robust and fully-featured way.

    This library supports two different kind of websocket endpoints:

        - CEX (Centralized exchange): binance.com, binance.vision, binance.je, binance.us, trbinance.com

        - DEX (Decentralized exchange): binance.org

    Binance.com websocket API documentation:

        - https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md

        - https://binance-docs.github.io/apidocs/futures/en/#user-data-streams

        - https://binance-docs.github.io/apidocs/spot/en/#user-data-streams

    Binance.vision (Testnet) websocket API documentation:

        - https://testnet.binance.vision/

    Binance.us websocket API documentation:

        - https://docs.binance.us/#introduction

    TRBinance.com websocket API documentation:

        - https://www.trbinance.com/apidocs/#general-wss-information

    Binance.org websocket API documentation:

        - https://docs.binance.org/api-reference/dex-api/ws-connection.html

    :param process_stream_data: Provide a function/method to process the received webstream data (callback). The function
                                will be called instead of
                                `add_to_stream_buffer() <unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_buffer>`_
                                like `process_stream_data(stream_data, stream_buffer_name)` where
                                `stream_data` cointains the raw_stream_data. If not provided, the raw stream_data will
                                get stored in the stream_buffer or provided to a specific callback function of
                                `create_stream()`! `How to read from stream_buffer!
                                <https://unicorn-binance-websocket-api.docs.lucit.tech/README.html#and-4-more-lines-to-print-the-receives>`_
    :type process_stream_data: function
    :param exchange: Select binance.com, binance.com-testnet, binance.com-margin, binance.com-margin-testnet,
                     binance.com-isolated_margin, binance.com-isolated_margin-testnet, binance.com-futures,
                     binance.com-futures-testnet, binance.com-coin_futures, binance.us, trbinance.com,
                     binance.org, binance.org-testnet (default: binance.com)
    :type exchange: str
    :param warn_on_update: set to `False` to disable the update warning of UBWA and also in UBRA used as submodule.
    :type warn_on_update: bool
    :param throw_exception_if_unrepairable: set to `True` to activate exceptions if a crashed stream is unrepairable
                                            (invalid API key, exceeded subscription limit) or an unknown exchange is
                                            used
    :type throw_exception_if_unrepairable: bool
    :param restart_timeout: A stream restart must be successful within this time, otherwise a new restart will be
                            initialized. Default is 6 seconds.
    :type restart_timeout: int
    :param show_secrets_in_logs: set to True to show secrets like listen_key, api_key or api_secret in log file
                                 (default=False)
    :type show_secrets_in_logs: bool
    :param output_default: set to "dict" to convert the received raw data to a python dict, set to "UnicornFy" to
                           convert with `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_ -  otherwise
                           with the default setting "raw_data" the output remains unchanged and gets delivered as
                           received from the endpoints. Change this for a specific stream with the `output` parameter
                           of `create_stream()` and `replace_stream()`
    :type output_default: str
    :param enable_stream_signal_buffer: set to True to enable the
                                        `stream_signal_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signal_buffer%60>`_
                                        and receive information about
                                        disconnects and reconnects to manage a restore of the lost data during the
                                        interruption or to recognize your bot got blind.
    :type enable_stream_signal_buffer: bool
    :param disable_colorama: set to True to disable the use of `colorama <https://pypi.org/project/colorama/>`_
    :type disable_colorama: bool
    :param stream_buffer_maxlen: Set a max len for the generic `stream_buffer`. This parameter can also be used within
                                 `create_stream()` for a specific `stream_buffer`.
    :type stream_buffer_maxlen: int or None
    :param process_stream_signals: Provide a function/method to process the received stream signals. The function is running inside an asyncio loop and will be 
                                   called instead of 
                                   `add_to_stream_signal_buffer() <unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_signal_buffer>`_
                                   like `process_stream_data(signal_type=False, stream_id=False, data_record=False)`.
    :type process_stream_signals: function
    :param close_timeout_default: The `close_timeout` parameter defines a maximum wait time in seconds for
                                completing the closing handshake and terminating the TCP connection.
                                This parameter is passed through to the `websockets.client.connect()
                                <https://websockets.readthedocs.io/en/stable/topics/design.html?highlight=close_timeout#closing-handshake>`_
    :type close_timeout_default: int
    :param ping_interval_default: Once the connection is open, a `Ping frame` is sent every
                                `ping_interval` seconds. This serves as a keepalive. It helps keeping
                                the connection open, especially in the presence of proxies with short
                                timeouts on inactive connections. Set `ping_interval` to `None` to
                                disable this behavior.
                                This parameter is passed through to the `websockets.client.connect()
                                <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websock ets>`_
    :type ping_interval_default: int
    :param ping_timeout_default: If the corresponding `Pong frame` isn't received within
                               `ping_timeout` seconds, the connection is considered unusable and is closed with
                               code 1011. This ensures that the remote endpoint remains responsive. Set
                               `ping_timeout` to `None` to disable this behavior.
                               This parameter is passed through to the `websockets.client.connect()
                               <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_timeout#keepalive-in-websockets>`_
    :type ping_timeout_default: int
    :param high_performance: Set to True makes `create_stream()` a non-blocking function
    :type high_performance:  bool
    :param debug: If True the lib adds additional information to logging outputs
    :type debug:  bool
    :param restful_base_uri: Override `restful_base_uri`. Example: `https://127.0.0.1`
    :type restful_base_uri:  str
    :param websocket_base_uri: Override `websocket_base_uri`. Example: `ws://127.0.0.1:8765/`
    :type websocket_base_uri:  str
    :param websocket_api_base_uri: Override `websocket_api_base_uri`. Example: `ws://127.0.0.1:8765/`
    :type websocket_api_base_uri:  str
    :param max_subscriptions_per_stream: Override the `max_subscriptions_per_stream` value. Example: 1024
    :type max_subscriptions_per_stream:  int
    :param exchange_type: Override the exchange type. Valid options are: 'cex', 'dex'
    :type exchange_type:  str
    :param socks5_proxy_server: Set this to activate the usage of a socks5 proxy. Example: '127.0.0.1:9050'
    :type socks5_proxy_server:  str
    :param socks5_proxy_user: Set this to activate the usage of a socks5 proxy user. Example: 'alice'
    :type socks5_proxy_user:  str
    :param socks5_proxy_pass: Set this to activate the usage of a socks5 proxy password.
    :type socks5_proxy_pass:  str
    :param socks5_proxy_ssl_verification: Set to `False` to disable SSL server verification. Default is `True`.
    :type socks5_proxy_ssl_verification:  bool
    """

    def __init__(self,
                 process_stream_data=False,
                 exchange: str = "binance.com",
                 warn_on_update: Optional[bool] = True,
                 throw_exception_if_unrepairable: Optional[bool] = False,
                 restart_timeout: int = 6,
                 show_secrets_in_logs: Optional[bool] = False,
                 output_default: Optional[Literal['dict', 'raw_data', 'UnicornFy']] = "raw_data",
                 enable_stream_signal_buffer: Optional[bool] = False,
                 disable_colorama: Optional[bool] = False,
                 stream_buffer_maxlen: Optional[int] = None,
                 process_stream_signals=False,
                 close_timeout_default: int = 1,
                 ping_interval_default: int = 5,
                 ping_timeout_default: int = 10,
                 high_performance: Optional[bool] = False,
                 debug: Optional[bool] = False,
                 restful_base_uri: Optional[str] = None,
                 websocket_base_uri: Optional[str] = None,
                 websocket_api_base_uri: Optional[str] = None,
                 max_subscriptions_per_stream: Optional[int] = None,
                 exchange_type: Optional[Literal['cex', 'dex']] = None,
                 socks5_proxy_server: Optional[str] = None,
                 socks5_proxy_user: Optional[str] = None,
                 socks5_proxy_pass: Optional[str] = None,
                 socks5_proxy_ssl_verification: Optional[bool] = True,):
        threading.Thread.__init__(self)
        self.name = "unicorn-binance-websocket-api"
        self.version = "1.46.2"
        logger.info(f"New instance of {self.get_user_agent()} on "
                    f"{str(platform.system())} {str(platform.release())} for exchange {exchange} started ...")
        self.debug = debug
        logger.info(f"Debug is {self.debug}")
        if disable_colorama is not True:
            logger.info(f"Initiating `colorama_{colorama.__version__}`")
            colorama.init()
        logger.info(f"Using `websockets_{websockets.__version__}`")
        self.specific_process_stream_data = {}

        if process_stream_data is False:
            # no special method to process stream data provided, so we use add_to_stream_buffer:
            self.process_stream_data = self.add_to_stream_buffer
            logger.info(f"Using `stream_buffer`")
        else:
            # use the provided method to process stream data:
            self.process_stream_data = process_stream_data
            logger.info(f"Using `process_stream_data`")

        if process_stream_signals is False:
            # no special method to process stream signals provided, so we use add_to_stream_signal_buffer:
            self.process_stream_signals = self.add_to_stream_signal_buffer
            logger.info(f"Using `stream_signal_buffer`")
        else:
            # use the provided method to process stream signals:
            self.process_stream_signals = process_stream_signals
            logger.info(f"Using `process_stream_signals` ...")
        self.enable_stream_signal_buffer = enable_stream_signal_buffer
        if self.enable_stream_signal_buffer is True:
            logger.info(f"Enabled `stream_signal_buffer` ...")

        if exchange not in CONNECTION_SETTINGS:
            error_msg = f"Unknown exchange '{str(exchange)}'! List of supported exchanges: " \
                        f"https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/" \
                        f"Binance-websocket-endpoint-configuration-overview"
            logger.critical(error_msg)
            raise UnknownExchange(error_msg)

        self.exchange = exchange
        self.max_subscriptions_per_stream = max_subscriptions_per_stream or CONNECTION_SETTINGS[self.exchange][0]
        self.websocket_base_uri = websocket_base_uri or CONNECTION_SETTINGS[self.exchange][1]
        self.websocket_api_base_uri = websocket_api_base_uri or CONNECTION_SETTINGS[self.exchange][2]
        self.restful_base_uri = restful_base_uri
        self.exchange_type = exchange_type
        if not self.exchange_type:
            if self.exchange in DEX_EXCHANGES:
                self.exchange_type = "dex"
            elif self.exchange in CEX_EXCHANGES:
                self.exchange_type = "cex"
            else:
                logger.critical(f"BinanceWebSocketApiManager.is_exchange_type() - Can not determine exchange type for"
                                f"exchange={str(self.exchange)}, resetting to default 'cex'")
                self.exchange_type = "cex"
        logger.info(f"Using exchange_type '{self.exchange_type}' ...")

        self.socks5_proxy_server = socks5_proxy_server
        if socks5_proxy_server is None:
            self.socks5_proxy_address = None
            self.socks5_proxy_user: Optional[str] = None
            self.socks5_proxy_pass: Optional[str] = None
            self.socks5_proxy_port = None
        else:
            # Prepare Socks Proxy usage
            self.socks5_proxy_ssl_verification = socks5_proxy_ssl_verification
            self.socks5_proxy_user = socks5_proxy_user
            self.socks5_proxy_pass = socks5_proxy_pass
            self.socks5_proxy_address, self.socks5_proxy_port = socks5_proxy_server.split(":")
            websocket_ssl_context = ssl.SSLContext()
            if self.socks5_proxy_ssl_verification is False:
                websocket_ssl_context.verify_mode = ssl.CERT_NONE
                websocket_ssl_context.check_hostname = False
            self.websocket_ssl_context = websocket_ssl_context

        self.stop_manager_request = None
        self.all_subscriptions_number = 0
        self.binance_api_status = {'weight': None,
                                   'timestamp': 0,
                                   'status_code': None}
        self.dex_user_address = False
        self.event_loops = {}
        self.frequent_checks_list = {}
        self.frequent_checks_list_lock = threading.Lock()
        self.receiving_speed_average = 0
        self.receiving_speed_peak = {'value': 0,
                                     'timestamp': time.time()}
        self.high_performance = high_performance
        self.keep_max_received_last_second_entries = 5
        self.keepalive_streams_list = {}
        self.last_entry_added_to_stream_buffer = 0
        self.last_monitoring_check = time.time()
        self.last_update_check_github = {'timestamp': time.time(),
                                         'status': None}
        self.last_update_check_github['status']: dict = None
        self.last_update_check_github_check_command = {'timestamp': time.time(),
                                                       'status': None}
        self.max_send_messages_per_second = 5
        self.max_send_messages_per_second_reserve = 2
        self.most_receives_per_second = 0
        self.monitoring_api_server = False
        self.monitoring_total_received_bytes = 0
        self.monitoring_total_receives = 0
        self.output_default = output_default
        self.process_response = {}
        self.process_response_lock = threading.Lock()
        self.reconnects = 0
        self.reconnects_lock = threading.Lock()
        self.request_id = 0
        self.request_id_lock = threading.Lock()
        self.restart_requests = {}
        self.restart_timeout = restart_timeout
        self.return_response = {}
        self.return_response_lock = threading.Lock()
        self.ringbuffer_error = []
        self.ringbuffer_error_max_size = 500
        self.ringbuffer_result = []
        self.ringbuffer_result_max_size = 500
        self.show_secrets_in_logs = show_secrets_in_logs
        self.start_time = time.time()
        self.stream_buffer_maxlen = stream_buffer_maxlen
        self.stream_buffer = deque(maxlen=self.stream_buffer_maxlen)
        self.stream_buffer_lock = threading.Lock()
        self.stream_buffer_locks = {}
        self.stream_buffers = {}
        self.stream_list = {}
        self.stream_list_lock = threading.Lock()
        self.stream_signal_buffer = deque()
        self.stream_signal_buffer_lock = threading.Lock()
        self.socket_is_ready = {}
        self.stream_threads = {}
        self.stream_threading_lock = {}
        self.throw_exception_if_unrepairable = throw_exception_if_unrepairable
        self.total_received_bytes = 0
        self.total_received_bytes_lock = threading.Lock()
        self.total_receives = 0
        self.total_receives_lock = threading.Lock()
        self.total_transmitted = 0
        self.total_transmitted_lock = threading.Lock()
        self.websocket_list = {}
        self.close_timeout_default = close_timeout_default
        self.ping_interval_default = ping_interval_default
        self.ping_timeout_default = ping_timeout_default
        self.start()
        self.replacement_text = "***SECRET_REMOVED***"
        self.api = BinanceWebSocketApiApi(manager=self)
        self.restclient = BinanceWebSocketApiRestclient(manager=self)
        self.warn_on_update = warn_on_update
        if warn_on_update and self.is_update_available():
            update_msg = f"Release {self.name}_" + self.get_latest_version() + " is available, " \
                         f"please consider updating! (Changelog: " \
                         f"https://unicorn-binance-websocket-api.docs.lucit.tech/CHANGELOG.html)"
            print(update_msg)
            logger.warning(update_msg)

    def _add_stream_to_stream_list(self,
                                   stream_id,
                                   channels,
                                   markets,
                                   stream_label=None,
                                   stream_buffer_name=False,
                                   api_key=False,
                                   api_secret=False,
                                   symbols=False,
                                   output=False,
                                   ping_interval=None,
                                   ping_timeout=None,
                                   close_timeout=None,
                                   stream_buffer_maxlen=None,
                                   api=False,
                                   process_stream_data=None):
        """
        Create a list entry for new streams

        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: str
        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :param stream_label: provide a stream_label for the stream
        :type stream_label: str
        :param stream_buffer_name: If `False` the data is going to get written to the default stream_buffer,
                                   set to `True` to read the data via `pop_stream_data_from_stream_buffer(stream_id)` or
                                   provide a string to create and use a shared stream_buffer and read it via
                                   `pop_stream_data_from_stream_buffer('string')`.
        :type stream_buffer_name: bool or str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param symbols: provide the symbols for isolated_margin user_data streams
        :type symbols: str
        :param output: the default setting `raw_data` can be globaly overwritten with the parameter
                       `output_default <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=output_default#module-unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager>`_
                       of BinanceWebSocketApiManager`. To overrule the `output_default` value for this specific stream,
                       set `output` to "dict" to convert the received raw data to a python dict,  set to "UnicornFy" to
                       convert with `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_ -  otherwise with
                       the default setting "raw_data" the output remains unchanged and gets delivered as received from
                       the endpoints
        :type output: str
        :param ping_interval: Once the connection is open, a `Ping frame` is sent every
                              `ping_interval` seconds. This serves as a keepalive. It helps keeping
                              the connection open, especially in the presence of proxies with short
                              timeouts on inactive connections. Set `ping_interval` to `None` to
                              disable this behavior. (default: 20)
                              This parameter is passed through to the `websockets.client.connect()
                              <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`_
        :type ping_interval: int or None
        :param ping_timeout: If the corresponding `Pong frame` isn't received within
                             `ping_timeout` seconds, the connection is considered unusable and is closed with
                             code 1011. This ensures that the remote endpoint remains responsive. Set
                             `ping_timeout` to `None` to disable this behavior. (default: 20)
                             This parameter is passed through to the `websockets.client.connect()
                             <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`_
        :type ping_timeout: int or None
        :param close_timeout: The `close_timeout` parameter defines a maximum wait time in seconds for
                              completing the closing handshake and terminating the TCP connection. (default: 10)
                              This parameter is passed through to the `websockets.client.connect()
                              <https://websockets.readthedocs.io/en/stable/topics/design.html?highlight=close_timeout#closing-handshake>`_
        :type close_timeout: int or None
        :param stream_buffer_maxlen: Set a max len for the `stream_buffer`. Only used in combination with a non generic
                                     `stream_buffer`. The generic `stream_buffer` uses always the value of
                                     `BinanceWebSocketApiManager()`.
        :type stream_buffer_maxlen: int or None
        :param api: Setting this to `True` activates the creation of a Websocket API stream to send API requests via Websocket.
                    Needs `api_key` and `api_secret` in combination. This type of stream can not be combined with a UserData
                    stream or an other public endpoint. (Default is `False`)
        :type api: bool
        :param process_stream_data: Provide a function/method to process the received webstream data. The function
                            will be called instead of
                            `add_to_stream_buffer() <unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_buffer>`_
                            like `process_stream_data(stream_data, stream_buffer_name)` where
                            `stream_data` cointains the raw_stream_data. If not provided, the raw stream_data will
                            get stored in the stream_buffer! `How to read from stream_buffer!
                            <https://unicorn-binance-websocket-api.docs.lucit.tech/README.html#and-4-more-lines-to-print-the-receives>`_
        :type process_stream_data: function
        """
        output = output or self.output_default
        close_timeout = close_timeout or self.close_timeout_default
        ping_interval = ping_interval or self.ping_interval_default
        ping_timeout = ping_timeout or self.ping_timeout_default
        self.specific_process_stream_data[stream_id] = process_stream_data
        self.stream_threading_lock[stream_id] = {'full_lock': threading.Lock(),
                                                 'receives_statistic_last_second_lock': threading.Lock()}
        self.stream_list[stream_id] = {'exchange': self.exchange,
                                       'stream_id': copy.deepcopy(stream_id),
                                       'recent_socket_id': None,
                                       'channels': copy.deepcopy(channels),
                                       'markets': copy.deepcopy(markets),
                                       'stream_label': copy.deepcopy(stream_label),
                                       'stream_buffer_name': copy.deepcopy(stream_buffer_name),
                                       'stream_buffer_maxlen': copy.deepcopy(stream_buffer_maxlen),
                                       'symbols': copy.deepcopy(symbols),
                                       'output': copy.deepcopy(output),
                                       'subscriptions': 0,
                                       'payload': [],
                                       'api': copy.deepcopy(api),
                                       'api_key': copy.deepcopy(api_key),
                                       'api_secret': copy.deepcopy(api_secret),
                                       'dex_user_address': copy.deepcopy(self.dex_user_address),
                                       'ping_interval': copy.deepcopy(ping_interval),
                                       'ping_timeout': copy.deepcopy(ping_timeout),
                                       'close_timeout': copy.deepcopy(close_timeout),
                                       'status': 'starting',
                                       'start_time': time.time(),
                                       'processed_receives_total': 0,
                                       'receives_statistic_last_second': {'most_receives_per_second': 0, 'entries': {}},
                                       'seconds_to_last_heartbeat': None,
                                       'last_heartbeat': None,
                                       'stop_request': None,
                                       'crash_request': None,
                                       'kill_request': None,
                                       'seconds_since_has_stopped': None,
                                       'has_stopped': False,
                                       'reconnects': 0,
                                       'last_stream_signal': None,
                                       'logged_reconnects': [],
                                       'processed_transmitted_total': 0,
                                       'last_static_ping_listen_key': 0,
                                       'listen_key': False,
                                       'listen_key_cache_time':  10 * 60,
                                       'last_received_data_record': None,
                                       'processed_receives_statistic': {},
                                       'transfer_rate_per_second': {'bytes': {}, 'speed': 0},
                                       'websocket_uri': None}
        logger.info("BinanceWebSocketApiManager._add_stream_to_stream_list(" +
                    str(stream_id) + ", " + str(channels) + ", " + str(markets) + ", " + str(stream_label) + ", "
                    + str(stream_buffer_name) + ", " + str(stream_buffer_maxlen) + ", " + str(symbols) + ")")

    def _create_stream_thread(self,
                              loop,
                              stream_id,
                              channels,
                              markets,
                              stream_buffer_name=False,
                              stream_buffer_maxlen=None,
                              restart=False):
        """
        Co function of self.create_stream to create a thread for the socket and to manage the coroutine

        :param loop: provide a asynio loop
        :type loop: asyncio loop
        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: str
        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :param stream_buffer_name: If `False` the data is going to get written to the default stream_buffer,
                           set to `True` to read the data via `pop_stream_data_from_stream_buffer(stream_id)` or
                           provide a string to create and use a shared stream_buffer and read it via
                           `pop_stream_data_from_stream_buffer('string')`.
        :type stream_buffer_name: bool or str
        :param stream_buffer_maxlen: Set a max len for the `stream_buffer`. Only used in combination with a non generic
                                     `stream_buffer`. The generic `stream_buffer` uses always the value of
                                     `BinanceWebSocketApiManager()`.
        :type stream_buffer_maxlen: int or None
        :param restart: set to `True`, if it's a restart!
        :type restart: bool
        :return:
        """
        if self.is_stop_request(stream_id):
            return False
        if restart is False:
            if stream_buffer_name is not False:
                self.stream_buffer_locks[stream_buffer_name] = threading.Lock()
                try:
                    # Not resetting the stream_buffer during a restart:
                    if self.stream_buffers[stream_buffer_name]:
                        pass
                except KeyError:
                    # Resetting
                    self.stream_buffers[stream_buffer_name] = deque(maxlen=stream_buffer_maxlen)
        asyncio.set_event_loop(loop)
        socket = BinanceWebSocketApiSocket(self, stream_id, channels, markets)
        try:
            loop.run_until_complete(socket.start_socket())
        except RuntimeError as error_msg:
            if "cannot schedule new futures after interpreter shutdown" in str(error_msg):
                logger.critical(f"BinanceWebSocketApiManager._create_stream_thread() stream_id={str(stream_id)} "
                                f" - RuntimeError `error: 11` - error_msg:  {str(error_msg)} - Info: https://github.com/"
                                f"LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/299")
                self.stop_manager_with_all_streams()
                sys.exit(1)
            elif "This event loop is already running" in str(error_msg):
                logger.critical(f"BinanceWebSocketApiManager._create_stream_thread() stream_id={str(stream_id)} "
                                f" - RuntimeError - error_msg:  {str(error_msg)}")
            else:
                logger.critical(f"BinanceWebSocketApiManager._create_stream_thread() stream_id={str(stream_id)} "
                                f" - RuntimeError `error: 7` - error_msg: {str(error_msg)} - Please create an issue: "
                                f"https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues"
                                f"/new/choose")
        finally:
            try:
                if self.stream_list[stream_id]['last_stream_signal'] is not None and \
                        self.stream_list[stream_id]['last_stream_signal'] != "DISCONNECT":
                    self.process_stream_signals("DISCONNECT", stream_id)
                    self.stream_list[stream_id]['last_stream_signal'] = "DISCONNECT"
            except KeyError as error_msg:
                logger.debug(f"BinanceWebSocketApiManager._create_stream_thread() stream_id={str(stream_id)} - "
                             f"KeyError `error: 12` - {error_msg}")
            loop.close()
            self.set_socket_is_ready(stream_id)

    def generate_signature(self, api_secret=None, data=None):
        """
        Signe the request.

        :param api_secret:
        :param data:

        :return:
        """
        ordered_data = self.order_params(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    @staticmethod
    def order_params(data):
        """
        Convert params to list with signature as last element

        :param data:
        :return:

        """
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def _frequent_checks(self):
        """
        This method gets started as a thread and is doing the frequent checks
        """
        frequent_checks_id = time.time()
        cpu_usage_time = False
        with self.frequent_checks_list_lock:
            self.frequent_checks_list[frequent_checks_id] = {'last_heartbeat': 0,
                                                             'stop_request': None,
                                                             'has_stopped': False}
        logger.info("BinanceWebSocketApiManager._frequent_checks() new instance created with frequent_checks_id=" +
                    str(frequent_checks_id))
        # threaded loop for min 1 check per second
        while self.stop_manager_request is None and self.frequent_checks_list[frequent_checks_id]['stop_request'] \
                is None:
            with self.frequent_checks_list_lock:
                self.frequent_checks_list[frequent_checks_id]['last_heartbeat'] = time.time()
            time.sleep(0.3)
            current_timestamp = int(time.time())
            last_timestamp = current_timestamp - 1
            next_to_last_timestamp = current_timestamp - 2
            total_most_stream_receives_last_timestamp = 0
            total_most_stream_receives_next_to_last_timestamp = 0
            active_stream_list = self.get_active_stream_list()
            # check CPU stats
            cpu = self.get_process_usage_cpu()
            if cpu >= 95:
                time_of_waiting = 5
                if cpu_usage_time is False:
                    cpu_usage_time = time.time()
                elif (time.time() - cpu_usage_time) > time_of_waiting:
                    logger.warning(f"BinanceWebSocketApiManager._frequent_checks() - High CPU usage since "
                                   f"{str(time_of_waiting)} seconds: {str(cpu)}")
                    cpu_usage_time = False
            else:
                cpu_usage_time = False
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
                    if len(self.stream_list[stream_id]['receives_statistic_last_second']['entries']) > \
                            self.keep_max_received_last_second_entries:
                        with self.stream_threading_lock[stream_id]['receives_statistic_last_second_lock']:
                            temp_entries = copy.deepcopy(self.stream_list[stream_id]['receives_statistic_last_second']['entries'])
                        for timestamp_key in temp_entries:
                            try:
                                if timestamp_key < current_timestamp - self.keep_max_received_last_second_entries:
                                    delete_index.append(timestamp_key)
                            except ValueError as error_msg:
                                logger.error("BinanceWebSocketApiManager._frequent_checks() timestamp_key=" +
                                             str(timestamp_key) + " current_timestamp=" + str(current_timestamp) +
                                             " keep_max_received_last_second_entries=" +
                                             str(self.keep_max_received_last_second_entries) + " error_msg=" +
                                             str(error_msg))
                    for timestamp_key in delete_index:
                        with self.stream_threading_lock[stream_id]['receives_statistic_last_second_lock']:
                            self.stream_list[stream_id]['receives_statistic_last_second']['entries'].pop(timestamp_key,
                                                                                                         None)
                    # transfer_rate_per_second
                    delete_index = []
                    if len(self.stream_list[stream_id]['transfer_rate_per_second']['bytes']) > \
                            self.keep_max_received_last_second_entries:
                        try:
                            temp_bytes = self.stream_list[stream_id]['transfer_rate_per_second']['bytes']
                            for timestamp_key in temp_bytes:
                                try:
                                    if timestamp_key < current_timestamp - self.keep_max_received_last_second_entries:
                                        delete_index.append(timestamp_key)
                                except ValueError as error_msg:
                                    logger.error(
                                        "BinanceWebSocketApiManager._frequent_checks() timestamp_key="
                                        + str(timestamp_key) +
                                        " current_timestamp=" + str(current_timestamp) +
                                        " keep_max_received_last_second_"
                                        "entries=" + str(self.keep_max_received_last_second_entries) + " error_msg=" +
                                        str(error_msg))
                        except RuntimeError as error_msg:
                            logger.info("BinanceWebSocketApiManager._frequent_checks() - "
                                        "Catched RuntimeError: " + str(error_msg))
                    for timestamp_key in delete_index:
                        self.stream_list[stream_id]['transfer_rate_per_second']['bytes'].pop(timestamp_key, None)
            # set most_receives_per_second
            try:
                if int(self.most_receives_per_second) < int(total_most_stream_receives_last_timestamp):
                    self.most_receives_per_second = int(total_most_stream_receives_last_timestamp)
            except ValueError as error_msg:
                logger.error("BinanceWebSocketApiManager._frequent_checks() self.most_receives_per_second"
                             "=" + str(self.most_receives_per_second) + " total_most_stream_receives_last_timestamp"
                             "=" + str(total_most_stream_receives_last_timestamp) + " total_most_stream_receives_next_"
                             "to_last_timestamp=" + str(total_most_stream_receives_next_to_last_timestamp) + " error_"
                             "msg=" + str(error_msg))
            # check receiving_speed_peak
            last_second_receiving_speed = self.get_current_receiving_speed_global()
            try:
                if last_second_receiving_speed > self.receiving_speed_peak['value']:
                    self.receiving_speed_peak['value'] = last_second_receiving_speed
                    self.receiving_speed_peak['timestamp'] = time.time()
                    logger.info(f"BinanceWebSocketApiManager._frequent_checks() - reached new "
                                f"`highest_receiving_speed` "
                                f"{str(self.get_human_bytesize(self.receiving_speed_peak['value'], '/s'))} at "
                                f"{self.get_date_of_timestamp(self.receiving_speed_peak['timestamp'])}")
            except TypeError:
                pass
            # send keepalive for `!userData` streams every 30 minutes
            if active_stream_list:
                for stream_id in active_stream_list:
                    if isinstance(active_stream_list[stream_id]['markets'], str):
                        active_stream_list[stream_id]['markets'] = [active_stream_list[stream_id]['markets'], ]
                    if isinstance(active_stream_list[stream_id]['channels'], str):
                        active_stream_list[stream_id]['channels'] = [active_stream_list[stream_id]['channels'], ]
                    if active_stream_list[stream_id]['api'] is False:
                        if "!userData" in active_stream_list[stream_id]['markets'] or \
                                "!userData" in active_stream_list[stream_id]['channels']:
                            if (active_stream_list[stream_id]['start_time'] +
                                active_stream_list[stream_id]['listen_key_cache_time']) < time.time() and \
                                    (active_stream_list[stream_id]['last_static_ping_listen_key'] +
                                     active_stream_list[stream_id]['listen_key_cache_time']) < time.time():
                                # keep-alive the listenKey
                                self.restclient.keepalive_listen_key(stream_id)
                                # set last_static_ping_listen_key
                                self.stream_list[stream_id]['last_static_ping_listen_key'] = time.time()
                                self.set_heartbeat(stream_id)
                                logger.info("BinanceWebSocketApiManager._frequent_checks() - sent listen_key keepalive "
                                            "ping for stream_id=" + str(stream_id))
        sys.exit(0)

    def _handle_task_result(self, task: asyncio.Task) -> None:
        """
        This method is a callback for `loop.create_task()` to retrive the task exception and avoid the `Task exception
        was never retrieved` traceback on stdout:
        https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/261
        """
        try:
            task.result()
        except asyncio.CancelledError:
            logger.debug(f"BinanceWebSocketApiManager._handle_task_result() - asyncio.CancelledError raised by task "
                         f"= {task}")
        except SystemExit as error_code:
            logger.debug(f"BinanceWebSocketApiManager._handle_task_result() - SystemExit({error_code}) raised by task "
                         f"= {task}")
        except Exception as error_msg:
            logger.critical(f"BinanceWebSocketApiManager._handle_task_result() - Exception({error_msg}) raised by task "
                            f"= {task}")

    def _keepalive_streams(self):
        """
        This method is started as a thread and is observing the streams, if neccessary it restarts a dead stream
        """
        keepalive_streams_id = time.time()
        self.keepalive_streams_list[keepalive_streams_id] = {'last_heartbeat': 0,
                                                             'stop_request': None,
                                                             'has_stopped': False}
        logger.info("BinanceWebSocketApiManager._keepalive_streams() new instance created with "
                    "keepalive_streams_id=" + str(keepalive_streams_id))
        # threaded loop to restart crashed streams:
        while self.stop_manager_request is None and \
                self.keepalive_streams_list[keepalive_streams_id]['stop_request'] is None:
            time.sleep(1)
            self.keepalive_streams_list[keepalive_streams_id]['last_heartbeat'] = time.time()
            # restart streams with a restart_request (status == new)
            try:
                temp_restart_requests = copy.deepcopy(self.restart_requests)
            except RuntimeError as error_msg:
                if "dictionary changed size during iteration" in error_msg:
                    continue
                else:
                    raise RuntimeError(error_msg)
            for stream_id in temp_restart_requests:
                try:
                    # find restarts that didn't work
                    if self.restart_requests[stream_id]['status'] == "restarted" and \
                            self.restart_requests[stream_id]['last_restart_time']+self.restart_timeout < time.time():
                        self.restart_requests[stream_id] = {'status': "new",
                                                            'initiated': None}
                    # restart streams with requests
                    if self.restart_requests[stream_id]['status'] == "new" or \
                            self.stream_list[stream_id]['kill_request'] is not None:
                        self.kill_stream(stream_id)
                        if self.restart_requests[stream_id]['initiated'] is None or \
                                self.restart_requests[stream_id]['initiated']+5 < time.time():
                            self.restart_requests[stream_id]['initiated'] = time.time()
                            thread = threading.Thread(target=self._restart_stream_thread,
                                                      args=(stream_id,),
                                                      name=f"_restart_stream_thread:  stream_id={stream_id}, "
                                                           f"time={time.time()}")
                            thread.start()
                except KeyError:
                    pass
        sys.exit(0)

    def _restart_stream(self, stream_id):
        """
        This is NOT stop/start! Its purpose is to start a died stream again! Use `set_restart_request()` for stop/start!

        :param stream_id: id of a stream
        :type stream_id: str

        :return: stream_id or False
        """
        try:
            if self.restart_requests[stream_id]['status'] != "new":
                logger.warning("BinanceWebSocketApiManager._restart_stream() please use `set_restart_request()` "
                               "instead!")
                return False
        except KeyError:
            # no restart_request entry for this stream_id:
            logger.warning("BinanceWebSocketApiManager._restart_stream() please use `set_restart_request() instead!")
            return False
        logger.info("BinanceWebSocketApiManager._restart_stream(" + str(stream_id) + ", " +
                    str(self.stream_list[stream_id]['channels']) +
                    ", " + str(self.stream_list[stream_id]['markets']) + f"){self.get_debug_log()}")
        self.restart_requests[stream_id] = {'status': "restarted"}
        self.restart_requests[stream_id]['last_restart_time'] = time.time()
        self.stream_list[stream_id]['status'] = "restarting"
        self.stream_list[stream_id]['kill_request'] = None
        self.stream_list[stream_id]['payload'] = []
        loop = asyncio.new_event_loop()
        self.set_socket_is_not_ready(stream_id)
        try:
            thread = threading.Thread(target=self._create_stream_thread,
                                      args=(loop,
                                            stream_id,
                                            self.stream_list[stream_id]['channels'],
                                            self.stream_list[stream_id]['markets'],
                                            self.stream_list[stream_id]['stream_buffer_name'],
                                            self.stream_list[stream_id]['stream_buffer_maxlen'],
                                            True),
                                      name=f"_create_stream_thread: stream_id={stream_id}, time={time.time()}")
            thread.start()
        except OSError as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.create_stream({str(stream_id)}) - OSError - {error_msg}")
        self.stream_threads[stream_id] = thread
        while self.socket_is_ready[stream_id] is False and self.high_performance is False:
            # This loop will wait till the thread and the asyncio init is ready. This avoids two possible errors as
            # described here: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/131
            logger.debug(f"BinanceWebSocketApiManager.create_stream({str(stream_id)}) - Waiting till new socket and "
                         f"asyncio is ready")
            time.sleep(1)
        return stream_id

    def _restart_stream_thread(self, stream_id):
        """
        Wait till the old socket has closed and then start it again

        :param stream_id: id of a stream
        :type stream_id: str
        """
        try:
            logger.debug(f"BinanceWebSocketApiManager._restart_stream_thread({stream_id}, "
                         f"{self.stream_list[stream_id]['channels']}, {self.stream_list[stream_id]['markets']}) "
                         f"{self.get_debug_log()}")
        except KeyError as error_msg:
            logger.error(f"BinanceWebSocketApiManager._restart_stream_thread({stream_id}) - KeyError {error_msg} - "
                         f"restart canceled!{self.get_debug_log()}")
            self.restart_requests[stream_id]['status'] = "canceled"
            return False
        self._restart_stream(stream_id)
        return True

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
        logger.info("BinanceWebSocketApiManager._start_monitoring_api_thread() - Starting monitoring API service ...")
        app = Flask(__name__)

        @app.route('/')
        @app.route('/status/')
        def redirect_to_wiki():
            logger.info("BinanceWebSocketApiManager._start_monitoring_api_thread() 200 - "
                        "Visit https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/UNICORN-"
                        "Monitoring-API-Service for further information!")
            return redirect("https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/"
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
            logger.critical("BinanceWebSocketApiManager._start_monitoring_api_thread() - Monitoring API service is "
                            "going down! - Info: " + str(error_msg))
        except OSError as error_msg:
            logger.critical("BinanceWebSocketApiManager._start_monitoring_api_thread() - Monitoring API service is "
                            "going down! - Info: " + str(error_msg))

    def add_payload_to_stream(self, stream_id=None, payload: dict = None):
        """
        Add a payload to a stream by `stream_id`.

        :param stream_id: id of a stream
        :type stream_id: str
        :param payload: The payload in JSON to add.
        :type payload: dict
        :return: bool
        """
        if payload is None or stream_id is None:
            return False
        else:
            self.stream_list[stream_id]['payload'].append(payload)
            return True

    def add_to_ringbuffer_error(self, error):
        """
        Add received error messages from websocket endpoints to the error ringbuffer

        :param error: The data to add.
        :type error: string
        :return: bool
        """
        while len(self.ringbuffer_error) >= self.get_ringbuffer_error_max_size():
            self.ringbuffer_error.pop(0)
        self.ringbuffer_error.append(str(error))
        return True

    def add_to_ringbuffer_result(self, result):
        """
        Add received result messages from websocket endpoints to the result ringbuffer

        :param result: The data to add.
        :type result: string
        :return: bool
        """
        while len(self.ringbuffer_result) >= self.get_ringbuffer_result_max_size():
            self.ringbuffer_result.pop(0)
        self.ringbuffer_result.append(str(result))
        return True

    def add_to_stream_buffer(self, stream_data, stream_buffer_name=False):
        """
        Kick back data to the
        `stream_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_buffer%60>`_


        If it is not possible to process received stream data (for example, the database is restarting, so it's not
        possible to save the data), you can return the data back into the stream_buffer. After a few seconds you stopped
        writing data back to the stream_buffer, the BinanceWebSocketApiManager starts flushing back the data to normal
        processing.

        :param stream_data: the data you want to write back to the buffer
        :type stream_data: raw stream_data or unicorn_fied stream data
        :param stream_buffer_name: If `False` the data is going to get written to the default stream_buffer,
                                   set to `True` to read the data via `pop_stream_data_from_stream_buffer(stream_id)` or
                                   provide a string to create and use a shared stream_buffer and read it via
                                   `pop_stream_data_from_stream_buffer('string')`.
        :type stream_buffer_name: bool or str
        :return: bool
        """
        if stream_buffer_name is False:
            with self.stream_buffer_lock:
                self.stream_buffer.append(stream_data)
        else:
            with self.stream_buffer_locks[stream_buffer_name]:
                self.stream_buffers[stream_buffer_name].append(stream_data)
        self.last_entry_added_to_stream_buffer = time.time()
        return True

    def add_to_stream_signal_buffer(self, signal_type=False, stream_id=False, data_record=False):
        """
        Add signals about a stream to the
        `stream_signal_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signal_buffer%60>`_

        :param signal_type: "CONNECT", "DISCONNECT" or "FIRST_RECEIVED_DATA"
        :type signal_type: str
        :param stream_id: id of a stream
        :type stream_id: str
        :param data_record: The last or first received data record
        :type data_record: str or dict
        :return: bool
        """
        if self.enable_stream_signal_buffer:
            stream_signal = {'type': signal_type,
                             'stream_id': stream_id,
                             'timestamp': time.time()}
            if signal_type == "CONNECT":
                # nothing to add ...
                pass
            elif signal_type == "DISCONNECT":
                try:
                    stream_signal['last_received_data_record'] = self.stream_list[stream_id]['last_received_data_record']
                except KeyError as error_msg:
                    logger.critical(f"BinanceWebSocketApiManager.add_to_stream_signal_buffer({signal_type}) - "
                                    f"Cant determine last_received_data_record! - error_msg: {error_msg}")
                    stream_signal['last_received_data_record'] = None
            elif signal_type == "FIRST_RECEIVED_DATA":
                stream_signal['first_received_data_record'] = data_record
            else:
                logger.error(f"BinanceWebSocketApiManager.add_to_stream_signal_buffer({signal_type}) - "
                             f"Received invalid `signal_type`!")
                return False
            with self.stream_signal_buffer_lock:
                self.stream_signal_buffer.append(stream_signal)
            logger.info(f"BinanceWebSocketApiManager.add_to_stream_signal_buffer({stream_signal})")
            return True
        else:
            return False

    def add_total_received_bytes(self, size):
        """
        Add received bytes to the total received bytes statistic

        :param size: int value of added bytes
        :type size: int
        """
        with self.total_received_bytes_lock:
            self.total_received_bytes += int(size)

    def clear_stream_buffer(self, stream_buffer_name=False):
        """
        Clear the
        `stream_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_buffer%60>`_

        :param stream_buffer_name: `False` to read from generic stream_buffer, the stream_id if you used True in
                                   create_stream() or the string name of a shared stream_buffer.
        :type stream_buffer_name: bool or str
        :return: bool
        """
        if stream_buffer_name is False:
            try:
                self.stream_buffer.clear()
                return True
            except IndexError:
                return False
        else:
            try:
                with self.stream_buffer_locks[stream_buffer_name]:
                    self.stream_buffers[stream_buffer_name].clear()
                return True
            except IndexError:
                return False
            except KeyError:
                return False

    def create_payload(self, stream_id, method, channels=False, markets=False):
        """
        Create the payload for subscriptions

        :param stream_id: provide a stream_id
        :type stream_id: str
        :param method: `SUBSCRIBE` or `UNSUBSCRIBE`
        :type method: str
        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :return: payload (list) or False
        """
        logger.info("BinanceWebSocketApiManager.create_payload(" + str(stream_id) + ", " + str(channels) + ", " +
                    str(markets) + ") started ...")
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        payload = []
        if self.is_exchange_type("dex"):
            if method == "subscribe" and channels is not False:
                for channel in channels:
                    add_payload = {"method": method,
                                   "topic": channel}
                    symbols = []
                    if channel == "allMiniTickers" or \
                            channel == "allTickers" or \
                            channel == "blockheight":
                        add_payload["symbols"] = ["$all"]
                        payload.append(add_payload)
                        continue
                    if markets:
                        for market in markets:
                            if market == "allMiniTickers" or \
                                    market == "allTickers" or \
                                    market == "blockheight":
                                add_payload_from_market = {"method": method,
                                                           "topic": market,
                                                           "symbols": ["$all"]}
                                payload.append(add_payload_from_market)
                                continue
                            elif re.match(r'[a-zA-Z0-9]{41,43}', market) is not None:
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
                logger.critical("BinanceWebSocketApiManager.create_payload(" + str(stream_id) + ", "
                                + str(channels) + ", " + str(markets) + ") - Allowed values for `method`: `subscribe` "
                                "or `unsubscribe`!")
                return False
        elif self.is_exchange_type("cex"):
            final_market = "@arr"
            if markets:
                for market in markets:
                    if "arr@" in market:
                        final_market = "@" + market
            final_channel = "@arr"
            if channels:
                for channel in channels:
                    if "arr@" in channel:
                        final_channel = "@" + channel
            if method == "subscribe":
                params = []
                for channel in channels:
                    if "!" in channel:
                        params.append(channel + final_market)
                        continue
                    else:
                        for market in markets:
                            if "!" in market:
                                params.append(market + final_channel)
                            else:
                                params.append(market.lower() + "@" + channel)
                if len(params) > 0:
                    params = list(set(params))
                    payload = self.split_payload(params, "SUBSCRIBE")
            elif method == "unsubscribe":
                if markets:
                    params = []
                    try:
                        for channel in self.stream_list[stream_id]['channels']:
                            if "!" in channel:
                                params.append(channel + final_market)
                            else:
                                for market in markets:
                                    params.append(market.lower() + "@" + channel)
                        if len(params) > 0:
                            payload = self.split_payload(params, "UNSUBSCRIBE")
                    except KeyError:
                        pass
                if channels:
                    params = []
                    for market in self.stream_list[stream_id]['markets']:
                        if "!" in market:
                            params.append(market + final_channel)
                        else:
                            for channel in channels:
                                params.append(market.lower() + "@" + channel)
                    if len(params) > 0:
                        payload = self.split_payload(params, "UNSUBSCRIBE")
            else:
                logger.critical("BinanceWebSocketApiManager.create_payload(" + str(stream_id) + ", "
                                + str(channels) + ", " + str(markets) + ") - Allowed values for `method`: `subscribe` "
                                "or `unsubscribe`!")
                return False
        logger.info("BinanceWebSocketApiManager.create_payload(" + str(stream_id) + ", "
                    + str(channels) + ", " + str(markets) + ") - Payload: " + str(payload))
        logger.info("BinanceWebSocketApiManager.create_payload(" + str(stream_id) + ", " + str(channels) + ", " +
                    str(markets) + ") finished ...")
        return payload

    def create_stream(self,
                      channels=[],
                      markets=[],
                      stream_label=None,
                      stream_buffer_name=False,
                      api_key=False,
                      api_secret=False,
                      symbols=False,
                      output=False,
                      ping_interval=None,
                      ping_timeout=None,
                      close_timeout=None,
                      stream_buffer_maxlen=None,
                      api=False,
                      process_stream_data=None):
        """
        Create a websocket stream

        If you provide 2 markets and 2 channels, then you are going to create 4 subscriptions (markets * channels).

            Example:

                channels = ['trade', 'kline_1']

                markets = ['bnbbtc', 'ethbtc']

                Finally:  bnbbtc@trade, ethbtc@trade, bnbbtc@kline_1, ethbtc@kline_1

        `There is a subscriptions limit per stream!
        <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/Binance-websocket-endpoint-configuration-overview>`_

        Create `!userData` streams as single streams, because it's using a different endpoint and can not get combined
        with other streams in a multiplexed stream!

            Example CEX:

                ``binance_websocket_api_manager.create_stream(["arr"], ["!userData"], api_key="aaa", api_secret="bbb")``

                Isolated Margin:

                ``binance_websocket_api_manager.create_stream(["arr"], ["!userData"], api_key="aaa", api_secret="bbb", symbols="ankrbtc")``

            Example DEX:

                ``binance_websocket_api_manager.create_stream(['orders', 'transfers', 'accounts'], binance_dex_user_address)``

        To create a multiplexed stream which includes also `!miniTicker@arr`, `!ticker@arr`, `!forceOrder@arr` or
        `!bookTicker@arr` you just need to add `!bookTicker` to the channels list - dont add `arr` (cex) or `$all`
        (dex) to the markets list.

            Example:

                ``binance_websocket_api_manager.create_stream(['kline_5m', 'marketDepth', '!miniTicker'], ['bnbbtc'])``

        But you have to add `arr` or `$all` if you want to start it as a single stream!

            Example:

                ``binance_websocket_api_manager.create_stream(["arr"], ["!miniTicker"])``

        :param channels: provide the channels you wish to stream
        :type channels: str, tuple, list, set
        :param markets: provide the markets you wish to stream
        :type markets: str, tuple, list, set
        :param stream_label: provide a stream_label to identify the stream
        :type stream_label: str
        :param stream_buffer_name: If `False` the data is going to get written to the default stream_buffer,
                                   set to `True` to read the data via `pop_stream_data_from_stream_buffer(stream_id)` or
                                   provide a string to create and use a shared stream_buffer and read it via
                                   `pop_stream_data_from_stream_buffer('string')`.
        :type stream_buffer_name: bool or str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param symbols: provide the symbols for isolated_margin user_data streams
        :type symbols: str
        :param output: the default setting `raw_data` can be globaly overwritten with the parameter
                       `output_default <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=output_default#module-unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager>`_
                       of BinanceWebSocketApiManager`. To overrule the `output_default` value for this specific stream,
                       set `output` to "dict" to convert the received raw data to a python dict,  set to "UnicornFy" to
                       convert with `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_ -  otherwise with
                       the default setting "raw_data" the output remains unchanged and gets delivered as received from
                       the endpoints
        :type output: str
        :param ping_interval: Once the connection is open, a `Ping frame` is sent every
                              `ping_interval` seconds. This serves as a keepalive. It helps keeping
                              the connection open, especially in the presence of proxies with short
                              timeouts on inactive connections. Set `ping_interval` to `None` to
                              disable this behavior. (default: 20)
                              This parameter is passed through to the `websockets.client.connect()
                              <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`_
        :type ping_interval: int or None
        :param ping_timeout: If the corresponding `Pong frame` isn't received within
                             `ping_timeout` seconds, the connection is considered unusable and is closed with
                             code 1011. This ensures that the remote endpoint remains responsive. Set
                             `ping_timeout` to `None` to disable this behavior. (default: 20)
                             This parameter is passed through to the `websockets.client.connect()
                             <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`_
        :type ping_timeout: int or None
        :param close_timeout: The `close_timeout` parameter defines a maximum wait time in seconds for
                              completing the closing handshake and terminating the TCP connection. (default: 10)
                              This parameter is passed through to the `websockets.client.connect()
                              <https://websockets.readthedocs.io/en/stable/topics/design.html?highlight=close_timeout#closing-handshake>`_
        :type close_timeout: int or None
        :param stream_buffer_maxlen: Set a max len for the `stream_buffer`. Only used in combination with a non generic
                                     `stream_buffer`. The generic `stream_buffer` uses always the value of
                                     `BinanceWebSocketApiManager()`.
        :type stream_buffer_maxlen: int or None
        :param api: Setting this to `True` activates the creation of a Websocket API stream to send API requests via Websocket.
                    Needs `api_key` and `api_secret` in combination. This type of stream can not be combined with a UserData
                    stream or a other public endpoint. (Default is `False`)
        :type api: bool
        :param process_stream_data: Provide a function/method to process the received webstream data (callback). The
                            function will be called instead of
                            `add_to_stream_buffer() <unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_buffer>`_
                            like `process_stream_data(stream_data)` where
                            `stream_data` cointains the raw_stream_data. If not provided, the raw stream_data will
                            get stored in the stream_buffer or provided to the global callback function provided during
                            object instantiation! `How to read from stream_buffer!
                            <https://unicorn-binance-websocket-api.docs.lucit.tech/README.html?highlight=pop_stream_data_from_stream_buffer#and-4-more-lines-to-print-the-receives>`_
        :type process_stream_data: function
        :return: stream_id or 'False'
        """
        # handle Websocket API streams: https://developers.binance.com/docs/binance-trading-api/websocket_api
        if api is True:
            if api_key is False or api_secret is False:
                logger.error(f"BinanceWebSocketApiManager.create_stream(api={api}) - `api_key` and `api_secret` are "
                             f"mandatory if `api=True`")
                return False
        else:
            # create an ordinary stream
            if isinstance(channels, bool):
                logger.error(f"BinanceWebSocketApiManager.create_stream(" + str(channels) + ", " + str(markets) + ", "
                             + str(stream_label) + ", " + str(stream_buffer_name) + ", " + str(symbols) + ", " +
                             str(stream_buffer_maxlen) + ") - Parameter "
                             f"`channels` must be str, tuple, list or a set!")
                return False
            elif isinstance(markets, bool):
                if isinstance(channels, bool):
                    logger.error(f"BinanceWebSocketApiManager.create_stream(" + str(channels) + ", " + str(markets) + ", "
                                 + str(stream_label) + ", " + str(stream_buffer_name) + ", " + str(symbols) + ", " +
                                 str(stream_buffer_maxlen) + ") - Parameter "
                                 f"`markets` must be str, tuple, list or a set!")
                return False
            if type(channels) is str:
                channels = [channels]
            if type(markets) is str:
                markets = [markets]
        output = output or self.output_default
        close_timeout = close_timeout or self.close_timeout_default
        ping_interval = ping_interval or self.ping_interval_default
        ping_timeout = ping_timeout or self.ping_timeout_default
        stream_id = self.get_new_uuid_id()
        markets_new = []
        if stream_buffer_name is True:
            stream_buffer_name = stream_id
        for market in markets:
            if "!" in market \
                    or market == "allMiniTickers" \
                    or market == "allTickers" \
                    or market == "blockheight" \
                    or market == "$all":
                markets_new.append(market)
            else:
                if self.is_exchange_type('dex'):
                    if re.match(r'[a-zA-Z0-9]{41,43}', market) is None:
                        markets_new.append(str(market).upper())
                    else:
                        markets_new.append(str(market))
                elif self.is_exchange_type('cex'):
                    markets_new.append(str(market).lower())
        logger.info("BinanceWebSocketApiManager.create_stream(" + str(channels) + ", " + str(markets_new) + ", "
                    + str(stream_label) + ", " + str(stream_buffer_name) + ", " + str(symbols) + ", " + str(symbols) +
                    ", " + str(api) + ") with stream_id=" + str(stream_id))
        self._add_stream_to_stream_list(stream_id,
                                        channels,
                                        markets_new,
                                        stream_label,
                                        stream_buffer_name,
                                        symbols=symbols,
                                        api_key=api_key,
                                        api_secret=api_secret,
                                        output=output,
                                        ping_interval=ping_interval,
                                        ping_timeout=ping_timeout,
                                        close_timeout=close_timeout,
                                        stream_buffer_maxlen=stream_buffer_maxlen,
                                        api=api,
                                        process_stream_data=process_stream_data)
        try:
            loop = asyncio.new_event_loop()
        except OSError as error_msg:
            logger.critical(f"BinanceWebSocketApiManager.create_stream({str(channels)}, {str(markets_new)}, "
                            f"{str(stream_label)}, {str(stream_buffer_name)}, {str(symbols)}, {stream_buffer_maxlen}, "
                            f"{api}) with stream_id={str(stream_id)} - OSError  - can not create stream - "
                            f"error_msg: {str(error_msg)}")
            return False
        self.event_loops[stream_id] = loop
        self.set_socket_is_not_ready(stream_id)
        thread = threading.Thread(target=self._create_stream_thread,
                                  args=(loop,
                                        stream_id,
                                        channels,
                                        markets_new,
                                        stream_buffer_name,
                                        stream_buffer_maxlen,
                                        False),
                                  name=f"_create_stream_thread:  stream_id={stream_id}, time={time.time()}")
        thread.start()
        self.stream_threads[stream_id] = thread
        while self.socket_is_ready[stream_id] is False and self.high_performance is False:
            # This loop will wait till the thread and the asyncio init is ready. This avoids two possible errors as
            # described here: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/131
            logger.debug(f"BinanceWebSocketApiManager.create_stream({str(channels)}, {str(markets_new)}, "
                         f"{str(stream_label)}, {str(stream_buffer_name)}, {str(symbols)}, {stream_buffer_maxlen}, "
                         f"{api}) with stream_id={str(stream_id)} - Waiting till new socket and asyncio is ready")
            time.sleep(1)
        return stream_id

    def create_websocket_uri(self, channels, markets, stream_id=False, api_key=False, api_secret=False, symbols=False,
                             api=False):
        """
        Create a websocket URI

        :param channels: provide the channels to create the URI
        :type channels: str, tuple, list, set
        :param markets: provide the markets to create the URI
        :type markets: str, tuple, list, set
        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param symbols: provide the symbols for isolated_margin user_data streams
        :type symbols: str
        :return: str or False
        :param api: Setting this to `True` activates the creation of a Websocket API stream to send API requests via Websocket.
                    Needs `api_key` and `api_secret` in combination. This type of stream can not be combined with a UserData
                    stream or an other public endpoint. (Default is `False`)
        :type api: bool
        """
        if api is True:
            logger.info("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                        str(markets) + ", " + ", " + str(symbols) + ", " + str(api) + ") - Created websocket URI for "
                        "stream_id=" + str(stream_id) + " is " + self.websocket_api_base_uri)
            return self.websocket_api_base_uri
        if isinstance(channels, bool):
            logger.error(f"BinanceWebSocketApiManager.create_websocket_uri({str(channels)}, {str(markets)}"
                         f", {str(symbols)}) - error_msg: Parameter `channels` must be str, tuple, list "
                         f"or a set!")
            return False
        elif isinstance(markets, bool):
            logger.error(f"BinanceWebSocketApiManager.create_websocket_uri({str(channels)}, {str(markets)}"
                         f", {str(symbols)}) - error_msg: Parameter `markets` must be str, tuple, list "
                         f"or a set!")
            return False
        payload = []
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        if len(channels) == 1 and len(markets) == 1:
            if "!userData" in channels or "!userData" in markets:
                if stream_id is not False:
                    response = self.get_listen_key_from_restclient(stream_id, api_key, api_secret, symbols=symbols)
                    try:
                        if response['code'] == -1102 or \
                                response['code'] == -2008 or \
                                response['code'] == -2014 or \
                                response['code'] == -2015 or \
                                response['code'] == -11001:
                            # -1102 = Mandatory parameter 'symbol' was not sent, was empty/null, or malformed.
                            # -2008 = Invalid Api-Key ID
                            # -2014 = API-key format invalid
                            # -2015 = Invalid API-key, IP, or permissions for action
                            # -11001 = Isolated margin account does not exist.
                            logger.critical("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) +
                                            ", " + str(markets) + ", " + ", " + str(symbols) + ") - Received known "
                                            "error code from rest client: " + str(response))
                            return response
                        else:
                            logger.critical("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) +
                                            ", " + str(markets) + ", " + ", " + str(symbols) + ") - Received unknown "
                                            "error code from rest client: " + str(response))
                            return response
                    except KeyError:
                        pass
                    except TypeError:
                        pass
                    if response:
                        try:
                            uri = self.websocket_base_uri + "ws/" + str(response['listenKey'])
                            uri_hidden = self.websocket_base_uri + "ws/" + self.replacement_text
                            if self.show_secrets_in_logs is True:
                                logger.info("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) +
                                            ", " + str(markets) + ", " + str(symbols) + ") - result: " + uri)
                            else:
                                logger.info("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) +
                                            ", " + str(markets) + ", " + str(symbols) + ") - result: " +
                                            uri_hidden)
                            self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
                            return uri
                        except KeyError:
                            logger.critical("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", "
                                            + str(markets) + ", " + ", " + str(symbols) + ") - error_msg: can not "
                                            "create URI!!")
                            return False
                        except TypeError:
                            logger.critical("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", "
                                            + str(markets) + ", " + ", " + str(symbols) + ") - error_msg: can not "
                                            "create URI!!")
                            return False
                    else:
                        logger.critical("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                                        str(markets) + ", " + ", " + str(symbols) + ") - error_msg: can not create "
                                        "URI!!")
                        return False
                else:
                    logger.critical("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                                    str(markets) + ", " + ", " + str(symbols) + ") - error_msg: can not create URI!!")
                    return False
            elif "!bookTicker" in channels or "!bookTicker" in markets:
                if stream_id:
                    self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
                return self.websocket_base_uri + "ws/!bookTicker"
            elif "arr" in channels or "$all" in markets:
                if stream_id:
                    self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
                return self.websocket_base_uri + "ws/" + markets[0] + "@" + channels[0]
            elif "arr" in markets or "$all" in channels:
                if stream_id:
                    self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
                return self.websocket_base_uri + "ws/" + channels[0] + "@" + markets[0]
            elif self.is_exchange_type("dex"):
                if re.match(r'[a-zA-Z0-9]{41,43}', markets[0]) is not None:
                    try:
                        if self.stream_list[stream_id]['dex_user_address'] is False:
                            self.stream_list[stream_id]['dex_user_address'] = markets[0]
                        if self.stream_list[stream_id]['dex_user_address'] != markets[0]:
                            logger.error("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                                         str(markets) + ", " + ", " + str(symbols) + ") - Error: once set, the "
                                         "dex_user_address is not allowed to get changed anymore!")
                            return False
                    except KeyError:
                        pass
                    add_payload = {"method": "subscribe",
                                   "topic": channels[0],
                                   "address": markets[0]}
                    payload.append(add_payload)
                    if stream_id:
                        self.stream_list[stream_id]['payload'] = payload
                        self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
                    return self.websocket_base_uri + "ws/" + markets[0]
                elif markets[0] != "" and channels[0] != "":
                    return self.websocket_base_uri + "ws/" + markets[0] + "@" + channels[0]
                else:
                    logger.error("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                                 str(markets) + ", " + ", " + str(symbols) + ") - Error: not able to create websocket "
                                 "URI for DEX")
                    return False
        if self.is_exchange_type("dex"):
            query = "ws"
            if stream_id:
                payload = self.create_payload(stream_id, "subscribe", channels=channels, markets=markets)
                self.stream_list[stream_id]['payload'] = payload
                self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
            return self.websocket_base_uri + str(query)
        else:
            query = "stream?streams="
            final_market = "@arr"
            market = ""
            channel = ""
            for market in markets:
                if "arr@" in market:
                    final_market = "@" + market
            final_channel = "@arr"
            for channel in channels:
                if "arr@" in channel:
                    final_channel = "@" + channel
            for channel in channels:
                if channel == "!userData":
                    logger.error("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                                 str(markets) + ", " + ", " + str(symbols) + ") - Can not create "
                                 "'outboundAccountInfo' in a multi channel socket! "
                                 "Unfortunately Binance only stream it in a single stream socket! ./"
                                 "Use create_stream([\"arr\"], [\"!userData\"]) to "
                                 "initiate an extra connection.")
                    return False
            for market in markets:
                if market == "!userData":
                    logger.error("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                                 str(markets) + ", " + ", " + str(symbols) + ") - Can not create "
                                 "'outboundAccountInfo' in a multi channel socket! "
                                 "Unfortunatly Binance only stream it in a single stream socket! ./"
                                 "Use create_stream([\"arr\"], [\"!userData\"]) to "
                                 "initiate an extra connection.")
                    return False
            if "!" in channel:
                query += channel + final_market
            elif "!" in market:
                query += market + final_channel
            else:
                query += market.lower() + "@" + channel
            try:
                if self.subscribe_to_stream(stream_id, markets=markets, channels=channels) is False:
                    sys.exit(1)
            except KeyError:
                pass
            logger.info("BinanceWebSocketApiManager.create_websocket_uri(" + str(channels) + ", " +
                        str(markets) + ", " + ", " + str(symbols) + ") - Created websocket URI for stream_id=" +
                        str(stream_id) + " is " + self.websocket_base_uri + str(query))
            return self.websocket_base_uri + str(query)

    def delete_listen_key_by_stream_id(self, stream_id):
        """
        Delete a binance listen_key from a specific !userData stream

        :param stream_id: id of a !userData stream
        :type stream_id: str
        """
        try:
            if self.stream_list[stream_id]['listen_key'] is not False:
                logger.info("BinanceWebSocketApiManager.delete_listen_key_by_stream_id(" + str(stream_id) + ")")
                self.restclient.delete_listen_key(stream_id)
        except KeyError:
            return False

    def delete_stream_from_stream_list(self, stream_id):
        """
        Delete a stream from the stream_list

        Even if a stream crashes or get stopped, its data remains in the BinanceWebSocketApiManager till you stop the
        BinanceWebSocketApiManager itself. If you want to tidy up the stream_list you can use this method.

        :param stream_id: id of a stream
        :type stream_id: str
        :return: bool
        """
        logger.info("BinanceWebSocketApiManager.delete_stream_from_stream_list(" + str(stream_id) + ")")
        return self.stream_list.pop(stream_id, False)

    def fill_up_space_left(self, demand_of_chars, string, filling=" "):
        """
        Add whitespaces to `string` to a length of `demand_of_chars` on the left side

        :param demand_of_chars: how much chars does the string have to have?
        :type demand_of_chars: int
        :param string: the string that has to get filled up with spaces
        :type string: str
        :param filling: filling char (default: blank space)
        :type filling: str
        :return: the filled up string
        """
        blanks_pre = ""
        blanks_post = ""
        demand_of_blanks = demand_of_chars - len(str(string)) - 1
        while len(blanks_pre) < demand_of_blanks:
            blanks_pre += filling
            blanks_post = filling
        return blanks_pre + str(string) + blanks_post

    def fill_up_space_centered(self, demand_of_chars, string, filling=" "):
        """
        Add whitespaces to `string` to a length of `demand_of_chars`

        :param demand_of_chars: how much chars does the string have to have?
        :type demand_of_chars: int
        :param string: the string that has to get filled up with spaces
        :type string: str
        :param filling: filling char (default: blank space)
        :type filling: str
        :return: the filled up string
        """
        blanks_pre = ""
        blanks_post = ""
        demand_of_blanks = demand_of_chars - len(str(string)) - 1
        while (len(blanks_pre)+len(blanks_post)) < demand_of_blanks:
            blanks_pre += filling
            if (len(blanks_pre) + len(blanks_post)) < demand_of_blanks:
                blanks_post += filling
        return blanks_pre + str(string) + blanks_post

    def fill_up_space_right(self, demand_of_chars, string, filling=" "):
        """
        Add whitespaces to `string` to a length of `demand_of_chars` on the right side

        :param demand_of_chars: how much chars does the string have to have?
        :type demand_of_chars: int
        :param string: the string that has to get filled up with spaces
        :type string: str
        :param filling: filling char (default: blank space)
        :type filling: str
        :return: the filled up string
        """
        blanks_pre = " "
        blanks_post = ""
        demand_of_blanks = demand_of_chars - len(str(string))
        while len(blanks_post) < demand_of_blanks-1:
            blanks_pre = filling
            blanks_post += filling
        string = blanks_pre + str(string) + blanks_post
        return string[0:demand_of_chars]

    def get_active_stream_list(self):
        """
        Get a list of all active streams

        :return: set or False
        """
        # get the stream_list without stopped and crashed streams
        stream_list_with_active_streams = {}
        for stream_id in self.stream_list:
            if self.stream_list[stream_id]['status'] == "running":
                stream_list_with_active_streams[stream_id] = self.stream_list[stream_id]
        try:
            if len(stream_list_with_active_streams) > 0:
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
        `get_binance_api_status()` is obsolete and will be removed in future releases, please use `get_used_weight()`
        instead!

        :return: dict
        """
        logger.warning("`get_binance_api_status()` is obsolete and will be removed in future releases, please use"
                       "`get_used_weight()` instead!")
        return self.binance_api_status

    def get_debug_log(self):
        """
        Get the debug log string.

        :return: str
        """
        if self.debug:
            debug_msg = f" - called by {str(traceback.format_stack()[-2]).strip()}"
        else:
            debug_msg = ""
        return debug_msg

    @staticmethod
    def get_timestamp() -> int:
        """
        Get a Binance conform Timestamp.

        :return: int
        """
        return int(time.time() * 1000)

    def get_used_weight(self):
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
            return 0
        except KeyError:
            return 0
        try:
            current_receiving_speed = self.stream_list[stream_id]['transfer_rate_per_second']['speed']
        except KeyError:
            current_receiving_speed = 0
        return current_receiving_speed

    def get_current_receiving_speed_global(self):
        """
        Get the receiving speed of the last second in Bytes from all streams!

        :return: int
        """
        current_receiving_speed = 0
        try:
            temp_stream_list = copy.deepcopy(self.stream_list)
        except RuntimeError as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.get_current_receiving_speed_global() - RuntimeError: "
                         f"{str(error_msg)}")
            return 0
        except TypeError as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.get_current_receiving_speed_global() - RuntimeError: "
                         f"{str(error_msg)}")
            return 0
        for stream_id in temp_stream_list:
            current_receiving_speed += self.get_current_receiving_speed(stream_id)
        return current_receiving_speed

    @staticmethod
    def get_date_of_timestamp(timestamp):
        """
        Convert a timestamp into a readable date/time format for humans

        :param timestamp: provide the timestamp you want to convert into a date
        :type timestamp: timestamp
        :return: str
        """
        date = str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d, %H:%M:%S UTC'))
        return date

    def get_errors_from_endpoints(self):
        """
        Get all the stored error messages from the ringbuffer sent by the endpoints.

        :return: list
        """
        return self.ringbuffer_error

    def get_event_loop_by_stream_id(self, stream_id: Optional[Union[str, bool]] = False) -> bool:
        """
        Get the asyncio event loop used by a specific stream.

        :return: asyncio event loop or False
        """
        if stream_id is False:
            return False
        else:
            try:
                return self.event_loops[stream_id]
            except KeyError as error_msg:
                logger.debug(f"BinanceWebSocketApiManager.get_event_loop_by_stream_id() - KeyError - {str(error_msg)}")
                return False

    def get_exchange(self):
        """
        Get the name of the used exchange like "binance.com" or "binance.org-testnet"

        :return: str
        """
        return self.exchange

    @staticmethod
    def get_human_bytesize(bytes, suffix=""):
        """
        Convert the bytes to something readable

        :param bytes: amount of bytes
        :type bytes: int
        :param suffix: add a string after
        :type suffix: str
        :return:
        """
        if bytes > 1024 * 1024 * 1024 *1024:
            bytes = str(round(bytes / (1024 * 1024 * 1024 * 1024), 3)) + " tB" + suffix
        elif bytes > 1024 * 1024 * 1024:
            bytes = str(round(bytes / (1024 * 1024 * 1024), 2)) + " gB" + suffix
        elif bytes > 1024 * 1024:
            bytes = str(round(bytes / (1024 * 1024), 2)) + " mB" + suffix
        elif bytes > 1024:
            bytes = str(round(bytes / 1024, 2)) + " kB" + suffix
        else:
            bytes = str(bytes) + " B" + suffix
        return bytes

    @staticmethod
    def get_human_uptime(uptime):
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

    @staticmethod
    def get_latest_release_info():
        """
        Get infos about the latest available release

        :return: dict or False
        """
        try:
            respond = requests.get('https://api.github.com/repos/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/releases/latest')
            latest_release_info = respond.json()
            return latest_release_info
        except Exception:
            return False

    @staticmethod
    def get_latest_release_info_check_command():
        """
        Get infos about the latest available `check_lucit_collector` release
        
        :return: dict or False
        """
        try:
            respond = requests.get('https://api.github.com/repos/LUCIT-Development/check_lucit_collector.py/'
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
        Get the version of the latest available `check_lucit_collector.py` release (cache time 1 hour)
        
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

    def get_limit_of_subscriptions_per_stream(self):
        """
        Get the number of allowed active subscriptions per stream (limit of binance API)

        :return: int
        """
        return self.max_subscriptions_per_stream

    def get_number_of_all_subscriptions(self):
        """
        Get the amount of all stream subscriptions

        :return: int
        """
        subscriptions = 0
        try:
            active_stream_list = copy.deepcopy(self.get_active_stream_list())
            if active_stream_list:
                for stream_id in active_stream_list:
                    subscriptions += active_stream_list[stream_id]['subscriptions']
                self.all_subscriptions_number = subscriptions
        except TypeError:
            return self.all_subscriptions_number
        except RuntimeError:
            return self.all_subscriptions_number
        return subscriptions

    def get_number_of_free_subscription_slots(self, stream_id):
        """
        Get the number of free subscription slots (max allowed subscriptions - subscriptions) of a specific stream

        :return: int
        """
        free_slots =  self.max_subscriptions_per_stream - self.stream_list[stream_id]['subscriptions']
        return free_slots

    def get_listen_key_from_restclient(self, stream_id, api_key, api_secret, symbols=False):
        """
        Get a new or cached (<30m) listen_key

        :param stream_id: provide a stream_id
        :type stream_id: str
        :param api_key: provide a valid Binance API key
        :type api_key: str
        :param api_secret: provide a valid Binance API secret
        :type api_secret: str
        :param symbols: provide the symbols for isolated_margin user_data streams
        :type symbols: str
        :return: str or False
        """
        try:
            if (self.stream_list[stream_id]['start_time'] + self.stream_list[stream_id]['listen_key_cache_time']) > \
                    time.time() or (self.stream_list[stream_id]['last_static_ping_listen_key'] +
                                    self.stream_list[stream_id]['listen_key_cache_time']) > time.time():
                # listen_key is not older than 30 min
                if self.stream_list[stream_id]['listen_key'] is not False:
                    response = {'listenKey': self.stream_list[stream_id]['listen_key']}
                    return response
        except KeyError:
            logger.debug(f"BinanceWebSocketApiManager.get_listen_key_from_restclient() - KeyError")
            return False
        # no cached listen_key or listen_key is older than 30 min
        # acquire a new listen_key:
        response = self.restclient.get_listen_key(stream_id)
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

    def get_number_of_subscriptions(self, stream_id):
        """
        Get the number of subscriptions of a specific stream

        :return: int
        """
        count_subscriptions = 0
        for channel in self.stream_list[stream_id]['channels']:
            if "!" in channel \
                    or channel == "orders" \
                    or channel == "accounts" \
                    or channel == "transfers" \
                    or channel == "allTickers" \
                    or channel == "allMiniTickers" \
                    or channel == "blockheight":
                count_subscriptions += 1
                continue
            else:
                for market in self.stream_list[stream_id]['markets']:
                    if "!" in market \
                            or market == "orders" \
                            or market == "accounts" \
                            or market == "transfers" \
                            or market == "allTickers" \
                            or market == "allMiniTickers" \
                            or market == "blockheight":
                        count_subscriptions += 1
                    else:
                        count_subscriptions += 1
        return count_subscriptions

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

        :param check_command_version: is the version of the calling `check_command <https://github.com/LUCIT-Systems-and-Development/check_lucit_collector.py>`_
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

        :param check_command_version: is the version of the calling `check_command <https://github.com/LUCIT-Systems-and-Development/check_lucit_collector.py>`_
        :type check_command_version: False or str
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
            is_update_available_unicorn_fy = unicorn_fy.is_update_available()
        except ModuleNotFoundError:
            logger.critical("BinanceWebSocketApiManager.get_monitoring_status_plain() - UnicornFy not installed!")
            is_update_available_unicorn_fy = False
        except AttributeError:
            logger.error("BinanceWebSocketApiManager.get_monitoring_status_plain() - UnicornFy outdated!")
            is_update_available_unicorn_fy = True
        if check_command_version:
            is_update_available_check_command = self.is_update_availabe_check_command(
                check_command_version=check_command_version)
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
        if self.is_update_available() and is_update_available_unicorn_fy and is_update_available_check_command:
            result['update_msg'] = " Update available: UNICORN Binance WebSocket API, UnicornFy and " \
                                   "check_lucit_collector.py!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif self.is_update_available() and is_update_available_unicorn_fy:
            result['update_msg'] = " Update available: UNICORN Binance WebSocket API and UnicornFy"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif self.is_update_available() and is_update_available_check_command:
            result['update_msg'] = " Update available: UNICORN Binance WebSocket API and check_lucit_collector.py!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif is_update_available_unicorn_fy and is_update_available_check_command:
            result['update_msg'] = " Update available: UnicornFy and check_lucit_collector.py!"
            if warn_on_update is True:
                result['status_text'] = "WARNING"
                result['return_code'] = 1
        elif self.is_update_available():
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
            result['update_msg'] = " Update `check_lucit_collector.py` " + \
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

    @staticmethod
    def get_new_uuid_id() -> str:
        """
        Get a new unique uuid in string format. This is used as 'stream_id' or 'socket_id'.

        :return: uuid (str)
        """
        stream_id = uuid.uuid4()
        new_id_hash = hashlib.sha256(str(stream_id).encode()).hexdigest()
        new_id = f"{new_id_hash[0:12]}-{new_id_hash[12:16]}-{new_id_hash[16:20]}-{new_id_hash[20:24]}-" \
                 f"{new_id_hash[24:32]}"
        return new_id

    def get_process_usage_memory(self):
        """
        Get the used memory of this process

        :return: str
        """
        process = psutil.Process(os.getpid())
        memory = self.get_human_bytesize(process.memory_info()[0])
        return memory

    def get_process_usage_cpu(self):
        """
        Get the used cpu power of this process

        :return: int
        """
        try:
            cpu = psutil.cpu_percent(interval=None)
        except OSError as error_msg:
            logger.error(f"BinanceWebSocketApiManager.get_process_usage_cpu() - OSError - error_msg: {str(error_msg)}")
            return False
        return cpu

    def get_process_usage_threads(self):
        """
        Get the amount of threads that this process is using

        :return: int
        """
        threads = threading.active_count()
        return threads

    def get_reconnects(self):
        """
        Get the number of total reconnects

        :return: int
        """
        return self.reconnects

    def get_request_id(self):
        """
        Get a unique `request_id`

        :return: int
        """
        with self.request_id_lock:
            self.request_id += 1
            return self.request_id

    def get_result_by_request_id(self, request_id=False, timeout=10):
        """
        Get the result related to the provided `request_id`

        :param request_id: if you run `get_stream_subscriptions()
                           <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_subscriptions>`_
                           it returns a unique `request_id` - provide it to this method to receive the result.
        :type request_id: stream_id (uuid)
        :param timeout: seconds to wait to receive the result. If not there it returns 'False'
        :type timeout: int
        :return: `result` or False
        """
        if request_id is False:
            return False
        wait_till_timestamp = time.time() + timeout
        while wait_till_timestamp >= time.time():
            for result in self.ringbuffer_result:
                result_dict = json.loads(result)
                if result_dict['id'] == request_id:
                    return result
        return False

    def get_results_from_endpoints(self):
        """
        Get all the stored result messages from the ringbuffer sent by the endpoints.

        :return: list
        """
        return self.ringbuffer_result

    def get_ringbuffer_error_max_size(self):
        """
        How many entries should be stored in the ringbuffer?

        :return: int
        """
        return self.ringbuffer_error_max_size

    def get_ringbuffer_result_max_size(self):
        """
        How many entries should be stored in the ringbuffer?

        :return: int
        """
        return self.ringbuffer_result_max_size

    def get_start_time(self):
        """
        Get the start_time of the  BinanceWebSocketApiManager instance

        :return: timestamp
        """
        return self.start_time

    def get_stream_buffer_byte_size(self):
        """
        Get the current byte size estimation of the stream_buffer

        :return: int
        """
        total_received_bytes = self.get_total_received_bytes()
        total_receives = self.get_total_receives()
        stream_buffer_length = self.get_stream_buffer_length()
        if total_received_bytes == 0 or total_receives == 0:
            return 0
        else:
            return round(total_received_bytes / total_receives * stream_buffer_length)

    def get_stream_buffer_length(self, stream_buffer_name=False):
        """
        Get the current number of items in all stream_buffer or of a specific stream_buffer

        :param stream_buffer_name: Name of the stream_buffer
        :type stream_buffer_name: str or stream_id
        :return: int
        """
        number = 0
        if stream_buffer_name:
            try:
                return len(self.stream_buffers[stream_buffer_name])
            except KeyError as error_msg:
                logger.debug(f"BinanceWebSocketApiManager.get_stream_buffer_length() - KeyError - "
                             f"error_msg: {error_msg}")
                return 0
        else:
            number += len(self.stream_buffer)
            for stream_buffer_name in self.stream_buffers:
                number += len(self.stream_buffers[stream_buffer_name])
            return number

    def get_stream_id_by_label(self, stream_label=False):
        """
        Get the stream_id of a specific stream by stream label

        :param stream_label: stream_label of the stream you search
        :type stream_label: str
        :return: stream_id or False
        """
        if stream_label:
            for stream_id in self.stream_list:
                if self.stream_list[stream_id]['stream_label'] == stream_label:
                    logger.debug(f"BinanceWebSocketApiManager.get_stream_id_by_label() - Found `stream_id` via `stream_label` "
                                 f"`{stream_label}`")
                    return stream_id
        logger.error(f"BinanceWebSocketApiManager.get_stream_id_by_label() - No `stream_id` found via `stream_label` "
                     f"`{stream_label}`")
        return False

    def get_stream_info(self, stream_id):
        """
        Get all infos about a specific stream

        :param stream_id: id of a stream
        :type stream_id: str
        :return: set
        """
        current_timestamp = time.time()
        try:
            temp_stream_list = copy.deepcopy(self.stream_list[stream_id])
        except RuntimeError:
            logger.error("BinanceWebSocketApiManager.get_stream_info(" + str(stream_id) + ") Info: RuntimeError")
            return self.get_stream_info(stream_id)
        except KeyError:
            logger.error("BinanceWebSocketApiManager.get_stream_info(" + str(stream_id) + ") Info: KeyError")
            return False
        if temp_stream_list['last_heartbeat'] is not None:
            temp_stream_list['seconds_to_last_heartbeat'] = \
                current_timestamp - self.stream_list[stream_id]['last_heartbeat']
        if temp_stream_list['has_stopped'] is not False:
            temp_stream_list['seconds_since_has_stopped'] = \
                int(current_timestamp) - int(self.stream_list[stream_id]['has_stopped'])
        try:
            self.stream_list[stream_id]['processed_receives_statistic'] = self.get_stream_statistic(stream_id)
        except ZeroDivisionError:
            pass
        self.stream_list[stream_id]['transfer_rate_per_second']['speed'] = self.get_current_receiving_speed(stream_id)
        return temp_stream_list

    def get_stream_label(self, stream_id=False):
        """
        Get the stream_label of a specific stream

        :param stream_id: id of a stream
        :type stream_id: str
        :return: str or False
        """
        if stream_id:
            return self.stream_list[stream_id]['stream_label']
        else:
            return False

    def get_stream_subscriptions(self, stream_id, request_id=False):
        """
        Get a list of subscriptions of a specific stream from Binance endpoints - the result can be received via
        the `stream_buffer` and is also added to the results ringbuffer - `get_results_from_endpoints()
        <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_results_from_endpoints>`_
        to get all results or use `get_result_by_request_id(request_id)
        <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_result_by_request_id>`_
        to get a specific one!

        This function is supported by CEX endpoints only!

        Info: https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#listing-subscriptions

        :param stream_id: id of a stream
        :type stream_id: str
        :param request_id: id to use for the request - use `get_request_id()` to create a unique id. If not provided or
                           `False`, then this method is using `get_request_id()
                           <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_request_id>`_
                           automatically.
        :type request_id: int
        :return: request_id (int)
        """
        if request_id is False:
            request_id = self.get_request_id()
        if self.is_exchange_type('dex'):
            logger.error("BinanceWebSocketApiManager.get_stream_subscriptions(" + str(stream_id) + ", " +
                         str(request_id) + ") DEX websockets dont support the listing of subscriptions! Request not "
                         "sent!")
            return False
        elif self.is_exchange_type('cex'):
            payload = {"method": "LIST_SUBSCRIPTIONS",
                       "id": request_id}
            self.stream_list[stream_id]['payload'].append(payload)
            logger.info("BinanceWebSocketApiManager.get_stream_subscriptions(" + str(stream_id) + ", " +
                        str(request_id) + ") payload added!")
            return request_id
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

    def get_stream_buffer_maxlen(self, stream_buffer_name=False):
        """
        Get the maxlen value of the
        `stream_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_buffer%60>`_

        If maxlen is not specified or is None, `stream_buffer` may grow to an arbitrary length. Otherwise, the
        `stream_buffer` is bounded to the specified maximum length. Once a bounded length `stream_buffer` is full, when
        new items are added, a corresponding number of items are discarded from the opposite end.

        :param stream_buffer_name: `False` to read from generic stream_buffer, the stream_id if you used True in
                                   create_stream() or the string name of a shared stream_buffer.
        :type stream_buffer_name: bool or str
        :return: int or False
        """
        if stream_buffer_name is False:
            try:
                return self.stream_buffer.maxlen
            except IndexError:
                return False
        else:
            try:
                return self.stream_buffers[stream_buffer_name].maxlen
            except IndexError:
                return False
            except KeyError:
                return False

    def get_stream_receives_last_second(self, stream_id):
        """
        Get the number of receives of specific stream from the last seconds

        :param stream_id: id of a stream
        :type stream_id: str
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
        :type stream_id: str
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

    def get_the_one_active_websocket_api(self):
        """
        This function is needed to simplify the access to the websocket API, if only one API stream exists it is clear
        that only this stream can be used for the requests and therefore will be used.

        :return: stream_id or False
        """
        found_entries = 0
        found_stream_id = None
        for stream_id in self.stream_list:
            if self.stream_list[stream_id]['api'] is True:
                found_entries += 1
                found_stream_id = stream_id

        if found_entries == 1:
            # Its clear, there is only one valid connection to use, so we can take it!
            logger.debug(f"BinanceWebSocketApiManager.get_the_one_active_websocket_api() - Found `stream_id` "
                         f"`{found_stream_id}`")
            return found_stream_id
        else:
            logger.error(f"BinanceWebSocketApiManager.get_the_one_active_websocket_api() - No valid `stream_id` found! "
                         f"- `found_entries` = {found_entries}")
            return False

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

    def get_user_agent(self):
        """
        Get the user_agent string "lib name + lib version + python version"

        :return:
        """
        user_agent = f"{self.name}_{str(self.get_version())}-python_{str(platform.python_version())}"
        return user_agent

    def get_version(self):
        """
        Get the package/module version

        :return: str
        """
        return self.version

    def get_version_unicorn_fy(self):
        """
        Get the package/module version of `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_

        :return: str
        """
        from unicorn_fy.unicorn_fy import UnicornFy

        unicorn_fy = UnicornFy()

        return unicorn_fy.get_version()

    @staticmethod
    def help():
        """
        Help in iPython
        """
        print("Ctrl+D to close")

    def increase_received_bytes_per_second(self, stream_id, size):
        """
        Add the amount of received bytes per second

        :param stream_id: id of a stream
        :type stream_id: str
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
        :type stream_id: str
        """
        current_timestamp = int(time.time())
        try:
            self.stream_list[stream_id]['processed_receives_total'] += 1
        except KeyError:
            return False
        try:
            with self.stream_threading_lock[stream_id]['receives_statistic_last_second_lock']:
                self.stream_list[stream_id]['receives_statistic_last_second']['entries'][current_timestamp] += 1
        except KeyError:
            with self.stream_threading_lock[stream_id]['receives_statistic_last_second_lock']:
                self.stream_list[stream_id]['receives_statistic_last_second']['entries'][current_timestamp] = 1
        with self.total_receives_lock:
            self.total_receives += 1

    def increase_reconnect_counter(self, stream_id):
        """
        Increase reconnect counter

        :param stream_id: id of a stream
        :type stream_id: str
        """
        self.stream_list[stream_id]['logged_reconnects'].append(time.time())
        self.stream_list[stream_id]['reconnects'] += 1
        with self.reconnects_lock:
            self.reconnects += 1

    def increase_transmitted_counter(self, stream_id):
        """
        Increase the counter of transmitted payloads
        :param stream_id: id of a stream
        :type stream_id: str
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
        if exchange_type is False or not self.exchange_type:
            return False
        return self.exchange_type == exchange_type

    def is_stop_request(self, stream_id, exclude_kill_requests=False):
        """
        Has a specific stream a stop_request?

        :param stream_id: id of a stream
        :type stream_id: str
        :param exclude_kill_requests: if `True` this method returns `False` on kill_requests
        :type exclude_kill_requests: bool
        :return: bool
        """
        logger.debug(f"BinanceWebSocketApiManager.is_stop_request({stream_id}){self.get_debug_log()}")
        try:
            if self.stream_list[stream_id]['stop_request'] is True:
                return True
            elif self.is_manager_stopping():
                return True
            elif self.stream_list[stream_id]['kill_request'] is True and exclude_kill_requests is False:
                return True
            else:
                return False
        except KeyError:
            return False

    def is_stop_as_crash_request(self, stream_id):
        """
        Has a specific stream a stop_as_crash_request?

        :param stream_id: id of a stream
        :type stream_id: str
        :return: bool
        """
        logger.debug(f"BinanceWebSocketApiManager.is_stop_as_crash_request(" + str(stream_id) +
                     f"){self.get_debug_log()}")
        try:
            if self.stream_list[stream_id]['crash_request'] is True:
                return True
        except KeyError:
            pass
        if self.is_manager_stopping():
            return True
        else:
            return False

    def is_stream_signal_buffer_enabled(self):
        """
        Is the stream_signal_buffer enabled?

        :return: bool
        """
        return self.enable_stream_signal_buffer

    def is_update_available(self):
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

    def is_update_availabe_unicorn_fy(self):
        """
        Is a new release of `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_ available?

        :return: bool
        """
        from unicorn_fy.unicorn_fy import UnicornFy

        unicorn_fy = UnicornFy()

        return unicorn_fy.is_update_available()

    def is_update_availabe_check_command(self, check_command_version=False):
        """
        Is a new release of `check_lucit_collector.py` available?

        :return: bool
        """
        installed_version = check_command_version
        latest_version = self.get_latest_version_check_command()
        if ".dev" in str(installed_version):
            installed_version = installed_version[:-4]
        if latest_version == installed_version:
            return False
        elif latest_version == "unknown":
            return False
        else:
            return True

    def kill_stream(self, stream_id):
        """
        Kill a specific stream

        :param stream_id: id of a stream
        :type stream_id: str
        :return: bool
        """
        # stop a specific stream by stream_id
        logger.debug(f"BinanceWebSocketApiManager.kill_stream({stream_id}){self.get_debug_log()}")
        try:
            loop = self.get_event_loop_by_stream_id(stream_id)
            try:
                if loop.is_running():
                    logger.debug(f"BinanceWebSocketApiManager.kill_stream({stream_id}) - Closing event_loop "
                                 f"of stream_id {stream_id}")
                    loop.close()
            except AttributeError as error_msg:
                logger.debug(f"BinanceWebSocketApiManager.kill_stream({stream_id}) - AttributeError - {error_msg}")
        except RuntimeError as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.kill_stream({stream_id}) - RuntimeError - {error_msg}")
        except RuntimeWarning as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.kill_stream({stream_id}) - RuntimeWarning - {error_msg}")
        return True

    def pop_stream_data_from_stream_buffer(self, stream_buffer_name=False, mode="FIFO"):
        """
        Get oldest or latest entry from
        `stream_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_buffer%60>`_
        and remove from FIFO/LIFO stack.

        :param stream_buffer_name: `False` to read from generic stream_buffer, the stream_id if you used True in
                                   create_stream() or the string name of a shared stream_buffer.
        :type stream_buffer_name: bool or str
        :param mode: How to read from the `stream_buffer` - "FIFO" (default) or "LIFO".
        :type mode: str
        :return: stream_data - str, dict or False
        """
        if stream_buffer_name is False:
            try:
                with self.stream_buffer_lock:
                    if mode.upper() == "FIFO":
                        stream_data = self.stream_buffer.popleft()
                    elif mode.upper() == "LIFO":
                        stream_data = self.stream_buffer.pop()
                    else:
                        return False
                return stream_data
            except IndexError:
                return False
        else:
            try:
                with self.stream_buffer_locks[stream_buffer_name]:
                    if mode.upper() == "FIFO":
                        stream_data = self.stream_buffers[stream_buffer_name].popleft()
                    elif mode.upper() == "LIFO":
                        stream_data = self.stream_buffers[stream_buffer_name].pop()
                    else:
                        return False
                return stream_data
            except IndexError:
                return False
            except KeyError:
                return False

    def pop_stream_signal_from_stream_signal_buffer(self):
        """
        Get oldest entry from
        `stream_signal_buffer <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signal_buffer%60>`_
        and remove from stack/pipe (FIFO stack)

        :return: stream_signal - dict or False
        """
        try:
            with self.stream_signal_buffer_lock:
                stream_signal = self.stream_signal_buffer.popleft()
            return stream_signal
        except IndexError:
            return False

    def print_stream_info(self, stream_id, add_string="", title=None):
        """
        Print all infos about a specific stream, helps debugging :)

        :param stream_id: id of a stream
        :type stream_id: str
        :param add_string: text to add to the output
        :type add_string: str
        :param title: set to `True` to use curses instead of print()
        :type title: bool
        :return: bool
        """
        restart_requests_row = ""
        binance_api_status_row = ""
        stream_label_row = ""
        status_row = ""
        payload_row = ""
        symbol_row = ""
        dex_user_address_row = ""
        last_static_ping_listen_key = ""
        stream_info = self.get_stream_info(stream_id)
        stream_row_color_prefix = ""
        stream_row_color_suffix = ""
        if len(add_string) > 0:
            add_string = " " + str(add_string) + "\r\n"
        if self.socks5_proxy_address is not None and self.socks5_proxy_port is not None:
            proxy = f"\r\n proxy: {self.socks5_proxy_address}:{self.socks5_proxy_port} (ssl:" \
                    f"{self.socks5_proxy_ssl_verification})"
        else:
            proxy = ""
        try:
            if len(self.stream_list[stream_id]['logged_reconnects']) > 0:
                logged_reconnects_row = "\r\n logged_reconnects: "
                row_prefix = ""
                for timestamp in self.stream_list[stream_id]['logged_reconnects']:
                    logged_reconnects_row += row_prefix + \
                                             datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d, %H:%M:%S UTC')
                    row_prefix = ", "
            else:
                logged_reconnects_row = ""
        except KeyError:
            return False
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
        if self.stream_list[stream_id]['symbols'] is not False:
            symbol_row = " symbols:" + str(stream_info['symbols']) + "\r\n"
        if self.stream_list[stream_id]["payload"]:
            payload_row = " payload: " + str(self.stream_list[stream_id]["payload"]) + "\r\n"
        if self.stream_list[stream_id]["dex_user_address"] is not False:
            dex_user_address_row = " user_address: " + str(self.stream_list[stream_id]["dex_user_address"]) + "\r\n"
        if self.stream_list[stream_id]["stream_label"] is not None:
            stream_label_row = " stream_label: " + self.stream_list[stream_id]["stream_label"] + "\r\n"
        if isinstance(stream_info['ping_interval'], int):
            ping_interval = f"{stream_info['ping_interval']} seconds"
        else:
            ping_interval = stream_info['ping_interval']
        if isinstance(stream_info['ping_timeout'], int):
            ping_timeout = f"{stream_info['ping_timeout']} seconds"
        else:
            ping_timeout = stream_info['ping_timeout']
        if isinstance(stream_info['close_timeout'], int):
            close_timeout = f"{stream_info['close_timeout']} seconds"
        else: 
            close_timeout = stream_info['close_timeout']
        if title:
            first_row = str(self.fill_up_space_centered(96, f" {title} ", "=")) + "\r\n"
            last_row = str(self.fill_up_space_centered(96, f" Powered by {self.get_user_agent()} ", "=")) + "\r\n"
        else:
            first_row = str(self.fill_up_space_centered(96, f"{self.get_user_agent()} ", "=")) + "\r\n"
            last_row = "========================================================================================" \
                       "=======\r\n"
        try:
            uptime = self.get_human_uptime(stream_info['processed_receives_statistic']['uptime'])
            print(first_row +
                  " exchange: " + str(self.stream_list[stream_id]['exchange']) + f"{proxy}\r\n" +
                  str(add_string) +
                  " stream_id:", str(stream_id), "\r\n" +
                  str(stream_label_row) +
                  " stream_buffer_maxlen:", str(stream_info['stream_buffer_maxlen']), "\r\n" +
                  f" api: {self.stream_list[stream_id]['api']}\r\n" +
                  " channels (" + str(len(stream_info['channels'])) + "):", str(stream_info['channels']), "\r\n" +
                  " markets (" + str(len(stream_info['markets'])) + "):", str(stream_info['markets']), "\r\n" +
                  f" websocket_uri: {self.stream_list[stream_id]['websocket_uri']}\r\n" +
                  str(symbol_row) +
                  " subscriptions: " + str(self.stream_list[stream_id]['subscriptions']) + "\r\n" +
                  str(payload_row) +
                  str(status_row) +
                  str(dex_user_address_row) +
                  f" ping_interval: {ping_interval}\r\n"
                  f" ping_timeout: {ping_timeout}\r\n"
                  f" close_timeout: {close_timeout}\r\n"
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
                  " kill_request:", str(stream_info['kill_request']), "\r\n"
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
                  str(stream_info['processed_receives_statistic']['stream_receives_per_day'].__round__(3)), "\r\n" +
                  last_row)
        except KeyError:
            self.print_stream_info(stream_id)

    def print_summary(self, add_string="", disable_print=False, title=None):
        """
        Print an overview of all streams
        
        :param add_string: text to add to the output
        :type add_string: str
        :param disable_print: set to `True` to use curses instead of print()
        :type disable_print: bool
        :param title: set a title (first row) for print_summary output
        :type title: str
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
        highest_receiving_speed_row = f"{str(self.get_human_bytesize(self.receiving_speed_peak['value'], '/s'))} " \
                                      f"(reached at " \
                                      f"{self.get_date_of_timestamp(self.receiving_speed_peak['timestamp'])})"

        if self.socks5_proxy_address is not None and self.socks5_proxy_port is not None:
            proxy = f"\r\n proxy: {self.socks5_proxy_address}:{self.socks5_proxy_port} (ssl_verification: " \
                    f"{self.socks5_proxy_ssl_verification})"
        else:
            proxy = ""

        if len(add_string) > 0:
            add_string = " " + str(add_string) + "\r\n"
        try:
            temp_stream_list = copy.deepcopy(self.stream_list)
        except RuntimeError:
            return ""
        except TypeError:
            return ""
        for stream_id in temp_stream_list:
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
            if self.stream_list[stream_id]['stream_label'] is not None:
                if len(self.stream_list[stream_id]['stream_label']) > 18:
                    stream_label = str(self.stream_list[stream_id]['stream_label'])[:13] + "..."
                else:
                    stream_label = str(self.stream_list[stream_id]['stream_label'])
            else:
                stream_label = str(self.stream_list[stream_id]['stream_label'])
            stream_rows += stream_row_color_prefix + str(stream_id) + stream_row_color_suffix + " |" + \
                self.fill_up_space_right(17, stream_label) + "|" + \
                self.fill_up_space_left(8, self.get_stream_receives_last_second(stream_id)) + "|" + \
                self.fill_up_space_left(11, stream_statistic['stream_receives_per_second'].__round__(2)) + "|" + \
                self.fill_up_space_left(8, self.stream_list[stream_id]['receives_statistic_last_second']['most_receives_per_second']) \
                + "|" + stream_row_color_prefix + \
                self.fill_up_space_left(8, len(self.stream_list[stream_id]['logged_reconnects'])) + \
                stream_row_color_suffix + "\r\n "
            if self.is_stop_request(stream_id, exclude_kill_requests=True) is True and \
                    self.stream_list[stream_id]['status'] == "running":
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
            received_bytes_per_x_row += str(self.get_human_bytesize(received_bytes_per_second, '/s')) + " (per day " + \
                                        str(((received_bytes_per_second / 1024 / 1024 / 1024) * 60 * 60 * 24).__round__(2))\
                                        + " gB)"
            if self.get_stream_buffer_length() > 50:
                stream_row_color_prefix = "\033[1m\033[34m"
                stream_row_color_suffix = "\033[0m"
                stream_buffer_row += stream_row_color_prefix + " stream_buffer_stored_items: " + \
                                     str(self.get_stream_buffer_length()) + "\r\n"
                stream_buffer_row += " stream_buffer_byte_size: " + str(self.get_stream_buffer_byte_size()) + \
                                     " (" + str(self.get_human_bytesize(self.get_stream_buffer_byte_size())) + ")" + \
                                     stream_row_color_suffix + "\r\n"
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
                    binance_api_status_code = "\033[1m\033[31m" + str(self.binance_api_status['status_code']) + \
                                              "\033[0m"
                else:
                    binance_api_status_code = "\033[1m\033[33m" + str(self.binance_api_status['status_code']) + \
                                              "\033[0m"
                binance_api_status_row = " binance_api_status: used_weight=" + \
                                         str(self.binance_api_status['weight']) + \
                                         ", status_code=" + str(binance_api_status_code) + " (last update " + \
                                         str(datetime.utcfromtimestamp(
                                             self.binance_api_status['timestamp']).strftime('%Y-%m-%d, %H:%M:%S UTC')) + \
                                         ")\r\n"

            if title:
                first_row = str(self.fill_up_space_centered(96, f" {title} ", "=")) + "\r\n"
                last_row = str(self.fill_up_space_centered(96, f" Powered by {self.get_user_agent()} ", "=")) + "\r\n"
            else:
                first_row = str(self.fill_up_space_centered(96, f" {self.get_user_agent()} ", "=")) + "\r\n"
                last_row = "========================================================================================" \
                           "=======\r\n"
            try:
                print_text = (
                    first_row +
                    " exchange: " + str(self.stream_list[stream_id]['exchange']) + f"{proxy}\r\n" +
                    " uptime: " + str(self.get_human_uptime(time.time() - self.start_time)) + " since " +
                    str(self.get_date_of_timestamp(self.start_time)) + "\r\n" +
                    " streams: " + str(streams) + "\r\n" +
                    str(active_streams_row) +
                    str(crashed_streams_row) +
                    str(restarting_streams_row) +
                    str(stopped_streams_row) +
                    str(streams_with_stop_request_row) +
                    " subscriptions: " + str(self.get_number_of_all_subscriptions()) + "\r\n" +
                    str(stream_buffer_row) +
                    " current_receiving_speed: " + str(self.get_human_bytesize(current_receiving_speed, "/s")) + "\r\n" +
                    " average_receiving_speed: " + str(received_bytes_per_x_row) + "\r\n" +
                    " highest_receiving_speed: " + str(highest_receiving_speed_row) + "\r\n" +
                    " total_receives: " + str(self.total_receives) + "\r\n"
                    " total_received_bytes: " + str(total_received_bytes) + "\r\n"
                    " total_transmitted_payloads: " + str(self.total_transmitted) + "\r\n" +
                    " stream_buffer_maxlen: " + str(self.stream_buffer_maxlen) + "\r\n" +
                    str(binance_api_status_row) +
                    " process_ressource_usage: cpu=" + str(self.get_process_usage_cpu()) + "%, memory=" +
                    str(self.get_process_usage_memory()) + ", threads=" + str(self.get_process_usage_threads()) +
                    "\r\n" + str(add_string) +
                    " ---------------------------------------------------------------------------------------------\r\n"
                    "               stream_id              |   stream_label  |  last  |  average  |  peak  | recon\r\n"
                    " ---------------------------------------------------------------------------------------------\r\n"
                    " " + str(stream_rows) +
                    "---------------------------------------------------------------------------------------------\r\n"
                    " all_streams                                            |" +
                    self.fill_up_space_left(8, self.get_all_receives_last_second()) + "|" +
                    self.fill_up_space_left(11, all_receives_per_second.__round__(2)) + "|" +
                    self.fill_up_space_left(8, self.most_receives_per_second) + "|" +
                    self.fill_up_space_left(8, self.reconnects) + "\r\n" +
                    last_row
                )
                if disable_print:
                    if sys.platform.startswith('Windows'):
                        print_text = self.remove_ansi_escape_codes(print_text)
                    return print_text
                else:
                    print(print_text)
            except UnboundLocalError:
                pass
        except ZeroDivisionError:
            pass

    def print_summary_to_png(self, print_summary_export_path, hight_per_row=12.5):
        """
        Create a PNG image file with the console output of `print_summary()`

        *LINUX ONLY* It should not be hard to make it OS independent:
        https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/61

        :param print_summary_export_path: If you want to export the output of print_summary() to an image,
                                          please provide a path like "/var/www/html/". `View the Wiki!
                                          <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/How-to-export-print_summary()-stdout-to-PNG%3F>`_
        :type print_summary_export_path: str
        :param hight_per_row: set the hight per row for the image hight calculation
        :type hight_per_row: int
        :return: bool
        """
        print_text = self.print_summary(disable_print=True)
        # Todo:
        # 1. Handle paths right
        # 2. Use PythonMagick instead of Linux ImageMagick
        with open(print_summary_export_path + "print_summary.txt", 'w') as text_file:
            print(self.remove_ansi_escape_codes(print_text), file=text_file)
            try:
                image_hight = print_text.count("\n") * hight_per_row + 15
            except AttributeError:
                return False
        os.system('convert -size 720x' + str(image_hight) + ' xc:black -font "FreeMono" -pointsize 12 -fill white -annotate '
                  '+30+30 "@' + print_summary_export_path + 'print_summary.txt' + '" ' +
                  print_summary_export_path + 'print_summary_plain.png')
        os.system('convert ' + print_summary_export_path + 'print_summary_plain.png -font "FreeMono" '
                  '-pointsize 12 -fill red -undercolor \'#00000080\' -gravity North -annotate +0+5 '
                  '"$(date)" ' + print_summary_export_path + 'print_summary.png')
        return True

    @staticmethod
    def remove_ansi_escape_codes(text):
        """
        Remove ansi excape codes from the text string!

        :param text: str
        :return:
        """
        text = str(text)
        text = text.replace("\033[1m\033[31m", "")
        text = text.replace("\033[1m\033[32m", "")
        text = text.replace("\033[1m\033[33m", "")
        text = text.replace("\033[1m\033[34m", "")
        text = text.replace("\033[0m", "")
        return text

    def replace_stream(self,
                       stream_id,
                       new_channels,
                       new_markets,
                       new_stream_label=None,
                       new_stream_buffer_name=False,
                       new_api_key=False,
                       new_api_secret=False,
                       new_symbols=False,
                       new_output="raw_data",
                       new_ping_interval=20,
                       new_ping_timeout=20,
                       new_close_timeout=10,
                       new_stream_buffer_maxlen=None):
        """
        Replace a stream

        If you want to start a stream with a new config, its recommended, to first start a new stream with the new
        settings and close the old stream not before the new stream received its first data. So your data will stay
        consistent.

        :param stream_id: id of the old stream
        :type stream_id: str
        :param new_channels: the new channel list for the stream
        :type new_channels: str, tuple, list, set
        :param new_markets: the new markets list for the stream
        :type new_markets: str, tuple, list, set
        :param new_stream_label: provide a stream_label to identify the stream
        :type new_stream_label: str
        :param new_stream_buffer_name: If `False` the data is going to get written to the default stream_buffer,
                                   set to `True` to read the data via `pop_stream_data_from_stream_buffer(stream_id)` or
                                   provide a string to create and use a shared stream_buffer and read it via
                                   `pop_stream_data_from_stream_buffer('string')`.
        :type new_stream_buffer_name: bool or str
        :param new_api_key: provide a valid Binance API key
        :type new_api_key: str
        :param new_api_secret: provide a valid Binance API secret
        :type new_api_secret: str
        :param new_symbols: provide the symbols for isolated_margin user_data streams
        :type new_symbols: str
        :return: new stream_id
        :param new_output: set to "dict" to convert the received raw data to a python dict, set to "UnicornFy" to convert
                           with `UnicornFy <https://github.com/LUCIT-Systems-and-Development/unicorn-fy>`_ - otherwise the output
                           remains unchanged and gets delivered as received from the endpoints
        :type new_output: str
        :param new_ping_interval: Once the connection is open, a `Ping frame` is sent every
                                  `ping_interval` seconds. This serves as a keepalive. It helps keeping
                                  the connection open, especially in the presence of proxies with short
                                  timeouts on inactive connections. Set `ping_interval` to `None` to
                                  disable this behavior. (default: 20)
                                  This parameter is passed through to the `websockets.client.connect()
                                  <https://websockets.readthedocs.io/en/stable/api.html?highlight=ping_interval#websockets.client.connect>`_
        :type new_ping_interval: int or None
        :param new_ping_timeout: If the corresponding `Pong frame` isn't received within
                                 `ping_timeout` seconds, the connection is considered unusable and is closed with
                                 code 1011. This ensures that the remote endpoint remains responsive. Set
                                 `ping_timeout` to `None` to disable this behavior. (default: 20)
                                 This parameter is passed through to the `websockets.client.connect()
                                 <https://websockets.readthedocs.io/en/stable/api.html?highlight=ping_interval#websockets.client.connect>`_
        :type new_ping_timeout: int or None
        :param new_close_timeout: The `close_timeout` parameter defines a maximum wait time in seconds for
                                  completing the closing handshake and terminating the TCP connection. (default: 10)
                                  This parameter is passed through to the `websockets.client.connect()
                                  <https://websockets.readthedocs.io/en/stable/api.html?highlight=ping_interval#websockets.client.connect>`_
        :type new_close_timeout: int or None
        :param new_stream_buffer_maxlen: Set a max len for the `stream_buffer`. Only used in combination with a non generic
                                     `stream_buffer`. The generic `stream_buffer` uses always the value of
                                     `BinanceWebSocketApiManager()`.
        :type new_stream_buffer_maxlen: int or None
        :return: new_stream_id or 'False'
        """
        # starting a new socket and stop the old stream not before the new stream received its first record
        new_stream_id = self.create_stream(new_channels,
                                           new_markets,
                                           new_stream_label,
                                           new_stream_buffer_name,
                                           new_api_key,
                                           new_api_secret,
                                           new_symbols,
                                           new_output,
                                           new_ping_interval,
                                           new_ping_timeout,
                                           new_close_timeout,
                                           new_stream_buffer_maxlen)
        if self.wait_till_stream_has_started(new_stream_id):
            self.stop_stream(stream_id=stream_id, delete_listen_key=False)
        return new_stream_id

    def run(self):
        """
        This method overloads `threading.run()` and starts management threads
        """
        thread_frequent_checks = threading.Thread(target=self._frequent_checks, name="frequent_checks")
        thread_frequent_checks.start()
        thread_keepalive_streams = threading.Thread(target=self._keepalive_streams, name="keepalive_streams")
        thread_keepalive_streams.start()

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
        logger.debug("BinanceWebSocketApiManager.set_heartbeat(" + str(stream_id) + ")")
        try:
            self.stream_list[stream_id]['last_heartbeat'] = time.time()
            self.stream_list[stream_id]['status'] = "running"
        except KeyError:
            pass

    def set_ringbuffer_error_max_size(self, max_size):
        """
        How many error messages should be kept in the ringbuffer?

        :param max_size: Max entries of error messages in the ringbuffer.
        :type max_size: int
        :return: bool
        """
        self.ringbuffer_error_max_size = int(max_size)

    def set_ringbuffer_result_max_size(self, max_size):
        """
        How many result messages should be kept in the ringbuffer?

        :param max_size: Max entries of result messages in the ringbuffer.
        :type max_size: int
        :return: bool
        """
        self.ringbuffer_result_max_size = int(max_size)

    def set_socket_is_not_ready(self, stream_id: str) -> None:
        """
        Set `socket_is_ready` for a specific stream to False.

        :param stream_id: id of the stream
        :type stream_id: str
        """
        logger.debug(f"BinanceWebSocketApiManager.set_socket_is_not_ready({stream_id}){self.get_debug_log()}")
        self.socket_is_ready[stream_id] = False

    def set_socket_is_ready(self, stream_id: str) -> None:
        """
        Set `socket_is_ready` for a specific stream to True.

        :param stream_id: id of the stream
        :type stream_id: str
        """
        logger.debug(f"BinanceWebSocketApiManager.set_socket_is_ready({stream_id}){self.get_debug_log()}")
        self.socket_is_ready[stream_id] = True

    def set_stream_label(self, stream_id, stream_label=None):
        """
        Set a stream_label by stream_id

        :param stream_id: id of the stream
        :type stream_id: str
        :param stream_label: stream_label to set
        :type stream_label: str
        """
        self.stream_list[stream_id]['stream_label'] = stream_label

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
        :type stream_id: str
        """
        logger.debug(f"BinanceWebSocketApiManager.set_restart_request({stream_id}){self.get_debug_log()}")
        try:
            if self.restart_requests[stream_id]['last_restart_time'] + self.restart_timeout > time.time():
                logger.debug(f"BinanceWebSocketApiManager.set_restart_request() - last_restart_time timeout, "
                             f"initiate new")
                return False
        except KeyError:
            pass
        logger.debug(f"BinanceWebSocketApiManager.set_restart_request() - creating new request")
        self.restart_requests[stream_id] = {'status': "new",
                                            'initiated': None}
        return True

    def split_payload(self, params, method, max_items_per_request=350):
        """
        Sending more than 8000 chars via websocket.send() leads to a connection loss, 350 list elements is a good limit
        to keep the payload length under 8000 chars and avoid reconnects

        :param params: params of subscribe payload
        :type params: list
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

        Take a look into the
        `Wiki <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service>`_
        to see how this works!

        :param host: listening ip address, use 0.0.0.0 or a specific address (default: 127.0.0.1)
        :type host: str
        :param port: listening port number (default: 64201)
        :type port: int
        :param warn_on_update: set to `False` to disable the update warning
        :type warn_on_update: bool
        """
        thread = threading.Thread(target=self._start_monitoring_api_thread,
                                  args=(host, port, warn_on_update),
                                  name="monitoring_api")
        thread.start()
        return True

    def stop_manager_with_all_streams(self):
        """
        Stop the BinanceWebSocketApiManager with all streams and management threads
        """
        logger.info("BinanceWebSocketApiManager.stop_manager_with_all_streams() - Stopping "
                    "unicorn_binance_websocket_api_manager " + self.version + " ...")
        for stream_id in self.stream_list:
            self.stop_stream(stream_id)
        # stop monitoring API services
        self.stop_monitoring_api()
        # send signal to all threads
        self.stop_manager_request = True

    def stop_monitoring_api(self):
        """
        Stop the monitoring API service

        :return: bool
        """
        try:
            if not isinstance(self.monitoring_api_server, bool):
                self.monitoring_api_server.stop()
                return True
        except AttributeError as error_msg:
            logger.info("BinanceWebSocketApiManager.stop_monitoring_api() - can not execute "
                        "self.monitoring_api_server.stop() - info: " + str(error_msg))
            return False

    def stop_stream(self, stream_id, delete_listen_key=True):
        """
        Stop a specific stream

        :param stream_id: id of a stream
        :type stream_id: str
        :param delete_listen_key: If set to `True` (default), the `listen_key` gets deleted. Set to `False` if you run
                                  more than one userData stream with this `listen_key`!
        :type delete_listen_key: str
        :return: bool
        """
        # stop a specific stream by stream_id
        logger.info(f"BinanceWebSocketApiManager.stop_stream({stream_id}){self.get_debug_log()}")
        try:
            self.stream_list[stream_id]['stop_request'] = True
        except KeyError:
            return False
        try:
            del self.restart_requests[stream_id]
        except KeyError:
            pass
        if delete_listen_key:
            self.delete_listen_key_by_stream_id(stream_id)
        try:
            loop = self.get_event_loop_by_stream_id(stream_id)
            try:
                if loop.is_running():
                    logger.debug(f"BinanceWebSocketApiManager.stop_stream({stream_id}) - Closing event_loop "
                                 f"of stream_id {stream_id}")
                    loop.close()
            except AttributeError as error_msg:
                logger.debug(f"BinanceWebSocketApiManager.stop_stream({stream_id}) - AttributeError - {error_msg}")
        except RuntimeError as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.stop_stream({stream_id}) - RuntimeError - {error_msg}")
        except RuntimeWarning as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.stop_stream({stream_id}) - RuntimeWarning - {error_msg}")
        # Test (moved to connection and sockets
        # self.stream_is_stopping(stream_id)
        return True

    def stop_stream_as_crash(self, stream_id):
        """
        Stop a specific stream with 'crashed' status

        :param stream_id: id of a stream
        :type stream_id: str
        :return: bool
        """
        # stop a specific stream by stream_id
        logger.critical(f"BinanceWebSocketApiManager.stop_stream_as_crash({stream_id}){self.get_debug_log()}")
        try:
            del self.restart_requests[stream_id]
        except KeyError:
            pass
        try:
            self.stream_list[stream_id]['crash_request'] = True
        except KeyError:
            return False
        try:
            loop = self.get_event_loop_by_stream_id(stream_id)
            try:
                if loop.is_running():
                    logger.debug(f"BinanceWebSocketApiManager.stop_stream_as_crash({stream_id}) - Closing event_loop "
                                 f"of stream_id {stream_id}")
                    loop.close()
            except AttributeError as error_msg:
                logger.debug(f"BinanceWebSocketApiManager.stop_stream_as_crash({stream_id}) - AttributeError - "
                             f"{error_msg}")
        except RuntimeError as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.stop_stream_as_crash({stream_id}) - RuntimeError - {error_msg}")
        except RuntimeWarning as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.stop_stream_as_crash({stream_id}) - RuntimeWarning - {error_msg}")
        return True

    def stream_is_crashing(self, stream_id, error_msg=False):
        """
        If a stream can not heal itself in cause of wrong parameter (wrong market, channel type) it calls this method

        :param stream_id: id of a stream
        :type stream_id: str
        :param error_msg: Error msg to add to the stream status!
        :type error_msg: str
        """
        logger.critical(f"BinanceWebSocketApiManager.stream_is_crashing({stream_id}){self.get_debug_log()}")
        if self.stream_list[stream_id]['last_stream_signal'] is not None and \
                self.stream_list[stream_id]['last_stream_signal'] != "DISCONNECT":
            self.process_stream_signals("DISCONNECT", stream_id)
            self.stream_list[stream_id]['last_stream_signal'] = "DISCONNECT"
        self.stream_list[stream_id]['has_stopped'] = time.time()
        self.stream_list[stream_id]['status'] = "crashed"
        self.set_socket_is_ready(stream_id)  # necessary to release `create_stream()`
        if error_msg:
            self.stream_list[stream_id]['status'] += " - " + str(error_msg)

    def stream_is_stopping(self, stream_id):
        """
        Streams report with this call their shutdowns

        :param stream_id: id of a stream
        :type stream_id: str
        :return: bool
        """
        logger.info(f"BinanceWebSocketApiManager.stream_is_stopping({stream_id}){self.get_debug_log()}")

        try:
            self.stream_list[stream_id]['has_stopped'] = time.time()
            self.stream_list[stream_id]['status'] = "stopped"
            return True
        except KeyError:
            return False

    def subscribe_to_stream(self, stream_id, channels=[], markets=[]):
        """
        Subscribe channels and/or markets to an existing stream

        If you provide one channel and one market, then every subscribed market is going to get added to the new channel
        and all subscribed channels are going to get added to the new market!

        `How are the parameter `channels` and `markets` used with
        `subscriptions <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream>`_

        :param stream_id: id of a stream
        :type stream_id: str
        :param channels: provide the channels you wish to stream
        :type channels: str, tuple, list, set
        :param markets: provide the markets you wish to stream
        :type markets: str, tuple, list, set
        :return: bool
        """
        logger.info(f"BinanceWebSocketApiManager.subscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                    f", " + str(markets) + f"){self.get_debug_log()} - started ... -")
        try:
            if type(channels) is str:
                channels = [channels]
            if type(markets) is str:
                markets = [markets]
            if type(channels) is set:
                channels = list(channels)
            if type(markets) is set:
                markets = list(markets)
        except KeyError:
            logger.error("BinanceWebSocketApiManager.subscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                         ", " + str(markets) + ") KeyError: setting a restart request for this stream ...")
            self.stream_is_stopping(stream_id)
            self.set_restart_request(stream_id)
            return False
        if type(self.stream_list[stream_id]['channels']) is str:
            self.stream_list[stream_id]['channels'] = [self.stream_list[stream_id]['channels']]
        if type(self.stream_list[stream_id]['markets']) is str:
            self.stream_list[stream_id]['markets'] = [self.stream_list[stream_id]['markets']]
        if type(self.stream_list[stream_id]['channels']) is set:
            self.stream_list[stream_id]['channels'] = list(self.stream_list[stream_id]['channels'])
        if type(self.stream_list[stream_id]['markets']) is set:
            self.stream_list[stream_id]['markets'] = list(self.stream_list[stream_id]['markets'])

        self.stream_list[stream_id]['channels'] = list(set(self.stream_list[stream_id]['channels'] + channels))
        markets_new = []
        for market in markets:
            if "!" in market \
                    or market == "allMiniTickers" \
                    or market == "allTickers" \
                    or market == "blockheight" \
                    or market == "$all":
                markets_new.append(market)
            else:
                if self.is_exchange_type('dex'):
                    markets_new.append(str(market).upper())
                elif self.is_exchange_type('cex'):
                    markets_new.append(str(market).lower())
        self.stream_list[stream_id]['markets'] = list(set(self.stream_list[stream_id]['markets'] + markets_new))
        payload = self.create_payload(stream_id, "subscribe",
                                      channels=self.stream_list[stream_id]['channels'],
                                      markets=self.stream_list[stream_id]['markets'])
        self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
        # control subscription limit:
        # https://github.com/binance-exchange/binance-official-api-docs/blob/5fccfd572db2f530e25e302c02be5dec12759cf9/CHANGELOG.md#2020-04-23
        if self.stream_list[stream_id]['subscriptions'] > self.max_subscriptions_per_stream:
            self.stop_stream_as_crash(stream_id)
            error_msg = "The limit of " + str(self.max_subscriptions_per_stream) + " subscriptions per stream has " \
                        "been exceeded!"
            logger.critical(f"BinanceWebSocketApiManager.subscribe_to_stream({str(stream_id)}) "
                            f"Info: {str(error_msg)}")
            self.stream_is_crashing(stream_id, error_msg)
            if self.throw_exception_if_unrepairable:
                raise StreamRecoveryError("stream_id " + str(stream_id) + ": " + str(error_msg))
            return False

        for item in payload:
            self.stream_list[stream_id]['payload'].append(item)
        logger.info("BinanceWebSocketApiManager.subscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                    ", " + str(markets) + ") finished ...")
        return True

    def unsubscribe_from_stream(self, stream_id, channels=None, markets=None):
        """
        Unsubscribe channels and/or markets to an existing stream

        If you provide one channel and one market, then all subscribed markets from the specific channel and all
        subscribed channels from the specific markets are going to be removed!

        `How are the parameter `channels` and `markets` used with
        `subscriptions <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream>`_

        :param stream_id: id of a stream
        :type stream_id: str
        :param channels: provide the channels you wish to stream
        :type channels: str, tuple, list, set
        :param markets: provide the markets you wish to stream
        :type markets: str, tuple, list, set
        :return: bool
        """
        logger.info(f"BinanceWebSocketApiManager.unsubscribe_from_stream(" + str(stream_id) + ", " + str(channels) +
                    f", " + str(markets) + f"){self.get_debug_log()} - started ... -")
        if markets is None:
            markets = []
        if channels is None:
            channels = []
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
        for i in range(len(markets)):
            markets[i] = markets[i].lower()
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
        self.stream_list[stream_id]['subscriptions'] = self.get_number_of_subscriptions(stream_id)
        logger.info("BinanceWebSocketApiManager.unsubscribe_to_stream(" + str(stream_id) + ", " + str(channels) +
                    ", " + str(markets) + ") finished ...")
        return True

    def wait_till_stream_has_started(self, stream_id):
        """
        Returns `True` as soon a specific stream has started and received its first stream data

        :param stream_id: id of a stream
        :type stream_id: str

        :return: bool
        """
        logger.debug(f"BinanceWebSocketApiManager.wait_till_stream_has_started({stream_id}) started!")
        try:
            while self.stream_list[stream_id]['last_heartbeat'] is None:
                time.sleep(0.1)
            logger.debug(f"BinanceWebSocketApiManager.wait_till_stream_has_started({stream_id}) finished with `True`!")
            return True
        except KeyError:
            logger.debug(f"BinanceWebSocketApiManager.wait_till_stream_has_started({stream_id}) finished with `False`!")
            return False

    def wait_till_stream_has_stopped(self, stream_id):
        """
        Returns `True` as soon a specific stream has stopped itself

        :param stream_id: id of a stream
        :type stream_id: str

        :return: bool
        """
        logger.debug(f"BinanceWebSocketApiManager.wait_till_stream_has_stopped({stream_id}) started!")
        try:
            while self.stream_list[stream_id]['status'] != "stopped":
                time.sleep(0.1)
            logger.debug(f"BinanceWebSocketApiManager.wait_till_stream_has_stopped({stream_id}) finished with `True`!")
            return True
        except KeyError:
            logger.debug(f"BinanceWebSocketApiManager.wait_till_stream_has_stopped({stream_id}) finished with `False`!")
            return False
