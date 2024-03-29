# Passing Binance Market Data to Apache Kafka in Python with aiokafka
## Overview
Read this article:
https://medium.lucit.tech/passing-binance-market-data-to-apache-kafka-in-python-with-aiokafka-570541574655

## Prerequisites
Ensure you have Python 3.7+ installed on your system. 

Before running the provided script, install the required Python packages:
```bash
pip install -r requirements.txt
```

Since kafka-python has a lot of updates but no new release since 2020 I recommend installing kafka from 
GitHub [1](https://github.com/dpkp/kafka-python/issues/2412#issuecomment-1806341342):
```bash
pip install git+https://github.com/dpkp/kafka-python.git
```

## Get a UNICORN Binance Suite License
To run modules of the *UNICORN Binance Suite* you need a [valid license](https://shop.lucit.services)!

## Usage
### Graceful Shutdown:
The script is designed to handle a graceful shutdown upon receiving a KeyboardInterrupt (e.g., Ctrl+C) or encountering 
an unexpected exception.

## Logging
The script employs logging to provide insights into its operation and to assist in troubleshooting. Logs are saved to a 
file named after the script with a .log extension.

For further assistance or to report issues, please [contact our support team](https://www.lucit.tech/get-support.html) 
or [visit our GitHub repository](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api).