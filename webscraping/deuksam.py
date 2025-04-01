from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import json

def extract_model_and_variant(model_element):
    # Stricter regex to capture the model and variant while removing extra text
    match = re.match(r'^([^\(\n]+)\s*(?:\(([^)\n]*)\))?', model_element.strip())

    if match:
        model = match.group(1).strip()  # Model name before "(" or newline
        variant = match.group(2).strip() if match.group(2) else ""  # Variant inside parentheses
        return model, variant
    else:
        return model_element.strip(), ""  # Return original text if no match


def safe_get_text(driver, by, value):
    try:
        return driver.find_element(by, value).text.strip()
    except:
        return ""  # Return empty string if element is not found

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.dueksam.com.ph/motorcycles")

motorcycles = []

def scrape_listing(url):
    driver.get(url)

    time.sleep(3)
    
    model_element = safe_get_text(driver, By.CSS_SELECTOR, ".box-45.px-2")
    model, variant = extract_model_and_variant(model_element)
    maker = safe_get_text(driver, By.XPATH, "//*[@id='tbody']/tr[2]/td[2]")
    transmission = safe_get_text(driver, By.XPATH, "//*[@id='tbody']/tr[4]/td[2]")
    
    price_text = safe_get_text(driver, By.XPATH, "//*[@id='price']/span[1]")
    price = int("".join(re.findall(r'\d+', price_text)))/100 if price_text else None

    motorcycles.append({
        "Maker": maker,
        "Model": model,
        "Variant": variant,
        "Transmission": transmission,
        "Year": -1,
        "Mileage": -1,
        "Price": price
    })
    print(motorcycles[-1])
    
    driver.back()

def scrape_all_pages():
    page_counter = 1
    while True:
        time.sleep(2)  # Allow time for page to load

        print(f"Scraping page: {page_counter}")

        listing_cards = driver.find_elements(By.CSS_SELECTOR, ".item-dt.wow.fadeIn")
        listing_urls = [listing.find_element(By.TAG_NAME, "a").get_attribute("href") for listing in listing_cards if listing.find_element(By.TAG_NAME, "a")]

        for _, url in enumerate(listing_urls):  # Corrected enumeration
            print(url)
            scrape_listing(url)

        try:
            if page_counter >= 6:  # Stop after 6 pages
                break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next')]")
            ))
            next_button.click()
            page_counter += 1
        except Exception as e:
            print(f"No next page found: {e}")
            break

    driver.quit()  # Close the browser when done

scrape_all_pages()

def filter_valid_prices(data):
    """Remove entries with a null (None) price."""
    return [entry for entry in data if entry.get("Price") is not None]

final_data = filter_valid_prices(motorcycles)
with open("webscraping/data_dump/deuksam.json", "w", encoding="utf-8") as json_file:
    json.dump(final_data, json_file, indent=4, ensure_ascii=False)

print(f"✅ Scraping Completed! Total Listings: {len(motorcycles)}")