# This is a script to check in on new design proposals in Denver every day.


from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import requests
from datetime import datetime, timedelta
import time
import json
import os


SLACKURL = os.environ['SLACKURL']
CITYLOGIN = os.environ['CITYLOGIN']

# What day is today? This needs a subtraction if it's posted after 18:00 MST.
date = datetime.now()
date = date - timedelta(days=1)
date = str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/' + str(date.year)


# Let's load in the addresses we want to keep tabs on.
addys = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSmhBBSJWwQSgegcqc8rZ6W5w_CT3XUPKPecLgSajw36_oOtM5ql7j0r-PbN0hDOSl6wAXH2EkNefE-/pub?output=tsv').text
addys = addys.split('\r\n')
addys = [x.upper() for x in addys]
watchList = []
for i in addys:
	watchList.append(i.split('\t')[1])



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


# Time to fire up Selenium!


url = 'https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Community-Planning-and-Development/E-permits/E-permits-portal'
browser.get(url)
time.sleep(10)


# Login to the portal
print(browser.find_element('xpath', '//*[@id="ctl00_PlaceHolderMain_divContent"]').text)
browser.switch_to.frame(browser.find_element('xpath', '//*[@id="LoginFrame"]'))
browser.find_element('xpath', '//*[@id="username"]').send_keys('kevinjbeaty')
browser.find_element('xpath', '//*[@id="passwordRequired"]').send_keys('kiL2M@0mDXtJAu$')
time.sleep(3)
browser.find_element('xpath', '/html/body/main/app-root/div/aca-login-panel/form/div[5]/accela-button-primary/div/button/span').click()
time.sleep(10)
print(browser.page_source)
