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
    
    price = parsed_html.find(class_="attribute price").text.replace(".", ",")
    parsed_data["Vehicle Price"] = price.replace("PHP", "").replace(",", "").replace("\u20b1", "").strip()
    
    characteristics = parsed_html.find_all(class_="att_description")
    for characteristic in characteristics:
        split_str = characteristic.text.split(":")
        key = split_str[0].strip()
        value = split_str[1].strip()
        if key == "Make":
            parsed_data["Maker"] = value
        elif key == "Year":
            parsed_data["Model Year"] = value
        elif key == "Type of Fuel":
            parsed_data["Fuel Type"] = value
        else:
            parsed_data[key] = value
        
    description = parsed_html.find(class_="description")
    for detail in description.findChildren("div"):
        split_str = detail.text.split(":")
        key = split_str[0].strip()
        value = split_str[1].strip()
        if key == "Model":
            parsed_data[key] = value
        elif key == "Mileage":    
            parsed_data[key] = value.replace("Mileage", "").replace(".", "").strip()
        elif key == "Type of fuel":
            parsed_data["Fuel Type"] = value
        elif key == "Transmission":
            parsed_data["Transmission Type"] = value

    
    final_data.append(parsed_data)    
    json_data = json.dumps(final_data, indent=4)
    
    with open("waa2_data.json", "w") as file:
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

    driver.get("https://cars.waa2.ph/search?q=truck&list_type=row&page=1")
    
    wait = WebDriverWait(driver, 10)
    assert len(driver.window_handles) == 1
    
    for i in range(2, 20):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "picture")))
            images = driver.find_elements(By.CLASS_NAME, "picture")
            for image in images:
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "picture")))
                    actions.move_to_element(image).perform()
                    image.click()
                    wait.until(EC.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[1])
                    curr_url = str(driver.current_url)
                    get_data(curr_url)
                    driver.switch_to.window(driver.window_handles[0])
                except Exception as e:
                    driver.switch_to.window(driver.window_handles[0])
                    print(e)
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://cars.waa2.ph/search?q=truck&list_type=row&page=" + str(i))
        except Exception as e:
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://cars.waa2.ph/search?q=truck&list_type=row&page=" + str(i))
            i -= 1
            print(e)
        print("I am on page " + str(i))


    
    
    



navigate()
json_data = json.dumps(final_data, indent=4)
