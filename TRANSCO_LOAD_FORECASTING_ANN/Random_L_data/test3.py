import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Number of data points
n_points = len(date_range)

# Function to interpolate temperatures between given points
def interpolate_temperatures(date_range):
    temperatures = []
    for date in date_range:
        if date.month < 5:  # Jan to Apr: 25 to 45 degrees
            temp = 25 + (45 - 25) * (date.timetuple().tm_yday / 120.0)
        elif date.month < 12:  # May to Nov: 45 to 25 degrees
            temp = 45 - (45 - 25) * ((date.timetuple().tm_yday - 120) / 214.0)
        else:  # Dec: 25 degrees
            temp = 25
        temperatures.append(temp)
    return temperatures

# Generate interpolated temperatures
temperatures = interpolate_temperatures(date_range)

# Function to generate loads that vary with temperature and increase year-wise
def interpolate_loads(temperatures, start_load, end_load, yearly_increment):
    loads = []
    for i, temp in enumerate(temperatures):
        year_offset = (date_range[i].year - start_date.year)  # Calculate year offset
        base_load = start_load + yearly_increment * year_offset
        
        if temp < 30:  # For temperatures below 30°C
            load = base_load + (1600 - base_load) * (temp - 25) / 5.0
        elif temp < 40:  # For temperatures between 30°C and 40°C
            load = base_load + (1700 - base_load) * (temp - 30) / 10.0
        else:  # For temperatures above 40°C
            load = base_load + (1500 - base_load) * (temp - 40) / 5.0
        
        loads.append(load)
    return loads

# Generate interpolated loads with yearly increment
start_load = 1450
end_load = 1700
yearly_increment = (end_load - start_load) / (2023 - 2020)  # Calculate the yearly increment
loads = interpolate_loads(temperatures, start_load, end_load, yearly_increment)

# Create a DataFrame
data = pd.DataFrame({
    'Date': date_range,
    'Load': loads,
    'Temperature': temperatures
})

# Save to CSV
data.to_csv('load_data_2.csv', index=False)

print("CSV file 'load_data.csv' created successfully.")
