from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import re
import os

# Initialize WebDriver
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://motorcyclecity.com.ph/motorcycles/")

motorcycles = []

def parse_listings(url):
    driver.get(url)
    time.sleep(3)  # Give time for the page to load (adjust as needed)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for listing in soup.find_all("li", class_=re.compile(r"\bproduct\b.*\btype-product\b|\btype-product\b.*\bproduct\b")):
        name_element = listing.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price_text = listing.find("span", class_="woocommerce-Price-amount").text.strip()
        price = int(re.sub(r"[^0-9]", "", price_text))/100

        parts = name_element.split()
        maker = parts[0] if len(parts) > 0 else ""

        # Remove any text inside parentheses (the variant)
        model = " ".join(parts[1:])
        model = re.sub(r"\s*\(.*?\)", "", model).strip()  # Remove variants
        variant_match = re.search(r"\((.*?)\)", name_element)
        variant = variant_match.group(1) if variant_match else ""

        motorcycles.append({
            "Maker": maker,
            "Model": model,
            "Variant": variant,
            "Mileage": -1,
            "Year": -1,
            "Price": price
        })

        print({
            "Maker": maker,
            "Model": model,
            "Price": price
        })

def parse_brands():
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "elementor-widget-container"))
    )
    
    listing_cards = driver.find_elements(By.CSS_SELECTOR, '[data-widget_type="image.default"]')
    
    if listing_cards:
        listing_urls = [
            card.find_element(By.TAG_NAME, "a").get_attribute("href")
            for card in listing_cards if card.find_elements(By.TAG_NAME, "a")
        ]

        for url in listing_urls:  # FIXED: Removed enumerate()
            parse_listings(url)
    else:
        print("Element not found")

# Ensure output directory exists
output_dir = "webscraping/data_dump"
os.makedirs(output_dir, exist_ok=True)

# Run scraping functions
parse_brands()

# Save to JSON file
with open(f"{output_dir}/motorcyclecity_motorcycles.json", "w", encoding="utf-8") as f:
    json.dump(motorcycles, f, ensure_ascii=False, indent=4)

driver.quit()  # Close browser when done
