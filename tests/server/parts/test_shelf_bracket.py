"""Tests for server.parts.shelf_bracket module."""

import pytest
from pydantic import ValidationError
from server.parts.shelf_bracket import (
    ShelfBracketDefinition, make_shelf_bracket_filename,
)
from server.enums import Variant


class TestShelfBracketDefinition:
    """Tests for ShelfBracketDefinition model."""

    def test_default_values(self):
        """Test that default values are set correctly."""
        body = ShelfBracketDefinition()
        assert body.height_units == 1
        assert body.depth == 120
        assert body.width == 41.5
        assert body.top_thickness == 3
        assert body.plate_thickness == 3
        assert body.supports == 2
        assert body.support_thickness == 4
        assert body.rear_gusset == 2
        assert body.support_gusset == 2
        assert body.top_mounting_holes == 0
        assert body.top_mounting_hole_diameter == 4
        assert body.top_mounting_hole_clearance_diameter == 8
        assert body.top_mounting_hole_end_offset == 25
        assert body.bolt_hole is True
        assert body.bolt_hole_head_clearance_depth == 14
        assert body.hanger_tolerance == 0.15
        assert body.variant == Variant.ORIGINAL

    def test_validation_height_units_gt_zero(self):
        """Test that height_units must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(height_units=0)

    def test_validation_depth_gt_zero(self):
        """Test that depth must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(depth=0)

    def test_validation_width_gt_zero(self):
        """Test that width must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(width=0)

    def test_validation_top_thickness_gt_zero(self):
        """Test that top_thickness must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(top_thickness=0)

    def test_validation_plate_thickness_gt_zero(self):
        """Test that plate_thickness must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(plate_thickness=0)

    def test_validation_supports_gt_zero(self):
        """Test that supports must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(supports=0)

    def test_validation_support_thickness_gt_zero(self):
        """Test that support_thickness must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(support_thickness=0)

    def test_validation_rear_gusset_ge_zero(self):
        """Test that rear_gusset must be greater than or equal to zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(rear_gusset=-1)

    def test_validation_support_gusset_ge_zero(self):
        """Test that support_gusset must be greater than or equal to zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(support_gusset=-1)

    def test_validation_top_mounting_hole_diameter_gt_zero(self):
        """Test that top_mounting_hole_diameter must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(top_mounting_hole_diameter=0)

    def test_validation_top_mounting_hole_clearance_diameter_gt_zero(self):
        """Test that top_mounting_hole_clearance_diameter must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(top_mounting_hole_clearance_diameter=0)

    def test_validation_top_mounting_hole_end_offset_gt_zero(self):
        """Test that top_mounting_hole_end_offset must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(top_mounting_hole_end_offset=0)

    def test_validation_bolt_hole_head_clearance_depth_gt_zero(self):
        """Test that bolt_hole_head_clearance_depth must be greater than zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(bolt_hole_head_clearance_depth=0)

    def test_validation_hanger_tolerance_ge_zero(self):
        """Test that hanger_tolerance must be greater than or equal to zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(hanger_tolerance=-0.1)

    def test_validation_top_mounting_holes_ge_zero(self):
        """Test that top_mounting_holes must be greater than or equal to zero."""
        with pytest.raises(ValidationError):
            ShelfBracketDefinition(top_mounting_holes=-1)


class TestMakeShelfBracketFilename:
    """Tests for make_shelf_bracket_filename function."""

    def test_default_shelf_bracket(self):
        """Test filename for default shelf bracket."""
        body = ShelfBracketDefinition()
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original.stl"

    def test_custom_dimensions(self):
        """Test filename with custom dimensions."""
        body = ShelfBracketDefinition(height_units=2, depth=80)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-2x80.0x41.5-original.stl"

    def test_thicker_cleats_variant(self):
        """Test filename with thicker cleats variant."""
        body = ShelfBracketDefinition(variant=Variant.THICKER_CLEATS)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-thicker_cleats.stl"

    def test_custom_width(self):
        """Test filename with custom width."""
        body = ShelfBracketDefinition(width=83.5)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x83.5-original.stl"

    def test_custom_top_thickness(self):
        """Test filename with custom top_thickness."""
        body = ShelfBracketDefinition(top_thickness=5)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-top_thickness_5.0.stl"

    def test_custom_plate_thickness(self):
        """Test filename with custom plate_thickness."""
        body = ShelfBracketDefinition(plate_thickness=4)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-plate_thickness_4.0.stl"

    def test_custom_supports(self):
        """Test filename with custom number of supports."""
        body = ShelfBracketDefinition(supports=3)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-supports_3.stl"

    def test_custom_support_thickness(self):
        """Test filename with custom support_thickness."""
        body = ShelfBracketDefinition(support_thickness=5)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-support_thickness_5.0.stl"

    def test_custom_rear_gusset(self):
        """Test filename with custom rear_gusset."""
        body = ShelfBracketDefinition(rear_gusset=3)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-rear_gusset_3.0.stl"

    def test_custom_support_gusset(self):
        """Test filename with custom support_gusset."""
        body = ShelfBracketDefinition(support_gusset=0)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-support_gusset_0.0.stl"

    def test_custom_hanger_tolerance(self):
        """Test filename with custom hanger_tolerance."""
        body = ShelfBracketDefinition(hanger_tolerance=0.2)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-hanger_tolerance_0.2.stl"

    def test_bolt_hole_disabled(self):
        """Test filename with bolt_hole disabled."""
        body = ShelfBracketDefinition(bolt_hole=False)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-bolt_hole.stl"

    def test_custom_top_mounting_holes(self):
        """Test filename with top_mounting_holes enabled."""
        body = ShelfBracketDefinition(top_mounting_holes=2)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-top_mounting_holes_2.stl"

    def test_custom_top_mounting_hole_diameter(self):
        """Test filename with custom top_mounting_hole_diameter."""
        body = ShelfBracketDefinition(top_mounting_holes=1, top_mounting_hole_diameter=5)
        assert make_shelf_bracket_filename(body) == "shelf-bracket-1x120x41.5-original-top_mounting_holes_1_top_mounting_hole_diameter_5.0.stl"

    def test_default_bolt_hole_not_in_filename(self):
        """Test that default bolt_hole=True doesn't appear in filename."""
        body = ShelfBracketDefinition()
        assert "bolt_hole" not in make_shelf_bracket_filename(body)

    def test_default_top_mounting_holes_not_in_filename(self):
        """Test that default top_mounting_holes=0 doesn't appear in filename."""
        body = ShelfBracketDefinition()
        assert "top_mounting_holes" not in make_shelf_bracket_filename(body)

    def test_multiple_custom_options(self):
        """Test filename with multiple custom options."""
        body = ShelfBracketDefinition(
            width=83.5,
            supports=3,
            bolt_hole=False,
        )
        filename = make_shelf_bracket_filename(body)
        assert filename == "shelf-bracket-1x120x83.5-original-supports_3_bolt_hole.stl"
