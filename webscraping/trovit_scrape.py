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
    
    price = parsed_html.find(class_="price")
    parsed_data["Vehicle Price"] = price.text.replace(",", "").strip()
    
    amenities = parsed_html.find(id="amenities")
    list_amenities = amenities.findChild("dl")
    list_amenities = [i for i in list_amenities.contents if i != ' ']
    for i in range(0, len(list_amenities), 2):
        if i + 1 > len(list_amenities):
            break
        key = list_amenities[i].text.strip()
        value = list_amenities[i+1].text.strip()
        if key == "Make":
            key = "Maker"
            parsed_data[key] = value
        elif key == "Year":
            key = "Model Year"
            parsed_data[key] = value
        elif key == "Transmission":
            key = "Transmission Type"
            parsed_data[key] = value
        elif key == "Kilometres":
            value = value.replace(",", "").strip() + " km"
            key = "Mileage"
            parsed_data[key] = value
        elif key == "Fuel Type":
            parsed_data[key] = value

    
    final_data.append(parsed_data)    
    # print(parsed_data)
    json_data = json.dumps(final_data, indent=4)
    
    with open("trovit_data.json", "w") as file:
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

    driver.get("https://cars.trovit.ph/index.php/cod.search_cars/type.0/what_d.truck/sug.0/isUserSearch.1/origin.2")
    
    wait = WebDriverWait(driver, 10)
    assert len(driver.window_handles) == 1

    for i in range (2, 5):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "snippet-image")))
            images = driver.find_elements(By.CLASS_NAME, "snippet-image")
            for image in images:
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "snippet-image")))
                    actions.move_to_element(image).perform()
                    image.click()
                    wait.until(EC.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[1])
                    curr_url = str(driver.current_url)
                    get_data(curr_url)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except Exception as e:
                    driver.switch_to.window(driver.window_handles[0])
                    print(e)
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://cars.trovit.ph/index.php/cod.search_cars/what_d.truck/origin.2/resultsPerPage.25/tracking.%7B%7D/isUserSearch.1/page." + str(i))
            print("Page " + str(i))
        except Exception as e:
            driver.switch_to.window(driver.window_handles[0])
            driver.get("https://cars.trovit.ph/index.php/cod.search_cars/what_d.truck/origin.2/resultsPerPage.25/tracking.%7B%7D/isUserSearch.1/page." + str(i))
            i -= 1
            print(e)


    
    
# https://cars.trovit.ph/index.php/cod.search_cars/what_d.truck/origin.2/resultsPerPage.25/tracking.%7B%7D/isUserSearch.1/page.3
# https://cars.trovit.ph/index.php/cod.search_cars/what_d.truck/origin.2/resultsPerPage.25/tracking.%7B%7D/isUserSearch.1/page.2


navigate()
json_data = json.dumps(final_data, indent=4)
