#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/restserver.py
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

from flask_restful import Resource
import logging

logger = logging.getLogger("unicorn_binance_websocket_api")


class BinanceWebSocketApiRestServer(Resource):
    """
    Provide a REST API server 
    
    Description:
    https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service

    :param handler_binance_websocket_api_manager: Provide the handler of the binance_websocket_api_manager
    :type handler_binance_websocket_api_manager: function
    :param warn_on_update: set to 'False' to avoid a warning on available updates
    :type warn_on_update: bool
    """
    def __init__(self, handler_binance_websocket_api_manager, warn_on_update=True):
        self.manager = handler_binance_websocket_api_manager
        self.warn_on_update = warn_on_update

    def get(self, statusformat, checkcommandversion=False):
        """
        Get the status of the 'UNICORN Binance WebSocket API Manager'

        :param statusformat: Choose the format for the export (e.g. 'icinga')
        :type statusformat: str

        :param checkcommandversion: Control if there is a new version of the check_command available!
        :type checkcommandversion: bool

        :return: status message of 'UNICORN Binance WebSocket API Manager'
        :rtype: list (status string, http status code)
        """
        if statusformat == "icinga":
            logger.info(f"BinanceWebSocketApiRestServer.get({statusformat}, {str(checkcommandversion)}) - 200")
            return self.manager.get_monitoring_status_icinga(check_command_version=checkcommandversion,
                                                             warn_on_update=self.warn_on_update), 200
        else:
            logger.error(f"BinanceWebSocketApiRestServer.get({statusformat}, {str(checkcommandversion)}) - Service not"
                          f"found!")
            return "service not found", 404
