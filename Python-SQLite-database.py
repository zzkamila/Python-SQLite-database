import pandas as pd
import sqlite3 as sl
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


sl_connection = sl.connect('mydata.db')
sql = "CREATE TABLE IF NOT EXISTS smartphones (name TEXT, reviews TEXT, price TEXT)"
cursor = sl_connection.cursor()
cursor.execute(sql)

URL_TEMPLATE = "https://kaspi.kz/shop/c/smartphones/?q=%3AavailableInZones%3AMagnum_ZONE1%3Acategory%3ASmartphones&sort=relevance&sc="


service = Service(executable_path='C:/chromedriver/chromedriver') 
browser = webdriver.Chrome(service=service)
browser.get(URL_TEMPLATE)

current_page = 0

while True:
    
    list_of_phones = browser.find_elements(By.CLASS_NAME, 'item-card__info')
    time.sleep(3)
    
    for phone in list_of_phones:
        phone_str = phone.text
        phone_data_split = phone_str.split('\n')
        phone_name = phone_data_split[0]
        phone_reviews = phone_data_split[1]
        phone_price = phone_data_split[3]
        cursor.executemany("INSERT INTO smartphones VALUES(?,?,?)", ((phone_name, phone_reviews, phone_price),))
        sl_connection.commit()
        
    if current_page == 6:
        break   
    
    try:
        xpath = "//li[@class='pagination__el'][5]"
        element = browser.find_element(By.XPATH, xpath)
        browser.execute_script("return arguments[0].scrollIntoView();", element)
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        current_page += 1
        
    except:
        break
        



