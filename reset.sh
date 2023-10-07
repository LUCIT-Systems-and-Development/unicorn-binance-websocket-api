#!/usr/bin/env bash

rm *.py.log

rm build -r
rm dist -r
rm *.egg-info -r

rm unicorn_binance_websocket_api/*.c
rm unicorn_binance_websocket_api/*.html
rm unicorn_binance_websocket_api/*.dll
rm unicorn_binance_websocket_api/*.so

rm .print_summary.txt