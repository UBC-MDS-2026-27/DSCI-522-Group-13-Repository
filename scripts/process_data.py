"""Download the Steam games dataset and produce the cleaned, split data (data contract v3).

Outputs (all in --processed-dir, default data/processed/):
    cleaned.csv      one row per game in the 2018-2022 cohort, contract columns only
    drop-ledger.csv  every dropped row with the reason it was dropped
    train.csv        80% of cleaned.csv (seed 1234)
    test.csv         20% of cleaned.csv (seed 1234)

Usage (from the repository root):

    uv run python scripts/process_data.py
    uv run python scripts/process_data.py --skip-download
"""

import json
import shutil
import urllib.request
from pathlib import Path

import click
import pandas as pd
from sklearn.model_selection import train_test_split

# Pin REVISION to a commit SHA from the dataset's "History" tab on Hugging Face
# so every run downloads the same bytes. "main" changes whenever the author updates the data.
REVISION = "main"
DATA_URL = (
    "https://huggingface.co/datasets/FronkonGames/steam-games-dataset/"
    f"resolve/{REVISION}/data/train-00000-of-00001.parquet"
)
RAW_FILENAME = "steam_games.parquet"

# --- Data contract v3 constants -------------------------------------------------
COHORT_START = pd.Timestamp("2018-01-01")
COHORT_END = pd.Timestamp("2022-12-31")
EXPECTED_COHORT_SIZE = 43_092
TEST_SIZE = 0.2
SEED = 1234
CLEANED_COLUMNS = [
    "appID",
    "name",
    "release_date",
    "price",
    "supported_languages",
    "categories",
    "genres",
    "n_languages",
    "total_reviews",
]
LIST_COLUMNS = ["supported_languages", "categories", "genres"]
RAW_COLUMNS_NEEDED = [
    "appID",
    "name",
    "release_date",
    "price",
    "supported_languages",
    "categories",
    "genres",
    "positive",
    "negative",
]


def download_data(url: str, dest: Path, force: bool = False) -> Path:
    """Download `url` to `dest`, skipping the download if `dest` already exists.

    Writes to a temporary `.part` file first, so an interrupted download
    never leaves a half-written file that looks complete.
    """
    if dest.exists() and not force:
        click.echo(
            f"Found {dest}; skipping download (use --force-download to refresh)."
        )
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    click.echo(f"Downloading {url}\n  -> {dest}")
    with urllib.request.urlopen(url) as response, open(tmp, "wb") as out:
        shutil.copyfileobj(response, out)
    tmp.replace(dest)
    return dest


def to_list(value) -> list:
    """Return a list-column cell as a plain Python list ([] for missing values)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    return list(value)


def clean_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply the contract's row drops in order and build the cleaned columns.

    Returns (cleaned, ledger). The ledger has one row per dropped game with
    columns appID, name, reason. The drops run in the contract's order, so
    each dropped row is counted under the first rule it fails.
    """
    missing = set(RAW_COLUMNS_NEEDED) - set(raw.columns)
    if missing:
        raise ValueError(f"Raw data is missing expected columns: {sorted(missing)}")

    df = raw[RAW_COLUMNS_NEEDED].copy()
    dropped = []

    def drop(mask: pd.Series, reason: str) -> pd.DataFrame:
        dropped.append(df.loc[mask, ["appID", "name"]].assign(reason=reason))
        return df.loc[~mask]

    # 1. Target inputs missing.
    df = drop(
        df["positive"].isna() | df["negative"].isna(), "positive/negative missing"
    )

    # 2. Duplicate appID: keep the first occurrence, drop the later ones.
    df = drop(df["appID"].duplicated(keep="first"), "duplicate appID")

    # 3. release_date unparseable.
    # format="mixed" accepts each row's own format (e.g. "Oct 21, 2008" or
    # "2008-10-21"); anything it cannot read becomes NaT.
    parsed = pd.to_datetime(df["release_date"], format="mixed", errors="coerce")
    df = df.assign(release_date=parsed)
    df = drop(df["release_date"].isna(), "release_date unparseable")

    # 4. Released outside the 2018-2022 cohort (both ends inclusive).
    in_cohort = df["release_date"].between(COHORT_START, COHORT_END)
    df = drop(~in_cohort, "released outside 2018-2022")

    # Target and derived count.
    df["total_reviews"] = (df["positive"] + df["negative"]).astype("int64")
    for col in LIST_COLUMNS:
        df[col] = df[col].map(to_list)
    # Uncapped count; the cap at 10 is applied when building the feature matrix.
    df["n_languages"] = df["supported_languages"].map(len)

    # CSV cannot hold lists, so store each list as a JSON string, e.g. ["Action", "Indie"].
    # Read back in Python with json.loads, or in R with jsonlite::fromJSON.
    for col in LIST_COLUMNS:
        df[col] = df[col].map(json.dumps)
    df["release_date"] = df["release_date"].dt.strftime("%Y-%m-%d")

    ledger = pd.concat(dropped, ignore_index=True)
    return df[CLEANED_COLUMNS].reset_index(drop=True), ledger


@click.command()
@click.option(
    "--url", default=DATA_URL, show_default=True, help="URL of the raw data file."
)
@click.option(
    "--raw-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("data/raw"),
    show_default=True,
    help="Directory to save the raw data in.",
)
@click.option(
    "--processed-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("data/processed"),
    show_default=True,
    help="Directory to write cleaned.csv, drop-ledger.csv, train.csv and test.csv to.",
)
@click.option(
    "--force-download", is_flag=True, help="Download again even if the raw file exists."
)
@click.option(
    "--skip-download", is_flag=True, help="Use the raw file already in --raw-dir."
)
@click.option(
    "--expected-cohort",
    type=int,
    default=EXPECTED_COHORT_SIZE,
    show_default=True,
    help="Stop if the cohort size differs from this (the data contract's number).",
)
def main(url, raw_dir, processed_dir, force_download, skip_download, expected_cohort):
    """Download the Steam games data, clean it to data contract v3, and split it."""
    raw_path = raw_dir / RAW_FILENAME
    if skip_download:
        if not raw_path.exists():
            raise click.ClickException(
                f"--skip-download was given but {raw_path} does not exist."
            )
    else:
        download_data(url, raw_path, force=force_download)

    raw = pd.read_parquet(raw_path)
    click.echo(f"Read {len(raw):,} rows from {raw_path}")

    cleaned, ledger = clean_data(raw)

    click.echo(f"Dropped {len(ledger):,} rows; kept {len(cleaned):,}:")
    for reason, n in ledger["reason"].value_counts(sort=False).items():
        click.echo(f"  {reason}: {n:,}")

    # Stop rather than warn: a different cohort means the data or the rules
    # changed, and the contract says neither may change silently.
    if len(cleaned) != expected_cohort:
        raise click.ClickException(
            f"Cohort has {len(cleaned):,} games but the data contract says "
            f"{expected_cohort:,}. Check REVISION and the release_date parsing rule."
        )

    train, test = train_test_split(cleaned, test_size=TEST_SIZE, random_state=SEED)

    processed_dir.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(processed_dir / "cleaned.csv", index=False)
    ledger.to_csv(processed_dir / "drop-ledger.csv", index=False)
    train.to_csv(processed_dir / "train.csv", index=False)
    test.to_csv(processed_dir / "test.csv", index=False)
    click.echo(
        f"Wrote cleaned.csv, drop-ledger.csv, train.csv ({len(train):,}) and test.csv ({len(test):,}) to {processed_dir}"
    )


if __name__ == "__main__":
    main()