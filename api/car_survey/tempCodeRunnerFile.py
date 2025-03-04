# PHILMOTORS
# with open('./formatted_scraped_data/automart_data.json', 'r') as file5:
#     data5 = json.load(file5)

# for truck in data5:
#     mileage_str = truck.get("Mileage", "").strip()
#     if mileage_str == "":
#         mileage = 50000  # Default mileage if empty
#     else:
#         numbers = re.findall(r'\d+', mileage_str)
#         mileage = int("".join(numbers)) if numbers else 50000
    
#     vehicle_price = truck.get("Vehicle Price", "").replace("\\u20b", "").replace(",", "").strip()
#     try:
#         vehicle_price = int(vehicle_price)
#     except ValueError:
#         vehicle_price = 0

#     transmission = truck.get("Transmission Type", "NULL")
#     fuel_type = truck.get("Fuel Type", "NULL")
#     maker = truck.get("Maker", "NULL")
#     model = truck.get("Model", "NULL").split("|")[0].strip()
#     variant = truck.get("Variant", "NULL")

#     cur.execute(f"""INSERT INTO trucks (
#             maker,
#             model,
#             variant,
#             transmission,
#             engine,
#             year,
#             mileage,
#             price
#         )
#         VALUES (
#             '{str(truck["Maker"])}',
#             '{str(truck["Model"])}',
#             'NULL',
#             '{transmission}',
#             '{fuel_type}',
#             '{str(truck["Model Year"])}',
#             {mileage},
#             {vehicle_price}
#             )
#     """)