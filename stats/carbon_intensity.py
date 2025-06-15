import pandas as pd

df = pd.read_csv("carbon-intensity-electricity.csv")

df_2022 = df[df["Year"] == 2022]

df_clean = df_2022.drop_duplicates(subset="Entity", keep="first")

df_final = df_clean[["Entity", "Carbon intensity of electricity - gCO2/kWh"]]


df_final.to_csv("carbon_intensity_per_country.csv")
