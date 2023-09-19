#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/api.py
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

from typing import Optional, Union
try:
    # python <=3.7 support
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import copy
import logging
import threading


logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiApi(object):
    """
    Connect to Binance API via Websocket.

    This is valid for each `ubwa.api.method()`:

    If no `stream_id` is provided, we try to find it via a provided `stream_label`, if also not available
    we use the `stream_id` of the one active websocket api stream if there is one. But if there is not exactly
    one valid websocket api stream, this will fail! It must be clear! The stream is also valid during a
    stream restart, the payload is submitted as soon the stream is online again.

    Read these instructions to get started:

        - https://medium.lucit.tech/create-and-cancel-orders-via-websocket-on-binance-7f828831404

    Binance.com SPOT websocket API documentation:

        - https://developers.binance.com/docs/binance-trading-api/websocket_api

    :param manager: Provide the initiated UNICORN Binance WebSocket API Manager instance.
    :type manager: BinanceWebsocketApiManager
    """

    def __init__(self, manager=None):
        self.manager = manager

    def cancel_open_orders(self, process_response=None, return_response: bool = False, symbol: str = None,
                           recv_window: int = None, request_id: str = None, stream_id: str = None,
                           stream_label: str = None) -> bool:
        """
        Cancel all open orders on a symbol, including OCO orders.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#cancel-open-orders-trade

        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param symbol: The symbol you want to trade
        :type symbol: int
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self.manager.get_timestamp()}

        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "openOrders.cancelAll"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def cancel_order(self, cancel_restrictions: Optional[Literal['ONLY_NEW', 'ONLY_PARTIALLY_FILLED']] = None,
                     new_client_order_id: str = None, order_id: int = None, orig_client_order_id: str = None,
                     process_response=None, recv_window: int = None, request_id: str = None,
                     return_response: bool = False, stream_id=None, symbol: str = None,
                     stream_label: str = None) -> bool:
        """
        Cancel an active order.

        If you cancel an order that is a part of an OCO pair, the entire OCO is canceled.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#cancel-order-trade

        :param cancel_restrictions: Supported values:

                                      - ONLY_NEW: Cancel will succeed if the order status is `NEW`.

                                      - ONLY_PARTIALLY_FILLED: Cancel will succeed if order status is
                                        `PARTIALLY_FILLED`.

                                    If the cancelRestrictions value is not any of the supported values, the error will
                                    be: `{"code": -1145,"msg": "Invalid cancelRestrictions"}`

                                    If the order did not pass the conditions for cancelRestrictions, the error will be:
                                    `{"code": -2011,"msg": "Order was not canceled due to cancel restrictions."}`
        :type cancel_restrictions: str
        :param new_client_order_id: New ID for the canceled order. Automatically generated if not sent.
                                    `newClientOrderId` will replace `clientOrderId` of the canceled order, freeing it
                                    up for new orders.
        :type new_client_order_id: str
        :param order_id: Cancel by `order_id`. If both `orderId` and `origClientOrderId` parameters are specified, only
                         `orderId` is used and `origClientOrderId` is ignored.
        :type order_id: str
        :param orig_client_order_id: Cancel by `origClientOrderId`. If both `orderId` and `origClientOrderId` parameters
                                     are specified, only `orderId` is used and `origClientOrderId` is ignored.
        :type orig_client_order_id: str
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param symbol: The symbol of the order you want to cancel
        :type symbol: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self.manager.get_timestamp()}

        if cancel_restrictions is not None:
            params['cancelRestrictions'] = cancel_restrictions
        if new_client_order_id is not None:
            params['newClientOrderId'] = new_client_order_id
        if order_id is not None:
            params['orderId'] = order_id
        if orig_client_order_id is not None:
            params['origClientOrderId'] = orig_client_order_id
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "order.cancel"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def create_order(self, iceberg_qty: float = None,
                     new_client_order_id: str = None,
                     new_order_resp_type: Optional[Literal['ACK', 'RESULT', 'FULL']] = None,
                     order_type: Optional[Literal['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT',
                                                  'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT']] = None,
                     price: float = 0.0,
                     process_response=None,
                     quantity: float = 0.0,
                     recv_window: int = None,
                     request_id: str = None,
                     return_response: bool = False,
                     self_trade_prevention_mode: Optional[Literal['EXPIRE_TAKER', 'EXPIRE_MAKER',
                                                                  'EXPIRE_BOTH', 'NONE']] = None,
                     side: Optional[Literal['BUY', 'SELL']] = None,
                     stop_price: float = None,
                     strategy_id: int = None,
                     strategy_type: int = None,
                     stream_id=None,
                     stream_label: str = None,
                     symbol: str = None,
                     time_in_force: Optional[Literal['GTC', 'IOC', 'FOK']] = "GTC",
                     test: bool = False,
                     trailing_delta: int = None) -> Union[int, bool]:
        """
        Create a new order.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#place-new-order-trade

        :param iceberg_qty: Any `LIMIT` or `LIMIT_MAKER` order can be made into an iceberg order by specifying the
                            `icebergQty`. An order with an `icebergQty` must have `timeInForce` set to `GTC`.
        :type iceberg_qty: float
        :param new_client_order_id: `newClientOrderId` specifies `clientOrderId` value for the order. A new order with
                                    the same 'clientOrderId' is accepted only when the previous one is filled or
                                    expired.
        :type new_client_order_id: str
        :param new_order_resp_type: Select response format: `ACK`, `RESULT`, `FULL`.
                                    'MARKET' and 'LIMIT' orders use `FULL` by default, other order types default to
                                    'ACK'
        :type new_order_resp_type: str
        :param order_type: 'LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT',
                           'TAKE_PROFIT_LIMIT'

                           Mandatory parameters per `order_type`:

                             - LIMIT: 'timeInForce', 'price', 'quantity'

                             - LIMIT_MAKER: 'price', 'quantity'

                             - MARKET: 'quantity' or 'quoteOrderQty'

                             - STOP_LOSS: 'quantity', 'stopPrice' or 'trailingDelta'

                             - STOP_LOSS_LIMIT: 'timeInForce', 'price', 'quantity', 'stopPrice' or 'trailingDelta'

                             - TAKE_PROFIT: 'quantity', 'stopPrice' or 'trailingDelta'

                             - TAKE_PROFIT_LIMIT: 'timeInForce', 'price', 'quantity', 'stopPrice' or 'trailingDelta'
        :type order_type: str
        :param price: Price e.g. 10.223
        :type price: float
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param quantity: Amount e.g. 20.5
        :type quantity: float
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param self_trade_prevention_mode: The allowed enums for `selfTradePreventionMode` is dependent on what is
                                           configured on the symbol. The possible supported values are `EXPIRE_TAKER`,
                                           `EXPIRE_MAKER`, `EXPIRE_BOTH`, `NONE`.
        :type self_trade_prevention_mode: str
        :param side: `BUY` or `SELL`
        :type side: str
        :param strategy_id: Arbitrary numeric value identifying the order within an order strategy.
        :type strategy_id: int
        :param strategy_type: Arbitrary numeric value identifying the order strategy. Values smaller than 1000000 are
                              reserved and cannot be used.
        :type strategy_type: int
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param stop_price: Trigger order price rules for STOP_LOSS/TAKE_PROFIT orders:

                             - `stopPrice` must be above market price: STOP_LOSS BUY, TAKE_PROFIT SELL

                             - stopPrice must be below market price: STOP_LOSS SELL, TAKE_PROFIT BUY
        :type stop_price: float
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param test: Test order placement. Validates new order parameters and verifies your signature but does not
                     send the order into the matching engine.
        :type test: bool
        :param time_in_force: Available timeInForce options, setting how long the order should be active before
                              expiration:

                                - GTC: Good 'til Canceled – the order will remain on the book until you cancel it, or
                                  the order is completely filled.

                                - IOC: Immediate or Cancel – the order will be filled for as much as possible, the
                                  unfilled quantity immediately expires.

                                - FOK: Fill or Kill – the order will expire unless it cannot be immediately filled for
                                  the entire quantity.

                              `MARKET` orders using `quoteOrderQty` follow `LOT_SIZE` filter rules. The order will
                              execute a quantity that has notional value as close as possible to requested
                              `quoteOrderQty`.
        :type time_in_force: str
        :param trailing_delta: For more details on SPOT implementation on trailing stops, please refer to
                               `Trailing Stop FAQ <https://github.com/binance/binance-spot-api-docs/blob/master/faqs/trailing-stop-faq.md>`_
        :type trailing_delta: int

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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
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

        if iceberg_qty is not None:
            params['icebergQty'] = str(iceberg_qty)
        if new_order_resp_type is not None:
            params['newOrderRespType'] = new_order_resp_type
        if side.upper() == "LIMIT":
            params['price'] = str(price)
            params['timeInForce'] = time_in_force
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)
        if self_trade_prevention_mode is not None:
            params['selfTradePreventionMode'] = self_trade_prevention_mode
        if stop_price is not None:
            params['stopPrice'] = str(stop_price)
        if strategy_id is not None:
            params['strategyId'] = str(strategy_id)
        if strategy_type is not None:
            params['strategyType'] = str(strategy_type)
        if trailing_delta is not None:
            params['trailingDelta'] = str(trailing_delta)

        method = "order.test" if test is True else "order.place"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return new_client_order_id

    def create_test_order(self, iceberg_qty: float = None,
                          new_client_order_id: str = None,
                          new_order_resp_type: Optional[Literal['ACK', 'RESULT', 'FULL']] = None,
                          order_type: Optional[Literal['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT',
                                                       'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT']] = None,
                          price: float = 0.0,
                          process_response=None,
                          quantity: float = 0.0,
                          recv_window: int = None,
                          request_id: str = None,
                          return_response: bool = False,
                          self_trade_prevention_mode: Optional[Literal['EXPIRE_TAKER', 'EXPIRE_MAKER',
                                                                       'EXPIRE_BOTH', 'NONE']] = None,
                          side: Optional[Literal['BUY', 'SELL']] = None,
                          stop_price: float = None,
                          strategy_id: int = None,
                          strategy_type: int = None,
                          stream_id=None,
                          stream_label: str = None,
                          symbol: str = None,
                          time_in_force: Optional[Literal['GTC', 'IOC', 'FOK']] = "GTC",
                          trailing_delta: int = None) -> Union[int, bool]:
        """
        Test order placement.

        Validates new order parameters and verifies your signature but does not send the order into the matching engine.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#test-new-order-trade

        :param iceberg_qty: Any `LIMIT` or `LIMIT_MAKER` order can be made into an iceberg order by specifying the
                            `icebergQty`. An order with an `icebergQty` must have `timeInForce` set to `GTC`.
        :type iceberg_qty: float
        :param new_client_order_id: `newClientOrderId` specifies `clientOrderId` value for the order. A new order with
                                    the same 'clientOrderId' is accepted only when the previous one is filled or
                                    expired.
        :type new_client_order_id: str
        :param new_order_resp_type: Select response format: `ACK`, `RESULT`, `FULL`.
                                    'MARKET' and 'LIMIT' orders use `FULL` by default, other order types default to
                                    'ACK'
        :type new_order_resp_type: str
        :param order_type: 'LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT',
                           'TAKE_PROFIT_LIMIT'

                           Mandatory parameters per `order_type`:

                             - LIMIT: 'timeInForce', 'price', 'quantity'

                             - LIMIT_MAKER: 'price', 'quantity'

                             - MARKET: 'quantity' or 'quoteOrderQty'

                             - STOP_LOSS: 'quantity', 'stopPrice' or 'trailingDelta'

                             - STOP_LOSS_LIMIT: 'timeInForce', 'price', 'quantity', 'stopPrice' or 'trailingDelta'

                             - TAKE_PROFIT: 'quantity', 'stopPrice' or 'trailingDelta'

                             - TAKE_PROFIT_LIMIT: 'timeInForce', 'price', 'quantity', 'stopPrice' or 'trailingDelta'
        :type order_type: str
        :param price: Price e.g. 10.223
        :type price: float
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param quantity: Amount e.g. 20.5
        :type quantity: float
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param self_trade_prevention_mode: The allowed enums for `selfTradePreventionMode` is dependent on what is
                                           configured on the symbol. The possible supported values are `EXPIRE_TAKER`,
                                           `EXPIRE_MAKER`, `EXPIRE_BOTH`, `NONE`.
        :type self_trade_prevention_mode: str
        :param side: `BUY` or `SELL`
        :type side: str
        :param strategy_id: Arbitrary numeric value identifying the order within an order strategy.
        :type strategy_id: int
        :param strategy_type: Arbitrary numeric value identifying the order strategy. Values smaller than 1000000 are
                              reserved and cannot be used.
        :type strategy_type: int
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param stop_price: Trigger order price rules for STOP_LOSS/TAKE_PROFIT orders:

                             - `stopPrice` must be above market price: STOP_LOSS BUY, TAKE_PROFIT SELL

                             - stopPrice must be below market price: STOP_LOSS SELL, TAKE_PROFIT BUY
        :type stop_price: float
        :param symbol: The symbol you want to trade
        :type symbol: str
        :param time_in_force: Available timeInForce options, setting how long the order should be active before
                              expiration:

                                - GTC: Good 'til Canceled – the order will remain on the book until you cancel it, or
                                  the order is completely filled.

                                - IOC: Immediate or Cancel – the order will be filled for as much as possible, the
                                  unfilled quantity immediately expires.

                                - FOK: Fill or Kill – the order will expire unless it cannot be immediately filled for
                                  the entire quantity.

                              `MARKET` orders using `quoteOrderQty` follow `LOT_SIZE` filter rules. The order will
                              execute a quantity that has notional value as close as possible to requested
                              `quoteOrderQty`.
        :type time_in_force: str
        :param trailing_delta: For more details on SPOT implementation on trailing stops, please refer to
                               `Trailing Stop FAQ <https://github.com/binance/binance-spot-api-docs/blob/master/faqs/trailing-stop-faq.md>`_
        :type trailing_delta: int

        :return: `False` or `orig_client_order_id`


        Message sent:

        .. code-block:: json

            {
                "id": "56374a46-3061-486b-a311-99ee972eb648",
                "method": "order.test",
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
        return self.create_order(iceberg_qty=iceberg_qty, new_client_order_id=new_client_order_id,
                                 new_order_resp_type=new_order_resp_type, price=price, order_type=order_type,
                                 process_response=process_response, quantity=quantity, recv_window=recv_window,
                                 request_id=request_id, return_response=return_response,
                                 self_trade_prevention_mode=self_trade_prevention_mode, side=side,
                                 stop_price=stop_price, strategy_id=strategy_id, strategy_type=strategy_type,
                                 stream_id=stream_id, stream_label=stream_label, symbol=symbol,
                                 time_in_force=time_in_force, test=True, trailing_delta=trailing_delta)

    def get_account_status(self, process_response=None, recv_window: int = None, request_id: str = None,
                           return_response: bool = False, stream_id=None, stream_label: str = None) -> bool:
        """
        Get the user account status.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#account-information-user_data

        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "timestamp": self.manager.get_timestamp()}

        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "account.status"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def get_exchange_info(self, permissions: list = None, process_response=None, recv_window: int = None,
                          request_id: str = None, return_response: bool = False, stream_id=None,
                          stream_label: str = None, symbol: str = None, symbols: list = None) -> bool:
        """
        Get the Exchange Information.

        Only one of `symbol`, `symbols`, `permissions` parameters can be specified.

        Without parameters, `exchangeInfo` displays all symbols with ["SPOT, "MARGIN", "LEVERAGED"] permissions. In
        order to list all active symbols on the exchange, you need to explicitly request all permissions

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#exchange-information

        :param permissions: Filter symbols by permissions. `permissions` accepts either a list of permissions, or a
                            single permission name: "SPOT".
                            `Available Permissions <https://developers.binance.com/docs/binance-trading-api/websocket_api#permissions>`_
        :type permissions: list
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param symbol: Describe a single symbol
        :type symbol: str
        :param symbols: Describe multiple symbols.
        :type symbols: list
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False
        if symbol is not None:
            params = {"symbol": symbol}
        if symbols is not None:
            symbols = [symbol.upper() for symbol in symbols]
            params = {"symbols": symbols}
        if permissions is not None:
            params = {"permissions": permissions}

        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "exchangeInfo"
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def get_open_orders(self, process_response=None, recv_window: int = None, request_id: str = None,
                        return_response: bool = False, stream_id=None, stream_label: str = None,
                        symbol: str = None) -> bool:
        """
        Query execution status of all open orders.

        Open orders are always returned as a flat list. If all symbols are requested, use the symbol field to tell
        which symbol the orders belong to.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#current-open-orders-user_data

        If you need to continuously monitor order status updates, please consider using
        'WebSocket Streams <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream>`_

          - `userData`

          - `executionReport` user data stream event

        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param symbol: If omitted, open orders for all symbols are returned.
        :type symbol: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self.manager.get_timestamp()}

        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "openOrders.status"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def get_order(self, order_id: int = None, orig_client_order_id: str = None, process_response=None,
                  recv_window: int = None, request_id: str = None, return_response: bool = False, stream_id=None,
                  stream_label: str = None, symbol: str = None) -> bool:
        """
        Check execution status of an order.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#query-order-user_data

        If both `orderId` and `origClientOrderId` parameters are specified, only `orderId` is used and
        `origClientOrderId` is ignored.

        For some historical orders the `cummulativeQuoteQty` response field may be negative, meaning the data is not
        available at this time.

        :param order_id: Lookup order by `orderId`.
        :type order_id: int
        :param orig_client_order_id: Lookup order by `clientOrderId`.
        :type orig_client_order_id: str
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param symbol: The symbol you want to trade
        :type symbol: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self.manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self.manager.get_timestamp()}

        if order_id is not None:
            params['orderId'] = int(order_id)
        if orig_client_order_id is not None:
            params['origClientOrderId'] = str(orig_client_order_id)
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "order.status"
        api_secret = self.manager.stream_list[stream_id]['api_secret']
        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self.manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def get_order_book(self, process_response=None, limit: int = None, recv_window: int = None, request_id: str = None,
                       return_response: bool = False, stream_id=None, stream_label: str = None,
                       symbol: str = None) -> bool:
        """
        Get current order book.

        Note that this request returns limited market depth.

        If you need to continuously monitor order book updates, please consider using
        'WebSocket Streams <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream>'_

          - <symbol>@depth<levels>

          - <symbol>@depth

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#order-book

        :param limit: Default 100; max 5000.
        :type limit: int
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param symbol: The selected symbol
        :type symbol: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"symbol": symbol.upper()}

        if limit is not None:
            params['limit'] = str(limit)
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "depth",
                   "params": params}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def get_server_time(self, process_response=None, request_id: str = None, return_response: bool = False,
                        stream_id=None, stream_label: str = None) -> bool:
        """
        Test connectivity to the WebSocket API and get the current server time.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#check-server-time

        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "time"}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True

    def ping(self, process_response=None, request_id: str = None, return_response: bool = False,
             stream_id=None, stream_label: str = None) -> bool:
        """
        Test connectivity to the WebSocket API.

        Official documentation:

            - https://developers.binance.com/docs/binance-trading-api/websocket_api#test-connectivity

        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param request_id: Provide a custom id for the request
        :type request_id: str
        :param return_response: If `True` the response of the API request is waited for and returned directly.
                                However, this increases the execution time of the function by the duration until the
                                response is received from the Binance API.
        :type return_response: bool
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
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
            if stream_label is not None:
                stream_id = self.manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self.manager.get_the_one_active_websocket_api()
            if stream_id is False:
                logger.critical(f"BinanceWebSocketApiApi.cancel_open_orders() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        request_id = self.manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "ping"}

        if process_response is not None:
            with self.manager.process_response_lock:
                entry = {'callback_function': process_response}
                self.manager.process_response[request_id] = entry

        self.manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if return_response is True:
            with self.manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self.manager.return_response[request_id] = entry
            self.manager.return_response[request_id]['event_return_response'].wait()
            with self.manager.return_response_lock:
                response_value = copy.deepcopy(self.manager.return_response[request_id]['response_value'])
                del self.manager.return_response[request_id]
            return response_value

        return True
