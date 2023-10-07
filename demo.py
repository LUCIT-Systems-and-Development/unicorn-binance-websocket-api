import logging
import os
import time

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager

logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

lucit_api_secret = "a43135e0273ca69eddee7d954b14848622d70856ada57752ecafbf1b6b6cb420"
lucit_license_token = "5622267f-72f4-4e04-aafb-t75c065d688d9"

ubwa = BinanceWebSocketApiManager(lucit_api_secret=lucit_api_secret,
                                  lucit_license_token=lucit_license_token)
ubwa.create_stream("trade", "btcusdt", output="UnicornFy")

try:
    while ubwa.is_manager_stopping() is False:
        time.sleep(1)
        print(f"Trades: {ubwa.pop_stream_data_from_stream_buffer()}")
except KeyboardInterrupt:
    print(f"Stopping ...")
    ubwa.stop_manager_with_all_streams()
