from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import gc

# Selenium Setup
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://motortrade.com.ph/motorcycle-type/regular-bike/")

scraped_data = []

def scrape_listing(url):
    """Extract details from an individual motorcycle listing"""
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        listing = BeautifulSoup(driver.page_source, "html.parser")

        name = listing.find("h1", class_="vehicle-title").text.strip()
        transmission_element = driver.find_element(By.CLASS_NAME, "transmission")
        transmission = transmission_element.text.strip()
        
        price_element = driver.find_element(By.CLASS_NAME, "pcd-pricing")
        price = price_element.text.strip()

        parts = name.split()
        maker = parts[0] if len(parts) > 0 else ""
        model = " ".join(parts[1:]) if len(parts) > 1 else ""

        scraped_data.append({
            "Maker": maker,
            "Model": model,
            "Transmission": transmission,
            "Price": price
        })
       

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

def scrape_all_pages():
    """Loop through all pages and extract listings"""
    while True:
        time.sleep(5)  # Allow time for page to load

        # Extract listing URLs on the current page
        listing_cards = driver.find_elements(By.CLASS_NAME, "Vehicle-Feature-Image")
        listing_urls = [listing.find_element(By.TAG_NAME, "a").get_attribute("href") for listing in listing_cards if listing.find_element(By.TAG_NAME, "a")]

        # Scrape each listing
        for url in listing_urls:
            scrape_listing(url)

        # Try to find and click the "Next" button
        try:
            next_button = driver.find_element(By.CLASS_NAME, "nextpostslink")
            next_button.click()
        except:
            print("No more pages found. Scraping complete.")
            break  # Exit loop if no more pages

# Start the full scraping process
scrape_all_pages()

driver.quit()

# Save data to JSON
with open("webscraping/motortrade.json", "w", encoding="utf-8") as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print(f"✅ Scraping Completed! Total Listings: {len(scraped_data)}")
