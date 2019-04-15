![GitHub release](https://img.shields.io/github/release/unicorn-data-analysis/unicorn-binance-websocket-api.svg) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/unicorn-data-analysis/unicorn-binance-websocket-api.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unicorn-binance-websocket-api.svg) ![PyPI - yes](https://img.shields.io/badge/PyPI-yes-brightgreen.svg) ![PyPI - Status](https://img.shields.io/pypi/status/unicorn-binance-websocket-api.svg) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/unicorn-binance-websocket-api.svg) ![GitHub](https://img.shields.io/github/license/unicorn-data-analysis/unicorn-binance-websocket-api.svg) 

# UNICORN Binance WebSocket API
A python API to use the Binance Websocket API in a easy, fast, flexible, robust and fully-featured way.

The python module [UNICORN Binance WebSocket API](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api) 
provides an API to the [Binance Websocket API](https://github.com/binance-exchange/binance-official-api-docs), which 
supports the streaming of public streams like trade, kline, ticker and depth, but also the private userData stream which 
need to be used with a valid api_key and api_secret from the [Binance Exchange](https://www.binance.com/).

The module requires python 3.5.1 or above, as it depends on pythons latest asyncio features for asynchronous/concurrent 
processing. The current dependencies are listed 
[here](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/requirements.txt).

Be aware that the Binance websocket API just offers to receive data. If you would like to set orders, withdraws and so 
on, you have to use the Binance Rest API in combination. Great support for this offers the package 
[sammchardy/python-binance](https://github.com/sammchardy/python-binance).

"[sammchardy/python-binance](https://github.com/sammchardy/python-binance)" provides a websocket client too, so why use 
the UNICORN Binance WebSocket API?

- 100% auto-reconnect.
- Streams are processing asynchronous/concurrent (python asyncio) and each stream is started in a separate thread.
- No use of the twisted module, so you can use this lib in a daemonized application (compatible with 
[python-daemon](https://pypi.org/project/python-daemon/)).
- If you can not store your data on an offline local database, you can kick back the data to the stream_buffer which 
stores the receives in the RAM till you are able to process the data in the normal way again.
- Helpful management features.

## Installation
`pip install unicorn-binance-websocket-api`

https://pypi.org/project/unicorn-binance-websocket-api/

## Howto: 
https://www.unicorn-data.com/blog/article-details/howto-unicorn-binance-websocket-api.html

## Documentation: 
https://www.unicorn-data.com/unicorn-binance-websocket-api.html

## Project, code and downloads: 
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api

## Wiki
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/wiki

## How to report bugs or suggest improvements?
Please open a new issue:
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/issues

If you report a bug, try first the latest release via [download](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/releases) 
or with `pip install unicorn-binance-websocket-api --upgrade`. If the issue still exists, provide the error trace, OS 
and python version and explain how to reproduce the error. A demo script is appreciated.
