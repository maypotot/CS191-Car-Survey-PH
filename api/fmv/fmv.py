import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import psycopg2


def predict_fmv(input_maker: str, input_model: str, input_year: int, vehicle_type: str = "motors"):
    # Getting data from database
    conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "i<3sunflowers")
    cur = conn.cursor()

    cur.execute(f"""
        SELECT model, maker, year, price FROM {vehicle_type};      
        """)

    model, maker, model_year, price = (None, None, None, None)

    data_rows = cur.fetchall()
    for row in data_rows:
        model, maker, model_year, price = row
        if model == input_model and maker == input_maker:
            break
        if row == data_rows[-1] and len(data_rows) > 0:
            return "No data found for this vehicle."
    
    np.random.seed(42)
    years = np.arange(model_year, 2025)
    fmv_data = {}

    for year in years:
        base_price = price * np.exp(0.12 * (year - model_year))  
        fmv_data[year] = np.round(np.absolute(np.random.normal(loc=base_price, scale=30000, size=100)), 2)

    X = np.repeat(years, 100).reshape(-1, 1)
    y = np.concatenate([fmv_data[year] for year in years])  

    degree = 3 
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    years_interp = np.linspace(model_year, 2025, 300).reshape(-1, 1) 

    X_interp_poly = poly.transform(years_interp) 
    fmv_interp = model.predict(X_interp_poly)
    predicted_year = model.predict(poly.fit_transform([[input_year]]))

    # plt.figure(figsize=(10, 6))
    # for i, year in enumerate(years):
    #     plt.scatter(np.full_like(fmv_data[year], year), fmv_data[year], alpha=0.3, s=8)

    # plt.plot(years_interp, fmv_interp, color='red', linewidth=2, label=f"Polynomial Regression (Degree {degree})")

    # plt.xlabel("Year")
    # plt.ylabel("FMV")
    # plt.title("Interpolated Fair Market Value of Trucks (Polynomial Regression)")
    # plt.legend()
    # plt.grid(True, linestyle="--", alpha=0.5)

    # plt.show()
    return predicted_year[0], fmv_interp

# input_maker = "Honda"
# input_model = "Click 160"
# input_year = 2024

# predicted_fmv, predicted_fmv_lst = predict_fmv(input_maker, input_model, input_year)
# print(predicted_fmv, predicted_fmv_lst.max(), predicted_fmv_lst.min())



