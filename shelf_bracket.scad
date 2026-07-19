include <BOSL2/std.scad>

include <constants.scad>
use <hanger.scad>


/* [Primary parameters] */
// Which variant to use
variant = 0; // [0: Original, 1: Thicker cleats]

// Added to hangers to allow for easier insertion and removal
hanger_tolerance = 0.15;

/* [Bracket parameters] */
// Bracket height in GOEWS vertical units. The top aligns with the bottom of the above tile
height_units = 1;

// Bracket depth in mm. Total depth from wall to front of bracket, includes plate thickness
depth = 120;

// Total bracket width in mm
width = 41.5;

// Thickness of the top surface in mm. Set to 0 to disable
top_thickness = 3;

// Plate thickness in mm
plate_thickness = 3;

// Number of diagonal supports, distributed across the width. If set to one, the support will be the entire width
supports = 2;

// Support thickness in mm. Only used when number of supports is > 0, otherwise support will match the width
support_thickness = 4;

// Rear gusset between back wall and top, in mm. Set to 0 to disable
rear_gusset = 2;

// Side gusset between each support and top, in mm. Set to 0 to disable
support_gusset = 2;

// Top mounting holes
top_mounting_holes = 0;

// Diameter of top mounting holes
top_mounting_hole_diameter = 4;

// Diameter of clearance for the underside of the top mounting holes
top_mounting_hole_clearance_diameter = 8;

// End offset of top mounting holes
top_mounting_hole_end_offset = 25;

// Enable bolt hole for mounting
bolt_hole = true;

// Depth of bolt hole head clearance
bolt_hole_head_clearance_depth = 14;


/* [Hidden] */
$fa=0.5;
$fs=0.5;


