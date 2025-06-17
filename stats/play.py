import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

# --- CONFIG ---
LAT = 10.5  # Nigeria example
LON = 7.4
YEAR = 2002


# --- 1. Fetch Daily GHI from NASA POWER ---
def fetch_ghi(lat, lon, year):
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=ALLSKY_SFC_SW_DWN"
        f"&start={year}&end={year}"
        f"&latitude={lat}&longitude={lon}&format=JSON&community=RE"
    )
    r = requests.get(url).json()
    ghi_data = r["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    return pd.DataFrame({
        "date": pd.to_datetime(list(ghi_data.keys())),
        "GHI": list(ghi_data.values()),
    })


# --- 2. Estimate Solar Zenith Angle (Approx) ---
def estimate_solar_zenith(df, lat):
    days = df["date"].dt.dayofyear
    decl = 23.45 * np.sin(np.radians((360 / 365) * (days - 81)))  # solar declination
    hour_angle = 0  # assume solar noon
    zenith = np.degrees(
        np.arccos(
            np.sin(np.radians(lat)) * np.sin(np.radians(decl))
            + np.cos(np.radians(lat))
            * np.cos(np.radians(decl))
            * np.cos(np.radians(hour_angle))
        )
    )
    df["zenith"] = zenith
    return df


# --- 3. Simulate Tilt Sweep ---
def simulate_tilts(df):
    results = []
    for tilt in range(0, 91):  # 0° to 90°
        incident_angle = np.abs(df["zenith"] - tilt)
        cos_factor = np.cos(np.radians(incident_angle)).clip(0, 1)
        irradiance = df["GHI"] * cos_factor
        total = irradiance.sum()
        results.append((tilt, total))
    return pd.DataFrame(
        results, columns=["Tilt Angle", "Total Irradiance"]
    ).sort_values("Total Irradiance", ascending=False)


# --- Run Full Pipeline ---
ghi_df = fetch_ghi(LAT, LON, YEAR)
zenith_df = estimate_solar_zenith(ghi_df, LAT)
tilt_results = simulate_tilts(zenith_df)

# --- Output Best Result ---
max_irr = tilt_results["Total Irradiance"].max()
tolerance = 0.001 * max_irr
close_to_max = tilt_results[tilt_results["Total Irradiance"] >= (max_irr - tolerance)]

# Use the mean or lowest of them
best_practical_tilt = close_to_max["Tilt Angle"].mean()  # or .min()
print("🎯 Practical Best Tilt:", round(best_practical_tilt, 2))
print(tilt_results.head(5))
