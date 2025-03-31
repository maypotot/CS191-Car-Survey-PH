from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import re

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)

motorcycles = []
def scrape_listing(url):
    driver.get(url)
    time.sleep(1)
    
    try:
        label_element = driver.find_element(By.CLASS_NAME, "woocommerce-breadcrumb")
        label_html = label_element.get_attribute("innerHTML")  # Get text including structure
        label_clean = re.sub(r"</?[^>]+>", "", label_html).replace("&nbsp;", " ").strip()
        label_parts = label_clean.split(" ")  # Split breadcrumb by " / "

        maker = label_parts[2]  # Third element
        model = label_parts[4]  # Fourth element
        variant = " ".join(label_parts[5:]) if len(label_parts) >= 4 else ""  # Everything after model
        
        price_element = driver.find_element(By.CLASS_NAME, "woocommerce-product-details__short-description")
        price_text = price_element.text.strip()
        price = (int(re.sub(r"\.(?=0+)|[^0-9]", "", price_text)))/100
        

        
        motorcycles.append({
            "Maker": maker,
            "Model": model,
            "Variants": variant,
            "Year": -1,
            "Mileage": -1,
            "Price": price
        })
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    

def scrape_page(url):
    driver.get(url)
    #Loop through all pages and extract listings

        # Extract listing URLs on the current page
    listing_cards = driver.find_elements(By.CLASS_NAME, "ast-loop-product__link")
    listing_urls = [listing.get_attribute("href") for listing in listing_cards]
    # Scrape each listing
    for url in listing_urls:
        scrape_listing(url)
        print(f"scraped {url}")
    # Try to find and click the "Next" button
        

scrape_page("https://motorace.ph/shop/")
scrape_page("https://motorace.ph/shop/page/2/")
scrape_page("https://motorace.ph/shop/page/3/")
scrape_page("https://motorace.ph/shop/page/4/")
scrape_page("https://motorace.ph/shop/page/5/")

output_dir = "webscraping/data_dump"

with open(f"{output_dir}/motorace_motorcycles.json", "w", encoding="utf-8") as f:
    json.dump(motorcycles, f, ensure_ascii=False, indent=4)
driver.quit()