"""DMCMatcher module - matches colors to DMC thread palette."""
import math
from typing import Dict, Tuple, Optional, Any
import json
import csv
from pathlib import Path


class DMCMatcher:
    """Matches image colors to DMC embroidery floss colors."""
    
    def __init__(self, dmc_colors: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        Initialize DMCMatcher.
        
        Args:
            dmc_colors: Dictionary of DMC colors in format:
                       {dmc_number: {name: str, hex: str, rgb: tuple}}
                       If None, uses bundled minimal set
        """
        self.dmc_colors = dmc_colors or self._get_default_colors()
        self._validate_dmc_colors()
    
    def _get_default_colors(self) -> Dict[str, Dict[str, Any]]:
        """
        Get default DMC color set from bundled CSV file.
        
        Returns:
            Dictionary of DMC colors from adrianj's comprehensive database
        """
        # Load from bundled CSV file
        csv_path = Path(__file__).parent / "dmc_colors.csv"
        
        if not csv_path.exists():
            # Fallback to minimal set if CSV not found
            return {
                "310": {"name": "Black", "hex": "000000", "rgb": (0, 0, 0)},
                "b5200": {"name": "Snow White", "hex": "ffffff", "rgb": (255, 255, 255)},
                "666": {"name": "Bright Red", "hex": "e42531", "rgb": (228, 37, 49)},
                "797": {"name": "Royal Blue", "hex": "13467b", "rgb": (19, 70, 123)},
                "702": {"name": "Kelly Green", "hex": "1d8636", "rgb": (29, 134, 54)},
            }
        
        colors = {}
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSV format: Floss#,Description,Red,Green,Blue,RGB code,Row
                dmc_num = row['Floss#'].strip()
                name = row['Description'].strip()
                r = int(row['Red'])
                g = int(row['Green'])
                b = int(row['Blue'])
                hex_color = row['RGB code'].strip().lower()
                
                colors[dmc_num] = {
                    "name": name,
                    "hex": hex_color,
                    "rgb": (r, g, b)
                }
        
        return colors
    
    def _validate_dmc_colors(self):
        """Validate DMC color database format."""
        for dmc_num, info in self.dmc_colors.items():
            if "rgb" not in info:
                raise ValueError(
                    f"DMC color {dmc_num} missing 'rgb' field. "
                    f"Required format: {{'name': str, 'hex': str, 'rgb': tuple}}"
                )
    
    @staticmethod
    def calculate_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
        """
        Calculate Euclidean distance between two RGB colors.
        
        Args:
            rgb1: First RGB color tuple
            rgb2: Second RGB color tuple
            
        Returns:
            Euclidean distance value
        """
        r_diff = rgb1[0] - rgb2[0]
        g_diff = rgb1[1] - rgb2[1]
        b_diff = rgb1[2] - rgb2[2]
        return math.sqrt(r_diff**2 + g_diff**2 + b_diff**2)
    
    def find_nearest(
        self, 
        rgb: Tuple[int, int, int],
        max_distance: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Find nearest DMC color to given RGB value.
        
        Args:
            rgb: RGB color tuple to match
            max_distance: Optional maximum distance threshold for warning
            
        Returns:
            Dictionary with DMC match info:
            {dmc_number, name, hex, rgb, distance}
        """
        best_match = None
        min_distance = float('inf')
        
        for dmc_num, info in self.dmc_colors.items():
            distance = self.calculate_distance(rgb, info["rgb"])
            
            if distance < min_distance:
                min_distance = distance
                best_match = {
                    "dmc_number": dmc_num,
                    "name": info["name"],
                    "hex": info["hex"],
                    "rgb": info["rgb"],
                    "distance": distance,
                    "is_good_match": (max_distance is None or distance <= max_distance)
                }
        
        return best_match
    
    def match_colors(
        self, 
        colors: Dict[str, Tuple[int, int, int]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Match multiple colors to DMC palette.
        
        Args:
            colors: Dictionary mapping hex colors to RGB tuples
            
        Returns:
            Dictionary mapping hex colors to DMC match info
        """
        matches = {}
        for hex_color, rgb in colors.items():
            matches[hex_color] = self.find_nearest(rgb)
        return matches
    
    def get_dmc_info(self, dmc_number: str) -> Dict[str, Any]:
        """
        Get full information for a DMC color.
        
        Args:
            dmc_number: DMC color number
            
        Returns:
            DMC color information dictionary
            
        Raises:
            KeyError: If DMC number not found
        """
        if dmc_number not in self.dmc_colors:
            raise KeyError(f"DMC color {dmc_number} not found in database")
        return self.dmc_colors[dmc_number]
    
    def format_for_legend(self, dmc_number: str, count: int) -> str:
        """
        Format DMC color info for pattern legend.
        
        Args:
            dmc_number: DMC color number
            count: Stitch count
            
        Returns:
            Formatted legend string
        """
        info = self.get_dmc_info(dmc_number)
        return f"DMC-{dmc_number} {info['name']} (#{info['hex']}, {count}ct)"
    
    def get_palette(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the full DMC color palette.
        
        Returns:
            Dictionary of DMC colors with RGB values
        """
        return self.dmc_colors
    
    def get_palette(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all available DMC colors.
        
        Returns:
            Complete DMC color database
        """
        return self.dmc_colors.copy()
    
    def get_palette_size(self) -> int:
        """Get number of DMC colors in database."""
        return len(self.dmc_colors)
    
    @classmethod
    def from_json(cls, json_path: Path) -> 'DMCMatcher':
        """
        Load DMC colors from JSON file.
        
        Args:
            json_path: Path to JSON file with DMC colors
            
        Returns:
            DMCMatcher instance
        """
        with open(json_path, 'r') as f:
            dmc_data = json.load(f)
        
        # Convert hex to RGB if needed
        for dmc_num, info in dmc_data.items():
            if "rgb" not in info and "hex" in info:
                hex_color = info["hex"].lstrip('#')
                info["rgb"] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        return cls(dmc_colors=dmc_data)
    
    def __repr__(self) -> str:
        return f"DMCMatcher(colors={len(self.dmc_colors)})"
