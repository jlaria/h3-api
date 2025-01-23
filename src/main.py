from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from shapely.ops import transform
from typing import List, Dict, Any
import shapely.geometry
import h3

app = FastAPI(
    title="H3 API",
    description="API for interacting with H3 library functions.",
    version="1.0.0"
)

@app.get("/latlng_to_cell", tags=["Indexing"])
async def latlng_to_cell(
    lat: float = Query(..., description="Latitude of the location"),
    lng: float = Query(..., description="Longitude of the location"),
    resolution: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)")
):
    cell = h3.latlng_to_cell(lat, lng, resolution)
    return {"cell": cell}

@app.get("/cell_to_latlng", tags=["Indexing"])
async def cell_to_latlng(cell: str = Query(..., description="H3 cell ID")):
    lat, lng = h3.cell_to_latlng(cell)
    return {"lat": lat, "lng": lng}

@app.get("/cell_to_boundary", tags=["Indexing"])
async def cell_to_boundary(cell: str = Query(..., description="H3 cell ID")):
    boundary = h3.cell_to_boundary(cell)
    return {"boundary": boundary}

@app.get("/get_resolution", tags=["Inspection"])
async def get_resolution(cell: str = Query(..., description="H3 cell ID")):
    resolution = h3.get_resolution(cell)
    return {"resolution": resolution}

@app.get("/get_base_cell_number", tags=["Inspection"])
async def get_base_cell_number(cell: str = Query(..., description="H3 cell ID")):
    base_cell_number = h3.get_base_cell_number(cell)
    return {"base_cell_number": base_cell_number}

@app.get("/str_to_int", tags=["Inspection"])
async def str_to_int(cell: str = Query(..., description="H3 cell ID")):
    cell_int = h3.str_to_int(cell)
    return {"cell_int": cell_int}

@app.get("/int_to_str", tags=["Inspection"])
async def int_to_str(cell_int: int = Query(..., description="H3 cell ID as integer")):
    cell_str = h3.int_to_str(cell_int)
    return {"cell_str": cell_str}

@app.get("/is_valid_cell", tags=["Inspection"])
async def is_valid_cell(cell: str = Query(..., description="H3 cell ID")) -> Dict[str, int]:
    is_valid = int(h3.is_valid_cell(cell))
    return {"is_valid": is_valid}

@app.get("/is_res_class_III", tags=["Inspection"])
async def is_res_class_III(cell: str = Query(..., description="H3 cell ID")):
    is_class_III = h3.is_res_class_III(cell)
    return {"is_class_III": is_class_III}

@app.get("/is_pentagon", tags=["Inspection"])
async def is_pentagon(cell: str = Query(..., description="H3 cell ID")):
    is_pentagon = h3.is_pentagon(cell)
    return {"is_pentagon": is_pentagon}

@app.get("/get_icosahedron_faces", tags=["Inspection"])
async def get_icosahedron_faces(cell: str = Query(..., description="H3 cell ID")):
    icosahedron_faces = h3.get_icosahedron_faces(cell)
    return {"icosahedron_faces": icosahedron_faces}

@app.get("/grid_distance", tags=["Traversal"])
async def grid_distance(cell1: str = Query(..., description="First H3 cell ID"), cell2: str = Query(..., description="Second H3 cell ID")):
    distance = h3.grid_distance(cell1, cell2)
    return {"distance": distance}

@app.get("/grid_disk", tags=["Traversal"])
async def grid_disk(origin: str = Query(..., description="Origin H3 cell ID"), k: int = Query(..., description="K-ring distance")):
    cells = h3.grid_disk(origin, k)
    return {"cells": cells}

@app.get("/grid_path_cells", tags=["Traversal"])
async def grid_path_cells(start: str = Query(..., description="Start H3 cell ID"), end: str = Query(..., description="End H3 cell ID")):
    cells = h3.grid_path_cells(start, end)
    return {"cells": cells}

@app.get("/cell_to_local_ij", tags=["Traversal"])
async def cell_to_local_ij(origin: str = Query(..., description="Origin H3 cell ID"), cell: str = Query(..., description="H3 cell ID")):
    coordinates = h3.cell_to_local_ij(origin, cell)
    return {"coordinates": coordinates}

