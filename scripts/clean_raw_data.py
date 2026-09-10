import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
for file_name in ["ADMISSIONS.csv", "PATIENTS.csv", "LABEVENTS.csv"]:
    path = RAW_DIR / file_name
    df = pd.read_csv(path, low_memory=False)
    
    # original rows have subject_id < 900000
    df_clean = df[df['subject_id'] < 900000]
    df_clean.to_csv(path, index=False)
    print(f"Cleaned {file_name}: {len(df)} -> {len(df_clean)} rows.")
