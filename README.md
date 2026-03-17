# Stitchify

Convert pixel art images into professional cross-stitch patterns with optional DMC thread color matching.

**Version 0.4.0** - Now with modular architecture and comprehensive testing!

## Features

- ✅ Converts pixel-art images to cross-stitch patterns (1px = 1 stitch)
- ✅ Generates pattern grid with major/minor gridlines
- ✅ Symbol-based color mapping (A-Z, a-z)
- ✅ Comprehensive legend with stitch counts
- ✅ **NEW:** DMC thread color matching
- ✅ **NEW:** Modular, testable architecture
- ✅ **NEW:** Comprehensive test suite (TDD)
- ✅ **NEW:** Thread-database integration support
- ✅ Deterministic output (same input = same output)

## Requirements

- Python 3.8+
- Pillow (PIL)

## Installation

### Basic Installation

```bash
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
