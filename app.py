import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Streamlit header
st.header("Welcome to my bin collection webapp")

# Set up Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # Comment out if you want to see the browser GUI

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the website
driver.get('https://online.cheshireeast.gov.uk/mycollectionday/')

# Wait until the postcode input is present and send keys
postcode_elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'postcode'))
)
postcode_elem.send_keys('SK118ED')

# Wait until the property name input is present and send keys
property_elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'propertyname'))
)
property_elem.send_keys('9')

# Wait until the search button is clickable and click it
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'btn-search-form'))
)
login_button.click()

# Wait for the link to be clickable, then scroll into view and click
bin_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "See bin collection dates for this address"))
)

# Scroll the link into view to ensure it is clickable
driver.execute_script("arguments[0].scrollIntoView(true);", bin_link)

# Click the link
bin_link.click()

# Optional: Wait for the next page or action to complete
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'some_element_on_next_page')))

# Always close the driver after use
driver.quit()
