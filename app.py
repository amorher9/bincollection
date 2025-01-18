
import streamlit as st
import pandas as pd
import numpy as np
import selenium #to navigate through the webb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#According to IA:
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import seleniumbase as sb

st.header("Welcome to my bin collection webapp")

# Using Chrome to access web
proxy = "20.235.159.154:80"
diver=sb.Driver(browser='chrome', headless2=True, uc=True, proxy=proxy)
driver = webdriver.Chrome()
# Open the website

driver.get('https://online.cheshireeast.gov.uk/mycollectionday/')
# Select the id box
#elem=driver.find_element(By.ID, 'postcode')
# Send id information
#elem.send_keys('SK118ED')
# Select the id box
#elem2=driver.find_element(By.ID, 'propertyname')
# Send id information
#elem2.send_keys('6')
# Find login button
#login_button = driver.find_element(By.ID, 'btn-search-form')
# Click login
#login_button.click()

#driver.implicitly_wait(10)
#driver.find_element(By.LINK_TEXT, "See bin collection dates for this address").click()
