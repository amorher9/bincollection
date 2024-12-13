
import streamlit as st
import pandas as pd
import numpy as np
import selenium #to navigate through the webb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


st.header("Welcome to my bin collection webapp")

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--window-size=1920x1080')
#chrome_options.add_argument('--disable-gpu')

#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = r"C:/Users/firerose/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_binary, options=options)


# Using Chrome to access web
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

driver.implicitly_wait(10)
driver.find_element(By.LINK_TEXT, "See bin collection dates for this address").click()

