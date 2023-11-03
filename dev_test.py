from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
import logging
import os
import time

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager

logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

input_config_file = f"{Path.home()}/.lucit/lucit_license.ini"
if os.path.isfile(input_config_file):
    print(f"Loading configuration file `{input_config_file}`")
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(input_config_file)
    LUCIT_API_SECRET = config['LUCIT']['api_secret']
    LUCIT_LICENSE_TOKEN = config['LUCIT']['license_token']
else:
    LUCIT_API_SECRET = os.environ['LUCIT_API_SECRET']
    LUCIT_LICENSE_TOKEN = os.environ['LUCIT_LICENSE_TOKEN']

ubwa = BinanceWebSocketApiManager(lucit_api_secret=LUCIT_API_SECRET,
                                  lucit_license_token=LUCIT_LICENSE_TOKEN)
ubwa.create_stream("trade", "btcusdt", output="UnicornFy")

try:
    while ubwa.is_manager_stopping() is False:
        time.sleep(1)
        print(f"Trades: {ubwa.pop_stream_data_from_stream_buffer()}")
except KeyboardInterrupt:
    print(f"Stopping ...")
    ubwa.stop_manager_with_all_streams()