module shelf_bracket(
    height_units=1,
    depth=30,
    width=83.5,
    top_thickness=4,
    plate_thickness=3,
    supports=2,
    support_thickness=4,
    rear_gusset=2,
    support_gusset=2,
    bolt_hole=true,
    hanger_tolerance=0.15,
    variant=variant_original
) {
    height = height_units * grid_tile_height;
    hanger_plate_offset = get_hanger_plate_offset(variant, hanger_tolerance);
    hanger_total_thickness = hanger_thickness + hanger_plate_offset;

    hanger_units = get_hanger_units_from_width(width);
    total_plate_width = hanger_units * plate_width;

    // Bracket body height is fixed at grid_tile_height (top aligned with bottom of tile above)
    extend_bottom = max(0, height - grid_tile_height);

    // Center bracket body on hanger plate
    x_offset = (total_plate_width - width) / 2;
    y_offset = hanger_total_thickness;

    support_height = height - top_thickness;
    support_depth = depth - plate_thickness;

    bracket_angle = atan2(support_height + overcut, depth);

    // Rotate to match the cut angle and make it printable
    rotate([-bracket_angle, 0, 0]) {
        difference() {
            union() {
                hanger_plate(
                    variant=variant,
                    hanger_units=hanger_units,
                    hanger_tolerance=hanger_tolerance,
                    extend_bottom=extend_bottom,
                    bolt_notch=bolt_hole
                );

                // Back wall
                translate([x_offset, y_offset, 0])
                    cuboid(
                        [width, plate_thickness, height],
                        anchor=BOTTOM+FRONT+LEFT
                    );

                // Top
                if (top_thickness > 0) {
                    translate([x_offset, y_offset + plate_thickness, height - top_thickness])
                        cuboid(
                            [width, depth - plate_thickness, top_thickness],
                            anchor=BOTTOM+FRONT+LEFT
                        );
                }

                // Supports
                if (supports > 1) {
                    support_interval = (width - support_thickness) / (supports - 1);
                    for (i = [0:supports - 1]) {
                        support_x = x_offset + (i * support_interval) + support_thickness / 2;
                        translate([support_x, y_offset + plate_thickness, height - top_thickness]) {
                            wedge([support_thickness, support_depth, support_height], anchor=FRONT+CENTER+BOTTOM, orient=DOWN);

                            // Support gussets
                            if (top_thickness > 0 && support_gusset > 0) {
                                if (i > 0)
                                    translate([-support_thickness / 2, 0, 0])
                                        wedge([support_depth - overcut, rear_gusset, rear_gusset], anchor=FRONT+RIGHT+BOTTOM, orient=DOWN, spin=270);
                                if (i < (supports - 1))
                                    translate([support_thickness / 2, 0, 0])
                                        wedge([support_depth - overcut, rear_gusset, rear_gusset], anchor=FRONT+LEFT+BOTTOM, orient=DOWN, spin=90);
                            }
                        }
                    }
                } else {
                    // Single support will use full width
                    translate([x_offset + (width / 2), y_offset + plate_thickness, height - top_thickness]) {
                        wedge([width, support_depth, support_height], anchor=FRONT+CENTER+BOTTOM, orient=DOWN);
                    }
                }

                // Rear gusset
                if (top_thickness > 0 && rear_gusset > 0) {
                    translate([x_offset, y_offset + plate_thickness, height - top_thickness])
                        wedge([width, rear_gusset, rear_gusset], anchor=FRONT+RIGHT+BOTTOM, orient=DOWN);
                }
            }

            // Top mounting holes
            if (top_mounting_holes == 1) {
                // Use end_offset from the front
                translate([x_offset + width / 2, y_offset + depth - top_mounting_hole_end_offset, height + overcut])
                    zcyl(d=top_mounting_hole_diameter, l=top_thickness + double_overcut, anchor=TOP);
                translate([x_offset + width / 2, y_offset + depth - top_mounting_hole_end_offset, height - top_thickness])
                    zcyl(d=top_mounting_hole_clearance_diameter, l=height, anchor=TOP);
            }
            else if (top_mounting_holes > 0) {
                // Use end offset from the front and back and distribute
                top_mounting_hole_gap = (depth - 2 * top_mounting_hole_end_offset) / (top_mounting_holes - 1);
                for (i = [0:top_mounting_holes - 1]) {
                    translate([x_offset + width / 2, y_offset + top_mounting_hole_end_offset + i * top_mounting_hole_gap, height + overcut])
                        zcyl(d=top_mounting_hole_diameter, l=top_thickness + double_overcut, anchor=TOP);
                    translate([x_offset + width / 2, y_offset + top_mounting_hole_end_offset + i * top_mounting_hole_gap, height - top_thickness])
                        zcyl(d=top_mounting_hole_clearance_diameter, l=height, anchor=TOP);
                }
            }

            // Bolt clearance hole
            if (bolt_hole) {
                for (i = [0:hanger_units - 1]) {
                    bolt_x = plate_width / 2 + plate_width * i;
                    bolt_z = plate_cutout_y_offset + extend_bottom;

                    // Through-hole
                    translate([bolt_x, y_offset + depth + overcut, bolt_z])
                        ycyl(
                            d=thread_diameter - thread_tolerance,
                            h=depth + double_overcut,
                            anchor=BACK
                        );

                    // Head clearance
                    clearance_depth = supports > 1 ? bolt_hole_head_clearance_depth : depth;
                    translate([bolt_x, y_offset + plate_thickness, bolt_z])
                        ycyl(
                            d=hanger_bolt_notch_head_clearance_diameter,
                            h=clearance_depth,
                            anchor=FRONT
                        );
                }
            }

            // Flatten bottom to make it easier to print and cut off the support gussets
            translate([total_plate_width / 2, y_offset, - overcut])
                wedge([total_plate_width, depth, support_height + overcut], spin=180, anchor=CENTER+BOTTOM+BACK);
        }
    }
}


shelf_bracket(
    height_units=height_units,
    depth=depth,
    width=width,
    top_thickness=top_thickness,
    plate_thickness=plate_thickness,
    supports=supports,
    support_thickness=support_thickness,
    rear_gusset=rear_gusset,
    support_gusset=support_gusset,
    bolt_hole=bolt_hole,
    hanger_tolerance=hanger_tolerance,
    variant=variant
);
