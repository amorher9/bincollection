from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from selenium.webdriver import FirefoxOptions

opts = FirefoxOptions()
opts.add_argument("--headless")
browser = webdriver.Firefox(options=opts)

st.header("Welcome to my bin collection webapp")
#browser = webdriver.Firefox()

browser.get('https://online.cheshireeast.gov.uk/mycollectionday/')
assert 'Yahoo' in browser.title

#elem = browser.find_element(By.NAME, 'p')  # Find the search box
#elem.send_keys('seleniumhq' + Keys.RETURN)

browser.quit()
