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
# Copyright (c) 2019-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from Cython.Build import cythonize
from setuptools import setup
import os
import shutil
import subprocess

source_dir = "unicorn_binance_websocket_api"
stubs_dir = "stubs"


def generate_stubs():
    print("Generating stub files ...")
    target_dir = os.path.join(stubs_dir)
    os.makedirs(target_dir, exist_ok=True)
    for filename in os.listdir(source_dir):
        if filename.endswith('.py'):
            source_path = os.path.join(source_dir, filename)
            stub_output_dir = os.path.join(stubs_dir, source_dir)
            os.makedirs(stub_output_dir, exist_ok=True)
            subprocess.run(['stubgen', '-o', stub_output_dir, source_path], check=True)
            for stub_file in os.listdir(stub_output_dir):
                if stub_file.endswith('.pyi'):
                    source_stub_path = os.path.join(stub_output_dir, stub_file)
                    shutil.move(source_stub_path, source_dir)
    print("Stub files generated and moved successfully.")


with open("README.md", "r") as fh:
    long_description = fh.read()

generate_stubs()

setup(
    ext_modules=cythonize(
        [f'{source_dir}/__init__.py',
         f'{source_dir}/api.py',
         f'{source_dir}/connection.py',
         f'{source_dir}/connection_settings.py',
         f'{source_dir}/exceptions.py',
         f'{source_dir}/manager.py',
         f'{source_dir}/restclient.py',
         f'{source_dir}/restserver.py',
         f'{source_dir}/sockets.py',
         f'{source_dir}/licensing_exceptions.py',
         f'{source_dir}/licensing_manager.py'],
        annotate=False),
    name='unicorn-binance-websocket-api',
    version="2.6.0",
    author="LUCIT Systems and Development",
    author_email='info@lucit.tech',
    url="https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api",
    description="A Python SDK by LUCIT to use the Binance Websocket API`s (com+testnet, "
                "com-margin+testnet, com-isolated_margin+testnet, com-futures+testnet, com-coin_futures, us, tr, "
                "dex/chain+testnet) in a easy, fast, flexible, robust and fully-featured way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LSOSL - LUCIT Synergetic Open Source License',
    install_requires=['colorama', 'requests', 'websocket-client', 'websockets==11.0.3', 'flask_restful',
                      'cheroot', 'flask', 'lucit-licensing-python', 'ujson', 'psutil', 'PySocks', 'unicorn-fy',
                      'unicorn-binance-rest-api', 'typing_extensions', 'Cython'],
    keywords='binance, asyncio, async, asynchronous, concurrent, websocket-api, webstream-api, '
             'binance-websocket, binance-webstream, webstream, websocket, api, binance-dex, '
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
    package_data={'': ['*.so', '*.dll', '*.py', '*.pyi']},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Cython",
        "License :: Other/Proprietary License",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
)
