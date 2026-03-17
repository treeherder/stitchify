#!/bin/bash
# Build GUI version for Windows distribution
# Run this on Windows (or Linux with Wine) for best compatibility

echo "🔨 Building pixelstitchifier GUI for Windows..."
echo ""

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Build the GUI executable
pyinstaller \
    --onefile \
    --windowed \
    --name=pixelstitchifier-gui \
    --add-data="src/pixelstitchifier/dmc_colors.csv:src/pixelstitchifier" \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=cv2 \
    --hidden-import=sklearn \
    --hidden-import=numpy \
    --collect-all=PIL \
    --collect-all=cv2 \
    --collect-all=sklearn \
    pixelstitchifier_gui.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📦 Executable created: dist/pixelstitchifier-gui.exe"
    echo "📊 Size: $(du -h dist/pixelstitchifier-gui.exe | cut -f1)"
    echo ""
    echo "📤 Distribution:"
    echo "   1. Test the .exe on Windows"
    echo "   2. Zip it: zip pixelstitchifier-gui-windows.zip dist/pixelstitchifier-gui.exe"
    echo "   3. Upload to GitHub Releases"
    echo ""
    echo "🎯 Usage: Just double-click pixelstitchifier-gui.exe on Windows!"
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
