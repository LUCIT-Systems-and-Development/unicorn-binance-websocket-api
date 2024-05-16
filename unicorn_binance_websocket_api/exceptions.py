#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_websocket_api/exception.py
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

class MaximumSubscriptionsExceeded(Exception):
    """
    Exception if the maximum number of subscriptions per stream has been exceeded!
    """
    def __init__(self, exchange: str = None, max_subscriptions_per_stream: int = None):
        self.message = (f"The maximum number of {max_subscriptions_per_stream} subscriptions per stream for exchange "
                        f"'{exchange}' has been exceeded! For detailed information please have a look at our wiki: "
                        f"https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/Binance-"
                        f"websocket-endpoint-configuration-overview")
        super().__init__(self.message)


class Socks5ProxyConnectionError(Exception):
    """
    Exception if the manager class is not able to establish a connection to the socks5 proxy.
    """
    pass


class StreamIsCrashing(Exception):
    """
    Exception if the stream is crashing.
    """
    def __init__(self, stream_id=None, reason=None):
        self.message = f"Stream with stream_id={stream_id} is crashing! Reason: {reason}"
        super().__init__(self.message)


class StreamIsRestarting(Exception):
    """
    Exception if the stream is restarting.
    """
    def __init__(self, stream_id=None, reason=None):
        self.message = f"Stream with stream_id={stream_id} is restarting! Reason: {reason}"
        super().__init__(self.message)


class StreamIsStopping(Exception):
    """
    Exception if the stream is stopping.
    """
    def __init__(self, stream_id=None, reason=None):
        self.message = f"Stream with stream_id={stream_id} is stopping! Reason: {reason}"
        super().__init__(self.message)


class UnknownExchange(Exception):
    """
    Exception if the manager class is started with an unknown exchange.
    """

    def __init__(self, error_msg=None):
        super().__init__(error_msg)