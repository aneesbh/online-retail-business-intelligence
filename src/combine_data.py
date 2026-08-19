import pandas as pd

file_path = "data/online_retail_II.xlsx"

# Read both sheets
df_2009_2010 = pd.read_excel(
    file_path,
    sheet_name="Year 2009-2010"
)

df_2010_2011 = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

# Combine both years
df = pd.concat(
    [df_2009_2010, df_2010_2011],
    ignore_index=True
)

# Save combined data
df.to_csv(
    "data/online_retail_combined.csv",
    index=False
)

print("Data combined successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Saved to: data/online_retail_combined.csv")