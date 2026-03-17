# Pixelstitchifier

> *For Andrea because she makes my heart sing*

Transform any image into a professional cross-stitch pattern with real DMC thread colors. Perfect for photos of loved ones, pets, landscapes, or pixel art.

## 📥 Download for Windows

**No technical knowledge required!** Just download and double-click:

### 👉 **[Download Windows App](../../releases/latest)** 👈

1. Download `pixelstitchifier-gui.exe`
2. Double-click to open
3. Select your photo
4. Click "Generate Pattern"
5. Start stitching!

Your pattern will be saved next to your original image.

> **Note:** Windows may show a security warning on first run. Click "More info" → "Run anyway". This is normal for applications that aren't code-signed.

## 🎨 How to Use

The graphical interface makes it simple to create patterns:

![screenshot](screenshot.png)

### Options:

- **Match to DMC thread colors** ✅ *(Recommended)*  
  Converts image colors to real DMC embroidery thread colors (454 official colors). Your pattern will tell you exactly which thread to buy.

- **Convert photo to pixel art first** 🎨 *(Recommended for photos)*  
  Turns photos into beautiful pixel art before making the pattern. Skip this if you're already starting with pixel art.

- **Presets** 🎯  
  - **photo** - General photos (family, pets, etc.)
  - **landscape** - Outdoor scenes with rich color
  - **portrait** - People and faces (gentler processing)
  - **detailed** - Intricate images needing fine details

### Output:

After generating, you'll get:

1. **`yourimage_pattern.png`** - Your cross-stitch pattern with grid, symbols, DMC legend, and stitch counts
2. **`yourimage_pixelated.png`** - The intermediate pixel art (if you used photo conversion)

## 💻 Command Line & Python Library

<details>
<summary><strong>Click to expand developer instructions</strong></summary>

### Installation

```bash
git clone https://github.com/treeherder/pixelstitchifier.git
cd pixelstitchifier
pip install -r requirements-dev.txt
```

**Requirements:** Python 3.8+

### Command Line Usage

```bash
# Basic usage (DMC matching enabled by default)
python3 pixelstitchifier your_image.png

# For photos: convert to pixel art first
python3 pixelstitchifier photo.jpg --pixelate --preset photo

# All options
python3 pixelstitchifier IMAGE [OPTIONS]

Options:
  --pixelate           Convert photo to pixel art before making pattern
  --preset PRESET      Quality preset: photo, landscape, portrait, detailed
  --width WIDTH        Pixel art width in stitches (default: varies by preset)
  --no-dmc            Use original colors instead of DMC thread colors
```

### Python Library

```python
from src.pixelstitchifier.converter import PixelstitchifierConverter

converter = PixelstitchifierConverter(
    use_dmc=True,
    pixelate=True,
    art_preset='photo'
)

output_path = converter.convert("my_photo.jpg")
```

</details>

## 🎯 What Makes This Different

This project builds on [Noëlle Anthony](https://github.com/NoelleDL)'s original [`stitchify`](https://github.com/NoelleDL/stitchify), which converted pixel art into cross-stitch patterns.

### New Features:

- **Photo-to-Pixel-Art Conversion** - Intelligent processing turns photos into stitchable pixel art
- **DMC Thread Matching** - Automatic matching to all 454 official DMC colors
- **Quality Presets** - Optimized settings for photos, landscapes, portraits, and detailed images
- **GUI Application** - Simple point-and-click interface
- **Windows Executable** - No installation required
- **Advanced Processing** - Edge-preserving filters, smart color clustering, dithering
- **Comprehensive Testing** - 61% test coverage and growing

Noëlle's original README said: *"TODO: Correspond hex colors to floss colors, where possible. (Maybe) add GUI."*

This fork makes that vision a reality. **Thank you, Noëlle, for the inspiration!**

## 📚 Technical Details

<details>
<summary><strong>For the technically curious...</strong></summary>

### Architecture

- Modular, testable design with clear separation of concerns
- Type hints throughout
- Deterministic output (same input always produces same result)
- 61% test coverage with pytest

### Image Processing Pipeline

1. **Load & Validate** - Check image format and accessibility
2. **Pixelate** *(optional)*:
   - Bilateral filtering (edge-preserving smoothing)
   - K-means color clustering (48-72 clusters by preset)
   - Preset-specific adjustments (saturation, contrast, edge enhancement)
3. **DMC Matching** *(optional)* - Map to 454 DMC thread colors
4. **Symbol Assignment** - Assign A-Z symbols to each color
5. **Pattern Generation** - Create grid with symbols, legend, and stitch counts

### Code Structure

```
src/pixelstitchifier/
├── converter.py             Main orchestrator
├── image_loader.py          Image loading and validation
├── color_processor.py       Color quantization  
├── symbol_mapper.py         Color-to-symbol mapping
├── pattern_generator.py     Pattern with grid and legend
├── dmc_matcher.py           DMC thread matching
├── art_converter.py         Photo-to-pixel-art conversion
└── dmc_colors.csv           DMC color database (454 colors)
```

### Dependencies

- `Pillow` - Core image processing
- `opencv-python` - Bilateral filtering
- `scikit-learn` - K-means clustering

</details>

## Credits

**Original Project:** [`stitchify`](https://github.com/NoelleDL/stitchify) by Noëlle Anthony

**This Fork:** Extensively modified by [treeherder](https://github.com/treeherder) (Brendan Reddy-Best)

**DMC Database:** Sharla Gelfand's [`dmc`](https://github.com/sharlagelfand/dmc) project

## License

MIT

---

## 💖 Made With Love

This project exists because someone special deserves beautiful, handmade gifts. May your stitching bring as much joy as the photos that inspire your patterns.

Happy stitching! 🧵✨
