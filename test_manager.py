#!/usr/bin/env python3

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import unittest


class TestManagerBinanceCom(unittest.TestCase):

    def setUp(self):
        self.binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")

    def test_create_uri_ticker_regular(self):
        self.assertEqual(self.binance_websocket_api_manager.create_websocket_uri(["!ticker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr/')

    def test_create_uri_ticker_reverse(self):
        self.assertEqual(self.binance_websocket_api_manager.create_websocket_uri(["arr"], ["!ticker"]),
                         'wss://stream.binance.com:9443/ws/!ticker@arr/')

    def test_create_uri_miniticker_regular(self):
        self.assertEqual(self.binance_websocket_api_manager.create_websocket_uri(["!miniTicker"], ["arr"]),
                         'wss://stream.binance.com:9443/ws/!miniTicker@arr')

    def test_create_uri_miniticker_reverse(self):
        self.assertEqual(self.binance_websocket_api_manager.create_websocket_uri(["arr"], ["!miniTicker"]),
                         'wss://stream.binance.com:9443/ws/!miniTicker@arr')

    def tearDown(self):
        self.binance_websocket_api_manager.stop_manager_with_all_streams()


if __name__ == '__main__':
    unittest.main()
