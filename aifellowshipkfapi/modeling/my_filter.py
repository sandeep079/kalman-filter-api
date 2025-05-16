import pandas as pd
import os

# Get the absolute path to this directory
current_dir = os.path.dirname(__file__)

# Construct the full path to the CSV file
csv_path = os.path.join(current_dir, "sensor_data.csv")

# Load the CSV file
df = pd.read_csv(csv_path)

print(df.head())  # or process it with Kalman Filter
