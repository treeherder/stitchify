"""Stitchify - Convert pixel-art images into cross-stitch patterns."""

__author__ = "Noëlle Anthony"
__version__ = "0.4.0"

from .image_loader import ImageLoader
from .color_processor import ColorProcessor
from .symbol_mapper import SymbolMapper
from .pattern_generator import PatternGenerator
from .dmc_matcher import DMCMatcher
from .converter import StitchifyConverter, main

__all__ = [
    "ImageLoader",
    "ColorProcessor",
    "SymbolMapper",
    "PatternGenerator",
    "DMCMatcher",
    "StitchifyConverter",
    "main",
]
