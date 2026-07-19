from pydantic import BaseModel, Field
from sanic import response
from sanic.request import Request
from sanic_ext import openapi, validate
from typing import Annotated

from server.openscad import build
from server.enums import Variant
from server.api import api_bp


@openapi.component
class ShelfBracketDefinition(BaseModel):
    height_units: Annotated[int, Field(gt=0, description="Bracket height in GOEWS vertical units")] = 1
    depth: Annotated[float, Field(gt=0, description="Total depth from wall to front of bracket in mm")] = 120
    width: Annotated[float, Field(gt=0, description="Total bracket width in mm")] = 41.5
    top_thickness: Annotated[float, Field(gt=0, description="Thickness of the top surface in mm")] = 3
    plate_thickness: Annotated[float, Field(gt=0, description="Plate thickness in mm")] = 3
    supports: Annotated[int, Field(gt=0, description="Number of diagonal supports")] = 2
    support_thickness: Annotated[float, Field(gt=0, description="Support thickness in mm")] = 4
    rear_gusset: Annotated[float, Field(ge=0, description="Rear gusset between back wall and top in mm. Set to 0 to disable")] = 2
    support_gusset: Annotated[float, Field(ge=0, description="Side gusset between each support and top in mm. Set to 0 to disable")] = 2
    top_mounting_holes: Annotated[int, Field(ge=0, description="Number of top mounting holes")] = 0
    top_mounting_hole_diameter: Annotated[float, Field(gt=0, description="Diameter of top mounting holes in mm")] = 4
    top_mounting_hole_clearance_diameter: Annotated[float, Field(gt=0, description="Clearance diameter for underside of top mounting holes in mm")] = 8
    top_mounting_hole_end_offset: Annotated[float, Field(gt=0, description="End offset of top mounting holes in mm")] = 25
    bolt_hole: Annotated[bool, Field(description="Enable bolt hole for mounting")] = True
    bolt_hole_head_clearance_depth: Annotated[float, Field(gt=0, description="Depth of bolt hole head clearance in mm")] = 14
    hanger_tolerance: Annotated[float, Field(ge=0)] = 0.15
    variant: Variant = Variant.ORIGINAL


def make_shelf_bracket_filename(body: ShelfBracketDefinition) -> str:
    parts = ["shelf-bracket", f"{body.height_units}x{body.depth}"]
    parts.append("original" if body.variant.to_int() == 0 else "thicker_cleats")

    options = []
    for name, info in type(body).model_fields.items():
        if name in ("height_units", "depth", "variant"):
            continue
        val = getattr(body, name)
        if val != info.default:
            if isinstance(val, bool):
                options.append(name)
            else:
                options.append(f"{name}_{val}")

    if options:
        parts.append("_".join(options))

    return "-".join(parts) + ".stl"


@api_bp.post("/shelf_bracket")
@openapi.body(ShelfBracketDefinition)
@openapi.response(200, "model/stl")
@openapi.description("Create a GOEWS shelf bracket")
@validate(json=ShelfBracketDefinition)
async def shelf_bracket(request: Request, body: ShelfBracketDefinition):
    filename = make_shelf_bracket_filename(body)
    return response.raw(
        await build(
            "shelf_bracket.scad",
            height_units=body.height_units,
            depth=body.depth,
            width=body.width,
            top_thickness=body.top_thickness,
            plate_thickness=body.plate_thickness,
            supports=body.supports,
            support_thickness=body.support_thickness,
            rear_gusset=body.rear_gusset,
            support_gusset=body.support_gusset,
            top_mounting_holes=body.top_mounting_holes,
            top_mounting_hole_diameter=body.top_mounting_hole_diameter,
            top_mounting_hole_clearance_diameter=body.top_mounting_hole_clearance_diameter,
            top_mounting_hole_end_offset=body.top_mounting_hole_end_offset,
            bolt_hole=body.bolt_hole,
            bolt_hole_head_clearance_depth=body.bolt_hole_head_clearance_depth,
            hanger_tolerance=body.hanger_tolerance,
            variant=body.variant.to_int(),
        ),
        content_type="model/stl",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
