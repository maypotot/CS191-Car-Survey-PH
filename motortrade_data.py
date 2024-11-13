from sys import executable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
from urllib import request 
from selenium.webdriver.common.action_chains import ActionChains


def get_info(url: str):
    parsed_data = dict()

    resp = request.urlopen(url)
    html = resp.read().decode('utf-8')

    parsed_html = BeautifulSoup(html, 'html.parser')
    with open("test.txt", "w", encoding='utf-8') as file:
        try:
            file.write(parsed_html.prettify())
        except Exception as e:
            print(e)

    price = parsed_html.find(class_="pcd-price")
    vehicle_name = parsed_html.find(id="vehicle-title")
    specifications = parsed_html.find(class_="pcd-specs")  

    parsed_data["price"] = price.text.strip()
    parsed_data["vehicle name"] = vehicle_name.text.strip()

    print(specifications)

    # for content in car_specs_contents:
    #     if content == "\n":
    #         continue
    #     if ":" in content.text:
    #         parsed_content = content.text.split(":")
    #         parsed_data[parsed_content[0].strip().replace("?", "")] = parsed_content[1].strip()  
            

def navigate():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://motortrade.com.ph/motorcycles/?freetxt=&mot-type=regular-bike&price-min=+&post_type=vehicle")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wp-post-image")))

    thumbnails = driver.find_elements(By.CLASS_NAME, "wp-post-image")

    for i in range(len(thumbnails)):
        print(i)
        try:
            thumbnails[i].click()
            get_url = driver.current_url    
            get_info(str(get_url))
            driver.execute_script("window.history.go(-1)")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "wp-post-image")))
            thumbnails = driver.find_elements(By.CLASS_NAME, "wp-post-image")
        except Exception as e:
            print(e)

navigate()
