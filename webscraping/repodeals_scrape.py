from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
from urllib import request 
from selenium.webdriver.common.action_chains import ActionChains


def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

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

def navigate():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    driver.get("https://repodeals.com.ph/motorcycles")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "img-responsive")))

    motor_links = driver.find_elements(By.CLASS_NAME, "img-responsive")
    thumbnails = driver.find_elements(By.CLASS_NAME, "thumbnail")

    for i in range(len(thumbnails)):
        # print(thumbnails[i].get_attribute("src"))
        try:
            # driver.execute_script("arguments[0].scrollIntoView();", thumbnails[i-1])
            # ActionChains(driver)\
            # .scroll_to_element(thumbnails[i])\
            # .perform()
            thumbnails[i].click()
            get_url = driver.current_url    
            # get_truck_info(str(get_url))
            driver.back()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "img-responsive")))
            thumbnails = driver.find_elements(By.CLASS_NAME, "img-responsive")
        except Exception as e:
            print(e)

navigate()
