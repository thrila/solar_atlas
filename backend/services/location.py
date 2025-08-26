import httpx


async def get_lon_lat(location: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": location, "format": "json"},
                headers={"User-Agent": "fastapi-app"},
            )
            res.raise_for_status()
            data = res.json()

        if not data:
            return {"error": "location not found"}

        return {
            "lat": float(data[0]["lat"]),
            "long": float(data[0]["lon"]),
        }

    except httpx.RequestError as e:
        return {"error": f"request failed: {str(e)}"}

    except (KeyError, ValueError, IndexError):
        return {"error": "invalid response from geocoding API"}


async def get_location_name(lat: float, lon: float) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat": lat, "lon": lon, "format": "json"},
                headers={
                    "User-Agent": "fastapi-app",
                    "Accept-Language": "en",
                },
            )
            res.raise_for_status()
            data = res.json()

        return {
            "location_name": data["address"].get("country", "unknown"),
            "raw": data,
        }

    except httpx.RequestError as e:
        return {"error": f"Reverse geocoding failed: {str(e)}"}
