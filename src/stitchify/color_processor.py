"""ColorProcessor module - converts pixels to hex and filters transparency."""
from typing import Tuple, Dict, List
from collections import defaultdict
from .image_loader import ImageLoader


class ColorProcessor:
    """Processes image colors, converting between formats and filtering transparency."""
    
    @staticmethod
    def rgba_to_hex(rgba: Tuple[int, int, int, int]) -> str:
        """
        Convert RGBA tuple to hex string (RGB only, no alpha).
        
        Uses the same algorithm as original code:
        hex(x//16) for first digit, hex(x%16) for second digit
        
        Args:
            rgba: Tuple of (R, G, B, A) values (0-255)
            
        Returns:
            Hex string without '#' prefix (e.g., "ff0000")
        """
        r, g, b, a = rgba
        return "".join([
            f"{r//16:x}{r%16:x}",
            f"{g//16:x}{g%16:x}",
            f"{b//16:x}{b%16:x}"
        ])
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex string to RGB tuple.
        
        Args:
            hex_color: Hex color string (with or without '#' prefix)
            
        Returns:
            Tuple of (R, G, B) values (0-255)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def normalize_hex(hex_color: str) -> str:
        """
        Normalize hex color string (lowercase, no '#').
        
        Args:
            hex_color: Hex color string
            
        Returns:
            Normalized hex string
        """
        return hex_color.lstrip('#').lower()
    
    @staticmethod
    def is_opaque(rgba: Tuple[int, int, int, int]) -> bool:
        """
        Check if pixel is fully opaque.
        
        Args:
            rgba: Tuple of (R, G, B, A) values
            
        Returns:
            True if alpha channel is 255 (fully opaque)
        """
        return rgba[3] == 255
    
    def get_opaque_pixels(self, loader: ImageLoader) -> List[Tuple[Tuple[int, int], str]]:
        """
        Get all opaque pixels with their hex colors.
        
        Args:
            loader: ImageLoader instance
            
        Returns:
            List of ((x, y), hex_color) tuples for opaque pixels
        """
        opaque_pixels = []
        for (x, y), rgba in loader.iter_pixels():
            if self.is_opaque(rgba):
                hex_color = self.rgba_to_hex(rgba)
                opaque_pixels.append(((x, y), hex_color))
        return opaque_pixels
    
    def get_unique_colors(self, loader: ImageLoader) -> set:
        """
        Extract unique opaque colors from image.
        
        Args:
            loader: ImageLoader instance
            
        Returns:
            Set of unique hex color strings
        """
        unique_colors = set()
        for _, rgba in loader.iter_pixels():
            if self.is_opaque(rgba):
                hex_color = self.rgba_to_hex(rgba)
                unique_colors.add(hex_color)
        return unique_colors
    
    def count_colors(self, loader: ImageLoader) -> Dict[str, int]:
        """
        Count occurrences of each opaque color.
        
        Args:
            loader: ImageLoader instance
            
        Returns:
            Dictionary mapping hex colors to counts
        """
        color_counts = defaultdict(int)
        for _, rgba in loader.iter_pixels():
            if self.is_opaque(rgba):
                hex_color = self.rgba_to_hex(rgba)
                color_counts[hex_color] += 1
        return dict(color_counts)
