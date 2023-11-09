#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# File: pypi/create_wheel.sh
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-binance-websocket-api.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://unicorn-binance-websocket-api.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/main/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

security-check() {
    echo -n "Did you change the version in \`build_wheels.yml\`, \`CHANGELOG.md\`, \`sphinx/source/conf.py\`, \`setup.py\` and \`/manager.py\`? [yes|NO] "
    local SURE
    read SURE
    if [ "$SURE" != "yes" ]; then
        exit 1
    fi
    echo "https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/build_wheels.yml"
    echo "Refresh conda-forge recipe!"
}

compile-check() {
    echo -n "Compile local? [yes|NO] "
    local SURE
    read SURE
    if [ "$SURE" != "yes" ]; then
        exit 1
    fi
    echo "ok, lets go ..."
    python3 setup.py bdist_wheel sdist
}

security-check
compile-check
