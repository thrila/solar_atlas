import pandas as pd
import sqlite3

df = pd.read_csv("test.csv")  # adjust path
conn = sqlite3.connect("test.sqlite")
df.to_sql("test_table", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
