with some elements being hidden or covered by others when you're attempting to click on them. I also see a few points that could be optimized or corrected.

Here's a checklist of issues to address:

Waiting for elements to become clickable: You're currently using implicitly_wait(10), which might not be enough to ensure that all elements are fully loaded and clickable before interacting with them. It's better to use an explicit wait to ensure the element you're trying to click is actually ready.

Handling the ElementClickInterceptedException: You might encounter this error if something (like a modal, overlay, or even the page itself) is blocking the element you're trying to click. We can use JavaScript to scroll the element into view or perform the click directly using JavaScript.

Headless mode: Sometimes, running Selenium in headless mode (without the browser GUI) can cause issues with rendering or interaction, especially with dynamically loaded elements. You might want to test in non-headless mode to see if the problem is related to the rendering.

Here's the revised version of your script with these adjustments:

python
Copiar código
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
