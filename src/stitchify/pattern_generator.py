"""PatternGenerator module - creates cross-stitch pattern images with grid."""
from typing import List, Tuple
from pathlib import Path
from PIL import Image, ImageDraw


class PatternGenerator:
    """Generates cross-stitch pattern images with grid and legend."""
    
    # Constants matching original implementation
    CELL_SIZE = 10  # Each cell is 10x10 pixels
    GRID_OFFSET = 10  # Offset from edge
    LEGEND_OFFSET = 20  # Space above legend
    LEGEND_LINE_HEIGHT = 15  # Height per legend line
    SYMBOL_OFFSET = 4  # Offset for symbol placement within cell
    
    MAJOR_GRID_INTERVAL = 100  # Major grid lines every 100px (10 stitches)
    MAJOR_LINE_WIDTH = 2
    MAJOR_LINE_COLOR = (0, 0, 0)  # Black
    MINOR_LINE_WIDTH = 1
    MINOR_LINE_COLOR = (128, 128, 128)  # Gray
    
    BACKGROUND_COLOR = (255, 255, 255)  # White
    TEXT_COLOR = (0, 0, 0)  # Black
    
    def __init__(self, width: int, height: int):
        """
        Initialize PatternGenerator.
        
        Args:
            width: Pattern width in stitches
            height: Pattern height in stitches
        """
        self.width = width
        self.height = height
        self.image = None
        self.draw = None
    
    def calculate_dimensions(self, legend_lines: int) -> Tuple[int, int]:
        """
        Calculate total pattern image dimensions.
        
        Args:
            legend_lines: Number of lines in legend
            
        Returns:
            Tuple of (width, height) in pixels
        """
        img_width = (self.width * self.CELL_SIZE) + self.GRID_OFFSET
        img_height = (
            (self.height * self.CELL_SIZE) + 
            self.LEGEND_OFFSET + 
            (self.LEGEND_LINE_HEIGHT * legend_lines)
        )
        return (img_width, img_height)
    
    def calculate_grid_offsets(self) -> Tuple[int, int]:
        """
        Calculate grid offsets for centering.
        
        Uses original algorithm: woff = int(((w)%10)/2)+1
        
        Returns:
            Tuple of (width_offset, height_offset)
        """
        woff = int(((self.width) % 10) / 2) + 1
        hoff = int(((self.height) % 10) / 2) + 1
        return (woff, hoff)
    
    def create_blank_pattern(self, legend_lines: int) -> Image.Image:
        """
        Create blank white pattern image.
        
        Args:
            legend_lines: Number of lines needed for legend
            
        Returns:
            PIL Image object
        """
        dimensions = self.calculate_dimensions(legend_lines)
        self.image = Image.new("RGB", dimensions, self.BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.image)
        return self.image
    
    def draw_grid(self):
        """Draw grid lines on the pattern."""
        if self.image is None:
            raise RuntimeError("Must create blank pattern before drawing grid")
        
        woff, hoff = self.calculate_grid_offsets()
        
        # Vertical grid lines
        for w in range(1, self.width + 1):
            posx = w * self.CELL_SIZE
            is_major = (posx - (woff * self.CELL_SIZE)) % self.MAJOR_GRID_INTERVAL == 0
            linecolor = self.MAJOR_LINE_COLOR if is_major else self.MINOR_LINE_COLOR
            linewidth = self.MAJOR_LINE_WIDTH if is_major else self.MINOR_LINE_WIDTH
            
            y_end = (self.height + 1) * self.CELL_SIZE
            self.draw.line(
                (posx, self.GRID_OFFSET, posx, y_end), 
                fill=linecolor, 
                width=linewidth
            )
        
        # Horizontal grid lines
        img_width = self.image.size[0]
        for h in range(1, self.height + 2):
            posy = h * self.CELL_SIZE
            is_major = (posy - (hoff * self.CELL_SIZE)) % self.MAJOR_GRID_INTERVAL == 0
            linecolor = self.MAJOR_LINE_COLOR if is_major else self.MINOR_LINE_COLOR
            linewidth = self.MAJOR_LINE_WIDTH if is_major else self.MINOR_LINE_WIDTH
            
            self.draw.line(
                (self.GRID_OFFSET, posy, img_width, posy),
                fill=linecolor,
                width=linewidth
            )
    
    def draw_symbols(self, symbol_grid: List[List[str]]):
        """
        Draw symbols on the pattern grid.
        
        Args:
            symbol_grid: 2D list of symbols (height x width)
        """
        if self.image is None:
            raise RuntimeError("Must create blank pattern before drawing symbols")
        
        char_positions = [x * self.CELL_SIZE + self.SYMBOL_OFFSET for x in range(1, max(self.height, self.width) + 1)]
        
        for row_idx, row in enumerate(symbol_grid):
            for col_idx, symbol in enumerate(row):
                # Skip transparent symbols (spaces)
                if symbol == " ":
                    continue
                
                try:
                    x_pos = char_positions[col_idx]
                    y_pos = char_positions[0] - self.SYMBOL_OFFSET + (row_idx * self.CELL_SIZE)
                    self.draw.text((x_pos, y_pos), symbol, fill=self.TEXT_COLOR)
                except (IndexError, TypeError):
                    # Handle edge cases gracefully
                    pass
    
    def add_legend(self, legend_text: str):
        """
        Add legend text below the pattern.
        
        Args:
            legend_text: Formatted legend string
        """
        if self.image is None:
            raise RuntimeError("Must create blank pattern before adding legend")
        
        legend_y = (self.height * self.CELL_SIZE) + self.LEGEND_OFFSET
        self.draw.text((20, legend_y), legend_text, fill=self.TEXT_COLOR)
    
    def save(self, output_path: Path):
        """
        Save pattern image to file.
        
        Args:
            output_path: Path where pattern image will be saved
        """
        if self.image is None:
            raise RuntimeError("No pattern to save - must create pattern first")
        
        self.image.save(output_path)
    
    def get_image(self) -> Image.Image:
        """
        Get the current pattern image.
        
        Returns:
            PIL Image object
        """
        return self.image
    
    def __repr__(self) -> str:
        return f"PatternGenerator(size={self.width}x{self.height})"
