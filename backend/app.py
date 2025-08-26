from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from logic.main import (
    post_location_name,
    post_long_lat,
    estimate_panels,
    estimate_energy,
)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://solar-atlas.vercel.app/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an API Router
v1_router = APIRouter(
    prefix="/v1",  # All paths defined in this router will start with /v1
    tags=["Version 1 API"],  # Optional: for documentation grouping
)


@app.get("/")
async def read_root():
    return {"message": "Hello, world"}


@v1_router.post("/")
async def location_name(location: str):
    """
    Receives location data via a POST request.
    The request body should be a JSON object like: {"location": "Some Place"}
    """
    return await post_location_name(location)


@v1_router.post("/coordinates")
async def location_longitude_latitude(long: float, lat: float):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return await post_long_lat(long, lat)


@v1_router.post("/estimate_panels")
async def get_kwh(long: float, lat: float, energy: float):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return await estimate_panels(long, lat, energy)


@v1_router.post("/estimate_energy")
async def get_panel_number(
    long: float, lat: float, panel_number: int, panel_output: int
):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return await estimate_energy(long, lat, panel_number, panel_output)


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
