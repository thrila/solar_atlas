from services.location import get_lon_lat, get_location_name
from services.sunlight_duration import SunLightDuration
from services.conversion import Conversion
from services.energy import Energy
from db.db import query_db
import datetime


def get_row(country: str) -> dict[str, float | int]:
    """Get row from table"""
    data = query_db(
        'SELECT * FROM test_table WHERE "Country Name" = ?', [country], one=True
    )
    return {
        "average_household_size": data["Avg_Household_Size"],
        "kWh_per_person": data["kWh_per_person"],
        "population": data["Population"],
        "carbon_intensity": data["Carbon intensity of electricity - gCO2/kWh"],
    }


def get_solar_metadata(lat: float, lon: float, panel_output=330):
    date = datetime.date(2022, 1, 1)
    sun_attr = SunLightDuration(lat, lon, "20220101", "20220101")
    location_name = get_location_name(lat, lon)["location_name"]
    sunlight_duration = sun_attr.get_daily_sunshine_duration(date)
    solar_intensity = sun_attr.get_daily_solar_intensity()
    direction = sun_attr.find_ideal_azimuth(lat)
    energy = Energy(panel_output, sunlight_duration)

    return {
        "location": location_name,
        "daily_solar_irradiance": solar_intensity,
        "sunlight_hours_per_day": sunlight_duration,
        "azimuth_angle": direction,
        "tilt_angle": lat,
        "lat": lat,
        "lon": lon,
    }, energy


def post_location_name(location: str):
    coords = get_lon_lat(location)
    lat = coords["lat"]
    lon = coords["long"]
    meta_data, energy = get_solar_metadata(lat, lon)
    energy_w = energy.amount_of_power()

    return {**meta_data, "energy": energy_w}


def post_long_lat(long: float, lat: float):
    """
    Logic for the post_long_lat route
    """
    sun_attr = SunLightDuration(lat, long, "20220101", "20220101")
    location_name = get_location_name(lat, long)["location_name"]
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_azimuth(lat)
    en = Energy(330, sunlight_duration)
    energy_w = en.amount_of_power()
    convert = Conversion()
    row = get_row(location_name)
    print(row)
    # NOTE: this data is annually man
    row = get_row(location_name)
    average_household_size = row["average_household_size"]
    kWh_per_person = row["kWh_per_person"]
    population = row["population"]
    carbon_intensity = row["carbon_intensity"]
    kilowatt_per_household = en.kWh_per_household(
        kWh_per_person, average_household_size
    )
    national_energy_demand = en.national_energy_demand(
        kilowatt_per_household, population
    )
    co_saving_potential = en.co2_saving_potential(
        convert.watts_to_kilowatts(energy_w) * 365, carbon_intensity
    )

    return {
        "daily_solar_irradiance": solar_intensity,
        "sunlight_hours_per_day": sunlight_duration,
        "lat": lat,
        "lon": long,
        "location": location_name,
        "tilt_angle": lat,
        "azimuth_angle": direction,
        "average_household_size": average_household_size,
        "kilowatt_per_household": kilowatt_per_household,
        "co_saving_potential": co_saving_potential,
        "national_energy_demand": national_energy_demand,
        "kWh_per_person": kWh_per_person,
        "population": population,
        "carbon_intensity": carbon_intensity,
    }


def estimate_panels(long: float, lat: float, energy_w: float):
    sun_attr = SunLightDuration(lat, long, "20220101", "20220101")
    location_name = get_location_name(lat, long)["location_name"]
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_azimuth(lat)
    en = Energy(330, sunlight_duration)
    convert = Conversion()
    panels_needed = en.number_of_panels(energy_w)

    # NOTE: this data is annually man
    row = get_row(location_name)
    average_household_size = row["average_household_size"]
    kWh_per_person = row["kWh_per_person"]
    population = row["population"]
    carbon_intensity = row["carbon_intensity"]
    kilowatt_per_household = en.kWh_per_household(
        kWh_per_person, average_household_size
    )
    national_energy_demand = en.national_energy_demand(
        kilowatt_per_household, population
    )
    co_saving_potential = en.co2_saving_potential(
        convert.watts_to_kilowatts(energy_w) * 365, carbon_intensity
    )

    return {
        "daily_solar_irradiance": solar_intensity,
        "sunlight_hours_per_day": sunlight_duration,
        "lat": lat,
        "lon": long,
        "location": location_name,
        "tilt_angle": lat,
        "azimuth_angle": direction,
        "number_of_panels": panels_needed,
        "output_power": energy_w,
        "power_per_household_annually": kilowatt_per_household,
        "national_energy_demand_annually": national_energy_demand,
        "carbon_saved_annually": co_saving_potential,
        "average_household_size": average_household_size,
        "kWh_per_person": kWh_per_person,
        "population": population,
        "carbon_intensity": carbon_intensity,
    }


def estimate_energy(long: float, lat: float, number_of_panels: int):
    sun_attr = SunLightDuration(lat, long, "20220101", "20220101")
    location_name = get_location_name(lat, long)["location_name"]
    solar_intensity = sun_attr.get_daily_solar_intensity()
    sunlight_duration = sun_attr.get_daily_sunshine_duration(datetime.date(2022, 1, 1))
    direction = sun_attr.find_ideal_azimuth(lat)
    en = Energy(330, sunlight_duration)
    power = en.amount_of_power(number_of_panels)

    return {
        "daily_solar_irradiance": solar_intensity,
        "sunlight_hours_per_day": sunlight_duration,
        "lat": lat,
        "lon": long,
        "location": location_name,
        "tilt_angle": lat,
        "azimuth_angle": direction,
        "number_of_panels": number_of_panels,
        "output_power": power,
    }
