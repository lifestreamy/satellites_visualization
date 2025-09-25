# Test script for the Satellite Tracker application
import unittest
import config
import sys
import os
import math
from datetime import datetime

# Import the refactored modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from satellite_data_manager import SatelliteDataManager
from coordinate_converter import CoordinateConverter
from satellite_visualizer import SatelliteVisualizer

class TestSatelliteDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = SatelliteDataManager()
    
    def test_initialization(self):
        """Test if SatelliteDataManager initializes correctly"""
        self.assertIsNotNone(self.data_manager)
        self.assertEqual(self.data_manager.n2yo_api_key, config.N2YO_API_KEY)
        self.assertIn('n2yo', self.data_manager.base_urls)
        self.assertIn('celestrak', self.data_manager.base_urls)
    
    def test_set_api_key(self):
        """Test setting the N2YO API key"""
        test_key = "test_api_key"
        self.data_manager.set_n2yo_api_key(test_key)
        self.assertEqual(self.data_manager.n2yo_api_key, test_key)
    
    def test_api_call_without_key(self):
        """Test API call behavior when no key is set"""
        # Temporarily set to None
        original_key = self.data_manager.n2yo_api_key
        self.data_manager.n2yo_api_key = None
        
        result = self.data_manager.get_satellites_above(0, 0, 0, 100)
        self.assertIn("error", result)
        
        # Restore original key
        self.data_manager.n2yo_api_key = original_key

class TestCoordinateConverter(unittest.TestCase):
    def test_geodetic_to_cartesian_conversion(self):
        """Test conversion from geodetic to Cartesian coordinates"""
        # Test with known values (equator, prime meridian, sea level)
        lat, lon, alt = 0.0, 0.0, 0.0
        x, y, z = CoordinateConverter.geodetic_to_cartesian(lat, lon, alt)
        
        # Check if x is approximately Earth's radius, y and z are near zero
        self.assertAlmostEqual(x, 6378.137, places=0)
        self.assertAlmostEqual(y, 0.0, places=5)
        self.assertAlmostEqual(z, 0.0, places=5)
    
    def test_cartesian_to_geodetic_conversion(self):
        """Test conversion from Cartesian to geodetic coordinates"""
        # Test with known values (Earth radius along x-axis)
        x, y, z = 6378.137, 0.0, 0.0  # Earth's equatorial radius in km
        lat, lon, alt = CoordinateConverter.cartesian_to_geodetic(x, y, z)
        
        # Check if lat and lon are near 0, alt is near 0
        self.assertAlmostEqual(lat, 0.0, places=5)
        self.assertAlmostEqual(lon, 0.0, places=5)
        self.assertAlmostEqual(alt, 0.0, places=2)
    
    def test_conversion_round_trip(self):
        """Test round-trip conversion maintains accuracy"""
        # Starting point
        lat, lon, alt = 34.0, -118.0, 100.0
        
        # Convert to Cartesian and back
        x, y, z = CoordinateConverter.geodetic_to_cartesian(lat, lon, alt)
        new_lat, new_lon, new_alt = CoordinateConverter.cartesian_to_geodetic(x, y, z)
        
        # Check if values are approximately the same
        self.assertAlmostEqual(lat, new_lat, places=5)
        self.assertAlmostEqual(lon, new_lon, places=5)
        self.assertAlmostEqual(alt, new_alt, places=2)

class TestSatelliteVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = SatelliteVisualizer()
    
    def test_initialization(self):
        """Test if SatelliteVisualizer initializes correctly"""
        self.assertIsNotNone(self.visualizer)
        self.assertEqual(self.visualizer.earth_radius, config.EARTH_RADIUS_KM)
    
    def test_create_earth_sphere(self):
        """Test creating the Earth sphere"""
        x, y, z = self.visualizer.create_earth_sphere()
        
        # Check if the sphere has the correct dimensions
        self.assertEqual(x.shape, y.shape)
        self.assertEqual(y.shape, z.shape)
        
        # Check if all points are on or inside the Earth radius
        max_radius = max(math.sqrt(x[i,j]**2 + y[i,j]**2 + z[i,j]**2) for i in range(10) for j in range(10))
        self.assertLessEqual(max_radius, config.EARTH_RADIUS_KM * 1.01)  # Allow 1% tolerance
    
    def test_create_cone(self):
        """Test creating the search area cone"""
        lat, lon, radius = 34.0, -118.0, 500.0
        cone = self.visualizer.create_cone(lat, lon, radius)
        
        # Check cone has required keys
        required_keys = ['apex', 'axis', 'height', 'angle', 'target_surface']
        for key in required_keys:
            self.assertIn(key, cone)
        
        # Check apex is at Earth's center
        self.assertEqual(cone['apex'], (0, 0, 0))

class TestIntegration(unittest.TestCase):
    def test_configuration_import(self):
        """Test if configuration is imported correctly"""
        self.assertTrue(hasattr(config, 'N2YO_API_KEY'))
        self.assertTrue(hasattr(config, 'DEFAULT_OBSERVATION_TIME'))
        self.assertTrue(hasattr(config, 'DEFAULT_LATITUDE'))
        self.assertTrue(hasattr(config, 'DEFAULT_LONGITUDE'))
        self.assertTrue(hasattr(config, 'DEFAULT_RADIUS'))
    
    def test_module_integration(self):
        """Test basic integration between modules"""
        data_manager = SatelliteDataManager()
        converter = CoordinateConverter()
        visualizer = SatelliteVisualizer()
        
        # This is a basic test to ensure modules can work together
        # Convert a point and prepare for visualization
        lat, lon, alt = config.DEFAULT_LATITUDE, config.DEFAULT_LONGITUDE, 0
        x, y, z = converter.geodetic_to_cartesian(lat, lon, alt)
        
        # Create a mock satellite for visualization
        mock_satellite = {'name': 'TestSat', 'id': '12345', 'x': x+1000, 'y': y+1000, 'z': z+1000}
        
        # This won't actually display the plot in a test environment, but verifies no exceptions are thrown
        try:
            visualizer.visualize_satellites([mock_satellite], lat, lon, config.DEFAULT_RADIUS)
            success = True
        except Exception:
            success = False
            
        self.assertTrue(success, "Visualization should not throw exceptions with valid data")

def run_tests():
    """Run all tests and provide a summary"""
    print("Running tests for Satellite Tracker application components...")
    print(f"Testing with configuration from {os.path.abspath('config.py')}")
    print(f"N2YO API Key set: {'Yes' if config.N2YO_API_KEY else 'No (using default)'}")
    print(f"Default observation time: {config.DEFAULT_OBSERVATION_TIME}")
    print(f"Default location: {config.DEFAULT_LATITUDE}, {config.DEFAULT_LONGITUDE}")
    print(f"Default search radius: {config.DEFAULT_RADIUS} km")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test cases
    test_suite.addTest(unittest.makeSuite(TestSatelliteDataManager))
    test_suite.addTest(unittest.makeSuite(TestCoordinateConverter))
    test_suite.addTest(unittest.makeSuite(TestSatelliteVisualizer))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Tests {'PASSED' if result.wasSuccessful() else 'FAILED'}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    # First, run all tests
    tests_passed = run_tests()
    
    print("\nApplication Information:")
    print("To run the full application, execute:\n")
    print("    python main.py\n")
    print("Important Notes:")
    print("1. Before running the application, ensure you have set up your N2YO API key in config.py")
    print("2. You can also load local ephemeris data in CSV format from the application interface")
    print("3. For best performance, Matplotlib should be configured to use an appropriate backend")
    print("4. All configurations are centralized in config.py")
    
    # If tests failed, provide a warning
    if not tests_passed:
        print("\nWARNING: Some tests failed. Please fix the issues before running the application.")
    else:
        print("\nAll tests passed successfully!")