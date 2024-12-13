
import streamlit as st
import pandas as pd
import numpy as np
import selenium #to navigate through the webb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


#word="casa"
#st.write("**Si quieres conocer el significado de la palabra, pulsa en el link**")
#definicionrae="[link]" + "(https:" + "//dle.rae.es/" + word + ")"
#st.write("**Si quieres conocer el significado RAE de la palabra, pulsa en el**", definicionrae)
st.header("Welcome to my bin collection webapp")

# Using Chrome to access web
driver = webdriver.Chrome()
# Open the website
#driver.get('https://canvas.case.edu')
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

#driver.find_element(By.TAG_NAME, 'See bin collection dates for this address').click()
#driver.find_element(By.LINK_TEXT, "See bin collection dates for this address").click()
#driver.find_element('.search-button-form').click()

# Find login button
#login_button2 = driver.find_element(By.ID, 'btn-search-form')
# Click login
#login_button.click()