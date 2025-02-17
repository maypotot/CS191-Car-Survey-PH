from ast import parse
from calendar import c
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
    
    price = parsed_html.find_all("p", class_="flex flex-1 items-center")[0].text.replace("₱", "").replace(",", "").strip()
    parsed_data["Vehicle Price"] = price
    
    title = parsed_html.find("h1", class_="text-h3").text.split()
    parsed_data["Model Year"] = title[0]
    parsed_data["Maker"] = title[1]
    parsed_data["Model"] = title[2]
    
    div = parsed_html.find("div", class_="flex flex-col gap-6")
    details = div.find_all("div")[1].find_all("p", class_="capitalize")
    for i in range(len(details)):
        if i == 0:
            if details[i].text == "MT":
                value = "Manual"
            else:
                value = "Automatic"
            parsed_data["Transmission Type"] = value
        if i == 1:
            parsed_data["Fuel Type"] = details[i].text
        if i == 2:
            parsed_data["Mileage"] = details[i].text
    
    
    
    final_data.append(parsed_data)    
    json_data = json.dumps(final_data, indent=4)
    
    with open("automart_data.json", "w") as file:
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

    driver.get("https://automart.ph/search?car_types=Utility%20/%20FB")
    
    class_to_find = "//a[@class='flex h-full flex-1 bg-white p-xs lg:flex-col lg:px-0 lg:pt-0']"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, class_to_find)))
    truck_list = driver.find_elements(By.XPATH, class_to_find)
    for i in range(2,7):
        for j in range(len(truck_list)):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, class_to_find)))
            truck_list = driver.find_elements(By.XPATH, class_to_find)
            truck = truck_list[j]
            actions.move_to_element(truck).perform()
            actions.scroll_by_amount(0, 250)
            truck.click()
            curr_url = str(driver.current_url)
            get_data(curr_url)
            driver.back()
            time.sleep(2)
        driver.get("https://automart.ph/search?car_types=Utility%20/%20FB&page=2" + str(i))
        print("Page " + str(i))
        time.sleep(1)
    
    
    


    
    
    



navigate()
json_data = json.dumps(final_data, indent=4)
