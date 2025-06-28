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


async def get_solar_metadata(lat: float, lon: float, panel_output=330):
    date = datetime.date(2022, 1, 1)
    sun_attr = SunLightDuration(lat, lon, "20220101", "20220101")
    location_name = get_location_name(lat, lon)["location_name"]
    sunlight_duration = await sun_attr.get_daily_sunshine_duration(date)
    solar_intensity = await sun_attr.get_daily_solar_intensity()
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
    location_name = get_location_name(lat, long)["location_name"]
    convert = Conversion()
    meta_data, energy = get_solar_metadata(lat, long)
    energy_w = energy.amount_of_power()
    # NOTE: this data is annually man
    row = get_row(location_name)
    average_household_size = row["average_household_size"]
    kWh_per_person = row["kWh_per_person"]
    population = row["population"]
    carbon_intensity = row["carbon_intensity"]
    kilowatt_per_household = energy.kWh_per_household(
        kWh_per_person, average_household_size
    )
    national_energy_demand = energy.national_energy_demand(
        kilowatt_per_household, population
    )
    co_saving_potential = energy.co2_saving_potential(
        convert.watts_to_kilowatts(energy_w) * 365, carbon_intensity
    )

    return {
        **meta_data,
        "average_household_size": average_household_size,
        "kilowatt_per_household": kilowatt_per_household,
        "co_saving_potential": co_saving_potential,
        "national_energy_demand": national_energy_demand,
        **row,
    }


def estimate_panels(long: float, lat: float, energy_w: float):
    location_name = get_location_name(lat, long)["location_name"]
    meta_data, energy = get_solar_metadata(lat, long)
    convert = Conversion()

    # NOTE: this data is annually man
    row = get_row(location_name)
    average_household_size = row["average_household_size"]
    kWh_per_person = row["kWh_per_person"]
    population = row["population"]
    carbon_intensity = row["carbon_intensity"]
    panels_needed = energy.number_of_panels(energy_w)
    kilowatt_per_household = energy.kWh_per_household(
        kWh_per_person, average_household_size
    )
    national_energy_demand = energy.national_energy_demand(
        kilowatt_per_household, population
    )
    co_saving_potential = energy.co2_saving_potential(
        convert.watts_to_kilowatts(energy_w) * 365, carbon_intensity
    )

    return {
        **meta_data,
        "location": location_name,
        "number_of_panels": panels_needed,
        "output_power": energy_w,
        "power_per_household_annually": kilowatt_per_household,
        "national_energy_demand_annually": national_energy_demand,
        "carbon_saved_annually": co_saving_potential,
        "carbon_intensity": carbon_intensity,
        **row,
    }


async def estimate_energy(
    long: float, lat: float, number_of_panels: int, panel_output=330
):
    location_name = get_location_name(lat, long)["location_name"]
    convert = Conversion()
    meta_data, energy = await get_solar_metadata(lat, long, panel_output)
    energy_w = energy.amount_of_power(number_of_panels)
    row = get_row(location_name)
    average_household_size = row["average_household_size"]
    kWh_per_person = row["kWh_per_person"]
    population = row["population"]
    carbon_intensity = row["carbon_intensity"]
    kilowatt_per_household = energy.kWh_per_household(
        kWh_per_person, average_household_size
    )
    national_energy_demand = energy.national_energy_demand(
        kilowatt_per_household, population
    )
    co_saving_potential = energy.co2_saving_potential(
        convert.watts_to_kilowatts(energy_w) * 365, carbon_intensity
    )

    return {
        **meta_data,
        "location": location_name,
        "number_of_panels": number_of_panels,
        "output_power": energy_w,
        "power_per_household_annually": kilowatt_per_household,
        "national_energy_demand_annually": national_energy_demand,
        "carbon_saved_annually": co_saving_potential,
        "carbon_intensity": carbon_intensity,
        **row,
    }
