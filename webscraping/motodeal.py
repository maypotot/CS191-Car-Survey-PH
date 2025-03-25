from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Initialize WebDriver
service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.motodeal.com.ph/motorcycles/search?sort-by=lowest-price-to-highest&page=1")
scraped_data = []

def close_cookie_popup():
    """Checks for and closes the cookie warning popup if present."""
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='cookie-warning']/div/div/a"))
        )
        cookie_button.click()
        print("✅ Cookie popup closed.")
        time.sleep(2)
    except:
        print("ℹ️ No cookie popup detected.") 

time.sleep(5)
close_cookie_popup()

def scrape_listing(url):
    """Extract details from an individual motorcycle listing with a timeout"""

    try:
        driver.get(url)

        time.sleep(3)
        close_cookie_popup()

        try:
            name_element = driver.find_element(By.CSS_SELECTOR, ".h1.bold")
            name = name_element.text.strip()
        except:                                         
            name = "Unknown"

        # Extract transmission
        try:
            transmission_element = driver.find_element(By.CSS_SELECTOR, ".nomargin.padbottom5.padright20")
            transmission = transmission_element.text.strip()
        except:
            transmission = "Unknown"

        # Extract price
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, ".h2.light")
            price = price_element.text.strip()
        except:
            price = ""

        # Extract maker and model
        parts = name.split()
        year = parts[0] if len(parts) > 0 else "Unknown"
        maker = parts[1] if len(parts) > 1 else "Unknown"
        model = " ".join(parts[2:]) if len(parts) > 2 else "Unknown"

        # Store scraped data
        scraped_data.append({
            "Year": year,
            "Maker": maker,
            "Model": model,
            "Transmission": transmission,
            "Price": price
        })
        driver.back()  # Go back to listings page

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        driver.back()  # Go back to listings page

def scrape_all_pages():
    while True:
        listing_cards = driver.find_elements(By.CSS_SELECTOR, ".blocklink.img-wrapper.ga-tracker")
        listing_urls = [listing.get_attribute("href") for listing in listing_cards]
        for i, url in enumerate(listing_urls, start=1):
            print(f"🔄 Scraping listing #{i}: {url}...")
            scrape_listing(url)

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            next_button = driver.find_element(By.XPATH, "//*[@id='results-view']/div[2]/nav/a[12]")
            next_link = next_button.get_attribute("href")
            print(next_link)
            driver.get(next_link)


        except:
            print("No more pages found. Scraping complete.")
            break  # Exit loop if no more pages

# Run scraper
scrape_all_pages()



# Close WebDriver
driver.quit()

# Save data to JSON
with open("webscraping/motodeal.json", "w", encoding="utf-8") as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print(f"✅ Scraping Completed! Total Listings: {len(scraped_data)}")
