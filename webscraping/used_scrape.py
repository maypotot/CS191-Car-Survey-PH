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

def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")



    # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page.
    
    time.sleep(1)
    
def get_data(url: str):
    parsed_data = dict()
    
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    html = urlopen(req).read().decode('utf-8')

    parsed_html = BeautifulSoup(html, 'html.parser')
    price_div = parsed_html.find("div", class_="post-price")
    price = price_div.find("span").text
    parsed_data["Vehicle Price"] = price.replace("PHP", "").replace(",", "").strip()[2:]
    print(parsed_data)
    final_data.append(parsed_data)    
    json_data = json.dumps(final_data, indent=4)
    
    with open("used_data.json", "w") as file:
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

    driver.get("https://used.com.ph/s?cat=0&q=truck&_l=&l=")
    
    image_class = "pr-img"
    close_class =  "ns-lqkp3-e-17"
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, image_class)))
    truck_list = driver.find_elements(By.CLASS_NAME, image_class)
    print(len(truck_list))
    
    for i in range(1, 4):
        if i > 1:
            driver.get("https://used.com.ph/s/truck?pg="+ str(i))
        for j in range(len(truck_list)):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, image_class)))
            truck_list = driver.find_elements(By.CLASS_NAME, image_class)
            truck = truck_list[j]
            actions.move_to_element(truck).perform()
            driver.execute_script("window.scrollBy(0, 200)")
            truck.click()
            time.sleep(6)
            try:
                close_button = driver.find_element(By.CLASS_NAME, close_class)
                close_button.click()
            except Exception as e:
                pass
            time.sleep(12)
            curr_url = str(driver.current_url)
            get_data(curr_url)
            driver.back()
        print("Page " + str(i))
    # next_button = driver.find_element(By.XPATH, f"//a[text()='{i}']")
    # next_button.click()
    # print("Page " + str(i))
    # time.sleep(1)
    
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
