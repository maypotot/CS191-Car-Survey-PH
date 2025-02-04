import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import psycopg2

input_maker = "Honda"
input_model = "Click 160"

conn = psycopg2.connect(host = "localhost", port = 5432, dbname = "vehicle", user = "postgres", password = "password")
cur = conn.cursor()

cur.execute("""
    SELECT model, maker, year, price FROM motors;      
    """)

model, maker, year, price = (None, None, None, None)

for row in cur.fetchall():
    model, maker, year, price = row
    if model == input_model and maker == input_maker:
        break


np.random.seed(42)  # For reproducibility

years = np.arange(2015, 2022)
fmv_data = {}

for year in years:
    base_price = price * np.exp(0.11 * (year - 2010))  # Exponential growth formula
    fmv_data[year] = np.round(np.random.normal(loc=base_price, scale=100000, size=100), 2)

# Flatten the data for sklearn
X = np.repeat(years, 100).reshape(-1, 1)  # Years (repeated for each data point)
y = np.concatenate([fmv_data[year] for year in years])  # FMV values


# Apply Polynomial Features
degree = 3  # You can change this for a higher-order polynomial
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(X)

# Train Polynomial Regression Model
model = LinearRegression()
model.fit(X_poly, y)

# Generate Interpolated Values
years_interp = np.linspace(2010, 2025, 300).reshape(-1, 1)  # More points for a smooth curve

X_interp_poly = poly.transform(years_interp)  # Transform to polynomial features
fmv_interp = model.predict(X_interp_poly)  # Predict FMV

# Plot Scatter Points
plt.figure(figsize=(10, 6))
for i, year in enumerate(years):
    plt.scatter(np.full_like(fmv_data[year], year), fmv_data[year], alpha=0.3, s=8)

# Plot Interpolated Polynomial Curve
plt.plot(years_interp, fmv_interp, color='red', linewidth=2, label=f"Polynomial Regression (Degree {degree})")

# Formatting the plot
plt.xlabel("Year")
plt.ylabel("FMV")
plt.title("Interpolated Fair Market Value of Trucks (Polynomial Regression)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)

plt.show()

