#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: setup.py
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
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from setuptools import setup
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    ext_modules=cythonize(
        ['unicorn_binance_websocket_api/__init__.py',
         'unicorn_binance_websocket_api/api.py',
         'unicorn_binance_websocket_api/connection.py',
         'unicorn_binance_websocket_api/connection_settings.py',
         'unicorn_binance_websocket_api/exceptions.py',
         'unicorn_binance_websocket_api/manager.py',
         'unicorn_binance_websocket_api/restclient.py',
         'unicorn_binance_websocket_api/restserver.py',
         'unicorn_binance_websocket_api/sockets.py'],
        annotate=False),
    name='unicorn-binance-websocket-api',
    version="2.1.2",
    author="LUCIT Systems and Development",
    author_email='info@lucit.tech',
    url="https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api",
    description="An unofficial Python API to use the Binance Websocket API`s (com+testnet, com-margin+testnet, "
                "com-isolated_margin+testnet, com-futures+testnet, jersey, us, dex/chain+testnet) in a easy, fast"
                ", flexible, robust and fully-featured way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LSOSL - LUCIT Synergetic Open Source License',
    install_requires=['colorama', 'requests', 'websocket-client', 'websockets==10.4', 'flask_restful',
                      'cheroot', 'flask', 'lucit-licensing-python>=1.8.1', 'ujson', 'psutil', 'PySocks', 'unicorn-fy',
                      'unicorn-binance-rest-api>=2.1.2', 'typing_extensions', 'Cython'],
    keywords='binance, asyncio, async, asynchronous, concurrent, websocket-api, webstream-api, '
             'binance-websocket, binance-webstream, webstream, websocket, api, binance-jersey, binance-dex, '
            'binance-futures, binance-margin, binance-us',
    project_urls={
        'Howto': 'https://www.lucit.tech/unicorn-binance-websocket-api.html#howto',
        'Documentation': 'https://unicorn-binance-websocket-api.docs.lucit.tech',
        'Wiki': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki',
        'Author': 'https://www.lucit.tech',
        'Changes': 'https://unicorn-binance-websocket-api.docs.lucit.tech/changelog.html',
        'License': 'https://unicorn-binance-websocket-api.docs.lucit.tech/license.html',
        'Issue Tracker': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues',
        'Chat': 'https://gitter.im/unicorn-binance-suite/unicorn-binance-websocket-api',
        'Telegram': 'https://t.me/unicorndevs',
        'Get Support': 'https://www.lucit.tech/get-support.html',
        'LUCIT Online Shop': 'https://shop.lucit.services/software',
    },
    python_requires='>=3.7.0',
    package_data={'': ['unicorn_binance_websocket_api/*.so',
                       'unicorn_binance_websocket_api/*.dll']},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
        'Intended Audience :: Developers',
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Framework :: AsyncIO",
    ],
)
