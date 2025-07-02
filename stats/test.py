import pandas as pd
from thefuzz import process

# Standard country name mapping for consistent merges
country_name_mapping = {
    "viet nam": "vietnam",
    "united states": "united states of america",
    "côte d'ivoire": "ivory coast",
    "russian federation": "russia",
    "syrian arab republic": "syria",
    "iran, islamic republic of": "iran",
    "korea, republic of": "south korea",
    "korea, dem. people's rep.": "north korea",
    "egypt, arab rep.": "egypt",
    "gambia, the": "gambia",
    "bahamas, the": "bahamas",
    "hong kong sar, china": "hong kong",
    "macedonia, fyr": "north macedonia",
    "brunei darussalam": "brunei",
    "lao pdr": "laos",
    "slovak republic": "slovakia",
    "moldova": "moldova",
    "venezuela, rb": "venezuela",
    "tanzania": "tanzania",
    "yemen, rep.": "yemen",
    "gambia the": "gambia",
    "micronesia, fed. sts.": "micronesia",
    "st. kitts and nevis": "saint kitts and nevis",
    "st. lucia": "saint lucia",
    "st. vincent and the grenadines": "saint vincent and the grenadines",
    "sao tome and principe": "são tomé and príncipe",
    "eswatini": "swaziland",
    "czechia": "czech republic",
    "myanmar": "burma",
}


# Fuzzy match function
def fuzzy_match(value, choices, threshold=85):
    match, score = process.extractOne(str(value), choices)
    if match and score >= threshold:
        return match
    else:
        return None


# Load datasets
pop = pd.read_csv("population_per_country.csv")
hh_size = pd.read_csv("household_size_per_country_filtered.csv")
kwh = pd.read_csv("kwh_per_person_2022.csv")
carbon = pd.read_csv("carbon_intensity_per_country.csv", index_col=0)
name = pd.read_csv("data.csv")


country_names_list = name["Name"].tolist()
# use the year 2022
df_pop = pop[["Country Name", "2022"]].copy()
df_pop = df_pop.rename(columns={"2022": "Population"})

kwh = kwh.rename(columns={"2022": "kwh_per_capita"})

# print(kwh)
# Standardize country names
# for df in [pop, hh_size, kwh, carbon]:
#     df["Country Name"] = df["Country Name"].str.strip().str.lower()

# # Apply mapping
for df in [df_pop, hh_size, kwh, carbon]:
    df["Country Name"] = df["Country Name"].replace(country_name_mapping)

# ------------------------
# 🔗 Merge in stages
df = df_pop.merge(hh_size, on="Country Name", how="left")
df = df.merge(kwh, on="Country Name", how="left")
df = df.merge(carbon, on="Country Name", how="left")
df = df.fillna(0)

# Apply fuzzy matching
df["Country Name"] = df["Country Name"].apply(
    lambda x: fuzzy_match(x, country_names_list, threshold=90)
)

# Drop unmatched rows
df = df[df["Country Name"].notna()].copy()

print("✅ Cleaned. Remaining rows:", len(df))
# # Optional: Drop redundant columns

# n = len(df)
# print(df.iloc[n // 2 - 2 : n // 2 + 3])
# # Save final clean world table
df.to_csv("world_energy_carbon_table_revised.csv", index=False)
