# Satellite Tracking Data Analysis Tool
# This script analyzes ephemeris data format and can generate sample data

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Import configuration
import config

# Define the expected CSV file path
csv_file = 'L08_OBS_LMOC_DEFEPH_2024366100000_2025001120000_2025001114413.csv'

# Check if the CSV file exists
if os.path.exists(csv_file):
    # Load the sample data to understand the format
    print(f"Loading data from {csv_file}...")
    df = pd.read_csv(csv_file, skiprows=2)
    print("Sample ephemeris data structure:")
    print(df.head())
    print("\nColumns:", df.columns.tolist())
    print("\nData types:")
    print(df.dtypes)
    
    # Check time format
    if 'Time (UTCJ4)' in df.columns:
        print("\nTime format sample:", df['Time (UTCJ4)'].iloc[0])
    if all(col in df.columns for col in ['x (km)', 'y (km)', 'z (km)']):
        print("Position coordinates sample:", df[['x (km)', 'y (km)', 'z (km)']].iloc[0])
else:
    print(f"CSV file not found: {csv_file}")
    print("\nExpected Landsat 8 ephemeris CSV format:")
    print("- First two rows are header information (skipped when reading)")
    print("- Columns should include:")
    print("  * 'Time (UTCJ4)': Timestamp in UTC format")
    print("  * 'x (km)', 'y (km)', 'z (km)': Cartesian coordinates relative to Earth center")
    print("  * 'vx (km/s)', 'vy (km/s)', 'vz (km/s)': Velocity components")
    
    # Generate sample data for demonstration
    print("\nGenerating sample ephemeris data for demonstration...")
    
    # Use default time from config as the base time for sample data
    base_time = datetime.strptime(config.DEFAULT_OBSERVATION_TIME, '%Y-%m-%dT%H:%M:%S')
    
    # Create sample data structure
    sample_data = {
        'Time (UTCJ4)': [
            base_time.strftime('%Y-%m-%dT%H:%M:%S'),
            (base_time + timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            (base_time + timedelta(seconds=2)).strftime('%Y-%m-%dT%H:%M:%S')
        ],
        'x (km)': [5000.0, 5001.5, 5003.0],
        'y (km)': [-3000.0, -2998.5, -2997.0],
        'z (km)': [4000.0, 4001.2, 4002.4],
        'vx (km/s)': [-4.5, -4.5, -4.5],
        'vy (km/s)': [5.2, 5.2, 5.2],
        'vz (km/s)': [3.8, 3.8, 3.8]
    }
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    print("Sample ephemeris data structure:")
    print(df)
    print("\nColumns:", df.columns.tolist())
    print("\nNote: You can load your own Landsat 8 ephemeris files using the 'Load Local Ephemeris Data' button in the GUI.")
    print("\nConfiguration settings can be modified in the config.py file.")