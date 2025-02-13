from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from bs4 import BeautifulSoup

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.carousell.ph/motorcycles-for-sale/h-2652/")

show_listings = driver.find_element(By.CSS_SELECTOR, "[role='submitButton'][type='submit']")
show_listings.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "D_pt"))
)

num_listings = len(driver.find_elements(By.CLASS_NAME, "D_pt"))
scraped_data = []  # Store scraped motorcycle data

for i in range(num_listings):
    # Re-fetch the listing elements to avoid stale element reference
    listing_cards = driver.find_elements(By.CLASS_NAME, "D_pt")
    
    if i >= len(listing_cards):  # If the number of listings changed
        break
    try:
        listing_cards[i].click()
        time.sleep(5)  # Wait for the listing page to load

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        spec_containers = soup.find_all('div', class_='D_aNU')
        spec_container = spec_containers[1] if len(spec_containers) > 1 else None

        motorcycle_specs = {}  # Dictionary to store specs

        if spec_container:
            for spec in spec_container.find_all("div", recursive=False):
                spec_type = spec.find('p').text.strip() if spec.find('p') else "Unknown Spec"
                spec_value = spec.find('span').text.strip() if spec.find('span') else "Unknown Value"
                motorcycle_specs[spec_type] = spec_value
        else:
            print("spec container not found")

        # Store data
        scraped_data.append(motorcycle_specs)
        print(f"Scraped Listing {i+1}: {motorcycle_specs}")

        driver.back()
        time.sleep(3)  # Wait for the listings page to reload
    except Exception as e:
        print(f"Error navigating listing {i+1}: {e}")

print("\nFinal Scraped Data:")
for idx, data in enumerate(scraped_data):
    print(f"Listing {idx+1}: {data}")

show_listings = driver.find_element(By.CLASS_NAME, "D_kr D_kM D_kE D_kz D_kQ D_KI")
show_listings.click()

time.sleep(10)
driver.quit()

#D_kr D_kM D_kE D_kz D_kQ D_KI