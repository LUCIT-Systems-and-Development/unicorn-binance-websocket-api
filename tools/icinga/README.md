# check_binance_websocket_api_manager
[ICINGA](https://icinga.com)/Nagios check_command '[check_binance_websocket_api_manager](https://exchange.icinga.com/bithon/check_binance_websocket_api_manager)' for the [UNICORN Binance WebSocket API](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api).

Requirements are listed in [requirements.txt](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/tools/icinga/requirements.txt)

This command is written in python 3 and depends on the monitoring API service of [UNICORN Binance WebSocket API](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api) which needs to get started with 'binance_websocket_api_manager.start_monitoring_api()'. Run '[example_monitoring.py](https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api/blob/master/example_monitoring.py)' to see an example!

Run './check_binance_websocket_api_manager -h' for further information!

Download the latest stable release from https://exchange.icinga.com/bithon/check_binance_websocket_api_manager

Read the [Howto: Monitoring UNICORN Binance WebSocket API Manager with Icinga2](https://www.unicorn-data.com/blog/article-details/howto-monitoring-unicorn-binance-websocket-api-manager-with-icinga2.html) to learn, how you can connect your application with ICINGA2

## Monitoring
### Status
OK, WARNING or CRITICAL
- WARNING: on restarts, available updates
- CRITICAL: crashed streams

### Perfdata
- average receives per second since last status check
- average speed per second since last status check
- received giga byte since start
- stream_buffer size
- stream_buffer items
- reconnects

![icinga2-demo](https://s3.gifyu.com/images/icinga2-unicorn_binance_websocket_api.png)