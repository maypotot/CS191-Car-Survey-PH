from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re

# Initialize WebDriver
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.carmudi.com.ph/motorcycles/")

scraped_data = []
time.sleep(10)

def load_all_listings():
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='filters__nav']/div/div[2]/div[2]/div[3]/div[3]/div[2]/a"))
            )
    
            # Click the button
            load_more_button.click()
            print("✅ Clicked 'Load More' button successfully!")

        except:
            print("No more 'Load More' button found.")
            break

def extract_price(price_text):
    # Remove anything after the first newline
    price_text = price_text.split("\n")[0]

    # Extract all numbers considering full prices (handles both single price and range)
    prices = re.findall(r"\d{1,3}(?:,\d{3})*", price_text)  # Match full numbers including commas
    prices = [int(price.replace(",", "")) for price in prices]  # Convert to integers

    # If it's a range, return the average; otherwise, return the single price
    return sum(prices) // len(prices) if prices else None

def scrape_page():
    # Find all listing elements
    listings = driver.find_elements(By.CLASS_NAME, "new__car__details")

    for index, listing in enumerate(listings, start=1):
        try:
            # Extract name
            name_element = listing.find_element(By.CSS_SELECTOR, ".new__car__title.d-flex.align-items-center")
            name = name_element.text.strip()

            # Extract price
            price_element = listing.find_element(By.CSS_SELECTOR, ".new__car__price")
            price_text = price_element.text.strip()
            price = extract_price(price_text)

            # Process name to extract maker & model
            name_parts = name.split()
            maker = name_parts[1] if len(name_parts) > 1 else ""
            model = name_parts[2] if len(name_parts) > 2 else ""
            variant = " ".join(name_parts[3:]) if len(name_parts) > 3 else ""

            # Store data
            scraped_data.append({
                "Maker": maker,
                "Model": model,
                "Variant": variant,
                "Price": price
            })

            print({
                "Maker": maker,
                "Model": model,
                "Variant": variant,
                "Price": price
            })

        except Exception as e:
            print(f"⚠️ Error extracting listing: {e}")
            continue

def filter_valid_prices(data):
    """Remove entries with a null (None) price."""
    return [entry for entry in data if entry.get("Price") is not None and entry["Price"] >= 1000]


load_all_listings()
# Close WebDriver
scrape_page()
driver.quit()

final_data = filter_valid_prices(scraped_data)

with open("webscraping/data_dump/carmudi.json", "w", encoding="utf-8") as json_file:
        json.dump(final_data, json_file, indent=4, ensure_ascii=False)

print(f"✅ Scraping Completed! Total Listings: {len(scraped_data)}")
