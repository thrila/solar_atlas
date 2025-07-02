import requests
import datetime


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

    def get_daily_solar_intensity(self):
        """Solar intensity"""
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
            response = requests.get(
                self.url_daily, params=params, timeout=30
            )  # Added timeout
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            daily_intensity_data = {}
            if (
                "properties" in data
                and "parameter" in data["properties"]
                and self.param_daily_intensity in data["properties"]["parameter"]
            ):
                daily_intensity_data = data["properties"]["parameter"][
                    self.param_daily_intensity
                ]
                print(
                    f"Successfully retrieved daily solar intensity for {len(daily_intensity_data)} days."
                )
            else:
                print(
                    f"Warning: Solar intensity data not found in expected structure for {self.start_date} to {self.end_date}."
                )
                print(data.get("messages", "No specific error messages."))
            return daily_intensity_data[self.start_date]

        except requests.exceptions.Timeout:
            print(
                f"Request timed out for daily intensity for {self.start_date} to {self.end_date}."
            )
            return 0.0
        except requests.exceptions.RequestException as e:
            print(
                f"Error fetching daily solar intensity for {self.start_date} to {self.end_date}: {e}"
            )
            if response and response.text:
                print(
                    "API Response (error details):",
                    response.json().get("messages", response.text),
                )
            return 0.0

    def get_daily_sunshine_duration(self, date: datetime.date):
        """Solar sunshine > 120w in hours"""
        date_str = date.strftime("%Y%m%d")
        params = {
            "parameters": self.param_hourly_irradiance,
            "community": "RE",
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start": date_str,
            "end": date_str,
            "format": "JSON",
        }

        try:
            response = requests.get(self.url_hourly, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "properties" in data and "parameter" in data["properties"]:
                irradiance_data = data["properties"]["parameter"][
                    self.param_hourly_irradiance
                ]

                sunshine_hours = 0.0
                for timestamp, value in irradiance_data.items():
                    if value is not None and float(value) >= self.sunshine_threshold:
                        sunshine_hours += (
                            1.0  # Count 1 hour if irradiance exceeds threshold
                        )

                return sunshine_hours

        except requests.RequestException as e:
            print(f"Error fetching data for {date_str}: {e}")
            return 0.0

    def find_ideal_azimuth(self, latitude):
        if latitude > 5:
            return 180  # True South
        elif latitude < -5:
            return 0  # True North
        else:
            return 90


if __name__ == "__main__":
    location = SunLightDuration("10.0", "8.0", "20220101", "20220101")
    ans = location.get_daily_solar_intensity()
    print(f"solar intensity {ans}")
    answer = location.get_daily_sunshine_duration(datetime.date(2024, 6, 10))
    print(answer)
