import requests
# import pandas as pd

# Define location and timeframe
lat, lon = "9.0", "7.5"
start, end = "20220101", "20221231"

url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "DAYL_CALC",
    "community": "RE",
    "latitude": lat,
    "longitude": lon,
    "start": start,
    "end": end,
    "format": "JSON",
}

resp = requests.get(url, params=params).json()
# print(resp.status_code)  # Should be 200
# print(resp.url)  # Debug the actual request URL
print(resp)  # Show the full response text

# data = resp["properties"]["parameter"]
# df = pd.DataFrame({
#     "date": list(data["ALLSKY_SFC_SW_DWN"].keys()),
#     "irradiance_W_m2": list(data["ALLSKY_SFC_SW_DWN"].values()),
#     "daylight_hours": list(data["SG_DAY_HOURS"].values()),
# })
# df["date"] = pd.to_datetime(df["date"])
# df.head()
