from services.location import get_lon_lat, get_location_name
from services.sunlight_duration import SunLightDuration
from services.energy import Energy
from db.db import query_db
import datetime


def post_location_name(location: str):
    coords = get_lon_lat(location)
    lat = coords["lat"]
    lon = coords["long"]

    # make time auto
    sun_attr = SunLightDuration(lat, lon, "20220101", "20220101")
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_direction(lat)

    return {
        "solar_intensity": solar_intensity,
        "solar_duration": sunlight_duration,
        "lat": lat,
        "lon": lon,
        "location": location,
        "angle_of_panel": lat,
        "direction": direction,
    }


def post_long_lat(long: float, lat: float):
    """
    Logic for the post_long_lat route
    """
    sun_attr = SunLightDuration(lat, long, "20220101", "20220101")
    location_name = get_location_name(lat, long)["location_name"]
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_direction(lat)

    return {
        "solar_intensity": solar_intensity,
        "solar_duration": sunlight_duration,
        "lat": lat,
        "lon": long,
        "location": location_name,
        "angle_of_panel": lat,
        "direction": direction,
    }


def estimate_panels(long: float, lat: float, energy: float):
    sun_attr = SunLightDuration(lat, long, "20220101", "20220101")
    location_name = get_location_name(lat, long)["location_name"]
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_direction(lat)
    en = Energy(330, sunlight_duration)
    panels_needed = en.number_of_panels(energy)

    return {
        "solar_intensity": solar_intensity,
        "solar_duration": sunlight_duration,
        "lat": lat,
        "lon": long,
        "location": location_name,
        "angle_of_panel": lat,
        "direction": direction,
        "number_of_panels": panels_needed,
        "power": energy,
    }


def estimate_energy(long: float, lat: float, number_of_panels: int):
    sun_attr = SunLightDuration(lat, long, "20220101", "20220101")
    location_name = get_location_name(lat, long)["location_name"]
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_direction(lat)
    en = Energy(330, sunlight_duration)
    power = en.amount_of_power(number_of_panels)

    return {
        "solar_intensity": solar_intensity,
        "solar_duration": sunlight_duration,
        "lat": lat,
        "lon": long,
        "location": location_name,
        "angle_of_panel": lat,
        "direction": direction,
        "panel_number": number_of_panels,
        "power": power,
    }


def see_row():
    query = 'SELECT "Country Name" FROM test_table'
    results = query_db(query)
    return results


print(see_row())
