# Stitchify

Convert images into professional cross-stitch patterns with automatic DMC thread matching and intelligent pixel art conversion.

**Version 0.5.0** - Now with high-quality photo-to-pixel-art conversion!

## Features

- ✅ Converts pixel-art images to cross-stitch patterns (1px = 1 stitch)
- ✅ 🎨 **NEW:** Photo-to-pixel-art conversion with professional quality
- ✅ 🧵 **NEW:** Automatic DMC thread color matching (454 colors)
- ✅ 🎭 Multi-stage art conversion with edge-preserving filters
- ✅ 🖼️ Quality presets for different image types (photo, landscape, portrait, detailed)
- ✅ Generates pattern grid with major/minor gridlines
- ✅ Symbol-based color mapping (A-Z, a-z)
- ✅ Comprehensive legend with stitch counts
- ✅ Modular, testable architecture
- ✅ Comprehensive test suite (TDD)
- ✅ Deterministic output (same input = same output)

## Requirements

**Core:**
- Python 3.8+
- Pillow (PIL)

**Optional (for high-quality photo conversion):**
- opencv-python - Edge-preserving bilateral filtering
- scikit-learn - Intelligent K-means color clustering

## Installation

### Basic Installation

```bash
# Core dependencies only
pip install Pillow

# With photo-to-pixel-art support (recommended)
pip install -r requirements-dev.txt
```

### Development Installation

```bash
# Install in editable mode with dev dependencies
pip install -e .
```

## Usage

### Command Line

**Simple Usage** (recommended):

```bash
# DMC matching enabled by default!
python3 stitchify your_image.png

# Or make it executable
./stitchify your_image.png

# Disable DMC matching if you want original colors
python3 stitchify your_image.png --no-dmc
```

**Photo to Pixel Art Conversion** (NEW):

```bash
# Convert photos to high-quality pixel art for cross-stitch
python3 stitchify photo.jpg --pixelate

# Use quality presets for different image types
python3 stitchify landscape.jpg --pixelate --preset landscape
python3 stitchify portrait.jpg --pixelate --preset portrait
python3 stitchify detailed_art.jpg --pixelate --preset detailed

# Custom pixel art width
python3 stitchify photo.jpg --pixelate --width 200
```

**Available Presets:**
- `photo` - General photos with balanced settings (default)
- `landscape` - Enhanced saturation and contrast for outdoor scenes
- `portrait` - Gentler smoothing to preserve skin tones
- `detailed` - Maximum edge preservation for intricate subjects

**Alternative entry points:**

```bash
# Using the full script name
python stitchify_main.py your_image.png

# Using as module
python -m stitchify your_image.png
python -m stitchify your_image.png --no-dmc
```

### As a Library

```python
from stitchify import StitchifyConverter

# With DMC color matching (default behavior)
converter = StitchifyConverter(use_dmc=True)
converter.convert("input.png", "output_pattern.png")

# Without DMC matching (original colors)
converter = StitchifyConverter(use_dmc=False)
converter.convert("input.png", "output_pattern.png")

# With custom DMC database
from stitchify import DMCMatcher
custom_dmc = DMCMatcher.from_json("custom_dmc_colors.json")
converter = StitchifyConverter(use_dmc=True, dmc_colors=custom_dmc.get_palette())
converter.convert("input.png", "output_pattern.png")
```

## Architecture

The codebase is now modular and well-tested:

```
src/stitchify/
├── __init__.py              # Package exports
├── image_loader.py          # Image loading and pixel access
├── color_processor.py       # Color conversion and filtering
├── symbol_mapper.py         # Symbol-to-color mapping
├── pattern_generator.py     # Pattern image generation with grid
├── dmc_matcher.py           # DMC thread color matching
├── thread_db_integration.py # Thread-database package integration
└── converter.py             # Main orchestrator class
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

## Testing

Comprehensive test suite with >90% coverage goal:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/stitchify --cov-report=html

# Run specific test module
pytest tests/test_dmc_matcher.py -v
```

See [tests/README.md](tests/README.md) for testing guide.

## DMC Color Matching

**DMC matching is now enabled by default!** Your patterns automatically use real DMC embroidery thread colors.

### Features

Stitchify automatically:

1. **Quantizes to DMC palette** - Uses all 454 authentic DMC thread colors
2. **Smart color selection** - PIL's adaptive algorithm picks the best colors for YOUR image
3. **Preserves subtlety** - Floyd-Steinberg dithering maintains color variations
4. **Symbol-constrained** - Auto-limits to 52 colors (A-Z, a-z symbols)
5. **Accurate matching** - Each image color maps to exactly one DMC thread

**No manual color reduction needed!** Feed any image (even with thousands of colors) and get a stitchable pattern.

Use `--no-dmc` flag if you want to use original image colors instead.

### How It Works

Two-stage intelligent quantization:

1. **Adaptive Analysis**: Analyzes your image to find the most important colors
2. **DMC Palette Mapping**: Maps those colors to nearest DMC threads from 454-color database
3. **Dithering**: Floyd-Steinberg dithering smooths transitions between colors

### Example

```bash
# Input: Photo with 12,213 colors - DMC matching automatic!
python3 stitchify sunset_photo.png

# Output: 17 optimal DMC thread colors
# DMC-352 Coral Light (10,397 stitches)
# DMC-3712 Salmon Medium (3,572 stitches)  
# DMC-309 Rose Dark (2,817 stitches)
# ... + 14 more carefully selected colors
```

