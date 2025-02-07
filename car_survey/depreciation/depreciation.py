import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import psycopg2




def predict_depreciation(input_maker: str, input_model: str, input_year: int):
    conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "password")
    cur = conn.cursor()

    cur.execute("""
        SELECT model, maker, year, price FROM motors;      
        """)

    model, maker, model_year, price = (None, None, None, None)

    for row in cur.fetchall():
        model, maker, model_year, price = row
        if model == input_model and maker == input_maker:
            break
        
    years_repeated = np.repeat(np.arange(0, 11), 100)

    initial_value = price 
    depreciation_rate = 0.15 
    values_repeated = initial_value * (1 - depreciation_rate) ** years_repeated + np.random.randint(-50000, 50000, size=len(years_repeated))

    years_repeated_reshaped = years_repeated.reshape(-1, 1)

    X_log = np.log1p(years_repeated_reshaped)

    model = LinearRegression()
    model.fit(X_log, values_repeated)

    predicted_values = model.predict(X_log)
    predicted_year = model.predict(np.log1p([[input_year-model_year]]))

    # plt.figure(figsize=(8, 5))
    # plt.scatter(years_repeated, values_repeated, color='b', alpha=0.6, label="Truck Value (PHP)")
    # plt.plot(years_repeated, predicted_values, color='r', linewidth=2, label="Logarithmic Regression")
    # plt.xlabel("Years")
    # plt.ylabel("Value (PHP)")
    # plt.title("Truck Depreciation with Logarithmic Regression")
    # plt.grid(True, linestyle="--", alpha=0.7)
    # plt.legend()
    # plt.show()

    return predicted_year[0], predicted_values

# input_maker = "Honda"
# input_model = "Click 160"
# input_year = 2024

# print(predict_depreciation(input_maker, input_model, input_year))