#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import asyncio
import logging
import os

api_key = ""
api_secret = ""
market = "BTCUSDT"

async def binance_stream(ubwa):
    async def handle_socket_message(stream_id=None):
        while ubwa.is_stop_request(stream_id=stream_id) is False:
            data = await ubwa.get_stream_data_from_asyncio_queue(stream_id=stream_id)
            print(f"received data:\r\n{data}\r\n")

    api_stream = ubwa.create_stream(api=True, api_key=api_key, api_secret=api_secret,
                                    stream_label="Bobs Websocket API",
                                    process_asyncio_queue=handle_socket_message)
    print(f"Start:")
    ubwa.api.get_listen_key(stream_id=api_stream)
    ubwa.api.get_server_time(stream_id=api_stream)
    ubwa.api.get_account_status(stream_id=api_stream)
    orig_client_order_id = ubwa.api.create_order(stream_id=api_stream, price=1.0, order_type="LIMIT",
                                                 quantity=15.0, side="SELL", symbol=market)
    ubwa.api.create_test_order(stream_id=api_stream, price=1.2, order_type="LIMIT",
                               quantity=12.0, side="SELL", symbol=market)
    ubwa.api.ping(stream_id=api_stream)
    ubwa.api.get_exchange_info(stream_id=api_stream, symbols=market)
    ubwa.api.get_order_book(stream_id=api_stream, symbol=market, limit=2)
    ubwa.api.cancel_order(stream_id=api_stream, symbol=market, orig_client_order_id=orig_client_order_id)
    ubwa.api.get_open_orders(stream_id=api_stream, symbol=market)
    ubwa.api.get_open_orders(stream_id=api_stream)
    ubwa.api.cancel_open_orders(stream_id=api_stream, symbol=market)
    ubwa.api.get_order(stream_id=api_stream, symbol=market, orig_client_order_id=orig_client_order_id)

    print(f"Finished! Waiting for responses:")
    await asyncio.sleep(5)

    print(f"Stopping!")
    ubwa.stop_manager()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename=os.path.basename(__file__) + '.log',
                        format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                        style="{")

    # To use this library you need a valid UNICORN Binance Suite License:
    # https://shop.lucit.services
    ubwa = BinanceWebSocketApiManager(exchange='binance.com-futures')
    try:
        asyncio.run(binance_stream(ubwa))
    except KeyboardInterrupt:
        print("\r\nGracefully stopping the websocket manager...")
        ubwa.stop_manager()
