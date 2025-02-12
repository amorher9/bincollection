import streamlit as st
import pandas as pd
import numpy as np
import selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from selenium.webdriver import FirefoxOptions

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
#opts = FirefoxOptions()
#opts.add_argument("--headless")
browser = webdriver.Firefox(options=opts)


opts = FirefoxOptions() #it was working without error

opts.add_argument("--headless") # the error is here. With this, webpage does not start
#opts.log.level = "trace"
browser = webdriver.Firefox(options=opts)

st.header("Welcome to my bin collection webapp")
#browser = webdriver.Firefox()

browser.get('https://online.cheshireeast.gov.uk/mycollectionday/')
#assert 'Yahoo' in browser.title

#elem = browser.find_element(By.NAME, 'p')  # Find the search box
#elem.send_keys('seleniumhq' + Keys.RETURN)
st.write("Has the web opened?")
#browser.quit()
