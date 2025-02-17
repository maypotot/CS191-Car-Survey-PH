from ast import parse
from calendar import c
from os import replace
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
from urllib import request 
from urllib.request import Request, urlopen
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.chrome.options import Options


final_data = list()
counter : int = 0

def scroll_up(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, 0);")

        # Wait to load the page.
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        break

def get_data(url: str):
    parsed_data = dict()
    
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    html = urlopen(req).read().decode('utf-8')

    parsed_html = BeautifulSoup(html, 'html.parser')
    
    price = parsed_html.find("span", class_="priceTag")
    parsed_data["Vehicle Price"] = price.text.replace("PHP,.", "").strip()
    
    detail_keys = parsed_html.find_all("small")[:3]
    detail_values = parsed_html.find_all("h6")[:3]
    for i in range(len(detail_keys)):
        parsed_data[detail_keys[i].text] = detail_values[i].text.replace("kms", "").replace("KMS", "").replace("T", "").strip().capitalize()
    
    title = parsed_html.find("h5", class_="mb-0 heading-text")
    title = title.text.split()
    parsed_data["Maker"] = title[0]
    parsed_data["Model"] = " ".join(title[1:])
    
    final_data.append(parsed_data)    
    json_data = json.dumps(final_data, indent=4)
    
    with open("rfshop_data.json", "w") as file:
        try:
            file.write(json_data)
        except Exception as e:
            print(e)

def navigate():
    
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("--disable-notifications")
    option.add_argument("--disable-extensions")

    option.add_argument("--start-maximized")
    option.add_experimental_option("useAutomationExtension", False)
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
            # with 2 should disable notifications
        },
    )

    # thumbnails: list = []
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(options=option, service=service)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)

    driver.get("https://rfshop.com.ph/product/search?keyword=truck&cat=1&brand=undefined&location=undefined&region=&price=")
    
    for i in range(2, 4):
        scroll_up(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-img-top")))
        truck_list = driver.find_elements(By.CLASS_NAME, "card-img-top")
        
        for j in range(len(truck_list)):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-img-top")))
            truck_list = driver.find_elements(By.CLASS_NAME, "card-img-top")
            actions.move_to_element(truck_list[j]).perform()
            truck_list[j].click()
            curr_url = str(driver.current_url)
            get_data(curr_url)
            driver.back()
        next_button = driver.find_element(By.XPATH, f"//a[text()='{i}']")
        next_button.click()
        print("Page " + str(i))
        time.sleep(1)
    
    # for i in range(2,7):
    #     for truck in truck_list:
    #         actions.move_to_element(truck).perform()
    #         truck.click()
    #         curr_url = str(driver.current_url)
    #         # get_data(curr_url)
    #         driver.back()
    #         time.sleep(2)
    #     driver.get("https://automart.ph/search?car_types=Utility%20/%20FB&page=2" + str(i))
    #     print("Page " + str(i))
    #     time.sleep(1)
    
    
    


    
    
    



navigate()
json_data = json.dumps(final_data, indent=4)
