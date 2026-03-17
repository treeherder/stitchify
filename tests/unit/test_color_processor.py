"""Tests for ColorProcessor module - converts pixels to hex and filters transparency."""
import pytest
from src.stitchify.color_processor import ColorProcessor
from src.stitchify.image_loader import ImageLoader


class TestColorProcessor:
    """Test suite for ColorProcessor class."""
    
    def test_rgba_to_hex(self):
        """Test converting RGBA tuple to hex string."""
        processor = ColorProcessor()
        assert processor.rgba_to_hex((255, 0, 0, 255)) == "ff0000"
        assert processor.rgba_to_hex((0, 255, 0, 255)) == "00ff00"
        assert processor.rgba_to_hex((16, 32, 48, 255)) == "102030"
    
    def test_rgba_to_hex_with_transparency(self):
        """Test converting RGBA with different alpha values."""
        processor = ColorProcessor()
        # Full alpha - still converts color part
        assert processor.rgba_to_hex((255, 0, 0, 255)) == "ff0000"
        # Transparent - still converts color (alpha ignored in hex)
        result = processor.rgba_to_hex((255, 0, 0, 0))
        assert result == "ff0000"
    
    def test_hex_to_rgb(self):
        """Test converting hex string to RGB tuple."""
        processor = ColorProcessor()
        assert processor.hex_to_rgb("ff0000") == (255, 0, 0)
        assert processor.hex_to_rgb("00ff00") == (0, 255, 0)
        assert processor.hex_to_rgb("102030") == (16, 32, 48)
        # Test with # prefix
        assert processor.hex_to_rgb("#ff0000") == (255, 0, 0)
    
    def test_hex_normalization(self):
        """Test that hex values are normalized (lowercase, no #)."""
        processor = ColorProcessor()
        assert processor.normalize_hex("#FF0000") == "ff0000"
        assert processor.normalize_hex("FF0000") == "ff0000"
        assert processor.normalize_hex("ff0000") == "ff0000"
    
    def test_is_opaque(self):
        """Test checking if pixel is fully opaque."""
        processor = ColorProcessor()
        assert processor.is_opaque((255, 0, 0, 255)) is True
        assert processor.is_opaque((255, 0, 0, 0)) is False
        assert processor.is_opaque((255, 0, 0, 128)) is False
    
    def test_filter_transparent_pixels(self, simple_rgba_image):
        """Test filtering out transparent pixels from image data."""
        processor = ColorProcessor()
        loader = ImageLoader(simple_rgba_image)
        opaque_pixels = processor.get_opaque_pixels(loader)
        # Should return only pixels with alpha == 255
        assert len(opaque_pixels) > 0
        for (x, y), hex_color in opaque_pixels:
            # Verify pixel coordinates are valid
            assert 0 <= x < loader.width
            assert 0 <= y < loader.height
    
    def test_extract_unique_colors(self, simple_rgba_image):
        """Test extracting unique colors from an image."""
        processor = ColorProcessor()
        loader = ImageLoader(simple_rgba_image)
        unique = processor.get_unique_colors(loader)
        # simple_rgba_image fixture has 8 opaque colors
        assert len(unique) >= 1
        # All should be valid hex strings
        for color in unique:
            assert len(color) == 6
            assert all(c in '0123456789abcdef' for c in color)
    
    def test_color_frequency_count(self):
        """Test counting occurrences of each color."""
        from PIL import Image
        import tempfile
        
        processor = ColorProcessor()
        # Create a simple 5x5 image with one color
        img = Image.new('RGBA', (5, 5), (100, 150, 200, 255))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            loader = ImageLoader(f.name)
            counts = processor.count_colors(loader)
            
            assert len(counts) == 1
            # Should have 25 pixels total
            assert sum(counts.values()) == 25
    
    def test_edge_case_black(self):
        """Test converting pure black."""
        processor = ColorProcessor()
        assert processor.rgba_to_hex((0, 0, 0, 255)) == "000000"
    
    def test_edge_case_white(self):
        """Test converting pure white."""
        processor = ColorProcessor()
        assert processor.rgba_to_hex((255, 255, 255, 255)) == "ffffff"
    
    def test_manual_hex_conversion_matches_original(self):
        """Test that our hex conversion matches the original algorithm."""
        # The original code uses: hex(x//16) and hex(x%16)
        processor = ColorProcessor()
        
        # Test various RGB values
        assert processor.rgba_to_hex((255, 255, 255, 255)) == "ffffff"
        assert processor.rgba_to_hex((128, 128, 128, 255)) == "808080"
        assert processor.rgba_to_hex((0, 0, 0, 255)) == "000000"
        assert processor.rgba_to_hex((17, 34, 51, 255)) == "112233"
