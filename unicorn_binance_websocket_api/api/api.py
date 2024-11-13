#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_websocket_api/api/api.py
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

from unicorn_binance_websocket_api.api.futures import BinanceWebSocketApiApiFutures
from unicorn_binance_websocket_api.api.spot import BinanceWebSocketApiApiSpot

class WsApi():
    def __init__(self, manager):
        self.futures: BinanceWebSocketApiApiFutures = BinanceWebSocketApiApiFutures(manager=manager)
        self.spot: BinanceWebSocketApiApiSpot = BinanceWebSocketApiApiSpot(manager=manager)
