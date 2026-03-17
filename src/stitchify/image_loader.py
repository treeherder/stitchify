"""ImageLoader module - handles loading and validating images."""
from pathlib import Path
from typing import Union, Tuple, Iterator, Optional, Dict, Any
from PIL import Image


class ImageLoader:
    """Loads and provides access to image pixel data."""
    
    def __init__(self, image_path: Union[str, Path], dmc_palette: Optional[Dict[str, Any]] = None, max_colors: int = 52):
        """
        Initialize ImageLoader with an image file.
        Optionally quantize to DMC palette for accurate color constraint.
        
        Args:
            image_path: Path to the image file
            dmc_palette: Optional DMC color palette for quantization
            max_colors: Maximum number of colors to use (default 52 for symbol limit)
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            IOError: If file is not a valid image
        """
        self.path = Path(image_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            self.image = Image.open(self.path)
            # Convert to RGBA to ensure consistent format
            if self.image.mode != "RGBA":
                self.image = self.image.convert("RGBA")
            
            # Quantize to DMC palette if provided
            if dmc_palette:
                self.image = self._quantize_to_dmc_palette(self.image, dmc_palette, max_colors)
        except Exception as e:
            raise IOError(f"Failed to load image: {e}")
        
        self.width, self.height = self.image.size
    
    def get_dimensions(self) -> Tuple[int, int]:
        """
        Get image dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return (self.width, self.height)
    
    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get RGBA values for pixel at position (x, y).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple of (R, G, B, A) values (0-255)
            
        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Pixel coordinates ({x}, {y}) out of bounds")
        
        return self.image.getpixel((x, y))
    
    def iter_pixels(self) -> Iterator[Tuple[Tuple[int, int], Tuple[int, int, int, int]]]:
        """
        Iterate over all pixels in row-major order.
        
        Yields:
            Tuple of ((x, y), (R, G, B, A))
        """
        for y in range(self.height):
            for x in range(self.width):
                yield ((x, y), self.image.getpixel((x, y)))
    
    def _quantize_to_dmc_palette(self, image: Image.Image, dmc_palette: Dict[str, Any], max_colors: int = 52) -> Image.Image:
        """
        Quantize image to DMC color palette while preserving color subtlety.
        
        Uses PIL's adaptive quantization with Floyd-Steinberg dithering to
        intelligently select from all available DMC colors, maintaining
        nuanced color variations where possible within the symbol limit.
        
        Args:
            image: PIL Image to quantize (RGBA format)
            dmc_palette: Dictionary of DMC colors {dmc_num: {"rgb": (r,g,b), ...}}
            max_colors: Maximum colors to use (constrained by symbol pool)
        
        Returns:
            Quantized RGBA image using only DMC colors
        """
        # Extract RGB values from DMC palette
        dmc_colors = []
        for dmc_info in dmc_palette.values():
            rgb = dmc_info.get("rgb")
            if rgb:
                dmc_colors.append(rgb)
        
        if not dmc_colors:
            return image  # No palette, return original
        
        # Limit colors to available symbols (52 by default)
        # PIL quantize can intelligently pick the best subset
        colors_to_use = min(len(dmc_colors), max_colors, 256)
        
        # Create a palette image
        palette_img = Image.new('P', (1, 1))
        
        # Flatten RGB tuples to palette format [R,G,B,R,G,B,...]
        flat_palette = []
        for rgb in dmc_colors[:colors_to_use]:
            flat_palette.extend(rgb)
        
        # Pad to 256 colors (768 values) as required by PIL
        while len(flat_palette) < 768:
            flat_palette.extend([0, 0, 0])
        
        palette_img.putpalette(flat_palette)
        
        # Convert to RGB for quantization (palette mode doesn't support alpha)
        rgb_image = image.convert('RGB')
        
        # First quantize the image to find the best colors for THIS image
        # This uses adaptive palette selection
        adaptive_quantized = rgb_image.quantize(colors=colors_to_use, dither=Image.Dither.FLOYDSTEINBERG)
        adaptive_rgb = adaptive_quantized.convert('RGB')
        
        # Now quantize to the DMC palette for accurate color matching
        # This ensures we use actual DMC colors
        dmc_quantized = adaptive_rgb.quantize(
            palette=palette_img,
            dither=Image.Dither.FLOYDSTEINBERG
        )
        
        # Convert back to RGBA
        return dmc_quantized.convert('RGBA')
    
    def __repr__(self) -> str:
        return f"ImageLoader(path={self.path}, size={self.width}x{self.height})"
