import requests


def get_lon_lat(location: str) -> dict:
    try:
        res = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={location}&format=json",
            headers={"User-Agent": "fastapi-app"},
            timeout=5,  # optional: avoid hanging forever
        )
        res.raise_for_status()
        data = res.json()

        if not data:
            return {"error": "location not found"}

        return {
            "lat": float(data[0]["lat"]),
            "long": float(data[0]["lon"]),
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"request failed: {str(e)}"}

    except (KeyError, ValueError, IndexError):
        return {"error": "invalid response from geocoding API"}


def get_location_name(lat: float, lon: float) -> dict:
    try:
        res = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json",
            headers={"User-Agent": "fastapi-app"},
            timeout=5,
        )
        res.raise_for_status()
        data = res.json()

        return {
            "location_name": data.get("display_name", "unknown"),
            "raw": data,  # optional: inspect full data
        }

    except Exception as e:
        return {"error": f"Reverse geocoding failed: {str(e)}"}


print(get_location_name(31.2638905, -98.5456116))
