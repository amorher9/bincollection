import streamlit as st
import pandas as pd
import numpy as np
import selenium #to navigate through the webb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from selenium.webdriver.chrome.service import Service


#According to IA:
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import seleniumbase as sb

st.header("Welcome to my bin collection webapp")

service=Service()

options=webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# Open the website

driver.get('https://online.cheshireeast.gov.uk/mycollectionday/')
