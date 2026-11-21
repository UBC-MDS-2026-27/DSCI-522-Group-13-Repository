# Contributing to the DSCI 522 Group 13 Project

Thank you for contributing to our DSCI 522 Group 13 project! This project analyzes Steam video game data to explore relationships between game features and outcomes.

## Fixing Typos

Small spelling or grammatical errors in documentation can be fixed using GitHub. Please modify the original source files, such as `.md` or `.qmd`, rather than rendered HTML or PDF files.

## Reporting Bugs and Suggesting Improvements

Before making substantial changes, create a GitHub Issue to describe the problem or proposed improvement.

When reporting a bug, include:

- A clear description of the issue.
- Steps to reproduce the problem.
- Expected and actual results.
- Relevant error messages or screenshots.

Check existing issues before opening a new one.

## Setting Up the Project

Clone the repository:

```bash
git clone https://github.com/UBC-MDS-2026-27/DSCI-522-Group-13-Steam-Game-popularity-analysis.git
cd DSCI-522-Group-13-Steam-Game-popularity-analysis
```

Install the project dependencies using `uv`:

```bash
uv sync
```

Use the project's existing `pyproject.toml` and `uv.lock` to maintain a reproducible environment.

If additional packages are required, use `uv add <package>` and commit the updated dependency files.

## Data and Reproducibility

- Store downloaded raw data in `data/raw/`.
- Store cleaned datasets in `data/processed/`.
- Use the agreed 2018–2022 cohort and document any filtering decisions.
- Use an 80/20 train-test split with random seed 1234.
- Fit preprocessing transformations only on the training data to prevent data leakage.
- Document the steps needed to reproduce the analysis.
- Avoid committing large data files that exceed GitHub's file-size limits.

## Pull Request Process

1. Create a new branch from an up-to-date `main` branch.
2. Use a short, descriptive branch name, such as `add-eda-plot` or `fix-data-cleaning`.
3. Make changes and commit them with meaningful commit messages.
4. Push your branch to GitHub and open a Pull Request into `main`.
5. Describe your changes and link any relevant GitHub Issues.
6. Request a review from at least one teammate before merging.
7. The reviewer should merge the PR after approval. Contributors should not push directly to `main`.

Keep each PR focused on one task to make reviewing easier.

Python code should follow the PEP 8 style guide.

## AI Usage Policy

AI tools, including ChatGPT and GitHub Copilot, may be used to assist with debugging, documentation, code explanations, and brainstorming.

Contributors must:

- Understand and verify any AI-generated code or text before submitting it.
- Test AI-assisted code and ensure it works correctly.
- Disclose substantial AI assistance in the relevant PR or documentation.
- Follow UBC MDS academic integrity guidelines.
- Ensure all contributions are reviewed by a human team member before merging.
- Open, review and merge all issues and PRs.

Contributors remain responsible for the accuracy and quality of their work.

## Code of Conduct

All contributors are expected to follow the project's `CODE_OF_CONDUCT.md` and communicate respectfully with teammates.

## Attribution

These guidelines were adapted from the UBC MDS Breast Cancer Predictor contributing guidelines and adjusted for our DSCI 522 Group 13 project.
