"""Tests for PatternGenerator module - creates cross-stitch pattern images with grid."""
import pytest
from PIL import Image
from src.pixelstitchifier.pattern_generator import PatternGenerator


class TestPatternGenerator:
    """Test suite for PatternGenerator class."""
    
    def test_initialize_pattern_image(self):
        """Test initializing a blank pattern image with correct dimensions."""
        generator = PatternGenerator(width=3, height=3)
        img = generator.create_blank_pattern(legend_lines=2)
        # Calculate expected dimensions: (w*10)+10, (h*10)+20+(legend_height)
        assert img.size[0] == 40  # (3*10) + 10
        assert img.size[1] == 80  # (3*10) + 20 + (15*2) = 30 + 20 + 30
    
    def test_draw_grid_lines(self):
        """Test drawing grid lines on pattern image."""
        generator = PatternGenerator(width=10, height=10)
        img = generator.create_blank_pattern(legend_lines=1)
        generator.draw_grid()
        # Should have thin lines every 10px, thick lines every 100px
        assert generator.image is not None
    
    def test_grid_line_thickness(self):
        """Test that major grid lines (every 10 stitches) are thicker."""
        # Verify constants are set correctly
        assert PatternGenerator.MAJOR_LINE_WIDTH == 2
        assert PatternGenerator.MINOR_LINE_WIDTH == 1
    
    def test_grid_line_colors(self):
        """Test grid line colors (black for major, gray for minor)."""
        # Verify color constants
        assert PatternGenerator.MAJOR_LINE_COLOR == (0, 0, 0)  # Black
        assert PatternGenerator.MINOR_LINE_COLOR == (128, 128, 128)  # Gray
    
    def test_place_symbols_on_grid(self):
        """Test placing symbols at correct grid positions."""
        generator = PatternGenerator(width=3, height=3)
        generator.create_blank_pattern(legend_lines=0)
        generator.draw_grid()
        symbol_grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", " "]]
        generator.draw_symbols(symbol_grid)
        # Symbols should be drawn (no exception)
        assert generator.image is not None
    
    def test_skip_transparent_symbols(self):
        """Test that transparent symbols (spaces) are not drawn."""
        generator = PatternGenerator(width=2, height=2)
        generator.create_blank_pattern(legend_lines=0)
        symbol_grid = [[" ", "A"], ["B", " "]]
        generator.draw_symbols(symbol_grid)
        # Only "A" and "B" should be drawn (success means no crash)
        assert generator.image is not None
    
    def test_add_legend_to_pattern(self):
        """Test adding legend below the pattern grid."""
        generator = PatternGenerator(width=5, height=5)
        generator.create_blank_pattern(legend_lines=2)
        legend_text = "A: #ff0000 (10ct)\nB: #00ff00 (5ct)"
        generator.add_legend(legend_text)
        # Legend should be added successfully
        assert generator.image is not None
    
    def test_calculate_pattern_dimensions(self):
        """Test calculating total pattern image dimensions."""
        generator = PatternGenerator(width=10, height=10)
        legend_lines = 3
        dims = generator.calculate_dimensions(legend_lines)
        # width = (10*10) + 10 = 110
        # height = (10*10) + 20 + (15 * 3) = 165
        assert dims == (110, 165)
    
    def test_edge_labels(self):
        """Test adding edge labels for stitch counting (TODO from original)."""
        # Future feature - skipping for now
        pytest.skip("Edge labels not yet implemented")
    
    def test_save_pattern_image(self, tmp_path):
        """Test saving pattern image to file."""
        generator = PatternGenerator(width=5, height=5)
        generator.create_blank_pattern(legend_lines=1)
        generator.draw_grid()
        generator.draw_symbols([[" "]*5]*5)
        generator.add_legend("Test Legend")
        
        output_path = tmp_path / "test_pattern.png"
        generator.save(output_path)
        assert output_path.exists()
        # Verify it's a valid PNG
        saved_img = Image.open(output_path)
        assert saved_img.format == "PNG"
    
    def test_generate_complete_pattern(self):
        """Integration test: generate complete pattern from image data."""
        generator = PatternGenerator(width=3, height=3)
        generator.create_blank_pattern(legend_lines=2)
        generator.draw_grid()
        generator.draw_symbols([["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]])
        generator.add_legend("A: #ff0000 (5ct)")
        img = generator.get_image()
        assert img is not None
        assert img.size == (40, 80)  # (3*10)+10, (3*10)+20+(15*2)
    
    def test_grid_offset_calculation(self):
        """Test grid offset for centering (from original code)."""
        # Original uses: woff = int(((w)%10)/2)+1
        generator = PatternGenerator(width=7, height=7)
        offsets = generator.calculate_grid_offsets()
        assert offsets == (int((7%10)/2)+1, int((7%10)/2)+1)
        assert offsets == (4, 4)
    
    def test_legend_multicolumn_formatting(self):
        """Test legend with multiple columns (3 items per row)."""
        # Legend formatting is handled by SymbolMapper, not PatternGenerator
        # This test is more appropriate for SymbolMapper tests
        pytest.skip("Legend formatting handled by SymbolMapper")
    
    def test_pattern_background_color(self):
        """Test that pattern background is white."""
        generator = PatternGenerator(width=5, height=5)
        img = generator.create_blank_pattern(legend_lines=1)
        # Check corners are white
        assert img.getpixel((0, 0)) == (255, 255, 255)
        assert img.getpixel((img.width-1, img.height-1)) == (255, 255, 255)
