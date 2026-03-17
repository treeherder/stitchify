"""Thread-database integration module.

This module provides integration with the thread-database package
for comprehensive DMC color data. Falls back to bundled minimal
set if thread-database is not installed.
"""
from typing import Dict, Any, Optional
import warnings


def load_thread_database() -> Optional[Dict[str, Dict[str, Any]]]:
    """
    Load DMC colors from thread-database package.
    
    Returns:
        Dictionary of DMC colors, or None if package not available
    """
    try:
        # Try to import thread-database
        # NOTE: This will be implemented once we add thread-database dependency
        # For now, this is a placeholder for the integration
        import thread_database
        
        dmc_colors = thread_database.get_dmc_colors()
        return convert_thread_db_format(dmc_colors)
    except ImportError:
        warnings.warn(
            "thread-database package not installed. "
            "Using bundled minimal DMC color set. "
            "Install with: pip install thread-database"
        )
        return None


def convert_thread_db_format(thread_db_data: Dict) -> Dict[str, Dict[str, Any]]:
    """
    Convert thread-database format to internal format.
    
    Args:
        thread_db_data: Raw data from thread-database
    
    Returns:
        Dictionary in DMCMatcher format:
        {dmc_number: {name: str, hex: str, rgb: tuple}}
    """
    converted = {}
    
    for dmc_num, info in thread_db_data.items():
        # Handle various possible formats from thread-database
        entry = {
            "name": info.get("name", info.get("description", "Unknown")),
        }
        
        # Get hex color
        if "hex" in info:
            hex_color = info["hex"].lstrip('#').lower()
            entry["hex"] = hex_color
        elif "rgb" in info:
            rgb = info["rgb"]
            entry["hex"] = f"{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        else:
            continue  # Skip entries without color data
        
        # Get RGB color
        if "rgb" in info:
            entry["rgb"] = tuple(info["rgb"])
        else:
            # Convert hex to RGB
            hex_color = entry["hex"]
            entry["rgb"] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        converted[str(dmc_num)] = entry
    
    return converted


def get_dmc_colors() -> Dict[str, Dict[str, Any]]:
    """
    Get DMC colors, trying thread-database first, falling back to minimal set.
    
    Returns:
        Dictionary of DMC colors
    """
    colors = load_thread_database()
    
    if colors is None:
        # Use minimal bundled set
        from .dmc_matcher import DMCMatcher
        matcher = DMCMatcher()
        colors = matcher.get_palette()
    
    return colors


class ThreadDatabaseLoader:
    """Lazy loader for thread-database integration."""
    
    def __init__(self):
        self._colors = None
        self._attempted_load = False
    
    def get_colors(self) -> Dict[str, Dict[str, Any]]:
        """
        Get DMC colors with lazy loading.
        
        Returns:
            Dictionary of DMC colors
        """
        if not self._attempted_load:
            self._colors = load_thread_database()
            self._attempted_load = True
        
        if self._colors is None:
            from .dmc_matcher import DMCMatcher
            matcher = DMCMatcher()
            return matcher.get_palette()
        
        return self._colors
    
    def is_available(self) -> bool:
        """
        Check if thread-database is available.
        
        Returns:
            True if thread-database is installed
        """
        try:
            import thread_database
            return True
        except ImportError:
            return False
