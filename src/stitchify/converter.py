"""Main StitchifyConverter class - orchestrates the conversion workflow."""
from pathlib import Path
from typing import Optional, Union, Dict, List
import sys

from .image_loader import ImageLoader
from .color_processor import ColorProcessor
from .symbol_mapper import SymbolMapper
from .pattern_generator import PatternGenerator
from .dmc_matcher import DMCMatcher


class StitchifyConverter:
    """Main converter class that orchestrates cross-stitch pattern generation."""
    
    def __init__(
        self,
        use_dmc: bool = False,
        dmc_colors: Optional[Dict] = None,
        symbols: Optional[str] = None,
        pixelate: bool = False,
        pixelate_width: Optional[int] = None,
        art_preset: str = 'photo'
    ):
        """
        Initialize StitchifyConverter.
        
        Args:
            use_dmc: Whether to match colors to DMC threads
            dmc_colors: Optional custom DMC color database
            symbols: Optional custom symbol characters
            pixelate: Convert photo to pixel art before processing
            pixelate_width: Target width for pixel art (default: auto-calculated)
            art_preset: Quality preset for art conversion ('photo', 'landscape', 'portrait', 'detailed')
        """
        self.use_dmc = use_dmc
        self.pixelate = pixelate
        self.pixelate_width = pixelate_width
        self.art_preset = art_preset
        self.color_processor = ColorProcessor()
        self.symbol_mapper = SymbolMapper(symbols=symbols)
        self.dmc_matcher = DMCMatcher(dmc_colors=dmc_colors) if use_dmc else None
    
    def convert(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Convert an image to a cross-stitch pattern.
        
        Args:
            input_path: Path to input image
            output_path: Optional path for output pattern.
                        If None, generates from input filename
        
        Returns:
            Path to generated pattern image
        """
        input_path = Path(input_path)
        
        # Generate output path if not provided
        if output_path is None:
            output_path = self._generate_output_path(input_path)
        else:
            output_path = Path(output_path)
        
        # Step 1: Load image
        print(f"Loading image: {input_path}")
        
        # If pixelating, notify user
        if self.pixelate:
            print(f"Converting to pixel art (preset: {self.art_preset})...")
        
        # If using DMC, get palette for quantization
        dmc_palette = None
        max_colors = len(self.symbol_mapper.available_symbols)  # Limit to symbol pool
        
        if self.use_dmc and self.dmc_matcher:
            dmc_palette = self.dmc_matcher.get_palette()
            print(f"Quantizing to max {max_colors} colors from {len(dmc_palette)} DMC palette...")
        
        loader = ImageLoader(
            input_path,
            dmc_palette=dmc_palette,
            max_colors=max_colors,
            pixelate=self.pixelate,
            pixelate_width=self.pixelate_width,
            art_preset=self.art_preset
        )
        width, height = loader.get_dimensions()
        
        # Save pixelated image if pixelation was used
        if self.pixelate:
            pixelated_path = self._generate_pixelated_path(input_path)
            loader.image.save(pixelated_path)
            print(f"Saved pixelated image to: {pixelated_path}")
        
        # Step 2: Process colors
        print("Processing colors...")
        color_counts = self.color_processor.count_colors(loader)
        unique_colors = set(color_counts.keys())
        
        print(f"{len(unique_colors)} unique colors found")
        
        # Step 3: Match to DMC colors if requested
        dmc_mapping = None
        if self.use_dmc and self.dmc_matcher:
            print("Matching colors to DMC palette...")
            # Convert hex colors to RGB for matching
            colors_rgb = {
                hex_color: self.color_processor.hex_to_rgb(hex_color)
                for hex_color in unique_colors
            }
            dmc_mapping = self.dmc_matcher.match_colors(colors_rgb)
        
        # Step 4: Assign symbols to colors
        print("Assigning symbols...")
        for hex_color in sorted(unique_colors):
            self.symbol_mapper.assign_symbol(hex_color)
        
        # Step 5: Build symbol grid
        print("Building pattern grid...")
        symbol_grid = self._build_symbol_grid(loader)
        
        # Step 6: Generate legend
        if self.use_dmc and dmc_mapping:
            legend_entries = self.symbol_mapper.generate_legend_with_dmc(
                color_counts, dmc_mapping
            )
        else:
            legend_entries = self.symbol_mapper.generate_legend(color_counts)
        
        legend_text = self.symbol_mapper.format_legend(legend_entries)
        legend_line_count = len(legend_entries) // 3 + (1 if len(legend_entries) % 3 else 0)
        
        print(f"{len(legend_entries)} colors in legend")
        
        # Print DMC legend to console if DMC matching is enabled
        if self.use_dmc and dmc_mapping:
            print("\nDMC Color Matches:")
            for entry in legend_entries:
                print(f"  {entry}")
            
            # Show DMC summary - which actual threads are needed
            dmc_summary = {}
            for hex_color, dmc_info in dmc_mapping.items():
                dmc_num = dmc_info.get("dmc_number", "")
                dmc_name = dmc_info.get("name", "")
                count = color_counts.get(hex_color, 0)
                
                key = f"DMC-{dmc_num} {dmc_name}"
                if key not in dmc_summary:
                    dmc_summary[key] = {"count": 0, "colors": 0}
                dmc_summary[key]["count"] += count
                dmc_summary[key]["colors"] += 1
            
            print(f"\n{'='*60}")
            print("DMC THREAD SUMMARY (Actual threads needed):")
            print(f"{'='*60}")
            for dmc_thread, info in sorted(dmc_summary.items()):
                print(f"  {dmc_thread}:")
                print(f"    • {info['count']} total stitches")
                print(f"    • Represents {info['colors']} different image colors")
            print(f"{'='*60}")
            print(f"Total unique DMC threads needed: {len(dmc_summary)}")
            print(f"NOTE: Limited to {self.dmc_matcher.get_palette_size()} color palette")
            print(f"{'='*60}\n")
        
        # Step 7: Generate pattern image
        print("Generating pattern image...")
        generator = PatternGenerator(width, height)
        generator.create_blank_pattern(legend_line_count)
        generator.draw_grid()
        generator.draw_symbols(symbol_grid)
        generator.add_legend(legend_text)
        
        # Step 8: Save pattern
        generator.save(output_path)
        print(f"Saved pattern to: {output_path}")
        
        return output_path
    
    def _generate_output_path(self, input_path: Path) -> Path:
        """
        Generate output filename from input filename.
        
        Args:
            input_path: Input image path
            
        Returns:
            Output pattern path
        """
        # Split filename and extension
        name_parts = input_path.name.split(".")
        extension = name_parts[-1]
        base_name = ".".join(name_parts[:-1])
        
        # Generate: "filename_pattern.ext"
        output_name = f"{base_name}_pattern.{extension}"
        return input_path.parent / output_name
    
    def _generate_pixelated_path(self, input_path: Path) -> Path:
        """
        Generate pixelated image filename from input filename.
        
        Args:
            input_path: Input image path
            
        Returns:
            Pixelated image output path
        """
        # Split filename and extension
        name_parts = input_path.name.split(".")
        extension = name_parts[-1]
        base_name = ".".join(name_parts[:-1])
        
        # Generate: "filename_pixelated.ext"
        output_name = f"{base_name}_pixelated.{extension}"
        return input_path.parent / output_name
    
    def _build_symbol_grid(self, loader: ImageLoader) -> List[List[str]]:
        """
        Build 2D grid of symbols from image.
        
        Args:
            loader: ImageLoader instance
            
        Returns:
            2D list of symbols (height x width)
        """
        width, height = loader.get_dimensions()
        symbol_grid = []
        
        for y in range(height):
            row = []
            for x in range(width):
                rgba = loader.get_pixel(x, y)
                
                if self.color_processor.is_opaque(rgba):
                    hex_color = self.color_processor.rgba_to_hex(rgba)
                    symbol = self.symbol_mapper.color_to_symbol[hex_color]
                else:
                    symbol = self.symbol_mapper.get_symbol_for_transparent()
                
                row.append(symbol)
            symbol_grid.append(row)
        
        return symbol_grid


def main(image_path: Optional[str] = None):
    """
    Main entry point for command-line usage.
    
    Args:
        image_path: Optional path to image. If None, uses command-line args
    """
    # Get image path from command line or parameter
    if image_path is None:
        if len(sys.argv) >= 2:
            image_path = sys.argv[1]
        else:
            print("Usage: python -m stitchify <image_path> [options]")
            print("")
            print("Options:")
            print("  --no-dmc              Disable DMC color matching")
            print("  --pixelate            Convert photo to pixel art")
            print("  --preset PRESET       Art quality preset: photo, landscape, portrait, detailed")
            print("  --width WIDTH         Pixel art target width (default: auto)")
            print("")
            print("Examples:")
            print("  python3 stitchify photo.jpg --pixelate")
            print("  python3 stitchify landscape.jpg --pixelate --preset landscape")
            sys.exit(1)
    
    # Parse flags
    use_dmc = "--no-dmc" not in sys.argv
    pixelate = "--pixelate" in sys.argv
    
    # Parse preset
    art_preset = 'photo'
    if "--preset" in sys.argv:
        try:
            preset_idx = sys.argv.index("--preset")
            if preset_idx + 1 < len(sys.argv):
                art_preset = sys.argv[preset_idx + 1]
        except (ValueError, IndexError):
            pass
    
    # Parse width
    pixelate_width = None
    if "--width" in sys.argv:
        try:
            width_idx = sys.argv.index("--width")
            if width_idx + 1 < len(sys.argv):
                pixelate_width = int(sys.argv[width_idx + 1])
        except (ValueError, IndexError):
            pass
    
    try:
        converter = StitchifyConverter(
            use_dmc=use_dmc,
            pixelate=pixelate,
            pixelate_width=pixelate_width,
            art_preset=art_preset
        )
        output_path = converter.convert(image_path)
        print(f"\n{'='*60}")
        print(f"✓ Pattern generation complete!")
        print(f"{'='*60}")
        print(f"  Input:  {image_path}")
        print(f"  Output: {output_path}")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
