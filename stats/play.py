import requests
import datetime
from collections import defaultdict  # Useful for grouping daily data

# --- Configuration ---
lat, lon = "9.0", "7.5"
start_date_str = "20220101"
end_date_str = "20221231"  # YYYYMMDD format for daily/hourly API requests

# API Endpoints
url_daily = "https://power.larc.nasa.gov/api/temporal/daily/point"
url_hourly = "https://power.larc.nasa.gov/api/temporal/hourly/point"

# Parameters
param_daily_intensity = "ALLSKY_SFC_SW_DWN"  # For daily sun intensity (kWh/m²/day)
param_hourly_irradiance = (
    "ALLSKY_SFC_SW_DWN"  # For hourly irradiance to derive sunshine duration (W/m²)
)

# Threshold for "sunshine hour" (if hourly irradiance exceeds this, count as sunshine)
# 120 W/m² is a common threshold for 'bright sunshine'
sunshine_threshold_Wm2 = 120


# --- Function to fetch daily solar intensity ---
def get_daily_solar_intensity(latitude, longitude, start, end):
    params = {
        "parameters": param_daily_intensity,
        "community": "RE",
        "latitude": latitude,
        "longitude": longitude,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    print(f"\n--- Requesting Daily Solar Intensity for {start} to {end} ---")
    # print(f"API Call: {url_daily}?{requests.compat.urlencode(params)}") # For debugging URL

    try:
        response = requests.get(url_daily, params=params, timeout=30)  # Added timeout
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        daily_intensity_data = {}
        if (
            "properties" in data
            and "parameter" in data["properties"]
            and param_daily_intensity in data["properties"]["parameter"]
        ):
            daily_intensity_data = data["properties"]["parameter"][
                param_daily_intensity
            ]
            print(
                f"Successfully retrieved daily solar intensity for {len(daily_intensity_data)} days."
            )
        else:
            print(
                f"Warning: Solar intensity data not found in expected structure for {start} to {end}."
            )
            print(data.get("messages", "No specific error messages."))
        return daily_intensity_data

    except requests.exceptions.Timeout:
        print(f"Request timed out for daily intensity for {start} to {end}.")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching daily solar intensity for {start} to {end}: {e}")
        if response and response.text:
            print(
                "API Response (error details):",
                response.json().get("messages", response.text),
            )
        return {}


# --- Function to fetch and process hourly data for sunshine duration ---
def get_daily_sunshine_duration(
    latitude, longitude, start_year, end_year, threshold_Wm2
):
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
                "parameters": param_hourly_irradiance,
                "community": "RE",
                "latitude": latitude,
                "longitude": longitude,
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
                    url_hourly, params=params_hourly, timeout=60
                )  # Increased timeout for hourly data
                response.raise_for_status()
                hourly_data = response.json()

                if (
                    "properties" in hourly_data
                    and "parameter" in hourly_data["properties"]
                    and param_hourly_irradiance
                    in hourly_data["properties"]["parameter"]
                ):
                    param_data = hourly_data["properties"]["parameter"][
                        param_hourly_irradiance
                    ]

                    for timestamp, value in param_data.items():
                        # Timestamp format is YYYYMMDDHH (e.g., "2022010101" for 1 AM on Jan 1)
                        date_key = timestamp[:8]  # Extract the YYYYMMDD part

                        # Ensure value is numeric and not None
                        if value is not None:
                            try:
                                hour_irradiance = float(value)
                                if hour_irradiance > threshold_Wm2:
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
                        f"Warning: Hourly data for '{param_hourly_irradiance}' not found in expected structure for {year}-{month:02d}."
                    )
                    print(hourly_data.get("messages", "No specific error messages."))

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


# --- Main Execution ---

if __name__ == "__main__":
    # 1. Get Daily Sun Intensity
    daily_intensity_results = get_daily_solar_intensity(
        lat, lon, start_date_str, end_date_str
    )

    print("\n--- Daily Solar Intensity Results (First 10 Days) ---")
    count = 0
    for date, intensity in daily_intensity_results.items():
        print(
            f"Date: {date}, Sun Intensity (ALLSKY_SFC_SW_DWN): {intensity} kWh/m²/day"
        )
        count += 1
        if count >= 10:
            break
    print(f"... and {len(daily_intensity_results) - count} more entries.")

    # 2. Get Daily Sunshine Duration (Derived from Hourly Data)
    # Extract start and end years for the hourly function
    start_year = int(start_date_str[:4])
    end_year = int(end_date_str[:4])

    daily_sunshine_duration_results = get_daily_sunshine_duration(
        lat, lon, start_year, end_year, sunshine_threshold_Wm2
    )

    print("\n--- Daily Sunshine Duration Results (First 10 Days) ---")
    count = 0
    for date, hours in daily_sunshine_duration_results.items():
        print(
            f"Date: {date}, Sunshine Hours (> {sunshine_threshold_Wm2} W/m²): {hours} hours"
        )
        count += 1
        if count >= 10:
            break
    print(f"... and {len(daily_sunshine_duration_results) - count} more entries.")

    print("\n--- All Data Collected ---")
    # At this point, you have two dictionaries:
    # daily_intensity_results: { 'YYYYMMDD': value_kWh_per_m2_per_day, ... }
    # daily_sunshine_duration_results: { 'YYYYMMDD': value_hours, ... }

    # You can now combine or use these dictionaries as needed for your daily analysis.
    # For example, to print both for a specific day:
    # common_date = "20220715"
    # if common_date in daily_intensity_results and common_date in daily_sunshine_duration_results:
    #     print(f"\nData for {common_date}:")
    #     print(f"  Intensity: {daily_intensity_results[common_date]} kWh/m²/day")
    #     print(f"  Sunshine Duration: {daily_sunshine_duration_results[common_date]} hours")

