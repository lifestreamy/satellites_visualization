# Configuration file for Satellite Proximity Explorer

# API keys configuration
# Replace with your actual API key if you want to set a default
# You can also set the API key through the application GUI
# Default is empty string to allow proper validation checks
N2YO_API_KEY = ""

# Default values
DEFAULT_OBSERVATION_TIME = "2025-01-01T00:00:00"
DEFAULT_LATITUDE = 40.7128  # New York City coordinates
DEFAULT_LONGITUDE = -74.0060
DEFAULT_RADIUS = 100  # km

# Data source configurations
N2YO_BASE_URL = "https://api.n2yo.com/rest/v1/satellite"
CELESTRAK_TLE_URL = "https://celestrak.com/NORAD/elements/"

# Visualization settings
EARTH_RADIUS_KM = 6371.0
SATELLITE_MARKER_SIZE = 50
PIN_COLOR = 'red'
EARTH_COLOR = 'blue'