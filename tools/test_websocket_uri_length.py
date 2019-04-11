#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: test_websocket_uri_length.py
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

from websocket import create_connection
import websocket
import time


def binance_test_uri_length(query):
    websocket = create_connection("wss://stream.binance.com:9443/stream?streams=" + query)
    while True:
        result = websocket.recv()
        websocket.close()
        print("Received '%s'\r\n" % result)
        break


markets = ['bnbbtc', 'ethbtc', 'btcusdt', 'bchabcusdt', 'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt',
           'neousdt', 'bnbusdt', 'adabtc', 'ethusdt', 'trxbtc', 'trxbtc', 'bchabcbtc', 'ltcbtc', 'xrpbtc',
           'ontbtc', 'bttusdt', 'eosbtc', 'xlmbtc', 'bttbtc', 'tusdusdt', 'xlmusdt', 'qkcbtc', 'zrxbtc',
           'neobtc', 'adaeth', 'icxusdt', 'btctusd', 'icxbtc', 'btcusdc', 'wanbtc', 'zecbtc', 'wtcbtc',
           'batbtc', 'adabnb', 'etcusdt', 'qtumusdt', 'xmrbtc', 'trxeth', 'adatusd', 'trxxrp', 'trxbnb',
           'dashbtc', 'rvnbnb', 'bchabctusd', 'etcbtc', 'bnbeth', 'ethpax', 'nanobtc', 'xembtc', 'xrpbnb',
           'bchabcpax', 'xrpeth', 'bttbnb', 'ltcbnb', 'agibtc', 'zrxusdt', 'xlmbnb', 'ltceth', 'eoseth',
           'ltctusd', 'polybnb', 'scbtc', 'steembtc', 'trxtusd', 'npxseth', 'kmdbtc', 'polybtc', 'gasbtc',
           'engbtc', 'zileth', 'xlmeth', 'eosbnb', 'xrppax', 'lskbtc', 'npxsbtc', 'xmrusdt', 'ltcpax', 'xmrusdt',
           'ethtusd', 'batusdt', 'mcobtc', 'neoeth', 'bntbtc', 'eostusd', 'lrcbtc', 'funbtc', 'zecusdt',
           'bnbpax', 'linkusdt', 'hceth', 'zrxeth', 'icxeth', 'xmreth', 'neobnb', 'etceth', 'zeceth', 'xmrbnb',
           'wanbnb', 'zrxbnb', 'agibnb', 'funeth', 'arketh', 'engeth']

