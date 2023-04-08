#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_websocket_api.py
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

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import asyncio
import logging
import os

api_key = ""
api_secret = ""


async def binance_stream(ubwa):
    def handle_socket_message(data):
        print(f"received data:\r\n{data}\r\n")

    api_stream = ubwa.create_stream(api=True, api_key=api_key, api_secret=api_secret,
                                    stream_label="Bobs Websocket API",
                                    process_stream_data=handle_socket_message)
    print(f"Start:")
    ubwa.api.get_server_time(stream_id=api_stream)
    ubwa.api.get_account_status(stream_id=api_stream)
    orig_client_order_id = ubwa.api.create_order(stream_id=api_stream, price=1.0, order_type="LIMIT",
                                                 quantity=15.0, side="SELL", symbol="BUSDUSDT")
    ubwa.api.test_create_order(stream_id=api_stream, price=1.2, order_type="LIMIT",
                               quantity=12.0, side="SELL", symbol="BUSDUSDT")
    ubwa.api.ping(stream_id=api_stream)
    ubwa.api.get_exchange_info(stream_id=api_stream, symbols=['BUSDUSDT'])
    ubwa.api.get_order_book(stream_id=api_stream, symbol="BUSDUSDT", limit=2)
    ubwa.api.cancel_order(stream_id=api_stream, symbol="BUSDUSDT", orig_client_order_id=orig_client_order_id)
    ubwa.api.get_open_orders(stream_id=api_stream, symbol="BUSDUSDT")
    ubwa.api.cancel_open_orders(stream_id=api_stream, symbol="BUSDUSDT")
    ubwa.api.get_order(stream_id=api_stream, symbol="BUSDUSDT", orig_client_order_id=orig_client_order_id)

    print(f"Finished! Waiting for responses:")
    await asyncio.sleep(5)

    print(f"Stopping!")
    ubwa.stop_manager_with_all_streams()

if __name__ == "__main__":
    logging.getLogger("unicorn_binance_websocket_api")
    logging.basicConfig(level=logging.DEBUG,
                        filename=os.path.basename(__file__) + '.log',
                        format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                        style="{")
    ubwa = BinanceWebSocketApiManager(exchange='binance.com')
    try:
        asyncio.run(binance_stream(ubwa))
    except KeyboardInterrupt:
        print("\r\nGracefully stopping the websocket manager...")
        ubwa.stop_manager_with_all_streams()



