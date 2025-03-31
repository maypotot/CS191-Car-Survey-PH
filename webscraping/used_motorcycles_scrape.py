import json
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser (optional)

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

page_links = [
    "https://used.com.ph/s/secondhand-motorcycle?pg=1",
    "https://used.com.ph/s/secondhand-motorcycle?pg=2",
    "https://used.com.ph/s/secondhand-motorcycle?pg=3",
    "https://used.com.ph/s/secondhand-motorcycle?pg=4",
]

motorcycles = []

def parse_motorcycle_name(name):
    """Extract Maker, Model, Year, and Variants from the name using regex."""
    year_match = re.search(r"\b(2\d{3})\b", name)  # Find a 4-digit year starting with 2
    year = int(year_match.group(1)) if year_match else -1
    
    # Remove the year from name
    name_without_year = re.sub(r"\b(2\d{3})\b", "", name).strip()
    
    # Split words and find the first non-numeric maker
    words = name_without_year.split()
    maker = ""
    model = ""
    variants = -1
    
    if words:
        maker = words[0]  # First word is assumed to be the Maker
        
        if len(words) > 1:
            model = words[1]  # Second word is the Model
            variants = " ".join(words[2:]) if len(words) > 2 else -1  # Remaining words are Variants

    return maker, model, year, variants

def scrape_page(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", class_="products-list-item")
    
    for listing in listings:
        try:
            name = listing.find("h3", itemprop="name").text.strip()
            price_text = listing.find("div", class_="products-list-price").text.strip()
            
            # Convert price to an integer (remove Peso sign and commas)
            price = int(re.sub(r"[^0-9]", "", price_text))
            
            maker, model, year, variant = parse_motorcycle_name(name)

            motorcycles.append({
                "Maker": maker,
                "Model": model,
                "Variant": variant,
                "Year": year,
                "Mileage": -1,
                "Price": price
            })
        except AttributeError:
            print(f"Skipping an entry due to missing fields in {url}")

# Scrape all pages
for link in page_links:
    scrape_page(link)

driver.quit()

# Ensure the directory exists before saving JSON
output_dir = "webscraping/data_dump"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/used_motorcycles.json", "w", encoding="utf-8") as f:
    json.dump(motorcycles, f, ensure_ascii=False, indent=4)

print("Scraping complete. Data saved to used_motorcycles.json.")
