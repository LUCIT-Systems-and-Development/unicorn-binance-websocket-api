# Binance WebSocket `stream_signals`
## Overview
Usually you want to know when a stream is working and when it is not. This can be useful to know that your own system is 
currently "blind" and you may want to close open positions to be on the safe side, know that indicators will now provide 
incorrect values or that you have to reload the missing data via REST as an alternative. 

For this purpose, the UNICORN Binance WebSocket API provides so-called 
[`stream_signals`](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signals%60)
, which are used to tell your code in real time when a stream is connected, when it received its first data record, when 
it was disconnected and stopped, and when the stream cannot be restored.

In this example, a stream is started and stopped. To keep the example lean and clear, we will not process any data, but 
only activate and process the stream signals.

## Prerequisites
Ensure you have Python 3.7+ installed on your system. 

Before running the provided script, install the required Python packages:
```bash
pip install -r requirements.txt
```
## Get a UNICORN Binance Suite License
To run modules of the *UNICORN Binance Suite* you need a [valid license](https://shop.lucit.services)!

## Usage
### Running the Script:
```bash
python binance_websocket_stream_signals.py
```

### Graceful Shutdown:
The script is designed to handle a graceful shutdown upon receiving a KeyboardInterrupt (e.g., Ctrl+C) or encountering 
an unexpected exception.

## Logging
The script employs logging to provide insights into its operation and to assist in troubleshooting. Logs are saved to a 
file named after the script with a .log extension.

For further assistance or to report issues, please [contact our support team](https://www.lucit.tech/get-support.html) 
or [visit our GitHub repository](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api).