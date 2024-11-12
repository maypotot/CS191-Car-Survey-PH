from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
from urllib import request 


def get_truck_info(url: str):
    truck_data = dict()
    parsed_data = dict()

    resp = request.urlopen(url)
    html = resp.read().decode('utf-8')

    parsed_html = BeautifulSoup(html, 'html.parser')
    with open("test.txt", "w", encoding='utf-8') as file:
        try:
            file.write(parsed_html.prettify())
        except Exception as e:
            print(e)

    car_specs = parsed_html.find(class_="car-specs")
    price = parsed_html.find(id="price_chng")
    manufacturer = parsed_html.find(itemprop="manufacturer")
    model = parsed_html.find(itemprop="model")

    parsed_data["manufacturer"] = manufacturer.text.strip()
    parsed_data["model"] = model.text.strip()
    parsed_data["price"] = price.text.strip()

    car_specs_contents = car_specs.contents[-2]

    for content in car_specs_contents:
        if content == "\n":
            continue
        if ":" in content.text:
            parsed_content = content.text.split(":")
            parsed_data[parsed_content[0].strip().replace("?", "")] = parsed_content[1].strip()  
    truck_data.update(parsed_data)
    print(truck_data)


driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get("https://www.philmotors.com/Truck")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hidelink")))

truck_links = driver.find_elements(By.CLASS_NAME, "hidelink")


for i in range(len(truck_links)):
    try:
        truck_links[i].click()
        get_url = driver.current_url
        get_truck_info(str(get_url))
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hidelink")))
        truck_links = driver.find_elements(By.CLASS_NAME, "hidelink")
    except Exception as e:
        print(e)

