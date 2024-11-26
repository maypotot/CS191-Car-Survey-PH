import re
from bs4 import BeautifulSoup
from urllib import request 

url = "https://www.carousell.ph/p/motorcycle-for-sale-honda-tmx-125-alpha-used-1316509257/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

req = request.Request(url, headers=headers)
resp = request.urlopen(req)
html = resp.read().decode('utf-8')

parsed_html = BeautifulSoup(html, 'html.parser')

with open("motor.txt", "w", encoding='utf-8') as file:
    try:
        file.write(parsed_html.prettify())
    except Exception as e:
        print("Error writing to file:", e)

spec_containers = parsed_html.find_all('div', style='grid-template-columns:1fr 1fr 1fr')

# There are two divs with the same properties in the html, the second one contains the information we need
if len(spec_containers) > 1:
    spec_container = spec_containers[1]  # Select the second div
else:
    spec_container = None
    print("Second spec container not found!")

# Initialize a list to store the spec values
motorcycle_specs = {}

# Extract the spec values
if spec_container:
    for spec in spec_container.find_all("div", recursive=False):
        spec_type = spec.find('p', style=re.compile(r'color:#57585a')).text.strip()
        spec_value = spec.find('span', style=re.compile(r'color:#57585a')).text.strip()

        motorcycle_specs[spec_type] = spec_value
        

# Print out each specifications
print("Motorcycle Specifications:")
for key, value in motorcycle_specs.items():
    print(f"{key}: {value}")
