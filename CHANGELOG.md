# unicorn-binance-websocket-api Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## 1.1.8.dev (development stage)
### Todo
- dev_test_full.py invalid streams become zombies 

## 1.1.8
### Adding
- pypi_install_packaging_tools.sh
### Changing
- README.md
- Removed 2nd argument binance_websocket_api_manager.stream_is_stopping()
### Fixing
- tabs in print_summary() for windows platform
- fixing format errors from auto reformat in unicorn_binance_websocket_api_connection

## 1.1.7 failed build

## 1.1.6
### Fixing
- catching "ssl.SSLError" BinanceWebSocketApiConnection.receive()
- improvment of reconnect on invalid URI caused by no network issue and a missing listen_key from Binance

## 1.1.5
### Adding
- 30 min cache for Binance "listenKey" from rest api to avoid weight costs and hammering the Binance API on a 
flapping network connection
### Fixing
- Reconnect issue on userData stream
- Reset "has_stopped" attr from "stream_list" after a conncection restart
- Modyfied docstrings descriptions
- Tabs in print_summary() on windows
