# Manages satellite data retrieval from various sources
import requests
import json
import config
from typing import List, Dict, Tuple, Optional

class SatelliteDataManager:
    """Manages satellite data retrieval from various sources"""
    
    def __init__(self):
        # Initialize with default API key from config
        self.n2yo_api_key = config.N2YO_API_KEY
        self.base_urls = {
            'n2yo': config.N2YO_BASE_URL,
            'celestrak': config.CELESTRAK_TLE_URL
        }
        
    def set_n2yo_api_key(self, api_key: str):
        """Set N2YO API key"""
        self.n2yo_api_key = api_key
    
    def get_satellites_above(self, lat: float, lon: float, alt: float, 
                           radius: float, category: str = '0') -> Dict:
        """Get satellites within radius of a point using N2YO API"""
        if not self.n2yo_api_key:
            return {"error": "N2YO API key not set"}
        
        url = f"{self.base_urls['n2yo']}/above/{lat}/{lon}/{alt}/{radius}/{category}/&apiKey={self.n2yo_api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def get_satellite_positions(self, norad_id: int, lat: float, lon: float, 
                              alt: float, seconds: int) -> Dict:
        """Get satellite position data"""
        if not self.n2yo_api_key:
            return {"error": "N2YO API key not set"}
            
        url = f"{self.base_urls['n2yo']}/positions/{norad_id}/{lat}/{lon}/{alt}/{seconds}/&apiKey={self.n2yo_api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def get_celestrak_tle_data(self, category: str = 'stations') -> List[str]:
        """Get TLE data from CelesTrak"""
        url = f"{self.base_urls['celestrak']}?GROUP={category}&FORMAT=tle"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text.strip().split('\n')
        except requests.exceptions.RequestException as e:
            return []
    
    @staticmethod
    def parse_tle(tle_lines: List[str]) -> List[Dict]:
        """Parse TLE data into structured format"""
        satellites = []
        for i in range(0, len(tle_lines), 3):
            if i + 2 < len(tle_lines):
                name = tle_lines[i].strip()
                line1 = tle_lines[i + 1]
                line2 = tle_lines[i + 2]
                
                # Extract NORAD ID from line 1
                norad_id = int(line1[2:7])
                
                satellites.append({
                    'name': name,
                    'norad_id': norad_id,
                    'line1': line1,
                    'line2': line2
                })
        return satellites