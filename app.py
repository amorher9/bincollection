
import streamlit as st
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.os_manager import ChromeType


# Set up Streamlit
st.header("Welcome to my bin collection webapp")

# Cache the driver initialization
@st.cache_resource
def get_driver():
    # Set Chrome options
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")  # Uncomment to disable GUI if necessary
    # Initialize Chrome driver
    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
    )

# Get the driver
driver = get_driver()

# Open the website
driver.get('https://online.cheshireeast.gov.uk/mycollectionday/')

# Wait for elements to be present and interact with them
try:
    # Wait for the postcode input field and send keys
    postcode_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'postcode'))
    )
    postcode_elem.send_keys('SK118ED')

    # Wait for the property name input field and send keys
    property_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'propertyname'))
    )
    property_elem.send_keys('6')

    # Find and click the search button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'btn-search-form'))
    )
    login_button.click()

    # Wait for the "See bin collection dates" link and click it
    bin_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "See bin collection dates for this address"))
    )
    
    # Scroll into view and click to avoid ElementClickInterceptedException
    driver.execute_script("arguments[0].scrollIntoView(true);", bin_link)
    bin_link.click()

except Exception as e:
    st.error(f"An error occurred: {e}")
finally:
    # Always close the driver after use (or you can keep it open depending on your use case)
    driver.quit()
