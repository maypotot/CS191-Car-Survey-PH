with open('./formatted_scraped_data/used_motorcycles.json', 'r') as file1:
#     data1 = json.load(file1)
# for motor in data1:
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
#             '{str(motor["Variant"])}',
#             'NULL',
#             'NULL',
#             '{str(motor["Year"])}',
#             '{str(motor["Mileage"])}',
#             '{str(motor["Price"])}'
#             )
#     """)