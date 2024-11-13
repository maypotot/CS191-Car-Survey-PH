from pydoc import text
import re
from bs4 import BeautifulSoup
from urllib import request 


url = "https://www.zigwheels.ph/best-motorcycles"
parsed_data = dict()

resp = request.urlopen(url)
html = resp.read().decode('utf-8')

parsed_html = BeautifulSoup(html, 'html.parser')
with open("test.txt", "w", encoding='utf-8') as file:
    try:
        file.write(parsed_html.prettify())
    except Exception as e:
        print(e)

print(parsed_html.prettify())   
# price = parsed_html.find(class_="pcd-price")
# vehicle_name = parsed_html.find(id="vehicle-title")
# specifications = parsed_html.find(class_="pcd-specs")  

# parsed_data["price"] = price.text.strip()
# parsed_data["vehicle name"] = vehicle_name.text.strip()

# print(specifications)
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

