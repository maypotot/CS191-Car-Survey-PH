import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the webpage
url = "https://used.com.ph/s/secondhand-motorcycle?pg=2"
driver.get(url)

# Extract page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()  # Close the browser

# Find all motorcycle listings
listings = soup.find_all("div", class_="products-list-item")

# Extract motorcycle details
motorcycles = []
for listing in listings:
    # Extract name (contains Maker, Model, and Year)
    name = listing.find("h3", itemprop="name").text.strip()
    
    # Extract price
    price = listing.find("div", class_="products-list-price").text.strip()
    
    # Parse the name to get Maker, Model, and Year
    parts = name.split()
    if len(parts) >= 3:
        maker = parts[0]  # First word is the Maker (e.g., "Suzuki", "Honda")
        year = parts[-1]   # Last word is the Year (e.g., "2022", "2019")
        model = " ".join(parts[1:-1])  # Everything in between is the Model
    else:
        maker, model, year = name, "", ""
    
    motorcycles.append({
        "Maker": maker,
        "Model": model,
        "Year": year,
        "Price": price
    })

# Save data to a JSON file
with open("used_motorcycles.json", "w", encoding="utf-8") as json_file:
    json.dump(motorcycles, json_file, indent=4, ensure_ascii=False)