#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: lucit_licensing_python/licensing_manager.py
#
# Project website: https://www.lucit.tech/lucit-licensing-python.html
# Github: https://github.com/LUCIT-Systems-and-Development/lucit-licensing-python
# Documentation: https://lucit-licensing-python.docs.lucit.tech
# PyPI: https://pypi.org/project/lucit-licensing-python
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/lucit-licensing-python/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2023-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

import cython
import hashlib
import hmac
import logging
import os
import platform
import requests
import threading
import time
import uuid
from configparser import ConfigParser, ExtendedInterpolation
from copy import deepcopy
from operator import itemgetter
from pathlib import Path
from requests.exceptions import ConnectionError, RequestException, HTTPError
from simplejson.errors import JSONDecodeError
from typing import Optional, Callable
try:
    from licensing_exceptions import NoValidatedLucitLicense
except ModuleNotFoundError:
    from unicorn_binance_websocket_api.licensing_exceptions import NoValidatedLucitLicense

logger = logging.getLogger("lucit_licensing_python")


class LucitLicensingManager(threading.Thread):
    def __init__(self,
                 api_secret: Optional[str] = None,
                 license_token: Optional[str] = None,
                 license_ini: Optional[str] = None,
                 license_profile: Optional[str] = None,
                 program_used: Optional[str] = None,
                 start: bool = True,
                 parent_shutdown_function: Callable[[bool], bool] = None,
                 needed_license_type: Optional[str] = None):
        super().__init__()
        self.module_version: str = "1.8.2_mbdt"
        self.parent_shutdown_function = parent_shutdown_function
        self.is_started = start
        self.sigterm = False
        self.id = str(uuid.uuid4())
        self.last_verified_licensing_result = None
        self.mac = str(hex(uuid.getnode()))
        self.needed_license_type = needed_license_type
        self.os = platform.system()
        self.program_used = program_used
        self.python_version = platform.python_version()
        self.raised_license_exception = None
        self.request_interval = 20
        self.time_delta = 0.0
        self.url: str = "https://private.api.lucit.services/licensing/v1/"
        if self.needed_license_type == "UNICORN-BINANCE-SUITE":
            self.shop_product_url = "https://shop.lucit.services/software/unicorn-binance-suite"
        else:
            self.shop_product_url = "https://shop.lucit.services/software"
        license_ini_search: bool = False
        if license_ini is None:
            license_ini = "lucit_license.ini"
        else:
            license_ini_search = True
        if license_profile is None:
            license_profile = "LUCIT"

        if api_secret is not None or license_token is not None:
            logger.debug(f"Loading LUCIT license from parameters.")
            self.api_secret = api_secret
            self.license_token = license_token
        elif os.path.isfile(f"{license_ini}"):
            logger.info(f"Loading license file `{license_ini}`")
            config = ConfigParser(interpolation=ExtendedInterpolation())
            config.read(license_ini)
            try:
                self.api_secret = config[license_profile]['api_secret']
                self.license_token = config[license_profile]['license_token']
                logger.info(f"Loading profile `{license_profile}`")
            except KeyError:
                info = f"Unknown license profile: {license_profile}"
                self.process_licensing_error(info)
        elif os.path.isfile(f"{Path.home()}/.lucit/{license_ini}"):
            logger.info(f"Loading license file `{Path.home()}/.lucit/{license_ini}`")
            config = ConfigParser(interpolation=ExtendedInterpolation())
            config.read(f"{Path.home()}/.lucit/{license_ini}")
            try:
                self.api_secret = config[license_profile]['api_secret']
                self.license_token = config[license_profile]['license_token']
                logger.info(f"Loading profile `{license_profile}`")
            except KeyError:
                info = f"Unknown license profile: {license_profile}"
                self.process_licensing_error(info)
        elif license_ini_search is True:
            info = f"License file not found: {license_ini}"
            self.process_licensing_error(info)
        else:
            logger.debug(f"Loading LUCIT license from environment: '{license_profile}_API_SECRET' and "
                         f"'{license_profile}_LICENSE_TOKEN'")
            try:
                self.api_secret = os.environ[f'{license_profile}_API_SECRET']
                self.license_token = os.environ[f'{license_profile}_LICENSE_TOKEN']
                logger.debug(f"Loaded LUCIT license from environment: '{license_profile}_API_SECRET' and "
                             f"'{license_profile}_LICENSE_TOKEN'")
            except KeyError:
                logger.debug(f'Can not load environment variables {license_profile}_API_SECRET and '
                             f'{license_profile}_LICENSE_TOKEN')
                self.api_secret = None
                self.license_token = None
        if self.sigterm is False:
            logger.info(f"New instance of lucit-licensing-python_{self.module_version}-python_"
                        f"{str(platform.python_version())}-{'compiled' if cython.compiled else 'source'} on "
                        f"{str(platform.system())} {str(platform.release())} started ...")
        if start is True and self.sigterm is False:
            self.start()
        while self.last_verified_licensing_result is None and self.sigterm is False and start is True:
            # Block the main process till a valid license is available
            time.sleep(0.1)
        licensing_exception = self.get_license_exception()
        if licensing_exception is not None:
            raise NoValidatedLucitLicense(licensing_exception)
        if self.sigterm is True:
            logger.warning(f"LUCIT License Manager is shutting down!")
        else:
            logger.debug(f"LUCIT License Manager is ready!")

    def __enter__(self):
        logger.debug(f"Entering with-context of LucitLicensingManager() ...")
        return self

    def __exit__(self, exc_type, exc_value, error_traceback):
        logger.debug(f"Leaving with-context of LucitLicensingManager() ...")
        if self.is_started:
            self.stop()
        if exc_type is not None:
            logger.critical(f"An exception occurred: {exc_type} - {exc_value} - {error_traceback}")

    def __generate_signature(self, api_secret: str = None, data: dict = None) -> str:
        if api_secret is None or data is None:
            logger.error(f"The parameters 'api_secret' and 'data' must not be None! ")
            return ""
        ordered_data = self.__order_params(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        hmac_string = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return str(hmac_string.hexdigest())

    @staticmethod
    def __order_params(data: dict = None) -> list:
        has_signature: bool = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, value))
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def __private_request(self, api_secret: str = None, license_token: str = None,
                          key_value: str = None, endpoint: str = None) -> dict:
        api_secret = api_secret if api_secret is not None else self.api_secret
        license_token = license_token if license_token is not None else self.license_token
        if api_secret is None or license_token is None:
            info = f"Please provide the api secret and license token of your lucit license! Read this article for " \
                   f"more information: https://medium.lucit.tech/87b0088124a8"
            self.process_licensing_error(info)
            return {"error": f"License Not Found - {info}"}
        params = {
            "license_token": license_token,
            "id": self.id,
            "mac": self.mac,
            "os": self.os,
            "program_used": self.program_used,
            "python_version": self.python_version,
            "timestamp": time.time()+self.time_delta,
        }
        if key_value is not None:
            params['key_value'] = key_value
        params["signature"] = self.__generate_signature(api_secret=api_secret, data=params)
        response = None
        try:
            response = requests.get(self.url+endpoint, params=params)
            response.raise_for_status()
        except (ConnectionError, RequestException, HTTPError):
            try:
                if response is None:
                    return {"error": f"Connection Error - Connection could not be established."}
                else:
                    if response.status_code == 404 or response.status_code == 500 or response.status_code == 503:
                        return {"error": f"Connection Error - Connection could not be established."}
                    else:
                        try:
                            return {"error": f"{response.status_code} {response.json()['detail']}"}
                        except KeyError:
                            return {"error": f"Connection Error - Connection could not be established."}
            except (UnboundLocalError, JSONDecodeError) as error_msg:
                if "HTTPConnectionPool" in str(error_msg):
                    return {"error": f"Connection Error - Connection could not be established."}
                return {"error": f"{error_msg}"}
        result: dict = response.json()
        time_gap = time.time() + self.time_delta - float(result['timestamp'])
        if time_gap > 30 or time_gap < -30:
            return {"error": "Server timestamp in signed response is out of valid range."}
        try:
            if self.__verify_signature(api_secret=api_secret, params=result,
                                       signature=result["signature"]):
                return result
            else:
                return {"error": "Invalid Signature - The response is not signed correctly."}
        except KeyError:
            return {"error": "Missing Signature - The response is not signed."}

    def __public_request(self, endpoint: str = None) -> dict:
        response = None
        try:
            response = requests.get(self.url+endpoint)
            response.raise_for_status()
        except (ConnectionError, RequestException, HTTPError):
            try:
                if response is None:
                    return {"error": f"Connection Error - Connection could not be established."}
                else:
                    if response.status_code == 404 or response.status_code == 500 or response.status_code == 503:
                        return {"error": f"Connection Error - Connection could not be established."}
                    else:
                        try:
                            return {"error": f"{response.status_code} {response.json()['detail']}"}
                        except KeyError:
                            return {"error": f"Connection Error - Connection could not be established."}
            except (UnboundLocalError, JSONDecodeError) as error_msg:
                if "HTTPConnectionPool" in str(error_msg):
                    return {"error": f"Connection Error - Connection could not be established."}
                return {"error": f"{error_msg}"}
        result: dict = response.json()
        return result

    def __verify_signature(self, api_secret: str = None, params: dict = None, signature: str = None) -> bool:
        params_without_signature: dict = deepcopy(params)
        try:
            del params_without_signature['signature']
        except KeyError:
            logger.debug(f"params_without_signature['signature'] not deletable, it does not exist.")
        params_signature: str = self.__generate_signature(api_secret=api_secret, data=params_without_signature)
        if params_signature == signature:
            return True
        else:
            return False

    def close(self, close_api_session: bool = True, key_value: str = None) -> dict:
        logger.debug(f"Stopping LUCIT Licensing Manager ...")
        self.sigterm = True
        if close_api_session is True and self.last_verified_licensing_result is not None:
            response = self.__private_request(api_secret=None, license_token=None,
                                              key_value=key_value, endpoint="close")
        else:
            response = {"close": {"status": "NOT_EXECUTED"}}
        if self.parent_shutdown_function is not None:
            logger.debug(f"Triggering shutdown of parent instance ...")
            self.parent_shutdown_function(close_api_session=False)
            self.parent_shutdown_function = None
        return response

    def get_license_exception(self):
        return self.raised_license_exception

    def set_license_exception(self, error):
        self.raised_license_exception = error

    def get_info(self, api_secret: str = None, license_token: str = None) -> dict:
        return self.__private_request(api_secret=api_secret, license_token=license_token, endpoint="info")

    def get_module_version(self):
        return self.module_version

    def get_quotas(self, api_secret: str = None, license_token: str = None) -> dict:
        return self.__private_request(api_secret=api_secret, license_token=license_token, endpoint="quotas")

    def get_timestamp(self) -> dict:
        return self.__public_request(endpoint="timestamp")

    def get_version(self) -> dict:
        return self.__public_request(endpoint="version")

    def is_verified(self) -> bool:
        if self.last_verified_licensing_result is None:
            return False
        else:
            return True

    def process_licensing_error(self, info: str = None):
        logger.critical(info)
        self.set_license_exception(info)
        self.sigterm = True
        if self.is_started is True:
            self.parent_shutdown_function(close_api_session=False)

    def reset(self, api_secret: str = None, license_token: str = None) -> dict:
        return self.__private_request(api_secret=api_secret, license_token=license_token, endpoint="reset")

    def run(self):
        connection_errors = 0
        too_many_requests_errors = 0
        while self.sigterm is False:
            license_result = self.verify()
            if license_result.get('license') is not None:
                if license_result['license']['licensed_product'] != self.needed_license_type:
                    info = f"License not usable, its issued for product " \
                           f"'{license_result['license']['licensed_product']}'. Please contact our support: " \
                           f"https://www.lucit.tech/get-support.html"
                    self.process_licensing_error(info)
                    break
                else:
                    if license_result['license']['status'] == "VALID":
                        try:
                            self.last_verified_licensing_result = license_result
                            request_interval = int(license_result['license']['request_interval'])
                            if request_interval != self.request_interval:
                                logger.debug(f"Setting `request_interval` to {request_interval}")
                                self.request_interval = request_interval-1
                        except KeyError:
                            pass
                        logger.debug(f"LUCIT License validated for product: "
                                     f"{license_result['license']['licensed_product']}")
                    else:
                        info = f"Unsuccessful verification! License Status: {license_result['license']['status']}"
                        self.process_licensing_error(info)
                        break
            elif license_result.get('error') is not None:
                if "403 Forbidden" in license_result['error']:
                    if "Forbidden - Timestamp not valid" in license_result['error']:
                        logger.error(f"Timestamp not valid - Syncing time ...")
                        self.sync_time()
                    elif "403 Forbidden - Access forbidden due to misuse of test licenses." in license_result['error']:
                        info = f"Access forbidden due to misuse of test licenses. Please get a valid license from " \
                               f"the LUCIT Online Shop: {self.shop_product_url}"
                        logger.critical(info)
                        self.process_licensing_error(info)
                        break
                    elif "403 Forbidden - Insufficient access rights." in license_result['error']:
                        logger.critical(f"{license_result['error']}")
                        info = f"The license is invalid! Please get a valid license from the LUCIT Online " \
                               f"Shop: {self.shop_product_url}"
                        if self.last_verified_licensing_result is None:
                            self.process_licensing_error(info)
                        else:
                            self.process_licensing_error(info)
                        break
                    else:
                        logger.critical(f"Caught unknown license error: {license_result['error']}")
                        info = f"Unknown error! Please submit an issue on GitHub: https://github.com/LUCIT-Systems-" \
                               f"and-Development/lucit-licensing-python/issues/new?labels=bug&projects=&template=" \
                               f"bug_report.yml"
                        self.process_licensing_error(info)
                        break
                elif "429 Too Many Requests" in license_result['error']:
                    logger.critical(f"{license_result['error']}")
                    if self.last_verified_licensing_result is None:
                        # If there never was a successful verification, we stop immediately
                        info = f"Too many requests to the LUCIT Licensing API! Not able to verify the license!"
                        self.process_licensing_error(info)
                        break
                    else:
                        if connection_errors > 9:
                            # This stopps an already running instance if the API rate limit gets hit for more
                            # than 90 min
                            info = f"Too many requests to the LUCIT Licensing API! Not able to verify the license " \
                                   f"for more than 90 minutes!"
                            self.process_licensing_error(info)
                            break
                        too_many_requests_errors += 1

                        # 600 * 9 = 90 minutes
                        # API rate limits expire after 60 minutes, so running instances survive even if the user
                        # unintentionally exceeds the LUCIT API rate limits continuously for 30 minutes.
                        time.sleep(600)
                    continue
                elif "Connection Error - Connection could not be established" in license_result['error']:
                    logger.critical(f"{license_result['error']}")
                    if self.last_verified_licensing_result is None:
                        # If there never was a successful verification, we after 3 retries
                        if connection_errors > 3:
                            info = f"Connection to LUCIT Licensing API could not be established. Please try " \
                                   f"again later!"
                            self.process_licensing_error(info)
                            break
                    else:
                        # This stopps an already running instance if the Connection is down for more than 90 minutes
                        if connection_errors > 9:
                            info = f"Connection to LUCIT Licensing API could not be established. Please try " \
                                   f"again later!"
                            self.process_licensing_error(info)
                            break
                        connection_errors += 1
                        # 600 * 9 = 90 minutes
                        # Running instances survive even if the LUCIT API is not connectable for 90 minutes
                        time.sleep(600)
                    continue
                elif "License Not Found" in license_result['error']:
                    logger.warning(f"LUCIT License Manager is shutting down!")
                    break
                else:
                    logger.critical(f"Unknown error: {license_result['error']} - Please submit an issue on GitHub: "
                                    f"https://github.com/LUCIT-Systems-and-Development/lucit-licensing-python/issues/"
                                    f"new?labels=bug&projects=&template=bug_report.yml")
                    break
            else:
                logger.critical(f"Unknown error: {license_result} - Please submit an issue on GitHub: "
                                f"https://github.com/LUCIT-Systems-and-Development/lucit-licensing-python/issues/"
                                f"new?labels=bug&projects=&template=bug_report.yml")
                break
            connection_errors = 0
            too_many_requests_errors = 0
            for _ in range(self.request_interval * 60):
                if self.sigterm is False:
                    threading.Event().wait(1)
                else:
                    break

    def stop(self) -> dict:
        return self.close()

    def sync_time(self) -> bool:
        try:
            self.time_delta = float(self.get_timestamp()['timestamp']) - time.time()
            return True
        except KeyError:
            return False

    def test(self) -> dict:
        return self.__public_request(endpoint="test")

    def verify(self, api_secret: str = None, license_token: str = None, key_value: str = None) -> dict:
        return self.__private_request(api_secret=api_secret, license_token=license_token,
                                      key_value=key_value, endpoint="verify")
