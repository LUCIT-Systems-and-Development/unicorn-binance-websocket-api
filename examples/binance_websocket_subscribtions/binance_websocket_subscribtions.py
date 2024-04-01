#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import time
import threading
import os


logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")

markets = ['bnbbtc', 'etcusdt']
channels = ['trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'depth5']


markets_1 = ['ethbtc']
channels_1 = ['trade', 'kline_1m', '!ticker']
stream_id = binance_websocket_api_manager.create_stream(channels_1, markets_1)
binance_websocket_api_manager.unsubscribe_from_stream(stream_id=stream_id, markets="BNBBTC")


markets_2 = ['batbtc', 'adabnb', 'etcusdt', 'qtumusdt', 'xmrbtc', 'trxeth', 'adatusd', 'trxxrp', 'trxbnb',
             'dashbtc', 'rvnbnb', 'bchabctusd', 'etcbtc', 'bnbeth', 'ethpax', 'nanobtc', 'xembtc']
binance_websocket_api_manager.subscribe_to_stream(stream_id, markets=markets_2)

markets_3 = ['!miniTicker']
binance_websocket_api_manager.subscribe_to_stream(stream_id, markets=markets_3)

markets_4 = ['engbtc', 'zileth', 'xlmeth', 'eosbnb', 'xrppax', 'lskbtc', 'npxsbtc', 'xmrusdt', 'ltcpax', 'xmrusdt',
           'ethtusd', 'batusdt', 'mcobtc', 'neoeth', 'bntbtc', 'eostusd', 'lrcbtc', 'funbtc', 'zecusdt',
           'bnbpax', 'linkusdt', 'hceth', 'zrxeth', 'icxeth', 'xmreth', 'neobnb', 'etceth', 'zeceth', 'xmrbnb',
           'wanbnb', 'zrxbnb', 'agibnb', 'funeth', 'arketh', 'engeth']
binance_websocket_api_manager.subscribe_to_stream(stream_id, markets=markets_4)
time.sleep(1)
binance_websocket_api_manager.get_stream_subscriptions(stream_id)

time.sleep(2)
channels_2 = ['trade', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'depth5']
binance_websocket_api_manager.unsubscribe_from_stream(stream_id, channels=channels_2)
request_id = binance_websocket_api_manager.get_stream_subscriptions(stream_id)

while binance_websocket_api_manager.get_result_by_request_id(request_id) is None:
    print("Wait to receive the result!")
    time.sleep(0.5)

print(str(binance_websocket_api_manager.get_result_by_request_id(request_id)))

time.sleep(10)
while True:
    #binance_websocket_api_manager.print_summary()
    binance_websocket_api_manager.print_stream_info(stream_id)
    #binance_websocket_api_manager.get_stream_subscriptions(stream_id)
    time.sleep(1)
