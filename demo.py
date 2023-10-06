import logging
import os
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager

logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

lucit_api_secret = "bf7df011327b09b80fb0c6bfbc8661633fdb0c58d42629c94abb5188d8b0115a"
lucit_license_token = "5e84cbc7-acfa-489f-a8bd-t7d1b615af40d"

ubwa = BinanceWebSocketApiManager(lucit_api_secret=lucit_api_secret,
                                  lucit_license_token=lucit_license_token)
ubwa.create_stream("trade", "btcusdt", output="UnicornFy")

try:
    while ubwa.is_manager_stopping() is False:
        print(f"Trades: {ubwa.pop_stream_data_from_stream_buffer()}")
except KeyboardInterrupt:
    print(f"Stopping ...")
    ubwa.stop_manager_with_all_streams()
