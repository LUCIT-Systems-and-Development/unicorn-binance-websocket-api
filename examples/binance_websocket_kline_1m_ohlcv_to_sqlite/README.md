# Downloading and Storing Binance OHLCV Data Asynchronously To SQLite
## Overview
This guide outlines how to use our Python library to asynchronously download Open, High, Low, Close, Volume (OHLCV) 
data from Binance for selected markets and store this data in a SQLite database `ohlcv.db`. Our solution leverages 
WebSocket and REST API connections for real-time data streaming and efficient data management.

To open the generated DB file you can use the [DB Browser for SQLite](https://sqlitebrowser.org).

## Prerequisites
Ensure you have Python 3.7+ installed on your system. 

Before running the provided script, install the required Python packages:
```bash
pip install -r requirements.txt
```
## Get a UNICORN Binance Suite License
To run modules of the *UNICORN Binance Suite* you need a [valid license](https://shop.lucit.services)!

## Usage
### Initialization:
The script initializes a WebSocket connection to Binance using unicorn_binance_websocket_api and sets up an asynchronous 
SQLite database using aiosqlite.

### Fetching Market Data:
It fetches available market symbols ending with `USDT` via Binance's REST API and subscribes to kline (OHLCV) data 
streams for these markets, limiting to the first 1024 (provided by `get_limit_of_subscriptions_per_stream()`) 
binance.com spot markets.

### Database Operations:
The script listens for incoming OHLCV data from the subscribed streams, validates the data, and stores it in a SQLite 
database in an asynchronous manner. The database operations include creating a connection, defining a table for OHLCV 
data, inserting new data records, and counting the number of records.

### Running the Script:
To start the data download and storage process, simply run the script:
```bash
python binance_websocket_kline_1m_ohlcv_to_sqlite.py
```

### Graceful Shutdown:
The script is designed to handle a graceful shutdown upon receiving a KeyboardInterrupt (e.g., Ctrl+C) or encountering 
an unexpected exception.

## Logging
The script employs logging to provide insights into its operation and to assist in troubleshooting. Logs are saved to a 
file named after the script with a .log extension.

For further assistance or to report issues, please [contact our support team](https://www.lucit.tech/get-support.html) 
or [visit our GitHub repository](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api).