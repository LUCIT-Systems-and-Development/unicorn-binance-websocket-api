# UNICORN Binance WebSocket API
A python API to use the Binance Websocket API in a easy, fast, robust and fully-featured way.

Read the Howto: UNICORN Binance WebSocket API for installation instructions and a guide on how to use it.
The python module UNICORN Binance WebSocket API provides an API to the Binance Websocket API, which supports the 
streaming of public streams like trades, kline, ticker and depth, but also the private userData stream which need to be 
used with a valid api_key and api_secret from the Binance Exchange.

The module requires python 3.5.1 or above, as it depends on pythons latest asyncio features for asynchronous/concurrent 
processing. The current requirements are listed here.

Be aware that the Binance websocket API just offers to receive data. If you would like to set orders, withdraws and so 
on, you have to use the Binance Rest API in combination. Great support for this offers the package 
sammchardy/python-binance.

"sammchardy/python-binance" provides a websocket client too, so why to use the UNICORN Binance WebSocket API?

- 100% auto-reconnect.
- Streams are processing asynchronous/concurrent (python asyncio) and each stream is started in an separate thread.
- No use of the twisted module, so you can use this lib in a daemonized application (compatible with python-daemon).
- If you can not store your data in couse of an offline local database, you can kick back the data to the stream_buffer 
which stores the receives in the RAM till you are able to process the data in the normal way again.
- Helpful management features.

## Howto: 
https://www.unicorn-data.com/blog/article-details/howto-unicorn-binance-websocket-api.html

## Documentation: 
https://www.unicorn-data.com/service/unicorn-binance-websocket-api.html

## Project, code and downloads: 
https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api
