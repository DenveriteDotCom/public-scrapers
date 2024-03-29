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



# Here's the Selenium setup.

timer = 6
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
time.sleep(timer)

print(browser.find_element('xpath', '//*[@id="ctl00_PlaceHolderMain_areaNotLoggedIn"]').text)

# Login to the portal

browser.switch_to.frame(browser.find_element('xpath', '//*[@id="LoginFrame"]'))
time.sleep(5)
browser.find_element('xpath', '//*[@id="username"]').send_keys('kevinjbeaty')
time.sleep(5)
browser.find_element('xpath', '//*[@id="passwordRequired"]').send_keys(CITYLOGIN)
time.sleep(5)
browser.find_element('xpath', '/html/body/main/app-root/div/aca-login-panel/form/div[5]/accela-button-primary/div/button/span').click()
time.sleep(10)

print(browser.page_source)

