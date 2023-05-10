# Webull Option Trade Watcher

The Webull Option Trade Watcher is a Python script that monitors a user's Webull brokerage account for option trades and sends alerts to Discord using a webhook. This guide will walk you through the steps to set up and run the script.

## Prerequisites

Before you begin, you must have the following:

- A Webull brokerage account
- Python 3.7 or higher installed on your system
- Chrome or Firefox web browser installed on your system

## Setup

1. Clone or download the repository to your local machine.
2. Open the `_secrets.py` file in a text editor.
3. Enter your Webull login information and device ID in the file:
```python
WEBULL_LOGIN_EMAIL: str = "your_email"
WEBULL_LOGIN_PWD: str = "your_password"
WEBULL_TRADING_PIN: str = "your_trading_pin"
WEBULL_DEVICE_ID: str = "Trader-Bot" # Change this if desired
WEBULL_SECURITY_DID: str = "your_device_id"
