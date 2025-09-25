# Satellite Proximity Explorer

An interactive application for tracking satellites and visualizing their proximity to specific locations on Earth.

---
*Satellites within the conical field of view defined by a 10 km surface radius centered on London, on 2025-01-01 00:00 UTC.*

<table>
  <tr>
    <td style="text-align: center;"><img width="1493" height="1037" alt="London__10km_01-01-25-00-00" src="https://github.com/user-attachments/assets/1aba51fb-c09c-40fa-a81e-97c678ed006a" /><br><strong>Found Satellites</strong></td>
    <td style="text-align: center;"><img width="1496" height="1035" alt="London__10km_01-01-25-00-00_visualized" src="https://github.com/user-attachments/assets/f884df8c-7938-41a9-8560-957334dbbf7a" /><br><strong>Visualized (rough, WIP)</strong></td>
  </tr>
</table>

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [API Requirements](#api-requirements)
- [Known Issues](#known-issues)

## Overview
This application allows users to search for satellites near specific geographic locations, visualize their positions in 3D, and analyze satellite ephemeris data. It provides both real-time data retrieval from APIs and the ability to load local ephemeris CSV files for analysis.

## Features
- Interactive GUI for entering search parameters
- Real-time satellite data retrieval using N2YO API
- TLE data support from CelesTrak
- Coordinate conversion between Cartesian and Geodetic systems
- 3D visualization of Earth and satellite positions
- Local CSV ephemeris data loading capability
- Results display in tabular format
- Threading for non-blocking API calls

## Requirements
- Python 3.8 or higher
- Virtual environment (recommended)
- Required packages (see requirements.txt):
  - matplotlib
  - numpy
  - pandas
  - requests
  - typing-extensions
  - tkinter (typically included with Python on Windows)
  
## Configuration
The application uses a configuration file to store API keys and default settings. Modify `config.py` to set:

- `N2YO_API_KEY`: Your N2YO API key (required for real-time data). Default is an empty string - users must provide a valid key either in this file or through the application GUI
- `DEFAULT_OBSERVATION_TIME`: Default observation time for searches
- `DEFAULT_LATITUDE` and `DEFAULT_LONGITUDE`: Default location for searches
- `DEFAULT_RADIUS`: Default search radius in kilometers
- API base URLs and visualization settings

## Installation
1. Clone or download this repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     .venv\Scripts\Activate.ps1
     ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Main Application
To start the full GUI application:
```
python main.py
```

### Using the Application
1. Enter your N2YO API key (required for real-time data)
2. Set the observation time, target latitude, longitude, and search radius
3. Click "Search Satellites" to fetch real-time satellite data
4. Alternatively, click "Load Local Data" to analyze ephemeris data from a CSV file
5. View results in the table
6. Click "Visualize Results" to see a 3D representation of satellite positions

### Testing Components
To verify that all core components are working correctly:
```
python test_satellite_app.py
```

### Analyzing CSV Data
To analyze satellite ephemeris data from a CSV file:
```
python data_analysis.py
```
If the specified CSV file is not found, this script will generate sample ephemeris data for demonstration purposes.

## Project Structure
- `main.py`: Entry point for the application
- `satellite_data_manager.py`: Manages satellite data retrieval from N2YO and CelesTrak APIs
- `coordinate_converter.py`: Handles coordinate system conversions (Cartesian ↔ Geodetic)
- `satellite_visualizer.py`: Implements 3D visualization of satellites and Earth
- `satellite_tracker_gui.py`: Main GUI application with all user interface components
- `data_analysis.py`: Helper script for analyzing ephemeris data
- `test_satellite_app.py`: Unit tests for all components
- `config.py`: Configuration file for API keys and default parameters
- `requirements.txt`: List of required Python packages
- `.gitignore`: Git ignore file for excluding unnecessary files from version control

## Data Sources
- **N2YO API**: Provides real-time satellite tracking data
- **CelesTrak**: Source of TLE (Two-Line Element) data
- **Local CSV Files**: Custom ephemeris data in CSV format

## API Requirements
- An N2YO API key is required for real-time satellite data retrieval
- You can obtain a free API key from [N2YO.com](https://www.n2yo.com/api/)

## Known Issues
- The 3D visualization may require specific matplotlib backend configurations
- Some features may have performance limitations with a large number of satellites
- API rate limiting may apply when using free-tier API keys

## License
MIT License.
This project is made for educational and personal research purposes.
