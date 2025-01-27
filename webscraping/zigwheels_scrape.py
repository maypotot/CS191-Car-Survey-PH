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

def collect_specs(parsed_html: BeautifulSoup, parsed_data: dict, id: str):
    needed_motor_specs = ["Fuel Type", "Transmission Type"]
    specs = parsed_html.find(id="tab-feature" + id + "-panel")
    li_list = specs.find_all("li")
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
    parsed_data["vehicle_name"] = vehicle_info.find("h1").text.strip()
    parsed_data["vehicle_price"] = vehicle_info.find(class_="vh-price").text.strip()
    
    
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
                print(e)
        
        collect_specs(parsed_html, parsed_data, str(i))

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

    driver.get("https://www.zigwheels.ph/best-motorcycles")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "splide05-slide01")))


    for i in range(5, 17):
        concat_str = "splide"
        if i < 10:
            concat_str = concat_str + "0" 
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, concat_str + str(i) + "-slide01")))
        thumbnail = driver.find_element(By.ID, concat_str + str(i) + "-slide01")
        # print(i)
        try:
            thumbnail.click()
            time.sleep(2)
            get_url = driver.current_url    
            get_info(str(get_url), driver)
            time.sleep(2)
            driver.execute_script("window.history.go(-2)")
        except Exception as e:
            print(e)

open('file.txt', 'w').close()
navigate()