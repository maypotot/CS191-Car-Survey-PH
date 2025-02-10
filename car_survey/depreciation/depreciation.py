import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import psycopg2

def predict_depreciation(input_maker: str, input_model: str, input_year: int, vehicle_type: str = "motors"):
    
    # conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "i<3sunflowers")
    conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "password")
    cur = conn.cursor()

    cur.execute(f"""
        SELECT model, maker, year, price, mileage FROM {vehicle_type};      
        """)

    model, maker, model_year, price, mileage = (None, None, None, None, None)

    data_rows = cur.fetchall()
    for row in data_rows:
        model, maker, model_year, price, mileage = row
        if model == input_model and maker == input_maker:
            break
        if row == data_rows[-1] and len(data_rows) > 0:
            return "No data found for this vehicle."
        
    years_repeated = np.repeat(np.arange(0, 11), 100)
    years = np.arange(0, 11)

    np.random.seed(42)
    initial_value = price 
    depreciation_rate = 0.15 
    mileage_rate = 0.000001
    values_repeated = initial_value * (1 - (depreciation_rate + mileage_rate * mileage)) ** years_repeated  + np.random.randint(-10000, 10000, size=len(years_repeated))

    years_repeated_reshaped = years_repeated.reshape(-1, 1)

    X_log = np.log1p(years_repeated_reshaped)

    model = LinearRegression()
    model.fit(X_log, values_repeated)

    predicted_values = model.predict(X_log)
    predicted_year = model.predict(np.log1p([[input_year-model_year]]))

    # plt.figure(figsize=(8, 5))
    # plt.plot(years_repeated, predicted_values, color='r', linewidth=2, label="Logarithmic Regression")
    # plt.xlabel("Years")
    # plt.ylabel("Value (PHP)")
    # plt.title("Truck Depreciation with Logarithmic Regression")
    # plt.grid(True, linestyle="--", alpha=0.7)
    # plt.legend()
    # plt.show()

    return predicted_year[0], sorted(list(set(predicted_values.tolist())), reverse=True)

# input_maker = "Honda"
# input_model = "Click 160"
# input_year = 2024

# print(predict_depreciation(input_maker, input_model, input_year))