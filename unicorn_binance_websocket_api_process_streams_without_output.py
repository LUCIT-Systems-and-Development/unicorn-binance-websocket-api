#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api_process_streams_without_output.py
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

from unicorn_binance_websocket_api.unicorn_fy import UnicornFy


class BinanceWebSocketApiProcessStreams():
    @staticmethod
    def process_stream_data(received_stream_data_json):
        #
        #  START HERE!
        #
        # `received_stream_data_json` contains one record of raw data from the stream
        # print it and you see the data like its given from Binance, its hard to work with them, because keys of
        # parameters are changing from stream to stream and they are not self explaining.
        #
        # So if you want, you can use the class `UnicornFy`, it converts the json to a dict and prepares the values.
        # `depth5` for example doesnt include the symbol, but the unicornfied set includes them, because the class
        # extracts it from the channel name, makes it upper size and adds it to the returned values.. just print both
        # to see the difference.
        unicorn_fied_stream_data = UnicornFy.binance_websocket(received_stream_data_json)

        # Now you can call different methods for different `channels`, here called `event_types`.
        # Its up to you if you call the methods in the bottom of this file or to call other classes which do what
        # ever you want to be done.
        try:
            if unicorn_fied_stream_data['event_type'] == "aggTrade":
                BinanceWebSocketApiProcessStreams.aggtrade(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data['event_type'] == "trade":
                BinanceWebSocketApiProcessStreams.trade(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data['event_type'] == "kline":
                BinanceWebSocketApiProcessStreams.kline(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data['event_type'] == "miniTicker":
                BinanceWebSocketApiProcessStreams.miniticker(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data['event_type'] == "ticker":
                BinanceWebSocketApiProcessStreams.ticker(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data['event_type'] == "depth":
                BinanceWebSocketApiProcessStreams.miniticker(unicorn_fied_stream_data)
            else:
                BinanceWebSocketApiProcessStreams.anything_else(unicorn_fied_stream_data)
        except KeyError as error_msg:
            print("received_data: " + str(received_stream_data_json), "error_msg: " + str(error_msg))

    @staticmethod
    def aggtrade(stream_data):
        # print `aggTrade` data
        pass

    @staticmethod
    def trade(stream_data):
        # print `trade` data
        pass

    @staticmethod
    def kline(stream_data):
        # print `kline` data
        pass

    @staticmethod
    def miniticker(stream_data):
        # print `miniTicker` data
        pass

    @staticmethod
    def ticker(stream_data):
        # print `ticker` data
        pass

    @staticmethod
    def depth(stream_data):
        # print `depth` data
        pass

    @staticmethod
    def outboundAccountInfo(stream_data):
        # print `outboundAccountInfo` data from userData stream
        pass

    @staticmethod
    def executionReport(stream_data):
        # print `executionReport` data from userData stream
        pass

    @staticmethod
    def anything_else(stream_data):
        pass
