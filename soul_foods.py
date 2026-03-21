import pandas as pd
import os

# ── 1. Load all 3 CSV files ──────────────────────────────────────────
files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv",
]

dataframes = [pd.read_csv(f) for f in files]

# ── 2. Combine into one DataFrame ────────────────────────────────────
df = pd.concat(dataframes, ignore_index=True)

# ── 3. Filter for Pink Morsels only ──────────────────────────────────
df = df[df["product"] == "pink morsel"]

# ── 4. Clean price column and calculate sales ────────────────────────
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["price"] * df["quantity"]

# ── 5. Keep only required columns ────────────────────────────────────
df = df[["sales", "date", "region"]]

# ── 6. Save output ───────────────────────────────────────────────────
os.makedirs("output", exist_ok=True)
df.to_csv("output/output.csv", index=False)

print(f"Done! {len(df)} rows written to output/output.csv")
