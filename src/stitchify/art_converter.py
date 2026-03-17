"""ArtConverter module - converts photos to high-quality pixel art for cross-stitch."""
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from typing import Union, Optional, Tuple
import warnings

# Optional dependencies for advanced features
try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    warnings.warn("opencv-python not installed. Advanced filters unavailable. Install with: pip install opencv-python")

try:
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    warnings.warn("scikit-learn not installed. K-means color clustering unavailable. Install with: pip install scikit-learn")


class QualityPreset:
    """Predefined quality presets for different image types."""
    
    PHOTO = {
        'bilateral_d': 9,
        'bilateral_sigma_color': 75,
        'bilateral_sigma_space': 75,
        'edge_enhance': 0.3,
        'contrast_boost': 1.1,
        'kmeans_colors': 64
    }
    
    LANDSCAPE = {
        'bilateral_d': 7,
        'bilateral_sigma_color': 60,
        'bilateral_sigma_space': 60,
        'edge_enhance': 0.5,
        'saturation_boost': 1.2,
        'contrast_boost': 1.15,
        'kmeans_colors': 48
    }
    
    PORTRAIT = {
        'bilateral_d': 11,
        'bilateral_sigma_color': 80,
        'bilateral_sigma_space': 80,
        'edge_enhance': 0.2,
        'contrast_boost': 1.05,
        'kmeans_colors': 56
    }
    
    DETAILED = {
        'bilateral_d': 5,
        'bilateral_sigma_color': 50,
        'bilateral_sigma_space': 50,
        'edge_enhance': 0.7,
        'sharpen_strength': 1.3,
        'kmeans_colors': 72
    }


