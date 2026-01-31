# src/load_data.py
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_raw() -> pd.DataFrame:
    """
    Load the Kaggle xAPI-Edu-Data dataset.
    Tries CSV first; if it fails, tries Excel.
    """
    # Your file name from the upload
    f_csv_like = RAW_DIR / "xAPI-Edu-Data.csv"

    # Try reading as CSV (because file content appears CSV-like)
    try:
        df = pd.read_csv(f_csv_like)
        return df
    except Exception:
        # Fallback: try Excel with xlrd/openpyxl
        try:
            df = pd.read_excel(f_csv_like, engine="xlrd")
            return df
        except Exception as e:
            raise RuntimeError(f"Could not load raw data: {e}")

def save_processed(df: pd.DataFrame, name: str = "xapi_edu_processed.csv") -> Path:
    out_path = PROCESSED_DIR / name
    df.to_csv(out_path, index=False)
    return out_path

def load_processed(name: str = "xapi_edu_processed.csv") -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / name)