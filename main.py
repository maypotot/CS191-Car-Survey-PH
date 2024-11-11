from pydoc import text
import re
from bs4 import BeautifulSoup
from urllib import request 


url = "https://www.philmotors.com/Isuzu-Elf-Dropside-Cargo-Truck-New-Model-TRUCK-FOR-SALE!-83717"
resp = request.urlopen(url)
html = resp.read().decode('utf-8')


parsed_html = BeautifulSoup(html, 'html.parser')
with open("test.txt", "w", encoding='utf-8') as file:
    try:
        file.write(parsed_html.prettify())
    except Exception as e:
        print(e)
# print(parsed_html.prettify())


# spans = parsed_html.find_all("span")
# for span in spans:
#     if "class" not in span.attrs.keys():
#         continue
#     if span.attrs["class"] == ['price']:
#         print(span.text.strip())
#     if span.attrs["class"] == ['mileage']:
#         print(span.text.strip())
#     if span.attrs["class"] == ['delimiter']:
#         print(span.text.strip())
#     if span.attrs["class"] == ['transmission']:
#         print(span.text.strip())

car_specs = parsed_html.find(class_="car-specs")
price = parsed_html.find(id="price_chng")

print(price.prettify())

car_specs_contents = car_specs.contents[-2]

parsed_data = dict()

for content in car_specs_contents:
    if content == "\n":
        continue
    if ":" in content.text:
        parsed_content = content.text.split(":")
        parsed_data[parsed_content[0].strip().replace("?", "")] = parsed_content[1].strip()  
print(parsed_data)
       
