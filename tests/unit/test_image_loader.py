"""Tests for ImageLoader module - handles loading and validating images."""
import pytest
from pathlib import Path
from PIL import Image
from src.pixelstitchifier.image_loader import ImageLoader

# Module will be: src.stitchify.image_loader.ImageLoader


class TestImageLoader:
    """Test suite for ImageLoader class."""
    
    def test_load_valid_png(self, simple_rgba_image):
        """Test loading a valid PNG image."""
        loader = ImageLoader(simple_rgba_image)
        assert loader.image is not None
        assert loader.width == 3
        assert loader.height == 3
    
    def test_load_valid_jpg(self, tmp_path):
        """Test loading a valid JPG image and converting to RGBA."""
        # JPG doesn't support transparency, should convert properly
        img = Image.new("RGB", (5, 5), (100, 150, 200))
        jpg_path = tmp_path / "test.jpg"
        img.save(jpg_path)
        
        loader = ImageLoader(jpg_path)
        assert loader.image.mode == "RGBA"
        assert loader.width == 5
        assert loader.height == 5
    
    def test_load_invalid_path(self):
        """Test loading from non-existent path raises appropriate error."""
        with pytest.raises(FileNotFoundError, match="Image file not found"):
            ImageLoader("/nonexistent/path/to/image.png")
    
    def test_load_non_image_file(self, tmp_path):
        """Test loading a non-image file raises appropriate error."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("Not an image")
        with pytest.raises(IOError, match="Failed to load image"):
            ImageLoader(text_file)
    
    def test_get_dimensions(self, simple_rgba_image):
        """Test getting image dimensions."""
        loader = ImageLoader(simple_rgba_image)
        assert loader.get_dimensions() == (3, 3)
    
    def test_get_pixel_at_position(self, simple_rgba_image):
        """Test getting pixel data at specific coordinates."""
        loader = ImageLoader(simple_rgba_image)
        # Red pixel at (0, 0) from fixture
        assert loader.get_pixel(0, 0) == (255, 0, 0, 255)
    
    def test_get_pixel_out_of_bounds(self, simple_rgba_image):
        """Test getting pixel outside image bounds raises error."""
        loader = ImageLoader(simple_rgba_image)
        with pytest.raises(IndexError, match="out of bounds"):
            loader.get_pixel(10, 10)
    
    def test_image_mode_conversion(self, tmp_path):
        """Test that images are converted to RGBA mode."""
        # Create RGB image (no alpha)
        img = Image.new("RGB", (2, 2), (255, 0, 0))
        img_path = tmp_path / "rgb_test.png"
        img.save(img_path)
        
        loader = ImageLoader(img_path)
        assert loader.image.mode == "RGBA"
    
    def test_load_with_pathlib_path(self, simple_rgba_image):
        """Test loading with pathlib.Path object."""
        # Should accept both str and Path objects
        loader1 = ImageLoader(simple_rgba_image)
        loader2 = ImageLoader(str(simple_rgba_image))
        assert loader1.width == loader2.width
        assert loader1.height == loader2.height
    
    def test_iterate_pixels(self, simple_rgba_image):
        """Test iterating over all pixels in row-major order."""
        loader = ImageLoader(simple_rgba_image)
        pixels = list(loader.iter_pixels())
        assert len(pixels) == 9  # 3x3 image
        # First pixel should be red (from fixture)
        assert pixels[0] == ((0, 0), (255, 0, 0, 255))
    
    def test_large_image_loading(self, large_image):
        """Test loading larger images (performance consideration)."""
        loader = ImageLoader(large_image)
        assert loader.width == 50
        assert loader.height == 50
