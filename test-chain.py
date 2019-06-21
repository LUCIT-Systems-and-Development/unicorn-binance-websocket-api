#!/usr/bin/env python

from websocket import create_connection
import ssl
import logging
import os


# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
logging.getLogger('unicorn-log').addHandler(logging.StreamHandler())
logging.getLogger('unicorn-log').setLevel(logging.DEBUG)


def binance_stream_trades():
    websocket = create_connection("wss://testnet-dex.binance.org/api/ws/$all@allMiniTickers")
    while True:
        result = websocket.recv()
        print("Received trade '%s'" % result)


binance_stream_trades()
