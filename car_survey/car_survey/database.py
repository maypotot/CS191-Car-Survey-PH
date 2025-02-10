import psycopg2
import json

conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "password")
# conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "i<3sunflowers")
cur = conn.cursor()

# cur.execute("TRUNCATE TABLE motors RESTART IDENTITY CASCADE;")

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

with open('./webscraping/zigwheels_data.json', 'r') as file1:
    data1 = json.load(file1)
    
for motor in data1:
    vehicle_name_parts = motor["vehicle_name"].split(" ", 1)
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
            '{str(vehicle_name_parts[0])}',
            '{str(vehicle_name_parts[1]) if len(vehicle_name_parts) > 1 else "NULL"}',
            'NULL',
            '{str(motor["Transmission Type"])}',
            '{str(motor["Fuel Type"])}',
            2022,
            50000,
            {vehicle_price}
            )
    """)

with open('./webscraping/test_data.json', 'r') as file2:
    data2 = json.load(file2)

for motor in data2:
    vehicle_price = motor["Vehicle Price"].split("-")[0].strip().replace(",", "")
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
            '{motor["Model Year"]}',
            '{int(motor["Mileage"].replace(" km", "")) * 1000}',
            {vehicle_price}
            )
    """)

conn.commit()

cur.close()
conn.close()