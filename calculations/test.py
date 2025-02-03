import psycopg2
import json

conn = psycopg2.connect(host="localhost", database="test", user="postgres", port="5432", password="password")
cur = conn.cursor()



# cur.execute("""
#     ALTER TABLE motor drop column created_on
# """)



with open('./webscraping/zigwheels_data.json', 'r') as file:
    data = json.load(file)

for motor in data:
    cur.execute(f"""
        INSERT INTO motor (
            maker,
            model,
            variant,
            transmission,
            engine,
            model_year,
            mileage
        )
        VALUES (
            '{str(motor["vehicle_name"])}',
            'Vios',
            '1.3 E',
            'Automatic',
            '{str(motor["Fuel Type"])}',
            2015,
            50000
            )
    """)   

    


conn.commit()

cur.close()
conn.close()