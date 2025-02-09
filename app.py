import streamlit as st
import pandas as pd
import numpy as np
import selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#from selenium.webdriver import FirefoxOptions

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.log.level = "trace"
browser = Firefox(options=opts)

#opts = FirefoxOptions() #it was working without error

#opts.add_argument("--headless") # the error is here. With this, webpage does not start
#opts.log.level = "trace"
#browser = webdriver.Firefox(options=opts)

st.header("Welcome to my bin collection webapp")
#browser = webdriver.Firefox()

browser.get('https://online.cheshireeast.gov.uk/mycollectionday/')
#assert 'Yahoo' in browser.title

#elem = browser.find_element(By.NAME, 'p')  # Find the search box
#elem.send_keys('seleniumhq' + Keys.RETURN)
st.write("Has the web opened?")
#browser.quit()
