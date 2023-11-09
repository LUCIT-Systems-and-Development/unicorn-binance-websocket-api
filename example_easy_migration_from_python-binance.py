#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_easy_migration_from_python-binance.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech)
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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import time


api_key = ""
api_secret = ""


def book_ticker(msg):
    print("book_ticker: " + str(msg))


def order_status(msg):
    print("order_status: " + str(msg))


# To use this library you need a valid UNICORN Binance Suite License:
# https://medium.lucit.tech/-87b0088124a8
bwsm = BinanceWebSocketApiManager()

book_ticker_id = bwsm.create_stream("bookTicker", 'bnbbusd', stream_buffer_name=True)
user_stream_id = bwsm.create_stream('arr', '!userData', api_key=api_key, api_secret=api_secret, stream_buffer_name=True)

while True:
    msg = bwsm.pop_stream_data_from_stream_buffer(book_ticker_id)
    if msg:
        book_ticker(msg)
    msg = bwsm.pop_stream_data_from_stream_buffer(user_stream_id)
    if msg:
        order_status(msg)
    time.sleep(0.01)
