# Stitchify Testing Guide

## Overview

This directory contains comprehensive tests for the stitchify cross-stitch pattern generator, following Test-Driven Development (TDD) principles.

## Test Statistics

- **Total Tests**: 97 (95 passing, 2 skipped)
- **Overall Coverage**: 61%
- **Unit Tests**: 83 tests across 7 modules
- **Integration Tests**: 14 end-to-end workflow tests

### Module Coverage

| Module | Coverage | Tests | Status |
|--------|----------|-------|--------|
| color_processor.py | 100% | 11 | ✅ Complete |
| symbol_mapper.py | 98% | 12 | ✅ Complete |
| dmc_matcher.py | 93% | 14 | ✅ Complete |
| pattern_generator.py | 92% | 12 | ✅ Complete |
| art_converter.py | 91% | 12 | ✅ Complete |
| image_loader.py | 53% | 11 | ⚠️ Partial |
| converter.py | 9% | - | ℹ️ Via integration |
| thread_db_integration.py | 0% | 9 | ℹ️ External |

## Test Structure

```
tests/
├── __init__.py                      # Test package initialization
├── conftest.py                      # Pytest fixtures and test helpers
├── README.md                        # This file
├── unit/                            # Unit tests (focused, isolated)
│   ├── __init__.py
│   ├── test_art_converter.py       # Photo-to-pixel-art conversion tests
│   ├── test_color_processor.py     # Color conversion and processing tests
│   ├── test_dmc_matcher.py         # DMC color matching tests
│   ├── test_image_loader.py        # Image loading and validation tests
│   ├── test_pattern_generator.py   # Pattern image generation tests
│   ├── test_symbol_mapper.py       # Symbol assignment and legend tests
│   └── test_thread_database.py     # Thread-database integration tests
└── integration/                     # Integration tests (end-to-end)
    ├── __init__.py
    └── test_integration.py          # Full workflow integration tests
```

## Running Tests

### Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run Only Unit Tests

```bash
pytest tests/unit/
```

### Run Only Integration Tests

```bash
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=src/stitchify --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Run Specific Test Files

```bash
pytest tests/unit/test_image_loader.py
pytest tests/unit/test_dmc_matcher.py -v
pytest tests/integration/test_integration.py
```

### Run Specific Tests

```bash
pytest tests/integration/test_integration.py::TestStitchifyIntegration::test_simple_workflow_without_dmc
```

## Test Organization

### Unit Tests (`tests/unit/`)

Focused, isolated tests for individual modules and classes.

- **test_art_converter.py**: Tests for ArtConverter class (photo-to-pixel-art)
  - Bilateral filtering
  - K-means color simplification
  - Quality presets
  - Smart resizing with aspect ratio

- **test_color_processor.py**: Tests for ColorProcessor class
  - RGBA to hex conversion
  - Hex to RGB conversion
  - Transparency filtering
  - Color counting

- **test_dmc_matcher.py**: Tests for DMCMatcher class
  - Color distance calculations
  - Nearest color matching
  - DMC database loading
  - Batch color matching

- **test_image_loader.py**: Tests for ImageLoader class
  - Loading various image formats
  - Pixel data access
  - Dimension handling
  - Error cases

- **test_pattern_generator.py**: Tests for PatternGenerator class
  - Grid line drawing
  - Symbol placement
  - Legend formatting
  - Dimension calculations

- **test_symbol_mapper.py**: Tests for SymbolMapper class
  - Symbol assignment
  - Legend generation
  - DMC integration in legends
  - Symbol exhaustion handling

- **test_thread_database.py**: Tests for thread-database integration
  - Package availability detection
  - Format conversion
  - Fallback behavior

### Integration Tests (`tests/integration/`)

End-to-end workflow tests that exercise the complete system.

- **test_integration.py**: Full pipeline integration tests
  - Complete conversion workflow
  - CLI interface
  - Error handling
  - Performance benchmarks
  - Backwards compatibility

## Test Fixtures

Located in `conftest.py`:

- `test_images_dir`: Temporary directory for test images
- `simple_rgba_image`: 3x3 image with known colors
- `image_with_transparency`: Mixed transparent/opaque pixels
- `single_color_image`: Single-color edge case
- `large_image`: Performance testing
- `many_colors_image`: Symbol overflow testing
- `sample_dmc_colors`: Mock DMC color database

## Writing New Tests

### Example Test

```python
def test_feature_name(fixture_name):
    """Test description."""
    # Arrange
    loader = ImageLoader(fixture_name)
    
    # Act
    result = loader.get_dimensions()
    
    # Assert
    assert result == (expected_width, expected_height)
```

### Test Naming Convention

- Tests should start with `test_`
- Use descriptive names: `test_load_valid_png` not `test_1`
- Group related tests in classes

### Test Categories

- **Happy path**: Normal expected usage
- **Edge cases**: Boundary conditions
- **Error cases**: Invalid inputs, exceptions
- **Performance**: Large inputs, stress tests

## Development Workflow

1. Write failing test for new feature
2. Implement minimal code to pass test
3. Refactor while keeping tests green
4. Add more tests for edge cases
5. Document behavior in test docstrings

## Continuous Integration

Tests are designed to run in CI environments:
- All tests should be deterministic
- No external dependencies required
- Fixtures create temporary files (auto-cleaned)

## Coverage Goals

- Target: >90% code coverage
- All public APIs must be tested
- Critical paths require integration tests
- Edge cases should be documented in tests

## Troubleshooting

### Tests Not Found

```bash
# Make sure you're in the project root
cd /home/fiver/projects/stitchify
pytest
```

### Import Errors

```bash
# Install package in editable mode
pip install -e .
```

### Fixture Issues

Check that `conftest.py` is being loaded:
```bash
pytest --fixtures
```

## Future Test Additions

- Performance benchmarks
- Visual regression tests (compare generated patterns)
- Stress tests for extreme image sizes
- Thread safety tests (if concurrency added)