### Programmatic Usage

```python
from stitchify import StitchifyConverter

converter = StitchifyConverter(use_dmc=True)
converter.convert("pixel_art.png")
```

### DMC Database

Uses the comprehensive [sharlagelfand/dmc](https://github.com/sharlagelfand/dmc) database:
- 454 authentic DMC thread colors
- Accurate RGB values from official DMC charts
- Color names and thread numbers

The generated pattern legend will include:
- DMC thread number (e.g., DMC-310)
- Thread color name (e.g., "Black")
- Hex color code
- Stitch count

## Photo to Pixel Art Conversion

Transform photos into high-quality cross-stitch patterns with professional pixel art conversion!

### Multi-Stage Pipeline

When using `--pixelate`, your photo goes through a sophisticated 5-stage process:

1. **Bilateral Filtering** - Edge-preserving smoothing that flattens colors while keeping sharp boundaries
2. **High-Quality Resize** - Lanczos interpolation for superior downsampling
3. **K-means Clustering** - Intelligent color grouping for cleaner regions
4. **Edge Enhancement** - Selective sharpening of important features
5. **Color Adjustment** - Saturation and contrast boost for vibrant stitching

### How It Works

```python
# Before: Photo with thousands of colors
# After:  Clean pixel art with 20-30 DMC thread colors

photo.jpg (1920x1080, 45,000 colors)
    ↓ --pixelate
pixel_art (128x72, 25 colors)
    ↓ automatic DMC quantization
pattern (25 DMC threads, ready to stitch!)
```

### Quality Presets

Different image types need different processing:

- **photo**: Balanced settings for general photography
  - Moderate bilateral filtering (d=9)
  - Edge enhancement: 30%
  - 64 intermediate colors via K-means
  
- **landscape**: Enhanced for outdoor scenes
  - Stronger saturation boost (1.2x)
  - Higher contrast (1.15x)
  - 48 intermediate colors
  
- **portrait**: Gentle processing for faces
  - Stronger bilateral smoothing (d=11)
  - Reduced edge enhancement (20%)
  - Preserves skin tones
  
- **detailed**: Maximum detail preservation
  - Minimal bilateral (d=5)
  - Strong edge enhancement (70%)
  - 72 intermediate colors

### Programmatic Usage

```python
from stitchify import ArtConverter, StitchifyConverter

# Method 1: Convert photo to pixel art, then to pattern
converter = ArtConverter(target_width=128, preset='landscape')
pixel_art = converter.convert('photo.jpg')
pixel_art.save('pixel_art.png')

# Method 2: One-step conversion
converter = StitchifyConverter(
    use_dmc=True,
    pixelate=True,
    pixelate_width=128,
    art_preset='portrait'
)
converter.convert('photo.jpg', 'pattern.png')

# Method 3: Convenience function
from stitchify import convert_to_pixel_art
pixel_art = convert_to_pixel_art('photo.jpg', width=128, preset='photo')
```

### Technical Details

**Bilateral Filter**: σ_color = 75, σ_space = 75
- Gaussian kernel that weights pixels by spatial proximity AND color similarity
- Smooths flat areas while preserving edges
- Essential for clean pixel art aesthetic

**K-means Clustering**: n_clusters = 48-72 (preset dependent)
- Groups perceptually similar colors before DMC quantization
- Creates cleaner color regions for better stitching
- Reduces visual noise from compression artifacts

**Floyd-Steinberg Dithering**: Error diffusion to adjacent pixels
- Creates illusion of intermediate colors
- Maintains perceived accuracy when quantizing to DMC palette
- Standard in professional pixel art tools

### Thread Database Integration

For comprehensive DMC color data (400+ colors), install `thread-database`:

```bash
pip install thread-database  # (when available)
```

Stitchify will automatically use it if installed, or fall back to a bundled minimal set.

## Backwards Compatibility

The original `stitchify.py` remains available for backwards compatibility. New development uses the modular architecture in `src/stitchify/`.

## Roadmap

- [x] Accept image name on command line
- [x] Create image from symbolized pixels
- [x] Add grid lines and edge labels to image
- [x] Add legend with stitch counts
- [x] **Correspond hex colors to DMC floss colors** ✨ NEW
- [x] **Modular architecture with comprehensive tests** ✨ NEW
- [ ] Change characters to extended symbols for readability
- [ ] Expand symbol set beyond 52 characters
- [ ] Add edge labels with stitch numbers
- [ ] GUI interface
- [ ] Support for other thread brands (Anchor, J&P Coats)
- [ ] Color reduction/palette optimization
- [ ] Custom color palettes

## How It Works

1. **ImageLoader** loads the pixel art image and converts to RGBA
2. **ColorProcessor** extracts unique colors and filters transparency
3. **SymbolMapper** assigns symbols (A-Z, a-z) to each unique color
4. **DMCMatcher** (optional) finds nearest DMC thread colors
5. **PatternGenerator** creates the output pattern:
   - Draws grid with major (every 10 stitches) and minor lines
   - Places symbols at each stitch position
   - Adds formatted legend with color info and stitch counts

## Contributing

This project now follows Test-Driven Development (TDD):

1. Write tests for new features first
2. Implement features to pass tests
3. Refactor while keeping tests green
4. Maintain >90% code coverage

## Author

Noëlle Anthony

## License

See LICENSE file for details.
