#!/usr/bin/env python3
"""
pixelstitchifier - Convert pixel-art images into cross-stitch patterns

This is a wrapper script that maintains backwards compatibility
with the original pixelstitchifier.py interface while using the new
modular architecture.

Usage:
    python pixelstitchifier_main.py <image_path>           (DMC matching enabled by default)
    python pixelstitchifier_main.py <image_path> --no-dmc (disable DMC matching)
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pixelstitchifier.converter import main

if __name__ == "__main__":
    main()