class ArtConverter:
    """
    Convert photos to high-quality cross-stitch ready pixel art.
    
    Uses multi-stage pipeline with edge-preserving filters, intelligent
    color reduction, and selective enhancement for professional results.
    """
    
    def __init__(self, target_width: int = 128, preset: str = 'photo'):
        """
        Initialize ArtConverter.
        
        Args:
            target_width: Target pixel width (default 128 for cross-stitch)
            preset: Quality preset name ('photo', 'landscape', 'portrait', 'detailed')
        """
        self.target_width = target_width
        self.preset = self._load_preset(preset)
    
    def _load_preset(self, preset_name: str) -> dict:
        """Load quality preset configuration."""
        presets = {
            'photo': QualityPreset.PHOTO,
            'landscape': QualityPreset.LANDSCAPE,
            'portrait': QualityPreset.PORTRAIT,
            'detailed': QualityPreset.DETAILED
        }
        return presets.get(preset_name.lower(), QualityPreset.PHOTO)
    
    def convert(
        self,
        image_path: Union[str, Path],
        preserve_details: bool = True
    ) -> Image.Image:
        """
        Convert photo to high-quality pixel art.
        
        Multi-stage pipeline:
        1. Bilateral filter (edge-preserving smoothing)
        2. Smart resize with Lanczos interpolation
        3. K-means color simplification
        4. Edge enhancement
        5. Color/contrast adjustment
        
        Args:
            image_path: Path to input image
            preserve_details: Apply edge-preserving filters (recommended)
        
        Returns:
            PIL Image ready for stitchify DMC quantization
        """
        # Load image
        img = Image.open(image_path).convert('RGB')
        
        # Stage 1: Bilateral filter (if opencv available)
        if preserve_details and HAS_OPENCV:
            img = self._bilateral_filter(img)
        
        # Stage 2: High-quality resize
        img = self._smart_resize(img)
        
        # Stage 3: Color simplification with K-means (if sklearn available)
        if HAS_SKLEARN:
            img = self._kmeans_simplify(img)
        
        # Stage 4: Edge enhancement
        edge_factor = self.preset.get('edge_enhance', 0.3)
        if edge_factor > 0:
            img = self._enhance_edges(img, edge_factor)
        
        # Stage 5: Color adjustments
        img = self._adjust_colors(img)
        
        return img
    
    def _bilateral_filter(self, image: Image.Image) -> Image.Image:
        """
        Apply bilateral filter for edge-preserving smoothing.
        
        Smooths flat areas while preserving sharp edges - critical for
        clean pixel art aesthetic.
        """
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        
        # Apply bilateral filter
        d = self.preset.get('bilateral_d', 9)
        sigma_color = self.preset.get('bilateral_sigma_color', 75)
        sigma_space = self.preset.get('bilateral_sigma_space', 75)
        
        filtered = cv2.bilateralFilter(
            img_array,
            d=d,
            sigmaColor=sigma_color,
            sigmaSpace=sigma_space
        )
        
        return Image.fromarray(filtered)
    
    def _smart_resize(self, image: Image.Image) -> Image.Image:
        """
        High-quality resize with Lanczos interpolation.
        
        Preserves more detail than simple downsampling while creating
        clean pixel boundaries.
        """
        # Calculate proportional height
        aspect = image.height / image.width
        target_height = int(self.target_width * aspect)
        
        # Lanczos is highest quality PIL resampling filter
        resized = image.resize(
            (self.target_width, target_height),
            Image.Resampling.LANCZOS
        )
        
        return resized
    
    def _kmeans_simplify(self, image: Image.Image) -> Image.Image:
        """
        Intelligent color grouping with K-means clustering.
        
        Groups perceptually similar colors before DMC quantization,
        creating cleaner color regions for better cross-stitch results.
        """
        img_array = np.array(image)
        h, w, c = img_array.shape
        
        # Reshape to pixel list
        pixels = img_array.reshape(-1, 3).astype(np.float32)
        
        # K-means clustering
        n_colors = self.preset.get('kmeans_colors', 64)
        unique_colors = len(np.unique(pixels, axis=0))
        n_clusters = min(n_colors, unique_colors)
        
        if n_clusters < unique_colors:
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10,
                max_iter=100
            )
            kmeans.fit(pixels)
            
            # Replace pixels with cluster centers
            simplified = kmeans.cluster_centers_[kmeans.labels_]
            simplified = simplified.reshape(h, w, c).astype(np.uint8)
            
            return Image.fromarray(simplified)
        
        return image
    
    def _enhance_edges(self, image: Image.Image, factor: float = 0.3) -> Image.Image:
        """
        Selective edge enhancement.
        
        Sharpens important boundaries while avoiding over-sharpening
        flat areas.
        """
        # Find edges
        edges = image.filter(ImageFilter.FIND_EDGES)
        
        # Apply sharpening
        enhancer = ImageEnhance.Sharpness(image)
        sharpened = enhancer.enhance(1.0 + factor)
        
        return sharpened
    
    def _adjust_colors(self, image: Image.Image) -> Image.Image:
        """
        Apply color and contrast adjustments.
        
        Boosts saturation and contrast for more vibrant cross-stitch.
        """
        # Contrast boost
        contrast_factor = self.preset.get('contrast_boost', 1.1)
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_factor)
        
        # Saturation boost (for landscapes)
        saturation_factor = self.preset.get('saturation_boost', 1.0)
        if saturation_factor != 1.0:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(saturation_factor)
        
        # Additional sharpening if specified
        sharpen_strength = self.preset.get('sharpen_strength', 0)
        if sharpen_strength > 0:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpen_strength)
        
        return image
    
    def convert_basic(self, image_path: Union[str, Path]) -> Image.Image:
        """
        Basic conversion without advanced features.
        
        Falls back to simple high-quality resize when opencv/sklearn
        are not available.
        
        Args:
            image_path: Path to input image
            
        Returns:
            PIL Image
        """
        img = Image.open(image_path).convert('RGB')
        
        # Just high-quality resize
        aspect = img.height / img.width
        target_height = int(self.target_width * aspect)
        
        resized = img.resize(
            (self.target_width, target_height),
            Image.Resampling.LANCZOS
        )
        
        # Basic sharpening
        enhancer = ImageEnhance.Sharpness(resized)
        sharpened = enhancer.enhance(1.2)
        
        return sharpened


def convert_to_pixel_art(
    image_path: Union[str, Path],
    width: int = 128,
    preset: str = 'photo'
) -> Image.Image:
    """
    Convenience function for converting photos to pixel art.
    
    Args:
        image_path: Path to input image
        width: Target width in pixels
        preset: Quality preset ('photo', 'landscape', 'portrait', 'detailed')
    
    Returns:
        PIL Image ready for stitchify conversion
    
    Example:
        >>> pixel_art = convert_to_pixel_art('photo.jpg', width=128, preset='portrait')
        >>> pixel_art.save('pixel_art.png')
    """
    converter = ArtConverter(target_width=width, preset=preset)
    
    if HAS_OPENCV and HAS_SKLEARN:
        return converter.convert(image_path, preserve_details=True)
    else:
        return converter.convert_basic(image_path)
