#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unicorn_binance_websocket_api import BinanceWebSocketApiManager
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import os

api_key = ""
api_secret = ""
exchange = "binance.com"

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


class BinanceDataProcessor:
    def __init__(self):
        self.ubwa = BinanceWebSocketApiManager(exchange=exchange)

    async def main(self):
        self.ubwa.create_stream(["!userData"], ["arr"],
                                stream_label="userData",
                                api_key=api_key,
                                api_secret=api_secret,
                                process_asyncio_queue=self.process_data)
        self.ubwa.create_stream(['!miniTicker', '!ticker', '!bookTicker'],  "arr",
                                stream_label="arr channels",
                                process_asyncio_queue=self.process_data)

        with BinanceRestApiManager(exchange=exchange) as ubra:
            markets = [item['symbol'] for item in ubra.get_all_tickers() if item['symbol'].endswith("USDT")]
        channels = ['trade', 'kline_1m', 'depth20']
        for channel in channels:
            self.ubwa.create_stream(channels=channel,
                                    markets=markets[:self.ubwa.get_limit_of_subscriptions_per_stream()],
                                    process_asyncio_queue=self.process_data,
                                    stream_label=channel)

        while self.ubwa.is_manager_stopping() is False:
            await asyncio.sleep(10)
            self.ubwa.print_summary()

    async def process_data(self, stream_id=None):
        while self.ubwa.is_stop_request(stream_id=stream_id) is False:
            await self.ubwa.get_stream_data_from_asyncio_queue(stream_id)
            self.ubwa.asyncio_queue_task_done(stream_id)


if __name__ == "__main__":
    bdp = BinanceDataProcessor()
    try:
        asyncio.run(bdp.main())
    except KeyboardInterrupt:
        print("\r\n")
    except Exception as e:
        print(f"\r\nError: {e}")
    print("Gracefully stopping ...")
    bdp.ubwa.stop_manager()
