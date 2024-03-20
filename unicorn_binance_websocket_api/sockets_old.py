#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/sockets_old.py
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

from __future__ import print_function
from unicorn_binance_websocket_api.connection_old import BinanceWebSocketApiConnection
from unicorn_fy.unicorn_fy import UnicornFy
import asyncio
import ujson as json
import logging
import uuid
import websockets

logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiSocket(object):
    def __init__(self, manager, stream_id, channels, markets):
        self.manager = manager
        self.stream_id = stream_id
        self.channels = channels
        self.markets = markets
        self.socket_id = uuid.uuid4()
        self.manager.stream_list[self.stream_id]['recent_socket_id'] = self.socket_id
        self.symbols = self.manager.stream_list[self.stream_id]['symbols']
        self.output = self.manager.stream_list[self.stream_id]['output']
        self.unicorn_fy = UnicornFy()
        self.exchange = manager.get_exchange()
        self.websocket = None

    async def __aenter__(self):
        logger.debug(f"Entering asynchronous with-context of BinanceWebSocketApiSocket() ...")
        if self.manager.is_stop_request(self.stream_id):
            self.manager.stream_is_stopping(self.stream_id)
            logger.error(f"Leaving BinanceWebSocketApiSocket() of {self.stream_id} in cause of the stop request!")
            return None
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Leaving asynchronous with-context of BinanceWebSocketApiSocket() ...")
        await self.close()

    async def close(self):
        try:
            await self.websocket.close()
        except AttributeError as error_msg:
            if "object has no attribute" not in str(error_msg):
                logger.debug(f"BinanceWebSocketApiSocket.start_socket() - error_msg: {error_msg}")

    async def start_socket(self):
        logger.info(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, {str(self.channels)}, "
                    f"{str(self.markets)}) socket_id={str(self.socket_id)} recent_socket_id={str(self.socket_id)}")
        try:
            async with BinanceWebSocketApiConnection(self.manager,
                                                     self.stream_id,
                                                     self.socket_id,
                                                     self.channels,
                                                     self.markets,
                                                     symbols=self.symbols) as self.websocket:
                if self.websocket is None:
                    self.manager.stream_is_stopping(self.stream_id)
                    # await self.close()
                    return False

                self.manager.socket_is_ready[self.stream_id] = True
                self.manager.process_stream_signals(signal_type="CONNECT", stream_id=self.stream_id)
                self.manager.stream_list[self.stream_id]['last_stream_signal'] = "CONNECT"
                while True:
                    if self.manager.is_stop_request(self.stream_id):
                        self.manager.stream_is_stopping(self.stream_id)
                        break
                        # await self.close()
                        # return False
                    elif self.manager.is_stop_as_crash_request(self.stream_id):
                        self.manager.stream_is_crashing(self.stream_id)
                        break
                        # await self.close()
                        # return False
                    try:
                        if self.manager.stream_list[self.stream_id]['recent_socket_id'] != self.socket_id:
                            logger.error(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                         f"{str(self.channels)}, {str(self.markets)} socket_id={str(self.socket_id)} "
                                         f"recent_socket_id={str(self.socket_id)} - Sending payload - exit because its "
                                         f"not the recent socket id! stream_id={str(self.stream_id)}, recent_socket_id="
                                         f"{str(self.manager.stream_list[self.stream_id]['recent_socket_id'])}")
                            break
                            # return False
                    except KeyError:
                        break
                        # return False
                    while self.manager.stream_list[self.stream_id]['payload']:
                        logger.info(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                    f"{str(self.channels)}, {str(self.markets)} socket_id={str(self.socket_id)} "
                                    f"recent_socket_id={str(self.socket_id)} - Sending payload started ...")
                        if self.manager.stream_list[self.stream_id]['recent_socket_id'] != self.socket_id:
                            logger.error(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                         f"{str(self.channels)}, {str(self.markets)} socket_id={str(self.socket_id)} "
                                         f"recent_socket_id={str(self.socket_id)} - Sending payload - exit because its "
                                         f"not the recent socket id! stream_id={str(self.stream_id)}, recent_socket_id="
                                         f"{str(self.manager.stream_list[self.stream_id]['recent_socket_id'])}")
                            break
                            # return False
                        payload = []
                        try:
                            payload = self.manager.stream_list[self.stream_id]['payload'].pop(0)
                        except IndexError as error_msg:
                            logger.debug(f"BinanceWebSocketApiSocket.start_socket() IndexError: {error_msg}")
                        logger.info(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                    f"{str(self.channels)}, {str(self.markets)} - Sending payload: {str(payload)}")
                        try:
                            await self.websocket.send(json.dumps(payload, ensure_ascii=False))
                        except AttributeError as error_msg:
                            logger.debug(f"BinanceWebSocketApiManager._create_stream_thread() "
                                         f"stream_id={str(self.stream_id)}  - AttributeError `error: 18` - "
                                         f"error_msg: {str(error_msg)}")
                        # To avoid a ban we respect the limits of binance:
                        # https://github.com/binance-exchange/binance-official-api-docs/blob/5fccfd572db2f530e25e302c02be5dec12759cf9/CHANGELOG.md#2020-04-23
                        # Limit: max 5 messages per second inclusive pings/pong
                        # Websocket API does not seem to have this restriction!
                        if self.manager.stream_list[self.stream_id]['api'] is False:
                            max_subscriptions_per_second = self.manager.max_send_messages_per_second - \
                                                           self.manager.max_send_messages_per_second_reserve
                            idle_time = 1/max_subscriptions_per_second
                            await asyncio.sleep(idle_time)
                    try:
                        try:
                            received_stream_data_json = await self.websocket.receive()
                        except asyncio.TimeoutError:
                            # Timeout from `asyncio.wait_for()` which we use to keep the loop running even if we don't
                            # receive new records via websocket.
                            logger.debug(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                         f"{str(self.channels)}, {str(self.markets)} - Received inner "
                                         f"asyncio.TimeoutError (This is no ERROR, its exactly what we want!)")
                            continue
                        if self.manager.is_stop_request(self.stream_id):
                            self.manager.stream_is_stopping(self.stream_id)
                            break
                            # return False
                        if received_stream_data_json is not None:
                            if self.output == "UnicornFy":
                                if self.manager.stream_list[self.stream_id]['api'] is False:
                                    if self.exchange == "binance.com":
                                        received_stream_data = self.unicorn_fy.binance_com_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-testnet":
                                        received_stream_data = self.unicorn_fy.binance_com_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-margin":
                                        received_stream_data = self.unicorn_fy.binance_com_margin_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-margin-testnet":
                                        received_stream_data = self.unicorn_fy.binance_com_margin_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-isolated_margin":
                                        received_stream_data = self.unicorn_fy.binance_com_isolated_margin_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-isolated_margin-testnet":
                                        received_stream_data = self.unicorn_fy.binance_com_isolated_margin_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-futures":
                                        received_stream_data = self.unicorn_fy.binance_com_futures_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-futures-testnet":
                                        received_stream_data = self.unicorn_fy.binance_com_futures_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.com-coin-futures" \
                                            or self.exchange == "binance.com-coin_futures":
                                        received_stream_data = self.unicorn_fy.binance_com_coin_futures_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.je":
                                        received_stream_data = self.unicorn_fy.binance_je_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.us":
                                        received_stream_data = self.unicorn_fy.binance_us_websocket(received_stream_data_json)
                                    elif self.exchange == "trbinance.com":
                                        received_stream_data = self.unicorn_fy.trbinance_com_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.org":
                                        received_stream_data = self.unicorn_fy.binance_org_websocket(received_stream_data_json)
                                    elif self.exchange == "binance.org-testnet":
                                        received_stream_data = self.unicorn_fy.binance_org_websocket(received_stream_data_json)
                                    else:
                                        received_stream_data = received_stream_data_json
                                else:
                                    # WS API does not need to get unicornfied, just turn it into a dict:
                                    received_stream_data = json.loads(received_stream_data_json)
                            elif self.output == "dict":
                                received_stream_data = json.loads(received_stream_data_json)
                            else:
                                received_stream_data = received_stream_data_json

                            if self.manager.stream_list[self.stream_id]['api'] is True:
                                return_response_by_request_id = None
                                with self.manager.return_response_lock:
                                    for request_id in self.manager.return_response:
                                        if request_id in received_stream_data_json:
                                            return_response_by_request_id = request_id
                                            break
                                if return_response_by_request_id is not None:
                                    self.manager.return_response[return_response_by_request_id]['response_value'] = received_stream_data
                                    self.manager.return_response[return_response_by_request_id]['event_return_response'].set()
                                    continue

                                process_by_request_id = None
                                with self.manager.process_response_lock:
                                    for request_id in self.manager.process_response:
                                        if request_id in received_stream_data_json:
                                            process_by_request_id = request_id
                                            break
                                if process_by_request_id is not None:
                                    self.manager.process_response[process_by_request_id]['callback_function'](received_stream_data)
                                    with self.manager.process_response_lock:
                                        del self.manager.process_response[process_by_request_id]
                                    continue

                            try:
                                stream_buffer_name = self.manager.stream_list[self.stream_id]['stream_buffer_name']
                            except KeyError:
                                stream_buffer_name = False
                            if stream_buffer_name is not False:
                                # if create_stream() got a stram_buffer_name -> use it
                                self.manager.add_to_stream_buffer(received_stream_data,
                                                                  stream_buffer_name=stream_buffer_name)
                            elif self.manager.specific_process_asyncio_queue[self.stream_id] is not None:
                                # if create_stream() got a asyncio consumer task for the asyncio queue -> use it
                                logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                             f"stream_id={self.stream_id} transferred to `asyncio_queue`!")
                                await self.manager.asyncio_queue[self.stream_id].put(received_stream_data)
                            elif self.manager.specific_process_stream_data[self.stream_id] is not None:
                                # if create_stream() got a callback function -> use it
                                logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                             f"stream_id={self.stream_id} transferred to `process_stream_data`!")
                                self.manager.specific_process_stream_data[self.stream_id](received_stream_data)
                            elif self.manager.specific_process_stream_data_async[self.stream_id] is not None:
                                # if create_stream() got an asynchronous callback function -> use it
                                logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                             f"stream_id={self.stream_id} transferred to "
                                             f"`process_stream_data_async`!")
                                await self.manager.specific_process_stream_data_async[self.stream_id](received_stream_data)
                            else:
                                if self.manager.process_asyncio_queue is not None:
                                    # if global asyncio consumer task for the asyncio queue -> use it
                                    logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                                 f"stream_id={self.stream_id} transferred to `asyncio_queue`!")
                                    await self.manager.asyncio_queue[self.stream_id].put(received_stream_data)
                                elif self.manager.process_stream_data is not None:
                                    # if global callback function -> use it
                                    logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                                 f"stream_id={self.stream_id} transferred to `process_stream_data`!")
                                    self.manager.process_stream_data(received_stream_data)
                                elif self.manager.process_stream_data_async is not None:
                                    # if global async callback function -> use it
                                    logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                                 f"stream_id={self.stream_id} transferred to "
                                                 f"`process_stream_data_async`!")
                                    await self.manager.process_stream_data_async(received_stream_data)
                                else:
                                    # If nothing else is used, write to global stream_buffer
                                    logger.debug(f"BinanceWebSocketApiSocket.start_socket() - Received data set from "
                                                 f"stream_id={self.stream_id} transferred to `stream_buffer`!")
                                    self.manager.add_to_stream_buffer(received_stream_data)

                            if "error" in received_stream_data_json:
                                logger.error("BinanceWebSocketApiSocket.start_socket(" +
                                             str(self.stream_id) + ") "
                                             "- Received error message: " + str(received_stream_data_json))
                                self.manager.add_to_ringbuffer_error(received_stream_data_json)
                            elif "result" in received_stream_data_json:
                                logger.debug("BinanceWebSocketApiSocket.start_socket(" +
                                             str(self.stream_id) + ") "
                                             "- Received result message: " + str(received_stream_data_json))
                                self.manager.add_to_ringbuffer_result(received_stream_data_json)
                            else:
                                if self.manager.stream_list[self.stream_id]['last_received_data_record'] is None:
                                    self.manager.process_stream_signals(signal_type="FIRST_RECEIVED_DATA",
                                                                        stream_id=self.stream_id,
                                                                        data_record=received_stream_data)
                                    self.manager.stream_list[self.stream_id]['last_stream_signal'] = "FIRST_RECEIVED_DATA"
                                self.manager.stream_list[self.stream_id]['last_received_data_record'] = received_stream_data
                    except websockets.ConnectionClosed as error_msg:
                        logger.critical(f"BinanceWebSocketApiSocket.start_socket({self.stream_id}, {self.channels}, "
                                        f"{self.markets}) - Exception ConnectionClosed - error_msg: {error_msg}")
                        if "WebSocket connection is closed: code = 1008" in str(error_msg):
                            # await self.close()
                            self.manager.stream_is_crashing(self.stream_id, error_msg)
                            self.manager.set_restart_request(self.stream_id)
                            break
                            # return False
                        elif "WebSocket connection is closed: code = 1006" in str(error_msg):
                            self.manager.stream_is_crashing(self.stream_id, error_msg)
                            self.manager.set_restart_request(self.stream_id)
                            break
                            # return False
                        self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                        self.manager.set_restart_request(self.stream_id)
                        break
                        #return False
                    except AttributeError as error_msg:
                        logger.error(f"BinanceWebSocketApiSocket.start_socket({self.stream_id}, {self.channels}, "
                                     f"{self.markets}) - Exception AttributeError - error_msg: {error_msg}")
                        self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                        self.manager.set_restart_request(self.stream_id)
                        break
                        # await self.close()
                        # return False
        except asyncio.TimeoutError as error_msg:
            # Catching https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/221
            self.manager.stream_is_crashing(self.stream_id, error_msg)
            self.manager.set_restart_request(self.stream_id)
            # return False
        except KeyError as error_msg:
            logger.debug(f"BinanceWebSocketApiSocket.start_socket() KeyError: {error_msg}")
            # return False
        finally:
            try:
                if self.manager.stream_list[self.stream_id]['last_stream_signal'] == "FIRST_RECEIVED_DATA" \
                        or self.manager.stream_list[self.stream_id]['last_stream_signal'] == "CONNECT":
                    self.manager.process_stream_signals(signal_type="DISCONNECT", stream_id=self.stream_id)
                    self.manager.stream_list[self.stream_id]['last_stream_signal'] = "DISCONNECT"
            except KeyError:
                pass
            await self.close()