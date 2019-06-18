![GitHub release](https://img.shields.io/github/release/unicorn-data-analysis/unicorn-binance-websocket-api.svg) 
![GitHub](https://img.shields.io/github/license/unicorn-data-analysis/unicorn-binance-websocket-api.svg?color=blue) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unicorn-binance-websocket-api.svg) 
![code coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg) 
![PyPI - Status](https://img.shields.io/pypi/status/unicorn-binance-websocket-api.svg) 
![PyPI - Wheel](https://img.shields.io/pypi/wheel/unicorn-binance-websocket-api.svg?label=PyPI%20wheel&color=orange) 
![PyPI - Downloads](https://img.shields.io/pypi/dm/unicorn-binance-websocket-api.svg?label=PyPI%20downloads&color=orange)


# UNICORN Binance WebSocket API
A python API to use the Binance Websocket API in a easy, fast, flexible, robust and fully-featured way.

### Create a multiplex websocket connection to Binance with just 3 lines of code:
```
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager

binance_websocket_api_manager = BinanceWebSocketApiManager()
binance_websocket_api_manager.create_stream(['trade', 'kline_1m'], ['btcusdt', 'bnbbtc', 'ethbtc'])
```

## Description
The python module [UNICORN Binance WebSocket API](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api) 
provides an API to the [Binance Websocket API](https://github.com/binance-exchange/binance-official-api-docs), which 
supports the streaming of public streams like trade, kline, ticker and depth, but also the private userData stream which 
need to be used with a valid api_key and api_secret from the [Binance Exchange](https://www.binance.com/).

The module requires python 3.5.3 or above, as it depends on pythons latest asyncio features for asynchronous/concurrent 
processing. The current dependencies are listed 
[here](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/requirements.txt).

Be aware that the Binance websocket API just offers to receive data. If you would like to set orders, withdraws and so 
on, you have to use the [Binance Rest API](https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md) 
in combination. 

### What are the benefits of the UNICORN Binance WebSocket API?
- 100% auto-reconnect!
- Supported exchanges: [Binance](https://www.binance.com) and [Binance Jersey](https://www.binance.je/)
- Streams are processing asynchronous/concurrent (python asyncio) and each stream is started in a separate thread.
- No use of the twisted module, so you can use this lib in a daemonized application (compatible with 
[python-daemon](https://pypi.org/project/python-daemon/)).
- If you can not store your data in cause of a temporary technical issue, you can kick back the data to the 
stream_buffer which stores the receives in the RAM till you are able to process the data in the normal way again.
- Helpful management features like `get_binance_api_status()`, `get_stream_info()`, `get_stream_list()`, 
`get_stream_statistic()`, `is_websocket_uri_length_valid()`, `replace_stream()`, `wait_till_stream_has_started()` and 
many more, explore them [here](https://www.unicorn-data.com/unicorn-binance-websocket-api.html#binance_websocket_api_docu).
- [Monitoring API service](https://www.unicorn-data.com/blog/article-details/howto-monitoring-unicorn-binance-websocket-api-manager-with-icinga2.html) 
and a [check_command](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/tools/icinga/) 
for [ICINGA](https://exchange.icinga.com/bithon/check_binance_websocket_api_manager)/Nagios 
![icinga2-demo](https://s3.gifyu.com/images/icinga2-unicorn_binance_websocket_api.png)

## Installation and Upgrade
Please note: UnicornFy is not longer part of this package, visit https://github.com/unicorn-data-analysis/unicorn_fy for
further information.
### A wheel of the latest release with PIP from [PyPI](https://pypi.org/project/unicorn-binance-websocket-api/)
`pip install unicorn-binance-websocket-api --upgrade`
### From source of the latest release with PIP from [Github](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api)
#### Linux, macOS, ...
Run in bash:

`pip install https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/archive/$(curl -s https://api.github.com/repos/unicorn-data-analysis/unicorn-binance-websocket-api/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")').tar.gz --upgrade`
#### Windows
Use the below command with the version (such as 1.3.8) you determined [here](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/releases/latest):

`pip install https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/archive/1.3.8.tar.gz --upgrade`
### From the latest source (dev-stage) with PIP from [Github](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api)
`pip install https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/tarball/master --upgrade`

### [Conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), [Virtualenv](https://virtualenv.pypa.io/en/latest/) or plain [python](https://docs.python.org/2/install/)
Download the [latest release](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/releases/latest) 
or the [current master branch](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/archive/master.zip)
 and use:
- ./environment.yml
- ./requirements.txt
- ./setup.py

## Demo
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/dev_test_full_non_stop.py

![demo_gif](https://s3.gifyu.com/images/unicorn_binance_websocket_api_demo.gif)

## Howto: 
https://www.unicorn-data.com/blog/article-details/howto-unicorn-binance-websocket-api.html

## Documentation: 
https://www.unicorn-data.com/unicorn-binance-websocket-api.html

## Project, Code and Downloads: 
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api

## Wiki
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/wiki

## How to report Bugs or suggest Improvements?
First try the latest release via [download](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/releases/latest) 
or with `pip install unicorn-binance-websocket-api --upgrade`. If the issue still exists, provide the error trace, OS 
and python version and explain how to reproduce the error. A demo script is appreciated.

Please open a new issue:
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/issues

## Contributing
UNICORN Binance WebSocket API is an open source project which welcomes contributions which can be anything from simple 
documentation fixes to new features. To contribute, fork the project on 
[GitHub](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api) and send a pull request.

We ![love](https://s3.gifyu.com/images/heartae002231c41d8a80.png) open source!
