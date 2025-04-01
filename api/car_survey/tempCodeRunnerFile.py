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
