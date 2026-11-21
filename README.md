# Regressing video game characteristics to predict Steam video game review counts

## Authors

- Howard Song
- Milan Bertolutti
- Yuanchen Ling	
- Maryamalsadat Hosseini	

## Summary


How well do game characteristics predict the total number of reviews for Steam games released 2018–2022? 

We aimed to answer this question using the [FronkonGames steam games dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset) to train a linear regression model using the features price, genre, category, language count and release date, compared against a mean baseline. Our trained model explains about one-third of the variance in log review counts on the test set and beats the mean baseline. This shows that game metadata carries useful predictive signal for developers/publishers, but it is predictive, not causal. One limitation of our model is that it is less accurate at very low and very high review counts. Features such as marketing, developer reputation, and community engagement are not taken into account within our model.


## How to run the analysis

These instructions were tested on macOS.
Run every command from the root of the repository.

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (installs Python 3.14 for you)
- [Quarto](https://quarto.org/docs/get-started/) 1.10 or later

### 1. Clone the repository

```bash
git clone https://github.com/UBC-MDS-2026-27/DSCI-522-Group-13-Repository
cd DSCI-522-Group-13-Repository
```

### 2. Set up the computational environment

```bash
uv sync
```

### 3. Download the data and run the analysis

Run these in order:

```bash
uv run python scripts/process_data.py
uv run python scripts/eda_summary.py
uv run python scripts/eda_visualizations.py
```

The first script downloads the dataset (about 190 MB) from Hugging Face to `data/raw/` and writes the cleaned and split data to `data/processed/`.
If the dataset is already downloaded, it skips the download.

### 4. Render the report

```bash
uv run quarto render analysis/videogames-regression.qmd
```

Rendering runs the model code in the report: it fits the regression, cross-validates it, and scores it on the test set.

### 5. View the report

The report is rendered to `analysis/videogames-regression.html`:

```bash
open analysis/videogames-regression.html    # macOS
start analysis/videogames-regression.html   # Windows
```

## Dependencies

- [uv](https://docs.astral.sh/uv/) 0.12 or later
- Python 3.14 (set in [`.python-version`](.python-version), installed by uv)
- [Quarto](https://quarto.org/) 1.10 or later
- Python packages listed in [`pyproject.toml`](pyproject.toml), with exact versions pinned in [`uv.lock`](uv.lock)

## License

- Code: MIT License
- Report: Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)

The data is not covered by either license and remains under the license of its original source.
See [`LICENSE.md`](LICENSE.md) for the full terms.

## AI use statement

Generative AI tools, including Claude (Opus 5.5), were used throughout this project as an assistant rather than a guide: for debugging, documentation, code explanations, and brainstorming.
All AI-assisted work was reviewed, tested, and verified by a team member before merging, following the AI usage policy in [`CONTRIBUTING.md`](CONTRIBUTING.md#ai-usage-policy).
Substantial AI contributions are cited in the code where they were used, for example in [`analysis/videogames-regression.qmd`](analysis/videogames-regression.qmd).

Instruction files: none are committed to this repository.

Example prompts:

- Verify the model training pipeline I have written for any issues. Does it align with the outlined question and data contract?
- Verify that my implementation of a log1p() and other transformation is correct here.
- I am having some trouble formatting this expression into LaTeX, correct the equation.

## Rendered report

https://ubc-mds-2026-27.github.io/DSCI-522-Group-13-Repository/
