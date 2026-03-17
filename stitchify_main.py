#!/usr/bin/env python3
"""
Stitchify - Convert pixel-art images into cross-stitch patterns

This is a wrapper script that maintains backwards compatibility
with the original stitchify.py interface while using the new
modular architecture.

Usage:
    python stitchify_main.py <image_path>           (DMC matching enabled by default)
    python stitchify_main.py <image_path> --no-dmc (disable DMC matching)
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from stitchify.converter import main

if __name__ == "__main__":
    main()
