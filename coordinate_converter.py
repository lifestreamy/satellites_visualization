# Converts between coordinate systems
import math
from typing import Tuple

class CoordinateConverter:
    """Converts between coordinate systems"""
    
    EARTH_RADIUS_KM = 6371.0
    
    @staticmethod
    def cartesian_to_geodetic(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Convert Cartesian (X,Y,Z) coordinates to Geodetic (lat, lon, alt)"""
        # Convert km to meters for calculation
        x_m, y_m, z_m = x * 1000, y * 1000, z * 1000
        
        # WGS84 ellipsoid parameters
        a = 6378137.0  # semi-major axis in meters
        f = 1 / 298.257223563  # flattening
        e2 = 2 * f - f * f  # first eccentricity squared
        
        # Calculate longitude
        lon = math.atan2(y_m, x_m)
        
        # Calculate latitude and altitude using iterative method
        p = math.sqrt(x_m * x_m + y_m * y_m)
        lat = math.atan2(z_m, p * (1 - e2))
        
        for _ in range(5):  # 5 iterations usually sufficient
            N = a / math.sqrt(1 - e2 * math.sin(lat) * math.sin(lat))
            alt = p / math.cos(lat) - N
            lat = math.atan2(z_m, p * (1 - e2 * N / (N + alt)))
        
        # Convert to degrees and altitude to km
        lat_deg = math.degrees(lat)
        lon_deg = math.degrees(lon)
        alt_km = alt / 1000
        
        return lat_deg, lon_deg, alt_km
    
    @staticmethod
    def geodetic_to_cartesian(lat: float, lon: float, alt: float) -> Tuple[float, float, float]:
        """Convert Geodetic (lat, lon, alt) to Cartesian (X,Y,Z)"""
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        alt_m = alt * 1000  # Convert km to meters
        
        # WGS84 parameters
        a = 6378137.0
        f = 1 / 298.257223563
        e2 = 2 * f - f * f
        
        N = a / math.sqrt(1 - e2 * math.sin(lat_rad) * math.sin(lat_rad))
        
        x = (N + alt_m) * math.cos(lat_rad) * math.cos(lon_rad)
        y = (N + alt_m) * math.cos(lat_rad) * math.sin(lon_rad)
        z = (N * (1 - e2) + alt_m) * math.sin(lat_rad)
        
        # Convert back to km
        return x / 1000, y / 1000, z / 1000