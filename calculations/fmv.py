from hmac import new
from math import exp
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import random
import sys
import statistics
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

"""
Sample Car:

Make: Audi
Model: A1
Engine Capacity: 1400cc
Fuel Type: Gas
Transmission: A/T (Automatic Transmission)
Drive Type: FWD (Front-Wheel Drive)
Body Type: Hatchback
Seating Capacity: 5-seater
Doors: 3-door

PIRA data is taken from https://www.peoplesgen.com/images/pdf/fairmarketvaluecar2022.pdf
"""

# # Interpolation function
# def interp_func(new_year, odometer, quality):
#     final = []
#     for i in range(len(new_year)):
#         base_value = scraped_data[0] - 0.6 + 0.06 * (exp((new_year[i] - year[0]) * 0.475))
#         depreciation = -0.0004 * odometer
#         quality_factor = 0.02 * quality
#         weight_factor = -0.0001 * 90
#         engine_factor = 0.0005 * 1000
#         final.append(base_value + depreciation + quality_factor + weight_factor + engine_factor)
#     return final


# # Predict FMV for new mileage values
# def get_fmv(input_year, odometer, quality, new_year):
#     final = {}
#     predicted_fmv = interp_func(new_year, odometer, quality)
#     for i in range(len(new_year)):
#         final[int(new_year[i])] = int(float(predicted_fmv[i]) * 1000000)
#     for i in range(len(year)):
#         final[int(year[i])] = int(float(fmv[i]) * 1000000)
#     return final, final.get(input_year, None)


# Example data from web scraping in millions
# scraped_data = {2018: 1.27, 2019: 1.54, 2020: 1.87, 2021: 2.27, 2022: 2.75}
# scraped_years = list(scraped_data.keys())
# scraped_fmv = list(scraped_data.values())
np.random.seed(42)  # For reproducibility

years = np.arange(2015, 2022)
fmv_data = {}

for year in years:
    base_price = 1.5 * np.exp(0.11 * (year - 2010))  # Exponential growth formula
    fmv_data[year] = np.round(np.random.normal(loc=base_price, scale=0.4, size=100), 2)

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
plt.ylabel("FMV (Millions of Pesos)")
plt.title("Interpolated Fair Market Value of Trucks (Polynomial Regression)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)

plt.show()
exit()


# # Define new years for prediction
# # new_year = np.array([2014, 2015, 2016, 2017, 2023])
# # predicted_fmv, fmv_2022 = get_fmv(2022, 10000, 5, new_year)

# # # Generate interpolation points
# # year_interp = np.linspace(new_year[0], new_year[-1], 100)
# # predicted_fmv_interp = interp_func(year_interp, 10000, 5)

# # Plot results
# plt.figure(figsize=(10, 6))
# plt.plot(scraped_years, scraped_fmv, "o", label='Original Data Points')
# # plt.plot(new_year, [predicted_fmv[y] / 1000000 for y in new_year], "x", label='Predicted FMV')
# # plt.plot(year_interp, predicted_fmv_interp, label='Interpolated FMV', linestyle='dashed')
# plt.xlabel('Model Year')
# plt.ylabel('FMV (in millions)')
# plt.legend()
# plt.title("Fair Market Value (FMV) Prediction")
# plt.grid()
# plt.show()

