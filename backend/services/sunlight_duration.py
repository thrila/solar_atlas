import httpx


class SunLightDuration:
    """
    params:
        - longitude
        - latitude
        - start_date
        - end_date
        - sunshine_threshold
    returns:
        Sunlight SunLightDuration in hours for periods where the sunshine intensity is greater than the threshold
        (default) sunshine_threshold = 120
    """

    url_daily = "https://power.larc.nasa.gov/api/temporal/daily/point"
    url_hourly = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    param_daily_intensity = "ALLSKY_SFC_SW_DWN"  # For daily sun intensity (kWh/m²/day)
    param_hourly_irradiance = "ALLSKY_SFC_SW_DWN"

    def __init__(self, lat, long, start_date, end_date, sunshine_threshold=120) -> None:
        self.longitude = long
        self.latitude = lat
        self.start_date = start_date
        self.end_date = end_date
        self.sunshine_threshold = sunshine_threshold

    async def get_daily_solar_intensity(self):
        """Solar intensity (daily kWh/m²)"""
        params = {
            "parameters": self.param_daily_intensity,
            "community": "RE",
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start": self.start_date,
            "end": self.end_date,
            "format": "JSON",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.url_daily, params=params)
                response.raise_for_status()
                data = response.json()

            param_data = data.get("properties", {}).get("parameter", {})
            if self.param_daily_intensity in param_data:
                daily_data = param_data[self.param_daily_intensity]
                # print(f"Retrieved solar intensity for {len(daily_data)} days.")
                return daily_data.get(self.start_date, 0.0)
            else:
                print("Warning: Expected solar intensity data not found.")
                print(data.get("messages", "No specific error messages."))
                return 0.0

        except httpx.TimeoutException:
            print(f"Timeout while fetching solar intensity for {self.start_date}.")
            return 0.0
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code}: {e.response.text}")
            return 0.0
        except httpx.RequestError as e:
            print(f"Request error while fetching solar intensity: {e}")
            return 0.0

    async def get_daily_sunshine_duration(self):
        """Sunshine duration (hours with irradiance > threshold)"""
        params = {
            "parameters": self.param_hourly_irradiance,
            "community": "RE",
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start": self.start_date,
            "end": self.start_date,
            "format": "JSON",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.url_hourly, params=params)
                response.raise_for_status()
                data = response.json()

            param_data = data.get("properties", {}).get("parameter", {})
            irradiance_data = param_data.get(self.param_hourly_irradiance, {})

            sunshine_hours = sum(
                1.0
                for v in irradiance_data.values()
                if v is not None and float(v) >= self.sunshine_threshold
            )

            return sunshine_hours

        except httpx.TimeoutException:
            print(f"Timeout while fetching sunshine duration for {self.start_date}.")
            return 0.0
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code}: {e.response.text}")
            return 0.0
        except httpx.RequestError as e:
            print(f"Request error while fetching sunshine duration: {e}")
            return 0.0

    def find_ideal_azimuth(self, latitude):
        if latitude > 5:
            return 180  # True South
        elif latitude < -5:
            return 0  # True North
        else:
            return 90
