# This is a script to check in on new design proposals in Denver every day.


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
time.sleep(20)

browser.switch_to.parent_frame()
browser.find_element('xpath','//*[@id="span_tab_1"]/table/tbody/tr/td[2]/div/a').click()
time.sleep(timer)

select = Select(browser.find_element('xpath','//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]'))
select.select_by_visible_text('Formal Site Development Plan')
time.sleep(1)
browser.find_element('xpath','//*[@id="ctl00_PlaceHolderMain_btnNewSearch"]').click()

time.sleep(20)

html = browser.find_element('xpath','//*[@id="ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList"]/tbody').get_attribute('innerHTML')
soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all('tr')[3:-2]
records = []
for i in rows:
	if i.find_all('td')[2].text.replace('\n',"") == '12/20/2024':
        	records.append(i.find_all('td')[3].find('a')['href'])

for i in records:
	browser.get('https://aca-prod.accela.com/' + i)
	time.sleep(12)
	soup = BeautifulSoup(browser.page_source, 'html.parser')
	try:
		units = int(soup.find(string=re.compile('number of residential')).next.next.next.text.replace('\n',''))
	except:
		units = ''
	try:
		use1 = soup.find(string=re.compile('Proposed Use 1')).next.next.next.text.replace('\n','')
	except:
		use1 = ''
	try:
		use2 = soup.find(string=re.compile('Proposed Use 2')).next.next.next.text.replace('\n','')
	except:
		use2 = ''
	#projectId = soup.find(string=re.compile('Project Master Number')).next.next.next.text.replace('\n','')
	try:
		addy = soup.find('div',{'id':'divWorkLocationInfo'}).text.replace('\n','').replace('\xa0','').replace('*','')
	except:
		addy = ''
	try:
		desc = soup.find(string=re.compile('Project Description')).next.next.next.text.replace('\n','')
	except:
		desc = ''
	if units < 20:
		postThis = 'New formal site development plan!\n\n' + address + '\n' + use1 + '\n' + use2 + '\n' + desc
		response = requests.post(SLACKURL, data=json.dumps(postThis), headers={'Content-Type': 'application/json'}) 
	else:
		postThis = 'New formal site development plan WITH A LOT OF UNITS!\n\n' + address + '\n' + use1 + '\n' + use2 + '\n' + desc
		response = requests.post(SLACKURL, data=json.dumps(postThis), headers={'Content-Type': 'application/json'}) 
