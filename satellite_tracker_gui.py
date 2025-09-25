# Main GUI application for tracking satellites
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import threading
from typing import List, Dict
import config
from satellite_data_manager import SatelliteDataManager
from coordinate_converter import CoordinateConverter
from satellite_visualizer import SatelliteVisualizer

class SatelliteTrackerGUI:
    """Main GUI application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Satellite Tracker - Earth Observation Satellites")
        self.root.geometry("1200x800")
        
        self.data_manager = SatelliteDataManager()
        self.visualizer = SatelliteVisualizer()
        self.converter = CoordinateConverter()
        
        self.satellites_data = []
        self.current_results = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        control_frame = ttk.LabelFrame(main_frame, text="Search Parameters", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # API Key input
        ttk.Label(control_frame, text="N2YO API Key:").pack(anchor=tk.W)
        self.api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(control_frame, textvariable=self.api_key_var, width=30, show="*")
        api_key_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(control_frame, text="Set API Key", 
                  command=self.set_api_key).pack(fill=tk.X, pady=(0, 10))
        
        # Time input
        ttk.Label(control_frame, text="Time (YYYY-MM-DD HH:MM:SS):").pack(anchor=tk.W)
        # Use default time from config or current time
        default_time = config.DEFAULT_OBSERVATION_TIME.replace('T', ' ')
        self.time_var = tk.StringVar(value=default_time)
        ttk.Entry(control_frame, textvariable=self.time_var, width=30).pack(fill=tk.X, pady=(0, 10))
        
        # Location inputs with config defaults
        ttk.Label(control_frame, text="Target Latitude (°):").pack(anchor=tk.W)
        self.lat_var = tk.DoubleVar(value=config.DEFAULT_LATITUDE)
        ttk.Entry(control_frame, textvariable=self.lat_var, width=30).pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(control_frame, text="Target Longitude (°):").pack(anchor=tk.W)
        self.lon_var = tk.DoubleVar(value=config.DEFAULT_LONGITUDE)
        ttk.Entry(control_frame, textvariable=self.lon_var, width=30).pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(control_frame, text="Search Radius (km):").pack(anchor=tk.W)
        self.radius_var = tk.DoubleVar(value=config.DEFAULT_RADIUS)
        ttk.Entry(control_frame, textvariable=self.radius_var, width=30).pack(fill=tk.X, pady=(0, 10))
        
        # Search button
        ttk.Button(control_frame, text="Search Satellites", 
                  command=self.search_satellites).pack(fill=tk.X, pady=(0, 10))
        
        # Load local data button
        ttk.Button(control_frame, text="Load Local Ephemeris Data", 
                  command=self.load_local_data).pack(fill=tk.X, pady=(0, 10))
        
        # Visualize button
        ttk.Button(control_frame, text="Visualize in 3D", 
                  command=self.visualize_results).pack(fill=tk.X, pady=(0, 10))
        
        # Right panel for results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results tree
        columns = ("Name", "ID", "Latitude", "Longitude", "Altitude (km)")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_api_key(self):
        """Set N2YO API key"""
        api_key = self.api_key_var.get().strip()
        if api_key:
            self.data_manager.set_n2yo_api_key(api_key)
            self.status_var.set("API Key set successfully")
            messagebox.showinfo("Success", "API Key set successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key")
    
    def search_satellites(self):
        """Search for satellites in the specified area"""
        def search_thread():
            try:
                self.status_var.set("Searching satellites...")
                self.root.update()
                
                lat = self.lat_var.get()
                lon = self.lon_var.get()
                radius = self.radius_var.get()
                
                # Get satellites above location using N2YO API
                result = self.data_manager.get_satellites_above(lat, lon, 0, radius)
                
                if "error" in result:
                    messagebox.showerror("Error", result["error"])
                    self.status_var.set("Search failed")
                    return
                
                # Clear previous results
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
                
                self.current_results = []
                
                if "above" in result:
                    for sat in result["above"]:
                        # Convert satellite position to standard format
                        sat_data = {
                            'name': sat.get('satname', 'Unknown'),
                            'id': sat.get('satid', 'Unknown'),
                            'latitude': sat.get('satlat', 0),
                            'longitude': sat.get('satlng', 0),
                            'altitude': sat.get('satalt', 0),
                            'x': None, 'y': None, 'z': None  # Will calculate if needed
                        }
                        
                        # Convert to Cartesian coordinates for visualization
                        if sat_data['latitude'] and sat_data['longitude'] and sat_data['altitude']:
                            x, y, z = self.converter.geodetic_to_cartesian(
                                sat_data['latitude'], sat_data['longitude'], sat_data['altitude']
                            )
                            sat_data['x'] = x
                            sat_data['y'] = y
                            sat_data['z'] = z
                        
                        self.current_results.append(sat_data)
                        
                        # Add to tree
                        self.results_tree.insert("", "end", values=(
                            sat_data['name'],
                            sat_data['id'],
                            f"{sat_data['latitude']:.4f}",
                            f"{sat_data['longitude']:.4f}",
                            f"{sat_data['altitude']:.2f}"
                        ))
                
                self.status_var.set(f"Found {len(self.current_results)} satellites")
                
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
                self.status_var.set("Search failed")
        
        # Run in separate thread to avoid GUI blocking
        threading.Thread(target=search_thread, daemon=True).start()
    
    def load_local_data(self):
        """Load local ephemeris data from CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Ephemeris CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.status_var.set("Loading local data...")
            
            # Try to load the CSV file (skip header rows if needed)
            df = pd.read_csv(file_path, skiprows=2)
            
            # Clear previous results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            self.current_results = []
            
            # Process each row
            for idx, row in df.iterrows():
                if idx >= 100:  # Limit to first 100 entries for performance
                    break
                
                # Extract Cartesian coordinates
                x = row['x (km)']
                y = row['y (km)']
                z = row['z (km)']
                
                # Convert to geodetic
                lat, lon, alt = self.converter.cartesian_to_geodetic(x, y, z)
                
                # Create satellite data entry
                sat_data = {
                    'name': f"Satellite_{idx + 1}",
                    'id': f"LOCAL_{idx + 1}",
                    'latitude': lat,
                    'longitude': lon,
                    'altitude': alt,
                    'x': x, 'y': y, 'z': z,
                    'time': row['Time (UTCJ4)']
                }
                
                self.current_results.append(sat_data)
                
                # Add to tree
                self.results_tree.insert("", "end", values=(
                    sat_data['name'],
                    sat_data['id'],
                    f"{lat:.4f}",
                    f"{lon:.4f}",
                    f"{alt:.2f}"
                ))
            
            self.status_var.set(f"Loaded {len(self.current_results)} satellite positions from local data")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            self.status_var.set("Load failed")
    
    def visualize_results(self):
        """Create 3D visualization of current results"""
        if not self.current_results:
            messagebox.showwarning("Warning", "No data to visualize. Please search for satellites first.")
            return
        
        try:
            self.status_var.set("Creating 3D visualization...")
            
            lat = self.lat_var.get()
            lon = self.lon_var.get()
            radius = self.radius_var.get()
            
            # Create visualization
            fig = self.visualizer.visualize_satellites(self.current_results, lat, lon, radius)
            
            # Show in new window
            viz_window = tk.Toplevel(self.root)
            viz_window.title("3D Satellite Visualization")
            viz_window.geometry("800x600")
            
            canvas = FigureCanvasTkAgg(fig, viz_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set("3D visualization created")
            
        except Exception as e:
            messagebox.showerror("Error", f"Visualization failed: {str(e)}")
            self.status_var.set("Visualization failed")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    app = SatelliteTrackerGUI()
    app.run()