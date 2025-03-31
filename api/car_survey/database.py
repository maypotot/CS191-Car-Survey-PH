import psycopg2
import re
import json

# conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "gaesunflower6283")
conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "i<3sunflowers")
cur = conn.cursor()

cur.execute("TRUNCATE TABLE motors RESTART IDENTITY CASCADE;")
cur.execute("TRUNCATE TABLE trucks RESTART IDENTITY CASCADE;")

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

cur.execute("""CREATE TABLE IF NOT EXISTS trucks (
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
with open('./formatted_scraped_data/zigwheels_updated.json', 'r') as file1:
    data1 = json.load(file1)
for motor in data1:
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

with open('./formatted_scraped_data/waa2_data.json', 'r') as file2:
    data2 = json.load(file2)
for motor in data2:
    vehicle_price = motor["Vehicle Price"].split("-")[0].strip().replace(",", "")
    try:
        vehicle_price = int(vehicle_price)
    except ValueError:
        vehicle_price = -1

    # vehicle_year = motor["Model Year"]
    # try:
    #     vehicle_year = str(vehicle_year)
    # except ValueError:
    #     vehicle_year = -1
    
    # try:
    #     vehicle_fuel = str(motor["Type of fuel"])
    # except ValueError:
    #     vehicle_fuel = None

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
            -1,
            -1,
            {vehicle_price}
            )
    """)

# RFSHOP
with open('./formatted_scraped_data/rfshop_data.json', 'r') as file3:
    data3 = json.load(file3)

for truck in data3:
    vehicle_price = truck.get("Vehicle Price", "").replace(
        "PHP ", "").replace(",", "").replace(".00", "").strip()
    try:
        vehicle_price = int(vehicle_price)
    except ValueError:
        vehicle_price = 0
        
    mileage_str = truck.get("Mileage", "").strip()
    if mileage_str == "":
        mileage = 50000  # Default mileage if empty
    else:
        numbers = re.findall(r'\d+', mileage_str)
        mileage = int("".join(numbers)) if numbers else 50000

    cur.execute(f"""INSERT INTO trucks (
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
            '{str(truck["Maker"])}',
            '{str(truck["Model"])}',
            'NULL',
            '{str(truck["Transmission"])}',
            '{str(truck["Fuel Type"])}',
            2022,
            {mileage},
            {vehicle_price}
            )
    """)
    
# AUTO MART
with open('./formatted_scraped_data/automart_data.json', 'r') as file4:
    data4 = json.load(file4)

for truck in data4:
    mileage_str = truck.get("Mileage", "").strip()
    if mileage_str == "":
        mileage = 50000  # Default mileage if empty
    else:
        numbers = re.findall(r'\d+', mileage_str)
        mileage = int("".join(numbers)) if numbers else 50000
    
    transmission = truck.get("Transmission Type", "NULL")
    fuel_type = truck.get("Fuel Type", "NULL")
    maker = truck.get("Maker", "NULL")
    model = truck.get("Model", "NULL")
    variant = truck.get("Variant", "NULL")

    cur.execute(f"""INSERT INTO trucks (
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
            '{str(truck["Maker"])}',
            '{str(truck["Model"])}',
            'NULL',
            '{transmission}',
            '{fuel_type}',
            '{str(truck["Model Year"])}',
            {mileage},
            {truck["Vehicle Price"]}
            )
    """)
    
# # PHILMOTORS
# with open('./formatted_scraped_data/philmotors_data.json', 'r') as file5:
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
#             '{str(truck["Model Year"].replace(" Year", ""))}',
#             {mileage},
#             {vehicle_price}
#             )
#     """)

conn.commit()

cur.close()
conn.close()