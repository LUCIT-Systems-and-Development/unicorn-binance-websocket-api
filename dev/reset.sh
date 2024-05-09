#!/usr/bin/bash

rm *.log
rm dev/*.log

rm build -r
rm dist -r
rm *.egg-info -r
rm stubs -r
rm out -r

rm unicorn_binance_websocket_api/*.c
rm unicorn_binance_websocket_api/*.html
rm unicorn_binance_websocket_api/*.dll
rm unicorn_binance_websocket_api/*.so
rm unicorn_binance_websocket_api/*.pyi

rm .print_summary.txt