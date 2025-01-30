from operator import ne
from sys import executable
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
from urllib import request 
from selenium.webdriver.common.action_chains import ActionChains
import json


final_data = list()

def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height
        
        
def collect_specs(parsed_html: BeautifulSoup, parsed_data: dict, id: str):
    needed_motor_specs = ["Fuel Type", "Transmission Type"]
    specs = parsed_html.find(id="tab-feature" + id + "-panel")
    try:
        li_list = specs.find_all("li")
    except Exception as e:
        print(e)
        return
    for li in li_list:
        details = li.find_all("span")
        key = details[0].text.strip()
        data = details[1].text.strip()
        if key in needed_motor_specs: 
            parsed_data[key] = data
        
def get_info(url: str, driver: webdriver.Chrome):
    parsed_data = dict()

    resp = request.urlopen(url)
    html = resp.read().decode('utf-8')
    parsed_html = BeautifulSoup(html, 'html.parser')
    # with open("test.txt", "w", encoding='utf-8') as file:
    #     try:
    #         file.write(parsed_html.prettify())
    #     except Exception as e:
    #         print(e)

    vehicle_info = parsed_html.find(class_="overview-info card-panel")
    try:
        parsed_data["vehicle_name"] = vehicle_info.find("h1").text.strip()
        parsed_data["vehicle_price"] = vehicle_info.find(class_="vh-price").text.strip()[1:]
    except Exception as e:
        print(e)
        return
    
    specs_button = driver.find_element(By.LINK_TEXT, "Specs")
    specs_button.click()
    url = str(driver.current_url)
    
    resp = request.urlopen(url)
    html = resp.read().decode('utf-8')
    parsed_html = BeautifulSoup(html, 'html.parser')
    
    
    collect_specs(parsed_html, parsed_data, "0")
    
    for i in range(1, 7):
        if i == 6 or i == 2:
            try:
                specs_button = driver.find_element(By.ID, "tab-feature" + str(i))
                specs_button.click()    
            except Exception as e:
                pass
        
        collect_specs(parsed_html, parsed_data, str(i))

    # put data into json file
    final_data.append(parsed_data)
    json_data = json.dumps(final_data, indent=4)
    
    with open("zigwheels_data.json", "w") as file:
        try:
            file.write(json_data)
        except Exception as e:
            print(e)
    file.close()
    

    
def navigate():
    thumbnails: list = []
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.set_window_size(1024, 600)
    driver.maximize_window()

    driver.get("https://www.zigwheels.ph/best-motorcycles")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "splide05-slide01")))

    for j in range(2):
        for i in range(5, 53):
            concat_str = "splide"
            if i == 3 or i == 4:
                continue
            print(i)
            scroll_down(driver)
            if i < 10:
                concat_str = concat_str + "0" 
            element_to_find = concat_str + str(i) + "-slide01"
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_to_find)))
                thumbnail = driver.find_element(By.ID, element_to_find)
                actions = ActionChains(driver)
                actions.move_to_element(thumbnail).perform()
                thumbnail.click()
                time.sleep(2)
                get_url = driver.current_url  
                print(get_url)
                get_info(str(get_url), driver)
                time.sleep(2)
                driver.execute_script("window.history.go(-2)")
            except Exception as e:
                print(e)
        next_button = driver.find_element(By.ID, "view-more-btn")
        actions = ActionChains(driver)
        actions.move_to_element(next_button).perform()
        next_button.click()  
        
        
open('file.txt', 'w').close()
navigate()