channels = ['trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'depth5']

streams = []
for market in markets:
    for channel in channels:
        streams.append(market + "@" + channel)

print("generated stream items:", len(streams), "\r\n")

query = ""
round = 0
#start_testing = int(input("start at round (try 484): "))
start_testing = 484
if start_testing != "":
    for stream in streams:
        if round < len(streams):
            query += stream + "/"
            if round >= start_testing:
                print("round:", round)
                try:
                    binance_test_uri_length(query)
                except websocket._exceptions.WebSocketBadStatusException as error_msg:
                    print("error_msg:", error_msg)
                    print("uri length:", str(len("wss://stream.binance.com:9443/stream?streams=" + query)))
                    print("query:")
                    print(query)
                    if "Large" in str(error_msg):
                        print("\r\nfound too long URI!")
                        break
                time.sleep(11)
            round += 1

full_query = "bnbbtc@trade/bnbbtc@kline_1m/bnbbtc@kline_5m/bnbbtc@kline_15m/bnbbtc@kline_30m/bnbbtc@kline_1h/bnbbtc@kline_12h/bnbbtc@depth5/ethbtc@trade/ethbtc@kline_1m/ethbtc@kline_5m/ethbtc@kline_15m/ethbtc@kline_30m/ethbtc@kline_1h/ethbtc@kline_12h/ethbtc@depth5/btcusdt@trade/btcusdt@kline_1m/btcusdt@kline_5m/btcusdt@kline_15m/btcusdt@kline_30m/btcusdt@kline_1h/btcusdt@kline_12h/btcusdt@depth5/bchabcusdt@trade/bchabcusdt@kline_1m/bchabcusdt@kline_5m/bchabcusdt@kline_15m/bchabcusdt@kline_30m/bchabcusdt@kline_1h/bchabcusdt@kline_12h/bchabcusdt@depth5/xrpusdt@trade/xrpusdt@kline_1m/xrpusdt@kline_5m/xrpusdt@kline_15m/xrpusdt@kline_30m/xrpusdt@kline_1h/xrpusdt@kline_12h/xrpusdt@depth5/rvnbtc@trade/rvnbtc@kline_1m/rvnbtc@kline_5m/rvnbtc@kline_15m/rvnbtc@kline_30m/rvnbtc@kline_1h/rvnbtc@kline_12h/rvnbtc@depth5/ltcusdt@trade/ltcusdt@kline_1m/ltcusdt@kline_5m/ltcusdt@kline_15m/ltcusdt@kline_30m/ltcusdt@kline_1h/ltcusdt@kline_12h/ltcusdt@depth5/adausdt@trade/adausdt@kline_1m/adausdt@kline_5m/adausdt@kline_15m/adausdt@kline_30m/adausdt@kline_1h/adausdt@kline_12h/adausdt@depth5/eosusdt@trade/eosusdt@kline_1m/eosusdt@kline_5m/eosusdt@kline_15m/eosusdt@kline_30m/eosusdt@kline_1h/eosusdt@kline_12h/eosusdt@depth5/neousdt@trade/neousdt@kline_1m/neousdt@kline_5m/neousdt@kline_15m/neousdt@kline_30m/neousdt@kline_1h/neousdt@kline_12h/neousdt@depth5/bnbusdt@trade/bnbusdt@kline_1m/bnbusdt@kline_5m/bnbusdt@kline_15m/bnbusdt@kline_30m/bnbusdt@kline_1h/bnbusdt@kline_12h/bnbusdt@depth5/adabtc@trade/adabtc@kline_1m/adabtc@kline_5m/adabtc@kline_15m/adabtc@kline_30m/adabtc@kline_1h/adabtc@kline_12h/adabtc@depth5/ethusdt@trade/ethusdt@kline_1m/ethusdt@kline_5m/ethusdt@kline_15m/ethusdt@kline_30m/ethusdt@kline_1h/ethusdt@kline_12h/ethusdt@depth5/trxbtc@trade/trxbtc@kline_1m/trxbtc@kline_5m/trxbtc@kline_15m/trxbtc@kline_30m/trxbtc@kline_1h/trxbtc@kline_12h/trxbtc@depth5/trxbtc@trade/trxbtc@kline_1m/trxbtc@kline_5m/trxbtc@kline_15m/trxbtc@kline_30m/trxbtc@kline_1h/trxbtc@kline_12h/trxbtc@depth5/bchabcbtc@trade/bchabcbtc@kline_1m/bchabcbtc@kline_5m/bchabcbtc@kline_15m/bchabcbtc@kline_30m/bchabcbtc@kline_1h/bchabcbtc@kline_12h/bchabcbtc@depth5/ltcbtc@trade/ltcbtc@kline_1m/ltcbtc@kline_5m/ltcbtc@kline_15m/ltcbtc@kline_30m/ltcbtc@kline_1h/ltcbtc@kline_12h/ltcbtc@depth5/xrpbtc@trade/xrpbtc@kline_1m/xrpbtc@kline_5m/xrpbtc@kline_15m/xrpbtc@kline_30m/xrpbtc@kline_1h/xrpbtc@kline_12h/xrpbtc@depth5/ontbtc@trade/ontbtc@kline_1m/ontbtc@kline_5m/ontbtc@kline_15m/ontbtc@kline_30m/ontbtc@kline_1h/ontbtc@kline_12h/ontbtc@depth5/bttusdt@trade/bttusdt@kline_1m/bttusdt@kline_5m/bttusdt@kline_15m/bttusdt@kline_30m/bttusdt@kline_1h/bttusdt@kline_12h/bttusdt@depth5/eosbtc@trade/eosbtc@kline_1m/eosbtc@kline_5m/eosbtc@kline_15m/eosbtc@kline_30m/eosbtc@kline_1h/eosbtc@kline_12h/eosbtc@depth5/xlmbtc@trade/xlmbtc@kline_1m/xlmbtc@kline_5m/xlmbtc@kline_15m/xlmbtc@kline_30m/xlmbtc@kline_1h/xlmbtc@kline_12h/xlmbtc@depth5/bttbtc@trade/bttbtc@kline_1m/bttbtc@kline_5m/bttbtc@kline_15m/bttbtc@kline_30m/bttbtc@kline_1h/bttbtc@kline_12h/bttbtc@depth5/tusdusdt@trade/tusdusdt@kline_1m/tusdusdt@kline_5m/tusdusdt@kline_15m/tusdusdt@kline_30m/tusdusdt@kline_1h/tusdusdt@kline_12h/tusdusdt@depth5/xlmusdt@trade/xlmusdt@kline_1m/xlmusdt@kline_5m/xlmusdt@kline_15m/xlmusdt@kline_30m/xlmusdt@kline_1h/xlmusdt@kline_12h/xlmusdt@depth5/qkcbtc@trade/qkcbtc@kline_1m/qkcbtc@kline_5m/qkcbtc@kline_15m/qkcbtc@kline_30m/qkcbtc@kline_1h/qkcbtc@kline_12h/qkcbtc@depth5/zrxbtc@trade/zrxbtc@kline_1m/zrxbtc@kline_5m/zrxbtc@kline_15m/zrxbtc@kline_30m/zrxbtc@kline_1h/zrxbtc@kline_12h/zrxbtc@depth5/neobtc@trade/neobtc@kline_1m/neobtc@kline_5m/neobtc@kline_15m/neobtc@kline_30m/neobtc@kline_1h/neobtc@kline_12h/neobtc@depth5/adaeth@trade/adaeth@kline_1m/adaeth@kline_5m/adaeth@kline_15m/adaeth@kline_30m/adaeth@kline_1h/adaeth@kline_12h/adaeth@depth5/icxusdt@trade/icxusdt@kline_1m/icxusdt@kline_5m/icxusdt@kline_15m/icxusdt@kline_30m/icxusdt@kline_1h/icxusdt@kline_12h/icxusdt@depth5/btctusd@trade/btctusd@kline_1m/btctusd@kline_5m/btctusd@kline_15m/btctusd@kline_30m/btctusd@kline_1h/btctusd@kline_12h/btctusd@depth5/icxbtc@trade/icxbtc@kline_1m/icxbtc@kline_5m/icxbtc@kline_15m/icxbtc@kline_30m/icxbtc@kline_1h/icxbtc@kline_12h/icxbtc@depth5/btcusdc@trade/btcusdc@kline_1m/btcusdc@kline_5m/btcusdc@kline_15m/btcusdc@kline_30m/btcusdc@kline_1h/btcusdc@kline_12h/btcusdc@depth5/wanbtc@trade/wanbtc@kline_1m/wanbtc@kline_5m/wanbtc@kline_15m/wanbtc@kline_30m/wanbtc@kline_1h/wanbtc@kline_12h/wanbtc@depth5/zecbtc@trade/zecbtc@kline_1m/zecbtc@kline_5m/zecbtc@kline_15m/zecbtc@kline_30m/zecbtc@kline_1h/zecbtc@kline_12h/zecbtc@depth5/wtcbtc@trade/wtcbtc@kline_1m/wtcbtc@kline_5m/wtcbtc@kline_15m/wtcbtc@kline_30m/wtcbtc@kline_1h/wtcbtc@kline_12h/wtcbtc@depth5/batbtc@trade/batbtc@kline_1m/batbtc@kline_5m/batbtc@kline_15m/batbtc@kline_30m/batbtc@kline_1h/batbtc@kline_12h/batbtc@depth5/adabnb@trade/adabnb@kline_1m/adabnb@kline_5m/adabnb@kline_15m/adabnb@kline_30m/adabnb@kline_1h/adabnb@kline_12h/adabnb@depth5/etcusdt@trade/etcusdt@kline_1m/etcusdt@kline_5m/etcusdt@kline_15m/etcusdt@kline_30m/etcusdt@kline_1h/etcusdt@kline_12h/etcusdt@depth5/qtumusdt@trade/qtumusdt@kline_1m/qtumusdt@kline_5m/qtumusdt@kline_15m/qtumusdt@kline_30m/qtumusdt@kline_1h/qtumusdt@kline_12h/qtumusdt@depth5/xmrbtc@trade/xmrbtc@kline_1m/xmrbtc@kline_5m/xmrbtc@kline_15m/xmrbtc@kline_30m/xmrbtc@kline_1h/xmrbtc@kline_12h/xmrbtc@depth5/trxeth@trade/trxeth@kline_1m/trxeth@kline_5m/trxeth@kline_15m/trxeth@kline_30m/trxeth@kline_1h/trxeth@kline_12h/trxeth@depth5/adatusd@trade/adatusd@kline_1m/adatusd@kline_5m/adatusd@kline_15m/adatusd@kline_30m/adatusd@kline_1h/adatusd@kline_12h/adatusd@depth5/trxxrp@trade/trxxrp@kline_1m/trxxrp@kline_5m/trxxrp@kline_15m/trxxrp@kline_30m/trxxrp@kline_1h/trxxrp@kline_12h/trxxrp@depth5/trxbnb@trade/trxbnb@kline_1m/trxbnb@kline_5m/trxbnb@kline_15m/trxbnb@kline_30m/trxbnb@kline_1h/trxbnb@kline_12h/trxbnb@depth5/dashbtc@trade/dashbtc@kline_1m/dashbtc@kline_5m/dashbtc@kline_15m/dashbtc@kline_30m/dashbtc@kline_1h/dashbtc@kline_12h/dashbtc@depth5/rvnbnb@trade/rvnbnb@kline_1m/rvnbnb@kline_5m/rvnbnb@kline_15m/rvnbnb@kline_30m/rvnbnb@kline_1h/rvnbnb@kline_12h/rvnbnb@depth5/bchabctusd@trade/bchabctusd@kline_1m/bchabctusd@kline_5m/bchabctusd@kline_15m/bchabctusd@kline_30m/bchabctusd@kline_1h/bchabctusd@kline_12h/bchabctusd@depth5/etcbtc@trade/etcbtc@kline_1m/etcbtc@kline_5m/etcbtc@kline_15m/etcbtc@kline_30m/etcbtc@kline_1h/etcbtc@kline_12h/etcbtc@depth5/bnbeth@trade/bnbeth@kline_1m/bnbeth@kline_5m/bnbeth@kline_15m/bnbeth@kline_30m/bnbeth@kline_1h/bnbeth@kline_12h/bnbeth@depth5/ethpax@trade/ethpax@kline_1m/ethpax@kline_5m/ethpax@kline_15m/ethpax@kline_30m/ethpax@kline_1h/ethpax@kline_12h/ethpax@depth5/nanobtc@trade/nanobtc@kline_1m/nanobtc@kline_5m/nanobtc@kline_15m/nanobtc@kline_30m/nanobtc@kline_1h/nanobtc@kline_12h/nanobtc@depth5/xembtc@trade/xembtc@kline_1m/xembtc@kline_5m/xembtc@kline_15m/xembtc@kline_30m/xembtc@kline_1h/xembtc@kline_12h/xembtc@depth5/xrpbnb@trade/xrpbnb@kline_1m/xrpbnb@kline_5m/xrpbnb@kline_15m/xrpbnb@kline_30m/xrpbnb@kline_1h/xrpbnb@kline_12h/xrpbnb@depth5/bchabcpax@trade/bchabcpax@kline_1m/bchabcpax@kline_5m/bchabcpax@kline_15m/bchabcpax@kline_30m/bchabcpax@kline_1h/bchabcpax@kline_12h/bchabcpax@depth5/xrpeth@trade/xrpeth@kline_1m/xrpeth@kline_5m/xrpeth@kline_15m/xrpeth@kline_30m/xrpeth@kline_1h/xrpeth@kline_12h/xrpeth@depth5/bttbnb@trade/bttbnb@kline_1m/bttbnb@kline_5m/bttbnb@kline_15m/bttbnb@kline_30m/bttbnb@kline_1h/bttbnb@kline_12h/bttbnb@depth5/ltcbnb@trade/ltcbnb@kline_1m/ltcbnb@kline_5m/ltcbnb@kline_15m/ltcbnb@kline_30m/ltcbnb@kline_1h/ltcbnb@kline_12h/ltcbnb@depth5/agibtc@trade/agibtc@kline_1m/agibtc@kline_5m/agibtc@kline_15m/agibtc@kline_30m/agibtc@kline_1h/agibtc@kline_12h/agibtc@depth5/zrxusdt@trade/zrxusdt@kline_1m/zrxusdt@kline_5m/zrxusdt@kline_15m/zrxusdt@kline_30m/zrxusdt@kline_1h/zrxusdt@kline_12h/zrxusdt@depth5/xlmbnb@trade/xlmbnb@kline_1m/xlmbnb@kline_5m/xlmbnb@kline_15m/xlmbnb@kline_30m/xlmbnb@kline_1h/xlmbnb@kline_12h/"

print("\r\nstart shorting the URI:")
while True:
    shorted_query = full_query[:-1]
    try:
        binance_test_uri_length(shorted_query)
        print("\r\nfound first valid URI length before URI too long error")
        print("longest valid URI length:", str(len("wss://stream.binance.com:9443/stream?streams=" + shorted_query)))
        print("longest valid URI string:")
        print("wss://stream.binance.com:9443/stream?streams=" + shorted_query)
        exit(0)
    except websocket._exceptions.WebSocketBadStatusException as error_msg:
        pass

    time.sleep(11)


