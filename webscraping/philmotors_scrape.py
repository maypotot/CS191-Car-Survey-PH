import time
from typing import final
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
from urllib import request 
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.chrome.options import Options


final_data = list()

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

def get_truck_info(url: str):
    parsed_data = dict()

    resp = request.urlopen(url)
    html = resp.read().decode('utf-8')

    parsed_html = BeautifulSoup(html, 'html.parser')
    # with open("test.txt", "w", encoding='utf-8') as file:
    #     try:
    #         file.write(parsed_html.prettify())
    #     except Exception as e:
    #         print(e)

    car_specs = parsed_html.find(class_="car-specs")
    price = parsed_html.find(id="price_chng")
    maker = parsed_html.find(itemprop="manufacturer")
    model = parsed_html.find(itemprop="model")

    parsed_data["Maker"] = maker.text.strip()
    parsed_data["Model"] = model.text.strip()
    parsed_data["Vehicle Price"] = price.text.strip()

    car_specs_contents = car_specs.contents[-2]

    for content in car_specs_contents:
        if content == "\n":
            continue
        if ":" in content.text:
            parsed_content = content.text.split(":")
            truck_spec_key = parsed_content[0].strip().replace("?", "")
            if truck_spec_key == "Engine":
                truck_spec_key = "Engine Type"
                parsed_data[truck_spec_key] = parsed_content[1].strip()  
            elif truck_spec_key == "Transmission":
                truck_spec_key = "Transmission Type"
                parsed_data[truck_spec_key] = parsed_content[1].strip()  
            
    for spec in car_specs:
        if "Year" in spec.text:
            parsed_data["Model Year"] = spec.text.strip()
        elif "Fuel" in spec.text:
            parsed_data["Fuel Type"] = spec.text.strip()
        elif "mileage" in spec.text:
            parsed_data["Mileage"] = spec.text.strip()

    final_data.append(parsed_data)

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

    driver.get("https://www.philmotors.com/Truck")
    
    
    
    actions = ActionChains(driver)
    

    for i in range(2, 24):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "hidelink")))
        truck_links = driver.find_elements(By.CLASS_NAME, "hidelink")

        for j in range(len(truck_links)):
            try:
                truck_links[j].click()
                get_url = driver.current_url
                get_truck_info(str(get_url))
                driver.back()
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "hidelink")))
                truck_links = driver.find_elements(By.CLASS_NAME, "hidelink")
            except Exception as e:
                print(e)
        
        # scroll_up(driver)
        # next_page = driver.find_element(By.CLASS_NAME, "ajaxurl")
        # time.sleep(0.1)
        # actions.move_to_element(next_page).perform()
        # time.sleep(0.5)
        # next_page.click()
        
        
        driver.get("https://www.philmotors.com/Truck/sale-" + str(i))
        print("Page" + str(i))


navigate()
json_data = json.dumps(final_data, indent=4)
    
with open("philmotors_data.json", "w") as file:
    try:
        file.write(json_data)
    except Exception as e:
        print(e)