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
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)
browser = webdriver.Chrome(options=chrome_options)


# Time to fire up Selenium!


url = 'https://www.denvergov.org/AccelaCitizenAccess/Cap/CapHome.aspx?module=Development&TabName=Home'
browser.get(url)
time.sleep(timer)


# Login to the portal

browser.switch_to.frame(browser.find_element('xpath', '//*[@id="LoginFrame"]'))
browser.find_element('xpath', '//*[@id="username"]').send_keys('kevinjbeaty')
browser.find_element('xpath', '//*[@id="passwordRequired"]').send_keys(CITYLOGIN)
browser.find_element('xpath', '/html/body/main/app-root/div/aca-login-panel/form/div[5]/accela-button-primary/div/button/span').click()
time.sleep(timer)
browser.find_element('xpath','//*[@id="span_tab_1"]/table/tbody/tr/td[2]/div/a').click()
time.sleep(timer)

# Select design proposals and search for all entries

browser.find_element('xpath', '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]').click()
browser.find_element('xpath', '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"]/option[9]').click()
time.sleep(timer)
browser.find_element('xpath', '//*[@id="ctl00_PlaceHolderMain_btnNewSearch"]').click()
time.sleep(timer)



# Feed the page into BeautifulSoup and select stuff that was added today.

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
todaysLinks = soup.findAll(text=date)
count = 0

# Run through all of today's entries and ping Slack if there's anything that meets our criteria.
# This now also has a function to try the next page if there are 10 listings on the current page, suggesting there could be more.


def handleListing():
	global todaysLinks
	global date
	global count
	for i in todaysLinks:
		count = count + 1
		try:
			# Access list items from today
			link = 'https://aca-prod.accela.com' + i.parent.parent.parent.findNext('td').find('a')['href']
			address = i.parent.parent.parent.findNext('td').findNext('td').findNext('td').findNext('td').text.replace('\n','').split('\r')
			address = address[0].upper().split(', DENVER')[0]
			type = i.parent.parent.parent.findNext('td').findNext('td').findNext('td').text.replace('\n','')
			print(address)
			print(link)
			# Access details in the second page
			page = requests.get(link).text
			soup2 = BeautifulSoup(page, 'html.parser')
			time.sleep(5)
			emer = soup2.find(text='Flag as Emergency?: ').parent.parent.findNext('div').text.replace('\n','')
			desc = soup2.find(text='Project Description:').parent.findNext('span').text.replace('\n','')
			print(emer, desc)
			if emer == 'No':
				postThis2 = {'text':"Howdy! There's a new building complaint about <" + link + "|" + address + ">\nIt's categorized as '" + type + "' and described as '" + desc + "'."}
			else:
				postThis2 = {'text':"Howdy! There's a new building complaint about " + address + "\nIt's categorized as '" + type + "' and described as '" + desc + "'.\nHeads up <!here>, it was listed as an emergency!"}
			response2 = requests.post(SLACKURL, data=json.dumps(postThis2), headers={'Content-Type': 'application/json'})
		except:
			pass
	if count == 10:
		time.sleep(5)
		count = 0
		browser.find_element('xpath', '//a[text()="Next >"]').click()
		time.sleep(5)
		html = browser.page_source
		soup = BeautifulSoup(html, 'html.parser')
		todaysLinks = soup.findAll(text=date)
		if len(todaysLinks)>0:
			try:
				handleListing()
			except:
				pass


if len(todaysLinks) > 0:
	handleListing()
