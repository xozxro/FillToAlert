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
```
You can retrieve your device ID by following the instructions in the next section.
4. Save and close the _secrets.py file.

#### Retrieving the Webull Device ID

To retrieve your Webull device ID:

- Open a private window in your Chrome or Firefox web browser.
- Navigate to https://app.webull.com.
- Visit the paper trading tab.
- Open the developer tools using the keyboard shortcut Ctrl + Shift + I for Chrome or Ctrl + Shift + K for Firefox.
- Click on the Network tab in the developer tools.
- Click on any line listing 'getQuote'.
- Scroll down to the 'Request Headers' section and copy the 'did' value.
- Paste the 'did' value into the WEBULL_SECURITY_DID field in the _secrets.py file with 0 spaces between any of the quotes.

#### Running the Script

To run the script:

- Ensure that the _secrets.py file is saved and closed.
- Open a command prompt or terminal window in the project directory.
- Run the run.bat file by double-clicking on it. This will start the script and handle any unexpected script exits so that errors can be read.

#### Configuring Discord Webhook

To configure the Discord webhook:

- Open the settings.json file in a text editor.
- Enter the Discord webhook URL and webhook author name in the file:

```json
{
    "discord_webhook_url": "your_discord_webhook_url_here",
    "discord_webhook_name": "Trader Bot"
}
```
