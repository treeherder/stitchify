"""SymbolMapper module - assigns symbols to colors and manages legend."""
from typing import Dict, List, Optional
from collections import defaultdict


class SymbolMapper:
    """Maps colors to symbols for cross-stitch patterns."""
    
    # Default symbol set matching original implementation
    DEFAULT_SYMBOLS = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    TRANSPARENT_SYMBOL = " "
    
    def __init__(self, symbols: Optional[str] = None):
        """
        Initialize SymbolMapper.
        
        Args:
            symbols: String of characters to use as symbols.
                    Defaults to A-Z, a-z (52 symbols)
        """
        self.available_symbols = symbols or self.DEFAULT_SYMBOLS
        self.color_to_symbol: Dict[str, str] = {}
        self.symbol_to_color: Dict[str, str] = {}
        self._next_symbol_index = 0
    
    def assign_symbol(self, hex_color: str) -> str:
        """
        Assign a symbol to a color, or return existing mapping.
        
        Args:
            hex_color: Hex color string
            
        Returns:
            Assigned symbol character
            
        Raises:
            ValueError: If all symbols are exhausted
        """
        # Return existing mapping if color already has a symbol
        if hex_color in self.color_to_symbol:
            return self.color_to_symbol[hex_color]
        
        # Check if we have symbols available
        if self._next_symbol_index >= len(self.available_symbols):
            raise ValueError(
                f"Symbol pool exhausted! Image has more than "
                f"{len(self.available_symbols)} unique colors. "
                f"Consider reducing colors or extending symbol set."
            )
        
        # Assign next available symbol
        symbol = self.available_symbols[self._next_symbol_index]
        self.color_to_symbol[hex_color] = symbol
        self.symbol_to_color[symbol] = hex_color
        self._next_symbol_index += 1
        
        return symbol
    
    def get_symbol_for_transparent(self) -> str:
        """Get the symbol used for transparent pixels."""
        return self.TRANSPARENT_SYMBOL
    
    def generate_legend(self, color_counts: Dict[str, int]) -> List[str]:
        """
        Generate legend entries for all mapped colors.
        
        Args:
            color_counts: Dictionary mapping hex colors to stitch counts
            
        Returns:
            List of legend entry strings
        """
        legend_entries = []
        for hex_color, symbol in sorted(self.color_to_symbol.items()):
            count = color_counts.get(hex_color, 0)
            legend_entries.append(f"{symbol}: #{hex_color} ({count}ct)")
        return legend_entries
    
    def generate_legend_with_dmc(
        self, 
        color_counts: Dict[str, int],
        dmc_mapping: Dict[str, Dict[str, any]]
    ) -> List[str]:
        """
        Generate legend entries with DMC thread information.
        
        Args:
            color_counts: Dictionary mapping hex colors to stitch counts
            dmc_mapping: Dictionary mapping hex colors to DMC info
            
        Returns:
            List of legend entry strings with DMC numbers
        """
        legend_entries = []
        for hex_color, symbol in sorted(self.color_to_symbol.items()):
            count = color_counts.get(hex_color, 0)
            
            if hex_color in dmc_mapping:
                dmc_info = dmc_mapping[hex_color]
                dmc_num = dmc_info.get("dmc_number", "")
                dmc_name = dmc_info.get("name", "")
                entry = f"{symbol}: DMC-{dmc_num} {dmc_name} (#{hex_color}, {count}ct)"
            else:
                entry = f"{symbol}: #{hex_color} ({count}ct)"
            
            legend_entries.append(entry)
        return legend_entries
    
    def format_legend(self, legend_entries: List[str], columns: int = 3) -> str:
        """
        Format legend entries into multi-column layout.
        
        Args:
            legend_entries: List of legend entry strings
            columns: Number of columns (default: 3)
            
        Returns:
            Formatted legend string with newlines
        """
        formatted_lines = []
        for i in range(0, len(legend_entries), columns):
            row_entries = legend_entries[i:i+columns]
            formatted_lines.append("    ".join(row_entries))
        return "\n".join(formatted_lines)
    
    def reset(self):
        """Reset all symbol-color mappings."""
        self.color_to_symbol.clear()
        self.symbol_to_color.clear()
        self._next_symbol_index = 0
    
    def get_mappings(self) -> Dict[str, str]:
        """
        Get all current color-symbol mappings.
        
        Returns:
            Dictionary mapping hex colors to symbols
        """
        return self.color_to_symbol.copy()
    
    def get_symbol_count(self) -> int:
        """Get number of symbols currently assigned."""
        return len(self.color_to_symbol)
    
    def __repr__(self) -> str:
        return f"SymbolMapper(symbols={self.get_symbol_count()}/{len(self.available_symbols)})"
