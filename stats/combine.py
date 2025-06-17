import pandas as pd

# Load all CSVs
population_per_country = pd.read_csv("countries&population.csv")
household_size = pd.read_csv("household_size_per_country_filtered.csv")
kwh_per_person = pd.read_csv("kwh_per_person_2022.csv")
carbon_intensity = pd.read_csv("carbon_intensity_per_country.csv")


# Merge on 'Country'
merged = population_per_country.merge(household_size, on="Country Name", how="inner")
merged = merged.merge(kwh_per_person, on="Country Name", how="inner")
merged = merged.merge(carbon_intensity, on="Country Name", how="inner")

# merged["kWh_per_household"] = merged["kWh_per_person"] * merged["Avg_Household_Size"]

merged.to_csv("energy_stats_by_country.csv", index=False)
