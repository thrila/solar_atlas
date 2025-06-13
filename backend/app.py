from fastapi import FastAPI, APIRouter

app = FastAPI()

# Create an API Router
v1_router = APIRouter(
    prefix="/v1",  # All paths defined in this router will start with /v1
    tags=["Version 1 API"],  # Optional: for documentation grouping
)


@v1_router.get("/")
async def read_root():
    return {"message": "Hello World"}


@v1_router.post("/")
async def location_name(location: str):
    """
    Receives location data via a POST request.
    The request body should be a JSON object like: {"location": "Some Place"}
    """
    return {"received_location": location, "message": "Location data received!"}


@v1_router.post("/v1/")
async def location_longitude_latitude(long: float, lat: float):
    """
    Recieves Longitude and Latitude via a post request and returns data
    """
    return {"long": long, "lat": lat}


app.include_router(v1_router)
