import gspread

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import requests
import json
import os
import re

import time
from datetime import datetime, timedelta

PRICEKEY = os.environ['PRICEKEY']
PRIVATEKEY = os.environ['PRIVATEKEY']
PRIVATEIDKEY = os.environ['PRIVATEIDKEY']


# What day is today?

date = datetime.now()
date = date - timedelta(days=1)
date = str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/' + str(date.year)


# Here's the Selenium setup.

timer = 5
chrome_options = Options()
options = [
    "--headless",
    "--window-size=1920,1200",
    "--ignore-certificate-errors"
]
for option in options:
    chrome_options.add_argument(option)
browser = webdriver.Chrome(options=chrome_options)

# And the Gspread setup, to append data to a Google sheet.

creds = {
  "type": "service_account",
  "project_id": "airbot-291606",
  "private_key_id": PRIVATEIDKEY,
  "private_key": "-----BEGIN PRIVATE KEY-----\n" + PRIVATEKEY + "\n-----END PRIVATE KEY-----\n",
  "client_email": "dailyairbot@airbot-291606.iam.gserviceaccount.com",
  "client_id": "105388363485733269650",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dailyairbot%40airbot-291606.iam.gserviceaccount.com"
}

def loadItIn(data):
  gc = gspread.service_account_from_dict(creds)
  gsheet = gc.open_by_key(PRICEKEY)
  sheetdata = gsheet.get_worksheet(0)
  sheetdata.append_row(data)  

# Good Times

url = "https://www.grubhub.com/restaurant/good-times-burgers--frozen-custard-102-808-e-colfax-ave-denver/2061835"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')
loadItIn([date, "Good Times", "Deluxe Cheesburger"])
