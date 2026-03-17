"""Stitchify - Convert pixel-art images into cross-stitch patterns."""

__author__ = "Noëlle Anthony"
__version__ = "0.5.0"

from .image_loader import ImageLoader
from .color_processor import ColorProcessor
from .symbol_mapper import SymbolMapper
from .pattern_generator import PatternGenerator
from .dmc_matcher import DMCMatcher
from .art_converter import ArtConverter, convert_to_pixel_art
from .converter import StitchifyConverter, main

__all__ = [
    "ImageLoader",
    "ColorProcessor",
    "SymbolMapper",
    "PatternGenerator",
    "DMCMatcher",
    "ArtConverter",
    "convert_to_pixel_art",
    "StitchifyConverter",
    "main",
]
