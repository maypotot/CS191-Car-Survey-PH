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
    
# carousell
with open('./formatted_scraped_data/carousell_data.json', 'r') as file:
    data = json.load(file)
for motor in data:
    vehicle_price = motor["Price"]
    if vehicle_price:  
        vehicle_price = re.search(r"\d{1,3}(?:,\d{3})*", vehicle_price)  # Match first number
        if vehicle_price:
            vehicle_price = int(vehicle_price.group().replace(",", ""))  
        else:
            vehicle_price = -1 
    else:
        vehicle_price = -1 
    
    maker = str(motor.get("Brand", "NULL"))
    model = str(motor.get("Model", "NULL"))  
    transmission = str(motor.get("Transmission", "NULL"))  
    year = motor.get("Year", -1)
    mileage = motor.get("Mileage", "NULL")
    if mileage == "NULL":
        vehicle_mileage = -1  
    else:
        vehicle_mileage = int(mileage.replace(" km", "").split("-")[1].strip().replace(",", ""))

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
            '{maker}',
            '{model}',
            'NULL',
            '{transmission}',
            'NULL',
            {year},
            {vehicle_mileage},
            {vehicle_price}
            )
    """)

# motodeal
with open('./formatted_scraped_data/motodeal_data.json', 'r') as file:
    data = json.load(file)
for motor in data:
    vehicle_price = motor["Price"].split("-")[0].replace(",", "").strip()
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
            {int(motor["Year"])},
            -1,
            {price}
            )
    """)
    
# sbfinance pt. 1 
with open('./formatted_scraped_data/sbfinance_updated.json', 'r') as file:
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
            '{str(motor["Brand"])}',
            '{str(motor["Model"])}',
            '{str(motor["Variant"])}',
            'NULL',
            'NULL',
            -1,
            '{round(motor["Mileage"]) if motor["Mileage"] is not None else -1}',
            '{round(motor["Price"]) if motor["Price"] is not None else -1}'
            )
    """)
    
# sbfinance pt. 2
with open('./formatted_scraped_data/sbfinance2.json', 'r') as file:
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
            '{str(motor["Brand"])}',
            '{str(motor["Model"])}',
            'NULL',
            'NULL',
            'NULL',
            -1,
            '{round(motor["Mileage"]) if motor["Mileage"] is not None else -1}',
            '{round(motor["Price"]) if motor["Price"] is not None else -1}'
            )
    """)

# motorace
with open('./formatted_scraped_data/motorace_motorcycles.json', 'r') as file:
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
            '{str(motor["Variants"])}',
            'NULL',
            'NULL',
            '{str(motor["Year"])}',
            '{str(motor["Mileage"])}',
            '{round(motor["Price"]) if motor["Price"] is not None else -1}'
            )
    """)

# carmudi
with open('./formatted_scraped_data/carmudi_data.json', 'r') as file:
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

# repodeals
with open('./formatted_scraped_data/repodeals_data.json', 'r') as file:
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
            'NULL',
            'NULL',
            'NULL',
            '{str(motor["Year"])}',
            -1,
            '{str(motor["Price"])}'
            )
    """)

conn.commit()

cur.close()
conn.close()