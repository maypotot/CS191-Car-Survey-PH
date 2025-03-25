from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json
import gc

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.carmudi.com.ph/motorcycles/")

def load_all_listings():
    while True:
        try:
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-offer mb-30"))
            )

            load_more_button = driver.find_element(By.CLASS_NAME, "btn-offer mb-30")
            load_more_link = load_more_button.get_attribute("href")
            driver.get(load_more_link)

        except:
            print("No more 'Load More' button found.")
            break

load_all_listings()