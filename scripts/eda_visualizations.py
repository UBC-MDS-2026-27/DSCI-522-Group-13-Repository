from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set file paths
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "train.csv"
OUTPUT_DIR = ROOT / "analysis" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load training data only
train = pd.read_csv(DATA_PATH)

print(f"Number of training games: {len(train):,}")


# --------------------------------------------------
# Figure 1: Distribution of total reviews
# --------------------------------------------------

# Log transformation handles zero-review games
log_reviews = np.log1p(train["total_reviews"])

fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(
    log_reviews,
    bins=60,
    edgecolor="white",
    linewidth=0.5
)

ax.set_title("Distribution of Total Reviews")
ax.set_xlabel("log(1 + Total Reviews) (unitless)")
ax.set_ylabel("Number of Games (games)")

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "review_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close(fig)


# --------------------------------------------------
# Figure 2: Reviews by supported languages
# --------------------------------------------------

# Group games by number of supported languages
bins = [-1, 0, 1, 3, 10, np.inf]
labels = ["0", "1", "2–3", "4–10", "11+"]

train["language_group"] = pd.cut(
    train["n_languages"],
    bins=bins,
    labels=labels
)

# Calculate median review count and group size
summary = (
    train.groupby("language_group", observed=False)
    ["total_reviews"]
    .agg(["median", "size"])
)

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    summary.index.astype(str),
    summary["median"]
)

# Display sample size above each bar
for bar, n in zip(bars, summary["size"]):
    ax.annotate(
        f"n={n:,}",
        (
            bar.get_x() + bar.get_width() / 2,
            bar.get_height()
        ),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center"
    )

ax.set_title("Median Total Reviews by Supported Languages")
ax.set_xlabel("Number of Supported Languages (languages per game)")
ax.set_ylabel("Median Total Reviews (reviews per game)")

ax.set_ylim(0, summary["median"].max() * 1.25)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "reviews_by_languages.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close(fig)

print("Both figures have been saved successfully.")