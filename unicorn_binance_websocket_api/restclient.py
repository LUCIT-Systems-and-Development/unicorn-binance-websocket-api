#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/restclient.py
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

from unicorn_binance_rest_api import BinanceRestApiManager
from typing import Optional, Union, Tuple
import logging
import requests
import threading
import time

logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiRestclient(object):
    def __init__(self,
                 debug: Optional[bool] = False,
                 disable_colorama: Optional[bool] = False,
                 exchange: Optional[str] = "binance.com",
                 lucit_api_secret: Optional[str] = None,
                 lucit_license_ini: str = None,
                 lucit_license_profile: Optional[str] = None,
                 lucit_license_token: Optional[str] = None,
                 restful_base_uri: Optional[str] = None,
                 show_secrets_in_logs: Optional[bool] = False,
                 socks5_proxy_server: Optional[str] = None,
                 socks5_proxy_user: Optional[str] = None,
                 socks5_proxy_pass: Optional[str] = None,
                 socks5_proxy_ssl_verification: Optional[bool] = True,
                 stream_list: dict = None,
                 ubra: BinanceRestApiManager = None,
                 warn_on_update: Optional[bool] = True):
        """
        Create a restclient instance!

        """
        self.threading_lock = threading.Lock()
        self.debug = debug
        self.disable_colorama = disable_colorama
        self.exchange = exchange
        self.lucit_api_secret: Optional[str] = lucit_api_secret
        self.lucit_license_ini = lucit_license_ini
        self.lucit_license_profile = lucit_license_profile
        self.lucit_license_token = lucit_license_token
        self.restful_base_uri = restful_base_uri
        self.show_secrets_in_logs = show_secrets_in_logs
        self.socks5_proxy_server = socks5_proxy_server
        self.socks5_proxy_user = socks5_proxy_user
        self.socks5_proxy_pass = socks5_proxy_pass
        self.socks5_proxy_ssl_verification = socks5_proxy_ssl_verification
        self.stream_list = stream_list
        self.ubra = ubra
        self.warn_on_update = warn_on_update
        self.sigterm = False

    def _init_ubra(self) -> bool:
        """
        Init UBRA if necessary.

        """
        if self.ubra is None:
            logger.debug(f"Init UBRA for UBWA restclient.")
            self.ubra = BinanceRestApiManager(debug=self.debug,
                                              disable_colorama=self.disable_colorama,
                                              exchange=self.exchange,
                                              lucit_api_secret=self.lucit_api_secret,
                                              lucit_license_ini=self.lucit_license_ini,
                                              lucit_license_profile=self.lucit_license_profile,
                                              lucit_license_token=self.lucit_license_token,
                                              socks5_proxy_server=self.socks5_proxy_server,
                                              socks5_proxy_user=self.socks5_proxy_user,
                                              socks5_proxy_pass=self.socks5_proxy_pass,
                                              warn_on_update=self.warn_on_update)
        return True

    def delete_listen_key(self, stream_id=None) -> Tuple[Union[str, None], Union[dict, None]]:
        """
        Delete a specific listen key

        :param stream_id: provide a stream_id
        :type stream_id: str

        :return: listen_key, binance_api_status
        :rtype: Tuple[Union[str, None], Union[dict, None]]
        """
        logger.info(f"BinanceWebSocketApiRestclient.delete_listen_key() stream_id='{str(stream_id)}')")

        if stream_id is None:
            return None, None

        try:
            with (self.threading_lock):
                self._init_ubra()

                try:
                    kwargs = {'api_key': self.stream_list[stream_id]['api_key'],
                              'api_secret': self.stream_list[stream_id]['api_secret']}
                except TypeError:
                    logger.critical(f"delete_listen_key(stream_id='{str(stream_id)}') - No API key available!")
                    return None, None

                if self.exchange == "binance.com-margin" or \
                        self.exchange == "binance.com-margin-testnet":
                    if self.restful_base_uri is not None:
                        self.ubra.MARGIN_API_URL = self.restful_base_uri
                    result = self.ubra.margin_stream_close(listenKey=self.stream_list[stream_id]['listen_key'],
                                                           throw_exception=False,
                                                           **kwargs)
                elif self.exchange == "binance.com-isolated_margin" or \
                        self.exchange == "binance.com-isolated_margin-testnet":
                    if self.restful_base_uri is not None:
                        self.ubra.MARGIN_API_URL = self.restful_base_uri
                    result = self.ubra.isolated_margin_stream_close(symbol=self.stream_list[stream_id]['symbols'],
                                                                    listenKey=self.stream_list[stream_id]['listen_key'],
                                                                    throw_exception=False,
                                                                    **kwargs)
                elif self.exchange == "binance.com-futures" or self.exchange == "binance.com-futures-testnet":
                    if self.restful_base_uri is not None:
                        self.ubra.FUTURES_URL = self.restful_base_uri
                    result = self.ubra.futures_stream_close(listenKey=self.stream_list[stream_id]['listen_key'],
                                                            throw_exception=False,
                                                            **kwargs)
                elif self.exchange == "binance.com-coin_futures":
                    if self.restful_base_uri is not None:
                        self.ubra.FUTURES_COIN_URL = self.restful_base_uri
                    result = self.ubra.futures_coin_stream_close(listenKey=self.stream_list[stream_id]['listen_key'],
                                                                 throw_exception=False,
                                                                 **kwargs)
                else:
                    if self.restful_base_uri is not None:
                        self.ubra.API_URL = self.restful_base_uri
                    result = self.ubra.stream_close(listenKey=self.stream_list[stream_id]['listen_key'],
                                                    throw_exception=False,
                                                    **kwargs)
        except requests.exceptions.ReadTimeout as error_msg:
            logger.debug(f"BinanceWebSocketApiManager.delete_listen_key_by_stream_id() - Not able to delete "
                         f"listen_key - requests.exceptions.ReadTimeout: {error_msg}")

        self.stream_list[stream_id]['listen_key'] = None

        return result, self.get_binance_api_status()

    def get_binance_api_status(self) -> dict:
        """
        Get the used weight of the last api request, with a current timestamp.

        :return: binance_api_status
        :rtype: dict
        """
        binance_api_status = self.ubra.get_used_weight()
        weight = binance_api_status['weight']
        binance_api_status['weight'] = 0 if weight is None else weight
        binance_api_status['timestamp'] = time.time()
        return binance_api_status

    def get_listen_key(self, stream_id=None) -> Tuple[Union[str, None], Union[dict, None]]:
        """
        Request a valid listen_key from binance

        :param stream_id: provide a stream_id
        :type stream_id: str

        :return: listen_key, binance_api_status
        :rtype: Tuple[Union[str, None], Union[dict, None]]
        """
        logger.info(f"BinanceWebSocketApiRestclient.get_listen_key() symbol='{self.stream_list[stream_id]['symbols']}' "
                    f"stream_id='{str(stream_id)}')")

        if stream_id is None:
            return None, None

        with (self.threading_lock):
            self._init_ubra()

            try:
                kwargs = {'api_key': self.stream_list[stream_id]['api_key'],
                          'api_secret': self.stream_list[stream_id]['api_secret']}
            except TypeError as error_msg:
                logger.debug(f"delete_listen_key(stream_id='{str(stream_id)}') - TypeError: {error_msg}")
                return None, None

            if self.exchange == "binance.com-margin" or self.exchange == "binance.com-margin-testnet":
                try:
                    if self.restful_base_uri is not None:
                        self.ubra.MARGIN_API_URL = self.restful_base_uri
                    response = self.ubra.margin_stream_get_listen_key(output="raw_data",
                                                                      throw_exception=False,
                                                                      **kwargs)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for margin!")
                    return None, None
            elif self.exchange == "binance.com-isolated_margin" or \
                    self.exchange == "binance.com-isolated_margin-testnet":
                if self.stream_list[stream_id]['symbols'] is None:
                    logger.critical("BinanceWebSocketApiRestclient.get_listen_key() - error_msg: Parameter "
                                    "`symbol` is missing!")
                    return None, None
                else:
                    try:
                        if self.restful_base_uri is not None:
                            self.ubra.MARGIN_API_URL = self.restful_base_uri
                        symbols = self.stream_list[stream_id]['symbols']
                        response = self.ubra.isolated_margin_stream_get_listen_key(symbol=symbols,
                                                                                   output="raw_data",
                                                                                   throw_exception=False,
                                                                                   **kwargs)
                    except AttributeError as error_msg:
                        logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                        f"error_msg: {error_msg} - Can not acquire listen_key for isolated_margin!")
                        return None, None
            elif self.exchange == "binance.com-futures" or self.exchange == "binance.com-futures-testnet":
                try:
                    if self.restful_base_uri is not None:
                        self.ubra.FUTURES_URL = self.restful_base_uri
                    response = self.ubra.futures_stream_get_listen_key(output="raw_data",
                                                                       throw_exception=False,
                                                                       **kwargs)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for futures!!")
                    return None, None
            elif self.exchange == "binance.com-coin_futures":
                try:
                    if self.restful_base_uri is not None:
                        self.ubra.FUTURES_COIN_URL = self.restful_base_uri
                    response = self.ubra.futures_coin_stream_get_listen_key(output="raw_data",
                                                                            throw_exception=False,
                                                                            **kwargs)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for coin futures!!")
                    return None, None
            else:
                try:
                    if self.restful_base_uri is not None:
                        self.ubra.API_URL = self.restful_base_uri
                    response = self.ubra.stream_get_listen_key(output="raw_data",
                                                               throw_exception=False,
                                                               **kwargs)
                except AttributeError as error_msg:
                    logger.critical(f"BinanceWebSocketApiRestclient.get_listen_key() - error: 8 - "
                                    f"error_msg: {error_msg} - Can not acquire listen_key for exchange='"
                                    f"{self.exchange}'!")
                    return None, None

            try:
                self.stream_list[stream_id]['listen_key'] = response['listenKey']
                self.stream_list[stream_id]['last_static_ping_listen_key'] = time.time()
                return response, self.get_binance_api_status()
            except KeyError:
                return response, self.get_binance_api_status()
            except TypeError:
                return None, None

    def keepalive_listen_key(self, stream_id=None) -> Tuple[Union[str, None], Union[dict, None]]:
        """
        Ping a listenkey to keep it alive

        :param stream_id: provide a stream_id
        :type stream_id: str

        :return: listen_key, binance_api_status
        :rtype: Tuple[Union[str, None], Union[dict, None]]
        """
        logger.info(f"BinanceWebSocketApiRestclient.keepalive_listen_key() "
                    f"symbol='{self.stream_list[stream_id]['symbols']}' stream_id='{str(stream_id)}')")

        if stream_id is None:
            return None, None

        with (self.threading_lock):
            self._init_ubra()

            try:
                kwargs = {'api_key': self.stream_list[stream_id]['api_key'],
                          'api_secret': self.stream_list[stream_id]['api_secret']}
            except TypeError as error_msg:
                logger.debug(f"delete_listen_key(stream_id='{str(stream_id)}') - TypeError: {error_msg}")
                return None, None

            if self.exchange == "binance.com-margin" or \
                    self.exchange == "binance.com-margin-testnet":
                if self.restful_base_uri is not None:
                    self.ubra.MARGIN_API_URL = self.restful_base_uri
                result = self.ubra.margin_stream_keepalive(listenKey=self.stream_list[stream_id]['listen_key'],
                                                           throw_exception=False,
                                                           **kwargs)
            elif self.exchange == "binance.com-isolated_margin" or \
                    self.exchange == "binance.com-isolated_margin-testnet":
                if self.restful_base_uri is not None:
                    self.ubra.MARGIN_API_URL = self.restful_base_uri
                result = self.ubra.isolated_margin_stream_keepalive(symbol=self.stream_list[stream_id]['symbols'],
                                                                    listenKey=self.stream_list[stream_id]['listen_key'],
                                                                    throw_exception=False,
                                                                    **kwargs)
            elif self.exchange == "binance.com-futures" or self.exchange == "binance.com-futures-testnet":
                if self.restful_base_uri is not None:
                    self.ubra.FUTURES_URL = self.restful_base_uri
                result = self.ubra.futures_stream_keepalive(listenKey=self.stream_list[stream_id]['listen_key'],
                                                            throw_exception=False,
                                                            **kwargs)
            elif self.exchange == "binance.com-coin_futures":
                if self.restful_base_uri is not None:
                    self.ubra.FUTURES_URL = self.restful_base_uri
                result = self.ubra.futures_stream_keepalive(listenKey=self.stream_list[stream_id]['listen_key'],
                                                            throw_exception=False,
                                                            **kwargs)
            else:
                if self.restful_base_uri is not None:
                    self.ubra.API_URL = self.restful_base_uri
                result = self.ubra.stream_keepalive(listenKey=self.stream_list[stream_id]['listen_key'],
                                                    throw_exception=False,
                                                    **kwargs)

            self.stream_list[stream_id]['last_static_ping_listen_key'] = time.time()

            return result, self.get_binance_api_status()

    def stop(self) -> bool:
        """
        Stop this instance!r

        :rtype: bool
        """
        logger.debug(f"Stopping instance of `BinanceWebSocketApiRestclient()` ...")
        self.sigterm = True
        if self.ubra is not None:
            self.ubra.stop_manager()
        return True
