import gspread

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

PRICEKEY = os.environ['PRICEKEY']
PRIVATEKEY = os.environ['PRIVATEKEY']
PRIVATEIDKEY = os.environ['PRIVATEIDKEY']


# What day is today?

date = datetime.now()
date = date - timedelta(days=1)
date = str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/' + str(date.year)


# Here's the Selenium setup.

timer = 10
quicktimer = 5
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
  gsheet = gc.open_by_key(PRICEKEY)
  sheetdata = gsheet.get_worksheet(0)
  sheetdata.append_row(data)  

# Phillips 66

url = "https://www.gasbuddy.com/station/7098"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Phillips 66", "Regular", soup.find(string="Regular").parent.parent.parent.next_sibling.text.split("\xa0")[0]])
time.sleep(quicktimer)

# Mayfair Liquor / Modelo

url = "https://mayfairliquors.com/shop/product/modelo-especial-cans/58afba2c01ff952311790d51?option-id=dcf13820e8cc5cfe38c5788886011d3cfb105e7b01d1b87607be80c506935c19"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Mayfair Liquor", "Modelo Especial 12 Cans", soup.find('div',{'class':'product-price-discount-with'}).text.replace(' ','')])
time.sleep(quicktimer)

# Mayfair Liquor / Coors

url = "https://mayfairliquors.com/shop/product/coors-light/58a4bc8f01ff950d1fb225cb?option-id=9abd3e0e120ae2fd9bbbf5c6aad534db5a01051f3bb42a213499450c21832b37"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Mayfair Liquor", "Coors Light 12 Cans", soup.find('div',{'class':'product-price-discount-with'}).text.replace(' ','')])
time.sleep(quicktimer)

# Mayfair Liquor / 90 Shilling

url = "https://mayfairliquors.com/shop/product/odell-90-shilling-ale-cans/58afbc9b01ff952311790f59?option-id=026446ebba847d889f1b714ce878e5ea3fdd9b75e5a2bcc8165f9a34a2aab5a5"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Mayfair Liquor", "90 Shilling 12 Cans", soup.find('div',{'class':'product-price-discount-with'}).text.replace(' ','')])
time.sleep(quicktimer)

# Mayfair Liquor / Yeti

url = "https://mayfairliquors.com/shop/product/great-divide-yeti-imperial-stout/58a45cb701ff950d1fb1fe4c?option-id=5af2d63ba577f6ae0f4c88f7d8ad62f9eca01aa2686127c24447a9badcea9076"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Mayfair Liquor", "Yeti Imperial 6 Cans", soup.find('div',{'class':'product-price-discount-with'}).text.replace(' ','')])
time.sleep(quicktimer)

# Mayfair Liquor / Cerebral

url = "https://mayfairliquors.com/shop/product/cerebral-secure-line/608079fa5af39567402f2987?option-id=84a73280dbb290b5c0c84366072730ab5bd43132baed4906da0fcca3dea23872"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Mayfair Liquor", "Cerebral Secure Line 4 Cans", soup.find('div',{'class':'product-price-discount-with'}).text.replace(' ','')])
time.sleep(quicktimer)

# Mayfair Liquor / Station 26

url = "https://mayfairliquors.com/shop/product/station-26-colorado-tangerine-cream-ale/59655875355d0935c14d8c29?option-id=d47b0d57e2836dc81fc3bd515135b6885d7bc2394abd57f8142abb79d693efcd"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Mayfair Liquor", "Station 26 Tangerine Cream 6 Cans", soup.find('div',{'class':'product-price-discount-with'}).text.replace(' ','')])
time.sleep(quicktimer)

# Tokyo Premium

url = "https://my-site-100105-109931.square.site"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Tokyo Premium", "Matcha Cream", soup.find("p",{"title":"Matcha Cream"}).parent.parent.parent.find('div',{'class':'item__price-badges-order-again'}).text.replace('\n','').replace('\t','').replace(' ','')])
loadItIn([date, "Tokyo Premium", "Red Bean Donut", soup.find("p",{"title":"Red Bean Donut"}).parent.parent.parent.find('div',{'class':'item__price-badges-order-again'}).text.replace('\n','').replace('\t','').replace(' ','')])
loadItIn([date, "Tokyo Premium", "Beef Curry", soup.find("p",{"title":"Beef Curry"}).parent.parent.parent.find('div',{'class':'item__price-badges-order-again'}).text.replace('\n','').replace('\t','').replace(' ','')])

# Soops / eggs

url = "https://www.kingsoopers.com/p/kroger-cage-free-extra-large-grade-aa-white-eggs/0001111009039?fulfillment=PICKUP&searchType=default_search"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')
loadItIn([date, "King Soopers", "12 Extra Large AA Eggs", soup.find("data",{"typeof":"Price"}).text])

# Soops / avocado

url = "https://www.kingsoopers.com/p/large-avocado/0000000004225?fulfillment=PICKUP&searchType=suggestions"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')
loadItIn([date, "King Soopers", "Large Avocados", soup.find("data",{"typeof":"Price"}).text])

# Soops / peaches

url = "https://www.kingsoopers.com/p/fresh-california-yellow-peach-each/0000000004038?fulfillment=PICKUP&searchType=suggestions"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')
loadItIn([date, "King Soopers", "Yellow California Peaches", soup.find("span",{"id":"ProductDetails-sellBy-weight"}).text])

# Zorba's

url = "https://order.toasttab.com/online/chef-zorbas-restaurant"
browser.get(url)
time.sleep(timer)
soup = BeautifulSoup(browser.page_source, 'html.parser')

loadItIn([date, "Zorba's", "Just Eggs", soup.find(string="Just Eggs").parent.parent.parent.parent.parent.find('span',{'class':'price'}).text])
loadItIn([date, "Zorba's", "Steak & Eggs", soup.find(string="Steak & Eggs").parent.parent.parent.parent.parent.find('span',{'class':'price'}).text])
loadItIn([date, "Zorba's", "2 Eggs & Gyro", soup.find(string="2 Eggs & Gyro").parent.parent.parent.parent.parent.find('span',{'class':'price'}).text])
time.sleep(quicktimer)

# Good Times

url = "https://www.grubhub.com/restaurant/good-times-burgers--frozen-custard-102-808-e-colfax-ave-denver/2061835"
browser.get(url)
time.sleep(timer)

soup = BeautifulSoup(browser.page_source, 'html.parser')
loadItIn([date, "Good Times", "Deluxe Cheesburger", soup.find(string="Deluxe Cheeseburger").parent.parent.parent.parent.parent.find('span',{'itemprop':'price'}).text])
loadItIn([date, "Good Times", "Guacamole Bacon Burger", soup.find(string="Guacamole Bacon Burger").parent.parent.parent.parent.parent.find('span',{'itemprop':'price'}).text])

browser.find_element('xpath','/html/body/ghs-site-container/span/div/div[3]/div[1]/span/div/ghs-router-outlet/span/ghs-restaurant-provider/div/div[1]/div/main/div[4]/div/div[1]/div[1]/div/span/ul/li[4]/span').click()
time.sleep(quicktimer)
loadItIn([date, "Good Times", "Crispy Chicken Sandwich", soup.find(string="Crispy Chicken Sandwich").parent.parent.parent.parent.parent.find('span',{'itemprop':'price'}).text])
time.sleep(quicktimer)
