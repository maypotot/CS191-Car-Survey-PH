import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Generate multiple points per year
years_repeated = np.repeat(np.arange(0, 11), 10)  # 10 points for each year

# Random depreciation values per year with some spread
initial_value = 2000000  # Initial truck value in PHP
depreciation_rate = 0.15  # Average annual depreciation rate
values_repeated = initial_value * (1 - depreciation_rate) ** years_repeated + np.random.randint(-50000, 50000, size=len(years_repeated))

# Convert years to 2D array for scikit-learn
years_repeated_reshaped = years_repeated.reshape(-1, 1)

# Apply logarithmic transformation
X_log = np.log1p(years_repeated_reshaped)

# Fit logarithmic regression model
model = LinearRegression()
model.fit(X_log, values_repeated)

# Predict values using the model
predicted_values = model.predict(X_log)

# Plot the depreciation with multiple points per year
plt.figure(figsize=(8, 5))
plt.scatter(years_repeated, values_repeated, color='b', alpha=0.6, label="Truck Value (PHP)")
plt.plot(years_repeated, predicted_values, color='r', linewidth=2, label="Logarithmic Regression")
plt.xlabel("Years")
plt.ylabel("Value (PHP)")
plt.title("Truck Depreciation with Logarithmic Regression")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.show()