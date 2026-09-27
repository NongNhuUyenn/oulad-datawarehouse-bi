from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

files = [
    "courses.csv",
    "assessments.csv",
    "vle.csv",
    "studentInfo.csv",
    "studentRegistration.csv",
    "studentAssessment.csv",
    "studentVle.csv"
]

summary = []

for file_name in files:

    file_path = DATA_DIR / file_name

    print("\n" + "=" * 80)
    print("FILE:", file_name)
    print("=" * 80)

    df = pd.read_csv(file_path)

    rows = df.shape[0]
    columns = df.shape[1]
    size_mb = file_path.stat().st_size / (1024 ** 2)

    print(f"Rows: {rows:,}")
    print(f"Columns: {columns}")
    print(f"Size: {size_mb:.2f} MB")

    print("\nCOLUMN NAMES")
    print(df.columns.tolist())

    print("\nDATA TYPES")
    print(df.dtypes)

    print("\nNULL VALUES")
    print(df.isnull().sum())

    print("\nUNIQUE VALUES")
    print(df.nunique())

    print("\nFIRST 5 ROWS")
    print(df.head())

    summary.append({
        "file": file_name,
        "rows": rows,
        "columns": columns,
        "size_mb": round(size_mb, 2),
        "total_null": int(df.isnull().sum().sum())
    })


summary_df = pd.DataFrame(summary)

Path("data/processed").mkdir(parents=True, exist_ok=True)

summary_df.to_csv(
    "data/processed/dataset_summary.csv",
    index=False
)

print("\n")
print("=" * 80)
print("FINAL SUMMARY")
print("=" * 80)

print(summary_df.to_string(index=False))