import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Streamlit app layout
st.title("Open Web Page in Chrome")
st.write("Click the button below to open the webpage in Chrome.")

# Button to trigger browser opening
if st.button("Open My Collection Day Page"):
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Uncomment if you want it to run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open the specified webpage
        driver.get("https://online.cheshireeast.gov.uk/mycollectionday/")
        st.success("Webpage opened successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.quit()
