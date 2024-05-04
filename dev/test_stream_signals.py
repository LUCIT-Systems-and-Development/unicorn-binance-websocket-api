#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import time


def receive_stream_signal(self, signal_type=None, stream_id=None, data_record=None, error_msg=None):
    print(f"Received stream_signal for stream '{ubwa.get_stream_label(stream_id=stream_id)}': "
          f"{signal_type} - {stream_id} - {data_record} - {error_msg}")


with BinanceWebSocketApiManager(process_stream_signals=receive_stream_signal) as ubwa:
    ubwa.create_stream(channels="trade", markets="btcusdt", stream_label="HEALTHY")
    print(f"Waiting 5 seconds and then stop the stream ...")
    time.sleep(5)

