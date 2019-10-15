from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path="C:\\Program Files\\Git\\usr\\bin\\chromedriver.exe")
driver.get("http://www.python.org")
assert "Python" in driver.title
time.sleep(2)
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