@app.get("/cell_to_parent", tags=["Hierarchy"])
async def cell_to_parent(cell: str = Query(..., description="H3 cell ID"), resolution: int = Query(None, description="Resolution level")):
    parent = h3.cell_to_parent(cell, resolution)
    return {"parent": parent}

@app.get("/cell_to_children", tags=["Hierarchy"])
async def cell_to_children(cell: str = Query(..., description="H3 cell ID"), resolution: int = Query(None, description="Resolution level")):
    children = h3.cell_to_children(cell, resolution)
    return {"children": children}

@app.get("/cell_to_children_size", tags=["Hierarchy"])
async def cell_to_children_size(cell: str = Query(..., description="H3 cell ID"), resolution: int = Query(None, description="Resolution level")):
    size = h3.cell_to_children_size(cell, resolution)
    return {"size": size}

@app.get("/cell_to_center_child", tags=["Hierarchy"])
async def cell_to_center_child(cell: str = Query(..., description="H3 cell ID"), resolution: int = Query(None, description="Resolution level")):
    center_child = h3.cell_to_center_child(cell, resolution)
    return {"center_child": center_child}

@app.get("/cell_to_child_pos", tags=["Hierarchy"])
async def cell_to_child_pos(child: str = Query(..., description="H3 cell ID"), res_parent: int = Query(..., description="Resolution of the parent")):
    child_pos = h3.cell_to_child_pos(child, res_parent)
    return {"child_pos": child_pos}

@app.get("/child_pos_to_cell", tags=["Hierarchy"])
async def child_pos_to_cell(parent: str = Query(..., description="Parent H3 cell ID"), res_child: int = Query(..., description="Resolution of the child"), child_pos: int = Query(..., description="Child position")):
    cell = h3.child_pos_to_cell(parent, res_child, child_pos)
    return {"cell": cell}

@app.get("/are_neighbor_cells", tags=["Directed edges"])
async def are_neighbor_cells(
    origin: str = Query(..., description="Origin H3 cell ID"),
    destination: str = Query(..., description="Destination H3 cell ID")
):
    are_neighbors = h3.are_neighbor_cells(origin, destination)
    return {"are_neighbors": are_neighbors}

@app.get("/cells_to_directed_edge", tags=["Directed edges"])
async def cells_to_directed_edge(
    origin: str = Query(..., description="Origin H3 cell ID"),
    destination: str = Query(..., description="Destination H3 cell ID")
):
    edge = h3.cells_to_directed_edge(origin, destination)
    return {"edge": edge}

@app.get("/is_valid_directed_edge", tags=["Directed edges"])
async def is_valid_directed_edge(edge: str = Query(..., description="H3 directed edge ID")):
    is_valid = h3.is_valid_directed_edge(edge)
    return {"is_valid": is_valid}

@app.get("/get_directed_edge_origin", tags=["Directed edges"])
async def get_directed_edge_origin(edge: str = Query(..., description="H3 directed edge ID")):
    origin = h3.get_directed_edge_origin(edge)
    return {"origin": origin}

@app.get("/get_directed_edge_destination", tags=["Directed edges"])
async def get_directed_edge_destination(edge: str = Query(..., description="H3 directed edge ID")):
    destination = h3.get_directed_edge_destination(edge)
    return {"destination": destination}

@app.get("/directed_edge_to_cells", tags=["Directed edges"])
async def directed_edge_to_cells(edge: str = Query(..., description="H3 directed edge ID")):
    cells = h3.directed_edge_to_cells(edge)
    return {"cells": cells}

@app.get("/origin_to_directed_edges", tags=["Directed edges"])
async def origin_to_directed_edges(origin: str = Query(..., description="H3 cell ID")):
    edges = h3.origin_to_directed_edges(origin)
    return {"edges": edges}

@app.get("/directed_edge_to_boundary", tags=["Directed edges"])
async def directed_edge_to_boundary(edge: str = Query(..., description="H3 directed edge ID")):
    boundary = h3.directed_edge_to_boundary(edge)
    return {"boundary": boundary}

@app.get("/cell_to_vertex", tags=["Vertexes"])
async def cell_to_vertex(
    origin: str = Query(..., description="Origin H3 cell ID"),
    vertex_num: int = Query(..., description="Vertex number")
):
    vertex = h3.cell_to_vertex(origin, vertex_num)
    return {"vertex": vertex}

