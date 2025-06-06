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
        time.sleep(1)  # Wait for the page to load

        listing = BeautifulSoup(driver.page_source, "html.parser")

        # Extract name
        name = listing.find("h1", class_="vehicle-title")
        name = name.text.strip() if name else "Unknown"

        # Extract transmission (handle missing cases)
        try:
            transmission_element = driver.find_element(By.CLASS_NAME, "transmission")
            transmission = transmission_element.text.strip()
        except:
            transmission = ""

        # Extract price (handle missing cases)
        try:
            price_element = driver.find_element(By.CLASS_NAME, "pcd-pricing")
            price = price_element.text.strip()
        except:
            price = "Not Available"

        # Extract maker and model
        parts = name.split()
        maker = parts[0] if len(parts) > 0 else "Unknown"
        model = " ".join(parts[1:]) if len(parts) > 1 else "Unknown"

        # Add to scraped data
        scraped_data.append({
            "Maker": maker,
            "Model": model,
            "Transmission": transmission,
            "Price": price
        })

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

    finally:
        driver.back()  # Go back to listings page
        time.sleep(1)  # Allow time for the page to reload
       

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
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            next_button = driver.find_element(By.CLASS_NAME, "nextpostslink")
            next_link = next_button.get_attribute("href")
            print(next_link)
            driver.get(next_link)
        except:
            print("No more pages found. Scraping complete.")
            break  # Exit loop if no more pages

# Start the full scraping process
scrape_all_pages()

driver.quit()

# Save data to JSON
with open("webscraping/motortrade_regular.json", "w", encoding="utf-8") as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print(f"✅ Scraping Completed! Total Listings: {len(scraped_data)}")
