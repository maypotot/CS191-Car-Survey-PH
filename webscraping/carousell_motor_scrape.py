from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json

showmorelistings_selector = ".D_lj.D_lE.D_lw.D_lr.D_lI.D_Ke"
thumbnailclass = "D_p_"

service = Service(executable_path="webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.carousell.ph/motorcycles-for-sale/h-2652/")

# Click the initial "Show Listings" button
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "[role='submitButton'][type='submit']"))
).click()

time.sleep(3)  # Wait for initial listings to load

# Scroll amount
scrollamt = 4420

def load_all_listings():
    global scrollamt  # Ensure scrollamt is used from the global scope

    while True:
        try:
            # Scroll down
            driver.execute_script(f"window.scrollTo(0, {scrollamt});")
            time.sleep(2)  # Wait for content to load

            # Wait for the "Show More" button to be clickable
            show_more_listings = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, showmorelistings_selector))
            )

            show_more_listings.click()
            time.sleep(3)  # Wait for new listings to load

            # Increase scroll position
            scrollamt += 4420
        except:
            print("No more 'Load More' button found.")
            break

# Run function
load_all_listings()

driver.execute_script("window.scrollTo(0, 0);")
time.sleep(10)

#def load_all_listings():
#    while True:
#        try:
#            driver.execute_script("window.scrollTo(0, 500)")
#            time.sleep(10)
#        except:
#            print("No more 'Load More' button found.")
#            break


#WebDriverWait(driver, 5).until(
#    EC.presence_of_element_located((By.CLASS_NAME, showmorelistingsclass))
#)
#
#show_more_listings = driver.find_element(By.CLASS_NAME, showmorelistingsclass)
#show_more_listings.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, thumbnailclass))
)

num_listings = len(driver.find_elements(By.CLASS_NAME, thumbnailclass))
scraped_data = []  # Store scraped motorcycle data

for i in range(num_listings):
    # Re-fetch the listing elements to avoid stale element reference
    listing_cards = driver.find_elements(By.CLASS_NAME, thumbnailclass)
    
    if i >= len(listing_cards):  # If the number of listings changed
        break
    try:
        listing_cards[i].click()
        time.sleep(5)  # Wait for the listing page to load

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        spec_containers = soup.find_all('div', class_='D_aLP')
        spec_container = spec_containers[1] if len(spec_containers) > 1 else None
        price = soup.find('p', class_='D_kf D_kg D_kk D_kn D_kq D_ks D_bfl D_kz').text.strip()
        motorcycle_specs = {}  # Dictionary to store specs

        if spec_container:
            for spec in spec_container.find_all("div", recursive=False):
                spec_type = spec.find('p').text.strip() if spec.find('p') else "Unknown Spec"
                spec_value = spec.find('span').text.strip() if spec.find('span') else "Unknown Value"
                
                motorcycle_specs[spec_type] = spec_value
                motorcycle_specs["Price"] = price
        else:
            print("spec container not found")

        # Store data
        scraped_data.append(motorcycle_specs)
        print(f"Scraped Listing {i+1}: {motorcycle_specs}")

        driver.back()
        time.sleep(3)  # Wait for the listings page to reload
    except Exception as e:
        print(f"Error navigating listing {i+1}: {e}")


json_data = json.dumps(scraped_data, indent=4)
    
with open("carousell_data.json", "w") as file:
    try:
        file.write(json_data)
    except Exception as e:
        print(e)
file.close()

time.sleep(10)
driver.quit()

