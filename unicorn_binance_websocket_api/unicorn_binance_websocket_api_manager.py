#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_manager.py
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

from .unicorn_binance_websocket_api_socket import BinanceWebSocketApiSocket
from .unicorn_binance_websocket_api_restclient import BinanceWebSocketApiRestclient
from .unicorn_binance_websocket_api_restserver import BinanceWebSocketApiRestServer
from cheroot import wsgi
from datetime import datetime
from flask import Flask
from flask_restful import Api
import asyncio
import colorama
import copy
import logging
import requests
import sys
import threading
import time
import uuid


class BinanceWebSocketApiManager(threading.Thread):
    """
    A python API to handle the Binance websocket API

    Binance websocket API documentation:
    https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md
    https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md

    :param process_stream_data: Provide a function/method to process the received webstream data. The function
                                will be called with one variable like `process_stream_data(data)` where
                                data` cointains the raw_stream_data. If not provided, the raw stream_data will get
                                stored in the stream_buffer.
    :type process_stream_data: function
    """

    def __init__(self, process_stream_data=False):
        threading.Thread.__init__(self)
        self.version = "1.3.7.dev"
        self.websocket_base_uri = "wss://stream.binance.com:9443/"
        if process_stream_data is False:
            # no special method to process stream data provided, so we use write_to_stream_buffer:
            self.process_stream_data = self.add_to_stream_buffer
        else:
            # use the provided method to process stream data:
            self.process_stream_data = process_stream_data
        self.stop_manager_request = None
        self._frequent_checks_restart_request = None
        self._keepalive_streams_restart_request = None
        self.api_key = False
        self.api_secret = False
        self.frequent_checks_list = {}
        self.keep_max_received_last_second_entries = 5
        self.keepalive_streams_list = {}
        self.most_receives_per_second = 0
        self.monitoring_api_server = False
        self.monitoring_total_received_bytes = 0
        self.monitoring_total_receives = 0
        self.reconnects = 0
        self.restart_requests = {}
        self.start_time = time.time()
        self.stream_buffer = []
        self.stream_buffer_byte_size = 0
        self.last_entry_added_to_stream_buffer = 0
        self.last_monitoring_check = time.time()
        self.last_update_check_github = {'timestamp': time.time(),
                                         'status': None}
        self.stream_list = {}
        self.total_received_bytes = 0
        self.total_receives = 0
        self.websocket_list = {}
        self.binance_api_status = {'weight': None,
                                   'timestamp': 0,
                                   'status_code': None}
        self.start()
        colorama.init()

    def _add_socket_to_socket_list(self, stream_id, channels, markets):
        # create a list entry for new sockets
        self.stream_list[stream_id] = {'exchange': "binance",
                                       'stream_id': copy.deepcopy(stream_id),
                                       'channels': copy.deepcopy(channels),
                                       'markets': copy.deepcopy(markets),
                                       'api_key': copy.deepcopy(self.api_key),
                                       'api_secret': copy.deepcopy(self.api_secret),
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
                                       'last_static_ping_listen_key': 0,
                                       'listen_key': False,
                                       'listen_key_cache_time': 30 * 60,
                                       'processed_receives_statistic': {}}
        logging.debug("BinanceWebSocketApiManager->_add_socket_to_socket_list(" +
                      str(stream_id) + ", " + str(channels) + ", " + str(markets) + ")")

    def _create_stream_thread(self, loop, stream_id, channels, markets, restart=False):
        # co function of self.create_stream to create a thread for the socket and to manage the coroutine
        if restart is False:
            self._add_socket_to_socket_list(stream_id, channels, markets)
        asyncio.set_event_loop(loop)
        binance_websocket_api_socket = BinanceWebSocketApiSocket(self, loop, stream_id, channels, markets)
        try:
            loop.run_until_complete(binance_websocket_api_socket.start_socket())
        finally:
            loop.close()

    def _frequent_checks(self):
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
                                self.stream_list[stream_id]['receives_statistic_last_second'][
                                    'most_receives_per_second']:
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
                    delete_index = []
                    if len(self.stream_list[stream_id]['receives_statistic_last_second']['entries']) > self.keep_max_received_last_second_entries:
                        for timestamp_key in self.stream_list[stream_id]['receives_statistic_last_second']['entries']:
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
                                binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.stream_list[stream_id]['api_key'],
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

    def _fill_up_space(self, demand_of_chars, string):
        blanks_pre = ""
        blanks_post = ""
        demand_of_blanks = demand_of_chars - len(str(string)) - 1
        while len(blanks_pre) < demand_of_blanks:
            blanks_pre += " "
            blanks_post = " "
        return blanks_pre + str(string) + blanks_post

    def _keepalive_streams(self):
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

    def _start_monitoring_api(self, host, port, ssl_context):
        logging.info("starting monitoring API server ...")
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(BinanceWebSocketApiRestServer, "/status/<string:statusformat>",
                         resource_class_kwargs={'handler_binance_websocket_api_manager': self})
        try:
            dispatcher = wsgi.PathInfoDispatcher({'/': app})
            self.monitoring_api_server = wsgi.WSGIServer((host, port), dispatcher)
            self.monitoring_api_server.start()
        except RuntimeError as error_msg:
            logging.error("monitoring API server is going down! - info: " + str(error_msg))

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
        self.stream_buffer_byte_size += sys.getsizeof(stream_data)

    def add_total_received_bytes(self, size):
        # add received bytes to the total received bytes statistic
        self.total_received_bytes += int(size)

    def create_stream(self, channels, markets):
        """
        Create a websocket stream

        :param channels: provide the channels you wish to stream
        :type channels: str or tuple

        :param markets: provide the markets you wish to stream
        :type markets: str or tuple

        :return: stream_id
        """
        # create a stream
        logging.info("BinanceWebSocketApiManager->create_stream(" + str(channels) + ", " + str(markets) + ")")
        stream_id = uuid.uuid4()
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self._create_stream_thread, args=(loop, stream_id, channels, markets))
        thread.start()
        return stream_id

    def create_websocket_uri(self, channels, markets, stream_id=False, api_key=False, api_secret=False):
        """
        Create a websocket URI

        :param channels: provide the channels to create the URI
        :type channels: str or tuple

        :param markets: provide the markets to create the URI
        :type markets: str or tuple

        :param stream_id: provide a stream_id (only needed for userData Streams (acquiring a listenKey)
        :type stream_id: uuid

        :param api_key: provide a valid Binance API key
        :type api_key: str

        :param api_secret: provide a valid Binance API secret
        :type api_secret: str

        :return: str
        """
        if type(channels) is str:
            channels = [channels]
        if type(markets) is str:
            markets = [markets]
        if len(channels) == 1:
            if "arr" in channels:
                query = "ws/"
            else:
                query = "stream?streams="
        else:
            query = "stream?streams="
        for channel in channels:
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
            for market in markets:
                if market == "!userData":
                    if stream_id is not False:
                        # only execute this code block with a provided stream_id
                        response = self.get_listen_key_from_restclient(stream_id, api_key, api_secret)
                        try:
                            if response['code'] == -2014 or response['code'] == -2015:
                                return response
                            else:
                                logging.critical("Found new error code from restclient: " + str(response))
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
                            return False
                else:
                    if market == "!userData" or market == "!miniTicker":
                        query += market + "@" + channel + "/"
                    else:
                        query += market.lower() + "@" + channel + "/"
        uri = self.websocket_base_uri + str(query)
        return uri

    def delete_listen_key_by_stream_id(self, stream_id):
        """
        Delete a binance listen_key from a specific !userData stream

        :param stream_id: id of a !userData stream
        :type stream_id: uuid
        """
        if self.stream_list[stream_id]['listen_key'] is not False:
            logging.info("BinanceWebSocketApiManager->stop_manager_with_all_streams(" + str(
                stream_id) + ")->delete_listen_key")
            binance_websocket_api_restclient = BinanceWebSocketApiRestclient(self.stream_list[stream_id]['api_key'],
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
        # how much receives did we have last second?
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

    def get_human_bytesize(self, bytes):
        if bytes > 1024 * 1024 * 1024:
            bytes = str(round(bytes / (1024 * 1024 * 1024), 2)) + " gB"
        elif bytes > 1024 * 1024:
            bytes = str(round(bytes / (1024 * 1024), 1)) + " mB"
        elif bytes > 1024:
            bytes = str(int(bytes / 1024)) + " kB"
        return bytes

    def get_human_uptime(self, uptime):
        # formats a timestamp to a human readable output
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
            respond = requests.get('https://api.github.com/repos/unicorn-data-analysis/unicorn-binance-websocket-api/'
                                   'releases/latest')
            latest_release_info = respond.json()
            return latest_release_info
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
        binance_websocket_api_restclient = BinanceWebSocketApiRestclient(api_key, api_secret, self.get_version(),
                                                                         self.binance_api_status)
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
        Get the number of received_last_second entries are stored till they get deleted

        :return: int
        """
        return self.keep_max_received_last_second_entries

    def get_monitoring_status_icinga(self, **kwargs):
        """
        Get status and perfdata to monitor and collect metrics with ICINGA/Nagios

        status: OK, WARNING, CRITICAL
            WARNING: on restarts, available updates
            CRITICAL: crashed streams

        perfdata:
        - average receives per second since last status check
        - average speed per second since last status check
        - received giga byte since start
        - stream_buffer size
        - stream_buffer items
        - reconnects
        - uptime

        :return: dict (text, time, return_code)
        """
        result = self.get_monitoring_status_plain()
        if len(result['update_msg']) > 0:
            result['update_msg'] = " - " + result['update_msg']
        check_message = "BINANCE WEBSOCKETS - " + result['status_text'] + ": O:" + str(result['active_streams']) + \
                        "/R:" + str(result['restarting_streams']) + "/C:" + str(result['crashed_streams']) + "/S:" + \
                        str(result['stopped_streams']) + result['update_msg'] + " | " + "receives_per_second=" + \
                        str(int(result['average_receives_per_second'])) + ";;;0 kb_per_second=" + \
                        str(result['average_speed_per_second']) + ";;;0 " \
                        "received_mb=" + str(result['total_received_mb']) + ";;;0 stream_buffer_mb=" + \
                        str(int(result['stream_buffer_mb'])) + ";;;0 stream_buffer_items=" + \
                        str(result['stream_buffer_items']) + ";;;0 reconnects=" + str(result['reconnects']) + ";;;0 " \
                        "uptime_days=" + str(result['uptime']) + ";;;0"
        status = {'text': check_message,
                  'time': int(result['timestamp']),
                  'return_code': result['return_code']}
        return status

    def get_monitoring_status_plain(self):
        """
        Get plain monitoring status data:
        active_streams, crashed_streams, restarting_streams, stopped_streams, return_code, status_text,
        timestamp, update_msg, average_receives_per_second, average_speed_per_second, total_received_mb,
        stream_buffer_items, stream_buffer_mb, reconnects, uptime

        :return: dict
        """
        result = {}
        result['active_streams'] = 0
        result['crashed_streams'] = 0
        result['restarting_streams'] = 0
        result['return_code'] = 0
        result['status_text'] = "OK"
        result['stopped_streams'] = 0
        result['timestamp'] = time.time()
        result['update_msg'] = ""
        time_period = result['timestamp'] - self.last_monitoring_check
        for stream_id in self.stream_list:
            if self.stream_list[stream_id]['status'] == "running":
                result['active_streams'] += 1
            elif self.stream_list[stream_id]['status'] == "stopped":
                result['stopped_streams'] += 1
            elif self.stream_list[stream_id]['status'] == "restarting":
                result['restarting_streams'] += 1
            elif "crashed" in self.stream_list[stream_id]['status']:
                result['crashed_streams'] += 1
        if self.is_update_availabe():
            result['update_msg'] = "Update " + str(self.get_latest_version()) + " available!"
            result['status_text'] = "WARNING"
            result['return_code'] = 1
        if result['crashed_streams'] > 0:
            result['status_text'] = "CRITICAL"
            result['return_code'] = 2
        elif result['restarting_streams'] > 0:
            result['status_text'] = "WARNING"
            result['return_code'] = 1
        result['average_receives_per_second'] = ((self.total_receives - self.monitoring_total_receives) /
                                                 time_period).__round__(2)
        result['average_speed_per_second'] = (((self.total_received_bytes - self.monitoring_total_received_bytes) /
                                               time_period) / 1024).__round__(2)
        result['total_received_mb'] = (self.get_total_received_bytes() / (1024 * 1024)).__round__(2)
        result['stream_buffer_items'] = str(self.get_stream_buffer_length())
        result['stream_buffer_mb'] = (self.get_stream_buffer_byte_size() / (1024 * 1024)).__round__(2)
        result['reconnects'] = self.get_reconnects()
        self.monitoring_total_receives = self.get_total_receives()
        self.monitoring_total_received_bytes = self.get_total_received_bytes()
        self.last_monitoring_check = result['timestamp']
        result['uptime'] = ((result['timestamp'] - self.start_time) / (60*60*24)).__round__(2)
        return result

    def get_reconnects(self):
        """
        Get the number of total reconnects

        :return: int
        """
        return self.reconnects

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
        return self.stream_buffer_byte_size

    def get_stream_buffer_length(self):
        """
        Get the current number of data in the stream_buffer

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
        :type channels: str or tuple

        :param markets: provide the markets to create the URI
        :type markets: str or tuple

        :return: int
        """
        uri = self.create_websocket_uri(channels, markets)
        return len(uri)

    def increase_processed_receives_statistic(self, stream_id):
        # for every receive we call this method to increase the receives statistics
        current_timestamp = int(time.time())
        # for every received row of data, the stream counts + 1 in to the statistic (average values)
        self.stream_list[stream_id]['processed_receives_total'] += 1
        # increase for every received row the global received stats for the current second
        try:
            self.stream_list[stream_id]['receives_statistic_last_second']['entries'][current_timestamp] += 1
        except KeyError:
            self.stream_list[stream_id]['receives_statistic_last_second']['entries'][current_timestamp] = 1
        # increase `total_receives`
        self.total_receives += 1

    def increase_reconnect_counter(self, stream_id):
        # at every reconnect we call this method to increase the reconnect statistic
        self.stream_list[stream_id]['logged_reconnects'].append(time.time())
        self.stream_list[stream_id]['reconnects'] += 1
        self.reconnects += 1

    def is_manager_stopping(self):
        """
        Returns `True` if the manager has a stop request, 'False' if not.

        :return: bool
        """
        if self.stop_manager_request is None:
            return False
        else:
            return True

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

    def is_websocket_uri_length_valid(self, channels, markets):
        """
        Is the websocket URI length valid?

        A test with https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/tools/test_max_websocket_uri_length.py
        indicates that the allowed max length of an URI to binance websocket server is 8004 characters.

        :return: bool
        """
        uri = self.create_websocket_uri(channels, markets)
        if len(uri) >= 8004:
            return False
        else:
            return True

    def pop_stream_data_from_stream_buffer(self):
        """
        Get oldest entry from stream_buffer and remove from stack (FIFO stack)

        :return: raw_stream_data (set) or False
        """
        try:
            stream_data = self.stream_buffer.pop(0)
            self.stream_buffer_byte_size -= sys.getsizeof(stream_data)
            return stream_data
        except IndexError:
            return False

    def print_stream_info(self, stream_id):
        """
        Print all infos about a specific stream, helps debugging :)

        :param stream_id: id of a stream
        :type stream_id: uuid
        :return: bool
        """
        restart_requests_row = ""
        stream_row_color_prefix = ""
        stream_row_color_suffix = ""
        binance_api_status_row = ""
        status_row = ""
        last_static_ping_listen_key = ""
        stream_info = self.get_stream_info(stream_id)

        if len(self.stream_list[stream_id]['logged_reconnects']) > 0:
            logged_reconnects_row = "\r\n logged_reconnects: "
            row_prefix = ""
            for timestamp in self.stream_list[stream_id]['logged_reconnects']:
                logged_reconnects_row += row_prefix + datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d, %H:%M:%S UTC')
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
        try:
            if self.restart_requests[stream_id]['status']:
                restart_requests_row = " restart_request: " + self.restart_requests[stream_id]['status'] + "\r\n"
        except KeyError:
            pass
        if self.stream_list[stream_id]['markets'] == "!userData":
            last_static_ping_listen_key = " last_static_ping_listen_key: " + str(self.stream_list[stream_id]['last_static_ping_listen_key']) + "\r\n"
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
            uptime = self.get_human_uptime(stream_info['processed_receives_statistic']['uptime'])
            print("===============================================================================================\r\n"
                  " exchange:", str(stream_info['exchange']), "\r\n"
                  " stream_id:", str(stream_id), "\r\n"
                  " channels:", str(stream_info['channels']), "\r\n"
                  " markets:", str(stream_info['markets']), "\r\n" +
                  str(status_row) +
                  " start_time:", str(stream_info['start_time']), "\r\n"
                  " uptime:", str(uptime),
                  "since " + str(
                      datetime.utcfromtimestamp(stream_info['start_time']).strftime('%Y-%m-%d, %H:%M:%S UTC')) + "\r\n" +
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
                  " processed_receives:",
                  str(stream_info['processed_receives_total']), "\r\n" +
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
                  " stream_receives_per_month:",
                  str(stream_info['processed_receives_statistic']['stream_receives_per_month'].__round__(3)), "\r\n"
                  " stream_receives_per_year:",
                  str(stream_info['processed_receives_statistic']['stream_receives_per_year'].__round__(3)), "\r\n"
                  "===============================================================================================\r\n")
        except KeyError:
            self.print_stream_info(stream_id)

    def print_summary(self):
        """
        Print an overview of all streams
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
        streams_with_stop_request = 0
        stream_rows = ""
        crashed_streams_row = ""
        binance_api_status_row = ""
        received_bytes_per_x_row = ""
        streams_with_stop_request_row = ""
        stream_buffer_row = ""
        for stream_id in self.stream_list:
            stream_row_color_prefix = ""
            stream_row_color_suffix = ""
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
                self._fill_up_space(14, self.get_stream_receives_last_second(stream_id)) + "|" + \
                self._fill_up_space(13, stream_statistic['stream_receives_per_second'].__round__(2)) + "|" + \
                self._fill_up_space(18, self.stream_list[stream_id]['receives_statistic_last_second']['most_receives_per_second']) + "|" + \
                stream_row_color_prefix + \
                self._fill_up_space(8, len(self.stream_list[stream_id]['logged_reconnects'])) + \
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
            crashed_streams_row = stream_row_color_prefix + " crashed_streams: " + str(crashed_streams) + stream_row_color_suffix + "\r\n"
        total_received_bytes = str(self.get_total_received_bytes()) + " (" + str(
            self.get_human_bytesize(self.get_total_received_bytes())) + ")"
        try:
            received_bytes_per_second = self.get_total_received_bytes() / (time.time() - self.start_time)
            received_bytes_per_x_row += str((received_bytes_per_second / 1024).__round__(2)) + " kB/s (per day " + \
                                        str(((received_bytes_per_second / 1024 / 1024 / 1024) * 60 * 60 * 24).__round__(2)) + " gB)"
            if len(self.stream_buffer) > 50:
                stream_row_color_prefix = "\033[1m\033[34m"
                stream_row_color_suffix = "\033[0m"
                stream_buffer_row += stream_row_color_prefix + " stream_buffer_stored_items: " + str(len(self.stream_buffer)) + "\r\n"
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
                    " exchange:", str(self.stream_list[stream_id]['exchange']), "(lib " + str(self.version) + ")\r\n" +
                    " uptime:", str(self.get_human_uptime(time.time() - self.start_time)), "since " +
                    str(datetime.utcfromtimestamp(self.start_time).strftime('%Y-%m-%d, %H:%M:%S UTC')) + "\r\n" +
                    " streams:", str(streams), "\r\n" +
                    str(active_streams_row) +
                    str(crashed_streams_row) +
                    str(restarting_streams_row) +
                    str(stopped_streams_row) +
                    str(streams_with_stop_request_row) +
                    str(stream_buffer_row) +
                    " total_receives:", str(self.total_receives), "\r\n"
                    " total_received_bytes:", str(total_received_bytes), "\r\n"
                    " total_receiving_speed:", str(received_bytes_per_x_row), "\r\n" +
                    str(binance_api_status_row) +
                    " ---------------------------------------------------------------------------------------------\r\n"
                    "              stream_id               | rec_last_sec | rec_per_sec | most_rec_per_sec | recon\r\n"
                    " ---------------------------------------------------------------------------------------------\r\n"
                    " " + str(stream_rows) +
                    "---------------------------------------------------------------------------------------------\r\n"
                    " all_streams                          |" +
                    self._fill_up_space(14, self.get_all_receives_last_second()) + "|" +
                    self._fill_up_space(13, all_receives_per_second.__round__(2)) + "|" +
                    self._fill_up_space(18, self.most_receives_per_second) + "|" +
                    self._fill_up_space(8, self.reconnects) + "\r\n"
                    " ---------------------------------------------------------------------------------------------\r\n"
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
        :type new_channels: str or tuple

        :param new_markets: the new markets list for the stream
        :type new_markets: str or tuple

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
        # overload inherited threading.run()
        # starting threads
        # start thread for frequent_checks
        thread_frequent_checks = threading.Thread(target=self._frequent_checks)
        thread_frequent_checks.start()
        # start thread for keepalive_streams
        thread_keepalive_streams = threading.Thread(target=self._keepalive_streams)
        thread_keepalive_streams.start()
        time.sleep(5)
        while self.stop_manager_request is None:
            if self._keepalive_streams_restart_request is True:
                # start thread for keepalive_streams
                self._keepalive_streams_restart_request = None
                thread_keepalive_streams = threading.Thread(target=self._keepalive_streams)
                thread_keepalive_streams.start()
            if self._frequent_checks_restart_request is True:
                self._frequent_checks_restart_request = None
                # start thread for frequent_checks
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

    def set_heartbeat(self, stream_id):
        # set heartbeat for a specific thread (should only be done by the stream itself)
        logging.debug("BinanceWebSocketApiManager->set_heartbeat(" + str(stream_id) + ")")
        try:
            self.stream_list[stream_id]['last_heartbeat'] = time.time()
            self.stream_list[stream_id]['status'] = "running"
        except KeyError:
            pass

    def set_keep_max_received_last_second_entries(self, number_of_max_entries):
        # set how much received_last_second entries are stored till they get deleted!
        self.keep_max_received_last_second_entries = number_of_max_entries

    def set_restart_request(self, stream_id):
        self.restart_requests[stream_id] = {'status': "new"}

    def start_monitoring_api(self, host='127.0.0.1', port=64201, ssl_context='adhoc'):
        """
        Start the monitorint API server

        :param host: host name or ip address (default: 127.0.0.1)
        :type host: str

        :param port: port number (default: 64201)
        :type port: int
        """
        thread = threading.Thread(target=self._start_monitoring_api, args=(host, port, ssl_context))
        thread.start()

    def stop_manager_with_all_streams(self):
        """
        Stop the BinanceWebSocketApiManager with all streams and management threads
        """
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
        # if a stream can not heal itself in cause of wrong parameter (wrong market, channel type) it calls this method
        logging.critical("BinanceWebSocketApiManager->stream_is_crashing(" + str(stream_id) + ")")
        self.stream_list[stream_id]['has_stopped'] = time.time()
        self.stream_list[stream_id]['status'] = "crashed"
        if error_msg:
            self.stream_list[stream_id]['status'] += " - " + str(error_msg)

    def stream_is_stopping(self, stream_id):
        # streams report with this call their shutdowns
        logging.debug("BinanceWebSocketApiManager->stream_is_stopping(" + str(stream_id) + ")")
        self.stream_list[stream_id]['has_stopped'] = time.time()
        self.stream_list[stream_id]['status'] = "stopped"

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
