from pathlib import Path
import pandas as pd


BASE_DIR = Path(_file_).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


def load_csv(filename):
    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{file_path}"
        )

    return pd.read_csv(file_path)