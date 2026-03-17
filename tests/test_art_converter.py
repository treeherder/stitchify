"""Tests for ArtConverter module - photo to pixel art conversion."""
import pytest
from PIL import Image
import tempfile
from pathlib import Path

try:
    from src.stitchify.art_converter import ArtConverter, QualityPreset, convert_to_pixel_art, HAS_OPENCV, HAS_SKLEARN
    ART_CONVERTER_AVAILABLE = True
except ImportError:
    ART_CONVERTER_AVAILABLE = False
    pytest.skip("ArtConverter not available", allow_module_level=True)


class TestArtConverter:
    """Test suite for photo-to-pixel-art conversion."""
    
    def test_initialize_with_default_preset(self):
        """Test creating converter with default photo preset."""
        converter = ArtConverter(target_width=128)
        assert converter.target_width == 128
        assert converter.preset is not None
        assert 'bilateral_d' in converter.preset
    
    def test_initialize_with_custom_preset(self):
        """Test creating converter with different presets."""
        presets = ['photo', 'landscape', 'portrait', 'detailed']
        for preset_name in presets:
            converter = ArtConverter(target_width=128, preset=preset_name)
            assert converter.preset is not None
            assert isinstance(converter.preset, dict)
    
    def test_basic_resize_without_advanced_features(self):
        """Test basic pixel art conversion without opencv/sklearn."""
        # Create a simple test image
        img = Image.new('RGB', (256, 256), (100, 150, 200))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            temp_path = f.name
        
        try:
            converter = ArtConverter(target_width=64)
            result = converter.convert_basic(temp_path)
            
            assert isinstance(result, Image.Image)
            assert result.width == 64
            # Height should be proportional
            assert result.height == 64
        finally:
            Path(temp_path).unlink()
    
    def test_convert_with_advanced_features(self):
        """Test full pipeline conversion with opencv/sklearn if available."""
        if not (HAS_OPENCV and HAS_SKLEARN):
            pytest.skip("OpenCV or scikit-learn not available")
        
        # Create a gradient test image
        img = Image.new('RGB', (256, 256))
        pixels = []
        for y in range(256):
            for x in range(256):
                pixels.append((x % 256, y % 256, (x + y) % 256))
        img.putdata(pixels)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            temp_path = f.name
        
        try:
            converter = ArtConverter(target_width=64, preset='photo')
            result = converter.convert(temp_path, preserve_details=True)
            
            assert isinstance(result, Image.Image)
            assert result.width == 64
        finally:
            Path(temp_path).unlink()
    
    def test_preset_configurations(self):
        """Test that different presets have different configurations."""
        photo = QualityPreset.PHOTO
        landscape = QualityPreset.LANDSCAPE
        portrait = QualityPreset.PORTRAIT
        detailed = QualityPreset.DETAILED
        
        # Each preset should have different settings
        assert photo['bilateral_d'] != portrait['bilateral_d']
        assert landscape.get('saturation_boost', 1.0) > photo.get('saturation_boost', 1.0)
        assert detailed['edge_enhance'] > photo['edge_enhance']
    
    def test_smart_resize_maintains_aspect_ratio(self):
        """Test that resize maintains aspect ratio."""
        # Create rectangular image
        img = Image.new('RGB', (400, 200), (255, 0, 0))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            temp_path = f.name
        
        try:
            converter = ArtConverter(target_width=100)
            result = converter._smart_resize(img)
            
            # Should be 100x50 to maintain 2:1 aspect ratio
            assert result.width == 100
            assert result.height == 50
        finally:
            Path(temp_path).unlink()
    
    def test_convenience_function(self):
        """Test convert_to_pixel_art convenience function."""
        img = Image.new('RGB', (256, 256), (50, 100, 150))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            temp_path = f.name
        
        try:
            result = convert_to_pixel_art(temp_path, width=64, preset='photo')
            assert isinstance(result, Image.Image)
            assert result.width == 64
        finally:
            Path(temp_path).unlink()
    
    def test_bilateral_filter_availability(self):
        """Test bilateral filter when opencv is available."""
        if not HAS_OPENCV:
            pytest.skip("OpenCV not available")
        
        img = Image.new('RGB', (128, 128), (100, 100, 100))
        
        converter = ArtConverter(target_width=64)
        filtered = converter._bilateral_filter(img)
        
        assert isinstance(filtered, Image.Image)
        assert filtered.size == img.size
    
    def test_kmeans_simplification_availability(self):
        """Test K-means color simplification when sklearn is available."""
        if not HAS_SKLEARN:
            pytest.skip("scikit-learn not available")
        
        # Create image with many colors
        img = Image.new('RGB', (50, 50))
        pixels = [(x * 5, y * 5, (x + y) * 3) for y in range(50) for x in range(50)]
        img.putdata(pixels)
        
        converter = ArtConverter(target_width=25, preset='photo')
        simplified = converter._kmeans_simplify(img)
        
        assert isinstance(simplified, Image.Image)
        # Should have fewer unique colors
        colors_before = len(set(img.getdata()))
        colors_after = len(set(simplified.getdata()))
        assert colors_after <= colors_before
    
    def test_edge_enhancement(self):
        """Test edge enhancement processing."""
        img = Image.new('RGB', (100, 100), (200, 200, 200))
        
        converter = ArtConverter(target_width=50)
        enhanced = converter._enhance_edges(img, factor=0.5)
        
        assert isinstance(enhanced, Image.Image)
        assert enhanced.size == img.size
    
    def test_color_adjustments(self):
        """Test color and contrast adjustments."""
        img = Image.new('RGB', (100, 100), (128, 128, 128))
        
        converter = ArtConverter(target_width=50, preset='landscape')
        adjusted = converter._adjust_colors(img)
        
        assert isinstance(adjusted, Image.Image)
        assert adjusted.size == img.size
    
    def test_different_target_widths(self):
        """Test conversion with various target widths."""
        img = Image.new('RGB', (512, 512), (100, 150, 200))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img.save(f.name)
            temp_path = f.name
        
        try:
            for width in [32, 64, 128, 256]:
                converter = ArtConverter(target_width=width)
                result = converter.convert_basic(temp_path)
                assert result.width == width
        finally:
            Path(temp_path).unlink()
