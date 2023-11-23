[![Get a UNICORN Binance Suite License](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-suite/master/images/logo/LUCIT-UBS-License-Offer.png)](https://shop.lucit.services)

[![Github](https://img.shields.io/badge/source-github-cbc2c8)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api)
[![GitHub Release](https://img.shields.io/github/release/LUCIT-Systems-and-Development/unicorn-binance-websocket-api.svg?label=github)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/releases)
[![GitHub Downloads](https://img.shields.io/github/downloads/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/total?color=blue)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/releases)
[![Anaconda Release](https://anaconda.org/lucit/unicorn-binance-websocket-api/badges/version.svg)](https://anaconda.org/lucit/unicorn-binance-websocket-api)
[![Anaconda Downloads](https://anaconda.org/lucit/unicorn-binance-websocket-api/badges/downloads.svg)](https://anaconda.org/lucit/unicorn-binance-websocket-api)
[![PyPi Release](https://img.shields.io/pypi/v/unicorn-binance-websocket-api?color=blue)](https://pypi.org/project/unicorn-binance-websocket-api/)
[![PyPi Downloads](https://pepy.tech/badge/unicorn-binance-websocket-api)](https://pepy.tech/project/unicorn-binance-websocket-api)
[![License](https://img.shields.io/badge/license-LSOSL-blue)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/LICENSE)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/unicorn_binance_websocket_api.svg)](https://www.python.org/downloads/)
[![PyPI - Status](https://img.shields.io/pypi/status/unicorn_binance_websocket_api.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues)
[![codecov](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/branch/master/graph/badge.svg?token=5I03AZ3F5S)](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-websocket-api)
[![CodeQL](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/codeql-analysis.yml)
[![Unit Tests](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/unit-tests.yml)
[![Build and Publish GH+PyPi](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/build_wheels.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/build_wheels.yml)
[![Build and Publish Anaconda](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/build_conda.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/build_conda.yml)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://unicorn-binance-websocket-api.docs.lucit.tech)
[![Read How To`s](https://img.shields.io/badge/read-%20howto-yellow)](https://medium.lucit.tech)
[![Telegram](https://img.shields.io/badge/chat-telegram-41ab8c)](https://t.me/unicorndevs)
[![Gitter](https://badges.gitter.im/unicorn-binance-suite/unicorn-binance-websocket-api.svg)](https://gitter.im/unicorn-binance-suite/unicorn-binance-websocket-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![LUCIT-UBWA-Banner](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/master/images/logo/LUCIT-UBWA-Banner-Readme.png)](https://www.lucit.tech/unicorn-binance-websocket-api.html)

# UNICORN Binance WebSocket API

[Description](#description) | [Live Demo](#live-demo) | [Installation](#installation-and-upgrade) | [How To](#howto) |
[Documentation](#documentation) | [Examples](#examples) | [Change Log](#change-log) | [Wiki](#wiki) | [Social](#social) |
[Notifications](#receive-notifications) | [Bugs](#how-to-report-bugs-or-suggest-improvements) | 
[Contributing](#contributing) | [Disclaimer](#disclaimer) | [Commercial Support](#commercial-support)

An unofficial Python API to use the Binance Websocket API`s (com+testnet, com-margin+testnet, 
com-isolated_margin+testnet, com-futures+testnet, com-coin_futures, us, tr, dex/chain+testnet) 
in a easy, fast, flexible, robust and fully-featured way. 

Part of '[UNICORN Binance Suite](https://www.lucit.tech/unicorn-binance-suite.html)'.

## Get a UNICORN Binance Suite License

To run modules of the *UNICORN Binance Suite* you need a [valid license](https://medium.lucit.tech/how-to-obtain-and-use-a-unicorn-binance-suite-license-key-and-run-the-ubs-module-according-to-best-87b0088124a8#4ca4)!

## Receive Data from Binance WebSockets

### [Create a multiplex websocket connection](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream) to Binance with a [`stream_buffer`](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_buffer%60) with just 3 lines of code:

```
import unicorn_binance_websocket_api

ubwa = BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(channels=['trade', 'kline_1m'], markets=['btcusdt', 'bnbbtc', 'ethbtc'])
```

### And 4 more lines to print the receives:
```
while True:
    oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
    if oldest_data_from_stream_buffer:
        print(oldest_data_from_stream_buffer)
```

### Or with a [callback function](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=process_stream_data#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.create_stream) just do:
```
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager


def process_new_receives(stream_data):
    print(str(stream_data))


ubwa = BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(channels=['trade', 'kline_1m'], 
                   markets=['btcusdt', 'bnbbtc', 'ethbtc'], 
                   process_stream_data=process_new_receives)
```

Basically that's it, but there are more options.

### Convert received raw webstream data into well-formed Python dictionaries with [UnicornFy](https://www.lucit.tech/unicorn-fy.html):
```
unicorn_fied_stream_data = UnicornFy.binance_com_websocket(oldest_data_from_stream_buffer)
```

or

```
ubwa.create_stream(['trade'], ['btcusdt'], output="UnicornFy")
```

### [Subscribe](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.subscribe_to_stream) / [unsubscribe](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.unsubscribe_from_stream) new markets and channels:
```
markets = ['engbtc', 'zileth']
channels = ['kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h', 'depth5']

ubwa.subscribe_to_stream(stream_id=stream_id, channels=channels, markets=markets)

ubwa.unsubscribe_from_stream(stream_id=stream_id, markets=markets)

ubwa.unsubscribe_from_stream(stream_id=stream_id, channels=channels)
```

## Send Requests to Binance WebSocket API
### [Place orders](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.api.BinanceWebSocketApiApi.create_order), [cancel orders](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.api.BinanceWebSocketApiApi.cancel_order) or [send other requests](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#module-unicorn_binance_websocket_api.api) via WebSocket:
```
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager


def process_api_responses(stream_data):
    print(str(stream_data))


api_key = "YOUR_BINANCE_API_KEY"
api_secret = "YOUR_BINANCE_API_SECRET"


ubwa = BinanceWebSocketApiManager(exchange="binance.com")
api_stream = ubwa.create_stream(api=True, 
                                api_key=api_key, 
                                api_secret=api_secret,
                                process_stream_data=process_api_responses)
                                
orig_client_order_id = ubwa.api.create_order(order_type="LIMIT", 
                                             price=1.1, 
                                             quantity=15.0, 
                                             side="SELL", 
                                             symbol="BUSDUSDT")
ubwa.api.cancel_order(orig_client_order_id=orig_client_order_id, symbol="BUSDUSDT")                                             
```

[Here](https://medium.lucit.tech/create-and-cancel-orders-via-websocket-on-binance-7f828831404) you can find a complete 
guide on 
[how to process requests via the Binance WebSocket API](https://medium.lucit.tech/create-and-cancel-orders-via-websocket-on-binance-7f828831404)!

## Stop `ubwa` after usage to avoid memory leaks

```
ubwa.stop_manager()
```

[Discover even more possibilities](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html)
or [use this script](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_everything.py) 
to stream everything from "binance.com".

This should be known by everyone using this lib: 

- [Best practice solutions for a maximum stable connection](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/Best-practice-solutions-for-a-maximum-stable-connection!)
- [Do you want consistent data from binance?](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/discussions/254)

## Description
The Python package [UNICORN Binance WebSocket API](https://www.lucit.tech/unicorn-binance-websocket-api.html) 
provides an API to the Binance Websocket API`s of 
[Binance](https://github.com/binance-exchange/binance-official-api-docs) 
([+Testnet](https://testnet.binance.vision/)), 
[Binance Margin](https://binance-docs.github.io/apidocs/spot/en/#user-data-streams) 
([+Testnet](https://testnet.binance.vision/)), 
[Binance Isolated Margin](https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin)
([+Testnet](https://testnet.binance.vision/)), 
[Binance Futures](https://binance-docs.github.io/apidocs/futures/en/#websocket-market-streams) 
([+Testnet](https://testnet.binancefuture.com)), 
[Binance COIN-M Futures](https://binance-docs.github.io/apidocs/delivery/en/#change-log),
[Binance US](https://github.com/binance-us/binance-official-api-docs), 
[Binance TR](https://www.trbinance.com/apidocs), 
[Binance DEX](https://docs.binance.org/api-reference/dex-api/ws-connection.html) and 
[Binance DEX Testnet](https://docs.binance.org/api-reference/dex-api/ws-connection.html) and supports sending requests 
to the [Binance Websocket API](https://developers.binance.com/docs/binance-trading-api/websocket_api) and the streaming 
of all public streams like trade, kline, ticker, depth, bookTicker, forceOrder, compositeIndex, blockheight etc. and 
also all private userData streams which needs to be used with a valid 
[api_key and api_secret](https://medium.lucit.tech/how-to-create-a-binance-api-key-and-api-secret-3bb5f47e360d)
from the Binance Exchange [www.binance.com](https://www.binance.com/), 
[testnet.binance.vision](https://testnet.binance.vision/) or 
[www.binance.us](https://www.binance.us) - for the DEX you need a user address from 
[www.binance.org](https://www.binance.org/en/create) or [testnet.binance.org](https://testnet.binance.org/en/create) 
and you can [get funds](https://www.binance.vision/tutorials/binance-dex-funding-your-testnet-account) for the testnet.

Use the [UNICORN Binance REST API](https://www.lucit.tech/unicorn-binance-rest-api.html) in combination. 

### What are the benefits of the UNICORN Binance WebSocket API?
- Fully managed websockets and 100% auto-reconnect! Also handles maintenance windows!

- Support for [Binance Websocket API](https://developers.binance.com/docs/binance-trading-api/websocket_api), send 
  requests like [create_order](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.ws_api.BinanceWebSocketApiWsApi.create_order),
  [cancel_open_orders](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.ws_api.BinanceWebSocketApiWsApi.cancel_open_orders)
  and [many more](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#module-unicorn_binance_websocket_api.ws_api) directly over websocket!

- [Supported exchanges](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/Binance-websocket-endpoint-configuration-overview): 

| Exchange                                                           | Exchange string                       | WS API                                                                                                                               |
|--------------------------------------------------------------------|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| [Binance](https://www.binance.com)                                 | `binance.com`                         | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/ok-icon.png) |
| [Binance Testnet](https://testnet.binance.vision/)                 | `binance.com-testnet`                 | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/ok-icon.png) |
| [Binance Margin](https://www.binance.com)                          | `binance.com-margin`                  | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |                                                                                                                                     
| [Binance Margin Testnet](https://testnet.binance.vision/)          | `binance.com-margin-testnet`          | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance Isolated Margin](https://www.binance.com)                 | `binance.com-isolated_margin`         | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance Isolated Margin Testnet](https://testnet.binance.vision/) | `binance.com-isolated_margin-testnet` | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance USD-M Futures](https://www.binance.com)                   | `binance.com-futures`                 | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance USD-M Futures Testnet](https://testnet.binancefuture.com) | `binance.com-futures-testnet`         | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance Coin-M Futures](https://www.binance.com)                  | `binance.com-coin_futures`            | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance US](https://www.binance.us)                               | `binance.us`                          | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance TR](https://www.trbinance.com)                            | `trbinance.com`                       | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance DEX](https://www.binance.org)                             | `binance.org`                         | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |
| [Binance DEX Testnet](https://testnet.binance.org)                 | `binance.org-testnet`                 | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/x-icon.png)   |

- Streams are processing asynchronous/concurrent (Python asyncio) and each stream is started in a separate thread, so 
you don't need to deal with asyncio in your code!

- Supports 
[subscribe](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.subscribe_to_stream)/[unsubscribe](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.unsubscribe_from_stream)
on all exchanges! (Take a look to the max supported subscriptions per stream in the [endpoint configuration overview](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/Binance-websocket-endpoint-configuration-overview)!)

- [UNICORN Binance WebSocket API](https://www.lucit.tech/unicorn-binance-websocket-api.html) respects Binance's API guidelines and protects you from avoidable reconnects and bans.

- Support for multiple private `!userData` streams with different `api_key` and `api_secret`. ([example_multiple_userdata_streams.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_multiple_userdata_streams.py))

- [Pick up the received data from the `stream_buffer`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=get_stream_info#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.pop_stream_data_from_stream_buffer) - 
if you can not store your data in cause of a temporary technical issue, you can 
[kick back the data to the `stream_buffer`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=get_stream_info#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.add_to_stream_buffer) 
which stores the receives in the RAM till you are able to process the data in the normal way again. 
[Learn more!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_buffer%60)

- Use separate `stream_buffers` for 
[specific streams](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_buffer_extended.py) 
or 
[users](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_multiple_userdata_streams.py)!

- Watch the `stream_signal_buffer` to receive `CONNECT`, `DISCONNECT` and `FIRST_RECEIVED_DATA` signals about the 
streams! [Learn more!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signal_buffer%60)

- Get the received data unchanged as received, as Python dictionary or converted with 
[UnicornFy](https://github.com/LUCIT-Systems-and-Development/unicorn-fy) into well-formed Python dictionaries. Use the `output`
parameter of 
[`create_stream()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=create_stream#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream) 
to control the output format.

- Helpful management features like 
[`get_binance_api_status()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_binance_api_status), 
[`get_current_receiving_speed()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_current_receiving_speed), 
[`get_errors_from_endpoints()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_errors_from_endpoints), 
[`get_limit_of_subscriptions_per_stream()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_limit_of_subscriptions_per_stream), 
[`get_request_id()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_request_id), 
[`get_result_by_request_id()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_result_by_request_id),
[`get_results_from_endpoints()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_results_from_endpoints), 
[`get_stream_buffer_length()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_buffer_length), 
[`get_stream_info()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_info), 
[`get_stream_list()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_list), 
[`get_stream_id_by_label()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_id_by_label), 
[`get_stream_statistic()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_statistic), 
[`get_stream_subscriptions()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_subscriptions), 
[`get_version()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_version), 
[`is_update_available()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.is_update_availabe), 
[`pop_stream_data_from_stream_buffer()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.pop_stream_data_from_stream_buffer), 
[`print_summary()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.print_summary), 
[`replace_stream()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.replace_stream), 
[`set_stream_label()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.set_stream_label), 
[`set_ringbuffer_error_max_size()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.set_ringbuffer_error_max_size), 
[`subscribe_to_stream()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.subscribe_to_stream), 
[`stop_stream()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.stop_stream),
[`stop_manager_with_all_streams()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.stop_manager_with_all_streams), 
[`unsubscribe_from_stream()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.unsubscribe_from_stream), 
[`wait_till_stream_has_started()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.wait_till_stream_has_started) 
and many more! Explore them [here](https://unicorn-binance-websocket-api.docs.lucit.tech/modules.html).

- Monitor the status of the created `BinanceWebSocketApiManager()` instance within your code with 
[`get_monitoring_status_plain()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=plain#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.get_monitoring_status_plain)
and specific streams with 
[`get_stream_info()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.get_stream_info).

- Nice to use with [iPython](https://ipython.org/): 
"IPython (Interactive Python) is a command shell for interactive computing that offers introspection, 
rich media, shell syntax, tab completion, and history." 
([example_interactive_mode.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_interactive_mode.py)) 
[![iPython](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/ipython.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_interactive_mode.py) 

- Also, nice to use with the [Jupyter Notebook](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/tree/master/ipynb) :)

- [Monitoring API service](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service) 
and a [check_command](https://exchange.icinga.com/LUCIT/check_lucit_collector) 
for [ICINGA](https://exchange.icinga.com/LUCIT/check_lucit_collector)/Nagios 
[![icinga2-demo](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/icinga.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service)

- Integration of [test cases](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/actions/workflows/unit-tests.yml) and [examples](#examples).

- Customizable base URL.

- *Socks5 Proxy* support:

  ```
  ubwa = BinanceWebSocketApiManager(exchange="binance.com", socks5_proxy_server="127.0.0.1:9050") 
  ```
  
  Read the [docs](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager)
  or this [how to](https://medium.com/@oliverzehentleitner/how-to-connect-to-binance-com-websockets-using-python-via-a-socks5-proxy-3c5a3e063f12) 
  for more information or try 
  [example_socks5_proxy.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_socks5_proxy.py).

- Excessively tested on Linux, Mac and Windows

If you like the project, please [![star](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/star.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/stargazers) it on 
[GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api)!

## Live Demo
This live demo script is streaming from [binance.com](https://www.binance.com) and runs on a *cx31* virtual 
machine of [HETZNER CLOUD](https://www.hetzner.com) - [get 20 EUR starting credit!](https://hetzner.cloud/?ref=rKgYRMq0l8fd)

[Open live monitor!](https://www.lucit.tech/unicorn-binance-websocket-api-live-demo.html)

[![live-demo](https://ubwa-demo.lucit.tech/ps.png)](https://www.lucit.tech/unicorn-binance-websocket-api-live-demo.html)

(Refresh update once a minute!)

## Installation and Upgrade
The module requires Python 3.7 or above, as it depends on Pythons latest asyncio features for asynchronous/concurrent 
processing. 

For the PyPy interpreter we offer packages only from Python version 3.9 and higher.

Anaconda packages are available from Python version 3.8 and higher.

The current dependencies are listed [here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/requirements.txt).

If you run into errors during the installation take a look [here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/Installation).


### A Cython binary, PyPy or source code based CPython wheel of the latest version with `pip` from [PyPI](https://pypi.org/project/unicorn-binance-rest-api/)
Our [Cython](https://cython.org/) and [PyPy](https://www.pypy.org/) Wheels are available on [PyPI](https://pypi.org/), 
these wheels offer significant advantages for Python developers:
- ***Performance Boost with Cython Wheels:*** 
  Cython is a programming language that supplements Python with static typing and C-level performance. By compiling 
  Python code into C, Cython Wheels can significantly enhance the execution speed of Python code, especially in 
  computationally intensive tasks. This means faster runtimes and more efficient processing for users of our package. 
- ***PyPy Wheels for Enhanced Efficiency:*** 
  PyPy is an alternative Python interpreter known for its speed and efficiency. It uses Just-In-Time (JIT) compilation, 
  which can dramatically improve the performance of Python code. Our PyPy Wheels are tailored for compatibility with 
  PyPy, allowing users to leverage this speed advantage seamlessly.

Both Cython and PyPy Wheels on PyPI make the installation process simpler and more straightforward. They ensure that 
you get the optimized version of our package with minimal setup, allowing you to focus on development rather than 
configuration.

#### Installation
`pip install unicorn-binance-websocket-api`

#### Update
`pip install unicorn-binance-websocket-api --upgrade`

### A Conda Package of the latest version with `conda` from [Anaconda](https://anaconda.org/lucit)
The `unicorn-binance-websocket-api` package is available with [Conda](https://docs.conda.io/en/latest/) through the 
[`lucit` channel](https://anaconda.org/lucit). 

For optimal compatibility and performance, it is recommended to source the necessary dependencies from the 
[`conda-forge` channel](https://anaconda.org/conda-forge). 

#### Installation
```
conda config --add channels conda-forge
conda config --add channels lucit
conda install -c lucit unicorn-binance-websocket-api
```

#### Update
`conda update -c lucit unicorn-binance-websocket-api`

### From source of the latest release with PIP from [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api)
#### Linux, macOS, ...
Run in bash:

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/archive/$(curl -s https://api.github.com/repos/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")').tar.gz --upgrade`

#### Windows
Use the below command with the version (such as 2.1.2) you determined 
[here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/releases/latest):

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/archive/2.1.2.tar.gz --upgrade`
### From the latest source (dev-stage) with PIP from [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api)
This is not a release version and can not be considered to be stable!

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/tarball/master --upgrade`

### [Conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), [Virtualenv](https://virtualenv.pypa.io/en/latest/) or plain [Python](https://www.python.org)
Download the [latest release](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/releases/latest) 
or the [current master branch](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/archive/master.zip)
 and use:

- ./environment.yml
- ./pyproject.toml
- ./requirements.txt
- ./setup.py

## Change Log
[https://unicorn-binance-websocket-api.docs.lucit.tech/changelog.html](https://unicorn-binance-websocket-api.docs.lucit.tech/changelog.html)

## Documentation
- [General](https://unicorn-binance-websocket-api.docs.lucit.tech)
- [Modules](https://unicorn-binance-websocket-api.docs.lucit.tech/modules.html)

## Examples
- [example_apache_kafka.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_apache_kafka.py)
- [example_binance_coin_futures.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_binance_coin_futures.py)
- [example_binance_dex.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_binance_dex.py)
- [example_binance_futures.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_binance_futures.py)
- [example_binance_futures_1s.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_binance_futures_1s.py)
- [example_binance_us.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_binance_us.py)
- [example_bookticker.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_bookticker.py)
- [example_ctrl-c.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_ctrl-c.py)
- [example_demo.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_demo.py)
- [example_easy_migration_from_python-binance.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_easy_migration_from_python-binance.py)
- [example_interactive_mode.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_interactive_mode.py)
- [example_kline_1m_with_unicorn_fy.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_kline_1m_with_unicorn_fy.py)
- [example_logging.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_logging.py)
- [example_monitoring.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_monitoring.py)
- [example_multi_stream.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_multi_stream.py)
- [example_multiple_userdata_streams.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_multiple_userdata_streams.py)
- [example_pandas_ta-lib.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_pandas_ta-lib.py)
- [example_plotting_last_price.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_plotting_last_price.py)
- [example_process_streams.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_process_streams.py)
- [example_socks5_proxy.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_socks5_proxy.py)
- [example_stream_buffer.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_buffer.py)
- [example_stream_buffer_extended.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_buffer_extended.py)
- [example_stream_buffer_fifo-lifo.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_buffer_fifo-lifo.py)
- [example_stream_everything.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_everything.py)
- [example_stream_management.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_management.py)
- [example_stream_management_extended.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_management_extended.py)
- [example_stream_signals.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_signals.py)
- [example_stream_signals_callback.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_stream_signals_callback.py)
- [example_subscribe.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_subscribe.py)
- [example_ticker_and_miniticker.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_ticker_and_miniticker.py)
- [example_trade_stream.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_trade_stream.py)
- [example_trbinance.com.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_trbinance_com.py)
- [example_userdata_stream.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_userdata_stream.py)
- [example_userdata_stream_new_style.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_userdata_stream_new_style.py)
- [example_version_of_this_package.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_version_of_this_package.py)
- [example_websocket_api.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_websocket_api.py)

## Howto
- [How to Obtain and Use a Unicorn Binance Suite License Key and Run the UBS Module According to Best Practice](https://medium.lucit.tech/how-to-obtain-and-use-a-unicorn-binance-suite-license-key-and-run-the-ubs-module-according-to-best-87b0088124a8)
- [Create and Cancel Orders via WebSocket on Binance](https://medium.lucit.tech/create-and-cancel-orders-via-websocket-on-binance-7f828831404)
- [How to Download Klines from Binance using Python?](https://medium.lucit.tech/how-to-download-data-from-binance-using-python-8f1b6e8f19f3)
- [Passing Binance Market Data to Apache Kafka in Python with aiokafka](https://medium.lucit.tech/passing-binance-market-data-to-apache-kafka-in-python-with-aiokafka-570541574655)
- [How to Connect to binance.com Websockets using Python via a Socks5 Proxy](https://medium.lucit.tech/how-to-connect-to-binance-com-websockets-using-python-via-a-socks5-proxy-3c5a3e063f12)

## Project Homepage
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api)

## Wiki
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki)

## Social
- [Discussions](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/discussions)
- [Gitter](https://gitter.im/unicorn-binance-suite/unicorn-binance-websocket-api)
- [https://t.me/unicorndevs](https://t.me/unicorndevs)
- [https://dev.binance.vision](https://dev.binance.vision)
- [https://community.binance.org](https://community.binance.org)

## Receive Notifications
To receive notifications on available updates you can 
[![watch](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/watch.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/watchers) 
the repository on [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api), write your 
[own script](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/example_version_of_this_package.py) 
with using 
[`is_update_available()`](https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.is_update_availabe) 
or you use the 
[monitoring API service](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/UNICORN-Monitoring-API-Service).

Follow us on [LinkedIn](https://www.linkedin.com/company/lucit-systems-and-development), 
[X](https://twitter.com/LUCIT_SysDev) or [Facebook](https://www.facebook.com/lucit.systems.and.development)!

To receive news (like inspection windows/maintenance) about the Binance API`s subscribe to their telegram groups: 

- [https://t.me/binance_api_announcements](https://t.me/binance_api_announcements)
- [https://t.me/binance_api_english](https://t.me/binance_api_english)
- [https://t.me/Binance_USA](https://t.me/Binance_USA)
- [https://t.me/TRBinanceTR](https://t.me/TRBinanceTR)
- [https://t.me/BinanceDEXchange](https://t.me/BinanceDEXchange)
- [https://t.me/BinanceExchange](https://t.me/BinanceExchange)

## How to report Bugs or suggest Improvements?
[List of planned features](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) - click ![thumbs-up](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/thumbup.png) if you need one of them or suggest a new feature!

Before you report a bug, [try the latest release](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api#installation-and-upgrade). If the issue still exists, provide the error trace, OS 
and Python version and explain how to reproduce the error. A demo script is appreciated.

If you don't find an issue related to your topic, please open a new [issue](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues)!

[Report a security bug!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/security/policy)

## Contributing
[UNICORN Binance WebSocket API](https://www.lucit.tech/unicorn-binance-websocket-api.html) is an open 
source project which welcomes contributions which can be anything from simple documentation fixes and reporting dead links to new features. To 
contribute follow 
[this guide](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/CONTRIBUTING.md).
 
### Contributors
[![Contributors](https://contributors-img.web.app/image?repo=oliver-zehentleitner/unicorn-binance-websocket-api)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/graphs/contributors)

We ![love](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-websocket-api/master/images/misc/heart.png) open source!

## Disclaimer
This project is for informational purposes only. You should not construe this information or any other material as 
legal, tax, investment, financial or other advice. Nothing contained herein constitutes a solicitation, recommendation, 
endorsement or offer by us or any third party provider to buy or sell any securities or other financial instruments in 
this or any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such 
jurisdiction.

### If you intend to use real money, use it at your own risk!

Under no circumstances will we be responsible or liable for any claims, damages, losses, expenses, costs or liabilities 
of any kind, including but not limited to direct or indirect damages for loss of profits.

### SOCKS5 Proxy / Geoblocking
We would like to explicitly point out that in our opinion US citizens are exclusively authorized to trade on Binance.US 
and that this restriction must not be circumvented!

The purpose of supporting a SOCKS5 proxy in the UNICORN Binance Suite and its modules is to allow non-US citizens to use 
US services. For example, GitHub actions with UBS will not work without a SOCKS5 proxy, as they will inevitably run on 
servers in the US and be blocked by Binance.com. Moreover, it also seems justified that traders, data scientists and 
companies from the US analyze binance.com market data - as long as they do not trade there.

## Commercial Support

[![Get professional and fast support](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-suite/master/images/support/LUCIT-get-professional-and-fast-support.png)](https://www.lucit.tech/get-support.html)

***Do you need a developer, operator or consultant?*** [Contact us](https://www.lucit.tech/contact.html) for a non-binding initial consultation!
