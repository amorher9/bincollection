import streamlit as st
import pandas as pd
import numpy as np
import selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os

from selenium.webdriver import FirefoxOptions

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

URL = ""
TIMEOUT = 20

st.title("Test Selenium")

firefoxOptions = Options()
firefoxOptions.add_argument("--headless")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(
    options=firefoxOptions,
    service=service,
)




#opts = FirefoxOptions() #it was working without error

#opts.add_argument("--headless") # the error is here. With this, webpage does not start
##opts.log.level = "trace"
#browser = webdriver.Firefox(options=opts)

#st.header("Welcome to my bin collection webapp")
##browser = webdriver.Firefox()

browser.get('https://online.cheshireeast.gov.uk/mycollectionday/')
#assert 'Yahoo' in browser.title

#elem = browser.find_element(By.NAME, 'p')  # Find the search box
#elem.send_keys('seleniumhq' + Keys.RETURN)
st.write("Has the web opened?")
#browser.quit()
