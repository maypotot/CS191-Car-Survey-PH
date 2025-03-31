import psycopg2
import re
import json

# conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "gaesunflower6283")
conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "i<3sunflowers")
cur = conn.cursor()

cur.execute("TRUNCATE TABLE motors RESTART IDENTITY CASCADE;")

cur.execute("""CREATE TABLE IF NOT EXISTS motors (
    maker VARCHAR(255),
    model VARCHAR(255),
    variant VARCHAR(255),
    transmission VARCHAR(255),
    engine VARCHAR(255),
    year INTEGER,
    mileage INTEGER,
    price INTEGER);
""")

# ZIGWHEELS
with open('./formatted_scraped_data/zigwheels_updated.json', 'r') as file:
    data = json.load(file)
for motor in data:
    vehicle_price = motor["vehicle_price"].split("-")[0].strip().replace(",", "")
    try:
        vehicle_price = int(vehicle_price)
    except ValueError:
        vehicle_price = None
    
    cur.execute(f"""INSERT INTO motors (
            maker,
            model,
            variant,
            transmission,
            engine,
            year,
            mileage,
            price
        )
        VALUES (
            '{str(motor["Maker"])}',
            '{str(motor["Model"])}',
            '{str(motor["Variant"])}',
            '{str(motor["Transmission Type"])}',
            '{str(motor["Fuel Type"])}',
            -1,
            -1,
            {vehicle_price}
            )
    """)
    
# # WAA2
# with open('./formatted_scraped_data/waa2_data.json', 'r') as file2:
#     data2 = json.load(file2)
# for motor in data2:
#     vehicle_price = motor["Vehicle Price"].split("-")[0].strip().replace(",", "")
#     try:
#         vehicle_price = int(vehicle_price)
#     except ValueError:
#         vehicle_price = -1

#     # vehicle_year = motor["Model Year"]
#     # try:
#     #     vehicle_year = str(vehicle_year)
#     # except ValueError:
#     #     vehicle_year = -1
    
#     # try:
#     #     vehicle_fuel = str(motor["Type of fuel"])
#     # except ValueError:
#     #     vehicle_fuel = None

#     cur.execute(f"""INSERT INTO motors (
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
#             '{str(motor["Maker"])}',
#             '{str(motor["Model"])}',
#             'NULL',
#             'NULL',
#             'NULL',
#             -1,
#             -1,
#             {vehicle_price}
#             )
#     """)

# used.com
with open('./formatted_scraped_data/used_motorcycles.json', 'r') as file:
    data = json.load(file)
for motor in data:
    cur.execute(f"""INSERT INTO motors (
            maker,
            model,
            variant,
            transmission,
            engine,
            year,
            mileage,
            price
        )
        VALUES (
            '{str(motor["Maker"])}',
            '{str(motor["Model"])}',
            '{str(motor["Variant"])}',
            'NULL',
            'NULL',
            '{str(motor["Year"])}',
            '{str(motor["Mileage"])}',
            '{str(motor["Price"])}'
            )
    """)

# AFS (sumisho)
with open('./formatted_scraped_data/AFS.json', 'r') as file:
    data = json.load(file)
for motor in data:
    vehicle_price = motor["Price"].split("-")[0].strip().replace(",", "")
    try:
        vehicle_price = int(vehicle_price)
    except ValueError:
        vehicle_price = None
        
    cur.execute(f"""INSERT INTO motors (
            maker,
            model,
            variant,
            transmission,
            engine,
            year,
            mileage,
            price
        )
        VALUES (
            '{str(motor["Brand"])}',
            '{str(motor["Model"])}',
            'NULL',
            'NULL',
            'NULL',
            '{str(motor["Year"])}',
            '{round(motor["Mileage"]) if motor["Mileage"] is not None else -1}',
            {vehicle_price}
            )
    """)
    
# motoxpress
with open('./formatted_scraped_data/motoxpress_data.json', 'r') as file:
    data = json.load(file)
for motor in data:
         
    vehicle_price = motor["Price"].replace(",", "").strip()
    if vehicle_price == "":
        price = -1
    else:
        numbers = re.findall(r'\d+', vehicle_price)
        price = int("".join(numbers)) if numbers else -1

    cur.execute(f"""INSERT INTO motors (
            maker,
            model,
            variant,
            transmission,
            engine,
            year,
            mileage,
            price
        )
        VALUES (
            '{str(motor["Maker"])}',
            '{str(motor["Model"])}',
            'NULL',
            '{str(motor["Transmission"])}',
            'NULL',
            -1,
            -1,
            {price}
            )
    """)
    
# mototrade pt. 1
with open('./formatted_scraped_data/motortrade_big-bike_data.json', 'r') as file:
    data = json.load(file)
for motor in data:
    vehicle_price = motor["Price"].split("\n")[0].replace(",", "").strip()
    if vehicle_price == "":
        price = -1
    else:
        numbers = re.findall(r'\d+', vehicle_price)
        price = int("".join(numbers)) if numbers else -1

    cur.execute(f"""INSERT INTO motors (
            maker,
            model,
            variant,
            transmission,
            engine,
            year,
            mileage,
            price
        )
        VALUES (
            '{str(motor["Maker"])}',
            '{str(motor["Model"])}',
            'NULL',
            '{str(motor["Transmission"])}',
            'NULL',
            -1,
            -1,
            {price}
            )
    """)
    
# mototrade pt. 2
with open('./formatted_scraped_data/motortrade_regular_data.json', 'r') as file:
    data = json.load(file)
for motor in data:
    vehicle_price = motor["Price"].split("\n")[0].replace(",", "").strip()
    if vehicle_price == "":
        price = -1
    else:
        numbers = re.findall(r'\d+', vehicle_price)
        price = int("".join(numbers)) if numbers else -1

    cur.execute(f"""INSERT INTO motors (
            maker,
            model,
            variant,
            transmission,
            engine,
            year,
            mileage,
            price
        )
        VALUES (
            '{str(motor["Maker"])}',
            '{str(motor["Model"])}',
            'NULL',
            '{str(motor["Transmission"])}',
            'NULL',
            -1,
            -1,
            {price}
            )
    """)

conn.commit()

cur.close()
conn.close()