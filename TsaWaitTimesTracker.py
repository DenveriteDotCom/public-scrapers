# Let's start with our variables and libraries.

import gspread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import requests
from datetime import datetime, timedelta
import time
import json
import os
import re

timer = 3

os.environ["DISPLAY"] = ":99"

TSAKEY = os.environ['TSAKEY']
PRIVATEKEY = os.environ['PRIVATEKEY']
PRIVATEIDKEY = os.environ['PRIVATEIDKEY']
SLACKURL = os.environ['SLACKURL']

# Next, we set up Selenium to open the page virtually.

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
chrome_options = Options()
options = [
    "--window-size=1920,1200",
    "--ignore-certificate-errors"
]
for option in options:
    chrome_options.add_argument(option)
browser = webdriver.Chrome(options=chrome_options)

# Next is the Gspread setup, to append data to a Google sheet.

creds = {
    "type": "service_account",
    "project_id": "airbot-291606",
    "private_key_id": PRIVATEIDKEY,
    "private_key": PRIVATEKEY,
    "client_email": "dailyairbot@airbot-291606.iam.gserviceaccount.com",
    "client_id": "105388363485733269650",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dailyairbot%40airbot-291606.iam.gserviceaccount.com"
}

def loadItIn(data):
    gc = gspread.service_account_from_dict(creds)
    gsheet = gc.open_by_key('19PEMS3Ajh4rPdakjcDISgbEW3d8mA293birFNrwe2Hc')
    sheetdata = gsheet.get_worksheet(0)
    sheetdata.append_row(data)
	
	# This ^ is our funcction to append an array of values into individual cells
	# in google sheets, per Gspread's API. We'll call it later. It requires additional
	# setup in Google Docs, creating a bot agent to act on our behalf.


# What day is today? What time? And we need to subtract 6 hours since this runs in GMT.

date = datetime.now()
date = date - timedelta(hours=6)
currentTime = str(date.hour).zfill(2) + ":" + str(date.minute).zfill(2)
date = str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/' + str(date.year)

# Grab the page and find our numbers.

url = 'https://www.flydenver.com/security/'
browser.get(url)
time.sleep(timer)
	# "sleep" just tells the system to wait a sec, in this case timer = 3 seconds, to let the virtual browser catch up.

numbers = browser.find_elements(By.CLASS_NAME, "wait-num")

	# This ^ finds six fields on the page called "wait num" and combines them into an array.
	# We'll use indexing [0] and [3] to get the first and fourth values in that array, which are regular
	# wait times and not precheck. Those values are string ranges, like "0-4", so we'll split them into
	# single numbers and assign each min and max to their own variables.

eastMin = numbers[0].text.split('-')[0]
eastMax = numbers[0].text.split('-')[1]
westMin = numbers[3].text.split('-')[0]
westMax = numbers[3].text.split('-')[1]
time.sleep(timer)

# Finally, toss the numbers into our sheet and, if necessary, ping Botlandia.

loadItIn([date,currentTime,eastMin,eastMax,westMin,westMax])
time.sleep(timer)

if int(westMax) > 30 or int(eastMax) > 30:
	postThis = '{"text":"<!here> <https://docs.google.com/spreadsheets/d/' + TSAKEY + '/edit?usp=sharing|TSA wait times> are longer than 30 minutes!\nEast Security times: ' + eastMin + '-' + eastMax + '\nWest Security times:' + westMin + '-' + westMax + '"}'
	response = requests.post(SLACKURL, data=postThis, headers={'Content-type': 'application/json'})

	# This stuff here ^ is how Slack accepts new messages via Webhook.
	# Slack has its own protocols for how this should be formatted.
