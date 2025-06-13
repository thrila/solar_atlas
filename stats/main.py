import pandas as pd

df = pd.read_csv("house_size_and_composition.csv", dayfirst=True)

df["Reference date"] = pd.to_datetime(
    df["Reference date"], dayfirst=True, errors="coerce"
)
df = df.dropna(subset=["Reference date"])

df_sorted = df.sort_values(
    by=["Country or area", "Reference date"], ascending=[True, False]
)

df_latest = df_sorted.drop_duplicates(subset=["Country or area"], keep="first")

result = df_latest[["Country or area", "family_size"]].rename(
    columns={"Country or area": "Country", "family_size": "Avg_Household_Size"}
)

print(result.head(5))
result.to_csv("household_size_per_country_filtered.csv", index=False)
