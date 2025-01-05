# This is a script to check on new DDPHE violations in Denver every day.


from bs4 import BeautifulSoup

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

SLACKURL = os.environ['SLACKURL']
CITYLOGIN = os.environ['CITYLOGIN']

# What day is today? This needs a subtraction if it's posted after 18:00 MST.
date = datetime.now()
date = date - timedelta(days=1)
date = str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/' + str(date.year)
print(date)

with open('DdpheViolationsLatestEntry.txt', 'r') as file:
    last_entry = file.read().strip()

# Let's load in the addresses we want to keep tabs on.
#addys = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSmhBBSJWwQSgegcqc8rZ6W5w_CT3XUPKPecLgSajw36_oOtM5ql7j0r-PbN0hDOSl6wAXH2EkNefE-/pub?output=tsv').text
#addys = addys.split('\r\n')
#addys = [x.upper() for x in addys]
#watchList = []
#for i in addys:
#	watchList.append(i.split('\t')[1])




# Here's the Selenium setup.

timer = 3
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
time.sleep(6)


# Login to the portal
browser.switch_to.frame(browser.find_element('xpath', '//*[@id="LoginFrame"]'))
browser.find_element('xpath', '//*[@id="username"]').send_keys('kevinjbeaty')
browser.find_element('xpath', '//*[@id="passwordRequired"]').send_keys(CITYLOGIN)
time.sleep(timer)

browser.find_element('xpath', '//*[@id="FirstAnchorInACAMainContent"]/app-login-screen/div/p-card/div/div/div/aca-login-panel/form/div[5]/accela-button-primary/div/button/span').click()
time.sleep(10)

browser.switch_to.parent_frame()
browser.find_element('xpath','//*[@id="span_tab_2"]/table/tbody/tr/td[2]/div/a').click()
time.sleep(timer)

select = Select(browser.find_element('xpath','//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]'))
select.select_by_visible_text('DDPHE Administrative Citation')
time.sleep(1)
browser.find_element('xpath','//*[@id="ctl00_PlaceHolderMain_btnNewSearch"]').click()

time.sleep(20)

html = browser.find_element('xpath','//*[@id="ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList"]/tbody').get_attribute('innerHTML')
soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all('tr')[3:-2]
count = 0
for i in rows:
	count += 1
	rowID = i.find_all('td')[1].text.replace('\n',"")
	if (rowID == last_entry):
        	break
	else:
		if (count == 1):
			with open('DdpheViolationsLatestEntry.txt', 'w') as file:
				file.write(rowID)
		desc = i.find_all('td')[3].text.replace('\n',"")
		addy = i.find_all('td')[4].text.replace('\n',"")
		postThis = '{"text":":grimacing: *New DDPHE violation!*\n\n*<' + url +  '|' + addy + '>*\n' + desc + '\n\n"}'
		response = requests.post(SLACKURL, data=postThis, headers={'Content-type': 'application/json'})
		if (count == 10):
			postThis = '{"text":"There may be more here today, so check the website!"}'
			response = requests.post(SLACKURL, data=postThis, headers={'Content-type': 'application/json'})
