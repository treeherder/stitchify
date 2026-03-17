#!/usr/bin/env python3
"""Build script for creating Windows executable with PyInstaller."""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Build standalone Windows executable."""
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--name=pixelstitchifier',      # Output name
        '--icon=NONE',                  # Add icon path if you have one
        '--add-data=src/pixelstitchifier/dmc_colors.csv:src/pixelstitchifier',  # Include DMC database
        '--hidden-import=PIL._tkinter_finder',  # PIL dependencies
        '--hidden-import=cv2',          # OpenCV
        '--hidden-import=sklearn',      # scikit-learn
        '--hidden-import=numpy',        # NumPy
        '--collect-all=PIL',            # Collect all PIL modules
        '--collect-all=cv2',            # Collect all OpenCV modules
        '--collect-all=sklearn',        # Collect all sklearn modules
        'src/pixelstitchifier/__main__.py',   # Entry point
    ]
    
    print("Building Windows executable...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print("Executable location: dist/pixelstitchifier.exe")
        print("\nTo distribute:")
        print("1. Copy dist/pixelstitchifier.exe to Windows computer")
        print("2. Run from command prompt: pixelstitchifier.exe image.jpg --dmc")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)

if __name__ == '__main__':
    build_exe()
