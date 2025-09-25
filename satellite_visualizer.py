# Handles 3D visualization of satellites and Earth
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
from typing import List, Dict, Tuple
import config

class SatelliteVisualizer:
    """Handles 3D visualization of satellites and Earth"""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        self.earth_radius = config.EARTH_RADIUS_KM  # Load Earth radius from config
    
    def create_earth_sphere(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Create a sphere representing Earth"""
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.earth_radius * np.outer(np.cos(u), np.sin(v))
        y = self.earth_radius * np.outer(np.sin(u), np.sin(v))
        z = self.earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z
    
    def create_cone(self, target_lat: float, target_lon: float, radius_km: float) -> Dict:
        """Create cone representing search area"""
        from coordinate_converter import CoordinateConverter  # Import here to avoid circular dependency
        
        # Convert target point to Cartesian
        target_x, target_y, target_z = CoordinateConverter.geodetic_to_cartesian(
            target_lat, target_lon, 0
        )
        
        # Create cone from Earth center through circular area
        cone_height = 20000  # Extend cone 20,000 km into space
        
        # Calculate cone opening angle
        cone_angle = math.atan(radius_km / self.earth_radius)
        
        return {
            'apex': (0, 0, 0),  # Earth center
            'axis': (target_x, target_y, target_z),
            'height': cone_height,
            'angle': cone_angle,
            'target_surface': (target_x, target_y, target_z)
        }
    
    def visualize_satellites(self, satellites: List[Dict], target_lat: float, 
                           target_lon: float, radius_km: float) -> plt.Figure:
        """Create 3D visualization of satellites around Earth"""
        from coordinate_converter import CoordinateConverter  # Import here to avoid circular dependency
        
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Draw Earth with configured color
        x_earth, y_earth, z_earth = self.create_earth_sphere()
        self.ax.plot_surface(x_earth, y_earth, z_earth, alpha=0.3, color=config.EARTH_COLOR)
        
        # Draw target point
        target_x, target_y, target_z = CoordinateConverter.geodetic_to_cartesian(
            target_lat, target_lon, 0
        )
        self.ax.scatter([target_x], [target_y], [target_z], 
                       color='green', s=100, label='Target Point')
        
        # Draw satellites
        for sat in satellites:
            if 'x' in sat and 'y' in sat and 'z' in sat:
                # Satellite position
                sat_x, sat_y, sat_z = sat['x'], sat['y'], sat['z']
                
                # Draw satellite as pin color sphere
                self.ax.scatter([sat_x], [sat_y], [sat_z], 
                               color=config.PIN_COLOR, s=config.SATELLITE_MARKER_SIZE, alpha=0.8)
                
                # Draw "pin" - line from surface to satellite
                # Project satellite position onto Earth surface
                distance_from_center = math.sqrt(sat_x**2 + sat_y**2 + sat_z**2)
                if distance_from_center > 0:
                    surface_x = sat_x * self.earth_radius / distance_from_center
                    surface_y = sat_y * self.earth_radius / distance_from_center
                    surface_z = sat_z * self.earth_radius / distance_from_center
                    
                    # Draw line
                    self.ax.plot([surface_x, sat_x], [surface_y, sat_y], 
                                [surface_z, sat_z], 'k-', alpha=0.6, linewidth=1)
        
        # Set equal aspect ratio and labels
        max_range = 25000
        self.ax.set_xlim([-max_range, max_range])
        self.ax.set_ylim([-max_range, max_range])
        self.ax.set_zlim([-max_range, max_range])
        
        self.ax.set_xlabel('X (km)')
        self.ax.set_ylabel('Y (km)')
        self.ax.set_zlabel('Z (km)')
        self.ax.set_title(f'Satellites within {radius_km}km of ({target_lat:.2f}°, {target_lon:.2f}°)')
        self.ax.legend()
        
        return self.fig