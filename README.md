# Regressing video game characteristics to predict Steam video game review counts

## Authors

- Howard Song
- Milan Bertolutti
- Yuanchen Ling
- Maryamalsadat Hosseini

## About

This project investigates how well selected video game characteristics can predict the total number of reviews received by Steam games released between 2018 and 2022. The analysis uses the Steam Games Dataset published by FronkonGames on Hugging Face.

The project explores the relationships between review counts and game characteristics, including price, genres, Steam categories, supported languages, and release date. A linear regression model is developed and evaluated against a mean baseline to assess its predictive performance.

The results show that the linear regression model explains approximately one-third of the variation in log review counts on the test set and performs better than the mean baseline in cross-validation. However, the model is less accurate for games with very low or very high review counts. Since factors such as marketing activities, developer reputation, and community engagement are not included, the findings should be interpreted as predictive rather than causal.

## Report

The full analysis, including exploratory data analysis, model development, and evaluation, is available in the published report:

[View the Steam Games Analysis Report](https://ubc-mds-2026-27.github.io/DSCI-522-Group-13-Steam-Game-popularity-analysis/)

## Usage

The project uses Docker to provide a consistent and reproducible environment. The analysis runs inside a Docker container, so you do not need to install Python packages or Quarto locally. The image is published on Docker Hub at [milanbert/dsci-522-group-13-steam-game-popularity-analysis](https://hub.docker.com/r/milanbert/dsci-522-group-13-steam-game-popularity-analysis).

## Prerequisites

Before getting started, make sure you have the following installed:

- **Git** – to clone the project repository.
- **Docker Desktop** – to download and run the project container.

The project dependencies, Python environment, and Quarto are already configured inside the Docker image. You do not need to install Python or Quarto locally.

## Setup

### 1. Clone the repository

Clone the project repository and navigate to the project directory:

```bash
git clone https://github.com/UBC-MDS-2026-27/DSCI-522-Group-13-Steam-Game-popularity-analysis.git
cd DSCI-522-Group-13-Steam-Game-popularity-analysis
```

### 2. Set up an SSH key

Before downloading the Docker image, make sure you have an SSH key on your computer. If you do not already have one, open a terminal and run:

```bash
ssh-keygen -t ed25519
```

Press Enter at each prompt to accept the default settings.

If you skip this step, Docker may create a directory named `~/.ssh/id_ed25519.pub` instead of using an existing public key. This can cause SSH connection problems. If this happens, delete the incorrectly created directory and generate the SSH key using the command above.
Make sure `~/.gitconfig` exists as a file on your machine (and your Git name and email are configured) before starting the container, or Docker may create a directory at that path. Even though rendering the report does not use SSH directly, the `analysis-env` service in `docker-compose.yml` mounts both `~/.ssh/id_ed25519.pub` and `~/.gitconfig`, so both files must exist on your machine before running the container.

### 3. Download the Docker image

From the repository directory, download the project environment:

```bash
docker compose pull
```
The Docker image is approximately 190 MB. The initial download may take a few minutes depending on your internet connection.

### 4. Render the analysis report

Run the following command from the repository directory to render the Quarto report inside the Docker container:

```bash
docker compose run --rm analysis-env uv run quarto render analysis/videogames-regression.qmd
```

On the first run, rendering downloads the raw dataset from Hugging Face (so an internet connection is required) and saves local data files; raw data files are ignored by Git.
The rendered HTML report will be saved at `analysis/videogames-regression.html`.
The `--rm` option automatically removes the temporary container after the rendering command finishes. If you start the container in the background using `docker compose up -d`, stop and remove it when you finish by running `docker compose down`.

## Contributing

If you would like to contribute to this project, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on setting up the development environment, working with the Docker container, updating dependencies, reproducing the analysis, and publishing the report.

## Dependencies

The project environment is managed using Docker and includes the tools and packages required to reproduce the analysis.

The main tools used in the project include:

- **Python:** The project uses the Python version specified in `.python-version`.
- **uv:** Manages Python dependencies using `pyproject.toml` and `uv.lock`.
- **Quarto:** Renders the analysis report.
- **Docker:** Provides a consistent environment for running the project.

The exact Python package versions are managed through the project's dependency files to support reproducibility.

## AI Usage Statement

Generative AI tools, including Claude (Opus 5.5), were used throughout this project as an assistant rather than a guide: for debugging, documentation, code explanations, and brainstorming.

## References

FronkonGames. (n.d.). *Steam Games Dataset* [Data set]. Hugging Face. [https://doi.org/10.57967/hf/0511](https://doi.org/10.57967/hf/0511)

Valve. (n.d.). User reviews. *Steamworks Documentation*. [https://partner.steamgames.com/doc/store/reviews](https://partner.steamgames.com/doc/store/reviews)

## License

The code in this repository is licensed under the MIT License. The analysis report is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0). The dataset remains subject to its original source license.

For more information, see [LICENSE.md](LICENSE.md).
