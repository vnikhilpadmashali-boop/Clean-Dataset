# VINIX Task 3 – Clean a Dataset

This project cleans the supplied smartphone usage dataset (`1212.csv`) with Python and Pandas.

## Files
- `clean_dataset.py` — repeatable data-cleaning script.
- `data/1212.csv` — original uploaded dataset.
- `data/cleaned_dataset.csv` — cleaned output produced by the script.
- `cleaning_report.txt` — summary of cleaning operations and results.
- `requirements.txt` — Python dependency.

## Cleaning workflow
1. Standardize column names and trim text whitespace.
2. Convert expected numeric columns to numeric types.
3. Check reasonable ranges for age, daily hours, and phone unlock counts.
4. Remove exact duplicate rows and duplicate `User_ID` records (keeping the first).
5. Impute any remaining numeric missing values with the median and categorical missing values with the mode.
6. Flag potential numeric outliers with the IQR rule. Outliers are reported, not automatically removed, to avoid deleting valid observations.
7. Export the cleaned CSV and a text cleaning report.

## Run on Windows
Open Command Prompt in this project folder and run:

```bash
python -m pip install -r requirements.txt
python clean_dataset.py
```

## Dataset note
The source dataset contains smartphone usage fields such as screen time, social media hours, gaming hours, sleep hours, study hours, phone unlocks, and usage category. The script preserves valid records and documents cleaning decisions.
