#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/ws_api.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from typing import Union


class BinanceWebSocketApiWsApi(object):
    """
    Connect to Binance API via Websocket.

    Binance.com SPOT websocket API documentation:

        - https://developers.binance.com/docs/binance-trading-api/websocket_api

    :param manager: Provide the initiated UNICORN Binance WebSocket API Manager instance.
    :type manager: BinanceWebsocketApiManager
    """

    def __init__(self, manager=None):
        self.manager = manager

    def cancel_open_orders(self, stream_id=None, symbol: str = None, recv_window: int = None,
                           request_id: str = None) -> bool:
        """
        Cancel all open orders on a symbol, including OCO orders.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: int
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message Sent:

        .. code-block:: json

            {
                "id": "778f938f-9041-4b88-9914-efbf64eeacc8",
                "method": "openOrders.cancelAll"
                "params": {
                    "symbol": "BTCUSDT",
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "773f01b6e3c2c9e0c1d217bc043ce383c1ddd6f0e25f8d6070f2b66a6ceaf3a5",
                    "timestamp": 1660805557200
                }
            }


        Response:

        .. code-block:: json

            {
                "id": "778f938f-9041-4b88-9914-efbf64eeacc8",
                "status": 200,
                "result": [
                    {
                        "symbol": "BTCUSDT",
                        "origClientOrderId": "4d96324ff9d44481926157",
                        "orderId": 12569099453,
                        "orderListId": -1,
                        "clientOrderId": "91fe37ce9e69c90d6358c0",
                        "price": "23416.10000000",
                        "origQty": "0.00847000",
                        "executedQty": "0.00001000",
                        "cummulativeQuoteQty": "0.23416100",
                        "status": "CANCELED",
                        "timeInForce": "GTC",
                        "type": "LIMIT",
                        "side": "SELL",
                        "stopPrice": "0.00000000",
                        "trailingDelta": 0,
                        "trailingTime": -1,
                        "icebergQty": "0.00000000",
                        "strategyId": 37463720,
                        "strategyType": 1000000,
                        "selfTradePreventionMode": "NONE"
                    },
                    {
                        "orderListId": 19431,
                        "contingencyType": "OCO",
                        "listStatusType": "ALL_DONE",
                        "listOrderStatus": "ALL_DONE",
                        "listClientOrderId": "iuVNVJYYrByz6C4yGOPPK0",
                        "transactionTime": 1660803702431,
                        "symbol": "BTCUSDT",
                        "orders": [
                            {
                            "symbol": "BTCUSDT",
                            "orderId": 12569099453,
                            "clientOrderId": "bX5wROblo6YeDwa9iTLeyY"
                            },
                            {
                            "symbol": "BTCUSDT",
                            "orderId": 12569099454,
                            "clientOrderId": "Tnu2IP0J5Y4mxw3IATBfmW"
                            }
                        ],
                        "orderReports": [
                            {
                                "symbol": "BTCUSDT",
                                "origClientOrderId": "bX5wROblo6YeDwa9iTLeyY",
                                "orderId": 12569099453,
                                "orderListId": 19431,
                                "clientOrderId": "OFFXQtxVFZ6Nbcg4PgE2DA",
                                "price": "23450.50000000",
                                "origQty": "0.00850000",
                                "executedQty": "0.00000000",
                                "cummulativeQuoteQty": "0.00000000",
                                "status": "CANCELED",
                                "timeInForce": "GTC",
                                "type": "STOP_LOSS_LIMIT",
                                "side": "BUY",
                                "stopPrice": "23430.00000000",
                                "selfTradePreventionMode": "NONE"
                            },
                            {
                                "symbol": "BTCUSDT",
                                "origClientOrderId": "Tnu2IP0J5Y4mxw3IATBfmW",
                                "orderId": 12569099454,
                                "orderListId": 19431,
                                "clientOrderId": "OFFXQtxVFZ6Nbcg4PgE2DA",
                                "price": "23400.00000000",
                                "origQty": "0.00850000",
                                "executedQty": "0.00000000",
                                "cummulativeQuoteQty": "0.00000000",
                                "status": "CANCELED",
                                "timeInForce": "GTC",
                                "type": "LIMIT_MAKER",
                                "side": "BUY",
                                "selfTradePreventionMode": "NONE"
                            }
                        ]
                    }
                ],
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    }
                ]
            }
        """
        if stream_id is None:
            return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": str(symbol).upper(),
                  "timestamp": self.manager.get_timestamp()}

        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "openOrders.cancelAll"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def cancel_order(self, stream_id=None, symbol: str = None, order_id: int = None,
                     orig_client_order_id: str = None, recv_window: int = None, request_id: str = None) -> bool:
        """
        Cancel an active order.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol of the order you want to cancel
        :type symbol: str
        :param order_id: Cancel by `order_id`
        :type order_id: str
        :param orig_client_order_id: Cancel by `origClientOrderId`
        :type orig_client_order_id: str
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

        .. code-block:: json

            {
                "id": "5633b6a2-90a9-4192-83e7-925c90b6a2fd",
                "method": "order.cancel",
                "params": {
                    "symbol": "BTCUSDT",
                    "origClientOrderId": "4d96324ff9d44481926157",
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "33d5b721f278ae17a52f004a82a6f68a70c68e7dd6776ed0be77a455ab855282",
                    "timestamp": 1660801715830
                }
            }


        Response:

        .. code-block:: json

            {
                "id": "5633b6a2-90a9-4192-83e7-925c90b6a2fd",
                "status": 200,
                "result": {
                    "symbol": "BTCUSDT",
                    "origClientOrderId": "4d96324ff9d44481926157",
                    "orderId": 12569099453,
                    "orderListId": -1,
                    "clientOrderId": "91fe37ce9e69c90d6358c0",
                    "price": "23416.10000000",
                    "origQty": "0.00847000",
                    "executedQty": "0.00001000",
                    "cummulativeQuoteQty": "0.23416100",
                    "status": "CANCELED",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "SELL",
                    "stopPrice": "0.00000000",
                    "trailingDelta": 0,
                    "trailingTime": -1,
                    "icebergQty": "0.00000000",
                    "strategyId": 37463720,
                    "strategyType": 1000000,
                    "selfTradePreventionMode": "NONE"
                },
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    }
                ]
            }
        """
        if stream_id is None:
            return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": str(symbol).upper(),
                  "timestamp": self.manager.get_timestamp()}

        if order_id is not None:
            params['orderId'] = order_id
        if orig_client_order_id is not None:
            params['origClientOrderId'] = orig_client_order_id
        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "order.cancel"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def create_order(self, stream_id=None, new_client_order_id: str = None, order_type: str = None, price: float = 0.0,
                     quantity: float = 0.0, side: str = None, symbol: str = None, time_in_force: str = "GTC",
                     test: bool = False, recv_window: int = None, request_id: str = None) -> Union[int, bool]:
        """
        Create a new order.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param new_client_order_id: Set the `newClientOrderId`
        :type new_client_order_id: str
        :param order_type: `LIMIT` or `MARKET`
        :type order_type: str
        :param price: Price e.g. 10.223
        :type price: float
        :param quantity: Amount e.g. 20.5
        :type quantity: float
        :param side: `BUY` or `SELL`
        :type side: str
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param time_in_force: Default `GTC`
        :type time_in_force: str
        :param test: Test order placement. Validates new order parameters and verifies your signature but does not
                     send the order into the matching engine.
        :type test: bool
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: `False` or `orig_client_order_id`


        Message sent:

        .. code-block:: json

            {
                "id": "56374a46-3061-486b-a311-99ee972eb648",
                "method": "order.place",
                "params": {
                    "symbol": "BTCUSDT",
                    "side": "SELL",
                    "type": "LIMIT",
                    "timeInForce": "GTC",
                    "price": "23416.10000000",
                    "quantity": "0.00847000",
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "15af09e41c36f3cc61378c2fbe2c33719a03dd5eba8d0f9206fbda44de717c88",
                    "timestamp": 1660801715431
                }
            }


        Response

        .. code-block:: json

            {
                "id": "56374a46-3061-486b-a311-99ee972eb648",
                "status": 200,
                "result": {
                    "symbol": "BTCUSDT",
                    "orderId": 12569099453,
                    "orderListId": -1,
                    "clientOrderId": "4d96324ff9d44481926157ec08158a40",
                    "transactTime": 1660801715639
                },
                "rateLimits": [
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "intervalNum": 10,
                        "limit": 50,
                        "count": 1
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "intervalNum": 1,
                        "limit": 160000,
                        "count": 1
                    },
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    }
                ]
            }
        """
        if stream_id is None:
            return False

        new_client_order_id = new_client_order_id if new_client_order_id is not None else self.manager.get_request_id()
        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "newClientOrderId": new_client_order_id,
                  "price": str(price),
                  "quantity": quantity,
                  "side": side.upper(),
                  "symbol": symbol.upper(),
                  "timeInForce": time_in_force,
                  "timestamp": self.manager.get_timestamp(),
                  "type": order_type}

        if side.upper() == "LIMIT":
            params['price'] = str(price)
            params['timeInForce'] = time_in_force
        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "order.test" if test is True else "order.place"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return new_client_order_id

    def get_account_status(self, stream_id=None, recv_window: int = None, request_id: str = None) -> bool:
        """
        Get the user account status.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

        .. code-block:: json

            {
                "id": "605a6d20-6588-4cb9-afa0-b0ab087507ba",
                "method": "account.status",
                "params": {
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "83303b4a136ac1371795f465808367242685a9e3a42b22edb4d977d0696eb45c",
                    "timestamp": 1660801839480
                }
            }


        Response:

        .. code-block:: json

            {
                "id": "605a6d20-6588-4cb9-afa0-b0ab087507ba",
                "status": 200,
                "result": {
                    "makerCommission": 15,
                    "takerCommission": 15,
                    "buyerCommission": 0,
                    "sellerCommission": 0,
                    "canTrade": true,
                    "canWithdraw": true,
                    "canDeposit": true,
                    "commissionRates": {
                        "maker": "0.00150000",
                        "taker": "0.00150000",
                        "buyer": "0.00000000",
                        "seller":"0.00000000"
                    },
                    "brokered": false,
                    "requireSelfTradePrevention": false,
                    "updateTime": 1660801833000,
                    "accountType": "SPOT",
                    "balances": [
                        {
                            "asset": "BNB",
                            "free": "0.00000000",
                            "locked": "0.00000000"
                        },
                        {
                            "asset": "BTC",
                            "free": "1.3447112",
                            "locked": "0.08600000"
                        },
                        {
                            "asset": "USDT",
                            "free": "1021.21000000",
                            "locked": "0.00000000"
                        }
                    ],
                    "permissions": [
                        "SPOT"
                    ]
                },
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 10
                    }
                ]
            }
        """
        if stream_id is None:
            return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "timestamp": self.manager.get_timestamp()}

        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "account.status"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def get_exchange_info(self, stream_id=None, symbols=list, recv_window: int = None, request_id: str = None) -> bool:
        """
        Get the Exchange Information.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbols: List of selected symbols
        :type symbols: list
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

        .. code-block:: json

            {
                "id": "5494febb-d167-46a2-996d-70533eb4d976",
                "method": "exchangeInfo",
                "params": {
                    "symbols": [
                        "BNBBTC"
                    ]
                }
            }


        Response:

        .. code-block:: json

            {
                "id": "5494febb-d167-46a2-996d-70533eb4d976",
                "status": 200,
                "result": {
                "timezone": "UTC",
                "serverTime": 1655969291181,
                "rateLimits": [{
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "SECOND",
                    "intervalNum": 10,
                    "limit": 50
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "intervalNum": 1,
                    "limit": 160000
                },
                {
                    "rateLimitType": "RAW_REQUESTS",
                    "interval": "MINUTE",
                    "intervalNum": 5,
                    "limit": 6100
                }],
                "exchangeFilters": [],
                "symbols": [{
                    "symbol": "BNBBTC",
                    "status": "TRADING",
                    "baseAsset": "BNB",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": true,
                    "ocoAllowed": true,
                    "quoteOrderQtyMarketAllowed": true,
                    "allowTrailingStop": true,
                    "cancelReplaceAllowed": true,
                    "isSpotTradingAllowed": true,
                    "isMarginTradingAllowed": true,
                    "filters": [{
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00000100",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.00000100"
                    },
                    {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00100000",
                        "maxQty": "100000.00000000",
                        "stepSize": "0.00100000"
                    }],
                    "permissions": [
                        "SPOT",
                        "MARGIN",
                        "TRD_GRP_004"
                    ],
                    "defaultSelfTradePreventionMode": "NONE",
                    "allowedSelfTradePreventionModes": [
                        "NONE"
                    ]
                }]},
                "rateLimits": [{
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200,
                    "count": 10
                }]
            }
        """
        if stream_id is None:
            return False

        symbols = [symbol.upper() for symbol in symbols]
        params = {"symbols": symbols}

        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "exchangeInfo"
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def get_open_orders(self, stream_id=None, symbol: str = None, recv_window: int = None, request_id: str = None) -> bool:
        """
        Query execution status of all open orders.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message Sent:

        .. code-block:: json

            {
                "id": "55f07876-4f6f-4c47-87dc-43e5fff3f2e7",
                "method": "openOrders.status",
                "params": {
                    "symbol": "BTCUSDT",
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "d632b3fdb8a81dd44f82c7c901833309dd714fe508772a89b0a35b0ee0c48b89",
                    "timestamp": 1660813156812
                }
            }


        Response:

        .. code-block:: json

            {
                "id": "55f07876-4f6f-4c47-87dc-43e5fff3f2e7",
                "status": 200,
                "result": [
                    {
                        "symbol": "BTCUSDT",
                        "orderId": 12569099453,
                        "orderListId": -1,
                        "clientOrderId": "4d96324ff9d44481926157",
                        "price": "23416.10000000",
                        "origQty": "0.00847000",
                        "executedQty": "0.00720000",
                        "cummulativeQuoteQty": "172.43931000",
                        "status": "PARTIALLY_FILLED",
                        "timeInForce": "GTC",
                        "type": "LIMIT",
                        "side": "SELL",
                        "stopPrice": "0.00000000",
                        "icebergQty": "0.00000000",
                        "time": 1660801715639,
                        "updateTime": 1660801717945,
                        "isWorking": true,
                        "workingTime": 1660801715639,
                        "origQuoteOrderQty": "0.00000000",
                        "selfTradePreventionMode": "NONE"
                    }
                ],
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 3
                    }
                ]
            }
        """
        if stream_id is None:
            return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": str(symbol).upper(),
                  "timestamp": self.manager.get_timestamp()}

        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "openOrders.status"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def get_order(self, stream_id=None, symbol: str = None, order_id: int = None, orig_client_order_id: str = None,
                  recv_window: int = None, request_id: str = None) -> bool:
        """
        Check execution status of a specific order.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param order_id: The orderId to select the order
        :type order_id: int
        :param orig_client_order_id: The origClientOrderId to select the order
        :type orig_client_order_id: str
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

        .. code-block:: json

            {
                "id": "aa62318a-5a97-4f3b-bdc7-640bbe33b291",
                "method": "order.status",
                "params": {
                    "symbol": "BTCUSDT",
                    "orderId": 12569099453,
                    "apiKey": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                    "signature": "2c3aab5a078ee4ea465ecd95523b77289f61476c2f238ec10c55ea6cb11a6f35",
                    "timestamp": 1660801720951
                }
            }

        Response:

        .. code-block:: json

            {
                "id": "aa62318a-5a97-4f3b-bdc7-640bbe33b291",
                "status": 200,
                "result": {
                    "symbol": "BTCUSDT",
                    "orderId": 12569099453,
                    "orderListId": -1,
                    "clientOrderId": "4d96324ff9d44481926157",
                    "price": "23416.10000000",
                    "origQty": "0.00847000",
                    "executedQty": "0.00847000",
                    "cummulativeQuoteQty": "198.33521500",
                    "status": "FILLED",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "SELL",
                    "stopPrice": "0.00000000",
                    "trailingDelta": 10,
                    "trailingTime": -1,
                    "icebergQty": "0.00000000",
                    "time": 1660801715639,
                    "updateTime": 1660801717945,
                    "isWorking": true,
                    "workingTime": 1660801715639,
                    "origQuoteOrderQty": "0.00000000",
                    "strategyId": 37463720,
                    "strategyType": 1000000,
                    "selfTradePreventionMode": "NONE",
                    "preventedMatchId": 0,
                    "preventedQuantity": "1.200000"
                },
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 2
                    }
                ]
            }
        """
        if stream_id is None:
            return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self.manager.get_timestamp()}

        if order_id is not None:
            params['orderId'] = int(order_id)
        if orig_client_order_id is not None:
            params['origClientOrderId'] = str(orig_client_order_id)
        if recv_window is not None:
            params['recvWindow'] = recv_window

        method = "order.status"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def get_order_book(self, stream_id=None, symbol: str = None, limit: int = 100, recv_window: int = None,
                       request_id: str = None) -> bool:
        """
        Get the order book.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param symbol: The selected symbol
        :type symbol: str
        :param limit: Depth limit, default is 500. Valid values 1-5000. -
                      https://developers.binance.com/docs/binance-trading-api/websocket_api#order-book
        :type limit: int
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

            .. code-block:: json

                {
                    "id": "5494febb-d167-46a2-996d-70533eb4d976",
                    "method": "depth",
                    "params": {
                        "symbol": "BNBBTC",
                        "limit": 5
                    }
                }


            Response:

            .. code-block:: json

                {
                    "id": "5494febb-d167-46a2-996d-70533eb4d976",
                    "status": 200,
                    "result": {
                        "lastUpdateId": 2731179239,
                        "bids": [
                            [
                                "0.01379900",
                                "3.43200000"
                            ],
                            [
                                "0.01379800",
                                "3.24300000"
                            ],
                            [
                                "0.01379700",
                                "10.45500000"
                            ],
                            [
                                "0.01379600",
                                "3.82100000"
                            ],
                            [
                                "0.01379500",
                                "10.26200000"
                            ]
                        ],
                        "asks": [
                            [
                                "0.01380000",
                                "5.91700000"
                            ],
                            [
                                "0.01380100",
                                "6.01400000"
                            ],
                            [
                                "0.01380200",
                                "0.26800000"
                            ],
                            [
                                "0.01380300",
                                "0.33800000"
                            ],
                            [
                                "0.01380400",
                                "0.26800000"
                            ]
                        ]
                    },
                    "rateLimits": [
                        {
                            "rateLimitType": "REQUEST_WEIGHT",
                            "interval": "MINUTE",
                            "intervalNum": 1,
                            "limit": 1200,
                            "count": 1
                        }
                    ]
                }
        """
        if stream_id is None:
            return False

        params = {"symbol": symbol.upper(),
                  "limit": str(limit)}

        if recv_window is not None:
            params['recvWindow'] = recv_window

        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "depth",
                   "params": params}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def get_server_time(self, stream_id=None, request_id: str = None) -> bool:
        """
        Test connectivity to the WebSocket API and get the current server time.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

            .. code-block:: json

                {
                    "id": "187d3cb2-942d-484c-8271-4e2141bbadb1",
                    "method": "time"
                }


            Response:

            .. code-block:: json

                {
                    "id": "187d3cb2-942d-484c-8271-4e2141bbadb1",
                    "status": 200,
                    "result": {
                        "serverTime": 1656400526260
                    },
                    "rateLimits": [{
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    }]
                }
        """
        if stream_id is None:
            return False

        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "time"}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def ping(self, stream_id=None, request_id: str = None) -> bool:
        """
        Test connectivity to the WebSocket API.

        :param stream_id: id of a stream to send the request
        :type stream_id: str
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :return: bool


        Message sent:

            .. code-block:: json

                {
                    "id": "4e72973031d8-bff9-8481-c95b-c42414df",
                    "method": "ping"
                }


            Response:

            .. code-block:: json

                {
                    "id": "4e72973031d8-bff9-8481-c95b-c42414df",
                    "status": 200,
                    "result": {},
                    "rateLimits": [{
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    }]
                }
        """
        if stream_id is None:
            return False

        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "ping"}

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        return True

    def test_create_order(self, stream_id=None, price: float = 0.0, order_type: str = None, quantity: float = 0.0,
                          side: str = None, symbol: str = None, time_in_force: str = "GTC", recv_window=None,
                          request_id: str = None) -> Union[int, bool]:
        """
        A wrapper for `create_order()` with `test='True'`

        Test order placement. Validates new order parameters and verifies your signature but does not send the order
        into the matching engine.

        """
        return self.create_order(stream_id=stream_id, price=price, order_type=order_type, quantity=quantity, side=side,
                                 symbol=symbol, time_in_force=time_in_force, test=True, recv_window=recv_window,
                                 request_id=request_id)
