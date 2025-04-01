from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json
import gc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

showmorelistings_selector = "D_lk M_kM D_lF D_lx M_kZ D_ls M_kU D_lJ D_IL"
thumbnailclass = "D_o_"
linkclass = "D_in "

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


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(options=option, service=service)

driver.get("https://www.carousell.ph/trucks-for-sale/q/?searchId=ZT2aZM")
actions = ActionChains(driver)


time.sleep(3)

# Scroll amount
scrollamt = 4420

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

def load_all_listings():
    while True:
        try:
            scroll_down(driver)
            scroll_up(driver)
            show_more_listings = driver.find_element(By.CSS_SELECTOR, ".D_lk.D_lF.D_lx.D_ls.D_lJ.D_IL")
            actions.move_to_element(show_more_listings).perform()
            show_more_listings.click()
            print("More listings clicked!")
        except Exception as e:
            print("No more 'Load More' button found.")
            break

load_all_listings()

driver.execute_script("window.scrollTo(0, 0);")

truck_selector = "D_oO"

WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.CLASS_NAME, truck_selector))
)

scraped_data = []

listing_cards = driver.find_elements(By.CLASS_NAME, truck_selector)
print(len(listing_cards))

for i in range(len(listing_cards)):
    try:
        load_all_listings()
        listing_cards = driver.find_elements(By.CLASS_NAME, truck_selector)
        truck = listing_cards[i]
        actions.move_to_element(truck).perform()
        truck.click()
        driver.back()
        time.sleep(0.5)  

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        spec_containers = soup.find_all('div', class_='D_aLp')
        spec_container = spec_containers[1] if len(spec_containers) > 1 else None
        
        price_element = soup.find('p', {'data-testid': 'new-listing-details-page-desktop-text-price'})
        price = price_element.text.strip() if price_element else "Unknown Price"


        motorcycle_specs = {}

        if spec_container:
            for spec in spec_container.find_all("div", recursive=False):
                spec_type = spec.find('p').text.strip() if spec.find('p') else "Unknown Spec"
                spec_value = spec.find('span').text.strip() if spec.find('span') else "Unknown Value"
                motorcycle_specs[spec_type] = spec_value

        motorcycle_specs["Price"] = price
        scraped_data.append(motorcycle_specs)
        print(f"Scraped Listing {i+1}: {motorcycle_specs}")

        gc.collect()
        driver.delete_all_cookies()  # Free memory
    except Exception as e:
        continue

driver.quit()

json_data = json.dumps(scraped_data, indent=4)

with open("carousell_data.json", "w") as file:
    file.write(json_data)

print("✅ Scraping Completed Successfully!")
