import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import psycopg2

def predict_depreciation(input_maker: str, input_model: str = "", input_year: int = -1, input_variant: str = "", input_mileage: int = -1, 
                         input_transmission: str = "", input_fuel: str = "", vehicle_type: str = "motors"):
    conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "i<3sunflowers")
    cur = conn.cursor()

    cur.execute(f"""
        SELECT model, maker, variant, transmission, year, engine, mileage, price FROM {vehicle_type};      
        """)

    model: str
    maker: str
    variant: str
    transmission: str
    model_year: int
    engine: str
    price: int
    mileage: int
    
    scraped_vehicles: list = []
    scarped_vehicle: dict = {}

    data_rows = cur.fetchall()
    for row in data_rows:
        model, maker, variant, transmission, model_year, engine, mileage, price = row
        if not maker.lower() == input_maker.lower():
            continue
        if not model.lower() == input_model.lower() and not input_model == "":
            continue
        if not variant.lower() == input_variant.lower() and not input_variant == "":
            continue
        if not transmission.lower() == input_transmission.lower() and not input_transmission == "":
            continue
        if not engine.lower() == input_fuel.lower() and not input_fuel == "":
            continue
        if mileage < input_mileage - 5000 or mileage > input_mileage + 5000 or mileage <= 100:
            continue
        if model_year <= 100:
            continue
        scarped_vehicle["model"] = model
        scarped_vehicle["maker"] = maker
        scarped_vehicle["variant"] = variant
        scarped_vehicle["transmission"] = transmission
        scarped_vehicle["year"] = model_year
        scarped_vehicle["engine"] = engine
        scarped_vehicle["mileage"] = mileage
        scarped_vehicle["price"] = price
        scraped_vehicles.append(scarped_vehicle.copy())
        scarped_vehicle.clear()
        if row == data_rows[-1] and len(data_rows) > 0 and len(scraped_vehicles) == 0:
            return "No data found for this vehicle."
    
    model_years = [i["year"] for i in scraped_vehicles]
    min_year = min(model_years)
    years = np.arange(min_year, 2026)
    scraped_data = {}
    for year in years:
        for vehicle in scraped_vehicles:
            if vehicle["year"] == year:
                if year not in scraped_data:
                    scraped_data[year] = []
                scraped_data[year].append(vehicle["price"])
    scraped_data[2025] = [x * 1.1 for x in scraped_data[list(scraped_data.keys())[-1]]]

    X = np.concatenate([[year] * len(scraped_data[year]) for year in years if year in scraped_data]).reshape(-1, 1)
    y = np.concatenate([scraped_data[year] for year in years if year in scraped_data])  

    degree = 3 
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    years_interp = np.linspace(2025, min_year, 300).reshape(-1, 1) 

    X_interp_poly = poly.transform(years_interp) 
    depreciation_interp = model.predict(X_interp_poly)
    predicted_year = model.predict(poly.fit_transform([[input_year]]))

    plt.figure(figsize=(10, 6))
    scatter_years = [year for year in years if year in scraped_data]
    for year in scatter_years:
        for price in scraped_data[year]:
            plt.scatter(year, price, color='blue', alpha=0.5, s=10)

    plt.plot(years_interp, depreciation_interp, color='red', linewidth=2, label=f"Polynomial Regression (Degree {degree})")

    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.title("Interpolated Depreciation of Motor (Polynomial Regression)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.gca().invert_xaxis()
    plt.show()
    
    return predicted_year[0].round(2), np.asarray([i.round(2) for i in depreciation_interp]).tolist()

input_maker = "Honda"
input_model = "Click 125i"
input_year = 2025
# input_variant = "ABS"
input_mileage = 12000
# input_transmission = "Manual"

predict_depreciation(input_maker, input_model=input_model, input_year=input_year, input_mileage=input_mileage)
# predicted_fmv, predicted_fmv_lst = predict_fmv(input_maker, input_year=input_year)
# # print(predicted_fmv, predicted_fmv_lst.max(), predicted_fmv_lst.min())
# print(predicted_fmv_lst[10])