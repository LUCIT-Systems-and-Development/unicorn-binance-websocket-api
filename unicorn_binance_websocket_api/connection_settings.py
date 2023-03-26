from enum import Enum
from typing import Tuple


MAX_SUBSCRIPTIONS_PER_STREAM = int
RESTFUL_BASE_URI = str
RESTFUL_PATH_USERDATA = str
WEBSOCKET_BASE_URI = str


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
    JEX = "jex.com"
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
    Exchanges.JEX,
]

CONNECTION_SETTINGS: dict[str, Tuple[MAX_SUBSCRIPTIONS_PER_STREAM, RESTFUL_BASE_URI, RESTFUL_PATH_USERDATA, WEBSOCKET_BASE_URI]] = {
    Exchanges.BINANCE: (1024, "https://api.binance.com/", "api/v3/userDataStream", "wss://stream.binance.com:9443/"),
    Exchanges.BINANCE_TESTNET: (1024, "https://testnet.binance.vision/", "api/v3/userDataStream", "wss://testnet.binance.vision/"),
    Exchanges.BINANCE_MARGIN: (1024, "https://api.binance.com/", "sapi/v1/userDataStream", "wss://stream.binance.com:9443/"),
    Exchanges.BINANCE_MARGIN_TESTNET: (1024, "https://testnet.binance.vision/", "sapi/v1/userDataStream", "wss://testnet.binance.vision/"),
    Exchanges.BINANCE_ISOLATED_MARGIN: (1024, "https://api.binance.com/", "sapi/v1/userDataStream/isolated", "wss://stream.binance.com:9443/"),
    Exchanges.BINANCE_ISOLATED_MARGIN_TESTNET: (1024, "https://testnet.binance.vision/", "sapi/v1/userDataStream/isolated", "wss://testnet.binance.vision/"),
    Exchanges.BINANCE_FUTURES: (200, "https://fapi.binance.com/", "fapi/v1/listenKey", "wss://fstream.binance.com/"),
    Exchanges.BINANCE_FUTURES_TESTNET: (200, "https://testnet.binancefuture.com/", "fapi/v1/listenKey", "wss://stream.binancefuture.com/"),
    Exchanges.BINANCE_COIN_FUTURES: (200, "https://dapi.binance.com/", "dapi/v1/listenKey", "wss://dstream.binance.com/"),
    Exchanges.BINANCE_US: (1024, "https://api.binance.us/", "api/v1/userDataStream", "wss://stream.binance.us:9443/"),
    Exchanges.TRBINANCE: (1024, "https://api.binance.cc/", "api/v1/userDataStream", "wss://stream-cloud.trbinance.com/"),
    Exchanges.JEX: (10, "https://www.jex.com/", "api/v1/userDataStream", "wss://ws.jex.com/"),
    Exchanges.BINANCE_ORG: (1024, "", "", "wss://dex.binance.org/api/"),
    Exchanges.BINANCE_ORG_TESTNET: (1024, "", "", "wss://testnet-dex.binance.org/api/"),
}
