from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

# Initialize Selenium WebDriver
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://motoxpress.ph/shop")

# Wait for listings to load
time.sleep(10)  # Adjust based on loading time

# Get page source after JavaScript execution
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()  # Close the browser after getting the HTML

# Find all listings
listings = soup.find_all("div", class_="col-md-3 col-6")

motorcycles = []
for listing in listings:
    try:
        name = listing.find("p", class_="Item_title__1iz0q").text.strip()
        transmission = listing.find("div", class_="col").text.strip()
        price = listing.find("div", class_="Item_price__2V3Yj").text.strip()

        parts = name.split()
        maker = parts[0] if len(parts) > 0 else ""
        model = " ".join(parts[1:]) if len(parts) > 1 else ""

        motorcycles.append({
            "Maker": maker,
            "Model": model,
            "Transmission": transmission,
            "Price": price
        })
    except AttributeError:
        continue  # Skip listings with missing data

# Save to JSON file
with open("webscraping/motoxpress_data.json", "w", encoding="utf-8") as json_file:
    json.dump(motorcycles, json_file, indent=4, ensure_ascii=False)

