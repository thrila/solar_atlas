import requests
import json


"""
country_name -> lon, lat
lon lat -> solar data
"""

# Location for Abuja (approximately)
latitude = 9.0765
longitude = 7.3986

# Dates for May 2024
start_date = "20240501"
end_date = "20240531"

# Parameters for Renewable Energy community
# ALLSKY_SFC_SW_DWN: All-Sky Surface Shortwave Downward Irradiance (solar radiation)
# T2M: Temperature at 2 Meters
parameters = "ALLSKY_SFC_SW_DWN,T2M"
community = "RE"
temporal_level = "daily"
output_format = "JSON"

# Construct the API URL
base_url = "https://power.larc.nasa.gov/api/temporal"
api_url = (
    f"{base_url}/{temporal_level}/point?"
    f"parameters={parameters}&community={community}&"
    f"longitude={longitude}&latitude={latitude}&"
    f"start={start_date}&end={end_date}&format={output_format}"
)

print(f"Requesting data from: {api_url}\n")

try:
    response = requests.get(api_url, verify=True, timeout=30)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

    data = response.json()

    # Process the data (example: print daily values)
    if "properties" in data and "parameter" in data["properties"]:
        print("Date | Solar Radiation (kWh/m^2/day) | Temperature (C)")
        print("-" * 50)
        for date, values in data["properties"]["parameter"][
            "ALLSKY_SFC_SW_DWN"
        ].items():
            solar_rad = values
            temp = data["properties"]["parameter"]["T2M"].get(date)
            if solar_rad is not None and temp is not None:
                print(f"{date} | {solar_rad:.2f} | {temp:.2f}")
            elif solar_rad is not None:
                print(f"{date} | {solar_rad:.2f} | N/A")
            else:
                print(f"{date} | N/A | N/A")
    else:
        print("No data found or unexpected response structure.")
        print(data)  # Print full response for debugging

except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Something unexpected happened: {err}")
except json.JSONDecodeError:
    print("Failed to decode JSON from response.")
    print(response.text)  # Print raw response text for debugging
