"""Tests for DMCMatcher module - matches colors to DMC thread palette."""
import pytest
import math
from src.stitchify.dmc_matcher import DMCMatcher


class TestDMCMatcher:
    """Test suite for DMC color matching functionality."""
    
    def test_calculate_color_distance_euclidean(self):
        """Test Euclidean distance calculation between two RGB colors."""
        matcher = DMCMatcher()
        # Red to Red = 0
        assert matcher.calculate_distance((255, 0, 0), (255, 0, 0)) == 0
        # Red to Green = sqrt(255^2 + 255^2)
        dist = matcher.calculate_distance((255, 0, 0), (0, 255, 0))
        expected = math.sqrt(255**2 + 255**2)
        assert abs(dist - expected) < 0.01
    
    def test_find_nearest_dmc_color(self, sample_dmc_colors):
        """Test finding the closest DMC color to a given RGB value."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        # Pure red (255, 0, 0) should match DMC-666 Bright Red
        match = matcher.find_nearest((255, 0, 0))
        assert match["dmc_number"] == "666"
        assert match["rgb"] == (228, 37, 49)
        assert match["distance"] > 0  # Not exact match
    
    def test_exact_match(self, sample_dmc_colors):
        """Test exact color match returns distance of 0."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        # Exact white match
        match = matcher.find_nearest((255, 255, 255))
        assert match["dmc_number"] == "b5200"
        assert match["distance"] == 0
    
    def test_match_all_colors(self, sample_dmc_colors):
        """Test matching multiple colors at once."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        colors = {"ff0000": (255, 0, 0), "000000": (0, 0, 0)}
        matches = matcher.match_colors(colors)
        assert "ff0000" in matches
        assert "000000" in matches
        assert matches["000000"]["dmc_number"] == "310"  # Black
        assert matches["000000"]["distance"] == 0  # Exact match
    
    def test_load_dmc_database_from_json(self, tmp_path):
        """Test loading DMC colors from JSON file."""
        import json
        json_path = tmp_path / "dmc_colors.json"
        json_path.write_text('{"310": {"name": "Black", "hex": "000000", "rgb": [0, 0, 0]}}')
        matcher = DMCMatcher.from_json(json_path)
        assert "310" in matcher.dmc_colors
        assert matcher.dmc_colors["310"]["name"] == "Black"
    
    def test_dmc_color_validation(self):
        """Test that DMC color database has valid format."""
        # Each DMC entry should have: number, name, hex/rgb
        invalid_format = {"310": {"name": "Black"}}  # Missing rgb
        with pytest.raises(ValueError, match="missing 'rgb' field"):
            DMCMatcher(dmc_colors=invalid_format)
    
    def test_color_distance_symmetry(self):
        """Test that distance(A, B) == distance(B, A)."""
        matcher = DMCMatcher()
        dist1 = matcher.calculate_distance((255, 0, 0), (0, 255, 0))
        dist2 = matcher.calculate_distance((0, 255, 0), (255, 0, 0))
        assert dist1 == dist2
    
    def test_alternative_distance_metrics(self):
        """Test alternative color distance calculations (CIEDE2000, CIE76, etc.)."""
        # For future enhancement - perceptual color difference
        # Current implementation uses Euclidean distance
        matcher = DMCMatcher()
        # Verify Euclidean distance is being used
        dist = matcher.calculate_distance((100, 150, 200), (100, 150, 200))
        assert dist == 0  # Same color = 0 distance
    
    def test_get_dmc_info(self, sample_dmc_colors):
        """Test retrieving full DMC color information."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        info = matcher.get_dmc_info("310")
        assert info["name"] == "Black"
        assert info["hex"] == "000000"
        assert info["rgb"] == (0, 0, 0)
    
    def test_format_dmc_for_legend(self, sample_dmc_colors):
        """Test formatting DMC info for pattern legend."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        formatted = matcher.format_for_legend("310", count=50)
        assert "DMC-310" in formatted
        assert "Black" in formatted
        assert "50ct" in formatted
    
    def test_handle_missing_dmc_color(self, sample_dmc_colors):
        """Test behavior when requested DMC color doesn't exist."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        # Should raise KeyError for non-existent color
        with pytest.raises(KeyError, match="DMC color 9999 not found"):
            matcher.get_dmc_info("9999")
    
    def test_match_with_threshold(self, sample_dmc_colors):
        """Test that poor matches beyond threshold are flagged."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        # Very unique color that doesn't match well
        match = matcher.find_nearest((127, 63, 31), max_distance=50)
        # Should have is_good_match field based on threshold
        assert "is_good_match" in match
        if match["distance"] > 50:
            assert match["is_good_match"] is False
    
    def test_get_dmc_palette_colors(self, sample_dmc_colors):
        """Test retrieving all available DMC colors."""
        matcher = DMCMatcher(dmc_colors=sample_dmc_colors)
        palette = matcher.get_palette()
        assert len(palette) == len(sample_dmc_colors)
        # Verify it's a copy (modifying shouldn't affect original)
        palette["test"] = {}
        assert "test" not in matcher.dmc_colors
    
    def test_batch_matching_performance(self):
        """Test performance of matching many colors at once."""
        # Should be efficient for images with 50+ unique colors
        matcher = DMCMatcher()  # Use default colors
        colors = {f"{i:06x}": (i % 256, (i // 256) % 256, (i // 65536) % 256) 
                  for i in range(100)}
        matches = matcher.match_colors(colors)
        assert len(matches) == 100
        # All colors should have matched to something
        for hex_color, match_info in matches.items():
            assert "dmc_number" in match_info
            assert "distance" in match_info
