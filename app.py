import streamlit as st
import pandas as pd
import numpy as np
import selenium #to navigate through the webb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os
import subprocess
import sys
import pytest

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

st.header("Welcome to my bin collection webapp")

# Using Chrome to access web
#proxy = "20.235.159.154:80"
#driver=sb.Driver(browser='chrome', headless=False, uc=True, proxy=proxy)

#options = webdriver.FirefoxOptions()
#driver = webdriver.Firefox(options=options)

#driver = webdriver.Chrome()
# Open the website

driver.get('https://online.cheshireeast.gov.uk/mycollectionday/')
# Select the id box
elem=driver.find_element(By.ID, 'postcode')
# Send id information
elem.send_keys('SK118ED')
# Select the id box
elem2=driver.find_element(By.ID, 'propertyname')
# Send id information
elem2.send_keys('6')
# Find login button
login_button = driver.find_element(By.ID, 'btn-search-form')
# Click login
login_button.click()

#lnks=driver.find_elements(By.TAG_NAME, "a")
# traverse list
#for lnk in lnks:
   # get_attribute() to get all href
   #print(lnk.get_attribute("href"))

driver.implicitly_wait(10)
driver.find_element(By.LINK_TEXT, "See bin collection dates for this address").click()  #Original
#driver.find_element(By.ID, "See bin collection dates for this address").click()
#driver.find_element(By.CLASS_NAME, "get-job-details sys_0 sys_t1090").click()


