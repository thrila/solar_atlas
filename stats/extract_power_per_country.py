import pandas as pd

df_elec = pd.read_csv("power_per_country.csv")
df_elec.columns = df_elec.columns.str.strip()

df_elec = df_elec[["Country Name", "2022"]]
df_elec.columns = ["Country", "kWh_per_person"]


df_elec.dropna(subset=["kWh_per_person"], inplace=True)

df_elec.to_csv("kwh_per_person_2022.csv", index=False)
