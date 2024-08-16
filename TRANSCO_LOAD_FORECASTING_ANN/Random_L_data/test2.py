import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]



# Number of data points
n_points = len(date_range)

# Generate a base trend that gradually increases from 1400 to 1700
base_trend = np.linspace(1400, 2000, n_points)

# Add small random deviations
np.random.seed(0)  # For reproducibility
deviations = np.random.normal(0, 5, n_points)  # mean 0, standard deviation 20

# Create the final load values by adding deviations to the base trend
loads = base_trend + deviations

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

# Create a DataFrame
data = pd.DataFrame({
    'Date': date_range,
    'Load': loads,
    'Temperature': temperatures
})

# Save to CSV
data.to_csv('load_data_5.csv', index=False)

print("CSV file 'load_data.csv' created successfully.")