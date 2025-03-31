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

conn.commit()

cur.close()
conn.close()