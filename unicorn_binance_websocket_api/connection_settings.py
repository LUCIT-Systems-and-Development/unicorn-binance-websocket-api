import sys
from enum import Enum

if sys.version_info >= (3, 9):
    from typing import Type
    MAX_SUBSCRIPTIONS_PER_STREAM: Type[int] = int
    WEBSOCKET_BASE_URI: Type[str] = str
    WEBSOCKET_API_BASE_URI: Type[str] = str
else:
    MAX_SUBSCRIPTIONS_PER_STREAM = int
    WEBSOCKET_BASE_URI = str
    WEBSOCKET_API_BASE_URI = str


class Exchanges(str, Enum):
    BINANCE = "binance.com"
    BINANCE_TESTNET = "binance.com-testnet"
    BINANCE_MARGIN = "binance.com-margin"
    BINANCE_MARGIN_TESTNET = "binance.com-margin-testnet"
    BINANCE_ISOLATED_MARGIN = "binance.com-isolated_margin"
    BINANCE_ISOLATED_MARGIN_TESTNET = "binance.com-isolated_margin-testnet"
    BINANCE_FUTURES = "binance.com-futures"
    BINANCE_COIN_FUTURES = "binance.com-coin_futures"
    BINANCE_FUTURES_TESTNET = "binance.com-futures-testnet"
    BINANCE_US = "binance.us"
    TRBINANCE = "trbinance.com"
    BINANCE_ORG = "binance.org"
    BINANCE_ORG_TESTNET = "binance.org-testnet"


DEX_EXCHANGES = [Exchanges.BINANCE_ORG, Exchanges.BINANCE_ORG_TESTNET]
CEX_EXCHANGES = [
    Exchanges.BINANCE,
    Exchanges.BINANCE_TESTNET,
    Exchanges.BINANCE_MARGIN,
    Exchanges.BINANCE_MARGIN_TESTNET,
    Exchanges.BINANCE_ISOLATED_MARGIN,
    Exchanges.BINANCE_ISOLATED_MARGIN_TESTNET,
    Exchanges.BINANCE_FUTURES,
    Exchanges.BINANCE_COIN_FUTURES,
    Exchanges.BINANCE_FUTURES_TESTNET,
    Exchanges.BINANCE_US,
    Exchanges.TRBINANCE,
]

# only python 3.9+
# CONNECTION_SETTINGS: dict[str, Tuple[MAX_SUBSCRIPTIONS_PER_STREAM, WEBSOCKET_BASE_URI, WEBSOCKET_API_BASE_URI]] = {

CONNECTION_SETTINGS = {
    Exchanges.BINANCE: (1024, "wss://stream.binance.com:9443/", "wss://ws-api.binance.com/ws-api/v3"),
    Exchanges.BINANCE_TESTNET: (1024, "wss://testnet.binance.vision/", "wss://testnet.binance.vision/ws-api/v3"),
    Exchanges.BINANCE_MARGIN: (1024, "wss://stream.binance.com:9443/", ""),
    Exchanges.BINANCE_MARGIN_TESTNET: (1024, "wss://testnet.binance.vision/", ""),
    Exchanges.BINANCE_ISOLATED_MARGIN: (1024, "wss://stream.binance.com:9443/", ""),
    Exchanges.BINANCE_ISOLATED_MARGIN_TESTNET: (1024, "wss://testnet.binance.vision/", ""),
    Exchanges.BINANCE_FUTURES: (200, "wss://fstream.binance.com/", ""),
    Exchanges.BINANCE_FUTURES_TESTNET: (200, "wss://stream.binancefuture.com/", ""),
    Exchanges.BINANCE_COIN_FUTURES: (200, "wss://dstream.binance.com/", ""),
    Exchanges.BINANCE_US: (1024, "wss://stream.binance.us:9443/", ""),
    Exchanges.TRBINANCE: (1024, "wss://stream-cloud.trbinance.com/", ""),
    Exchanges.BINANCE_ORG: (1024, "wss://dex.binance.org/api/", ""),
    Exchanges.BINANCE_ORG_TESTNET: (1024, "wss://testnet-dex.binance.org/api/", ""),
}
