from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Initialize WebDriver
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.carmudi.com.ph/motorcycles/")

scraped_data = []
time.sleep(10)
def load_all_listings():
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-offer"))
            )
    
            # Click the button
            load_more_button.click()
            print("✅ Clicked 'Load More' button successfully!")

        except:
            print("No more 'Load More' button found.")
            break


def scrape_page():
    # Find all listing elements
    listings = driver.find_elements(By.CLASS_NAME, "new__car__details")

    for index, listing in enumerate(listings, start=1):
        try:
            # Extract name
            name_element = listing.find_element(By.XPATH, "//*[@id='filters__nav']/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]")
            name = name_element.text.strip()

            # Extract price
            price_element = listing.find_element(By.XPATH, "//*[@id='filters__nav']/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[2]")
            price = price_element.text.strip()

            # Process name to extract maker & model
            name_parts = name.split()
            maker = name_parts[1] if len(name_parts) > 1 else ""
            model = " ".join(name_parts[2:]) if len(name_parts) > 2 else ""

            # Store data
            scraped_data.append({
                "Maker": maker,
                "Model": model,
                "Price": price
            })

            print({
                "Maker": maker,
                "Model": model,
                "Price": price
            })

        except Exception as e:
            print(f"⚠️ Error extracting listing: {e}")
            continue


load_all_listings()
# Close WebDriver
#scrape_page()
time.sleep(10)
driver.quit()


with open("webscraping/carmudi.json", "w", encoding="utf-8") as json_file:
        json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print(f"✅ Scraping Completed! Total Listings: {len(scraped_data)}")
