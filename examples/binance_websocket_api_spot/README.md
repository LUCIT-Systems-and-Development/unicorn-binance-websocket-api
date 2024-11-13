# Binance WebSocket API Spot
## Overview
Examples for the Binance Websocket API Spot.

## Prerequisites
Ensure you have Python 3.8+ installed on your system. 

Before running the provided script, install the required Python packages:
```bash
pip install -r requirements.txt
```

Create an `.env` file with the environment variables using `.env-example` as a template:
```bash
BINANCE_API_KEY=12A34BCD5678EFG90HIJKLM12NOP3456QR789STUV0WXYZ
BINANCE_API_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

## Get a UNICORN Binance Suite License
To run modules of the *UNICORN Trading Suite* you need a [valid license](https://shop.lucit.services)!

## Usage
### Running the Script:
```bash
python binance_chain_websocket_best_practice.py
```

### Graceful Shutdown:
The script is designed to handle a graceful shutdown upon receiving a KeyboardInterrupt (e.g., Ctrl+C) or encountering 
an unexpected exception.

## Logging
The script employs logging to provide insights into its operation and to assist in troubleshooting. Logs are saved to a 
file named after the script with a .log extension.

For further assistance or to report issues, please [contact our support team](https://www.lucit.tech/get-support.html) 
or [visit our GitHub repository](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api).