@app.get("/cell_to_vertexes", tags=["Vertexes"])
async def cell_to_vertexes(origin: str = Query(..., description="Origin H3 cell ID")):
    vertexes = h3.cell_to_vertexes(origin)
    return {"vertexes": vertexes}

@app.get("/vertex_to_latlng", tags=["Vertexes"])
async def vertex_to_latlng(vertex: str = Query(..., description="H3 vertex ID")):
    latlng = h3.vertex_to_latlng(vertex)
    return {"latlng": latlng}

@app.get("/is_valid_vertex", tags=["Vertexes"])
async def is_valid_vertex(vertex: str = Query(..., description="H3 vertex ID")):
    is_valid = h3.is_valid_vertex(vertex)
    return {"is_valid": is_valid}

@app.get("/average_hexagon_area", tags=["Miscellaneous"])
async def average_hexagon_area(
    res: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)"),
    unit: str = Query('m^2', description="Unit of area (e.g., m^2, km^2, rads^2)")
):
    area = h3.average_hexagon_area(res, unit)
    return {"area": area}

@app.get("/cell_area", tags=["Miscellaneous"])
async def cell_area(
    cell: str = Query(..., description="H3 cell ID"),
    unit: str = Query('rads^2', description="Unit of area (e.g., m^2, km^2, rads^2)")
):
    area = h3.cell_area(cell, unit)
    return {"area": area}

@app.get("/average_hexagon_edge_length", tags=["Miscellaneous"])
async def average_hexagon_edge_length(
    res: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)"),
    unit: str = Query('km', description="Unit of length (e.g., m, km, rads)")
):
    length = h3.average_hexagon_edge_length(res, unit)
    return {"length": length}

@app.get("/edge_length", tags=["Miscellaneous"])
async def edge_length(
    edge: str = Query(..., description="H3 edge ID"),
    unit: str = Query('km', description="Unit of length (e.g., m, km, rads)")
):
    length = h3.edge_length(edge, unit)
    return {"length": length}

@app.get("/get_num_cells", tags=["Miscellaneous"])
async def get_num_cells(
    res: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)")
):
    num_cells = h3.get_num_cells(res)
    return {"num_cells": num_cells}

@app.get("/get_res0_cells", tags=["Miscellaneous"])
async def get_res0_cells():
    cells = h3.get_res0_cells()
    return {"cells": cells}

@app.get("/get_pentagons", tags=["Miscellaneous"])
async def get_pentagons(
    res: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)")
):
    pentagons = h3.get_pentagons(res)
    return {"pentagons": pentagons}

# Define the request schema with an example
class H3Cells(BaseModel):
    cells: List[str] = Field(
        ...,
        example=['8928341aec3ffff', '8928341aeb7ffff'],
    )

@app.post("/compact_cells", tags=["Hierarchy"])
async def compact_cells(request: H3Cells) -> H3Cells:
    cells = h3.compact_cells(request.cells)
    return H3Cells(cells=cells)

@app.post("/uncompact_cells", tags=["Hierarchy"])
async def uncompact_cells(request: H3Cells, 
                          res: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)")) -> H3Cells:
    cells = h3.uncompact_cells(request.cells, res)
    return H3Cells(cells=cells)

# Define the request schema with an example
class H3Polygon(BaseModel):
    geometry: Dict[str, Any] = Field(
        ...,
        example={
            "type": "Polygon",
            "coordinates": [
                [
                    [-122.40898, 37.7834],
                    [-122.40901, 37.7835],
                    [-122.40902, 37.7835],
                    [-122.40902, 37.7834],
                    [-122.40898, 37.7834]
                ]
            ]
        }
    )

@app.post("/h3shape_to_cells", tags=["Region"])
async def h3shape_to_cells(request: H3Polygon, 
                          res: int = Query(..., ge=0, le=15, description="Resolution level (between 0 and 15)")) -> H3Cells:
    poly = shapely.geometry.shape(request.geometry)
    poly = h3.geo_to_h3shape(poly)
    cells = h3.polygon_to_cells(poly, res)
    return H3Cells(cells=cells)

#h3.cells_to_h3shape(cells, *, tight=True)
@app.post("/cells_to_h3shape", tags=["Region"])
async def cells_to_h3shape(request: H3Cells) -> H3Polygon:
    h3shape = h3.cells_to_h3shape(request.cells)
    return H3Polygon(geometry=h3shape.__geo_interface__)

# Health check endpoint
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "ok", "message": "H3 API is running."}