from math import exp
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import random
import sys
import statistics
from scipy.interpolate import interp1d

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

# example data from webscraping; not yet implemented
scraped_data = []
random.seed(42)
for i in range(5):
    scraped_data.append(statistics.median([random.uniform(0.6, 1.5) for _ in range(100)]) + (2 ** i) * 0.4)

# print(scraped_data)
# sys.exit()

# Example data from webscraping
year = np.array([2016, 2017, 2018, 2019, 2020])
fmv = np.array(scraped_data) #in millions of pesos

# Fit cubic spline
def findMiddle(input_list):
    middle = float(len(input_list))/2
    if middle % 2 != 0:
        return input_list[int(middle - .5)]
    else:
        return input_list[int(middle-1)]

def interp_func(new_year: list[int], odometer, quality):
    final = []
    for i in range(len(new_year)):
        final.append(scraped_data[0] - 0.6 + 0.06 * (exp((new_year[i] - new_year[0]) * 0.475)) - 0.0004 * odometer + 0.02 * quality)
    return final

# Predict FMV for new mileage values

    
    
def get_fmv(input_year: int, odometer: int, quality: int):
    final = dict()
    new_year = np.array([2010, 2011, 2012, 2013, 2014, 2015, 2021, 2022, 2023])
    predicted_fmv = interp_func(new_year, odometer, quality)
    for i in range(len(new_year)):
        final[int(new_year[i])] = float(predicted_fmv[i])
    for i in range(len(year)):
        final[int(year[i])] = float(fmv[i])
        
    return final, final[input_year]
    
print(get_fmv(2020, 1000, 5))

# year_interp = np.linspace(new_year[0], new_year[-1], 100)
# predicted_fmv_interp = interp_func(year_interp, 1000, 5)

# Plot original data and spline interpolation
# plt.plot(year, fmv, "o", label='Data points')
# plt.plot(new_year, predicted_fmv, "x", label='Predicted FMV')
# plt.plot(year_interp, predicted_fmv_interp, label='Predicted FMV')
# plt.xlabel('Model Year')
# plt.ylabel('FMV')
# plt.legend()
# plt.show()
