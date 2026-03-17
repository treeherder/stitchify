"""Tests for SymbolMapper module - assigns symbols to colors and manages legend."""
import pytest
from src.stitchify.symbol_mapper import SymbolMapper


class TestSymbolMapper:
    """Test suite for SymbolMapper class."""
    
    def test_initialize_with_default_symbols(self):
        """Test initialization with default symbol set."""
        mapper = SymbolMapper()
        # Default should use A-Z, a-z (52 symbols)
        assert len(mapper.available_symbols) == 52
    
    def test_initialize_with_custom_symbols(self):
        """Test initialization with custom symbol characters."""
        mapper = SymbolMapper(symbols="ABC123")
        assert len(mapper.available_symbols) == 6
    
    def test_assign_symbol_to_color(self):
        """Test assigning a unique symbol to a color."""
        mapper = SymbolMapper()
        symbol = mapper.assign_symbol("ff0000")
        assert symbol == "A"
        next_symbol = mapper.assign_symbol("00ff00")
        assert next_symbol == "a"
    
    def test_same_color_gets_same_symbol(self):
        """Test that requesting symbol for same color returns same symbol."""
        mapper = SymbolMapper()
        symbol1 = mapper.assign_symbol("ff0000")
        symbol2 = mapper.assign_symbol("ff0000")
        assert symbol1 == symbol2
        assert mapper.get_symbol_count() == 1
    
    def test_symbol_exhaustion(self):
        """Test behavior when running out of symbols."""
        mapper = SymbolMapper(symbols="ABC")  # Only 3 symbols
        mapper.assign_symbol("color1")
        mapper.assign_symbol("color2")
        mapper.assign_symbol("color3")
        # Should raise ValueError when trying to assign 4th symbol
        with pytest.raises(ValueError, match="Symbol pool exhausted"):
            mapper.assign_symbol("color4")
    
    def test_transparent_symbol(self):
        """Test that transparent pixels get space character."""
        mapper = SymbolMapper()
        symbol = mapper.get_symbol_for_transparent()
        assert symbol == " "
    
    def test_generate_legend(self):
        """Test generating a legend of color-symbol mappings."""
        mapper = SymbolMapper()
        mapper.assign_symbol("ff0000")
        mapper.assign_symbol("00ff00")
        legend = mapper.generate_legend(color_counts={"ff0000": 10, "00ff00": 5})
        assert len(legend) == 2
        assert "A: #ff0000 (10ct)" in legend
        assert "a: #00ff00 (5ct)" in legend
    
    def test_legend_with_dmc_colors(self):
        """Test generating legend with DMC color names."""
        mapper = SymbolMapper()
        mapper.assign_symbol("000000")  # Black
        dmc_mapping = {
            "000000": {"dmc_number": "310", "name": "Black"}
        }
        legend = mapper.generate_legend_with_dmc(
            color_counts={"000000": 100},
            dmc_mapping=dmc_mapping
        )
        assert len(legend) == 1
        assert "DMC-310" in legend[0]
        assert "Black" in legend[0]
    
    def test_reset_mappings(self):
        """Test resetting symbol-color mappings."""
        mapper = SymbolMapper()
        mapper.assign_symbol("ff0000")
        assert mapper.get_symbol_count() == 1
        mapper.reset()
        assert mapper.get_symbol_count() == 0
        # Should be able to reassign from beginning
        symbol = mapper.assign_symbol("00ff00")
        assert symbol == "A"
    
    def test_get_all_mappings(self):
        """Test retrieving all color-symbol mappings."""
        mapper = SymbolMapper()
        mapper.assign_symbol("ff0000")
        mapper.assign_symbol("00ff00")
        mappings = mapper.get_mappings()
        assert mappings == {"ff0000": "A", "00ff00": "a"}
        # Verify it's a copy
        mappings["test"] = "Z"
        assert "test" not in mapper.get_mappings()
    
    def test_symbol_order_matches_original(self):
        """Test that symbol assignment order matches original implementation."""
        # Original uses: "AaBbCcDd..."
        mapper = SymbolMapper()
        symbols = [mapper.assign_symbol(f"{i:06x}") for i in range(10)]
        assert symbols == ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e"]
    
    def test_legend_formatting_multicolumn(self):
        """Test legend formatting with multiple columns (3 per row)."""
        mapper = SymbolMapper()
        for i in range(9):
            mapper.assign_symbol(f"{i:06x}")
        legend_entries = mapper.generate_legend(color_counts={f"{i:06x}": 1 for i in range(9)})
        formatted = mapper.format_legend(legend_entries, columns=3)
        lines = formatted.split("\n")
        # Should have 3 rows
        assert len(lines) == 3
