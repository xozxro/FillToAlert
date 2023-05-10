# FillToOpenAlert
This repo contains scripts to monitor a brokerage account and call option alerts to a Discord as configured.
!
2 / 2
Webull Option Alerts Discord Bot

This script monitors a user's Webull brokerage account for option trades and sends alerts to a Discord server using webhooks. To get started, follow the steps below to authenticate with Webull and set up your Discord webhook.
Table of Contents

    Requirements
    Configuration
        Edit _secrets.py
        Edit settings.json
    Authentication with Webull
        Chrome
        Firefox
    Running the Script

Requirements

    Python 3.6 or later
    Chrome or Firefox browser

Configuration
Edit _secrets.py

Update the _secrets.py file with your Webull login information and device ID. The file should look like this:

python

WEBULL_LOGIN_EMAIL: str = "<YOUR_EMAIL>"
WEBULL_LOGIN_PWD: str = "<YOUR_PASSWORD>"
WEBULL_TRADING_PIN: str = "<YOUR_TRADING_PIN>"
WEBULL_DEVICE_ID: str = "Trader-Bot"
WEBULL_SECURITY_DID: str = "<YOUR_DEVICE_ID>"

Replace <YOUR_EMAIL>, <YOUR_PASSWORD>, <YOUR_TRADING_PIN>, and <YOUR_DEVICE_ID> with your actual Webull credentials and device ID. The device ID will be retrieved in the next section.
Edit settings.json

Update the settings.json file with your Discord webhook URL and author name:

json

{
  "webhook_url": "<YOUR_WEBHOOK_URL>",
  "webhook_author_name": "<YOUR_AUTHOR_NAME>"
}

Replace <YOUR_WEBHOOK_URL> and <YOUR_AUTHOR_NAME> with your actual Discord webhook URL and preferred author name.
Authentication with Webull

To authenticate with Webull, you need to generate and retrieve a device ID from the page response headers when accessing the Webull app website.
Chrome

    Open a new Incognito window in Chrome (press Ctrl+Shift+N or Cmd+Shift+N on macOS).
    Navigate to app.webull.com.
    Go to the Paper Trading tab.
    Open Developer Tools by pressing Ctrl+Shift+I or Cmd+Opt+I on macOS.
    Click on the Network tab.
    In the list of network requests, click on any line listing getQuote.
    In the Headers section, scroll down to Request Headers.
    Copy the value of did.
    Paste the value into the WEBULL_SECURITY_DID field in the _secrets.py file.

Firefox

    Open a new Private window in Firefox (press Ctrl+Shift+P or Cmd+Shift+P on macOS).
    Navigate to app.webull.com.
    Go to the Paper Trading tab.
    Open Developer Tools by pressing Ctrl+Shift+I or Cmd+Opt+I on macOS.
    Click on the Network tab.
    In the list of network requests, click on any line listing getQuote.
    In the Headers section, scroll down to Request Headers.
    Copy the value of did.
    Paste the value into
