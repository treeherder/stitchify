"""Pytest fixtures and test helpers for stitchify tests."""
import io
from pathlib import Path
import pytest
from PIL import Image


@pytest.fixture
def test_images_dir(tmp_path):
    """Create a temporary directory for test images."""
    images_dir = tmp_path / "test_images"
    images_dir.mkdir()
    return images_dir


@pytest.fixture
def simple_rgba_image(test_images_dir):
    """Create a simple 3x3 RGBA test image with known colors."""
    img = Image.new("RGBA", (3, 3), (255, 255, 255, 255))
    pixels = [
        # Row 0: Red, Green, Blue
        (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
        # Row 1: Yellow, Magenta, Cyan
        (255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255),
        # Row 2: White, Black, Transparent
        (255, 255, 255, 255), (0, 0, 0, 255), (128, 128, 128, 0),
    ]
    img.putdata(pixels)
    
    img_path = test_images_dir / "simple_test.png"
    img.save(img_path)
    return img_path


@pytest.fixture
def image_with_transparency(test_images_dir):
    """Create an image with mixed transparent and opaque pixels."""
    img = Image.new("RGBA", (2, 2), (0, 0, 0, 0))
    pixels = [
        (255, 0, 0, 255),    # Opaque red
        (0, 255, 0, 0),      # Transparent green
        (0, 0, 255, 128),    # Semi-transparent blue
        (255, 255, 255, 255) # Opaque white
    ]
    img.putdata(pixels)
    
    img_path = test_images_dir / "transparency_test.png"
    img.save(img_path)
    return img_path


@pytest.fixture
def single_color_image(test_images_dir):
    """Create a single color image (useful for edge cases)."""
    img = Image.new("RGBA", (5, 5), (100, 150, 200, 255))
    img_path = test_images_dir / "single_color.png"
    img.save(img_path)
    return img_path


@pytest.fixture
def large_image(test_images_dir):
    """Create a larger test image for performance testing."""
    img = Image.new("RGBA", (50, 50), (255, 255, 255, 255))
    # Create a simple pattern
    for y in range(50):
        for x in range(50):
            if (x + y) % 2 == 0:
                img.putpixel((x, y), (255, 0, 0, 255))  # Red
            else:
                img.putpixel((x, y), (0, 0, 255, 255))  # Blue
    
    img_path = test_images_dir / "large_test.png"
    img.save(img_path)
    return img_path


@pytest.fixture
def many_colors_image(test_images_dir):
    """Create an image with many different colors (>26 to test symbol overflow)."""
    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    for i in range(100):
        x, y = i % 10, i // 10
        # Create 100 different colors
        r = (i * 17) % 256
        g = (i * 31) % 256
        b = (i * 47) % 256
        img.putpixel((x, y), (r, g, b, 255))
    
    img_path = test_images_dir / "many_colors.png"
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_dmc_colors():
    """Sample DMC thread colors for testing."""
    return {
        "310": {"name": "Black", "hex": "000000", "rgb": (0, 0, 0)},
        "321": {"name": "Red", "hex": "c1313a", "rgb": (193, 49, 58)},
        "666": {"name": "Bright Red", "hex": "e42531", "rgb": (228, 37, 49)},
        "700": {"name": "Bright Green", "hex": "117f51", "rgb": (17, 127, 81)},
        "797": {"name": "Royal Blue", "hex": "13467b", "rgb": (19, 70, 123)},
        "b5200": {"name": "Snow White", "hex": "ffffff", "rgb": (255, 255, 255)},
        "444": {"name": "Dark Yellow", "hex": "fcd20a", "rgb": (252, 210, 10)},
        "3843": {"name": "Electric Blue", "hex": "19bfe2", "rgb": (25, 191, 226)},
    }


@pytest.fixture
def mock_pattern_output(tmp_path):
    """Create a temporary directory for pattern output files."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


def create_test_image_bytes(width=3, height=3, color=(255, 0, 0, 255)):
    """Helper to create an image as bytes for testing."""
    img = Image.new("RGBA", (width, height), color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes
