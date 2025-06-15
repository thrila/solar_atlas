from typing import AnyStr
import requests
import datetime
from collections import defaultdict  # Useful for grouping daily data


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
            print(data)
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
            return daily_intensity_data

        except requests.exceptions.Timeout:
            print(
                f"Request timed out for daily intensity for {self.start_date} to {self.end_date}."
            )
            return {}
        except requests.exceptions.RequestException as e:
            print(
                f"Error fetching daily solar intensity for {self.start_date} to {self.end_date}: {e}"
            )
            if response and response.text:
                print(
                    "API Response (error details):",
                    response.json().get("messages", response.text),
                )
            return {}

    def get_daily_sunshine_duration(self, start_year, end_year):
        all_daily_sunshine_hours = defaultdict(
            float
        )  # Using defaultdict for easy accumulation

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):  # Iterate through each month
                # Calculate start and end dates for the current month
                current_month_start = datetime.date(year, month, 1)
                # Find the last day of the month
                if month == 12:
                    current_month_end = datetime.date(year, month, 31)
                else:
                    current_month_end = datetime.date(
                        year, month + 1, 1
                    ) - datetime.timedelta(days=1)

                start_date_month_str = current_month_start.strftime("%Y%m%d")
                end_date_month_str = current_month_end.strftime("%Y%m%d")

                params_hourly = {
                    "parameters": self.param_hourly_irradiance,
                    "community": "RE",
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "start": start_date_month_str,
                    "end": end_date_month_str,
                    "format": "JSON",
                }

                print(
                    f"\n--- Requesting Hourly Data for {start_date_month_str} to {end_date_month_str} ---"
                )
                # print(f"API Call: {url_hourly}?{requests.compat.urlencode(params_hourly)}") # For debugging URL

                try:
                    response = requests.get(
                        self.url_hourly, params=params_hourly, timeout=60
                    )  # Increased timeout for hourly data
                    response.raise_for_status()
                    hourly_data = response.json()

                    if (
                        "properties" in hourly_data
                        and "parameter" in hourly_data["properties"]
                        and self.param_hourly_irradiance
                        in hourly_data["properties"]["parameter"]
                    ):
                        param_data = hourly_data["properties"]["parameter"][
                            self.param_hourly_irradiance
                        ]

                        for timestamp, value in param_data.items():
                            # Timestamp format is YYYYMMDDHH (e.g., "2022010101" for 1 AM on Jan 1)
                            date_key = timestamp[:8]  # Extract the YYYYMMDD part

                            # Ensure value is numeric and not None
                            if value is not None:
                                try:
                                    hour_irradiance = float(value)
                                    if hour_irradiance > self.sunshine_threshold:
                                        all_daily_sunshine_hours[date_key] += (
                                            1.0  # Count as one sunshine hour
                                        )
                                except ValueError:
                                    print(
                                        f"Warning: Non-numeric value '{value}' for {hourly_param} at {timestamp}. Skipping."
                                    )
                            else:
                                # print(f"Info: Null value for {hourly_param} at {timestamp}. Skipping.")
                                pass  # Null values are common for night hours or missing data

                        print(f"Processed hourly data for {year}-{month:02d}.")
                    else:
                        print(
                            f"Warning: Hourly data for '{self.param_hourly_irradiance}' not found in expected structure for {year}-{month:02d}."
                        )
                        print(
                            hourly_data.get("messages", "No specific error messages.")
                        )

                except requests.exceptions.Timeout:
                    print(f"Request timed out for hourly data for {year}-{month:02d}.")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching hourly data for {year}-{month:02d}: {e}")
                    if response and response.text:
                        print(
                            "API Response (error details):",
                            response.json().get("messages", response.text),
                        )

        # Convert defaultdict to regular dict and sort by date for consistent output
        sorted_daily_sunshine_hours = dict(sorted(all_daily_sunshine_hours.items()))
        return sorted_daily_sunshine_hours


if __name__ == "__main__":
    location = SunLightDuration("9.0", "7.5", "20220101", "20220101")
    ans = location.get_daily_solar_intensity()
    answer = location.get_daily_sunshine_duration(2022, 2022)
    print(answer)
    # print(ans)
