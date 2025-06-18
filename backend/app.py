from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from logic.main import (
    post_location_name,
    post_long_lat,
    estimate_panels,
    estimate_energy,
)

app = FastAPI()

# Create an API Router
v1_router = APIRouter(
    prefix="/v1",  # All paths defined in this router will start with /v1
    tags=["Version 1 API"],  # Optional: for documentation grouping
)


@app.get("/")
async def read_root():
    return {"message": "hello, world"}


@v1_router.post("/")
async def location_name(location: str):
    """
    Receives location data via a POST request.
    The request body should be a JSON object like: {"location": "Some Place"}
    """
    return post_location_name(location)


@v1_router.post("/coordinates")
async def location_longitude_latitude(long: float, lat: float):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return post_long_lat(long, lat)


@v1_router.post("/estimate_panels")
async def get_kwh(long: float, lat: float, energy: float):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return estimate_panels(long, lat, energy)


@v1_router.post("/estimate_energy")
async def get_panel_number(long: float, lat: float, panel_number: int):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return estimate_energy(long, lat, panel_number)


@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"error": "Route not found", "path": request.url.path},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(v1_router)
