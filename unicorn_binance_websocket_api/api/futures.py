#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_websocket_api/api/futures.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from typing import Optional, Union, Literal
import logging
import threading

__logger__: logging.getLogger = logging.getLogger("unicorn_binance_websocket_api")

logger = __logger__


class BinanceWebSocketApiApiFutures(object):
    """
    Connect to Binance Futures API via Websocket.

    Namespace: `ubwa.api.futures.*`:

    If no `stream_id` is provided, we try to find it via a provided `stream_label`, if also not available
    we use the `stream_id` of the one active websocket api stream if there is one. But if there is not exactly
    one valid websocket api stream, this will fail! It must be clear! The stream is also valid during a
    stream restart, the payload is submitted as soon the stream is online again.

    Todo:
        - https://binance-docs.github.io/apidocs/futures/en/#account-information-v2-user_data-2
        - https://binance-docs.github.io/apidocs/futures/en/#account-information-user_data
        - https://binance-docs.github.io/apidocs/futures/en/#futures-account-balance-v2-user_data-2
        - https://binance-docs.github.io/apidocs/futures/en/#futures-account-balance-user_data
        - https://binance-docs.github.io/apidocs/futures/en/#position-information-v2-user_data-2
        - https://binance-docs.github.io/apidocs/futures/en/#position-information-user_data
        - https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker-2
        - https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker-2


    Read these instructions to get started:

        - https://medium.lucit.tech/create-and-cancel-orders-via-websocket-on-binance-7f828831404

    Binance.com Futures websocket API documentation:

        - https://binance-docs.github.io/apidocs/futures/en/#websocket-api

    :param manager: Provide the initiated UNICORN Binance WebSocket API Manager instance.
    :type manager: BinanceWebsocketApiManager
    """

    def __init__(self, manager=None):
        self._manager = manager

    def cancel_order(self, order_id: int = None, orig_client_order_id: str = None,
                     process_response=None, recv_window: int = None, request_id: str = None,
                     return_response: bool = False, stream_id: str = None, symbol: str = None,
                     stream_label: str = None) -> Union[str, dict, bool]:
        """
        Cancel an active order.

        Either order_id or orig_client_order_id must be sent.

        Weight: 1

        Official documentation:

            - https://binance-docs.github.io/apidocs/futures/en/#cancel-order-trade-2

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

        :return: str, dict, bool

        Message sent:

        .. code-block:: json

            {
                "id": "5633b6a2-90a9-4192-83e7-925c90b6a2fd",
                "method": "order.cancel",
                "params": {
                    "apiKey": "HsOehcfih8ZRxnhjp2XjGXhsOBd6msAhKz9joQaWwZ7arcJTlD2hGOGQj1lGdTjR",
                    "orderId": 283194212,
                    "symbol": "BTCUSDT",
                    "timestamp": 1703439070722,
                    "signature": "b09c49815b4e3f1f6098cd9fbe26a933a9af79803deaaaae03c29f719c08a8a8"
                }
            }


        Response:

        .. code-block:: json

            {
              "id": "5633b6a2-90a9-4192-83e7-925c90b6a2fd",
              "status": 200,
              "result": {
                "clientOrderId": "myOrder1",
                "cumQty": "0",
                "cumQuote": "0",
                "executedQty": "0",
                "orderId": 283194212,
                "origQty": "11",
                "origType": "TRAILING_STOP_MARKET",
                "price": "0",
                "reduceOnly": false,
                "side": "BUY",
                "positionSide": "SHORT",
                "status": "CANCELED",
                "stopPrice": "9300",                // please ignore when order type is TRAILING_STOP_MARKET
                "closePosition": false,   // if Close-All
                "symbol": "BTCUSDT",
                "timeInForce": "GTC",
                "type": "TRAILING_STOP_MARKET",
                "activatePrice": "9020",            // activation price, only return with TRAILING_STOP_MARKET order
                "priceRate": "0.3",                 // callback rate, only return with TRAILING_STOP_MARKET order
                "updateTime": 1571110484038,
                "workingType": "CONTRACT_PRICE",
                "priceProtect": false,            // if conditional order trigger is protected
                "priceMatch": "NONE",              //price match mode
                "selfTradePreventionMode": "NONE", //self trading prevention mode
                "goodTillDate": 0                  //order pre-set auto cancel time for TIF GTD order
              },
              "rateLimits": [
                {
                  "rateLimitType": "REQUEST_WEIGHT",
                  "interval": "MINUTE",
                  "intervalNum": 1,
                  "limit": 2400,
                  "count": 1
                }
              ]
            }
        """
        if stream_id is None:
            if stream_label is not None:
                stream_id = self._manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self._manager.get_the_one_active_websocket_api()
            if stream_id is None:
                logger.critical(f"BinanceWebSocketApiApiFutures.cancel_order() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self._manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self._manager.get_timestamp()}

        if order_id is not None:
            params['orderId'] = order_id
        if orig_client_order_id is not None:
            params['origClientOrderId'] = orig_client_order_id
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "order.cancel"
        api_secret = self._manager.stream_list[stream_id]['api_secret']
        request_id = self._manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self._manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if self._manager.send_with_stream(stream_id=stream_id, payload=payload) is False:
            self._manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if process_response is not None:
            with self._manager.process_response_lock:
                entry = {'callback_function': process_response}
                self._manager.process_response[request_id] = entry

        if return_response is True:
            with self._manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self._manager.return_response[request_id] = entry
            self._manager.return_response[request_id]['event_return_response'].wait()
            with self._manager.return_response_lock:
                response_value = self._manager.return_response[request_id]['response_value']
                del self._manager.return_response[request_id]
            return response_value

        return True

    def create_order(self,
                     activation_price: float = None,
                     callback_rate: float = None,
                     close_position: bool = None,
                     good_till_date: int = None,
                     new_client_order_id: str = None,
                     new_order_resp_type: Optional[Literal['ACK', 'RESULT', 'FULL']] = None,
                     order_type: Optional[Literal['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT',
                                                  'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT']] = None,
                     position_side: Optional[Literal['BOTH', 'LONG', 'SHORT']] = None,
                     price: float = 0.0,
                     price_match: Optional[Literal['OPPONENT', 'OPPONENT_5', 'OPPONENT_10', 'OPPONENT_20', 'QUEUE',
                                                   'QUEUE_5', 'QUEUE_10, QUEUE_20']] = None,
                     price_protect: bool = None,
                     process_response=None,
                     quantity: float = None,
                     recv_window: int = None,
                     reduce_only: bool = None,
                     request_id: str = None,
                     return_response: bool = False,
                     self_trade_prevention_mode: Optional[Literal['EXPIRE_TAKER', 'EXPIRE_MAKER',
                                                                  'EXPIRE_BOTH', 'NONE']] = None,
                     side: Optional[Literal['BUY', 'SELL']] = None,
                     stop_price: float = None,
                     stream_id: str = None,
                     stream_label: str = None,
                     symbol: str = None,
                     time_in_force: Optional[Literal['GTD', 'GTC', 'IOC', 'FOK']] = None,
                     working_type: Optional[Literal['MARK_PRICE', 'CONTRACT_PRICE']] = None) \
            -> Union[str, dict, bool, tuple]:
        """
        Create a new order.

        Weight: 0

        Official documentation:

            - https://binance-docs.github.io/apidocs/futures/en/#new-order-trade-2

        :param activation_price: Used with TRAILING_STOP_MARKET orders, default as the latest price(supporting
                                 different workingType)
        :type activation_price: float
        :param callback_rate: Used with TRAILING_STOP_MARKET orders, min 0.1, max 5 where 1 for 1%
        :type callback_rate: float
        :param close_position: True, False；Close-All，used with STOP_MARKET or TAKE_PROFIT_MARKET.
        :type close_position: bool
        :param good_till_date: Order cancel time for timeInForce GTD, mandatory when timeInforce set to GTD; order the
                               timestamp only retains second-level precision, ms part will be ignored; The goodTillDate
                               timestamp must be greater than the current time plus 600 seconds and smaller than
                               253402300799000
        :type good_till_date: int
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

                             - LIMIT: time_in_force, quantity, price

                             - MARKET: quantity

                             - STOP/TAKE_PROFIT: quantity, price, stop_price

                             - STOP_MARKET/TAKE_PROFIT_MARKET: stop_price

                             - TRAILING_STOP_MARKET: callback_rate

        :type order_type: str
        :param price: Price e.g. 10.223
        :type price: float
        :param position_side: Default BOTH for One-way Mode; LONG or SHORT for Hedge Mode. It must be sent in Hedge
                              Mode.
        :type position_side: str
        :param price_match: only available for LIMIT/STOP/TAKE_PROFIT order; can be set to OPPONENT/ OPPONENT_5/
                            OPPONENT_10/ OPPONENT_20: /QUEUE/ QUEUE_5/ QUEUE_10/ QUEUE_20; Can't be passed together
                            with price
        :type price_match: str
        :param price_protect: True, False；default False. Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET
                              orders.
        :type price_protect: bool
        :param process_response: Provide a function/method to process the received webstream data (callback)
                                 of this specific request.
        :type process_response: function
        :param quantity: Amount e.g. 20.5
        :type quantity: float
        :param recv_window: An additional parameter, `recvWindow`, may be sent to specify the number of milliseconds
                            after timestamp the request is valid for. If `recvWindow` is not sent, it defaults to 5000.
                            The value cannot be greater than 60000.
        :type recv_window: int
        :param reduce_only: True, False；default False. Cannot be sent in Hedge Mode; cannot be sent with
                            close_position=True
        :type reduce_only: bool
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

                                - GTD: Good til Date

                                - GTC: Good til Canceled – the order will remain on the book until you cancel it, or
                                  the order is completely filled.

                                - IOC: Immediate or Cancel – the order will be filled for as much as possible, the
                                  unfilled quantity immediately expires.

                                - FOK: Fill or Kill – the order will expire unless it cannot be immediately filled for
                                  the entire quantity.

                              `MARKET` orders using `quoteOrderQty` follow `LOT_SIZE` filter rules. The order will
                              execute a quantity that has notional value as close as possible to requested
                              `quoteOrderQty`.
        :type time_in_force: str
        :param working_type: stopPrice triggered by: "MARK_PRICE", "CONTRACT_PRICE". Default "CONTRACT_PRICE"
        :type working_type: str

        :return: str (new_client_order_id), bool or tuple (str (new_client_order_id), str/dict (response_value))

        Message sent:

        .. code-block:: json

            {
                "id": "3f7df6e3-2df4-44b9-9919-d2f38f90a99a",
                "method": "order.place",
                "params": {
                    "apiKey": "HMOchcfii9ZRZnhjp2XjGXhsOBd6msAhKz9joQaWwZ7arcJTlD2hGPHQj1lGdTjR",
                    "positionSide": "BOTH",
                    "price": "43187.00",
                    "quantity": 0.1,
                    "side": "BUY",
                    "symbol": "BTCUSDT",
                    "timeInForce": "GTC",
                    "timestamp": 1702555533821,
                    "type": "LIMIT",
                    "signature": "0f04368b2d22aafd0ggc8809ea34297eff602272917b5f01267db4efbc1c9422"
                }
            }

        Response

        .. code-block:: json

            {
                "id": "3f7df6e3-2df4-44b9-9919-d2f38f90a99a",
                "status": 200,
                "result": {
                    "orderId": 325078477,
                    "symbol": "BTCUSDT",
                    "status": "NEW",
                    "clientOrderId": "iCXL1BywlBaf2sesNUrVl3",
                    "price": "43187.00",
                    "avgPrice": "0.00",
                    "origQty": "0.100",
                    "executedQty": "0.000",
                    "cumQty": "0.000",
                    "cumQuote": "0.00000",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "reduceOnly": false,
                    "closePosition": false,
                    "side": "BUY",
                    "positionSide": "BOTH",
                    "stopPrice": "0.00",
                    "workingType": "CONTRACT_PRICE",
                    "priceProtect": false,
                    "origType": "LIMIT",
                    "priceMatch": "NONE",
                    "selfTradePreventionMode": "NONE",
                    "goodTillDate": 0,
                    "updateTime": 1702555534435
                },
                "rateLimits": [
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "intervalNum": 10,
                        "limit": 300,
                        "count": 1
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    },
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 2400,
                        "count": 1
                    }
                ]
            }
        """
        if stream_id is None:
            if stream_label is not None:
                stream_id = self._manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self._manager.get_the_one_active_websocket_api()
            if stream_id is None:
                logger.critical(f"BinanceWebSocketApiApiFutures.create_order() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        new_client_order_id = new_client_order_id if new_client_order_id is not None else str(self._manager.get_request_id())
        params = {"apiKey": self._manager.stream_list[stream_id]['api_key'],
                  "newClientOrderId": new_client_order_id,
                  "side": side.upper(),
                  "symbol": symbol.upper(),
                  "timestamp": self._manager.get_timestamp(),
                  "type": order_type}

        if activation_price is not None:
            params['activationPrice'] = activation_price
        if callback_rate is not None:
            params['callbackRate'] = callback_rate
        if close_position is not None:
            params['closePosition'] = "true" if close_position is True else "false"
        if good_till_date is not None:
            params['goodTillDate'] = good_till_date
        if new_order_resp_type is not None:
            params['newOrderRespType'] = new_order_resp_type
        if (order_type.upper() == "LIMIT" or
                order_type.upper() == "LIMIT_MAKER" or
                order_type.upper() == "STOP_LOSS_LIMIT" or
                order_type.upper() == "TAKE_PROFIT_LIMIT"):
            params['price'] = str(price)
        if (order_type.upper() == "LIMIT" or
                order_type.upper() == "STOP_LOSS_LIMIT" or
                order_type.upper() == "TAKE_PROFIT_LIMIT"):
            params['timeInForce'] = time_in_force
        if position_side is not None:
            params['positionSide'] = position_side
        if price_match is not None:
            params['priceMatch'] = price_match
        if price_protect is not None:
            params['priceProtect'] = "TRUE" if price_protect is True else "FALSE"
        if quantity is not None:
            params['quantity'] = str(quantity)
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)
        if reduce_only is not None:
            params['reduceOnly'] = "true" if reduce_only is True else "false"
        if self_trade_prevention_mode is not None:
            params['selfTradePreventionMode'] = self_trade_prevention_mode
        if stop_price is not None:
            params['stopPrice'] = str(stop_price)
        if working_type is not None:
            params['workingType'] = working_type

        method = "order.place"
        api_secret = self._manager.stream_list[stream_id]['api_secret']
        request_id = self._manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self._manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if self._manager.send_with_stream(stream_id=stream_id, payload=payload) is False:
            self._manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if process_response is not None:
            with self._manager.process_response_lock:
                entry = {'callback_function': process_response}
                self._manager.process_response[request_id] = entry

        if return_response is True:
            with self._manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self._manager.return_response[request_id] = entry
            self._manager.return_response[request_id]['event_return_response'].wait()
            with self._manager.return_response_lock:
                response_value = self._manager.return_response[request_id]['response_value']
                del self._manager.return_response[request_id]
            return new_client_order_id, response_value

        return new_client_order_id

    def get_order(self, order_id: int = None, orig_client_order_id: str = None, process_response=None,
                  recv_window: int = None, request_id: str = None, return_response: bool = False, stream_id: str = None,
                  stream_label: str = None, symbol: str = None) -> Union[str, dict, bool]:
        """
        Check execution status of an order.

        Official documentation:

            - https://binance-docs.github.io/apidocs/futures/en/#query-order-user_data-2

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

        :return: str, dict, bool

        Message sent:

        .. code-block:: json

            {
                "id": "0ce5d070-a5e5-4ff2-b57f-1556741a4204",
                "method": "order.status",
                "params": {
                    "apiKey": "HMOchcfii9ZRZnhjp2XjGXhsOBd6msAhKz9joQaWwZ7arcJTlD2hGPHQj1lGdTjR",
                    "orderId": 328999071,
                    "symbol": "BTCUSDT",
                    "timestamp": 1703441060152,
                    "signature": "ba48184fc38a71d03d2b5435bd67c1206e3191e989fe99bda1bc643a880dfdbf"
                }
            }

        Response:

        .. code-block:: json

            {
                "id": "0ce5d070-a5e5-4ff2-b57f-1556741a4204",
                "status": 200,
                "result": {
                    "orderId": 328999071,
                    "symbol": "BTCUSDT",
                    "status": "NEW",
                    "clientOrderId": "bK2CASGXToGAKVsePruSCs",
                    "price": "43634.50",
                    "avgPrice": "0.00",
                    "origQty": "0.010",
                    "executedQty": "0.000",
                    "cumQuote": "0.00000",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "reduceOnly": false,
                    "closePosition": false,
                    "side": "BUY",
                    "positionSide": "BOTH",
                    "stopPrice": "0.00",
                    "workingType": "CONTRACT_PRICE",
                    "priceProtect": false,
                    "origType": "LIMIT",
                    "priceMatch": "NONE",
                    "selfTradePreventionMode": "NONE",
                    "goodTillDate": 0,
                    "time": 1703441059890,
                    "updateTime": 1703441059890
                },
                "rateLimits": [
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 2400,
                        "count": 6
                    }
                ]
            }
        """
        if stream_id is None:
            if stream_label is not None:
                stream_id = self._manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self._manager.get_the_one_active_websocket_api()
            if stream_id is None:
                logger.critical(f"BinanceWebSocketApiApiFutures.get_order() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self._manager.stream_list[stream_id]['api_key'],
                  "symbol": symbol.upper(),
                  "timestamp": self._manager.get_timestamp()}

        if order_id is not None:
            params['orderId'] = int(order_id)
        if orig_client_order_id is not None:
            params['origClientOrderId'] = str(orig_client_order_id)
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "order.status"
        api_secret = self._manager.stream_list[stream_id]['api_secret']
        request_id = self._manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self._manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if self._manager.send_with_stream(stream_id=stream_id, payload=payload) is False:
            self._manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if process_response is not None:
            with self._manager.process_response_lock:
                entry = {'callback_function': process_response}
                self._manager.process_response[request_id] = entry

        if return_response is True:
            with self._manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self._manager.return_response[request_id] = entry
            self._manager.return_response[request_id]['event_return_response'].wait()
            with self._manager.return_response_lock:
                response_value = self._manager.return_response[request_id]['response_value']
                del self._manager.return_response[request_id]
            return response_value

        return True

    def get_order_book(self, process_response=None, limit: int = None, recv_window: int = None, request_id: str = None,
                       return_response: bool = False, stream_id: str = None, stream_label: str = None,
                       symbol: str = None) -> Union[str, dict, bool]:
        """
        Get current order book.

        Note that this request returns limited market depth.

        If you need to continuously monitor order book updates, please consider using
        'WebSocket Streams <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream>'_

          - <symbol>@depth<levels>

          - <symbol>@depth

        Official documentation:

            - https://binance-docs.github.io/apidocs/futures/en/#order-book-2

        :param limit: Default 500; Valid limits:[5, 10, 20, 50, 100, 500, 1000]
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

        :return: str, dict, bool

        Message sent:

        .. code-block:: json

            {
                "id": "51e2affb-0aba-4821-ba75-f2625006eb43",
                "method": "depth",
                "params": {
                  "symbol": "BTCUSDT"
                }
            }

        Response:

        .. code-block:: json

            {
              "id": "51e2affb-0aba-4821-ba75-f2625006eb43",
              "status": 200,
              "result": {
                "lastUpdateId": 1027024,
                "E": 1589436922972,   // Message output time
                "T": 1589436922959,   // Transaction time
                "bids": [
                  [
                    "4.00000000",     // PRICE
                    "431.00000000"    // QTY
                  ]
                ],
                "asks": [
                  [
                    "4.00000200",
                    "12.00000000"
                  ]
                ]
              },
              "rateLimits": [
                {
                  "rateLimitType": "REQUEST_WEIGHT",
                  "interval": "MINUTE",
                  "intervalNum": 1,
                  "limit": 2400,
                  "count": 5
                }
              ]
            }
        """
        if stream_id is None:
            if stream_label is not None:
                stream_id = self._manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self._manager.get_the_one_active_websocket_api()
            if stream_id is None:
                logger.critical(f"BinanceWebSocketApiApiFutures.get_order_book() - error_msg: No `stream_id` provided "
                                f"or found!")
                return False

        params = {"symbol": symbol.upper()}

        if limit is not None:
            params['limit'] = str(limit)
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        request_id = self._manager.get_new_uuid_id() if request_id is None else request_id

        payload = {"id": request_id,
                   "method": "depth",
                   "params": params}

        if self._manager.send_with_stream(stream_id=stream_id, payload=payload) is False:
            self._manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if process_response is not None:
            with self._manager.process_response_lock:
                entry = {'callback_function': process_response}
                self._manager.process_response[request_id] = entry

        if return_response is True:
            with self._manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self._manager.return_response[request_id] = entry
            self._manager.return_response[request_id]['event_return_response'].wait()
            with self._manager.return_response_lock:
                response_value = self._manager.return_response[request_id]['response_value']
                del self._manager.return_response[request_id]
            return response_value

        return True

    def modify_order(self,
                     order_id: int = None,
                     orig_client_order_id: str = None,
                     price: float = 0.0,
                     price_match: Optional[Literal['OPPONENT', 'OPPONENT_5', 'OPPONENT_10', 'OPPONENT_20', 'QUEUE',
                                                   'QUEUE_5', 'QUEUE_10, QUEUE_20']] = None,
                     process_response=None,
                     quantity: float = None,
                     recv_window: int = None,
                     request_id: str = None,
                     return_response: bool = False,
                     side: Optional[Literal['BUY', 'SELL']] = None,
                     stream_id: str = None,
                     stream_label: str = None,
                     symbol: str = None) \
            -> Union[str, dict, bool, tuple]:
        """
        Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered
        in the match queue

        Weight: 1 on 10s order rate limit(X-MBX-ORDER-COUNT-10S); 1 on 1min order rate limit(X-MBX-ORDER-COUNT-1M); 1 on
        IP rate limit(x-mbx-used-weight-1m)

        Official documentation:

            - https://binance-docs.github.io/apidocs/futures/en/#modify-order-trade-2

        :param order_id: Cancel by `order_id`. If both `orderId` and `origClientOrderId` parameters are specified, only
                         `orderId` is used and `origClientOrderId` is ignored.
        :type order_id: str
        :param orig_client_order_id: Cancel by `origClientOrderId`. If both `orderId` and `origClientOrderId` parameters
                                     are specified, only `orderId` is used and `origClientOrderId` is ignored.
        :type orig_client_order_id: str
        :param price: Price e.g. 10.223
        :type price: float
        :param price_match: only available for LIMIT/STOP/TAKE_PROFIT order; can be set to OPPONENT/ OPPONENT_5/
                            OPPONENT_10/ OPPONENT_20: /QUEUE/ QUEUE_5/ QUEUE_10/ QUEUE_20; Can't be passed together
                            with price
        :type price_match: str
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
        :param side: `BUY` or `SELL`
        :type side: str
        :param stream_id: ID of a stream to send the request
        :type stream_id: str
        :param stream_label: Label of a stream to send the request. Only used if `stream_id` is not provided!
        :type stream_label: str
        :param symbol: The symbol you want to trade
        :type symbol: str

        :return: str, dict, bool

        Message sent:

        .. code-block:: json

            {
                "id": "c8c271ba-de70-479e-870c-e64951c753d9",
                "method": "order.modify",
                "params": {
                    "apiKey": "HMOchcfiT9ZRZnhjp2XjGXhsOBd6msAhKz9joQaWwZ7arcJTlD2hGPHQj1lGdTjR",
                    "orderId": 328971409,
                    "origType": "LIMIT",
                    "positionSide": "SHORT",
                    "price": "43769.1",
                    "priceMatch": "NONE",
                    "quantity": "0.11",
                    "side": "SELL",
                    "symbol": "BTCUSDT",
                    "timestamp": 1703426755754,
                    "signature": "d30c9f0736a307f5a9988d4a40b688662d18324b17367d51421da5484e835923"
                }
            }

        Response

        .. code-block:: json

            {
                "id": "c8c271ba-de70-479e-870c-e64951c753d9",
                "status": 200,
                "result": {
                    "orderId": 328971409,
                    "symbol": "BTCUSDT",
                    "status": "NEW",
                    "clientOrderId": "xGHfltUMExx0TbQstQQfRX",
                    "price": "43769.10",
                    "avgPrice": "0.00",
                    "origQty": "0.110",
                    "executedQty": "0.000",
                    "cumQty": "0.000",
                    "cumQuote": "0.00000",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "reduceOnly": false,
                    "closePosition": false,
                    "side": "SELL",
                    "positionSide": "SHORT",
                    "stopPrice": "0.00",
                    "workingType": "CONTRACT_PRICE",
                    "priceProtect": false,
                    "origType": "LIMIT",
                    "priceMatch": "NONE",
                    "selfTradePreventionMode": "NONE",
                    "goodTillDate": 0,
                    "updateTime": 1703426756190
                },
                "rateLimits": [
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "intervalNum": 10,
                        "limit": 300,
                        "count": 1
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 1200,
                        "count": 1
                    },
                    {
                        "rateLimitType": "REQUEST_WEIGHT",
                        "interval": "MINUTE",
                        "intervalNum": 1,
                        "limit": 2400,
                        "count": 1
                    }
                ]
            }
        """
        if stream_id is None:
            if stream_label is not None:
                stream_id = self._manager.get_stream_id_by_label(stream_label=stream_label)
            else:
                stream_id = self._manager.get_the_one_active_websocket_api()
            if stream_id is None:
                logger.critical(f"BinanceWebSocketApiApiFutures.modify_order() - error_msg: No `stream_id` provided or "
                                f"found!")
                return False

        params = {"apiKey": self._manager.stream_list[stream_id]['api_key'],
                  "price": str(price),
                  "quantity": str(quantity),
                  "side": side.upper(),
                  "symbol": symbol.upper(),
                  "timestamp": self._manager.get_timestamp()}

        if order_id is not None:
            params['orderId'] = order_id
        if orig_client_order_id is not None:
            params['origClientOrderId'] = orig_client_order_id
        if price_match is not None:
            params['priceMatch'] = price_match
        if recv_window is not None:
            params['recvWindow'] = str(recv_window)

        method = "order.modify"
        api_secret = self._manager.stream_list[stream_id]['api_secret']
        request_id = self._manager.get_new_uuid_id() if request_id is None else request_id
        params['signature'] = self._manager.generate_signature(api_secret=api_secret, data=params)

        payload = {"id": request_id,
                   "method": method,
                   "params": params}

        if self._manager.send_with_stream(stream_id=stream_id, payload=payload) is False:
            self._manager.add_payload_to_stream(stream_id=stream_id, payload=payload)

        if process_response is not None:
            with self._manager.process_response_lock:
                entry = {'callback_function': process_response}
                self._manager.process_response[request_id] = entry

        if return_response is True:
            with self._manager.return_response_lock:
                entry = {'event_return_response': threading.Event()}
                self._manager.return_response[request_id] = entry
            self._manager.return_response[request_id]['event_return_response'].wait()
            with self._manager.return_response_lock:
                response_value = self._manager.return_response[request_id]['response_value']
                del self._manager.return_response[request_id]
            return response_value

        return True
