from enum import Enum
from typing import Tuple


WEBSOCKET_BASE_URI = str
MAX_SUBSCRIPTIONS_PER_STREAM = int


class Exchanges(str, Enum):
    BINANCE = "binance.com"
    BINANCE_TESTNET = "binance.com-testnet"
    BINANCE_MARGIN = "binance.com-margin"
    BINANCE_MARGIN_TESTNET = "binance.com-margin-testnet"
    BINANCE_ISOLATED_MARGIN = "binance.com-isolated_margin"
    BINANCE_ISOLATED_MARGIN_TESTNET = "binance.com-isolated_margin-testnet"
    BINANCE_FUTURES = "binance.com-futures"
    BINANCE_COIN_FUTURES = "binance.com-coin-futures"
    BINANCE_FUTURES_TESTNET = "binance.com-futures-testnet"
    BINANCE_US = "binance.us"
    TRBINANCE = "trbinance.com"
    JEX = "jex.com"
    BINANCE_ORG = "binance.org"
    BINANCE_ORG_TESTNET = "binance.org-testnet"
    LOCALHOST = "localhost"


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
    Exchanges.JEX,
]

ws_connection_settings: dict[str, Tuple[WEBSOCKET_BASE_URI, MAX_SUBSCRIPTIONS_PER_STREAM]] = {
    Exchanges.BINANCE: ("wss://stream.binance.com:9443/", 1024),
    Exchanges.BINANCE_TESTNET: ("wss://testnet.binance.vision/", 1024),
    Exchanges.BINANCE_MARGIN: ("wss://stream.binance.com:9443/", 1024),
    Exchanges.BINANCE_MARGIN_TESTNET: ("wss://testnet.binance.vision/", 1024),
    Exchanges.BINANCE_ISOLATED_MARGIN: ("wss://stream.binance.com:9443/", 1024),
    Exchanges.BINANCE_ISOLATED_MARGIN_TESTNET: ("wss://testnet.binance.vision/", 1024),
    Exchanges.BINANCE_FUTURES: ("wss://fstream.binance.com/", 200),
    Exchanges.BINANCE_COIN_FUTURES: ("wss://dstream.binance.com/", 200),
    Exchanges.BINANCE_FUTURES_TESTNET: ("wss://stream.binancefuture.com/", 200),
    Exchanges.BINANCE_US: ("wss://stream.binance.us:9443/", 1024),
    Exchanges.TRBINANCE: ("wss://stream-cloud.trbinance.com/", 1024),
    Exchanges.JEX: ("wss://ws.jex.com/", 10),
    Exchanges.BINANCE_ORG: ("wss://dex.binance.org/api/", 1024),
    Exchanges.BINANCE_ORG_TESTNET: ("wss://testnet-dex.binance.org/api/", 1024),
    Exchanges.LOCALHOST: ("ws://127.0.0.1:8765/", 1024),
}
