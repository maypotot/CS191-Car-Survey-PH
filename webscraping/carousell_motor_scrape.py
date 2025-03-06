from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json
import gc

showmorelistings_selector = ".D_ko.D_kJ.D_kA.D_kw.D_kN.D_Lm"
thumbnailclass = "D_o_"
linkclass = "D_in "
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.carousell.ph/motorcycles-for-sale/h-2652/")

# Click the initial "Show Listings" button
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "[role='submitButton'][type='submit']"))
).click()

time.sleep(3)

# Scroll amount
scrollamt = 4420

def load_all_listings():
    global scrollamt  
    while True:
        try:
            driver.execute_script(f"window.scrollTo(0, {scrollamt});")
            time.sleep(2)  

            show_more_listings = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, showmorelistings_selector))
            )
            show_more_listings.click()
            time.sleep(3)  

            scrollamt += 4420
        except:
            print("No more 'Load More' button found.")
            break

load_all_listings()

driver.execute_script("window.scrollTo(0, 0);")
time.sleep(5)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, thumbnailclass))
)

scraped_data = []

listing_cards = driver.find_elements(By.CLASS_NAME, linkclass)
listing_urls = [listing.get_attribute("href") for listing in listing_cards if listing.get_attribute("href")]

for i, url in enumerate(listing_urls):
    try:
        if (i <= 10):
            continue
        elif (i%2 == 1):
            continue
        else:
            driver.get(url)  # Open listing directly
            time.sleep(2)  

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
        print(f"Error navigating listing {i+1}: {e}")

driver.quit()

json_data = json.dumps(scraped_data, indent=4)

with open("carousell_data.json", "w") as file:
    file.write(json_data)

print("✅ Scraping Completed Successfully!")
