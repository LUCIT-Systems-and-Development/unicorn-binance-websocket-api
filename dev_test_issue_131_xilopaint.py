from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager

API_KEY = '*'
API_SECRET = '*'


binance_websocket_api_manager = BinanceWebSocketApiManager(
    exchange='binance.com-futures',
)

binance_websocket_api_manager.create_stream(
    channels=['!userData'],
    markets=['arr'],
    api_key=API_KEY,
    api_secret=API_SECRET
)