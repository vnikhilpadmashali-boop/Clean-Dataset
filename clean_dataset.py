from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
INPUT = BASE / "data" / "1212.csv"
OUTPUT = BASE / "data" / "cleaned_dataset.csv"
REPORT = BASE / "cleaning_report.txt"

df = pd.read_csv(INPUT)
original_rows, original_columns = df.shape

# Standardize column names and text values.
df.columns = df.columns.str.strip()
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("string").str.strip()

# Remove fully duplicated records and duplicate user IDs (keep first occurrence).
duplicate_rows = int(df.duplicated().sum())
df = df.drop_duplicates()
duplicate_ids = int(df["User_ID"].duplicated().sum()) if "User_ID" in df.columns else 0
if "User_ID" in df.columns:
    df = df.drop_duplicates(subset=["User_ID"], keep="first")

# Convert expected numeric columns to numeric values; invalid text becomes missing.
numeric_columns = [
    "User_ID", "Age", "Screen_Time", "Social_Media_Hours", "Gaming_Hours",
    "Entertainment_Hours", "Education_Hours", "Other_App_Hours",
    "Sleep_Hours", "Study_Hours", "Phone_Unlocks"
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

missing_before = int(df.isna().sum().sum())

# Replace impossible values with missing values before imputing.
if "Age" in df.columns:
    df.loc[~df["Age"].between(0, 120), "Age"] = pd.NA

hour_columns = [
    "Screen_Time", "Social_Media_Hours", "Gaming_Hours",
    "Entertainment_Hours", "Education_Hours", "Other_App_Hours",
    "Sleep_Hours", "Study_Hours"
]
for col in hour_columns:
    if col in df.columns:
        df.loc[~df[col].between(0, 24), col] = pd.NA

if "Phone_Unlocks" in df.columns:
    df.loc[df["Phone_Unlocks"] < 0, "Phone_Unlocks"] = pd.NA

# Fill numeric missing values with the median and categorical missing values with the mode.
for col in df.select_dtypes(include="number").columns:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())

for col in df.select_dtypes(include=["object", "string", "category"]).columns:
    if df[col].isna().any():
        mode = df[col].mode(dropna=True)
        if not mode.empty:
            df[col] = df[col].fillna(mode.iloc[0])

missing_after = int(df.isna().sum().sum())

# Flag potential outliers using the IQR rule; do not delete them automatically.
outlier_counts = {}
for col in df.select_dtypes(include="number").columns:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr > 0:
        mask = (df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)
        outlier_counts[col] = int(mask.sum())

df.to_csv(OUTPUT, index=False)

lines = [
    "DATA CLEANING REPORT",
    "====================",
    f"Input file: {INPUT.name}",
    f"Rows before cleaning: {original_rows}",
    f"Columns before cleaning: {original_columns}",
    f"Exact duplicate rows removed: {duplicate_rows}",
    f"Duplicate User_ID records removed: {duplicate_ids}",
    f"Missing cells before handling: {missing_before}",
    f"Missing cells after handling: {missing_after}",
    f"Rows after cleaning: {len(df)}",
    f"Columns after cleaning: {len(df.columns)}",
    "",
    "Potential outliers (IQR rule; flagged, not automatically removed):"
]
lines.extend([f"- {col}: {count}" for col, count in outlier_counts.items()] or ["- None detected"])
lines += [
    "",
    "Cleaning steps: standardized column/text whitespace; converted expected numeric",
    "fields; checked reasonable age/hour/unlock ranges; removed duplicate records;",
    "filled remaining numeric missing values with medians and categorical missing",
    "values with modes; exported cleaned CSV."
]
REPORT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nSaved cleaned dataset: {OUTPUT}")
