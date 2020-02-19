[![GitHub release](https://img.shields.io/github/release/oliver-zehentleitner/unicorn-binance-websocket-api.svg)](https://pypi.org/project/unicorn-binance-websocket-api/)
[![GitHub](https://img.shields.io/github/license/oliver-zehentleitner/unicorn-binance-websocket-api.svg?color=blue)](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unicorn-binance-websocket-api.svg)](https://www.python.org/downloads/)
[![PyPI - Status](https://img.shields.io/pypi/status/unicorn-binance-websocket-api.svg)](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/unicorn-binance-websocket-api.svg?label=PyPI%20wheel&color=orange)](https://pypi.org/project/unicorn-binance-websocket-api/)

# UNICORN Binance WebSocket API
A python API to use the Binance Websocket API's (com, com-margin, com-futures, jersey, us, dex/chain+testnet) in a easy, fast, flexible, robust and fully-featured way.

### [Create a multiplex websocket connection](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream) to Binance with just 3 lines of code:
```
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager

binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
binance_websocket_api_manager.create_stream(['trade', 'kline_1m'], ['btcusdt', 'bnbbtc', 'ethbtc'])
```
### And 4 more lines to print the receives:
```
while True:
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    if oldest_stream_data_from_stream_buffer:
        print(oldest_stream_data_from_stream_buffer)
```

Basically that's it, but there are more options:

### Convert received raw webstream data into well-formed python dictionaries with [UnicornFy](https://github.com/oliver-zehentleitner/unicorn_fy):
```
unicorn_fied_stream_data = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
```

### [Subscribe](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.subscribe_to_stream) / [Unsubscribe](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.unsubscribe_from_stream) new markets and channels:
```
markets = ['engbtc', 'zileth']
binance_websocket_api_manager.subscribe_to_stream(stream_id, markets=markets)

channels = ['kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'depth5']
binance_websocket_api_manager.unsubscribe_from_stream(stream_id, channels=channels)
```

[Discover even more possibilities!](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html)

## Description
The python module [UNICORN Binance WebSocket API](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api) 
provides an API to the Binance Websocket API`s of [Binance](https://github.com/binance-exchange/binance-official-api-docs), [Binance Margin](https://binance-docs.github.io/apidocs/spot/en/#user-data-streams),
[Binance Futures](https://binance-docs.github.io/apidocs/futures/en/#websocket-market-streams), 
[Binance Jersey](https://github.com/binance-jersey/binance-official-api-docs/), 
[Binance US](https://github.com/binance-us/binance-official-api-docs), 
[Binance DEX](https://docs.binance.org/api-reference/dex-api/ws-connection.html) and 
[Binance DEX Testnet](https://docs.binance.org/api-reference/dex-api/ws-connection.html) and supports the streaming of 
all public streams like trade, kline, ticker, depth, !bookTicker and blockheight and also all private userData streams 
which needs to be used with a valid api_key and api_secret from the Binance Exchange 
[www.binance.com](https://www.binance.com/userCenter/createApi.html), 
[www.binance.je](https://www.binance.je/userCenter/createApi.html)  or 
[www.binance.us](https://www.binance.us/userCenter/createApi.html) - for the DEX you need a user address from 
[www.binance.org](https://www.binance.org/en/create) or [testnet.binance.org](https://testnet.binance.org/en/create) 
and you can [get funds](https://www.binance.vision/tutorials/binance-dex-funding-your-testnet-account) for the testnet.

The module requires python 3.5.3 or above, as it depends on pythons latest asyncio features for asynchronous/concurrent 
processing. The current dependencies are listed 
[here](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/requirements.txt).

Be aware that the Binance websocket API just offers to receive data. If you would like to set orders, withdraws and so 
on, you have to use the Binance Rest API ([com](https://github.com/binance-exchange/binance-official-api-docs), 
[je](https://github.com/binance-jersey/binance-official-api-docs/), 
[us](https://github.com/binance-us/binance-official-api-docs/), 
[org](https://docs.binance.org/api-reference/dex-api/paths.html)) in combination. 

### What are the benefits of the UNICORN Binance WebSocket API?
- Fully managed websockets and 100% auto-reconnect!
- Supported exchanges: 
    * [Binance](https://www.binance.com) `BinanceWebSocketApiManager(exchange="binance.com")`
    * [Binance Margin](https://www.binance.com) `BinanceWebSocketApiManager(exchange="binance.com-margin")`
    * [Binance Futures](https://www.binance.com) `BinanceWebSocketApiManager(exchange="binance.com-futures")`
    * [Binance Jersey](https://www.binance.je) `BinanceWebSocketApiManager(exchange="binance.je")`
    * [Binance US](https://www.binance.us) `BinanceWebSocketApiManager(exchange="binance.us")`
    * [Binance DEX](https://www.binance.org) `BinanceWebSocketApiManager(exchange="binance.org")`
    * [Binance DEX testnet](https://testnet.binance.org) `BinanceWebSocketApiManager(exchange="binance.org-testnet")`

- Streams are processing asynchronous/concurrent (python asyncio) and each stream is started in a separate thread, but 
you dont need to deal with asyncio in your code!
- No use of the twisted module, so you can use this lib in a daemonized application (compatible with 
[python-daemon](https://pypi.org/project/python-daemon/)).
- Supports [subscribe](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.subscribe_to_stream)/[unsubscribe](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.unsubscribe_from_stream) on all exchanges!
- If you can not store your data in cause of a temporary technical issue, you can kick back the data to the 
stream_buffer which stores the receives in the RAM till you are able to process the data in the normal way again. 
[Learn more!](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/example_stream_buffer.py)
- Compatible with [UnicornFy](https://github.com/oliver-zehentleitner/unicorn_fy) to convert received raw data from
crypto API endpoints into well-formed python dictionaries. 
- Helpful management features like `get_binance_api_status()`, `get_stream_info()`, `get_stream_list()`, 
`get_stream_statistic()`, `get_stream_subscriptions()`, `replace_stream()`, `wait_till_stream_has_started()`, 
`get_current_receiving_speed()`, `subscribe_to_stream()`, `unsubscribe_from_stream()` and many more, explore them 
[here](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html).
- [Monitoring API service](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service) 
and a [check_command](https://github.com/oliver-zehentleitner/check_unicorn_monitoring_api) 
for [ICINGA](https://exchange.icinga.com/bithon/check_unicorn_monitoring_api)/Nagios 
[![icinga2-demo](https://s3.gifyu.com/images/icinga2-unicorn_binance_websocket_api.png)](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service)
- Excessively tested on Linux, Mac and Windows

If you like the project, please [![star](https://s3.gifyu.com/images/stard237b3003af9f9a9.png)](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/stargazers) it on 
[GitHub](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api)!

## Installation and Upgrade
Please note: UnicornFy is not longer part of this package, visit 
[https://github.com/oliver-zehentleitner/unicorn_fy](https://github.com/oliver-zehentleitner/unicorn_fy) for
further information.
### A wheel of the latest release with PIP from [PyPI](https://pypi.org/project/unicorn-binance-websocket-api/)
`pip install unicorn-binance-websocket-api --upgrade`
### From source of the latest release with PIP from [Github](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api)
#### Linux, macOS, ...
Run in bash:

`pip install https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/archive/$(curl -s https://api.github.com/repos/oliver-zehentleitner/unicorn-binance-websocket-api/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")').tar.gz --upgrade`
#### Windows
Use the below command with the version (such as 1.10.1) you determined 
[here](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/releases/latest):

`pip install https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/archive/1.3.8.tar.gz --upgrade`
### From the latest source (dev-stage) with PIP from [Github](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api)
This is not a release version and can not be considered to be stable!

`pip install https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/tarball/master --upgrade`

### [Conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), [Virtualenv](https://virtualenv.pypa.io/en/latest/) or plain [python](https://docs.python.org/2/install/)
Download the [latest release](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/releases/latest) 
or the [current master branch](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/archive/master.zip)
 and use:
- ./environment.yml
- ./requirements.txt
- ./setup.py

## Demo
[Demo source](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/dev_test_cex_full_non_stop.py)

[![demo_gif](https://s3.gifyu.com/images/unicorn-binance-websocket-api_demo_1.6.1.gif)](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/dev_test_full_non_stop.py)

## Howto
- [Howto: UNICORN Binance WebSocket API](https://www.technopathy.club/2019/11/02/howto-unicorn-binance-websocket-api/)
- [Howto: Monitoring UNICORN Binance WebSocket API Manager with ICINGA2](https://www.technopathy.club/2019/11/02/howto-monitoring-unicorn-binance-websocket-api-manager-with-icinga2/)

## Documentation
- [General](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api)
- [Modules](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html)

## Source, Downloads, Examples, ...
[https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api)

## Change Log
[https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/CHANGELOG.md](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/CHANGELOG.md)

## Wiki
[https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki)

## Receive Notifications
To receive notifications on available updates you can 
[![watch](https://s3.gifyu.com/images/github_watch.png)](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/watchers) 
the repository on [GitHub](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api), write your 
[own script](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/example_version_of_this_package.py) 
with using `binance_websocket_api_manager.is_update_availabe()` or you use the 
[monitoring API service](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service).

To receive news (like inspection windows/maintenance) about the Binance API`s subscribe to their telegram groups: 
- [https://t.me/binance_api_announcements](https://t.me/binance_api_announcements)
- [https://t.me/binance_api_english](https://t.me/binance_api_english)
- [https://t.me/BinanceExchange](https://t.me/BinanceExchange)
- [https://t.me/Binance_Jersey](https://t.me/Binance_Jersey)
- [https://t.me/Binance_USA](https://t.me/Binance_USA)
- [https://t.me/BinanceDEXchange](https://t.me/BinanceDEXchange)

## How to report Bugs or suggest Improvements?
[List of planned features](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) - 
click ![thumbs-up](https://s3.gifyu.com/images/tu.png) if you need one of them or suggest a new feature!

Before you report a bug, [try the latest release](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api#installation-and-upgrade). If the issue still exists, provide the error trace, OS 
and python version and explain how to reproduce the error. A demo script is appreciated.

If you dont find an issue related to your topic, please open a new [issue](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues)!

[Report a security bug!](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/security/policy)

## Contributing
[UNICORN Binance WebSocket API](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api) is an open 
source project which welcomes contributions which can be anything from simple documentation fixes to new features. To 
contribute follow 
[this guide](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/CONTRIBUTING.md).
 
We ![love](https://s3.gifyu.com/images/heartae002231c41d8a80.png) open source!
