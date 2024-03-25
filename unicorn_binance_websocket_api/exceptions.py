#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

# define Python user-defined exceptions
class Socks5ProxyConnectionError(Exception):
    """
    Exception if the manager class is not able to establish a connection to the socks5 proxy.
    """
    pass


class UnknownExchange(Exception):
    """
    Exception if the manager class is started with an unknown exchange.
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
