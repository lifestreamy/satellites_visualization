# Entry point for the Satellite Tracker application
from satellite_tracker_gui import SatelliteTrackerGUI

if __name__ == "__main__":
    # Create and run the application
    app = SatelliteTrackerGUI()
    app.run()