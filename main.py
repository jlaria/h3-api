from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import h3

import shapely.wkt
from shapely.ops import transform

# Create FastAPI instance
app = FastAPI()

# Define the request schema
class PolyfillRequest(BaseModel):
    wkt: str  
    resolution: int


# Define the response schema
class PolyfillResponse(BaseModel):
    h3_indexes: List[str]

def cell_to_wkt(cell):
    boundary = list(h3.cell_to_boundary(cell))
    boundary.append(boundary[0])
    poly = shapely.geometry.Polygon(boundary)
    poly = transform(lambda x,y: (y,x), poly)
    return poly.wkt

@app.post("/polyfill", response_model=PolyfillResponse)
async def polyfill(request: PolyfillRequest):
    """
    Endpoint to polyfill a wkt polygon with H3 indexes at a given resolution.
    """
    try:
        # Validate resolution
        if not (0 <= request.resolution <= 15):
            raise HTTPException(
                status_code=400, detail="Resolution must be between 0 and 15."
            )

        # Use the h3 library to polyfill the polygon
        poly = shapely.wkt.loads(request.wkt)
        poly = h3.geo_to_h3shape(poly)
        cells = h3.polygon_to_cells(poly, request.resolution)
        polygons = [cell_to_wkt(x) for x in cells]

        return PolyfillResponse(h3_indexes=list(polygons))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app.get("/")
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "ok", "message": "H3 Polyfill API is running."}