#!/usr/bin/env python3

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import unittest


class TestBinanceManager(unittest.TestCase):

    def test_create_uri(self):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        self.assertEqual(binance_websocket_api_manager.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr/')
        self.assertEqual(binance_websocket_api_manager.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr/')
        binance_websocket_api_manager.stop_manager_with_all_streams()


if __name__ == '__main__':
    unittest.main()
