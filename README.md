# Webull Option Trade Watcher

The Webull Option Trade Watcher is a Python script that monitors a user's Webull brokerage account for option trades and sends alerts to Discord using a webhook. This guide will walk you through the steps to set up and run the script.

The script will call alerts as such:

`BTO TICKER STRIKESIDE EXP @ FILLPRICE`

and will call sells and exits according to your open position QT as well:

`TRIM TICKER STRIKESIDE EXP @ FILLPRICE`

`STC TICKER STRIKESIDE EXP @ FILLPRICE`


This script is built to seamlessly integrate with [Nyria's Trade Bot](https://nyriabot.io/for-servers). This script will ensure that your alerts are 100% accurate and interpretable by the bot, and that everything is correct for stat tracking, formatting, etc. Additionally, your users will be able to get into the same plays within a split second of your order fill in Webull, when using these two in combination.

## Prerequisites

Before you begin, you must have the following:

- A Webull brokerage account
- Python 3.7 or higher installed on your system. [Install here](https://python.org).
- Chrome or Firefox web browser installed on your system

#### Run 'setup.bat' from the same directory as 'requirements.txt' to install the necessary packages.
#### Or, navigate to the directory in a terminal, and use `py -m pip install -r requirements.txt`

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

### Retrieving the Webull Device ID

To retrieve your Webull device ID:

- Open a private window in your Chrome or Firefox web browser.
- Navigate to https://app.webull.com.
- Visit the paper trading tab.
- Open the developer tools using the keyboard shortcut Ctrl + Shift + I for Chrome or Ctrl + Shift + K for Firefox.
- Click on the Network tab in the developer tools.
- Click on any line listing 'getQuote'.
- Scroll down to the 'Request Headers' section and copy the 'did' value.
- Paste the 'did' value into the WEBULL_SECURITY_DID field in the _secrets.py file with 0 spaces between any of the quotes.

By passing the image verification on Webull, after saving the DID created on your initial load of the Webull page, that DID is logged as having succesfully completed that verification. So, we need to pass this ID with your credentials, so that Webull doesn't require image verification when accessing the account via this script - which we cannot handle progrmatically.

Using this method, you will seldom need to redo your login. The script should continue to work for a period of time - I will update this section if an expiration time is discovered.

#### To read the original post on this process provided by the package used in this script, [please visit them here](https://github.com/tedchou12/webull/wiki/Workaround-for-Login-Method-2).

### Configuring Discord Webhook

To configure the Discord webhook:

- Open the settings.json file in a text editor.
- Enter the Discord webhook URL and webhook author name in the file:

```json
{
    "discord_webhook_url": "your_discord_webhook_url_here",
    "discord_webhook_name": "Trader Bot"
}
```

### Running the Script

To run the script:

- Ensure that the _secrets.py file is saved and closed.
- Open a command prompt or terminal window in the project directory.
- Run the run.bat file by double-clicking on it. This will start the script and handle any unexpected script exits so that errors can be read.
