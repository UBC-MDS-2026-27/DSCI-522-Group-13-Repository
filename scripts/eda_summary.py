from pathlib import Path
import pandas as pd

# File paths
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "train.csv"
OUTPUT_DIR = ROOT / "analysis" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load training data only
train = pd.read_csv(DATA_PATH)

# Select relevant numerical variables
columns = ["price", "n_languages", "total_reviews"]

# Descriptive statistics
summary = train[columns].describe().T

summary = summary.rename(
    columns={
        "count": "N",
        "mean": "Mean",
        "std": "SD",
        "min": "Min",
        "25%": "Q1",
        "50%": "Median",
        "75%": "Q3",
        "max": "Max"
    }
)

summary = summary.rename(
    index={
        "price": "Price (USD)",
        "n_languages": "Supported languages (count)",
        "total_reviews": "Total reviews (count)"
    }
)

summary.index.name = "Variable"

# Save table
summary.round(2).to_csv(
    OUTPUT_DIR / "training_summary.csv"
)

print(summary.round(2))
