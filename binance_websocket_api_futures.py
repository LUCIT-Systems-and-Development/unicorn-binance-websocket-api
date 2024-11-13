#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import asyncio
import logging
import os

market = "BTCUSDC"

async def binance_api(ubwa):
    async def handle_socket_message(stream_id=None):
        while ubwa.is_stop_request(stream_id=stream_id) is False:
            data = await ubwa.get_stream_data_from_asyncio_queue(stream_id=stream_id)
            print(f"received data:\r\n{data}\r\n")

    print(f"Starting the stream:")
    api_stream = ubwa.create_stream(api=True,
                                    api_key=os.getenv('BINANCE_API_KEY'),
                                    api_secret=os.getenv('BINANCE_API_SECRET'),
                                    stream_label="Bobs Future Websocket API",
                                    process_asyncio_queue=handle_socket_message)

    print(f"Executing API requests on Binance Futures:")
    ubwa.api.futures.get_account_status(stream_id=api_stream)
    ubwa.api.futures.get_listen_key(stream_id=api_stream)
    ubwa.api.futures.get_server_time(stream_id=api_stream)
    orig_client_order_id = ubwa.api.futures.create_order(stream_id=api_stream, price=1.0, order_type="LIMIT",
                                                        quantity=15.0, side="SELL", symbol=market)
    #ubwa.api.futures.ping(stream_id=api_stream)
    order_book = ubwa.api.futures.get_order_book(stream_id=api_stream, symbol=market, limit=2, return_response=True)
    print(f"Orderbook, lastUpdateId={order_book['result']['lastUpdateId']}: {order_book['result']['asks']}, "
          f"{order_book['result']['bids']}\r\n")
    ubwa.api.futures.cancel_order(stream_id=api_stream, symbol=market, orig_client_order_id=orig_client_order_id)
    ubwa.api.futures.get_order(stream_id=api_stream, symbol=market, orig_client_order_id=orig_client_order_id)

    print(f"Finished! Waiting for responses:")
    await asyncio.sleep(5)
    print(f"Stopping!")

def process_stream_signal(signal_type=None, stream_id=None, data_record=None, error_msg=None):
    # More info about `stream_signals`:
    # https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signals%60
    print(f"Received stream_signal for stream '{ubwa_manager.get_stream_label(stream_id=stream_id)}': "
          f"{signal_type} - {stream_id} - {data_record} - {error_msg}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename=os.path.basename(__file__) + '.log',
                        format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                        style="{")
    load_dotenv()

    # To use this library you need a valid UNICORN Binance Suite License:
    # https://shop.lucit.services
    with BinanceWebSocketApiManager(exchange='binance.com-futures',
                                    output_default="dict",
                                    process_stream_signals=process_stream_signal) as ubwa_manager:
        try:
            asyncio.run(binance_api(ubwa_manager))
        except KeyboardInterrupt:
            print("\r\nGracefully stopping the websocket manager...")
